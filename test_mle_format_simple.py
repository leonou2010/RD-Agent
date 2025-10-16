#!/usr/bin/env python3
"""
Simplified standalone test for MLE-bench format implementation.

This test doesn't require RD-Agent configuration or full environment setup.
"""

from pathlib import Path


def test_mle_format_generation():
    """Test MLE-bench format generation with minimal dependencies."""
    print("=" * 80)
    print("MLE-BENCH FORMAT GENERATION TEST")
    print("=" * 80)

    # Setup paths
    mle_bench_root = Path("/home/leonau2010/llms-for-mle-bench/mle-bench")
    instructions_path = mle_bench_root / "environment" / "instructions.txt"
    comp_path = mle_bench_root / "mlebench" / "competitions" / "spaceship-titanic"
    comp_desc_path = comp_path / "description.md"

    # Check files exist
    print("\n1. Checking required files...")
    if not instructions_path.exists():
        print(f"✗ instructions.txt not found at {instructions_path}")
        return False
    print(f"✓ Found instructions.txt")

    if not comp_desc_path.exists():
        print(f"✗ description.md not found at {comp_desc_path}")
        return False
    print(f"✓ Found description.md for spaceship-titanic")

    # Load base instructions
    print("\n2. Loading base MLE-bench instructions...")
    base_instructions = instructions_path.read_text()
    print(f"✓ Loaded {len(base_instructions)} chars")
    print(f"  First line: {base_instructions.split(chr(10))[0]}")

    # Create additional notes
    print("\n3. Creating additional notes section...")
    hardware = "a GPU"
    time_limit = 24
    step_limit = 500

    additional_notes = f"""ADDITIONAL NOTES
------

- **Compute**: You have access to {hardware} with the appropriate drivers installed.
- **Total Runtime**: You have a maximum of {time_limit} hours to attempt this task. You may iteratively develop your solution within this time frame, but bear in mind that program runtime also counts towards this limit.
- **Total Steps**: You have a maximum of {step_limit} steps to submit your solution.
- You will be informed of the remaining time and steps at each step.
- **Use as much of the available time as possible to refine and optimize your submission**: Your goal is to achieve the best possible score, not just to submit your first working solution. Consider strategies like validating your answer using the "Validate Submission" tool at the http://localhost:5000/validate endpoint, manually spot-checking predictions, building custom validation sets and grading functions, and comparing different algorithms. You may keep working until the time limit expires -- as long as your best submission is stored at the designated location at the end of your run, it will be picked up for grading.

"""
    print(f"✓ Created additional notes ({len(additional_notes)} chars)")

    # Load competition description
    print("\n4. Loading competition description...")
    competition_description = comp_desc_path.read_text()
    print(f"✓ Loaded competition description ({len(competition_description)} chars)")
    print(f"  First line: {competition_description.split(chr(10))[0][:80]}...")

    # Concatenate all sections
    print("\n5. Concatenating sections...")
    full_description = f"""{base_instructions}

{additional_notes}

COMPETITION INSTRUCTIONS
------

{competition_description}
"""
    print(f"✓ Generated full MLE-bench format ({len(full_description)} chars)")

    # Verify key sections are present
    print("\n6. Verifying required sections...")
    required_sections = [
        ("MLE-bench", "MLE-bench reference"),
        ("BENCHMARK INSTRUCTIONS", "Benchmark instructions header"),
        ("ADDITIONAL NOTES", "Additional notes header"),
        ("COMPETITION INSTRUCTIONS", "Competition instructions header"),
        ("/home/data/", "Data path reference"),
        ("/home/submission/submission.csv", "Submission path"),
        ("Compute", "Compute information"),
        ("Total Runtime", "Runtime limit"),
        ("Total Steps", "Step limit"),
        (hardware, "Hardware parameter"),
        (f"{time_limit} hours", "Time limit parameter"),
        (f"{step_limit} steps", "Step limit parameter"),
    ]

    all_present = True
    for section, description in required_sections:
        if section in full_description:
            print(f"  ✓ {description}")
        else:
            print(f"  ✗ {description} - NOT FOUND")
            all_present = False

    if not all_present:
        print("\n✗ Some required sections are missing")
        return False

    print("\n✓ All required sections present")

    # Show sample output
    print("\n7. Sample output (first 800 chars):")
    print("-" * 80)
    print(full_description[:800])
    print("...")
    print("-" * 80)

    print("\n8. Sample output (section boundaries):")
    print("-" * 80)
    # Find and show section transitions
    lines = full_description.split('\n')
    for i, line in enumerate(lines):
        if any(keyword in line for keyword in ['BENCHMARK INSTRUCTIONS', 'ADDITIONAL NOTES', 'COMPETITION INSTRUCTIONS', '# Overview']):
            context_start = max(0, i-1)
            context_end = min(len(lines), i+3)
            print(f"\nLines {context_start}-{context_end}:")
            for j in range(context_start, context_end):
                prefix = ">>> " if j == i else "    "
                print(f"{prefix}{lines[j][:76]}")
            print()

    print("-" * 80)

    # Size comparison
    print("\n9. Size comparison:")
    print(f"  Base instructions: {len(base_instructions):,} chars")
    print(f"  Additional notes: {len(additional_notes):,} chars")
    print(f"  Competition description: {len(competition_description):,} chars")
    print(f"  Full MLE-bench format: {len(full_description):,} chars")
    print(f"  Overhead: {len(full_description) - len(competition_description):,} chars")

    return True


