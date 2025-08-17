#!/usr/bin/env python3
"""
Test script to validate Issue #789 fix
Verifies CI build failures are addressed with proper GitHub Actions configuration
and LaTeX package additions including fontawesome5 support
"""

import yaml
import os
import sys

def test_latex_action_latest():
    """Test that the GitHub Actions workflow uses dante-ev/latex-action@latest"""
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
        print("✅ PASS: Using latest version for improved reliability")
        return True
    elif uses_action == 'dante-ev/latex-action@v2':
        print("⚠️  WARNING: Still using v2, but @latest was requested for CI reliability")
        print("The problem statement specifically mentions updating to @latest")
        return False
    else:
        print(f"❌ FAIL: Unexpected action version: {uses_action}")
        return False

def test_comprehensive_latex_packages():
    """Test that comprehensive LaTeX packages are installed including fontawesome5 support"""
    workflow_path = '.github/workflows/latex-build.yml'
    
    with open(workflow_path, 'r') as f:
        workflow_content = yaml.safe_load(f)
    
    # Find the LaTeX action step
    jobs = workflow_content.get('jobs', {})
    build_job = jobs.get('build', {})
    steps = build_job.get('steps', [])
    
    latex_step = None
    for step in steps:
        if step.get('name') == 'Set up LaTeX':
            latex_step = step
            break
    
    extra_packages = latex_step.get('with', {}).get('extra_system_packages', '')
    print(f"📋 Found LaTeX packages configuration:")
    for line in extra_packages.strip().split('\n'):
        if line.strip():
            print(f"   - {line.strip()}")
    
    # Essential package validation for fontawesome5 and German support
    required_packages = [
        'texlive-lang-german',       # German language support
        'texlive-fonts-extra',       # Should include fontawesome5 support
        'texlive-latex-extra',       # Extra LaTeX packages
        'texlive-pstricks'           # PostScript tricks (contains pifont)
    ]
    
    print("\n🔍 Validating essential packages for CI reliability...")
    all_passed = True
    
    for pkg in required_packages:
        if pkg in extra_packages:
            print(f"✅ FOUND: {pkg}")
        else:
            print(f"❌ MISSING: {pkg}")
            all_passed = False
    
    # Specific fontawesome5 validation
    print("\n🎯 Validating fontawesome5 package availability...")
    fontawesome_providers = ['texlive-fonts-extra', 'texlive-latex-extra']
    fontawesome_available = any(pkg in extra_packages for pkg in fontawesome_providers)
    
    if fontawesome_available:
        found_providers = [pkg for pkg in fontawesome_providers if pkg in extra_packages]
        print(f"✅ FONTAWESOME5 AVAILABLE: Found providers: {', '.join(found_providers)}")
    else:
        print("❌ FONTAWESOME5 MISSING: No packages found that provide fontawesome5")
        all_passed = False
    
    # Check for additional robustness packages
    robustness_packages = ['texlive-binaries']
    print("\n🔧 Checking additional robustness packages...")
    for pkg in robustness_packages:
        if pkg in extra_packages:
            print(f"✅ FOUND: {pkg} (improves CI robustness)")
        else:
            print(f"⚠️  OPTIONAL: {pkg} could improve CI robustness")
    
    return all_passed

def test_correct_latex_arguments():
    """Test that LaTeX compilation arguments are correct (no invalid -pdf flag)"""
    workflow_path = '.github/workflows/latex-build.yml'
    
    with open(workflow_path, 'r') as f:
        content = f.read()
    
    # Check that -pdf is NOT in the args line
    if "-pdf" in content and "args:" in content:
        lines = content.split('\n')
        for line in lines:
            if "args:" in line and "-pdf" in line:
                print(f"❌ FAILED: Found problematic -pdf argument in: {line.strip()}")
                return False
    
    print("✅ SUCCESS: No problematic -pdf argument found in workflow")
    
    # Check that the corrected arguments are present
    expected_args = ["-interaction=nonstopmode", "-halt-on-error", "-shell-escape"]
    args_line = None
    lines = content.split('\n')
    for line in lines:
        if "args:" in line:
            args_line = line.strip()
            break
    
    if not args_line:
        print("❌ FAILED: No args line found in workflow")
        return False
        
    print(f"📋 Found args line: {args_line}")
    
    for arg in expected_args:
        if arg not in args_line:
            print(f"❌ FAILED: Missing expected argument: {arg}")
            return False
    
    print("✅ SUCCESS: All expected LaTeX arguments found")
    return True

def test_yaml_syntax():
    """Test that YAML syntax is correct with quoted 'on' keyword"""
    workflow_files = [
        '.github/workflows/latex-build.yml',
        '.github/workflows/latex-validation.yml', 
        '.github/workflows/static.yml'
    ]
    
    all_passed = True
    print("🔍 Validating YAML syntax for quoted 'on' keyword...")
    
    for workflow_file in workflow_files:
        if not os.path.exists(workflow_file):
            continue
            
        try:
            with open(workflow_file, 'r') as f:
                content = f.read()
                workflow_content = yaml.safe_load(content)
            
            # Check that 'on' is properly parsed as string key
            if 'on' in workflow_content:
                print(f"✅ PASS: {workflow_file} has correct quoted 'on' syntax")
            else:
                print(f"❌ FAIL: {workflow_file} missing 'on' key or incorrect syntax")
                all_passed = False
                
        except Exception as e:
            print(f"❌ FAIL: {workflow_file} has YAML syntax error: {e}")
            all_passed = False
    
    return all_passed

def main():
    """Run all tests for Issue #789 fix"""
    print("=" * 70)
    print("Issue #789 Fix Validation")
    print("Critical CI Build Failures - GitHub Actions Configuration")
    print("=" * 70)
    
    tests = [
        ("dante-ev/latex-action@latest version", test_latex_action_latest),
        ("Comprehensive LaTeX packages", test_comprehensive_latex_packages),
        ("Correct LaTeX arguments", test_correct_latex_arguments),
        ("YAML syntax validation", test_yaml_syntax)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Testing {test_name}...")
        print("-" * 50)
        if test_func():
            print(f"✅ PASS: {test_name}")
            passed += 1
        else:
            print(f"❌ FAIL: {test_name}")
    
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    for i, (test_name, _) in enumerate(tests):
        status = "✅ PASS" if i < passed else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\nTests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED - Issue #789 fix is working correctly!")
        print("\nThe GitHub Actions workflow should now:")
        print("- Use the latest dante-ev/latex-action for improved reliability")
        print("- Have comprehensive LaTeX package support including fontawesome5")
        print("- Have correct YAML syntax with quoted 'on' keywords")
        print("- Use proper LaTeX compilation arguments")
        return True
    else:
        print("❌ SOME TESTS FAILED!")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)