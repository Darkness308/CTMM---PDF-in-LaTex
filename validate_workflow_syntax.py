#!/usr/bin/env python3
"""
GitHub Actions YAML Syntax Validation for Issue #458

This script validates that the GitHub Actions workflow files have the correct
syntax to prevent YAML boolean interpretation of the 'on:' keyword.

The issue: Unquoted 'on:' gets parsed as boolean True instead of string "on"
The fix: Quote the keyword as "on:" to ensure string interpretation
"""

import yaml
import os
from pathlib import Path
import sys

def validate_workflow_syntax():
    """Validate GitHub Actions workflow files for correct on: syntax."""

    print("=" * 70)
    print("GitHub Actions YAML Syntax Validation - Issue #458")
    print("=" * 70)

    # Define the workflow files to check
    workflow_files = [
        '.github/workflows/latex-build.yml',
        '.github/workflows/latex-validation.yml',
        '.github/workflows/static.yml'
    ]

    print(f"\nChecking {len(workflow_files)} workflow files...")

    all_correct = True
    results = []

    for file_path in workflow_files:
        if not os.path.exists(file_path):
            print(f"[FAIL] File not found: {file_path}")
            all_correct = False
            continue

        print(f"\n--- Analyzing {file_path} ---")

        # Read the file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find the 'on:' line
        lines = content.split('\n')
        on_lines = []
        for i, line in enumerate(lines, 1):
            if '"on":' in line:
                on_lines.append((i, line.strip(), 'quoted'))
            elif line.strip().startswith('on:'):
                on_lines.append((i, line.strip(), 'unquoted'))

        if not on_lines:
            print("[FAIL] No 'on:' trigger found in workflow")
            all_correct = False
            continue

        # Parse the YAML
        try:
            parsed = yaml.safe_load(content)

            # Check if 'on' is interpreted correctly
            if 'on' in parsed and isinstance(parsed['on'], dict):
                print("[PASS] 'on' correctly interpreted as string key")
                print(f"  Line {on_lines[0][0]}: {on_lines[0][1]}")
                print(f"  Triggers: {list(parsed['on'].keys())}")

                # Validate trigger structure
                triggers = parsed['on']
                if 'push' in triggers or 'pull_request' in triggers or 'workflow_dispatch' in triggers:
                    print("[PASS] Valid trigger configuration found")
                else:
                    print("[WARN]  No standard triggers (push/pull_request/workflow_dispatch) found")

                results.append((file_path, True, "Correct quoted syntax"))

            elif True in parsed:
                print("[FAIL] 'on' incorrectly interpreted as boolean True")
                print(f"  Line {on_lines[0][0]}: {on_lines[0][1]}")
                print("  This causes GitHub Actions parsing errors")
                all_correct = False
                results.append((file_path, False, "Incorrect unquoted syntax causing boolean interpretation"))

            else:
                print("[QUESTION] Unexpected parsing result - no 'on' or True key found")
                all_correct = False
                results.append((file_path, False, "Unexpected parsing result"))

        except yaml.YAMLError as e:
            print(f"[FAIL] YAML parsing error: {e}")
            all_correct = False
            results.append((file_path, False, f"YAML error: {e}"))

    # Summary
    print("\n" + "=" * 70)
    print("VALIDATION SUMMARY")
    print("=" * 70)

    for file_path, is_correct, message in results:
        status = "[PASS] PASS" if is_correct else "[FAIL] FAIL"
        print(f"{status} {os.path.basename(file_path)}: {message}")

    if all_correct:
        print("\n[SUCCESS] ALL WORKFLOW FILES HAVE CORRECT SYNTAX")
        print("The 'on:' keyword is properly quoted to prevent boolean interpretation.")
        print("GitHub Actions will correctly parse these workflow triggers.")
    else:
        print("\n[WARN]  SOME WORKFLOW FILES NEED FIXING")
        print("Files with unquoted 'on:' should be changed to quoted '\"on\":' syntax.")

    print(f"\nStatus: {'SUCCESS' if all_correct else 'NEEDS_FIXES'}")
    return all_correct

def demonstrate_yaml_issue():
    """Demonstrate the YAML boolean interpretation issue."""

    print("\n" + "=" * 70)
    print("DEMONSTRATION: YAML Boolean Interpretation Issue")
    print("=" * 70)

    # Example with unquoted 'on:' (problematic)
    problematic_yaml = """
name: Example Workflow
on:
  push:
    branches: [main]
jobs:
  test:
    runs-on: ubuntu-latest
"""

    # Example with quoted '"on":' (correct)
    correct_yaml = """
name: Example Workflow
"on":
  push:
    branches: [main]
jobs:
  test:
    runs-on: ubuntu-latest
"""

    print("\n1. PROBLEMATIC: Unquoted 'on:' syntax")
    print("-" * 40)
    print("YAML content:")
    print(problematic_yaml.strip())

    try:
        parsed = yaml.safe_load(problematic_yaml)
        print(f"\nParsed keys: {list(parsed.keys())}")
        print(f"Key types: {[(k, type(k).__name__) for k in parsed.keys()]}")

        if True in parsed:
            print("[FAIL] PROBLEM: 'on' became boolean True")
            print(f"  Triggers accessible via parsed[True]: {parsed[True]}")
        else:
            print("[PASS] No boolean interpretation issue found")

    except Exception as e:
        print(f"[FAIL] Error: {e}")

    print("\n2. CORRECT: Quoted '\"on\":' syntax")
    print("-" * 40)
    print("YAML content:")
    print(correct_yaml.strip())

    try:
        parsed = yaml.safe_load(correct_yaml)
        print(f"\nParsed keys: {list(parsed.keys())}")
        print(f"Key types: {[(k, type(k).__name__) for k in parsed.keys()]}")

        if 'on' in parsed:
            print("[PASS] CORRECT: 'on' is string key")
            print(f"  Triggers accessible via parsed['on']: {parsed['on']}")
        else:
            print("[FAIL] Expected 'on' key not found")

    except Exception as e:
        print(f"[FAIL] Error: {e}")

if __name__ == "__main__":
    # Change to repository root
    repo_root = Path(__file__).parent
    os.chdir(repo_root)

    print("Repository path:", os.getcwd())

    # Run validation
    all_correct = validate_workflow_syntax()

    # Demonstrate the issue
    demonstrate_yaml_issue()

    # Exit with appropriate code
    sys.exit(0 if all_correct else 1)
