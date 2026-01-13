#!/usr/bin/env python3
"""
Test validation for Issue #1157: CI Build Failure Resolution
Validates that the CI insights report failures have been resolved.
"""

import os
import sys
import yaml
import subprocess
import re

def test_latex_action_consistency():
    """Test that both workflows use consistent xu-cheng/latex-action@v3."""
    print("\n[FIX] Testing LaTeX Action Consistency")
    print("=" * 60)

    workflow_files = [
        '.github/workflows/latex-build.yml',
        '.github/workflows/latex-validation.yml'
    ]

    consistency_success = True
    latex_actions_found = {}

    for workflow_file in workflow_files:
        print(f"\n[FILE] Checking {workflow_file}...")

        if not os.path.exists(workflow_file):
            print(f"[FAIL] Workflow file not found: {workflow_file}")
            consistency_success = False
            continue

        try:
            with open(workflow_file, 'r') as f:
                content = f.read()

            # Find xu-cheng/latex-action usage
            xu_cheng_pattern = r'uses:\s*xu-cheng/latex-action@(v\d+)'
            matches = re.findall(xu_cheng_pattern, content)

            for match in matches:
                action_version = f"xu-cheng/latex-action@{match}"
                if action_version not in latex_actions_found:
                    latex_actions_found[action_version] = []
                latex_actions_found[action_version].append(workflow_file)

        except Exception as e:
            print(f"[FAIL] Error analyzing {workflow_file}: {e}")
            consistency_success = False

    print(f"\n[SUMMARY] LaTeX Action Version Summary:")
    for action, files in latex_actions_found.items():
        print(f"   {action} used in: {', '.join([os.path.basename(f) for f in files])}")

    # Check that all use xu-cheng/latex-action@v3
    expected_action = "xu-cheng/latex-action@v3"
    for action in latex_actions_found.keys():
        if action != expected_action:
            print(f"[FAIL] Inconsistent action version: {action} (expected {expected_action})")
            consistency_success = False

    if consistency_success and expected_action in latex_actions_found:
        print(f"[PASS] All workflows use consistent action version: {expected_action}")

    return consistency_success


def test_hyperref_bookmark_validation():
    """Test that hyperref/bookmark package order validation works correctly."""
    print("\n[PACKAGE] Testing hyperref/bookmark Package Order Validation")
    print("=" * 60)

    if not os.path.exists('main.tex'):
        print("[FAIL] main.tex not found")
        return False

    try:
        # Run the hyperref validation logic from latex-validation.yml
        result = subprocess.run([
            'bash', '-c', '''
            packages=$(grep "\\\\usepackage" main.tex | grep -v "^%")

            # Check that hyperref appears before the end and before any bookmark package
            echo "$packages" | grep -q "hyperref" || (echo "::error ::hyperref package not found in main.tex" && exit 1)

            # Get position of hyperref and bookmark (if exists)
            hyperref_line=$(echo "$packages" | grep -n "hyperref" | head -1 | cut -d: -f1)
            bookmark_line=$(echo "$packages" | grep -n "bookmark" | head -1 | cut -d: -f1)

            echo "Found hyperref at line: $hyperref_line"
            echo "Found bookmark at line: $bookmark_line"

            # If bookmark exists, it should come after hyperref
            if [ -n "$bookmark_line" ] && [ "$bookmark_line" -lt "$hyperref_line" ]; then
              echo "::error ::bookmark package should come after hyperref"
              exit 1
            fi

            # Check that no critical packages come after hyperref (except bookmark)
            packages_after_hyperref=$(echo "$packages" | tail -n +$((hyperref_line + 1)) | grep -v "bookmark")
            if [ -n "$packages_after_hyperref" ]; then
              echo "::error ::Core packages found after hyperref (only bookmark is allowed): $packages_after_hyperref"
              exit 1
            fi

            echo "[PASS] hyperref package ordering is correct"
            '''
        ], capture_output=True, text=True)

        print(result.stdout)
        if result.stderr:
            print(f"Errors: {result.stderr}")

        success = result.returncode == 0
        if success:
            print("[PASS] hyperref/bookmark validation passed")
        else:
            print("[FAIL] hyperref/bookmark validation failed")

        return success

    except Exception as e:
        print(f"[FAIL] Error running hyperref validation: {e}")
        return False


