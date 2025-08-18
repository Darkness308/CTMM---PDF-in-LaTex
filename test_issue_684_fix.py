#!/usr/bin/env python3
"""
Test script to validate Issue #684 fix - Hyperref package loading conflict resolution.

This test validates that the hyperref package loading issue in style/form-elements.sty
has been properly resolved and won't cause CI pipeline failures.
"""

import os
import sys
import re
from pathlib import Path

def test_hyperref_conditional_logic():
    """Test that form-elements.sty has correct hyperref conditional loading logic."""
    print("\n🔍 TESTING HYPERREF CONDITIONAL LOGIC")
    print("=" * 60)
    
    form_elements_path = Path("style/form-elements.sty")
    
    if not form_elements_path.exists():
        print("❌ ERROR: style/form-elements.sty not found")
        return False
    
    with open(form_elements_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the conditional logic section - need a more flexible pattern
    # Look for the @ifpackageloaded section and extract the branches
    start_pattern = r'\\@ifpackageloaded\{hyperref\}\{'
    start_match = re.search(start_pattern, content)
    
    if not start_match:
        print("❌ ERROR: Could not find \\@ifpackageloaded{hyperref} conditional")
        return False
    
    # Extract the conditional section manually by counting braces
    start_pos = start_match.end() - 1  # Position of the opening brace
    brace_count = 0
    true_branch_start = start_pos + 1
    true_branch_end = None
    false_branch_start = None
    false_branch_end = None
    
    for i, char in enumerate(content[start_pos:], start_pos):
        if char == '{':
            brace_count += 1
        elif char == '}':
            brace_count -= 1
            if brace_count == 0 and true_branch_end is None:
                true_branch_end = i
                # Find the next opening brace for false branch
                next_brace = content.find('{', i)
                if next_brace != -1:
                    false_branch_start = next_brace + 1
            elif brace_count == 0 and false_branch_start is not None:
                false_branch_end = i
                break
    
    if true_branch_end is None or false_branch_start is None or false_branch_end is None:
        print("❌ ERROR: Could not parse conditional structure")
        return False
    
    true_branch = content[true_branch_start:true_branch_end].strip()
    false_branch = content[false_branch_start:false_branch_end].strip()
    
    print("📋 Found conditional logic:")
    print(f"   True branch (hyperref already loaded): {true_branch[:50]}...")
    print(f"   False branch (hyperref not loaded): {false_branch[:50]}...")
    
    # Check that hyperref is NOT loaded in the true branch
    if "\\RequirePackage{hyperref}" in true_branch:
        print("❌ FAIL: True branch incorrectly loads hyperref when already loaded")
        return False
    else:
        print("✅ PASS: True branch correctly skips hyperref loading")
    
    # Check that hyperref IS loaded in the false branch
    if "\\RequirePackage{hyperref}" not in false_branch:
        print("❌ FAIL: False branch doesn't load hyperref when needed")
        return False
    else:
        print("✅ PASS: False branch correctly loads hyperref")
    
    # Check that both branches set the interactive flag
    if "\\newcommand{\\@ctmmInteractive}{true}" not in true_branch:
        print("❌ FAIL: True branch doesn't set interactive flag")
        return False
    
    if "\\newcommand{\\@ctmmInteractive}{true}" not in false_branch:
        print("❌ FAIL: False branch doesn't set interactive flag")
        return False
    
    print("✅ PASS: Both branches correctly set interactive flag")
    
    return True

def test_main_tex_package_order():
    """Test that main.tex loads hyperref before form-elements.sty."""
    print("\n📦 TESTING PACKAGE LOADING ORDER")
    print("=" * 60)
    
    main_tex_path = Path("main.tex")
    
    if not main_tex_path.exists():
        print("❌ ERROR: main.tex not found")
        return False
    
    with open(main_tex_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    hyperref_line = None
    form_elements_line = None
    
    for i, line in enumerate(lines):
        if "\\usepackage{hyperref}" in line:
            hyperref_line = i + 1
            print(f"✅ Found hyperref package at line {hyperref_line}")
        elif "\\usepackage{style/form-elements}" in line:
            form_elements_line = i + 1
            print(f"✅ Found form-elements package at line {form_elements_line}")
    
    if hyperref_line is None:
        print("❌ ERROR: hyperref package not found in main.tex")
        return False
    
    if form_elements_line is None:
        print("❌ ERROR: form-elements package not found in main.tex")
        return False
    
    if hyperref_line < form_elements_line:
        print("✅ PASS: hyperref is loaded before form-elements (correct order)")
        return True
    else:
        print("❌ FAIL: form-elements is loaded before hyperref (incorrect order)")
        return False

def test_form_elements_comments():
    """Test that form-elements.sty has proper explanatory comments."""
    print("\n📝 TESTING EXPLANATORY COMMENTS")
    print("=" * 60)
    
    form_elements_path = Path("style/form-elements.sty")
    
    with open(form_elements_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for explanatory comments
    expected_comments = [
        "hyperref is already loaded",
        "hyperref is not loaded",
        "just set interactive mode",
        "load it and set interactive mode"
    ]
    
    comments_found = 0
    for comment in expected_comments:
        if comment in content:
            print(f"✅ Found comment: {comment}")
            comments_found += 1
        else:
            print(f"❌ Missing comment: {comment}")
    
    if comments_found >= 2:  # At least some explanatory comments
        print("✅ PASS: Adequate explanatory comments found")
        return True
    else:
        print("❌ FAIL: Insufficient explanatory comments")
        return False

def test_no_duplicate_hyperref_loading():
    """Test that there's no duplicate hyperref loading in any style files."""
    print("\n🔄 TESTING FOR DUPLICATE HYPERREF LOADING")
    print("=" * 60)
    
    style_dir = Path("style")
    if not style_dir.exists():
        print("❌ ERROR: style/ directory not found")
        return False
    
    hyperref_loads = []
    
    for style_file in style_dir.glob("*.sty"):
        with open(style_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Count hyperref loading occurrences
        hyperref_pattern = r'\\(?:RequirePackage|usepackage)\{hyperref\}'
        matches = re.findall(hyperref_pattern, content)
        
        if matches:
            count = len(matches)
            hyperref_loads.append((style_file.name, count))
            print(f"📋 {style_file.name}: {count} hyperref load(s)")
    
    # Check form-elements.sty specifically
    form_elements_loads = next((count for name, count in hyperref_loads if name == "form-elements.sty"), 0)
    
    if form_elements_loads == 0:
        print("✅ PASS: form-elements.sty doesn't unconditionally load hyperref")
        return True
    elif form_elements_loads == 1:
        # Check if it's within the conditional
        form_elements_path = Path("style/form-elements.sty")
        with open(form_elements_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if the RequirePackage is in the false branch of the conditional
        with open(form_elements_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Find the conditional section
        start_pattern = r'\\@ifpackageloaded\{hyperref\}\{'
        start_match = re.search(start_pattern, content)
        
        if start_match:
            # Parse the conditional structure manually
            start_pos = start_match.end() - 1  # Position of the opening brace
            brace_count = 0
            true_branch_end = None
            false_branch_start = None
            false_branch_end = None
            
            for i, char in enumerate(content[start_pos:], start_pos):
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0 and true_branch_end is None:
                        true_branch_end = i
                        # Find the next opening brace for false branch
                        next_brace = content.find('{', i)
                        if next_brace != -1:
                            false_branch_start = next_brace + 1
                    elif brace_count == 0 and false_branch_start is not None:
                        false_branch_end = i
                        break
            
            if false_branch_start and false_branch_end:
                false_branch = content[false_branch_start:false_branch_end]
                if "\\RequirePackage{hyperref}" in false_branch:
                    print("✅ PASS: hyperref loading is properly conditional (only in false branch)")
                    return True
    
    print(f"❌ FAIL: Improper hyperref loading detected in form-elements.sty")
    return False

def run_all_tests():
    """Run all Issue #684 validation tests."""
    print("🎯 ISSUE #684 HYPERREF PACKAGE LOADING FIX VALIDATION")
    print("=" * 80)
    print("Testing the resolution of LaTeX compilation failures caused by")
    print("hyperref package loading conflicts in GitHub Actions CI pipeline.")
    print("=" * 80)
    
    tests = [
        ("Hyperref Conditional Logic", test_hyperref_conditional_logic),
        ("Package Loading Order", test_main_tex_package_order),
        ("Explanatory Comments", test_form_elements_comments),
        ("No Duplicate Loading", test_no_duplicate_hyperref_loading)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'=' * 20} {test_name} {'=' * 20}")
        try:
            if test_func():
                print(f"✅ {test_name}: PASSED")
                passed += 1
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
    
    print("\n" + "=" * 80)
    print("ISSUE #684 VALIDATION SUMMARY")
    print("=" * 80)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Issue #684 fix is working correctly.")
        print("✅ GitHub Actions CI pipeline should no longer fail due to hyperref conflicts.")
        return True
    else:
        print("❌ Some tests failed. Issue #684 fix may need attention.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)