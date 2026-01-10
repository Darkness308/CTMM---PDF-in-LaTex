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
    """Test that xu-cheng/latex-action uses Alpine-compatible packages"""
    print("🧪 Testing Alpine Package Compatibility")
    print("=" * 60)

    workflow_files = [
        '.github/workflows/latex-validation.yml',
        '.github/workflows/latex-build.yml',
        '.github/workflows/automated-pr-merge-test.yml'
    ]

    # Packages that are NOT available in Alpine Linux with xu-cheng/latex-action
    # Currently only texlive-lang-german is known to be unavailable
    # This is a list to allow for easy extension if other packages are found to be unavailable
    unavailable_packages = [
        'texlive-lang-german',  # NOT available in Alpine - use texlive-lang-european instead
    ]

    # Alpine-compatible packages that provide German language support
    alpine_german_packages = [
        'texlive-lang-european'  # Provides German language support in Alpine
    ]

    success = True

    for workflow_file in workflow_files:
        if not os.path.exists(workflow_file):
            continue

        print(f"\n📄 Checking {workflow_file}...")

        try:
            with open(workflow_file, 'r') as f:
                workflow_data = yaml.safe_load(f)

            jobs = workflow_data.get('jobs', {})

            for job_name, job_data in jobs.items():
                steps = job_data.get('steps', [])
                for step in steps:
                    if step.get('uses', '').startswith('xu-cheng/latex-action'):
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
                            print(f"❌ Found unavailable packages in xu-cheng/latex-action: {unavailable_found}")
                            print(f"   Replace with: texlive-lang-european")
                            success = False
                        elif alpine_german_found:
                            print(f"✅ xu-cheng/latex-action uses Alpine-compatible German support: {alpine_german_found}")
                        else:
                            # No German language package specified - this is acceptable if German support is not needed
                            print("✅ xu-cheng/latex-action found (no German language package specified)")

        except Exception as e:
            print(f"❌ Error checking {workflow_file}: {e}")
            success = False

    return success

def main():
    """Run Alpine compatibility validation for Issue #1165"""
    print("=" * 80)
    print("🧪 ISSUE #1165 ALPINE COMPATIBILITY VALIDATION")
    print("=" * 80)

    if test_alpine_compatibility():
        print("\n🎉 ALPINE COMPATIBILITY VALIDATION PASSED!")
        print("All xu-cheng/latex-action steps use Alpine-compatible packages.")
        return 0
    else:
        print("\n❌ ALPINE COMPATIBILITY VALIDATION FAILED!")
        print("Some xu-cheng/latex-action steps still use Ubuntu packages.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
