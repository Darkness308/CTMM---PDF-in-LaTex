#!/usr/bin/env python3
"""
Test script to validate Issue #857 fix for GitHub Actions LaTeX build configuration.

This script verifies the fixes mentioned in the PR overview:
- Updated dante-ev/latex-action from v2.0.0 to @latest
- Proper YAML syntax with quoted 'on' keyword
- Comprehensive LaTeX package installation
"""

import os
import re
import yaml
import subprocess

def test_latex_action_version():
    """Test that latex-build.yml uses dante-ev/latex-action@latest."""
    print("🧪 Testing LaTeX action version...")
    
    workflow_path = ".github/workflows/latex-build.yml"
    if not os.path.exists(workflow_path):
        print("❌ Workflow file not found")
        return False
    
    with open(workflow_path, 'r') as f:
        content = f.read()
    
    # Check for @latest version
    if "dante-ev/latex-action@latest" in content:
        print("✅ PASS: Using dante-ev/latex-action@latest")
        return True
    elif "dante-ev/latex-action@v2" in content:
        print("❌ FAIL: Still using old version @v2")
        return False
    else:
        print("❌ FAIL: dante-ev/latex-action not found")
        return False

def test_yaml_syntax():
    """Test that workflow YAML syntax is correct with quoted 'on' keyword."""
    print("\n🧪 Testing YAML syntax...")
    
    workflow_files = [
        ".github/workflows/latex-build.yml",
        ".github/workflows/latex-validation.yml", 
        ".github/workflows/static.yml"
    ]
    
    for workflow_path in workflow_files:
        if not os.path.exists(workflow_path):
            print(f"⚠️  Workflow file not found: {workflow_path}")
            continue
            
        try:
            with open(workflow_path, 'r') as f:
                content = f.read()
                
            # Parse YAML to check structure
            parsed = yaml.safe_load(content)
            
            # Check if 'on' is properly handled
            if 'on' in parsed:
                print(f"✅ PASS: {workflow_path} has correct YAML syntax")
            else:
                print(f"❌ FAIL: {workflow_path} missing 'on' trigger")
                return False
                
        except yaml.YAMLError as e:
            print(f"❌ FAIL: {workflow_path} has invalid YAML syntax: {e}")
            return False
    
    return True

def test_latex_packages():
    """Test that comprehensive LaTeX packages are installed."""
    print("\n🧪 Testing LaTeX package configuration...")
    
    workflow_path = ".github/workflows/latex-build.yml"
    if not os.path.exists(workflow_path):
        print("❌ Workflow file not found")
        return False
    
    with open(workflow_path, 'r') as f:
        content = f.read()
    
    required_packages = [
        "texlive-lang-german",      # German language support
        "texlive-fonts-extra",      # Extra fonts including fontawesome5
        "texlive-pstricks",         # PSTricks for additional graphics/symbols
        "texlive-latex-extra",      # Extra LaTeX packages
    ]
    
    missing_packages = []
    for package in required_packages:
        if package not in content:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ FAIL: Missing packages: {missing_packages}")
        return False
    else:
        print("✅ PASS: All required LaTeX packages are configured")
        return True

def test_workflow_compilation_args():
    """Test that workflow uses correct pdflatex arguments."""
    print("\n🧪 Testing LaTeX compilation arguments...")
    
    workflow_path = ".github/workflows/latex-build.yml"
    if not os.path.exists(workflow_path):
        print("❌ Workflow file not found")
        return False
    
    with open(workflow_path, 'r') as f:
        content = f.read()
    
    # Check for correct arguments (no -pdf flag)
    required_args = [
        "-interaction=nonstopmode",
        "-halt-on-error",
        "-shell-escape"
    ]
    
    missing_args = []
    for arg in required_args:
        if arg not in content:
            missing_args.append(arg)
    
    # Check that problematic -pdf argument is not present
    if "-pdf" in content and "-interaction=nonstopmode" in content:
        # Check if it's the problematic standalone -pdf
        args_line = re.search(r'args:\s*(.+)', content)
        if args_line and "-pdf " in args_line.group(1):
            print("❌ FAIL: Problematic -pdf argument found")
            return False
    
    if missing_args:
        print(f"❌ FAIL: Missing arguments: {missing_args}")
        return False
    else:
        print("✅ PASS: LaTeX compilation arguments are correct")
        return True

def main():
    """Run all validation tests."""
    print("=" * 70)
    print("Issue #857 Fix Validation: GitHub Actions LaTeX Build Configuration")
    print("=" * 70)
    
    tests = [
        test_latex_action_version,
        test_yaml_syntax,
        test_latex_packages,
        test_workflow_compilation_args
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 70)
    print(f"VALIDATION SUMMARY: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED - Issue #857 is properly resolved!")
        print("GitHub Actions LaTeX build configuration is ready for CI.")
        return True
    else:
        print("❌ SOME TESTS FAILED - Issue #857 not fully resolved")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)