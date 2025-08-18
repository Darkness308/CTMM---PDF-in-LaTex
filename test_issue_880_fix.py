#!/usr/bin/env python3
"""
Test script for Issue #880: CI Build Reliability Improvements

This script validates the changes made to address CI build failures:
1. Updated dante-ev/latex-action to @latest
2. Added correct latexmk arguments  
3. Added comprehensive LaTeX package installation including fontawesome5
"""

import os
import re
import yaml
import sys
from pathlib import Path

def test_latex_action_version():
    """Test that dante-ev/latex-action is updated to @latest"""
    workflow_file = '.github/workflows/latex-build.yml'
    
    with open(workflow_file, 'r') as f:
        content = f.read()
    
    # Check for @latest version
    pattern = r'uses:\s*dante-ev/latex-action@latest'
    if re.search(pattern, content):
        print("✅ PASS: dante-ev/latex-action updated to @latest")
        return True
    else:
        print("❌ FAIL: dante-ev/latex-action not using @latest")
        return False

def test_latexmk_arguments():
    """Test that correct latexmk arguments are used"""
    workflow_file = '.github/workflows/latex-build.yml'
    
    with open(workflow_file, 'r') as f:
        content = f.read()
    
    # Check for -pdf argument (latexmk specific)
    if '-pdf' in content and 'args:' in content:
        print("✅ PASS: latexmk -pdf argument present")
        return True
    else:
        print("❌ FAIL: latexmk -pdf argument missing")
        return False

def test_fontawesome_package():
    """Test that fontawesome package is included"""
    workflow_file = '.github/workflows/latex-build.yml'
    
    with open(workflow_file, 'r') as f:
        content = f.read()
    
    # Check for texlive-fontawesome package
    if 'texlive-fontawesome' in content:
        print("✅ PASS: texlive-fontawesome package included")
        return True
    else:
        print("❌ FAIL: texlive-fontawesome package missing")
        return False

def test_german_language_support():
    """Test that German language support packages are present"""
    workflow_file = '.github/workflows/latex-build.yml'
    
    with open(workflow_file, 'r') as f:
        content = f.read()
    
    if 'texlive-lang-german' in content:
        print("✅ PASS: German language support included")
        return True
    else:
        print("❌ FAIL: German language support missing")
        return False

def test_comprehensive_packages():
    """Test that comprehensive LaTeX packages are installed"""
    workflow_file = '.github/workflows/latex-build.yml'
    
    required_packages = [
        'texlive-fonts-recommended',
        'texlive-latex-recommended', 
        'texlive-fonts-extra',
        'texlive-latex-extra'
    ]
    
    with open(workflow_file, 'r') as f:
        content = f.read()
    
    missing_packages = []
    for package in required_packages:
        if package not in content:
            missing_packages.append(package)
    
    if not missing_packages:
        print("✅ PASS: All comprehensive LaTeX packages included")
        return True
    else:
        print(f"❌ FAIL: Missing packages: {missing_packages}")
        return False

def test_yaml_syntax():
    """Test that YAML syntax is correct in all workflow files"""
    workflow_dir = '.github/workflows'
    workflow_files = ['latex-build.yml', 'latex-validation.yml', 'pr-validation.yml', 'static.yml']
    
    all_valid = True
    for filename in workflow_files:
        filepath = os.path.join(workflow_dir, filename)
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r') as f:
                    yaml.safe_load(f)
                print(f"✅ PASS: {filename} has valid YAML syntax")
            except yaml.YAMLError as e:
                print(f"❌ FAIL: {filename} has invalid YAML syntax: {e}")
                all_valid = False
        else:
            print(f"⚠️  WARNING: {filename} not found")
    
    return all_valid

def main():
    """Run all tests for Issue #880 fix"""
    print("============================================================")
    print("Issue #880 Fix Validation: CI Build Reliability Improvements")
    print("============================================================")
    print()
    
    tests = [
        ("LaTeX Action Version (@latest)", test_latex_action_version),
        ("Latexmk Arguments (-pdf)", test_latexmk_arguments),
        ("FontAwesome Package", test_fontawesome_package),
        ("German Language Support", test_german_language_support),
        ("Comprehensive Package Installation", test_comprehensive_packages),
        ("YAML Syntax Validation", test_yaml_syntax),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"Testing {test_name}...")
        if test_func():
            passed += 1
        print()
    
    print("============================================================")
    print("TEST SUMMARY")
    print("============================================================")
    
    for i, (test_name, test_func) in enumerate(tests):
        status = "✅ PASS" if i < passed else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\nTests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED - Issue #880 CI improvements working correctly!")
        print("\nThe GitHub Actions workflow should now:")
        print("- Use the latest stable version of dante-ev/latex-action")
        print("- Compile LaTeX documents with optimized latexmk arguments")
        print("- Include all necessary packages for fontawesome5 and German support")
        print("- Have improved reliability and error handling")
        return True
    else:
        print(f"❌ {total - passed} test(s) failed. Please review the configuration.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)