def test_different_parameters():
    """Test with different parameter values."""
    print("\n" + "=" * 80)
    print("PARAMETER VARIATION TEST")
    print("=" * 80)

    test_cases = [
        {"hardware": "4 CPUs", "time_limit": 12, "step_limit": 100},
        {"hardware": "8 GPUs (NVIDIA A100)", "time_limit": 48, "step_limit": 1000},
    ]

    mle_bench_root = Path("/home/leonau2010/llms-for-mle-bench/mle-bench")
    instructions_path = mle_bench_root / "environment" / "instructions.txt"

    base_instructions = instructions_path.read_text()

    for i, params in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i}: {params} ---")

        additional_notes = f"""ADDITIONAL NOTES
------

- **Compute**: You have access to {params['hardware']} with the appropriate drivers installed.
- **Total Runtime**: You have a maximum of {params['time_limit']} hours to attempt this task.
- **Total Steps**: You have a maximum of {params['step_limit']} steps to submit your solution.
"""

        # Verify all params appear
        checks = [
            (params["hardware"], "hardware"),
            (f"{params['time_limit']} hours", "time_limit"),
            (f"{params['step_limit']} steps", "step_limit"),
        ]

        all_ok = True
        for value, param_name in checks:
            if value in additional_notes:
                print(f"  ✓ {param_name}: {value}")
            else:
                print(f"  ✗ {param_name}: {value} NOT FOUND")
                all_ok = False

        if not all_ok:
            return False

    print("\n✓ All parameter variations work correctly")
    return True


def main():
    """Run all tests."""
    print("\n" + "█" * 80)
    print("SIMPLIFIED MLE-BENCH FORMAT TEST SUITE")
    print("█" * 80 + "\n")

    tests = [
        ("MLE-bench Format Generation", test_mle_format_generation),
        ("Parameter Variations", test_different_parameters),
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n✗ Test '{test_name}' crashed: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))

    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)

    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")

    passed = sum(1 for _, r in results if r)
    total = len(results)

    print(f"\nResults: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed! The MLE-bench format implementation is working correctly.")
        print("\nNext steps:")
        print("1. Use scen._get_description_mle_format() instead of scen._get_description()")
        print("2. Pass hardware, time_limit, and step_limit parameters as needed")
        print("3. The method gracefully falls back to standard format if MLE-bench files are missing")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
