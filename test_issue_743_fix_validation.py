#!/usr/bin/env python3
"""
Test validation for Issue #743 fix: CI robustness with LaTeX action version pinning

This script validates that the specific changes mentioned in the PR have been properly implemented:
1. Comprehensive validation step is present in CI workflow
2. LaTeX action is pinned to @v2.0.0 for reliable builds
3. pifont package dependencies are properly configured
"""

import yaml
import os
import sys
from pathlib import Path


def test_latex_action_version_pinning():
    """Test that dante-ev/latex-action is pinned to v2.0.0 as mentioned in PR."""
    print("\n[FIX] TESTING LATEX ACTION VERSION PINNING")
    print("-" * 50)

    workflow_path = '.github/workflows/latex-build.yml'

    if not os.path.exists(workflow_path):
        print(f"[FAIL] ERROR: Main workflow file {workflow_path} not found")
        return False

    try:
        with open(workflow_path, 'r') as f:
            workflow_content = yaml.safe_load(f)
    except Exception as e:
        print(f"[FAIL] ERROR: Failed to parse {workflow_path}: {e}")
        return False

    # Find the LaTeX action step
    jobs = workflow_content.get('jobs', {})
    build_job = jobs.get('build', {})
    steps = build_job.get('steps', [])

    latex_step = None
    for step in steps:
        if step.get('name') == 'Set up LaTeX':
            latex_step = step
            break

    if not latex_step:
        print("[FAIL] ERROR: 'Set up LaTeX' step not found in workflow")
        return False

    # Check the uses field for the exact version
    uses_field = latex_step.get('uses', '')
    expected_version = 'dante-ev/latex-action@v2.0.0'

    if uses_field == expected_version:
        print(f"[PASS] CORRECT: LaTeX action is pinned to {expected_version}")
        return True
    else:
        print(f"[FAIL] INCORRECT: Expected '{expected_version}', found '{uses_field}'")
        return False


def test_comprehensive_validation_step():
    """Test that comprehensive CI validation step is present in workflow."""
    print("\n[TEST] TESTING COMPREHENSIVE VALIDATION STEP")
    print("-" * 50)

    workflow_path = '.github/workflows/latex-build.yml'

    try:
        with open(workflow_path, 'r') as f:
            workflow_content = yaml.safe_load(f)
    except Exception as e:
        print(f"[FAIL] ERROR: Failed to parse {workflow_path}: {e}")
        return False

    # Find the comprehensive validation step
    jobs = workflow_content.get('jobs', {})
    build_job = jobs.get('build', {})
    steps = build_job.get('steps', [])

    validation_step = None
    for step in steps:
        if 'comprehensive CI validation' in step.get('name', ''):
            validation_step = step
            break

    if not validation_step:
        print("[FAIL] ERROR: 'comprehensive CI validation' step not found in workflow")
        return False

    # Check that it runs the test_issue_743_validation.py script
    run_command = validation_step.get('run', '')
    if 'test_issue_743_validation.py' in run_command:
        print("[PASS] CORRECT: Comprehensive validation step runs test_issue_743_validation.py")
        return True
    else:
        print(f"[FAIL] INCORRECT: Validation step does not run expected script. Found: {run_command}")
        return False


