#!/usr/bin/env python3
"""
Final validation for GitHub Issue #532 - GitHub Actions YAML Syntax Fix

This script validates that all GitHub Actions workflow files use the correct
quoted "on": syntax to prevent YAML boolean interpretation issues.

Issue: Single quotes or unquoted 'on' keywords were causing YAML parsers to
misinterpret the trigger keyword as a boolean value instead of a string.

Solution: All workflow files now use double-quoted "on": syntax.
"""

import yaml
import os
import sys
from pathlib import Path

def validate_issue_532_fix():
    """Validate that Issue #532 (GitHub Actions YAML syntax) is fully resolved."""

    print("=" * 80)
    print("GITHUB ISSUE #532 - YAML SYNTAX VALIDATION")
    print("=" * 80)
    print("Validating that all GitHub Actions workflow files use correct syntax")
    print("to prevent YAML boolean interpretation of the 'on' keyword.\n")

    # Define expected workflow files
    workflow_files = [
        '.github/workflows/latex-build.yml',
        '.github/workflows/latex-validation.yml',
        '.github/workflows/static.yml'
    ]

    print(f"Checking {len(workflow_files)} workflow files...\n")

    all_correct = True
    validation_results = []

    for file_path in workflow_files:
        print(f"[SEARCH] Validating {os.path.basename(file_path)}")
        print("-" * 50)

        if not os.path.exists(file_path):
            print(f"[FAIL] File not found: {file_path}")
            all_correct = False
            validation_results.append((file_path, False, "File not found"))
            continue

        # Read and parse the file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        try:
            # Parse YAML content
            parsed = yaml.safe_load(content)

            # Check if 'on' key exists as string (correct)
            if 'on' in parsed and isinstance(parsed['on'], dict):
                print("[PASS] Correct: 'on' keyword parsed as string")

                # Verify trigger configuration
                triggers = parsed['on']
                trigger_types = list(triggers.keys())
                print(f"[PASS] Triggers configured: {trigger_types}")

                # Find the actual line with "on": in the file
                lines = content.split('\n')
                on_line = None
                for i, line in enumerate(lines, 1):
                    if '"on":' in line:
                        on_line = i
                        print(f"[PASS] Quoted syntax found on line {i}: {line.strip()}")
                        break

                if on_line:
                    validation_results.append((file_path, True, "Correct quoted syntax"))
                else:
                    print("[WARN]  Warning: Could not find quoted 'on': syntax in file")
                    validation_results.append((file_path, False, "Quoted syntax not found"))
                    all_correct = False

            elif True in parsed:
                print("[FAIL] ERROR: 'on' keyword interpreted as boolean True")
                print("  This indicates unquoted 'on:' syntax causing YAML boolean interpretation")
                all_correct = False
                validation_results.append((file_path, False, "Boolean interpretation detected"))

            else:
                print("[FAIL] ERROR: No 'on' trigger configuration found")
                all_correct = False
                validation_results.append((file_path, False, "No trigger configuration"))

        except yaml.YAMLError as e:
            print(f"[FAIL] YAML parsing error: {e}")
            all_correct = False
            validation_results.append((file_path, False, f"YAML error: {e}"))

        print()  # Empty line for readability

    # Summary
    print("=" * 80)
    print("VALIDATION SUMMARY")
    print("=" * 80)

    for file_path, is_correct, message in validation_results:
        status = "[PASS] PASS" if is_correct else "[FAIL] FAIL"
        filename = os.path.basename(file_path)
        print(f"{status} {filename}: {message}")

    print()

    if all_correct:
        print("[SUCCESS] ISSUE #532 RESOLUTION: SUCCESS")
        print("[PASS] All GitHub Actions workflow files have correct syntax")
        print("[PASS] The 'on' keyword is properly quoted to prevent boolean interpretation")
        print("[PASS] GitHub Actions will correctly parse all workflow triggers")
        print("[PASS] No YAML boolean interpretation issues detected")
        print("\n[TEST] STATUS: ISSUE #532 FULLY RESOLVED")
    else:
        print("[WARN]  ISSUE #532 RESOLUTION: INCOMPLETE")
        print("[FAIL] Some workflow files still have incorrect syntax")
        print("[FIX] Action needed: Fix files with unquoted 'on:' to use '\"on\":' syntax")

    print("=" * 80)
    return all_correct

def demonstrate_yaml_issue():
    """Demonstrate the YAML boolean interpretation issue and its solution."""

    print("\nDEMONSTRATION: YAML Boolean Interpretation Issue")
    print("=" * 80)

    # Problematic example (what Issue #532 was about)
    problematic_yaml = '''
name: Example Workflow
on:
  push:
    branches: [main]
jobs:
  test:
    runs-on: ubuntu-latest
'''

    # Correct example (the fix for Issue #532)
    correct_yaml = '''
name: Example Workflow
"on":
  push:
    branches: [main]
jobs:
  test:
    runs-on: ubuntu-latest
'''

    print("1. PROBLEMATIC: Unquoted 'on:' (causes Issue #532)")
    print("-" * 60)
    try:
        parsed = yaml.safe_load(problematic_yaml)
        print(f"Parsed keys: {list(parsed.keys())}")
        print(f"Key types: {[(k, type(k).__name__) for k in parsed.keys()]}")

        if True in parsed:
            print("[FAIL] PROBLEM: 'on' became boolean True - GitHub Actions won't recognize this!")

    except Exception as e:
        print(f"Error: {e}")

    print("\n2. CORRECT: Quoted \"on\": (Issue #532 solution)")
    print("-" * 60)
    try:
        parsed = yaml.safe_load(correct_yaml)
        print(f"Parsed keys: {list(parsed.keys())}")
        print(f"Key types: {[(k, type(k).__name__) for k in parsed.keys()]}")

        if 'on' in parsed and isinstance(parsed['on'], dict):
            print("[PASS] SUCCESS: 'on' is string key - GitHub Actions will work correctly!")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Ensure we're in the repository root
    if not Path('.github/workflows').exists():
        print("Error: This script must be run from the repository root directory")
        print("Expected to find .github/workflows/ directory")
        sys.exit(1)

    # Run validation
    success = validate_issue_532_fix()

    # Demonstrate the issue and solution
    demonstrate_yaml_issue()

    # Exit with appropriate code
    sys.exit(0 if success else 1)
