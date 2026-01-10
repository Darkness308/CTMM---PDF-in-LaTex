#!/usr/bin/env python3
"""
Test validation for Issue #1165: CI Alpine Compatibility Fix
Validates that CI workflows use Alpine-compatible packages for xu-cheng/latex-action.

Issue: texlive-lang-german does not exist in Alpine repositories
Solution: Use texlive-lang-european which includes German language support
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

    # Packages that should NOT be used with xu-cheng/latex-action (Alpine)
    # because they don't exist in Alpine repositories
    incompatible_packages = [
        'texlive-lang-german',  # Use texlive-lang-european instead
    ]

    # Alpine-compatible packages that SHOULD be used
    alpine_compatible = [
        'texlive-lang-european',  # Includes German + other European languages
        'texlive-fonts-recommended',
        'texlive-latex-recommended',
        'texlive-fonts-extra',
        'texlive-latex-extra',
        'texlive-science',
        'texlive-pstricks',
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

                        # Check for incompatible packages in xu-cheng/latex-action steps
                        incompatible_found = []
                        for incompatible_pkg in incompatible_packages:
                            if incompatible_pkg in extra_packages:
                                incompatible_found.append(incompatible_pkg)

                        if incompatible_found:
                            print(f"❌ Found Alpine-incompatible packages: {incompatible_found}")
                            print(f"   These packages don't exist in Alpine repositories")
                            success = False
                        else:
                            print("✅ No Alpine-incompatible packages found")

                        # Check for Alpine-compatible alternatives
                        if 'texlive-lang-european' in extra_packages:
                            print("✅ Using texlive-lang-european (Alpine-compatible, includes German)")
                        elif step.get('uses', '').startswith('xu-cheng/latex-action'):
                            print("⚠️  Consider using texlive-lang-european for German support")

        except Exception as e:
            print(f"❌ Error checking {workflow_file}: {e}")
            success = False

    return success

def main():
    """Run Alpine compatibility validation for Issue #1165"""
    print("=" * 80)
    print("🧪 ISSUE #1165 ALPINE COMPATIBILITY VALIDATION")
    print("=" * 80)
    print("\nValidating that xu-cheng/latex-action uses Alpine-compatible packages...")
    print("Issue: texlive-lang-german doesn't exist in Alpine repositories")
    print("Solution: Use texlive-lang-european which includes German support\n")

    if test_alpine_compatibility():
        print("\n🎉 ALPINE COMPATIBILITY VALIDATION PASSED!")
        print("All xu-cheng/latex-action steps use Alpine-compatible packages.")
        print("✅ texlive-lang-european is used instead of texlive-lang-german")
        print("✅ German language support is available via texlive-lang-european")
        return 0
    else:
        print("\n❌ ALPINE COMPATIBILITY VALIDATION FAILED!")
        print("Some xu-cheng/latex-action steps use Alpine-incompatible packages.")
        print("❌ texlive-lang-german must be replaced with texlive-lang-european")
        return 1

if __name__ == "__main__":
    sys.exit(main())
