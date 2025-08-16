#!/usr/bin/env python3
"""
Validation Test for Issue #684 - Hyperref Package Loading Conflict Resolution

This test validates that the hyperref package loading conflict has been properly
resolved in style/form-elements.sty. The fix ensures that hyperref is only loaded
when not already present, preventing LaTeX compilation failures in CI.
"""

import re
import sys
from pathlib import Path

def test_hyperref_conditional_logic():
    """Test that hyperref conditional loading is correctly implemented."""
    print("🔍 Testing Hyperref Conditional Logic Resolution")
    print("=" * 60)
    
    form_elements_path = Path("style/form-elements.sty")
    
    if not form_elements_path.exists():
        print("❌ ERROR: style/form-elements.sty not found")
        return False
        
    with open(form_elements_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Test 1: Find the conditional block
    if '@ifpackageloaded{hyperref}' not in content:
        print("❌ ERROR: Hyperref conditional loading not found")
        return False
    print("✅ Found hyperref conditional loading block")
    
    # Test 2: Extract and analyze the conditional logic
    lines = content.split('\n')
    conditional_start = None
    
    for i, line in enumerate(lines):
        if '@ifpackageloaded{hyperref}' in line:
            conditional_start = i
            break
    
    if conditional_start is None:
        print("❌ ERROR: Could not locate conditional logic")
        return False
        
    # Extract the relevant lines (typically 7-8 lines)
    conditional_block = lines[conditional_start:conditional_start + 8]
    
    print(f"📍 Found conditional block at line {conditional_start + 1}:")
    for i, line in enumerate(conditional_block):
        print(f"   {conditional_start + i + 1:2d}. {line.rstrip()}")
    
    # Test 3: Analyze true branch (hyperref already loaded)
    # Lines 15-16: true branch content
    # Lines 18-20: false branch content
    true_branch_lines = [lines[conditional_start + 1].strip(), lines[conditional_start + 2].strip()]
    false_branch_lines = [lines[conditional_start + 4].strip(), lines[conditional_start + 5].strip(), lines[conditional_start + 6].strip()]
    
    print(f"\n📊 Conditional Logic Analysis:")
    print(f"   True branch (hyperref already loaded): {len(true_branch_lines)} lines")
    print(f"   False branch (hyperref not loaded): {len(false_branch_lines)} lines")
    
    # Test 4: Validate true branch doesn't load hyperref
    true_branch_loads_hyperref = any('RequirePackage{hyperref}' in line for line in true_branch_lines)
    if true_branch_loads_hyperref:
        print("❌ CRITICAL ERROR: True branch incorrectly loads hyperref!")
        print("   This would cause the original package conflict issue!")
        return False
    else:
        print("✅ True branch correctly avoids loading hyperref")
    
    # Test 5: Validate false branch loads hyperref
    false_branch_loads_hyperref = any('RequirePackage{hyperref}' in line for line in false_branch_lines)
    if not false_branch_loads_hyperref:
        print("❌ ERROR: False branch doesn't load hyperref!")
        print("   This would break functionality when hyperref isn't pre-loaded!")
        return False
    else:
        print("✅ False branch correctly loads hyperref when needed")
    
    # Test 6: Check for explanatory comments
    has_explanatory_comments = (
        any('already loaded' in line.lower() for line in true_branch_lines) and
        any('not loaded' in line.lower() for line in false_branch_lines)
    )
    if has_explanatory_comments:
        print("✅ Explanatory comments present to prevent future confusion")
    else:
        print("⚠️  Warning: Missing explanatory comments")
    
    # Test 7: Validate both branches set the interactive flag
    true_sets_flag = any('@ctmmInteractive' in line for line in true_branch_lines)
    false_sets_flag = any('@ctmmInteractive' in line for line in false_branch_lines)
    
    if true_sets_flag and false_sets_flag:
        print("✅ Both branches correctly set @ctmmInteractive flag")
    else:
        print("❌ ERROR: Missing @ctmmInteractive flag in one or both branches")
        return False
    
    return True

def test_main_tex_package_order():
    """Test that main.tex loads hyperref before form-elements."""
    print("\n🔍 Testing Package Loading Order in main.tex")
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
        if '\\usepackage{hyperref}' in line:
            hyperref_line = i + 1
        elif '\\usepackage{style/form-elements}' in line:
            form_elements_line = i + 1
    
    if hyperref_line is None:
        print("❌ ERROR: hyperref package not found in main.tex")
        return False
        
    if form_elements_line is None:
        print("❌ ERROR: form-elements package not found in main.tex")
        return False
        
    print(f"📍 Package loading order:")
    print(f"   hyperref loaded at line {hyperref_line}")
    print(f"   form-elements loaded at line {form_elements_line}")
    
    if hyperref_line < form_elements_line:
        print("✅ Correct loading order: hyperref loaded before form-elements")
        return True
    else:
        print("❌ ERROR: Incorrect loading order - form-elements loaded before hyperref!")
        print("   This would trigger the false branch and cause unnecessary package loading")
        return False

def test_documentation_completeness():
    """Test that comprehensive documentation exists for this fix."""
    print("\n🔍 Testing Issue #684 Documentation Completeness")
    print("=" * 60)
    
    doc_path = Path("ISSUE_684_RESOLUTION.md")
    if not doc_path.exists():
        print("❌ ERROR: ISSUE_684_RESOLUTION.md not found")
        return False
        
    with open(doc_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    required_sections = [
        "Problem Statement",
        "Root Cause Analysis", 
        "Solution Implemented",
        "Prevention Guidelines"
    ]
    
    missing_sections = []
    for section in required_sections:
        if section not in content:
            missing_sections.append(section)
    
    if missing_sections:
        print(f"❌ ERROR: Missing documentation sections: {missing_sections}")
        return False
    
    # Check for specific key content
    checks = [
        ("package loading conflict", "Package loading conflict explanation"),
        ("conditional logic", "Conditional logic discussion"),
        ("GitHub Actions", "CI pipeline context"),
        ("RequirePackage{hyperref}", "Technical implementation details")
    ]
    
    for check_text, description in checks:
        if check_text.lower() in content.lower():
            print(f"✅ Found {description}")
        else:
            print(f"⚠️  Missing {description}")
    
    print(f"✅ Documentation file exists with {len(content.split())} words")
    return True

def main():
    """Run all validation tests for Issue #684 resolution."""
    print("🚀 Issue #684 Hyperref Package Conflict Resolution Validation")
    print("=" * 80)
    
    tests = [
        ("Hyperref Conditional Logic", test_hyperref_conditional_logic),
        ("Package Loading Order", test_main_tex_package_order),
        ("Documentation Completeness", test_documentation_completeness)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ ERROR in {test_name}: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 80)
    print("🏁 VALIDATION SUMMARY")
    print("=" * 80)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\nResults: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("\n🎉 All validation tests PASSED!")
        print("✅ Issue #684 hyperref package conflict has been properly resolved")
        return True
    else:
        print(f"\n⚠️  {len(tests) - passed} validation tests FAILED")
        print("❌ Issue #684 resolution needs attention")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)