#!/usr/bin/env python3
"""
Test GitHub Actions workflow files for proper structure and syntax.
"""

import yaml
import os
import json

def test_workflow_files():
    """Test each workflow file for GitHub Actions compatibility."""

    workflow_files = [
        '.github/workflows/latex-build.yml',
        '.github/workflows/latex-validation.yml',
        '.github/workflows/static.yml',
        '.github/workflows/pr-validation.yml',
        '.github/workflows/automated-pr-merge-test.yml'
    ]

    print("Testing GitHub Actions workflow file structure...")
    print("=" * 60)

    for file_path in workflow_files:
        print(f"\n[SEARCH] Testing {os.path.basename(file_path)}")
        print("-" * 40)

        with open(file_path, 'r') as f:
            content = f.read()

        try:
            # Parse YAML
            workflow = yaml.safe_load(content)

            # Required fields check
            required_fields = ['name', 'on', 'jobs']
            missing_fields = [field for field in required_fields if field not in workflow]

            if missing_fields:
                print(f"[FAIL] Missing required fields: {missing_fields}")
                continue

            print(f"[PASS] Name: {workflow['name']}")

            # Check triggers
            triggers = workflow['on']
            if isinstance(triggers, dict):
                print(f"[PASS] Triggers: {list(triggers.keys())}")

                # Validate common trigger types
                for trigger_type in triggers:
                    if trigger_type in ['push', 'pull_request']:
                        trigger_config = triggers[trigger_type]
                        if isinstance(trigger_config, dict) and 'branches' in trigger_config:
                            print(f"   {trigger_type}: {trigger_config['branches']}")
                        else:
                            print(f"   {trigger_type}: {trigger_config}")
                    elif trigger_type == 'workflow_dispatch':
                        print(f"   {trigger_type}: manual trigger enabled")
                    else:
                        print(f"   {trigger_type}: {triggers[trigger_type]}")
            else:
                print(f"[FAIL] Invalid triggers format: {type(triggers)}")
                continue

            # Check jobs
            jobs = workflow['jobs']
            if isinstance(jobs, dict):
                print(f"[PASS] Jobs: {list(jobs.keys())}")

                for job_name, job_config in jobs.items():
                    if 'runs-on' in job_config:
                        print(f"   {job_name}: {job_config['runs-on']}")
                    else:
                        print(f"   {job_name}: missing runs-on")
            else:
                print(f"[FAIL] Invalid jobs format: {type(jobs)}")
                continue

            print("[PASS] Workflow structure is valid")

        except yaml.YAMLError as e:
            print(f"[FAIL] YAML parsing error: {e}")
        except Exception as e:
            print(f"[FAIL] Error: {e}")

if __name__ == "__main__":
    test_workflow_files()
