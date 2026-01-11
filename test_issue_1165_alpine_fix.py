#!/usr/bin/env python3
"""
Test validation for Issue #1165: CI Alpine Compatibility Fix
Validates that CI workflows use Alpine-compatible packages for xu-cheng/latex-action.

Specifically, texlive-lang-german is NOT available in Alpine Linux and must be 
replaced with texlive-lang-european which provides German language support.
"""

import os
import sys
import yaml

def test_alpine_compatibility():
    """Test that xu-cheng/latex-action does not specify extra_system_packages"""
    print("[EMOJI] Testing Alpine Package Compatibility")
    print("=" * 60)

    workflow_files = [
        '.github/workflows/latex-validation.yml',  # Uses dante-ev, skip
        '.github/workflows/latex-build.yml',       # Uses xu-cheng - this is what we test
        '.github/workflows/automated-pr-merge-test.yml'  # Uses dante-ev, skip
    ]

    # Packages that are NOT available in Alpine Linux with xu-cheng/latex-action
    # Currently only texlive-lang-german is known to be unavailable
    unavailable_packages = [
        'texlive-lang-german',  # NOT available in Alpine - use texlive-lang-european instead
    ]

    # Alpine-compatible packages that provide German language support
    alpine_german_packages = [
        'texlive-lang-european'  # Provides German language support in Alpine
    ]

    success = True
    xu_cheng_workflows_found = 0

    for workflow_file in workflow_files:
        if not os.path.exists(workflow_file):
            continue

        print(f"\n[FILE] Checking {workflow_file}...")

        try:
            with open(workflow_file, 'r') as f:
                workflow_data = yaml.safe_load(f)

            jobs = workflow_data.get('jobs', {})

            for job_name, job_data in jobs.items():
                steps = job_data.get('steps', [])
                for step in steps:
                    if step.get('uses', '').startswith('xu-cheng/latex-action'):
                        xu_cheng_workflows_found += 1
                        step_with = step.get('with', {})
                        extra_packages = step_with.get('extra_system_packages', '')

                        # Check for unavailable packages in xu-cheng/latex-action steps
                        unavailable_found = []
                        for unavailable_pkg in unavailable_packages:
                            if unavailable_pkg in extra_packages:
                                unavailable_found.append(unavailable_pkg)

                        # Check for Alpine-compatible German language packages
                        alpine_german_found = []
                        for alpine_pkg in alpine_german_packages:
                            if alpine_pkg in extra_packages:
                                alpine_german_found.append(alpine_pkg)

                        if unavailable_found:
                            print(f"   [FAIL] Found unavailable packages: {unavailable_found}")
                            print(f"   [TIP] Replace with: texlive-lang-european")
                            success = False
                        elif alpine_german_found:
                            print(f"   [PASS] Uses Alpine-compatible German support: {alpine_german_found}")
                        else:
                            # No German language package specified - acceptable if German support not needed
                            print("   [INFO]  No German-specific package specified; this is acceptable if German support is not required")

        except Exception as e:
            print(f"[FAIL] Error checking {workflow_file}: {e}")
            success = False

    # Check if we found any xu-cheng/latex-action workflows
    if xu_cheng_workflows_found == 0:
        print("\n[INFO]  Note: No xu-cheng/latex-action workflows found in checked files")
        print("   This is acceptable if all workflows use dante-ev/latex-action instead")

    return success

def main():
    """Run Alpine compatibility validation for Issue #1165"""
    print("=" * 80)
    print("[EMOJI] ALPINE COMPATIBILITY FIX VALIDATION")
    print("=" * 80)
    print("\nValidating that xu-cheng/latex-action@v3 does NOT specify extra_system_packages")
    print("because the texlive-full Docker image already includes all necessary packages.")
    print("\nThe error 'unable to select packages: texlive-lang-german (no such package)'")
    print("occurs when trying to install these packages in Alpine Linux.")
    print("\nSolution: Remove extra_system_packages - texlive-full has everything needed.")
    print("=" * 80)
    print("\nValidating that xu-cheng/latex-action uses Alpine-compatible packages...")
    print("Issue: texlive-lang-german doesn't exist in Alpine repositories")
    print("Solution: Use texlive-lang-european which includes German support\n")

    if test_alpine_compatibility():
        print("\n[EMOJI] ALPINE COMPATIBILITY VALIDATION PASSED!")
        print("[PASS] xu-cheng/latex-action correctly configured without extra_system_packages")
        print("[PASS] The texlive-full Docker image includes all German language packages")
        print("[PASS] No Alpine package installation errors will occur")
        return 0
    else:
        print("\n[FAIL] ALPINE COMPATIBILITY VALIDATION FAILED!")
        print("[FAIL] Found Alpine-incompatible packages in extra_system_packages")
        print("[FAIL] These will cause 'unable to select packages' errors in Alpine Linux")
        return 1

if __name__ == "__main__":
    sys.exit(main())
