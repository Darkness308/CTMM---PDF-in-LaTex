#!/usr/bin/env python3
"""
Test Issue #1036 Fix: GitHub Actions LaTeX Build Failure - Action Version Resolution

This test validates that invalid dante-ev/latex-action versions (@v2, @v2.0.0)
have been updated to @latest in all GitHub Actions workflows.

Author: GitHub Copilot
Date: 2024
"""

import os
import re
import yaml
from pathlib import Path


def test_latex_action_version_fix():
    """Test that all dante-ev/latex-action references use @latest version."""
    print("[FIX] Testing dante-ev/latex-action version fix")
    print("=" * 60)

    workflow_dir = Path(".github/workflows")
    if not workflow_dir.exists():
        print("[FAIL] .github/workflows directory not found")
        return False

    found_issues = False
    latex_action_references = []

    # Check all workflow files
    for workflow_file in workflow_dir.glob("*.yml"):
        print(f"\n[TEST] Checking {workflow_file.name}...")

        try:
            with open(workflow_file, 'r') as f:
                content = f.read()

            # Look for dante-ev/latex-action references
            lines = content.split('\n')
            for line_num, line in enumerate(lines, 1):
                if 'dante-ev/latex-action@' in line:
                    # Extract the version
                    version_start = line.find('dante-ev/latex-action@') + len('dante-ev/latex-action@')
                    remaining = line[version_start:]
                    version = remaining.split()[0].rstrip()  # Get first word and remove trailing chars

                    latex_action_references.append({
                        'file': workflow_file.name,
                        'line': line_num,
                        'version': version,
                        'line_content': line.strip()
                    })

                    print(f"  Line {line_num}: Found dante-ev/latex-action@{version}")

                    # Check for problematic versions that should have been fixed
                    if version in ['v2', 'v2.0.0', 'v2.3.0']:
                        print(f"  [FAIL] Version {version} is problematic (should be @latest)")
                        found_issues = True
                    elif version == 'latest':
                        print(f"  [PASS] Version {version} is correct")
                    else:
                        print(f"  [WARN]  Version {version} - verify this is intentional")

        except Exception as e:
            print(f"[FAIL] Error reading {workflow_file}: {e}")
            found_issues = True

    # Summary
    print(f"\n[SUMMARY] Summary")
    print("=" * 60)
    print(f"Total dante-ev/latex-action references found: {len(latex_action_references)}")

    if not latex_action_references:
        print("[WARN]  No dante-ev/latex-action references found")
        return True

    print("\nAll references:")
    for ref in latex_action_references:
        status = "[PASS] FIXED" if ref['version'] == 'latest' else "[FAIL] NEEDS_FIX"
        print(f"  {ref['file']}:{ref['line']} - {ref['version']} - {status}")

    if found_issues:
        print("\n[FAIL] FOUND PROBLEMATIC VERSIONS - Fix needed")
        return False
    else:
        print("\n[PASS] ALL VERSIONS ARE CORRECT - Issue #1036 resolved")
        return True


def test_removal_of_problematic_versions():
    """Test that specific problematic versions mentioned in Issue #1036 are removed."""
    print("\n[TARGET] Testing removal of problematic versions (@v2, @v2.0.0)")
    print("=" * 60)

    workflow_dir = Path(".github/workflows")
    problematic_versions = ['@v2', '@v2.0.0', '@v2.3.0']
    found_problematic = []

    for workflow_file in workflow_dir.glob("*.yml"):
        try:
            with open(workflow_file, 'r') as f:
                content = f.read()

            for version in problematic_versions:
                if f'dante-ev/latex-action{version}' in content:
                    found_problematic.append(f"{workflow_file.name}: {version}")
                    print(f"[FAIL] Found problematic version {version} in {workflow_file.name}")

        except Exception as e:
            print(f"[FAIL] Error reading {workflow_file}: {e}")
            return False

    if found_problematic:
        print(f"\n[FAIL] FAILED: Found {len(found_problematic)} problematic version(s)")
        for item in found_problematic:
            print(f"  - {item}")
        return False
    else:
        print("\n[PASS] PASSED: No problematic versions found")
        return True


