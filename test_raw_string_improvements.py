#!/usr/bin/env python3
"""
Test script to validate that the raw string improvements are working correctly.
Tests the specific changes made to fix_latex_escaping.py and conversion_workflow.py.
"""

import re
import subprocess

def test_raw_strings_in_fix_latex_escaping():
    """Test that fix_latex_escaping.py uses raw strings for LaTeX patterns."""
    print("Testing fix_latex_escaping.py raw string usage...")
    
    with open('fix_latex_escaping.py', 'r') as f:
        content = f.read()
    
    # Look for the specific line that should now be a raw string
    pattern_found = False
    raw_string_used = False
    
    lines = content.split('\n')
    for line_num, line in enumerate(lines, 1):
        if 'textbackslash{}' in line and 'in content' in line:
            pattern_found = True
            # Check if it's using a raw string
            if r"r'\textbackslash{}'" in line:
                raw_string_used = True
                print(f"  ✅ Line {line_num}: Raw string correctly used: {line.strip()}")
            else:
                print(f"  ❌ Line {line_num}: Should use raw string: {line.strip()}")
    
    if not pattern_found:
        print("  ⚠️  Pattern not found - this may indicate the test needs updating")
        return False
    
    return raw_string_used

def test_raw_strings_in_conversion_workflow():
    """Test that conversion_workflow.py uses raw strings for LaTeX patterns.""" 
    print("Testing conversion_workflow.py raw string usage...")
    
    with open('conversion_workflow.py', 'r') as f:
        content = f.read()
    
    # Look for the specific line that should now be a raw string
    pattern_found = False
    raw_string_used = False
    
    lines = content.split('\n')
    for line_num, line in enumerate(lines, 1):
        if 'Problem: Excessive' in line and 'textbackslash{}' in line:
            pattern_found = True
            # Check if it's using a raw string
            if r'r"' in line or r"r'" in line:
                raw_string_used = True
                print(f"  ✅ Line {line_num}: Raw string correctly used: {line.strip()}")
            else:
                print(f"  ❌ Line {line_num}: Should use raw string: {line.strip()}")
    
    if not pattern_found:
        print("  ⚠️  Pattern not found - this may indicate the test needs updating")
        return False
    
    return raw_string_used

def test_workflow_empty_lines():
    """Test that the workflow file doesn't have redundant empty lines."""
    print("Testing workflow file formatting...")
    
    with open('.github/workflows/pr-validation.yml', 'r') as f:
        content = f.read()
    
    lines = content.split('\n')
    
    # Check for redundant empty lines before "### Need help?"
    found_help_section = False
    empty_lines_before_help = 0
    
    for i, line in enumerate(lines):
        if '### Need help?' in line:
            found_help_section = True
            # Count empty lines immediately before this line
            j = i - 1
            while j >= 0 and lines[j].strip() == '':
                empty_lines_before_help += 1
                j -= 1
            break
    
    if not found_help_section:
        print("  ⚠️  '### Need help?' section not found")
        return False
    
    if empty_lines_before_help <= 1:
        print(f"  ✅ Proper formatting: {empty_lines_before_help} empty line(s) before '### Need help?'")
        return True
    else:
        print(f"  ❌ Too many empty lines: {empty_lines_before_help} empty lines before '### Need help?'")
        return False

def test_functionality_preserved():
    """Test that the scripts still work correctly after changes."""
    print("Testing that functionality is preserved...")
    
    # Test fix_latex_escaping.py help
    try:
        result = subprocess.run(['python3', 'fix_latex_escaping.py', '--help'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("  ✅ fix_latex_escaping.py --help works")
        else:
            print("  ❌ fix_latex_escaping.py --help failed")
            return False
    except Exception as e:
        print(f"  ❌ Error testing fix_latex_escaping.py: {e}")
        return False
    
    # Test conversion_workflow.py (it runs automatically when called)
    try:
        result = subprocess.run(['python3', 'conversion_workflow.py'], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0 and 'Workflow completed successfully!' in result.stdout:
            print("  ✅ conversion_workflow.py runs successfully")
        else:
            print("  ❌ conversion_workflow.py failed or didn't complete properly")
            return False
    except Exception as e:
        print(f"  ❌ Error testing conversion_workflow.py: {e}")
        return False
    
    return True

def main():
    """Run all tests and report results."""
    print("🧪 Testing Raw String Improvements")
    print("=" * 50)
    
    tests = [
        test_raw_strings_in_fix_latex_escaping,
        test_raw_strings_in_conversion_workflow,
        test_workflow_empty_lines,
        test_functionality_preserved
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
            print()
        except Exception as e:
            print(f"  ❌ Test failed with error: {e}\n")
            results.append(False)
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    print("=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Raw string improvements are working correctly.")
        return True
    else:
        print("❌ Some tests failed. Please review the changes.")
        return False

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)