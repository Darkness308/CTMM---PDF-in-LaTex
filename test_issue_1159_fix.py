#!/usr/bin/env python3
"""
Test validation for Issue #1159: CI Validation Failure Fix
Validates that the hyperref validation logic has been improved to handle CI environment issues.
"""

import os
import sys
import subprocess
import re

def test_awk_regex_improvement():
    """Test that the improved AWK regex doesn't produce warnings."""
    print("\n[FIX] Testing AWK Regex Improvement")
    print("=" * 60)

    # Test the old problematic AWK command
    print("Testing old AWK pattern (should show warning)...")
    result_old = subprocess.run([
        'awk', '/\\begin{document}/ {flag=1; next} flag && /\\usepackage/ {print; exit 1}', 'main.tex'
    ], capture_output=True, text=True)

    old_has_warning = 'warning' in result_old.stderr
    print(f"Old pattern warning: {'Yes' if old_has_warning else 'No'}")

    # Test the new improved AWK command
    print("Testing new AWK pattern (should be clean)...")
    result_new = subprocess.run([
        'awk', '/\\\\begin\\{document\\}/ {flag=1; next} flag && /\\\\usepackage/ {print; exit 1}', 'main.tex'
    ], capture_output=True, text=True)

    new_has_warning = 'warning' in result_new.stderr
    print(f"New pattern warning: {'Yes' if new_has_warning else 'No'}")

    if not new_has_warning:
        print("[PASS] AWK regex improvement successful")
        return True
    else:
        print("[FAIL] AWK regex still has warnings")
        print(f"Error: {result_new.stderr}")
        return False


def test_robust_hyperref_validation():
    """Test that the improved hyperref validation logic is more robust."""
    print("\n[PACKAGE] Testing Robust Hyperref Validation")
    print("=" * 60)

    if not os.path.exists('main.tex'):
        print("[FAIL] main.tex not found")
        return False

    try:
        # Test the improved hyperref validation with debug output
        script = '''
        packages=$(grep "\\\\usepackage" main.tex | grep -v "^%")

        echo "$packages" | grep -q "hyperref" || (echo "::error ::hyperref package not found in main.tex" && exit 1)

        hyperref_line=$(echo "$packages" | grep -n "hyperref" | head -1 | cut -d: -f1)
        bookmark_line=$(echo "$packages" | grep -n "bookmark" | head -1 | cut -d: -f1)

        echo "Debug: hyperref at line $hyperref_line"
        echo "Debug: bookmark at line $bookmark_line"

        if [ -n "$bookmark_line" ] && [ "$bookmark_line" -lt "$hyperref_line" ]; then
          echo "::error ::bookmark package should come after hyperref"
          exit 1
        fi

        # Use more robust arithmetic to avoid potential shell issues
        next_line=$((hyperref_line + 1))
        echo "Debug: checking from line $next_line onward"
        packages_after_hyperref=$(echo "$packages" | tail -n +${next_line} | grep -v "bookmark")
        echo "Debug: packages after hyperref (filtered): '$packages_after_hyperref'"

        if [ -n "$packages_after_hyperref" ]; then
          echo "::error ::Core packages found after hyperref (only bookmark is allowed): $packages_after_hyperref"
          exit 1
        fi

        echo "[PASS] hyperref package ordering is correct"
        '''

        result = subprocess.run(['bash', '-c', script], capture_output=True, text=True)

        print(result.stdout)
        if result.stderr:
            print(f"Errors: {result.stderr}")

        success = result.returncode == 0
        if success:
            print("[PASS] Robust hyperref validation passed")
        else:
            print("[FAIL] Robust hyperref validation failed")

        return success

    except Exception as e:
        print(f"[FAIL] Error running robust hyperref validation: {e}")
        return False


def test_workflow_syntax_validity():
    """Test that the workflow file syntax is valid."""
    print("\n[FILE] Testing Workflow Syntax Validity")
    print("=" * 60)

    workflow_file = '.github/workflows/latex-validation.yml'

    if not os.path.exists(workflow_file):
        print(f"[FAIL] Workflow file not found: {workflow_file}")
        return False

    try:
        import yaml

        with open(workflow_file, 'r') as f:
            workflow_content = yaml.safe_load(f)

        print("[PASS] YAML syntax is valid")

        # Check for the improved validation step
        jobs = workflow_content.get('jobs', {})
        validate_job = jobs.get('validate', {})
        steps = validate_job.get('steps', [])

        hyperref_step = None
        for step in steps:
            if step.get('name') == 'Check hyperref is last core package':
                hyperref_step = step
                break

        if not hyperref_step:
            print("[FAIL] Hyperref validation step not found")
            return False

        print("[PASS] Found hyperref validation step")

        # Check for debug output and robust arithmetic
        step_script = hyperref_step.get('run', '')
        has_debug = 'Debug:' in step_script
        has_robust_arithmetic = 'next_line=$(' in step_script

        if has_debug:
            print("[PASS] Debug output present")
        else:
            print("[FAIL] Debug output missing")

        if has_robust_arithmetic:
            print("[PASS] Robust arithmetic present")
        else:
            print("[FAIL] Robust arithmetic missing")

        return has_debug and has_robust_arithmetic

    except Exception as e:
        print(f"[FAIL] Error validating workflow syntax: {e}")
        return False


def test_ci_environment_compatibility():
    """Test compatibility with different shell environments."""
    print("\n[EMOJI] Testing CI Environment Compatibility")
    print("=" * 60)

    # Test different shell environments if available
    shells_to_test = ['/bin/bash', '/bin/sh']

    success_count = 0
    for shell in shells_to_test:
        if os.path.exists(shell):
            print(f"Testing with {shell}...")

            script = '''
            packages=$(grep "\\\\usepackage" main.tex | grep -v "^%")
            hyperref_line=$(echo "$packages" | grep -n "hyperref" | head -1 | cut -d: -f1)
            next_line=$((hyperref_line + 1))
            packages_after_hyperref=$(echo "$packages" | tail -n +${next_line} | grep -v "bookmark")
            if [ -n "$packages_after_hyperref" ]; then
              exit 1
            fi
            echo "Shell test passed"
            '''

            result = subprocess.run([shell, '-c', script], capture_output=True, text=True)

            if result.returncode == 0:
                print(f"[PASS] {shell} compatibility: PASS")
                success_count += 1
            else:
                print(f"[FAIL] {shell} compatibility: FAIL")
                print(f"Error: {result.stderr}")
        else:
            print(f"[WARN]  {shell} not available")

    return success_count > 0


def main():
    """Run all validation tests for Issue #1159 fixes."""
    print("=" * 80)
    print("[TEST] ISSUE #1159 CI VALIDATION FAILURE FIX VALIDATION")
    print("=" * 80)

    tests = [
        ("AWK Regex Improvement", test_awk_regex_improvement),
        ("Robust Hyperref Validation", test_robust_hyperref_validation),
        ("Workflow Syntax Validity", test_workflow_syntax_validity),
        ("CI Environment Compatibility", test_ci_environment_compatibility)
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
        print("Issue #1159 CI validation failures have been resolved.")
        return 0
    else:
        print(f"\n[FAIL] {total - passed} test(s) failed")
        print("Some issues remain to be addressed.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
