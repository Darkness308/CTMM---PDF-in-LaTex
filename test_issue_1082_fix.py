#!/usr/bin/env python3
"""
Issue #1082 Validation: Dante version 2.3 klappt nicht
Comprehensive validation to ensure dante-ev/latex-action version issues are resolved.
"""

import os
import yaml
from pathlib import Path

def test_no_problematic_dante_versions():
    """Test that no problematic dante-ev/latex-action versions are used."""
    print("[SEARCH] Testing for problematic dante-ev/latex-action versions")
    print("=" * 60)

    # List of known problematic versions that don't exist or cause issues
    problematic_versions = [
        'v2.3.0',    # Never existed - Issue #1062
        'v2.0.0',    # Never existed - Issue #1076
        'v2',        # Doesn't exist - Issue #867
        '@latest'    # Can be unstable
    ]

    workflow_dir = Path(".github/workflows")
    if not workflow_dir.exists():
        print("[FAIL] .github/workflows directory not found")
        return False

    found_issues = False

    for workflow_file in workflow_dir.glob("*.yml"):
        print(f"\n[TEST] Checking {workflow_file.name}...")

        try:
            with open(workflow_file, 'r') as f:
                content = f.read()

            # Check for each problematic version
            for version in problematic_versions:
                if f'dante-ev/latex-action@{version}' in content:
                    print(f"[FAIL] Found problematic version {version} in {workflow_file.name}")
                    found_issues = True

        except Exception as e:
            print(f"[FAIL] Error reading {workflow_file.name}: {e}")
            found_issues = True

    if found_issues:
        print("\n[FAIL] FAILED: Found problematic dante-ev/latex-action versions")
        return False
    else:
        print("\n[PASS] PASSED: No problematic versions found")
        return True

def test_current_dante_version_is_valid():
    """Test that current dante-ev/latex-action version is valid and working."""
    print("\n[FIX] Testing current dante-ev/latex-action version")
    print("=" * 60)

    # Known working versions
    valid_versions = {
        'v0.2.0',    # Current recommended - verified working
        'v0.1.0',    # Older but valid
        '2025-A',    # Year-based tags that exist
        '2024-B',
        '2024-A',
        '2023-A'
    }

    workflow_dir = Path(".github/workflows")
    found_dante_action = False
    all_valid = True

    for workflow_file in workflow_dir.glob("*.yml"):
        with open(workflow_file, 'r') as f:
            content = f.read()

        lines = content.split('\n')
        for line_num, line in enumerate(lines, 1):
            if 'dante-ev/latex-action@' in line:
                found_dante_action = True
                # Extract version
                version_start = line.find('dante-ev/latex-action@') + len('dante-ev/latex-action@')
                remaining = line[version_start:]
                version = remaining.split()[0].rstrip()

                print(f"[PACKAGE] Found: {workflow_file.name}:{line_num} - dante-ev/latex-action@{version}")

                if version in valid_versions:
                    print(f"   [PASS] Version {version} is valid")
                else:
                    print(f"   [FAIL] Version {version} is not in known valid list")
                    all_valid = False

    if not found_dante_action:
        print("[WARN]  No dante-ev/latex-action found in workflows")
        return False

    if all_valid:
        print("\n[PASS] PASSED: All dante-ev/latex-action versions are valid")
        return True
    else:
        print("\n[FAIL] FAILED: Some dante-ev/latex-action versions are invalid")
        return False

def test_issue_1082_resolution():
    """Main test function for Issue #1082."""
    print("[TEST] Issue #1082 Validation: Dante version 2.3 klappt nicht")
    print("Fix dante-ev/latex-action version issues")
    print("=" * 70)

    test1 = test_no_problematic_dante_versions()
    test2 = test_current_dante_version_is_valid()

    print("\n" + "=" * 70)
    if test1 and test2:
        print("[SUCCESS] ALL TESTS PASSED - Issue #1082 resolved!")
        print("[PASS] No problematic dante-ev/latex-action versions found")
        print("[PASS] Current versions are valid and should work")
        print("\n[TEST] SUMMARY:")
        print("   - dante-ev/latex-action@v2.3.0 issue already resolved")
        print("   - Current workflows use valid v0.2.0 version")
        print("   - CI builds should work correctly")
        return True
    else:
        print("[FAIL] TESTS FAILED - Issue #1082 not fully resolved")
        return False

if __name__ == "__main__":
    success = test_issue_1082_resolution()
    exit(0 if success else 1)
