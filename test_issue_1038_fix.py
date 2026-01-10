#!/usr/bin/env python3
"""
Issue #1038 Validation: CI Build YAML Syntax Fix
=================================================

This script validates the fixes implemented for issue #1038, which addresses
the CI Insights report showing a broken "Build LaTeX PDF" workflow due to
YAML syntax violations (trailing whitespace and line length issues).

Key improvements tested:
1. YAML syntax validation (no trailing whitespace)
2. Line length compliance
3. Proper YAML structure
4. Workflow functionality validation
"""

import os
import sys
import yaml
import subprocess
from pathlib import Path

def test_yaml_syntax_cleanliness():
    """Test that workflow YAML files have no syntax issues."""
    print("\n🔧 Testing YAML Syntax Cleanliness")
    print("=" * 60)

    workflow_path = Path(".github/workflows/latex-build.yml")

    if not workflow_path.exists():
        print(f"❌ Workflow file not found: {workflow_path}")
        return False

    # Test 1: YAML parsing validation
    try:
        with open(workflow_path, 'r') as f:
            yaml.safe_load(f)
        print("✅ YAML syntax validation passed")
    except yaml.YAMLError as e:
        print(f"❌ YAML syntax error: {e}")
        return False

    # Test 2: No trailing whitespace
    with open(workflow_path, 'r') as f:
        lines = f.readlines()

    trailing_whitespace_lines = []
    for i, line in enumerate(lines, 1):
        if line.rstrip('\n') != line.rstrip():
            trailing_whitespace_lines.append(i)

    if trailing_whitespace_lines:
        print(f"❌ Found trailing whitespace on lines: {trailing_whitespace_lines}")
        return False
    else:
        print("✅ No trailing whitespace found")

    # Test 3: Line length compliance (max 80 chars)
    long_lines = []
    for i, line in enumerate(lines, 1):
        if len(line.rstrip('\n')) > 80:
            long_lines.append((i, len(line.rstrip('\n'))))

    if long_lines:
        print(f"❌ Lines exceeding 80 characters:")
        for line_num, length in long_lines:
            print(f"   Line {line_num}: {length} characters")
        return False
    else:
        print("✅ All lines within 80 character limit")

    # Test 4: Critical workflow structure
    with open(workflow_path, 'r') as f:
        content = yaml.safe_load(f)

    jobs = content.get('jobs', {})
    build_job = jobs.get('build', {})
    steps = build_job.get('steps', [])

    if len(steps) < 5:
        print(f"❌ Expected at least 5 workflow steps, found {len(steps)}")
        return False
    else:
        print(f"✅ Found {len(steps)} workflow steps")

    return True

def test_workflow_validation_steps():
    """Test that all validation steps are present and functional."""
    print("\n📋 Testing Workflow Validation Steps")
    print("=" * 60)

    # Test that the validation scripts referenced in the workflow exist
    validation_scripts = [
        'validate_latex_syntax.py',
        'ctmm_build.py',
        'test_issue_743_validation.py',
        'test_issue_761_fix.py'
    ]

    all_scripts_exist = True
    for script in validation_scripts:
        if Path(script).exists():
            print(f"✅ Found validation script: {script}")
        else:
            print(f"❌ Missing validation script: {script}")
            all_scripts_exist = False

    return all_scripts_exist

def test_enhanced_robustness_validation():
    """Test that the enhanced robustness validation works correctly."""
    print("\n🛡️ Testing Enhanced Robustness Validation")
    print("=" * 60)

    try:
        result = subprocess.run([sys.executable, 'test_issue_761_fix.py'],
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("✅ Enhanced robustness validation passed")
            return True
        else:
            print(f"❌ Enhanced robustness validation failed: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("❌ Enhanced robustness validation timed out")
        return False
    except Exception as e:
        print(f"❌ Error running enhanced robustness validation: {e}")
        return False

def test_yaml_workflow_structure():
    """Test that the YAML workflow structure is correct."""
    print("\n🏗️ Testing YAML Workflow Structure")
    print("=" * 60)

    workflow_path = Path(".github/workflows/latex-build.yml")

    with open(workflow_path, 'r') as f:
        content = yaml.safe_load(f)

    # Check essential workflow components
    essential_keys = ['name', 'on', 'jobs']
    for key in essential_keys:
        if key in content:
            print(f"✅ Found essential key: {key}")
        else:
            print(f"❌ Missing essential key: {key}")
            return False

    # Check job structure
    jobs = content.get('jobs', {})
    if 'build' in jobs:
        print("✅ Found 'build' job")

        build_job = jobs['build']
        if 'runs-on' in build_job and 'steps' in build_job:
            print("✅ Build job has proper structure")
        else:
            print("❌ Build job missing runs-on or steps")
            return False
    else:
        print("❌ Missing 'build' job")
        return False

    # Check for LaTeX action step
    steps = jobs['build']['steps']
    latex_step_found = False
    for step in steps:
        if step.get('name') == 'Set up LaTeX':
            latex_step_found = True
            if step.get('uses') == 'dante-ev/latex-action@v2':
                print("✅ Found proper LaTeX action step")
            else:
                print("❌ LaTeX action step has incorrect version")
                return False
            break

    if not latex_step_found:
        print("❌ LaTeX action step not found")
        return False

    return True

def main():
    """Run all validation tests for Issue #1038 fix."""
    print("======================================================================")
    print("ISSUE #1038 VALIDATION: CI Build YAML Syntax Fix")
    print("======================================================================")

    tests = [
        ("YAML Syntax Cleanliness", test_yaml_syntax_cleanliness),
        ("Workflow Validation Steps", test_workflow_validation_steps),
        ("Enhanced Robustness Validation", test_enhanced_robustness_validation),
        ("YAML Workflow Structure", test_yaml_workflow_structure)
    ]

    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results[test_name] = False

    print("\n======================================================================")
    print("VALIDATION SUMMARY")
    print("======================================================================")

    passed_count = sum(results.values())
    total_count = len(results)

    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} {test_name}")

    print(f"\nTests passed: {passed_count}/{total_count}")

    if passed_count == total_count:
        print("🎉 ALL TESTS PASSED! Issue #1038 CI YAML syntax fix validated.")
        print("\nThe workflow should now:")
        print("✓ Parse correctly without YAML syntax errors")
        print("✓ Execute all validation steps properly")
        print("✓ Build LaTeX PDF successfully in CI environment")
        print("✓ Provide proper error reporting on failures")
        return True
    else:
        print("❌ Some tests failed. The CI issue may not be fully resolved.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)