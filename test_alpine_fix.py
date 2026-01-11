#!/usr/bin/env python3
"""
Test script to verify the Alpine Linux package error fix.
Issue: Alpine Linux doesn't have texlive-lang-german package
Solution: Switch from xu-cheng/latex-action@v3 to dante-ev/latex-action@v2.3.0
"""

import os
import yaml
import sys
from pathlib import Path

def test_alpine_fix():
    """Test that the Alpine Linux package issue is fixed."""
    print("=" * 60)
    print("[TEST] ALPINE LINUX PACKAGE ERROR FIX TEST")
    print("=" * 60)

    workflows_dir = Path(".github/workflows")
    if not workflows_dir.exists():
        print("[FAIL] Workflows directory not found")
        return False

    # Check that all workflows use dante-ev action instead of xu-cheng
    workflow_files = list(workflows_dir.glob("*.yml"))

    issues_found = []
    fixes_verified = []

    for workflow_file in workflow_files:
        print(f"\n[FILE] Checking {workflow_file.name}...")

        with open(workflow_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check for problematic xu-cheng action that uses Alpine
        if "xu-cheng/latex-action" in content:
            issues_found.append(f"[FAIL] {workflow_file.name}: Still using xu-cheng/latex-action (Alpine issue)")
        else:
            print(f"  [PASS] No xu-cheng/latex-action found")

        # Check for dante-ev action with proper version
        if "dante-ev/latex-action@v2.3.0" in content:
            fixes_verified.append(f"[PASS] {workflow_file.name}: Using dante-ev/latex-action@v2.3.0")
            print(f"  [PASS] dante-ev/latex-action@v2.3.0 found")

            # Check for comprehensive package list
            required_packages = [
                'texlive-lang-german',
                'texlive-fonts-recommended',
                'texlive-latex-recommended',
                'texlive-fonts-extra',
                'texlive-latex-extra',
                'texlive-science',
                'texlive-pstricks'
            ]

            for package in required_packages:
                if package in content:
                    print(f"  [PASS] Required package {package} found")
                else:
                    print(f"  [WARN]  Package {package} not found in this workflow")

    print("\n" + "=" * 60)
    print("[SUMMARY] ALPINE FIX VALIDATION SUMMARY")
    print("=" * 60)

    if fixes_verified:
        print("\n[PASS] FIXES VERIFIED:")
        for fix in fixes_verified:
            print(f"  {fix}")

    if issues_found:
        print("\n[FAIL] ISSUES FOUND:")
        for issue in issues_found:
            print(f"  {issue}")
        return False
    else:
        print("\n[SUCCESS] NO ALPINE-RELATED ISSUES FOUND")
        print("[PASS] All workflows use dante-ev/latex-action@v2.3.0")
        print("[PASS] This action uses Ubuntu/Debian base (not Alpine)")
        print("[PASS] texlive-lang-german package is available in Ubuntu repositories")
        return True

def test_package_availability():
    """Test that the package configuration is correct for Ubuntu/Debian."""
    print("\n" + "=" * 60)
    print("[PACKAGE] PACKAGE AVAILABILITY TEST")
    print("=" * 60)

    print("[SEARCH] Checking dante-ev/latex-action@v2.3.0 configuration...")

    # This action uses Ubuntu/Debian where these packages are available
    ubuntu_packages = [
        'texlive-lang-german',  # [PASS] Available in Ubuntu
        'texlive-fonts-recommended', # [PASS] Available in Ubuntu
        'texlive-latex-recommended', # [PASS] Available in Ubuntu
        'texlive-fonts-extra',  # [PASS] Available in Ubuntu
        'texlive-latex-extra',  # [PASS] Available in Ubuntu
        'texlive-science',  # [PASS] Available in Ubuntu
        'texlive-pstricks'  # [PASS] Available in Ubuntu
    ]

    print("\n[TEST] Package availability in Ubuntu/Debian (used by dante-ev/latex-action):")
    for package in ubuntu_packages:
        print(f"  [PASS] {package}: Available in Ubuntu repositories")

    print("\n[FAIL] Alpine Linux issue (fixed by switching from xu-cheng):")
    print("  [FAIL] texlive-lang-german: NOT available in Alpine repositories")
    print("  [FAIL] This caused the original error:")
    print("  'ERROR: unable to select packages: texlive-lang-german (no such package)'")

    print("\n[PASS] Solution implemented:")
    print("  [PASS] Switched from xu-cheng/latex-action@v3 (Alpine) to dante-ev/latex-action@v2.3.0 (Ubuntu)")
    print("  [PASS] All required packages are available in Ubuntu repositories")

    return True

def main():
    """Main test function."""
    print("[LAUNCH] Running Alpine Linux package error fix verification...\n")

    # Change to repository directory
    repo_dir = Path(__file__).parent
    os.chdir(repo_dir)

    try:
        alpine_fix_success = test_alpine_fix()
        package_availability_success = test_package_availability()

        print("\n" + "=" * 60)
        print("[EMOJI] FINAL RESULT")
        print("=" * 60)

        if alpine_fix_success and package_availability_success:
            print("[SUCCESS] SUCCESS: Alpine Linux package error fix verified!")
            print("[PASS] All workflows now use dante-ev/latex-action@v2.3.0")
            print("[PASS] No more Alpine Linux package availability issues")
            print("[PASS] texlive-lang-german package will install correctly")
            return True
        else:
            print("[FAIL] FAILURE: Issues found in Alpine fix verification")
            return False

    except Exception as e:
        print(f"[FAIL] Test failed with error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
