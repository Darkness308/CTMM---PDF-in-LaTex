#!/usr/bin/env python3
"""
Test script to validate Issue #845 fix
Verifies CI workflow changes for LaTeX build improvements
"""

import yaml
import os
import sys

def test_dante_action_latest():
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
        print("✅ PASS: Using latest version (@latest)")
        return True
    elif uses_action == 'dante-ev/latex-action@v2':
        print("❌ FAIL: Still using pinned version v2")
        print("Expected: dante-ev/latex-action@latest")
        return False
    else:
        print(f"❌ ERROR: Unexpected action: {uses_action}")
        return False

def test_fontawesome5_package():
    """Test that fontawesome5 package is included in LaTeX dependencies"""
    
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
    
    extra_packages = latex_step.get('with', {}).get('extra_system_packages', '')
    
    print(f"📋 Found LaTeX packages configuration:")
    for line in extra_packages.strip().split('\n'):
        if line.strip():
            print(f"   - {line.strip()}")
    
    # Check for fontawesome5
    if 'texlive-fontawesome5' in extra_packages:
        print("✅ PASS: fontawesome5 package included (texlive-fontawesome5)")
        return True
    elif 'fontawesome5' in extra_packages:
        print("✅ PASS: fontawesome5 package included")
        return True
    else:
        print("❌ FAIL: fontawesome5 package not found in LaTeX dependencies")
        print("Expected to find 'texlive-fontawesome5' or 'fontawesome5' in package list")
        return False

def test_yaml_syntax():
    """Test that the workflow file has valid YAML syntax"""
    
    workflow_path = '.github/workflows/latex-build.yml'
    
    if not os.path.exists(workflow_path):
        print(f"❌ ERROR: Workflow file {workflow_path} not found")
        return False
    
    try:
        with open(workflow_path, 'r') as f:
            workflow_content = yaml.safe_load(f)
        print("✅ PASS: Workflow YAML syntax is valid")
        return True
    except yaml.YAMLError as e:
        print(f"❌ FAIL: YAML syntax error: {e}")
        return False
    except Exception as e:
        print(f"❌ ERROR: Failed to read workflow file: {e}")
        return False

def test_comprehensive_packages():
    """Test that comprehensive LaTeX packages are included including German support"""
    
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
    
    extra_packages = latex_step.get('with', {}).get('extra_system_packages', '')
    
    # Check for essential packages
    required_packages = [
        'texlive-lang-german',       # German language support
        'texlive-fonts-recommended', # Recommended fonts
        'texlive-latex-recommended', # Recommended LaTeX packages
        'texlive-latex-extra',       # Extra LaTeX packages
        'texlive-fonts-extra',       # Extra fonts
        'texlive-science',           # Scientific packages
        'texlive-pstricks',          # PostScript tricks (contains pifont)
        'texlive-fontawesome5'       # FontAwesome5 support
    ]
    
    all_passed = True
    print("\n🔍 Validating essential packages...")
    
    for pkg in required_packages:
        if pkg in extra_packages:
            print(f"✅ FOUND: {pkg}")
        else:
            print(f"❌ MISSING: {pkg}")
            all_passed = False
    
    return all_passed

def main():
    """Run all tests for Issue #845 fix"""
    print("=" * 60)
    print("Issue #845 Fix Validation")
    print("CI Workflow LaTeX Build Improvements")
    print("=" * 60)
    
    tests = [
        ("dante-ev/latex-action@latest version", test_dante_action_latest),
        ("FontAwesome5 package inclusion", test_fontawesome5_package),
        ("Workflow YAML syntax", test_yaml_syntax),
        ("Comprehensive LaTeX packages", test_comprehensive_packages)
    ]
    
    test_results = []
    
    for test_name, test_func in tests:
        print(f"\nTesting {test_name}...")
        result = test_func()
        test_results.append(result)
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    for (test_name, _), result in zip(tests, test_results):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    passed_tests = sum(test_results)
    total_tests = len(test_results)
    print(f"\nTests passed: {passed_tests}/{total_tests}")
    
    if passed_tests == total_tests:
        print("🎉 ALL TESTS PASSED - Issue #845 fix is working correctly!")
        print("\nThe CI workflow now includes:")
        print("✓ Latest dante-ev/latex-action version")
        print("✓ FontAwesome5 package support")
        print("✓ Comprehensive German LaTeX packages")
        print("✓ Proper YAML syntax")
        return True
    else:
        print("⚠️  Some tests failed. Please review the CI configuration.")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)