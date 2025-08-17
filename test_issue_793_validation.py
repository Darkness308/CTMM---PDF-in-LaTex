#!/usr/bin/env python3
"""
Test script to validate Issue #793 fix - CI LaTeX Build Failure Resolution
Validates all components mentioned in the PR overview for critical CI fixes.
"""

import os
import sys
import yaml
import subprocess
import tempfile
from pathlib import Path

def validate_github_actions_syntax():
    """Validate GitHub Actions workflow syntax fixes."""
    print("\n🔧 GITHUB ACTIONS SYNTAX VALIDATION")
    print("-" * 50)
    
    all_passed = True
    
    # Check workflow files
    workflow_files = [
        '.github/workflows/latex-build.yml',
        '.github/workflows/latex-validation.yml', 
        '.github/workflows/static.yml'
    ]
    
    print("📂 Checking workflow files...")
    for workflow_file in workflow_files:
        if not os.path.exists(workflow_file):
            print(f"❌ FAIL: Workflow file missing: {workflow_file}")
            all_passed = False
        else:
            print(f"✅ FOUND: {workflow_file}")
    
    # Validate YAML syntax
    print("\n📝 Validating YAML syntax...")
    for workflow_file in workflow_files:
        if os.path.exists(workflow_file):
            try:
                with open(workflow_file, 'r') as f:
                    yaml.safe_load(f)
                print(f"✅ VALID: {workflow_file} has correct YAML syntax")
            except yaml.YAMLError as e:
                print(f"❌ INVALID: {workflow_file} has YAML syntax error: {e}")
                all_passed = False
    
    # Check for quoted "on:" syntax (Issue #458/#532 compliance)
    print("\n🔤 Checking 'on:' keyword syntax...")
    for workflow_file in workflow_files:
        if os.path.exists(workflow_file):
            with open(workflow_file, 'r') as f:
                content = f.read()
            
            if '"on":' in content:
                print(f"✅ CORRECT: {workflow_file} uses quoted 'on:' syntax")
            elif 'on:' in content and '"on":' not in content:
                print(f"❌ INCORRECT: {workflow_file} uses unquoted 'on:' syntax")
                all_passed = False
    
    return all_passed

def validate_latex_action_version():
    """Validate dante-ev/latex-action version fix (Issue #735)."""
    print("\n📦 LATEX ACTION VERSION VALIDATION")
    print("-" * 50)
    
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
    
    # Check that it's using the correct version
    if uses_action == 'dante-ev/latex-action@v2.0.0':
        print("❌ FAIL: Still using problematic version v2.0.0")
        print("This version doesn't exist and will cause CI failure")
        return False
    elif uses_action == 'dante-ev/latex-action@v2':
        print("✅ PASS: Using correct version v2")
        return True
    else:
        print(f"⚠️  WARNING: Using unexpected version {uses_action}")
        return True

