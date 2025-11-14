FROM gcr.io/kaggle-gpu-images/python:latest

RUN apt-get clean && apt-get update && apt-get install -y \  
    curl \  
    vim \  
    git \  
    build-essential \
    strace \
    && rm -rf /var/lib/apt/lists/*

# Ensure required Python tooling is present in the runtime container
RUN python -m pip install --no-cache-dir --upgrade pip && \
    python -m pip install --no-cache-dir coverage pandas

# Create paths expected by RD-Agent generated code when running in the container.
# They point back into the workspace mount so any file written there is persisted.
RUN mkdir -p /home && ln -s /kaggle/workspace /home/submission && \
    ln -s /kaggle/workspace /home/code && \
    ln -s /kaggle/workspace /home/logs
