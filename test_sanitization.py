#!/usr/bin/env python3
"""
Test script for CTMM build system package name sanitization.
This ensures that LaTeX command generation is safe and doesn't create invalid command names.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from build_manager import sanitize_package_name, generate_placeholder_command


def test_sanitization():
    """Test that package name sanitization works correctly."""
    test_cases = [
        # (input, expected_output)
        ('ctmm-design', 'ctmmDesign'),
        ('form-elements', 'formElements'),
        ('ctmm_diagrams', 'ctmmDiagrams'),
        ('test-package-name', 'testPackageName'),
        ('simple', 'simple'),
        ('complex-name_with-mixed_separators', 'complexNameWithMixedSeparators'),
        ('123invalid', 'invalid'),
        ('-invalid-start', 'InvalidStart'),
        ('', 'pkg'),
        ('test.sty', 'test'),  # Should handle file extensions
    ]
    
    print("Testing package name sanitization...")
    print("=" * 50)
    
    all_passed = True
    for input_name, expected in test_cases:
        result = sanitize_package_name(input_name)
        passed = result == expected
        status = "✓" if passed else "✗"
        print(f"{status} '{input_name}' -> '{result}' (expected: '{expected}')")
        
        if not passed:
            all_passed = False
        
        # Ensure result is safe for LaTeX
        is_safe = result.isalpha() and (not result or result[0].isalpha())
        if not is_safe:
            print(f"  ERROR: Result '{result}' is not safe for LaTeX commands!")
            all_passed = False
    
    return all_passed


def test_placeholder_generation():
    """Test that placeholder command generation produces valid LaTeX."""
    test_cases = [
        'ctmm-design',
        'form-elements',
        'test_package',
        'simple',
    ]
    
    print("\nTesting placeholder command generation...")
    print("=" * 50)
    
    all_passed = True
    for package_name in test_cases:
        command = generate_placeholder_command(package_name)
        
        # Check that the command doesn't contain invalid characters in the command name
        # Extract the command name between \newcommand{\ and }
        import re
        match = re.search(r'\\newcommand\{\\(\w+)\}', command)
        if match:
            command_name = match.group(1)
            is_valid = command_name.isalpha()
            status = "✓" if is_valid else "✗"
            print(f"{status} {package_name}: \\{command_name}")
            if not is_valid:
                print(f"  ERROR: Command name '{command_name}' contains invalid characters!")
                all_passed = False
        else:
            print(f"✗ {package_name}: Could not extract command name from: {command}")
            all_passed = False
    
    return all_passed


def main():
    """Run all tests."""
    print("CTMM Build System - Package Name Sanitization Tests")
    print("=" * 60)
    
    test1_passed = test_sanitization()
    test2_passed = test_placeholder_generation()
    
    print("\n" + "=" * 60)
    if test1_passed and test2_passed:
        print("✓ All tests passed! Package name sanitization is working correctly.")
        return 0
    else:
        print("✗ Some tests failed. Package name sanitization needs attention.")
        return 1


if __name__ == "__main__":
    sys.exit(main())