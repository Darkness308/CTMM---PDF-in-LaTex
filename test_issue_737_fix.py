#!/usr/bin/env python3
"""
Test for Issue #737 Fix: GitHub Actions LaTeX Build Workflow Update

This test validates that the LaTeX action version has been updated to resolve CI failures.
"""

import yaml
import os
import sys


def test_latex_action_version():
    """Test that the LaTeX action uses a stable version (not v2.0.0)."""
    workflow_path = '.github/workflows/latex-build.yml'
    
    if not os.path.exists(workflow_path):
        print(f"❌ Workflow file not found: {workflow_path}")
        return False
    
    with open(workflow_path, 'r') as f:
        content = f.read()
    
    try:
        workflow = yaml.safe_load(content)
    except yaml.YAMLError as e:
        print(f"❌ Invalid YAML in {workflow_path}: {e}")
        return False
    
    # Find the LaTeX action step
    latex_action_found = False
    latex_action_version = None
    
    for job_name, job in workflow.get('jobs', {}).items():
        for step in job.get('steps', []):
            uses = step.get('uses', '')
            if 'dante-ev/latex-action' in uses:
                latex_action_found = True
                latex_action_version = uses
                break
        if latex_action_found:
            break
    
    if not latex_action_found:
        print("❌ dante-ev/latex-action not found in workflow")
        return False
    
    print(f"Found LaTeX action: {latex_action_version}")
    
    # Check that it's not the problematic v2.0.0 version
    if 'dante-ev/latex-action@v2.0.0' in latex_action_version:
        print("❌ Still using problematic v2.0.0 version")
        return False
    
    # Check that it uses a proper version tag
    if '@v' not in latex_action_version:
        print("❌ LaTeX action does not use proper version tag")
        return False
    
    # Preferred version should be v2.1.0 or higher
    if 'dante-ev/latex-action@v2.1.0' in latex_action_version:
        print("✅ Using recommended v2.1.0 version")
        return True
    elif '@v2.' in latex_action_version and not '@v2.0' in latex_action_version:
        print("✅ Using stable v2.x version (not v2.0.x)")
        return True
    else:
        print("⚠️  Using version other than recommended v2.1.0")
        return True  # Still valid as long as not v2.0.0


def test_workflow_syntax():
    """Test that the workflow file has valid syntax."""
    workflow_path = '.github/workflows/latex-build.yml'
    
    try:
        with open(workflow_path, 'r') as f:
            workflow = yaml.safe_load(f)
        
        # Basic structure checks
        required_keys = ['name', 'on', 'jobs']
        for key in required_keys:
            if key not in workflow:
                print(f"❌ Missing required key: {key}")
                return False
        
        # Check that 'on' is properly quoted (not boolean)
        with open(workflow_path, 'r') as f:
            content = f.read()
        
        if '"on":' not in content:
            print("❌ 'on' key is not properly quoted")
            return False
        
        print("✅ Workflow syntax is valid")
        return True
        
    except Exception as e:
        print(f"❌ Workflow syntax error: {e}")
        return False


def test_latex_compilation_arguments():
    """Test that LaTeX arguments are correct (no invalid -pdf argument)."""
    workflow_path = '.github/workflows/latex-build.yml'
    
    with open(workflow_path, 'r') as f:
        content = f.read()
    
    # Check that the problematic -pdf argument is not present
    if '-pdf ' in content or 'args: -pdf' in content:
        print("❌ Invalid -pdf argument found in LaTeX compilation")
        return False
    
    # Check that required arguments are present
    required_args = ['-interaction=nonstopmode', '-halt-on-error', '-shell-escape']
    for arg in required_args:
        if arg not in content:
            print(f"❌ Required LaTeX argument missing: {arg}")
            return False
    
    print("✅ LaTeX compilation arguments are correct")
    return True


def main():
    """Run all tests for Issue #737 fix."""
    print("=" * 70)
    print("Issue #737 Fix Validation - GitHub Actions LaTeX Build Workflow")
    print("=" * 70)
    print()
    
    tests = [
        test_latex_action_version,
        test_workflow_syntax,
        test_latex_compilation_arguments
    ]
    
    results = []
    for test in tests:
        print(f"Running {test.__name__}...")
        result = test()
        results.append(result)
        print()
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    print("=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED - Issue #737 fix is valid!")
        print()
        print("The GitHub Actions workflow should now build successfully with:")
        print("- Updated dante-ev/latex-action version (not v2.0.0)")
        print("- Valid YAML syntax")
        print("- Correct LaTeX compilation arguments")
        return True
    else:
        print("❌ Some tests failed - additional fixes needed")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)