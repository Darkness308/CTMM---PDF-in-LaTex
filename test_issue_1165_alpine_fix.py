#!/usr/bin/env python3
"""
Test validation for Issue #1165: CI Alpine Compatibility Fix
Validates that CI workflows use Alpine-compatible packages for xu-cheng/latex-action.
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

    # Ubuntu packages that should NOT be used with xu-cheng/latex-action
    ubuntu_packages = [
        'texlive-lang-german',
        'texlive-fonts-recommended',
        'texlive-latex-recommended',
        'texlive-fonts-extra',
        'texlive-latex-extra',
        'texlive-science',
        'texlive-pstricks',
        'texlive-latex-base'
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

                        # Check for Ubuntu packages in xu-cheng/latex-action steps
                        ubuntu_found = []
                        for ubuntu_pkg in ubuntu_packages:
                            if ubuntu_pkg in extra_packages:
                                ubuntu_found.append(ubuntu_pkg)

                        if ubuntu_found:
                            print(f"❌ Found Ubuntu packages in xu-cheng/latex-action: {ubuntu_found}")
                            success = False
                        else:
                            print("✅ xu-cheng/latex-action uses Alpine-compatible packages")

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
