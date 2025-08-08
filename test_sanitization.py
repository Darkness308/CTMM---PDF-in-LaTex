#!/usr/bin/env python3
"""
Test script for package name sanitization functionality.
This script verifies that the sanitize_latex_command_name function 
properly handles various edge cases and special characters.
"""

import sys
import os

# Add the current directory to the path so we can import our functions
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ctmm_build import sanitize_latex_command_name


def test_sanitization():
    """Test the sanitize_latex_command_name function with various inputs."""
    
    test_cases = [
        # (input, expected_output, description)
        ("ctmm-design", "ctmmDashDesign", "Handle hyphens"),
        ("form_elements", "formUnderscoreElements", "Handle underscores"),
        ("test.file", "testDotFile", "Handle dots"),
        ("123test", "numTest", "Handle leading numbers"),
        ("test123", "test", "Handle trailing numbers"),
        ("simple", "simple", "Handle simple names"),
        ("UPPERCASE", "uPPERCASE", "Handle uppercase"),
        ("mixed-Case_Test", "mixedDashCaseUnderscoreTest", "Handle mixed case and characters"),
        ("", "placeholder", "Handle empty string"),
        ("   ", "placeholder", "Handle whitespace only"),
        ("a", "a", "Handle single character"),
        ("test@example", "testAtExample", "Handle @ symbol"),
        ("test+plus", "testPlusPlus", "Handle + symbol"),
        ("test!", "testExclamation", "Handle exclamation"),
        ("测试", "placeholder", "Handle non-ASCII characters"),
        ("test\ttab\nnewline", "testtabnewline", "Handle whitespace characters"),
    ]
    
    print("Testing package name sanitization...")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for input_name, expected, description in test_cases:
        result = sanitize_latex_command_name(input_name)
        
        if result == expected:
            print(f"✓ PASS: {description}")
            print(f"  Input: '{input_name}' → Output: '{result}'")
            passed += 1
        else:
            print(f"✗ FAIL: {description}")
            print(f"  Input: '{input_name}'")
            print(f"  Expected: '{expected}'")
            print(f"  Got: '{result}'")
            failed += 1
        print()
    
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("All tests passed! ✓")
        return True
    else:
        print(f"{failed} tests failed! ✗")
        return False


def test_latex_compatibility():
    """Test that the sanitized names are valid LaTeX command names."""
    print("\nTesting LaTeX compatibility...")
    print("=" * 60)
    
    test_names = ["ctmm-design", "form_elements", "123test", "complex-test_case"]
    
    import re
    latex_command_pattern = r'^[a-zA-Z][a-zA-Z]*$'
    
    all_valid = True
    
    for test_name in test_names:
        sanitized = sanitize_latex_command_name(test_name)
        command_name = f"{sanitized}Placeholder"
        
        if re.match(latex_command_pattern, command_name):
            print(f"✓ VALID: '{test_name}' → '\\{command_name}'")
        else:
            print(f"✗ INVALID: '{test_name}' → '\\{command_name}'")
            all_valid = False
    
    print("=" * 60)
    if all_valid:
        print("All generated command names are LaTeX-compatible! ✓")
    else:
        print("Some command names are not LaTeX-compatible! ✗")
    
    return all_valid


def main():
    """Run all tests."""
    print("CTMM Package Name Sanitization Tests")
    print("=" * 60)
    
    test1_passed = test_sanitization()
    test2_passed = test_latex_compatibility()
    
    print("\n" + "=" * 60)
    print("OVERALL RESULTS")
    print("=" * 60)
    
    if test1_passed and test2_passed:
        print("🎉 All tests passed! The sanitization function is working correctly.")
        sys.exit(0)
    else:
        print("❌ Some tests failed. Please review and fix the issues.")
        sys.exit(1)


if __name__ == "__main__":
    main()