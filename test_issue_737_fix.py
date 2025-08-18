#!/usr/bin/env python3
"""
Test script to validate Issue #737 fix
Verifies that the GitHub Actions workflow uses dante-ev/latex-action@v2.1.0 for stability
"""

import yaml
import os
import sys

def test_dante_action_version():
    """Test that the GitHub Actions workflow uses the correct dante-ev/latex-action version"""
    
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
    
    # Check that it's using the correct version for Issue #737
    if uses_action == 'dante-ev/latex-action@v2.1.0':
        print("✅ PASS: Using correct stable version v2.1.0")
        return True
    elif uses_action == 'dante-ev/latex-action@latest':
        print("❌ FAIL: Still using @latest instead of stable v2.1.0")
        print("Issue #737 requires update to v2.1.0 for better CI stability")
        return False
    elif uses_action == 'dante-ev/latex-action@v2.0.0':
        print("❌ FAIL: Using problematic version v2.0.0")
        print("This version doesn't exist and will cause CI failure")
        return False
    elif uses_action.startswith('dante-ev/latex-action@'):
        print(f"⚠️  WARNING: Using unexpected version {uses_action}")
        print("Expected: dante-ev/latex-action@v2.1.0")
        return False
    else:
        print(f"❌ ERROR: Unexpected action: {uses_action}")
        return False

def test_workflow_syntax():
    """Test that the workflow file has valid syntax"""
    
    workflow_path = '.github/workflows/latex-build.yml'
    
    try:
        with open(workflow_path, 'r') as f:
            workflow_content = yaml.safe_load(f)
        print("✅ PASS: Workflow YAML syntax is valid")
        return True
    except yaml.YAMLError as e:
        print(f"❌ FAIL: Workflow YAML syntax error: {e}")
        return False
    except Exception as e:
        print(f"❌ FAIL: Error reading workflow file: {e}")
        return False

def test_latex_action_configuration():
    """Test that the LaTeX action has proper configuration"""
    
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
        print("❌ ERROR: 'Set up LaTeX' step not found")
        return False
    
    # Check required configuration parameters
    step_with = latex_step.get('with', {})
    
    # Check root_file
    if step_with.get('root_file') == 'main.tex':
        print("✅ root_file correctly set to main.tex")
    else:
        print(f"❌ root_file incorrect: {step_with.get('root_file')}")
        return False
    
    # Check args
    args = step_with.get('args', '')
    required_args = ['-interaction=nonstopmode', '-halt-on-error', '-shell-escape']
    missing_args = [arg for arg in required_args if arg not in args]
    
    if not missing_args:
        print("✅ LaTeX compilation args correctly configured")
    else:
        print(f"❌ Missing required args: {missing_args}")
        return False
    
    # Check extra_system_packages
    packages = step_with.get('extra_system_packages', '')
    required_packages = ['texlive-lang-german', 'texlive-pstricks']
    
    missing_packages = [pkg for pkg in required_packages if pkg not in packages]
    if not missing_packages:
        print("✅ Essential LaTeX packages configured")
    else:
        print(f"❌ Missing essential packages: {missing_packages}")
        return False
    
    return True

def main():
    """Run all tests for Issue #737 fix"""
    
    print("============================================================")
    print("Issue #737 Fix Validation")
    print("============================================================")
    
    tests = [
        ("dante-ev/latex-action version", test_dante_action_version),
        ("Workflow YAML syntax", test_workflow_syntax),
        ("LaTeX action configuration", test_latex_action_configuration),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\nTesting {test_name}...")
        result = test_func()
        results.append((test_name, result))
    
    print("\n============================================================")
    print("TEST SUMMARY")
    print("============================================================")
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\nTests passed: {passed}/{len(tests)}")
    
    if passed == len(tests):
        print("🎉 ALL TESTS PASSED - Issue #737 fix is working correctly!")
        print("\nThe GitHub Actions workflow should now:")
        print("- Use stable dante-ev/latex-action@v2.1.0 version")
        print("- Avoid compatibility issues with @latest or @v2.0.0")
        print("- Successfully compile LaTeX files and generate PDFs")
        print("- Maintain consistent CI build behavior")
        return True
    else:
        print("❌ Some tests failed. Please address the issues above.")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)