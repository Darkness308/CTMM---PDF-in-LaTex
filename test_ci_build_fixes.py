#!/usr/bin/env python3
"""
Test script to validate CI build fixes for LaTeX workflow
Verifies GitHub Actions configuration for successful PDF generation
"""

import yaml
import os
import sys
import re

def test_latex_action_update():
    """Test that dante-ev/latex-action is updated to @latest"""
    
    workflow_path = '.github/workflows/latex-build.yml'
    
    if not os.path.exists(workflow_path):
        print(f"❌ ERROR: Workflow file {workflow_path} not found")
        return False
    
    try:
        with open(workflow_path, 'r') as f:
            workflow_content = yaml.safe_load(f)
    except Exception as e:
        print(f"❌ ERROR: Failed to parse {workflow_path}: {e}")
        return False
    
    # Find the LaTeX action step
    jobs = workflow_content.get('jobs', {})
    build_job = jobs.get('build', {})
    steps = build_job.get('steps', [])
    
    latex_step = None
    for step in steps:
        if step.get('name') == 'Set up LaTeX':
            latex_step = step
            break
    
    if not latex_step:
        print("❌ ERROR: 'Set up LaTeX' step not found in workflow")
        return False
    
    uses_action = latex_step.get('uses', '')
    
    print(f"Found LaTeX action: {uses_action}")
    
    # Check that it's using @latest
    if uses_action == 'dante-ev/latex-action@latest':
        print("✅ PASS: Using latest version (@latest)")
        return True
    elif uses_action == 'dante-ev/latex-action@v2':
        print("❌ FAIL: Still using v2, should be updated to @latest")
        print("Expected: dante-ev/latex-action@latest")
        return False
    else:
        print(f"❌ ERROR: Unexpected action: {uses_action}")
        return False

def test_fontawesome5_support():
    """Test that fontawesome5 package dependencies are included"""
    
    workflow_path = '.github/workflows/latex-build.yml'
    
    with open(workflow_path, 'r') as f:
        content = f.read()
    
    # Check for fontawesome5-related packages
    required_packages = [
        'texlive-fonts-extra',  # Contains fontawesome5
        'texlive-latex-extra',  # Additional support
        'texlive-fontutils'     # Font utilities
    ]
    
    missing_packages = []
    for package in required_packages:
        if package not in content:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ FAIL: Missing packages for fontawesome5 support: {missing_packages}")
        return False
    else:
        print("✅ PASS: All required packages for fontawesome5 are included")
        return True

def test_latex_args():
    """Test that LaTeX compilation arguments are correct"""
    
    workflow_path = '.github/workflows/latex-build.yml'
    
    try:
        with open(workflow_path, 'r') as f:
            workflow_content = yaml.safe_load(f)
    except Exception as e:
        print(f"❌ ERROR: Failed to parse {workflow_path}: {e}")
        return False
    
    # Find the LaTeX action step
    jobs = workflow_content.get('jobs', {})
    build_job = jobs.get('build', {})
    steps = build_job.get('steps', [])
    
    latex_step = None
    for step in steps:
        if step.get('name') == 'Set up LaTeX':
            latex_step = step
            break
    
    if not latex_step:
        print("❌ ERROR: 'Set up LaTeX' step not found in workflow")
        return False
    
    step_with = latex_step.get('with', {})
    args = step_with.get('args', '')
    
    print(f"Found LaTeX args: {args}")
    
    # Check for required arguments
    required_args = [
        '-interaction=nonstopmode',  # No user interaction
        '-halt-on-error',           # Stop on first error
        '-shell-escape'             # Enable shell escape for packages
    ]
    
    missing_args = []
    for arg in required_args:
        if arg not in args:
            missing_args.append(arg)
    
    if missing_args:
        print(f"❌ FAIL: Missing required LaTeX arguments: {missing_args}")
        return False
    else:
        print("✅ PASS: All required LaTeX arguments are present")
        return True

def test_yaml_syntax():
    """Test that YAML syntax is correct (quoted on: keyword)"""
    
    workflow_files = [
        '.github/workflows/latex-build.yml',
        '.github/workflows/latex-validation.yml',
        '.github/workflows/static.yml',
        '.github/workflows/pr-validation.yml'
    ]
    
    all_correct = True
    
    for file_path in workflow_files:
        if not os.path.exists(file_path):
            print(f"⚠️  WARNING: {file_path} not found, skipping")
            continue
            
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Check for quoted "on": syntax
        if '"on":' in content:
            print(f"✅ PASS: {os.path.basename(file_path)} has correct quoted syntax")
        elif 'on:' in content and '"on":' not in content:
            print(f"❌ FAIL: {os.path.basename(file_path)} has unquoted 'on:' syntax")
            all_correct = False
        else:
            print(f"⚠️  WARNING: {os.path.basename(file_path)} doesn't contain 'on:' trigger")
    
    return all_correct

def main():
    """Run all tests for CI build fixes"""
    
    print("=" * 60)
    print("CI BUILD FIXES VALIDATION")
    print("=" * 60)
    print("Testing GitHub Actions LaTeX workflow improvements...")
    print()
    
    tests = [
        ("LaTeX action version update", test_latex_action_update),
        ("FontAwesome5 package support", test_fontawesome5_support),
        ("LaTeX compilation arguments", test_latex_args),
        ("YAML syntax validation", test_yaml_syntax)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"🔍 Testing: {test_name}")
        print("-" * 40)
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ ERROR in {test_name}: {e}")
            results.append((test_name, False))
        print()
    
    # Summary
    print("=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print()
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED - CI build fixes are working correctly!")
        print()
        print("The GitHub Actions workflow should now:")
        print("- Use the latest dante-ev/latex-action for better compatibility")
        print("- Support fontawesome5 package with proper dependencies")
        print("- Have correct LaTeX compilation arguments")
        print("- Maintain proper YAML syntax")
        return True
    else:
        print("❌ SOME TESTS FAILED - Please review and fix the issues above")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)