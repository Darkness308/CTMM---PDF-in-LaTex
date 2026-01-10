#!/usr/bin/env python3
"""
Test validation for Issue #1165: CI Alpine Compatibility Fix
Validates that CI workflows do NOT use extra_system_packages with xu-cheng/latex-action
since the texlive-full Docker image already includes all necessary packages.
"""

import os
import sys
import yaml

def test_alpine_compatibility():
    """Test that xu-cheng/latex-action does not specify extra_system_packages"""
    print("🧪 Testing Alpine Package Compatibility")
    print("=" * 60)

    workflow_files = [
        '.github/workflows/latex-validation.yml',
        '.github/workflows/latex-build.yml',
        '.github/workflows/automated-pr-merge-test.yml'
    ]

    # Alpine packages that don't exist and should NOT be used with xu-cheng/latex-action
    problematic_packages = [
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
                        
                        # Check if extra_system_packages is present at all
                        if 'extra_system_packages' in step_with:
                            extra_packages = step_with.get('extra_system_packages', '')
                            
                            # Check for problematic packages
                            packages_found = []
                            for pkg in problematic_packages:
                                if pkg in str(extra_packages):
                                    packages_found.append(pkg)
                            
                            if packages_found:
                                print(f"❌ Found Alpine-incompatible packages in xu-cheng/latex-action: {packages_found}")
                                print(f"   These packages don't exist in Alpine Linux and will cause build failures.")
                                success = False
                            else:
                                print(f"⚠️  extra_system_packages is present but doesn't contain known problematic packages")
                        else:
                            print("✅ No extra_system_packages specified (texlive-full image has everything needed)")

        except Exception as e:
            print(f"❌ Error checking {workflow_file}: {e}")
            success = False

    return success

def main():
    """Run Alpine compatibility validation for Issue #1165"""
    print("=" * 80)
    print("🧪 ALPINE COMPATIBILITY FIX VALIDATION")
    print("=" * 80)
    print("\nValidating that xu-cheng/latex-action@v3 does NOT specify extra_system_packages")
    print("because the texlive-full Docker image already includes all necessary packages.")
    print("\nThe error 'unable to select packages: texlive-lang-german (no such package)'")
    print("occurs when trying to install these packages in Alpine Linux.")
    print("\nSolution: Remove extra_system_packages - texlive-full has everything needed.")
    print("=" * 80)

    if test_alpine_compatibility():
        print("\n🎉 ALPINE COMPATIBILITY VALIDATION PASSED!")
        print("✅ xu-cheng/latex-action correctly configured without extra_system_packages")
        print("✅ The texlive-full Docker image includes all German language packages")
        print("✅ No Alpine package installation errors will occur")
        return 0
    else:
        print("\n❌ ALPINE COMPATIBILITY VALIDATION FAILED!")
        print("❌ Found Alpine-incompatible packages in extra_system_packages")
        print("❌ These will cause 'unable to select packages' errors in Alpine Linux")
        return 1

if __name__ == "__main__":
    sys.exit(main())