def test_workflow_yaml_syntax():
    """Test that workflow YAML files have valid syntax after the changes."""
    print("\n[TEST] Testing workflow YAML syntax")
    print("=" * 60)

    workflow_dir = Path(".github/workflows")
    syntax_errors = []

    for workflow_file in workflow_dir.glob("*.yml"):
        print(f"  Validating {workflow_file.name}...")

        try:
            with open(workflow_file, 'r') as f:
                content = f.read()

            # Parse YAML to check syntax
            yaml.safe_load(content)
            print(f"  [PASS] {workflow_file.name} - Valid YAML syntax")

        except yaml.YAMLError as e:
            syntax_errors.append(f"{workflow_file.name}: {e}")
            print(f"  [FAIL] {workflow_file.name} - YAML syntax error: {e}")
        except Exception as e:
            syntax_errors.append(f"{workflow_file.name}: {e}")
            print(f"  [FAIL] {workflow_file.name} - Error: {e}")

    if syntax_errors:
        print(f"\n[FAIL] FAILED: Found {len(syntax_errors)} syntax error(s)")
        for error in syntax_errors:
            print(f"  - {error}")
        return False
    else:
        print("\n[PASS] PASSED: All workflow files have valid YAML syntax")
        return True


def test_action_configuration_completeness():
    """Test that LaTeX action configurations include all required parameters."""
    print("\n[GEAR]  Testing LaTeX action configuration completeness")
    print("=" * 60)

    workflow_dir = Path(".github/workflows")
    config_issues = []

    for workflow_file in workflow_dir.glob("*.yml"):
        try:
            with open(workflow_file, 'r') as f:
                content = f.read()

            if 'dante-ev/latex-action@' in content:
                print(f"  Checking configuration in {workflow_file.name}...")

                # Check for required parameters
                required_params = ['root_file', 'args']
                missing_params = []

                for param in required_params:
                    if f'{param}:' not in content:
                        missing_params.append(param)

                if missing_params:
                    config_issues.append(f"{workflow_file.name}: Missing {', '.join(missing_params)}")
                    print(f"  [FAIL] Missing required parameters: {', '.join(missing_params)}")
                else:
                    print(f"  [PASS] All required parameters present")

                # Check for recommended extra_system_packages
                if 'extra_system_packages:' in content:
                    print(f"  [PASS] Extra system packages configured")
                else:
                    print(f"  [WARN]  No extra system packages specified (may cause build issues)")

        except Exception as e:
            config_issues.append(f"{workflow_file.name}: {e}")
            print(f"  [FAIL] Error checking {workflow_file}: {e}")

    if config_issues:
        print(f"\n[WARN]  Found {len(config_issues)} configuration issue(s)")
        for issue in config_issues:
            print(f"  - {issue}")
        return False
    else:
        print("\n[PASS] PASSED: All LaTeX action configurations are complete")
        return True


def main():
    """Run all tests for Issue #1036 fix validation."""
    print("[TEST] Issue #1036 Fix Validation")
    print("Fix dante-ev/latex-action version references in GitHub Actions workflows")
    print("=" * 70)

    tests = [
        ("LaTeX Action Version Fix", test_latex_action_version_fix),
        ("Removal of Problematic Versions", test_removal_of_problematic_versions),
        ("Workflow YAML Syntax", test_workflow_yaml_syntax),
        ("Action Configuration Completeness", test_action_configuration_completeness),
    ]

    passed_tests = 0
    total_tests = len(tests)

    for test_name, test_func in tests:
        print(f"\n{'='*70}")
        print(f"[TEST] TEST: {test_name}")
        print(f"{'='*70}")

        try:
            if test_func():
                print(f"[PASS] {test_name}: PASS")
                passed_tests += 1
            else:
                print(f"[FAIL] {test_name}: FAIL")
        except Exception as e:
            print(f"[FAIL] {test_name}: ERROR - {e}")

    print(f"\n{'='*70}")
    print(f"[SUMMARY] TEST SUMMARY")
    print(f"{'='*70}")
    print(f"Tests passed: {passed_tests}/{total_tests}")

    if passed_tests == total_tests:
        print("[SUCCESS] ALL TESTS PASSED! LaTeX action version issue resolved.")
        return True
    else:
        print("[FAIL] SOME TESTS FAILED - Issue #1036 fix needs more work")
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
