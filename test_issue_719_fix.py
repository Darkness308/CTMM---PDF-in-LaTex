#!/usr/bin/env python3
"""
Test for Issue #719: CI Build Failure due to IndentationError in latex_validator.py

This test validates that the latex_validator.py file has correct Python syntax
and that the CTMM build system can successfully import and use the LaTeXValidator class.
"""

import sys
import subprocess
from pathlib import Path

def test_latex_validator_import():
    """Test that latex_validator.py can be imported without syntax errors."""
    try:
        from latex_validator import LaTeXValidator
        print("✅ LaTeXValidator imported successfully")
        return True
    except IndentationError as e:
        print(f"❌ IndentationError in latex_validator.py: {e}")
        return False
    except SyntaxError as e:
        print(f"❌ SyntaxError in latex_validator.py: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error importing LaTeXValidator: {e}")
        return False

def test_sanitize_pkg_name_function():
    """Test the specific function that had the indentation error."""
    try:
        from latex_validator import sanitize_pkg_name

        # Test cases for the function
        test_cases = [
            ("arbeitsblatt-checkin", "pkgArbeitsblattCheckin"),
            ("trigger-management", "pkgTriggerManagement"),
            ("module123", "pkgModule123"),
            ("test", "pkgTest"),
            ("", "pkg")
        ]

        for input_val, expected in test_cases:
            result = sanitize_pkg_name(input_val)
            if result == expected:
                print(f"✅ sanitize_pkg_name('{input_val}') = '{result}'")
            else:
                print(f"❌ sanitize_pkg_name('{input_val}') = '{result}', expected '{expected}'")
                return False

        return True
    except Exception as e:
        print(f"❌ Error testing sanitize_pkg_name function: {e}")
        return False

def test_ctmm_build_system():
    """Test that the CTMM build system runs without errors."""
    try:
        result = subprocess.run(
            ["python3", "ctmm_build.py"],
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode == 0:
            print("✅ CTMM build system runs successfully")
            return True
        else:
            print(f"❌ CTMM build system failed with exit code {result.returncode}")
            print(f"Stderr: {result.stderr}")
            return False

    except subprocess.TimeoutExpired:
        print("❌ CTMM build system timed out")
        return False
    except Exception as e:
        print(f"❌ Error running CTMM build system: {e}")
        return False

def main():
    """Main test function for Issue #719."""
    print("=" * 70)
    print("ISSUE #719 FIX VALIDATION: CI Build Failure")
    print("=" * 70)
    print("Testing indentation fix in latex_validator.py")
    print()

    all_tests_passed = True

    # Test 1: Import LaTeXValidator
    print("1. Testing LaTeXValidator import...")
    if not test_latex_validator_import():
        all_tests_passed = False
    print()

    # Test 2: Test the specific function that had the error
    print("2. Testing sanitize_pkg_name function...")
    if not test_sanitize_pkg_name_function():
        all_tests_passed = False
    print()

    # Test 3: Test CTMM build system
    print("3. Testing CTMM build system...")
    if not test_ctmm_build_system():
        all_tests_passed = False
    print()

    # Summary
    print("=" * 70)
    if all_tests_passed:
        print("🎉 ALL TESTS PASSED - Issue #719 fix validated!")
        print("The CI build failure has been resolved.")
        print("The indentation error in latex_validator.py is fixed.")
        sys.exit(0)
    else:
        print("❌ SOME TESTS FAILED - Issue #719 not fully resolved")
        sys.exit(1)

if __name__ == "__main__":
    main()
