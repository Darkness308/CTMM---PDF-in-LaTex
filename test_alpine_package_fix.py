#!/usr/bin/env python3
"""
Test for Alpine Package Error Fix (Issue: Remove extra_system_packages)

This test validates that the latex-build.yml workflow file:
1. Does not contain extra_system_packages configuration
2. Uses xu-cheng/latex-action@v3 correctly
3. Has proper YAML structure
"""

import yaml
import os
import sys

def test_latex_build_workflow():
    """Test that latex-build.yml does not have extra_system_packages."""

    workflow_file = '.github/workflows/latex-build.yml'

    print("=" * 70)
    print("Testing Alpine Package Error Fix")
    print("=" * 70)

    if not os.path.exists(workflow_file):
        print(f"[FAIL] Workflow file not found: {workflow_file}")
        return False

    # Read the workflow file
    with open(workflow_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Parse YAML
    try:
        workflow = yaml.safe_load(content)
    except yaml.YAMLError as e:
        print(f"[FAIL] YAML parsing error: {e}")
        return False

    print(f"[PASS] Successfully parsed {workflow_file}")

    # Find the "Set up LaTeX" step
    latex_setup_step = None
    for job_name, job_config in workflow['jobs'].items():
        if 'steps' in job_config:
            for step in job_config['steps']:
                if 'name' in step and 'Set up LaTeX' in step['name']:
                    latex_setup_step = step
                    break

    if not latex_setup_step:
        print("[FAIL] 'Set up LaTeX' step not found in workflow")
        return False

    print("[PASS] Found 'Set up LaTeX' step")

    # Check if the step uses xu-cheng/latex-action@v3
    if 'uses' not in latex_setup_step:
        print("[FAIL] 'uses' field not found in LaTeX setup step")
        return False

    if 'xu-cheng/latex-action@v3' not in latex_setup_step['uses']:
        print(f"[WARN]  Warning: Using action {latex_setup_step['uses']}, expected xu-cheng/latex-action@v3")
    else:
        print("[PASS] Using xu-cheng/latex-action@v3")

    # Check if extra_system_packages is present (it should NOT be)
    if 'with' in latex_setup_step:
        with_config = latex_setup_step['with']

        if 'extra_system_packages' in with_config:
            print("[FAIL] FAIL: extra_system_packages found in LaTeX setup step")
            print("  This will cause Alpine package errors!")
            print(f"  Found packages: {with_config['extra_system_packages']}")
            return False
        else:
            print("[PASS] No extra_system_packages configuration (correct)")

    # Verify required fields are present
    required_fields = ['root_file', 'args']
    if 'with' not in latex_setup_step:
        print("[FAIL] 'with' configuration missing")
        return False

    with_config = latex_setup_step['with']
    missing_fields = [field for field in required_fields if field not in with_config]

    if missing_fields:
        print(f"[FAIL] Missing required fields in 'with': {missing_fields}")
        return False

    print(f"[PASS] Required fields present: {required_fields}")
    print(f"  root_file: {with_config['root_file']}")
    print(f"  args: {with_config['args']}")

    # Check timeout
    if 'timeout-minutes' in latex_setup_step:
        timeout = latex_setup_step['timeout-minutes']
        print(f"[PASS] Timeout configured: {timeout} minutes")
        if timeout < 10:
            print("[WARN]  Warning: Timeout might be too short for LaTeX compilation")

    print("\n" + "=" * 70)
    print("[PASS] ALL TESTS PASSED - Workflow configuration is correct")
    print("=" * 70)
    return True

if __name__ == "__main__":
    success = test_latex_build_workflow()
    sys.exit(0 if success else 1)
