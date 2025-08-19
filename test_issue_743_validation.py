#!/usr/bin/env python3
"""
Test validation for Issue #743 - CI Insights Report Failure
Validates that all necessary components are in place for successful CI builds.
"""

import os
import sys
import yaml
import re

def test_pifont_dependency():
    """Test that pifont dependency is properly configured in workflow."""
    print("🔍 Testing pifont package dependency configuration...")
    
    workflow_path = ".github/workflows/latex-build.yml"
    if not os.path.exists(workflow_path):
        print(f"❌ FAIL: Workflow file {workflow_path} not found")
        return False
    
    with open(workflow_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for texlive-pstricks which contains pifont
    if 'texlive-pstricks' not in content:
        print("❌ FAIL: texlive-pstricks package not found in workflow")
        return False
    
    print("✅ PASS: texlive-pstricks package found in workflow (provides pifont)")
    return True

def test_form_elements_style():
    """Test that form-elements.sty properly requires pifont."""
    print("🔍 Testing form-elements.sty pifont usage...")
    
    style_path = "style/form-elements.sty"
    if not os.path.exists(style_path):
        print(f"❌ FAIL: Style file {style_path} not found")
        return False
    
    with open(style_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for pifont requirement
    if '\\RequirePackage{pifont}' not in content:
        print("❌ FAIL: pifont package not required in form-elements.sty")
        return False
    
    # Check for ding usage
    if '\\ding{51}' not in content:
        print("❌ FAIL: \\ding{51} symbol not found in form-elements.sty")
        return False
    
    print("✅ PASS: form-elements.sty properly requires and uses pifont package")
    return True

def test_workflow_syntax():
    """Test that workflow YAML syntax is valid."""
    print("🔍 Testing GitHub Actions workflow syntax...")
    
    workflow_files = [
        ".github/workflows/latex-build.yml",
        ".github/workflows/latex-validation.yml", 
        ".github/workflows/pr-validation.yml",
        ".github/workflows/static.yml"
    ]
    
    for workflow_file in workflow_files:
        if not os.path.exists(workflow_file):
            print(f"⚠️  WARNING: Workflow file {workflow_file} not found")
            continue
            
        try:
            with open(workflow_file, 'r', encoding='utf-8') as f:
                yaml.safe_load(f)
            print(f"✅ PASS: {workflow_file} has valid YAML syntax")
        except yaml.YAMLError as e:
            print(f"❌ FAIL: {workflow_file} has invalid YAML syntax: {e}")
            return False
    
    return True

def test_action_versions():
    """Test that GitHub Actions versions are properly pinned."""
    print("🔍 Testing GitHub Actions version pinning...")
    
    workflow_path = ".github/workflows/latex-build.yml"
    if not os.path.exists(workflow_path):
        print(f"❌ FAIL: Workflow file {workflow_path} not found")
        return False
    
    with open(workflow_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for proper version pinning
    action_pattern = r'uses:\s+([^@\s]+)@([^\s]+)'
    actions = re.findall(action_pattern, content)
    
    for action, version in actions:
        if version == 'latest':
            print(f"❌ FAIL: Action {action} uses @latest tag")
            return False
        if version.startswith('v'):
            print(f"✅ PASS: Action {action}@{version} properly version-pinned")
        else:
            print(f"⚠️  WARNING: Action {action}@{version} has unusual version format")
    
    return True

def test_latex_packages():
    """Test that all required LaTeX packages are listed in workflow."""
    print("🔍 Testing LaTeX package installation configuration...")
    
    workflow_path = ".github/workflows/latex-build.yml"
    if not os.path.exists(workflow_path):
        print(f"❌ FAIL: Workflow file {workflow_path} not found")
        return False
    
    with open(workflow_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    required_packages = [
        'texlive-lang-german',
        'texlive-fonts-recommended', 
        'texlive-latex-recommended',
        'texlive-fonts-extra',
        'texlive-latex-extra',
        'texlive-science',
        'texlive-pstricks'  # Contains pifont
    ]
    
    missing_packages = []
    for package in required_packages:
        if package not in content:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ FAIL: Missing LaTeX packages: {', '.join(missing_packages)}")
        return False
    
    print("✅ PASS: All required LaTeX packages found in workflow")
    return True

def test_build_system_health():
    """Test that CTMM build system components are working."""
    print("🔍 Testing CTMM build system health...")
    
    # Test that main.tex exists and is readable
    if not os.path.exists("main.tex"):
        print("❌ FAIL: main.tex not found")
        return False
    
    # Test that style files exist
    style_files = ["style/ctmm-design.sty", "style/form-elements.sty", "style/ctmm-diagrams.sty"]
    for style_file in style_files:
        if not os.path.exists(style_file):
            print(f"❌ FAIL: Style file {style_file} not found")
            return False
    
    print("✅ PASS: CTMM build system components present")
    return True

def main():
    """Run all validation tests for Issue #743."""
    print("=" * 60)
    print("Issue #743 CI Failure Validation")
    print("=" * 60)
    
    tests = [
        ("pifont dependency", test_pifont_dependency),
        ("form-elements style", test_form_elements_style), 
        ("workflow syntax", test_workflow_syntax),
        ("action versions", test_action_versions),
        ("LaTeX packages", test_latex_packages),
        ("build system health", test_build_system_health)
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n--- Testing {test_name} ---")
        if test_func():
            passed_tests += 1
        else:
            print(f"❌ Test '{test_name}' failed")
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    for (test_name, _), result in zip(tests, test_results):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    for (test_name, _), result in zip(tests, test_results):
        status = "✅ PASS" if result else "❌ FAIL"
    print(f"\nTests passed: {passed_tests}/{total_tests}")
    
    if passed_tests == total_tests:
        print("🎉 ALL TESTS PASSED - CI should work correctly!")
        print("\nThe GitHub Actions workflow should now be able to:")
        print("- Install all required LaTeX packages including pifont")
        print("- Successfully compile LaTeX files with form elements")
        print("- Complete the PDF build without package errors")
        return True
    else:
        print("❌ SOME TESTS FAILED - CI may still have issues")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)