def test_pifont_package_dependencies():
    """Test that pifont package dependencies are properly configured."""
    print("\n[PACKAGE] TESTING PIFONT PACKAGE DEPENDENCIES")
    print("-" * 50)

    workflow_path = '.github/workflows/latex-build.yml'

    try:
        with open(workflow_path, 'r') as f:
            workflow_content = yaml.safe_load(f)
    except Exception as e:
        print(f"[FAIL] ERROR: Failed to parse {workflow_path}: {e}")
        return False

    # Find the LaTeX action step
    jobs = workflow_content.get('jobs', {})
    build_job = jobs.get('build', {})
    steps = build_job.get('steps', [])

    latex_step = None
    for step in steps:
        if step.get('name') == 'Set up LaTeX':
            latex_step = step
            break

    if not latex_step:
        print("[FAIL] ERROR: 'Set up LaTeX' step not found in workflow")
        return False

    extra_packages = latex_step.get('with', {}).get('extra_system_packages', '')

    # Check for pifont-providing packages
    pifont_providers = ['texlive-pstricks', 'texlive-latex-extra', 'texlive-fonts-extra']
    found_providers = [pkg for pkg in pifont_providers if pkg in extra_packages]

    if found_providers:
        print(f"[PASS] CORRECT: pifont available via packages: {', '.join(found_providers)}")

        # Specifically check for texlive-pstricks (Issue #739 fix)
        if 'texlive-pstricks' in extra_packages:
            print("[PASS] CORRECT: texlive-pstricks package present (Issue #739 compliance)")

        return True
    else:
        print("[FAIL] MISSING: No packages found that provide pifont")
        return False


def test_validation_script_exists():
    """Test that the comprehensive validation script exists and is executable."""
    print("\n[NOTE] TESTING VALIDATION SCRIPT EXISTS")
    print("-" * 50)

    script_path = 'test_issue_743_validation.py'

    if not os.path.exists(script_path):
        print(f"[FAIL] ERROR: Validation script {script_path} not found")
        return False

    print(f"[PASS] FOUND: {script_path}")

    # Check if it's executable
    if os.access(script_path, os.X_OK):
        print(f"[PASS] EXECUTABLE: {script_path} has execute permissions")
    else:
        print(f"[WARN]  INFO: {script_path} is not executable (but can be run with python3)")

    return True


def run_issue_743_fix_validation():
    """Run all Issue #743 fix validation tests."""
    print("=" * 70)
    print("ISSUE #743 FIX VALIDATION")
    print("CI Robustness with LaTeX Action Version Pinning")
    print("=" * 70)

    validation_tests = [
        ("LaTeX Action Version Pinning", test_latex_action_version_pinning),
        ("Comprehensive Validation Step", test_comprehensive_validation_step),
        ("pifont Package Dependencies", test_pifont_package_dependencies),
        ("Validation Script Exists", test_validation_script_exists),
    ]

    results = []

    for test_name, test_func in validation_tests:
        print(f"\n{'='*15} {test_name.upper()} {'='*15}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"[FAIL] ERROR: Test '{test_name}' failed with exception: {e}")
            results.append((test_name, False))

    # Summary report
    print("\n" + "=" * 70)
    print("FIX VALIDATION SUMMARY REPORT")
    print("=" * 70)

    passed = 0
    total = len(results)

    for test_name, result in results:
        status = "[PASS] PASS" if result else "[FAIL] FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1

    print(f"\nOverall Result: {passed}/{total} tests passed")

    if passed == total:
        print("\n[SUCCESS] ISSUE #743 FIX VALIDATION PASSED!")
        print("\nThe following PR requirements have been met:")
        print("  [OK] LaTeX action pinned to @v2.0.0 for reliable builds")
        print("  [OK] Comprehensive validation step present in CI workflow")
        print("  [OK] pifont package dependencies properly configured")
        print("  [OK] Validation script test_issue_743_validation.py exists")
        print("\nCI pipeline is now more robust and ready for production use.")
        return True
    else:
        print(f"\n[FAIL] {total - passed} validation test(s) failed")
        print("Please address the issues above to complete Issue #743 requirements.")
        return False


def main():
    """Main entry point for Issue #743 fix validation."""
    # Ensure we're in the right directory
    if not Path('main.tex').exists():
        print("[FAIL] ERROR: This script must be run from the CTMM repository root")
        print("Expected to find main.tex in current directory")
        sys.exit(1)

    success = run_issue_743_fix_validation()

    print("\n" + "=" * 70)
    if success:
        print("ISSUE #743 FIX VALIDATION: SUCCESS [PASS]")
        print("All PR requirements have been successfully implemented.")
    else:
        print("ISSUE #743 FIX VALIDATION: NEEDS ATTENTION [FAIL]")
        print("Some PR requirements are not yet met.")
    print("=" * 70)

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