def validate_latex_packages():
    """Validate LaTeX package dependencies (Issue #739)."""
    print("\n📋 LATEX PACKAGE DEPENDENCIES VALIDATION")
    print("-" * 50)
    
    workflow_path = '.github/workflows/latex-build.yml'
    
    if not os.path.exists(workflow_path):
        print(f"❌ ERROR: Workflow file {workflow_path} not found")
        return False
    
    try:
        with open(workflow_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ ERROR: Failed to read {workflow_path}: {e}")
        return False
    
    # Check for essential packages
    required_packages = [
        'texlive-lang-german',     # German language support
        'texlive-fonts-recommended',
        'texlive-latex-recommended',
        'texlive-fonts-extra',
        'texlive-latex-extra',
        'texlive-science',
        'texlive-pstricks'         # Contains pifont for checkboxes
    ]
    
    all_found = True
    print("🔍 Checking for required packages...")
    for package in required_packages:
        if package in content:
            print(f"✅ FOUND: {package}")
        else:
            print(f"❌ MISSING: {package}")
            all_found = False
    
    # Specific check for pifont availability
    if 'texlive-pstricks' in content:
        print("✅ PIFONT AVAILABLE: texlive-pstricks includes pifont package")
    else:
        print("❌ PIFONT MISSING: No package provides pifont for checkboxes")
        all_found = False
    
    return all_found

def validate_build_system_enhancements():
    """Validate build system pdflatex availability checks."""
    print("\n🏗️  BUILD SYSTEM ENHANCEMENTS VALIDATION")
    print("-" * 50)
    
    build_script = 'ctmm_build.py'
    
    if not os.path.exists(build_script):
        print(f"❌ ERROR: Build script {build_script} not found")
        return False
    
    try:
        with open(build_script, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ ERROR: Failed to read {build_script}: {e}")
        return False
    
    # Check for pdflatex availability checks
    pdflatex_checks = [
        'pdflatex not found',
        'WARNING:',
        'LaTeX not available'
    ]
    
    found_checks = []
    for check in pdflatex_checks:
        if check in content:
            found_checks.append(check)
    
    if found_checks:
        print("✅ FOUND: pdflatex availability checks in build system")
        for check in found_checks:
            print(f"   - Contains: '{check}'")
    else:
        print("❌ MISSING: No pdflatex availability checks found")
        return False
    
    # Test the build system
    print("\n🧪 Testing build system...")
    try:
        result = subprocess.run([sys.executable, build_script], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("✅ BUILD SYSTEM: Executed successfully")
            if 'CTMM BUILD SYSTEM SUMMARY' in result.stdout:
                print("✅ BUILD SYSTEM: Proper summary output")
            return True
        else:
            print(f"❌ BUILD SYSTEM: Failed with exit code {result.returncode}")
            return False
    except Exception as e:
        print(f"❌ BUILD SYSTEM: Exception during execution: {e}")
        return False

def validate_form_elements_integration():
    """Validate form elements with pifont integration."""
    print("\n📝 FORM ELEMENTS INTEGRATION VALIDATION")
    print("-" * 50)
    
    form_elements_file = 'style/form-elements.sty'
    
    if not os.path.exists(form_elements_file):
        print(f"❌ ERROR: Form elements file {form_elements_file} not found")
        return False
    
    try:
        with open(form_elements_file, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ ERROR: Failed to read {form_elements_file}: {e}")
        return False
    
    # Check for pifont requirement
    if '\\RequirePackage{pifont}' in content:
        print("✅ CORRECT: form-elements.sty requires pifont package")
    else:
        print("❌ MISSING: form-elements.sty doesn't require pifont package")
        return False
    
    # Check for ding usage (checkboxes)
    if '\\ding{51}' in content:
        print("✅ CORRECT: form-elements.sty uses pifont symbols (\\ding commands)")
    else:
        print("❌ MISSING: form-elements.sty doesn't use pifont symbols")
        return False
    
    # Check for CTMM form elements
    ctmm_elements = [
        'ctmmCheckBox',
        'ctmmTextField', 
        'ctmmTextArea',
        'ctmmRadioButton'
    ]
    
    found_elements = 0
    for element in ctmm_elements:
        if element in content:
            found_elements += 1
    
    print(f"📋 CTMM form elements found: {found_elements}/{len(ctmm_elements)}")
    for element in ctmm_elements:
        if element in content:
            print(f"   ✅ {element}")
        else:
            print(f"   ❌ {element}")
    
    return found_elements == len(ctmm_elements)

def main():
    """Run all validation tests for Issue #793."""
    print("=" * 70)
    print("ISSUE #793 COMPREHENSIVE VALIDATION SUITE")
    print("CI LaTeX Build Failure Resolution")
    print("=" * 70)
    
    # Track results
    test_results = {}
    
    # Run validation tests
    test_results['GitHub Actions Syntax'] = validate_github_actions_syntax()
    test_results['LaTeX Action Version'] = validate_latex_action_version()
    test_results['LaTeX Package Dependencies'] = validate_latex_packages()
    test_results['Build System Enhancements'] = validate_build_system_enhancements()
    test_results['Form Elements Integration'] = validate_form_elements_integration()
    
    # Summary
    print("\n" + "=" * 70)
    print("VALIDATION SUMMARY REPORT")
    print("=" * 70)
    
    passed_tests = 0
    total_tests = len(test_results)
    
    for test_name, result in test_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed_tests += 1
    
    print(f"\nOverall Result: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("\n🎉 ALL VALIDATION TESTS PASSED!")
        print("\nThe CI configuration fixes are working correctly:")
        print("  ✓ GitHub Actions workflow syntax fixed")
        print("  ✓ LaTeX action version corrected (v2 not v2.0.0)")
        print("  ✓ German language packages and pifont support added")
        print("  ✓ Build system enhanced with pdflatex availability checks")
        print("  ✓ Form elements properly integrated with pifont")
        print("\n" + "=" * 70)
        print("ISSUE #793 VALIDATION: SUCCESS ✅")
        print("All critical CI LaTeX build fixes are confirmed working.")
        print("=" * 70)
        return True
    else:
        print(f"\n❌ {total_tests - passed_tests} validation test(s) failed!")
        print("Some CI configuration issues may still exist.")
        print("\n" + "=" * 70)
        print("ISSUE #793 VALIDATION: FAILURE ❌")
        print("Additional fixes may be needed.")
        print("=" * 70)
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)