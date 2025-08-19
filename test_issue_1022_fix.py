#!/usr/bin/env python3
"""
Test script to validate the fix for Issue #1022: GitHub Actions LaTeX Build Failure

This script verifies that the LaTeX action version has been updated from the problematic
'@v2' version to '@latest', preventing CI build failures.

Based on Issue #867 resolution pattern.
"""

import yaml
import os
import sys

def test_latex_action_version():
    """Test that the workflow uses a valid LaTeX action version."""
    print("🔍 Testing LaTeX action version...")
    
    workflow_files = [
        '.github/workflows/latex-build.yml',
        '.github/workflows/automated-pr-merge-test.yml'
    ]
    
    all_passed = True
    
    for workflow_path in workflow_files:
        if not os.path.exists(workflow_path):
            print(f"❌ FAIL: Workflow file {workflow_path} not found")
            all_passed = False
            continue
        
        with open(workflow_path, 'r') as f:
            content = f.read()
        
        # Check that problematic versions are not present
        problematic_versions = ['dante-ev/latex-action@v2.0.0', 'dante-ev/latex-action@v2']
        for version in problematic_versions:
            if version in content:
                print(f"❌ FAIL: {workflow_path} still using problematic '{version}' version")
                all_passed = False
        
        # Check that the latest version is used
        if 'dante-ev/latex-action@latest' not in content:
            print(f"❌ FAIL: {workflow_path} not using '@latest' version")
            all_passed = False
        else:
            print(f"✅ PASS: {workflow_path} using correct '@latest' version")
    
    return all_passed

def test_workflow_yaml_syntax():
    """Test that the workflow YAML syntax is valid."""
    print("🔍 Testing workflow YAML syntax...")
    
    workflow_path = '.github/workflows/latex-build.yml'
    
    try:
        with open(workflow_path, 'r') as f:
            yaml.safe_load(f)
        print("✅ PASS: YAML syntax is valid")
        return True
    except yaml.YAMLError as e:
        print(f"❌ FAIL: YAML syntax error: {e}")
        return False

def test_action_configuration():
    """Test that the action configuration is complete."""
    print("🔍 Testing action configuration...")
    
    workflow_path = '.github/workflows/latex-build.yml'
    
    with open(workflow_path, 'r') as f:
        content = yaml.safe_load(f)
    
    # Find the LaTeX action step
    latex_step = None
    for job in content.get('jobs', {}).values():
        for step in job.get('steps', []):
            if step.get('uses', '').startswith('dante-ev/latex-action'):
                latex_step = step
                break
    
    if not latex_step:
        print("❌ FAIL: LaTeX action step not found")
        return False
    
    # Check required configuration
    with_config = latex_step.get('with', {})
    
    if 'root_file' not in with_config:
        print("❌ FAIL: Missing 'root_file' configuration")
        return False
    
    if 'args' not in with_config:
        print("❌ FAIL: Missing 'args' configuration")
        return False
    
    print("✅ PASS: Action configuration is complete")
    return True

def main():
    """Run all validation tests."""
    print("🚀 Starting Issue #1022 fix validation...")
    print("=" * 50)
    
    tests = [
        test_latex_action_version,
        test_workflow_yaml_syntax,
        test_action_configuration
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    if passed == total:
        print("🎉 ALL TESTS PASSED! LaTeX action version issue resolved.")
        print(f"\nTests passed: {passed}/{total}")
        print("✅ LaTeX Action Version: PASS")
        print("✅ Workflow YAML Syntax: PASS")
        print("✅ Action Configuration: PASS")
        return 0
    else:
        print(f"❌ SOME TESTS FAILED! {passed}/{total} tests passed")
        return 1

if __name__ == '__main__':
    sys.exit(main())