#!/usr/bin/env python3
"""
Validation script for Issue #684: Hyperref Package Loading Fix
This script validates that the hyperref package loading conflict has been resolved.
"""

import re
import os
import sys

def validate_hyperref_fix():
    """Comprehensive validation of the hyperref package loading fix."""
    
    print("=" * 80)
    print("VALIDATION: Issue #684 - Hyperref Package Loading Fix")
    print("=" * 80)
    
    results = {
        'conditional_logic': False,
        'comment_clarity': False,
        'single_load_point': False,
        'main_tex_structure': False,
        'documentation_exists': False
    }
    
    # 1. Check form-elements.sty for correct conditional logic
    print("\n1. 📋 Validating form-elements.sty conditional logic...")
    print("-" * 60)
    
    form_elements_path = "style/form-elements.sty"
    if not os.path.exists(form_elements_path):
        print(f"❌ CRITICAL: {form_elements_path} not found!")
        return False
    
    with open(form_elements_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for the correct conditional pattern
    conditional_pattern = r'\\@ifpackageloaded\{hyperref\}\{%\s*%[^\}]*\s*\\newcommand\{\\@ctmmInteractive\}\{true\}%\s*\}\{%\s*%[^\}]*\s*\\RequirePackage\{hyperref\}%\s*\\newcommand\{\\@ctmmInteractive\}\{true\}%\s*\}'
    
    if r'\@ifpackageloaded{hyperref}' in content:
        print("✅ Found conditional package loading logic")
        results['conditional_logic'] = True
        
        # Check that hyperref is only loaded in the FALSE branch
        lines = content.split('\n')
        in_true_branch = False
        in_false_branch = False
        hyperref_in_true_branch = False
        hyperref_in_false_branch = False
        
        for line in lines:
            line = line.strip()
            if r'\@ifpackageloaded{hyperref}{%' in line:
                in_true_branch = True
                in_false_branch = False
            elif in_true_branch and '}{% ' in line:
                in_true_branch = False
                in_false_branch = True
            elif in_true_branch and line == '}{%':
                in_true_branch = False
                in_false_branch = True
            elif in_false_branch and line == '}':
                in_false_branch = False
            
            if in_true_branch and r'\RequirePackage{hyperref}' in line:
                hyperref_in_true_branch = True
            if in_false_branch and r'\RequirePackage{hyperref}' in line:
                hyperref_in_false_branch = True
        
        if not hyperref_in_true_branch and hyperref_in_false_branch:
            print("✅ Hyperref only loaded when NOT already present (correct!)")
            results['single_load_point'] = True
        else:
            print("❌ PROBLEM: Hyperref loading logic incorrect")
            print(f"   - In true branch: {hyperref_in_true_branch}")
            print(f"   - In false branch: {hyperref_in_false_branch}")
    else:
        print("❌ Conditional package loading logic not found")
    
    # 2. Check for explanatory comments
    print("\n2. 💬 Validating explanatory comments...")
    print("-" * 60)
    
    if "% hyperref is already loaded" in content and "% hyperref is not loaded" in content:
        print("✅ Clear explanatory comments found")
        results['comment_clarity'] = True
    else:
        print("❌ Missing or unclear explanatory comments")
    
    # 3. Check main.tex for proper package loading order
    print("\n3. 📄 Validating main.tex package loading order...")
    print("-" * 60)
    
    main_tex_path = "main.tex"
    if os.path.exists(main_tex_path):
        with open(main_tex_path, 'r', encoding='utf-8') as f:
            main_content = f.read()
        
        # Check that hyperref is loaded before form-elements
        hyperref_pos = main_content.find(r'\usepackage{hyperref}')
        form_elements_pos = main_content.find(r'\usepackage{style/form-elements}')
        
        if hyperref_pos != -1 and form_elements_pos != -1:
            if hyperref_pos < form_elements_pos:
                print("✅ Package loading order: hyperref before form-elements (correct!)")
                results['main_tex_structure'] = True
            else:
                print("❌ PROBLEM: form-elements loaded before hyperref")
        else:
            print("⚠️  Could not verify package loading order")
    else:
        print("❌ main.tex not found")
    
    # 4. Check for documentation
    print("\n4. 📚 Validating documentation...")
    print("-" * 60)
    
    doc_path = "ISSUE_684_RESOLUTION.md"
    if os.path.exists(doc_path):
        print("✅ Issue resolution documentation exists")
        results['documentation_exists'] = True
        
        with open(doc_path, 'r', encoding='utf-8') as f:
            doc_content = f.read()
        
        if "hyperref package loading conflict" in doc_content.lower():
            print("✅ Documentation covers the hyperref conflict issue")
        if "conditional logic" in doc_content.lower():
            print("✅ Documentation explains conditional logic fix")
    else:
        print("❌ Issue resolution documentation missing")
    
    # 5. Summary and recommendations
    print("\n" + "=" * 80)
    print("VALIDATION SUMMARY")
    print("=" * 80)
    
    total_checks = len(results)
    passed_checks = sum(results.values())
    
    print(f"\nPassed: {passed_checks}/{total_checks} validation checks")
    
    for check, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status}: {check.replace('_', ' ').title()}")
    
    if passed_checks == total_checks:
        print(f"\n🎉 SUCCESS: All validation checks passed!")
        print("   The hyperref package loading fix is correctly implemented.")
        return True
    else:
        print(f"\n⚠️  WARNING: {total_checks - passed_checks} validation checks failed.")
        print("   The fix may need additional work.")
        return False

if __name__ == "__main__":
    # Ensure we're in the repository root
    if not os.path.exists('style/form-elements.sty'):
        print("Error: Run this script from the repository root directory")
        sys.exit(1)
    
    success = validate_hyperref_fix()
    sys.exit(0 if success else 1)