def test_latex_package_dependencies():
    """Test that LaTeX package dependencies are properly configured."""
    print("\n[PACKAGE] Testing LaTeX Package Dependencies")
    print("=" * 60)

    workflow_path = '.github/workflows/latex-build.yml'

    if not os.path.exists(workflow_path):
        print(f"[FAIL] Main workflow file {workflow_path} not found")
        return False

    try:
        with open(workflow_path, 'r') as f:
            workflow_content = yaml.safe_load(f)
    except Exception as e:
        print(f"[FAIL] Error parsing {workflow_path}: {e}")
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
        print("[FAIL] 'Set up LaTeX' step not found in workflow")
        return False

    print("[PASS] Found 'Set up LaTeX' step")

    # Check for xu-cheng/latex-action usage
    if latex_step.get('uses') != 'xu-cheng/latex-action@v3':
        print(f"[FAIL] Expected xu-cheng/latex-action@v3, got: {latex_step.get('uses')}")
        return False

    print("[PASS] Uses xu-cheng/latex-action@v3")

    extra_packages = latex_step.get('with', {}).get('extra_system_packages', '')
    print(f"[TEST] LaTeX packages configuration:")
    for line in extra_packages.strip().split('\n'):
        if line.strip():
            print(f"   - {line.strip()}")

    # Essential package validation
    required_packages = [
        'texlive-lang-german',       # German language support
        'texlive-fonts-recommended', # Recommended fonts
        'texlive-latex-recommended', # Recommended LaTeX packages
        'texlive-latex-extra',       # Extra LaTeX packages
        'texlive-fonts-extra',       # Extra fonts
        'texlive-science',           # Scientific packages
        'texlive-pstricks'           # PostScript tricks (contains pifont)
    ]

    all_packages_found = True
    print("\n[SEARCH] Validating essential packages...")

    for pkg in required_packages:
        if pkg in extra_packages:
            print(f"[PASS] FOUND: {pkg}")
        else:
            print(f"[FAIL] MISSING: {pkg}")
            all_packages_found = False

    return all_packages_found


def test_issue_743_validation_passes():
    """Test that the comprehensive Issue #743 validation now passes."""
    print("\n[TEST] Testing Issue #743 Validation Script")
    print("=" * 60)

    try:
        result = subprocess.run([
            'python3', 'test_issue_743_validation.py'
        ], capture_output=True, text=True)

        success = result.returncode == 0

        # Show summary of results
        lines = result.stdout.split('\n')
        for line in lines:
            if 'Overall Result:' in line or 'ALL VALIDATION TESTS PASSED' in line:
                print(line)
            elif 'PASS' in line or 'FAIL' in line:
                print(line)

        if success:
            print("[PASS] Issue #743 validation script passes")
        else:
            print("[FAIL] Issue #743 validation script fails")
            print("Error output:")
            print(result.stderr)

        return success

    except Exception as e:
        print(f"[FAIL] Error running validation script: {e}")
        return False


def main():
    """Run all validation tests for Issue #1157 fixes."""
    print("=" * 80)
    print("[TEST] ISSUE #1157 CI BUILD FAILURE RESOLUTION VALIDATION")
    print("=" * 80)

    tests = [
        ("LaTeX Action Consistency", test_latex_action_consistency),
        ("Hyperref/Bookmark Validation", test_hyperref_bookmark_validation),
        ("LaTeX Package Dependencies", test_latex_package_dependencies),
        ("Issue #743 Validation Passes", test_issue_743_validation_passes)
    ]

    results = {}

    for test_name, test_func in tests:
        print(f"\n{'='*80}")
        print(f"Running: {test_name}")
        print('='*80)

        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"[FAIL] Test failed with exception: {e}")
            results[test_name] = False

    # Summary
    print(f"\n{'='*80}")
    print("[SUMMARY] VALIDATION SUMMARY")
    print('='*80)

    passed = 0
    total = len(tests)

    for test_name, result in results.items():
        status = "[PASS] PASS" if result else "[FAIL] FAIL"
        print(f"{status}: {test_name}")
        if result:
            passed += 1

    print(f"\nOverall: {passed}/{total} tests passed")

    if passed == total:
        print("\n[SUCCESS] ALL TESTS PASSED!")
        print("Issue #1157 CI build failures have been resolved.")
        return 0
    else:
        print(f"\n[FAIL] {total - passed} test(s) failed")
        print("Some issues remain to be addressed.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
