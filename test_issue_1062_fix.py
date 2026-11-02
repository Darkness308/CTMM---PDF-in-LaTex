#!/usr/bin/env python3
"""
Test script for Issue #1062: Fix dante-ev/latex-action version reference
Validates that workflows use valid dante-ev/latex-action versions.
"""

import yaml
import sys
from pathlib import Path

def test_latex_action_versions():
    """Test that all workflow files use valid dante-ev/latex-action versions."""
    print("[FIX] Testing dante-ev/latex-action versions")
    print("=" * 60)

    # Valid versions from dante-ev/latex-action repository
    valid_versions = {
        'v0.2.0',  # Latest semantic version
        'v0.1.0',  # Older semantic version
        '2025-A',  # Latest year-based
        '2024-B',  # Older year-based
        '2024-A',  # Even older year-based
        '2023-A',
        '2021-C',
        '2021-B',
        '2021-A',
        '2020-A',
        '2019-A'
    }

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

                    if version in valid_versions:
                        print(f"  [PASS] Version {version} is valid")
                    else:
                        print(f"  [FAIL] Version {version} is INVALID")
                        print(f"  Valid versions: {', '.join(sorted(valid_versions))}")
                        found_issues = True

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
        status = "[PASS] VALID" if ref['version'] in valid_versions else "[FAIL] INVALID"
        print(f"  {ref['file']}:{ref['line']} - {ref['version']} - {status}")

    if found_issues:
        print("\n[FAIL] FOUND INVALID VERSIONS - CI will fail")
        return False
    else:
        print("\n[PASS] ALL VERSIONS ARE VALID - CI should work")
        return True


def test_specific_version_fix():
    """Test that the specific problematic version v2.3.0 is not present."""
    print("\n[TARGET] Testing for specific issue: v2.3.0 removal")
    print("=" * 60)

    problematic_version = "v2.3.0"
    workflow_dir = Path(".github/workflows")

    found_problematic = False

    for workflow_file in workflow_dir.glob("*.yml"):
        with open(workflow_file, 'r') as f:
            content = f.read()

        if f'dante-ev/latex-action@{problematic_version}' in content:
            print(f"[FAIL] Found problematic version {problematic_version} in {workflow_file.name}")
            found_problematic = True

    if found_problematic:
        print(f"[FAIL] FAILED: Problematic version {problematic_version} still present")
        return False
    else:
        print(f"[PASS] PASSED: Problematic version {problematic_version} successfully removed")
        return True


def main():
    """Main test function."""
    print("[TEST] Issue #1062 Fix Validation")
    print("Fix dante-ev/latex-action version references in GitHub Actions workflows")
    print("=" * 70)

    all_tests_passed = True

    # Test 1: Check all versions are valid
    if not test_latex_action_versions():
        all_tests_passed = False

    # Test 2: Check specific problematic version is removed
    if not test_specific_version_fix():
        all_tests_passed = False

    print("\n" + "=" * 70)
    if all_tests_passed:
        print("[SUCCESS] ALL TESTS PASSED - Issue #1062 fix validated successfully!")
        return 0
    else:
        print("[FAIL] TESTS FAILED - Issue #1062 fix needs more work")
        return 1


if __name__ == "__main__":
    sys.exit(main())
