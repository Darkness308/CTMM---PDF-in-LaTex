#!/usr/bin/env python3
"""
Test for Issue #749: CI Build Failure with dante-ev/latex-action@v2

This test validates that the LaTeX build workflow has been updated to use
a more stable and compatible LaTeX action version to resolve CI build failures.
"""

import os
import yaml
import subprocess
from pathlib import Path

def test_workflow_uses_updated_action():
    """Test that the workflow uses the updated xu-cheng/latex-action@v3 instead of dante-ev/latex-action@v2."""
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
    
    action_used = latex_step.get('uses', '')
    
    # Check that we're not using the problematic dante-ev/latex-action@v2
    if 'dante-ev/latex-action@v2' in action_used:
        print(f"❌ FAIL: Still using problematic dante-ev/latex-action@v2")
        return False
    
    # Check that we're using the updated xu-cheng/latex-action@v3
    if 'xu-cheng/latex-action@v3' in action_used:
        print(f"✅ SUCCESS: Using updated xu-cheng/latex-action@v3")
        return True
    
    print(f"❌ FAIL: Unexpected action used: {action_used}")
    return False

def test_package_configuration():
    """Test that the package configuration is correct for the new action."""
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
    
    # Check for correct package configuration
    if 'packages' in step_with:
        packages = step_with['packages']
        print(f"✅ SUCCESS: Found 'packages' configuration")
        
        # Check for essential packages
        required_packages = [
            'texlive-lang-german',
            'texlive-fonts-recommended',
            'texlive-latex-recommended',
            'texlive-latex-extra',
            'texlive-fonts-extra',
            'texlive-science',
            'texlive-pstricks'
        ]
        
        for pkg in required_packages:
            if pkg in packages:
                print(f"✅ Package found: {pkg}")
            else:
                print(f"❌ Missing package: {pkg}")
                return False
        
        return True
    
    elif 'extra_system_packages' in step_with:
        print("❌ FAIL: Still using old 'extra_system_packages' parameter")
        return False
    
    else:
        print("❌ FAIL: No package configuration found")
        return False

def test_workflow_yaml_syntax():
    """Test that the workflow file has valid YAML syntax."""
    workflow_path = '.github/workflows/latex-build.yml'
    
    try:
        with open(workflow_path, 'r') as f:
            yaml.safe_load(f)
        print("✅ SUCCESS: Workflow YAML syntax is valid")
        return True
    except yaml.YAMLError as e:
        print(f"❌ FAIL: Invalid YAML syntax: {e}")
        return False
    except Exception as e:
        print(f"❌ ERROR: Failed to read workflow file: {e}")
        return False

def test_basic_build_still_works():
    """Test that the basic build system still works after the change."""
    try:
        result = subprocess.run(
            ['python3', 'ctmm_build.py'],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            if "✓ PASS" in result.stdout and "CTMM BUILD SYSTEM SUMMARY" in result.stdout:
                print("✅ SUCCESS: CTMM build system still works correctly")
                return True
            else:
                print("❌ FAIL: CTMM build system passed but output looks incomplete")
                return False
        else:
            print(f"❌ FAIL: CTMM build system failed: {result.stderr}")
            return False
    
    except subprocess.TimeoutExpired:
        print("❌ FAIL: CTMM build system timed out")
        return False
    except Exception as e:
        print(f"❌ ERROR: Failed to run CTMM build system: {e}")
        return False

def main():
    """Main test function for Issue #749."""
    print("=" * 70)
    print("ISSUE #749 VALIDATION: CI Build Failure Fix")
    print("Testing LaTeX Action Update for GitHub Actions Compatibility")
    print("=" * 70)
    
    tests = [
        ("Updated LaTeX Action Version", test_workflow_uses_updated_action),
        ("Package Configuration", test_package_configuration),
        ("Workflow YAML Syntax", test_workflow_yaml_syntax),
        ("Build System Compatibility", test_basic_build_still_works),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🔍 Testing {test_name}...")
        print("-" * 50)
        try:
            result = test_func()
            results.append(result)
            if result:
                print(f"✅ {test_name}: PASSED")
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
            results.append(False)
    
    print("\n" + "=" * 70)
    print("ISSUE #749 VALIDATION SUMMARY")
    print("=" * 70)
    
    passed = sum(results)
    total = len(results)
    
    for i, (test_name, _) in enumerate(tests):
        status = "✅ PASS" if results[i] else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\nOverall Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("Issue #749 has been resolved:")
        print("- LaTeX action updated to xu-cheng/latex-action@v3")
        print("- Package configuration updated for new action")
        print("- Workflow maintains compatibility with existing build system")
        print("- CI build failure should be resolved")
        return 0
    else:
        print(f"\n❌ SOME TESTS FAILED - Issue #749 not fully resolved")
        return 1

if __name__ == "__main__":
    exit(main())