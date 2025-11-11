from typing import Literal

from docker.errors import DockerException
from loguru import logger

from rdagent.app.data_science.conf import DS_RD_SETTING
from rdagent.components.coder.CoSTEER.config import CoSTEERSettings
from rdagent.utils.env import (
    CondaConf,
    DockerEnv,
    DSDockerConf,
    Env,
    LocalEnv,
    MLEBDockerConf,
    MLECondaConf,
)


class DSCoderCoSTEERSettings(CoSTEERSettings):
    """Data Science CoSTEER settings"""

    class Config:
        env_prefix = "DS_Coder_CoSTEER_"

    max_seconds_multiplier: int = 4
    env_type: str = "docker"
    # TODO: extract a function for env and conf.
    extra_evaluator: list[str] = []
    """Extra evaluators to use"""

    extra_eval: list[str] = []
    """
    Extra evaluators

    The evaluator follows the following assumptions:
    - It runs after previous evaluator (So the running results are already there)

    It is not a complete feature due to it is only implemented in DS Pipeline & Coder.

    TODO: The complete version should be implemented in the CoSTEERSettings.
    """


def get_ds_env(
    conf_type: Literal["kaggle", "mlebench"] = "kaggle",
    extra_volumes: dict = {},
    running_timeout_period: int | None = DS_RD_SETTING.debug_timeout,
    enable_cache: bool | None = None,
) -> Env:
    """
    Retrieve the appropriate environment configuration based on the env_type setting.

    Returns:
        Env: An instance of the environment configured either as DockerEnv or LocalEnv.

    Raises:
        ValueError: If the env_type is not recognized.
    """
    conf = DSCoderCoSTEERSettings()
    assert conf_type in ["kaggle", "mlebench"], f"Unknown conf_type: {conf_type}"

    def _create_env(env_kind: str) -> Env:
        if env_kind == "docker":
            env_conf = DSDockerConf() if conf_type == "kaggle" else MLEBDockerConf()
            return DockerEnv(conf=env_conf)
        if env_kind == "conda":
            return LocalEnv(
                conf=(
                    CondaConf(conda_env_name=conf_type)
                    if conf_type == "kaggle"
                    else MLECondaConf(conda_env_name=conf_type)
                )
            )
        raise ValueError(f"Unknown env type: {env_kind}")

    env_type: Literal["docker", "conda"] = conf.env_type  # type: ignore[assignment]

    while True:
        env = _create_env(env_type)
        env.conf.extra_volumes = extra_volumes.copy()
        env.conf.running_timeout_period = running_timeout_period
        if enable_cache is not None:
            env.conf.enable_cache = enable_cache
        try:
            env.prepare()
            return env
        except (DockerException, FileNotFoundError) as exc:
            if env_type != "docker":
                raise
            logger.warning(
                "Docker unavailable when preparing data science environment; falling back to conda. Error: {}",
                exc,
            )
            env_type = "conda"


def get_clear_ws_cmd(stage: Literal["before_training", "before_inference"] = "before_training") -> str:
    """
    Clean the files in workspace to a specific stage
    """
    assert stage in ["before_training", "before_inference"], f"Unknown stage: {stage}"
    if DS_RD_SETTING.enable_model_dump and stage == "before_training":
        cmd = "rm -r submission.csv scores.csv models trace.log"
    else:
        cmd = "rm submission.csv scores.csv trace.log"
    return cmd
