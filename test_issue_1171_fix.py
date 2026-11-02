#!/usr/bin/env python3
"""
Test script for Issue #1171 - Fix dante-ev/latex-action version reference
Validates that all GitHub Actions workflows use the correct dante-ev/latex-action@v0.2.0
and include comprehensive German language support packages.
"""

import sys
import yaml
import re
from pathlib import Path


def test_latex_action_migration():
    """Test that all workflows have been migrated from xu-cheng to dante-ev latex action."""
    print("[SYNC] Testing LaTeX Action Migration")
    print("=" * 60)

    workflow_dir = Path(".github/workflows")
    if not workflow_dir.exists():
        print("[FAIL] .github/workflows directory not found")
        return False

    found_issues = False
    workflows_checked = 0
    dante_ev_usage = 0
    xu_cheng_usage = 0

    # Check all workflow files
    for workflow_file in workflow_dir.glob("*.yml"):
        workflows_checked += 1
        print(f"\n[TEST] Checking {workflow_file.name}...")

        try:
            with open(workflow_file, 'r') as f:
                content = f.read()

            # Check for xu-cheng/latex-action (should be removed)
            xu_cheng_matches = re.findall(r'xu-cheng/latex-action@([^\s\n]+)', content)
            if xu_cheng_matches:
                xu_cheng_usage += len(xu_cheng_matches)
                print(f"  [FAIL] Found xu-cheng/latex-action references: {xu_cheng_matches}")
                found_issues = True
            else:
                print(f"  [PASS] No xu-cheng/latex-action references found")

            # Check for dante-ev/latex-action@v0.2.0 (should be present)
            dante_ev_matches = re.findall(r'dante-ev/latex-action@([^\s\n]+)', content)
            if dante_ev_matches:
                dante_ev_usage += len(dante_ev_matches)
                print(f"  [PACKAGE] Found dante-ev/latex-action references: {dante_ev_matches}")

                # Validate version is v0.2.0
                for version in dante_ev_matches:
                    if version == "v0.2.0":
                        print(f"  [PASS] Version {version} is correct")
                    else:
                        print(f"  [FAIL] Version {version} is incorrect (should be v0.2.0)")
                        found_issues = True

        except Exception as e:
            print(f"[FAIL] Error reading {workflow_file}: {e}")
            found_issues = True

    # Summary
    print(f"\n[SUMMARY] Migration Summary")
    print("=" * 60)
    print(f"Workflows checked: {workflows_checked}")
    print(f"xu-cheng/latex-action usage: {xu_cheng_usage}")
    print(f"dante-ev/latex-action usage: {dante_ev_usage}")

    if xu_cheng_usage > 0:
        print("[FAIL] FAILED: xu-cheng/latex-action still found in workflows")
        found_issues = True
    else:
        print("[PASS] PASSED: No xu-cheng/latex-action references found")

    if dante_ev_usage > 0:
        print("[PASS] PASSED: dante-ev/latex-action references found")
    else:
        print("[WARN]  WARNING: No dante-ev/latex-action references found")

    return not found_issues


def test_german_language_support():
    """Test that workflows include comprehensive German language support packages."""
    print("\n[EMOJI][EMOJI] Testing German Language Support")
    print("=" * 60)

    workflow_dir = Path(".github/workflows")
    required_packages = {
        'texlive-lang-german',
        'texlive-fonts-recommended',
        'texlive-latex-recommended',
        'texlive-fonts-extra',
        'texlive-latex-extra',
        'texlive-science',
        'texlive-pstricks',
        'ghostscript'
    }

    found_issues = False
    workflows_with_latex = []

    # Check all workflow files with dante-ev/latex-action
    for workflow_file in workflow_dir.glob("*.yml"):
        try:
            with open(workflow_file, 'r') as f:
                content = f.read()

            if 'dante-ev/latex-action' in content:
                workflows_with_latex.append(workflow_file.name)
                print(f"\n[TEST] Checking {workflow_file.name}...")

                # Simple check - ensure all required packages are present somewhere after extra_system_packages
                found_packages = set()
                for package in required_packages:
                    if package in content:
                        found_packages.add(package)

                print(f"  [PACKAGE] Found packages: {sorted(found_packages)}")

                missing_packages = required_packages - found_packages
                if missing_packages:
                    print(f"  [FAIL] Missing packages: {sorted(missing_packages)}")
                    found_issues = True
                else:
                    print(f"  [PASS] All required packages present")

        except Exception as e:
            print(f"[FAIL] Error processing {workflow_file}: {e}")
            found_issues = True

    # Summary
    print(f"\n[SUMMARY] German Language Support Summary")
    print("=" * 60)
    print(f"Workflows with LaTeX action: {len(workflows_with_latex)}")
    print(f"Required packages: {sorted(required_packages)}")

    if not found_issues:
        print("[PASS] PASSED: All workflows have complete German language support")
    else:
        print("[FAIL] FAILED: Some workflows missing required packages")

    return not found_issues


def test_workflow_yaml_validity():
    """Test that all modified workflow files are valid YAML."""
    print("\n[NOTE] Testing YAML Validity")
    print("=" * 60)

    workflow_dir = Path(".github/workflows")
    found_issues = False
    workflows_checked = 0

    for workflow_file in workflow_dir.glob("*.yml"):
        workflows_checked += 1
        print(f"\n[TEST] Validating {workflow_file.name}...")

        try:
            with open(workflow_file, 'r') as f:
                yaml.safe_load(f)
            print(f"  [PASS] Valid YAML syntax")

        except yaml.YAMLError as e:
            print(f"  [FAIL] YAML syntax error: {e}")
            found_issues = True
        except Exception as e:
            print(f"  [FAIL] Error reading file: {e}")
            found_issues = True

    print(f"\n[SUMMARY] YAML Validation Summary")
    print("=" * 60)
    print(f"Workflows checked: {workflows_checked}")

    if not found_issues:
        print("[PASS] PASSED: All workflows have valid YAML syntax")
    else:
        print("[FAIL] FAILED: Some workflows have YAML syntax errors")

    return not found_issues


def main():
    """Run all validation tests for Issue #1171 fix."""
    print("[TEST] Issue #1171 Fix Validation")
    print("Fix GitHub Actions dante-ev/latex-action version and German language support")
    print("=" * 80)

    all_tests_passed = True

    # Run tests
    tests = [
        ("LaTeX Action Migration", test_latex_action_migration),
        ("German Language Support", test_german_language_support),
        ("YAML Validity", test_workflow_yaml_validity)
    ]

    for test_name, test_func in tests:
        try:
            result = test_func()
            if not result:
                all_tests_passed = False
        except Exception as e:
            print(f"[FAIL] Test '{test_name}' failed with exception: {e}")
            all_tests_passed = False

    # Final summary
    print("\n" + "=" * 80)
    if all_tests_passed:
        print("[SUCCESS] ALL TESTS PASSED - Issue #1171 fix validated successfully!")
        print("[PASS] GitHub Actions workflows now use dante-ev/latex-action@v0.2.0")
        print("[PASS] Comprehensive German language support packages included")
        print("[PASS] CI should now build successfully with German LaTeX support")
        return 0
    else:
        print("[FAIL] SOME TESTS FAILED - Issue #1171 fix needs attention")
        return 1


if __name__ == "__main__":
    sys.exit(main())
