#!/usr/bin/env python3
"""
Validation script for GitHub Actions workflow LaTeX action fix.
This script validates that the LaTeX action version regression is fixed.
"""

import os
import re
import sys
import yaml

def validate_workflow_files():
    """Validate GitHub Actions workflow files for correct LaTeX action versions."""

    workflow_dir = ".github/workflows"
    issues_found = []
    fixes_verified = []

    print("🔍 Validating GitHub Actions workflow files...")

    if not os.path.exists(workflow_dir):
        issues_found.append(f"❌ Workflow directory {workflow_dir} not found")
        return issues_found, fixes_verified

    # Expected version based on Issue #1056 resolution
    expected_version = "v2.3.0"

    for filename in os.listdir(workflow_dir):
        if filename.endswith('.yml') or filename.endswith('.yaml'):
            filepath = os.path.join(workflow_dir, filename)

            print(f"   📄 Checking {filename}...")

            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Check for LaTeX action usage
                latex_action_pattern = r'dante-ev/latex-action@(v?\d+\.\d+\.\d+)'
                matches = re.findall(latex_action_pattern, content)

                if matches:
                    for version in matches:
                        clean_version = version.lstrip('v')
                        expected_clean = expected_version.lstrip('v')

                        if clean_version == expected_clean:
                            fixes_verified.append(f"✅ {filename}: LaTeX action version {version} (correct)")
                        else:
                            issues_found.append(f"❌ {filename}: LaTeX action version {version} (should be {expected_version})")

                # Check for YAML syntax issues
                try:
                    yaml.safe_load(content)
                    print(f"      ✅ YAML syntax valid")
                except yaml.YAMLError as e:
                    issues_found.append(f"❌ {filename}: YAML syntax error - {e}")

                # Check for quoted "on": keyword (Issue #1056 fix)
                if '"on":' in content:
                    fixes_verified.append(f"✅ {filename}: Properly quoted 'on:' keyword")
                elif 'on:' in content and '"on":' not in content:
                    # Check if it's at start of line (not indented) - would be a trigger
                    lines = content.split('\n')
                    for i, line in enumerate(lines):
                        if line.strip().startswith('on:') and not line.strip().startswith('"on":'):
                            issues_found.append(f"❌ {filename}:{i+1}: Unquoted 'on:' keyword (should be quoted)")
                            break

            except Exception as e:
                issues_found.append(f"❌ Error reading {filename}: {e}")

    return issues_found, fixes_verified

def validate_latex_packages():
    """Validate that required LaTeX packages are listed in workflows."""

    print("\n🔍 Validating LaTeX package dependencies...")

    required_packages = [
        'texlive-lang-german',
        'texlive-fonts-recommended',
        'texlive-latex-recommended',
        'texlive-fonts-extra',
        'texlive-latex-extra',
        'texlive-science',
        'texlive-pstricks'
    ]

    workflow_file = ".github/workflows/latex-build.yml"
    issues_found = []
    fixes_verified = []

    if os.path.exists(workflow_file):
        with open(workflow_file, 'r', encoding='utf-8') as f:
            content = f.read()

        for package in required_packages:
            if package in content:
                fixes_verified.append(f"✅ Required package {package} found")
            else:
                issues_found.append(f"❌ Required package {package} missing")
    else:
        issues_found.append(f"❌ Main workflow file {workflow_file} not found")

    return issues_found, fixes_verified

def validate_build_system():
    """Validate that the CTMM build system works correctly."""

    print("\n🔍 Validating CTMM build system...")

    issues_found = []
    fixes_verified = []

    # Check main files exist
    critical_files = [
        'main.tex',
        'ctmm_build.py',
        'style/ctmm-design.sty',
        'style/form-elements.sty',
        'style/ctmm-diagrams.sty'
    ]

    for file in critical_files:
        if os.path.exists(file):
            fixes_verified.append(f"✅ Critical file {file} exists")
        else:
            issues_found.append(f"❌ Critical file {file} missing")

    # Test build system functionality
    try:
        import subprocess
        result = subprocess.run([
            'python3', 'ctmm_build.py'
        ], capture_output=True, text=True, timeout=60)

        if result.returncode == 0:
            if 'PASS' in result.stdout:
                fixes_verified.append("✅ CTMM build system validation passed")
            else:
                issues_found.append("❌ CTMM build system did not show PASS status")
        else:
            issues_found.append(f"❌ CTMM build system failed: {result.stderr}")

    except Exception as e:
        issues_found.append(f"❌ Error running CTMM build system: {e}")

    return issues_found, fixes_verified

def main():
    """Main validation function."""

    print("=" * 60)
    print("🚀 CTMM GitHub Actions Workflow Fix Validation")
    print("=" * 60)
    print("Validating fix for: 'Der build scheitert immer noch'")
    print("Based on Issue #1056 resolution requirements")
    print()

    all_issues = []
    all_fixes = []

    # Validate workflow files
    issues, fixes = validate_workflow_files()
    all_issues.extend(issues)
    all_fixes.extend(fixes)

    # Validate LaTeX packages
    issues, fixes = validate_latex_packages()
    all_issues.extend(issues)
    all_fixes.extend(fixes)

    # Validate build system
    issues, fixes = validate_build_system()
    all_issues.extend(issues)
    all_fixes.extend(fixes)

    # Summary
    print("\n" + "=" * 60)
    print("📊 VALIDATION SUMMARY")
    print("=" * 60)

    print(f"\n✅ FIXES VERIFIED ({len(all_fixes)}):")
    for fix in all_fixes:
        print(f"  {fix}")

    if all_issues:
        print(f"\n❌ ISSUES FOUND ({len(all_issues)}):")
        for issue in all_issues:
            print(f"  {issue}")

        print(f"\n🔧 VALIDATION RESULT: ISSUES NEED ATTENTION")
        return 1
    else:
        print(f"\n🎉 VALIDATION RESULT: ALL CHECKS PASSED")
        print("✅ The build failure issue should now be resolved!")
        return 0

if __name__ == "__main__":
    sys.exit(main())