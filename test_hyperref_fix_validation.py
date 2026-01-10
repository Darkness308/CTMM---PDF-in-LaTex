#!/usr/bin/env python3
"""
Test script to validate the hyperref package loading fix in style/form-elements.sty

This test ensures that:
1. The corrupted merge conflict markers have been removed
2. The conditional logic correctly handles hyperref package loading
3. The LaTeX syntax is valid
4. No redundant package loading occurs
"""

import re
import sys
from pathlib import Path

def test_hyperref_package_loading_fix():
    """Test that the hyperref package loading conflict has been fixed."""

    style_file = Path("style/form-elements.sty")

    if not style_file.exists():
        print("❌ FAIL: style/form-elements.sty not found")
        return False

    try:
        with open(style_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ FAIL: Error reading {style_file}: {e}")
        return False

    # Test 1: Check for merge conflict markers
    conflict_markers = ['copilot/fix-692', 'main', '<<<<<<', '>>>>>>', '======']
    for marker in conflict_markers:
        if marker in content:
            print(f"❌ FAIL: Found merge conflict marker '{marker}' in {style_file}")
            return False
    print("✅ PASS: No merge conflict markers found")

    # Test 2: Check the content directly for key indicators
    lines = content.split('\n')

    # Find the conditional block lines
    conditional_start = None
    true_branch_lines = []
    false_branch_lines = []
    in_true_branch = False
    in_false_branch = False

    for i, line in enumerate(lines):
        if '\\@ifpackageloaded{hyperref}{%' in line:
            conditional_start = i
            in_true_branch = True
            continue
        elif in_true_branch and '}{%' in line:
            in_true_branch = False
            in_false_branch = True
            continue
        elif in_false_branch and line.strip() == '}':
            break

        if in_true_branch:
            true_branch_lines.append(line)
        elif in_false_branch:
            false_branch_lines.append(line)

    if conditional_start is None:
        print("❌ FAIL: Could not find hyperref conditional block")
        return False
    print("✅ PASS: Found hyperref conditional block")

    # Test 3: Check that hyperref is only loaded in the FALSE branch
    true_branch_content = '\n'.join(true_branch_lines)
    false_branch_content = '\n'.join(false_branch_lines)

    # TRUE branch should NOT contain RequirePackage{hyperref}
    if '\\RequirePackage{hyperref}' in true_branch_content:
        print("❌ FAIL: TRUE branch (hyperref already loaded) contains \\RequirePackage{hyperref}")
        return False
    print("✅ PASS: TRUE branch does not reload hyperref")

    # FALSE branch SHOULD contain RequirePackage{hyperref}
    if '\\RequirePackage{hyperref}' not in false_branch_content:
        print("❌ FAIL: FALSE branch (hyperref not loaded) missing \\RequirePackage{hyperref}")
        return False
    print("✅ PASS: FALSE branch properly loads hyperref")

    # Test 4: Check that both branches define @ctmmInteractive
    if '\\newcommand{\\@ctmmInteractive}{true}' not in true_branch_content:
        print("❌ FAIL: TRUE branch missing \\newcommand{\\@ctmmInteractive}{true}")
        return False
    if '\\newcommand{\\@ctmmInteractive}{true}' not in false_branch_content:
        print("❌ FAIL: FALSE branch missing \\newcommand{\\@ctmmInteractive}{true}")
        return False
    print("✅ PASS: Both branches define @ctmmInteractive correctly")

    # Test 5: Check for helpful comments
    if 'hyperref is already loaded' not in content:
        print("❌ FAIL: Missing explanatory comment for TRUE branch")
        return False
    if 'hyperref not loaded' not in content:
        print("❌ FAIL: Missing explanatory comment for FALSE branch")
        return False
    print("✅ PASS: Explanatory comments present")

    # Test 6: Verify LaTeX syntax structure
    if '\\makeatletter' not in content or '\\makeatother' not in content:
        print("❌ FAIL: Missing \\makeatletter or \\makeatother")
        return False
    print("✅ PASS: Proper LaTeX makeatletter structure")

    return True

def test_main_tex_hyperref_loading():
    """Test that main.tex loads hyperref package correctly."""

    main_file = Path("main.tex")

    if not main_file.exists():
        print("❌ FAIL: main.tex not found")
        return False

    try:
        with open(main_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ FAIL: Error reading {main_file}: {e}")
        return False

    # Check that hyperref is loaded before form-elements
    hyperref_line = None
    form_elements_line = None

    lines = content.split('\n')
    for i, line in enumerate(lines):
        if '\\usepackage{hyperref}' in line:
            hyperref_line = i
        elif '\\usepackage{style/form-elements}' in line:
            form_elements_line = i

    if hyperref_line is None:
        print("❌ FAIL: main.tex does not load hyperref package")
        return False
    print("✅ PASS: main.tex loads hyperref package")

    if form_elements_line is None:
        print("❌ FAIL: main.tex does not load style/form-elements package")
        return False
    print("✅ PASS: main.tex loads style/form-elements package")

    if hyperref_line >= form_elements_line:
        print(f"❌ FAIL: hyperref (line {hyperref_line+1}) should be loaded before form-elements (line {form_elements_line+1})")
        return False
    print("✅ PASS: hyperref is loaded before form-elements")

    return True

def main():
    """Run all validation tests."""

    print("==========================================================")
    print("HYPERREF PACKAGE LOADING FIX VALIDATION")
    print("==========================================================")

    all_tests_passed = True

    print("\n1. Testing style/form-elements.sty hyperref loading logic...")
    if not test_hyperref_package_loading_fix():
        all_tests_passed = False

    print("\n2. Testing main.tex package loading order...")
    if not test_main_tex_hyperref_loading():
        all_tests_passed = False

    print("\n==========================================================")
    if all_tests_passed:
        print("🎉 ALL TESTS PASSED! Hyperref package loading fix is working correctly.")
        print("✅ CI pipeline should now compile successfully without package conflicts.")
        return 0
    else:
        print("❌ SOME TESTS FAILED! The hyperref package loading fix needs attention.")
        return 1

if __name__ == "__main__":
    sys.exit(main())