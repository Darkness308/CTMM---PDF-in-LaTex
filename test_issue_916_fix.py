#!/usr/bin/env python3
"""
Test script to validate Issue #916 fix
Verifies that the GitHub Actions workflow uses a valid dante-ev/latex-action version
and resolves CI build failures
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
    
    # Check that it's using the correct version
    if uses_action == 'dante-ev/latex-action@v2.0.0':
        print("❌ FAIL: Still using problematic version v2.0.0")
        print("This version doesn't exist and will cause CI failure:")
        print("'Unable to resolve action `dante-ev/latex-action@v2.0.0`, unable to find version `v2.0.0`'")
        return False
    elif uses_action == 'dante-ev/latex-action@v2':
        print("✅ PASS: Using correct version v2")
        return True
    elif uses_action.startswith('dante-ev/latex-action@'):
        print(f"⚠️  WARNING: Using version {uses_action}")
        print("Expected: dante-ev/latex-action@v2")
        return False
    else:
        print(f"❌ ERROR: Unexpected action: {uses_action}")
        return False

def test_workflow_syntax():
    """Test that the workflow file has valid syntax"""
    
    workflow_path = '.github/workflows/latex-build.yml'
    
    try:
        with open(workflow_path, 'r') as f:
            yaml.safe_load(f)
        print("✅ PASS: Workflow YAML syntax is valid")
        return True
    except yaml.YAMLError as e:
        print(f"❌ FAIL: Invalid YAML syntax: {e}")
        return False

def test_ci_robustness():
    """Test that CI robustness features are in place"""
    
    workflow_path = '.github/workflows/latex-build.yml'
    
    try:
        with open(workflow_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ ERROR: Failed to read {workflow_path}: {e}")
        return False
    
    checks = [
        ('LaTeX syntax validation step', 'validate_latex_syntax.py'),
        ('CTMM build system check', 'ctmm_build.py'),
        ('Comprehensive CI validation', 'test_issue_743_validation.py'),
        ('Build log upload on failure', 'upload-artifact@v4'),
        ('Proper quoted on syntax', '"on":'),
    ]
    
    all_passed = True
    for check_name, check_pattern in checks:
        if check_pattern in content:
            print(f"✅ FOUND: {check_name}")
        else:
            print(f"❌ MISSING: {check_name}")
            all_passed = False
    
    return all_passed

def main():
    """Run all tests for Issue #916 fix"""
    
    print("=" * 60)
    print("Issue #916 Fix Validation - CI Build Failure Resolution")
    print("=" * 60)
    print()
    
    tests = [
        ("dante-ev/latex-action version", test_dante_action_version),
        ("Workflow YAML syntax", test_workflow_syntax),
        ("CI robustness features", test_ci_robustness),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"Testing {test_name}...")
        result = test_func()
        results.append(result)
        print()
    
    # Summary
    print("=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    for i, (test_name, _) in enumerate(tests):
        status = "✅ PASS" if results[i] else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print()
    print(f"Tests passed: {passed}/{total}")
    
    if all(results):
        print("🎉 ALL TESTS PASSED - Issue #916 fix is working correctly!")
        print()
        print("The GitHub Actions workflow should now be able to:")
        print("- Resolve the dante-ev/latex-action@v2 action successfully")
        print("- Avoid the 'unable to find version v2.0.0' error")
        print("- Complete the LaTeX PDF build process without CI failures")
        print("- Benefit from enhanced robustness and error handling")
        return True
    else:
        print("❌ SOME TESTS FAILED - Issue #916 fix needs more work")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)