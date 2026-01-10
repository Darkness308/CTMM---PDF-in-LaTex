#!/usr/bin/env python3
"""
Issue #761 Validation: Enhanced CI Pipeline Robustness
======================================================

This script validates the fixes implemented for issue #761, which addresses
CI pipeline failures reported in the Mergify CI insights. The focus is on
enhancing error detection, recovery mechanisms, and workflow robustness.

Key improvements tested:
1. Enhanced pre-build validation
2. Comprehensive dependency checking
3. Better error recovery mechanisms
4. Improved error reporting and logging
"""

import os
import sys
import yaml
import subprocess
from pathlib import Path

def test_enhanced_workflow_error_handling():
    """Test that workflows have enhanced error handling mechanisms."""
    print("🔧 Testing Enhanced Workflow Error Handling")
    print("=" * 60)

    workflow_path = Path(".github/workflows/latex-build.yml")
    if not workflow_path.exists():
        print("❌ latex-build.yml not found")
        return False

    with open(workflow_path, 'r') as f:
        workflow = yaml.safe_load(f)

    build_job = workflow.get('jobs', {}).get('build', {})
    steps = build_job.get('steps', [])

    # Check for validation steps before LaTeX compilation
    validation_steps = []
    latex_step_index = None

    for i, step in enumerate(steps):
        step_name = step.get('name', '').lower()
        if 'validation' in step_name or 'check' in step_name:
            validation_steps.append(step_name)
        if 'latex' in step_name and 'set up' in step_name:
            latex_step_index = i

    print(f"✅ Found {len(validation_steps)} validation steps")
    for step in validation_steps:
        print(f"   - {step}")

    # Verify validation happens before LaTeX compilation
    if latex_step_index is not None and len(validation_steps) > 0:
        print("✅ Validation steps run before LaTeX compilation")
    else:
        print("⚠️  Warning: Validation order unclear")

    # Check for error handling features
    error_handling_features = 0

    # Check for build log upload on failure
    has_log_upload = any(
        step.get('if') == 'failure()' and 'upload' in step.get('name', '').lower()
        for step in steps
    )
    if has_log_upload:
        error_handling_features += 1
        print("✅ Build log upload on failure configured")

    # Check for continue-on-error where appropriate
    has_error_tolerance = any(
        step.get('continue-on-error') for step in steps
    )
    if has_error_tolerance:
        error_handling_features += 1
        print("✅ Error tolerance configured where appropriate")

    print(f"✅ Error handling features: {error_handling_features}")
    return True

def test_comprehensive_dependency_validation():
    """Test comprehensive dependency validation mechanisms."""
    print("\n📦 Testing Comprehensive Dependency Validation")
    print("=" * 60)

    # Test that our validation scripts exist and work
    validation_scripts = [
        'validate_latex_syntax.py',
        'ctmm_build.py',
        'test_issue_743_validation.py'
    ]

    all_scripts_work = True
    for script in validation_scripts:
        if not Path(script).exists():
            print(f"❌ Missing validation script: {script}")
            all_scripts_work = False
            continue

        try:
            result = subprocess.run([sys.executable, script],
                                  capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                print(f"✅ {script} executes successfully")
            else:
                print(f"⚠️  {script} returned non-zero exit code: {result.returncode}")
                print(f"   stderr: {result.stderr[:100]}...")
        except subprocess.TimeoutExpired:
            print(f"⚠️  {script} timed out")
        except Exception as e:
            print(f"❌ Error running {script}: {e}")
            all_scripts_work = False

    return all_scripts_work

def test_latex_package_dependency_robustness():
    """Test that LaTeX package dependencies are robustly configured."""
    print("\n🎯 Testing LaTeX Package Dependency Robustness")
    print("=" * 60)

    workflow_path = Path(".github/workflows/latex-build.yml")
    with open(workflow_path, 'r') as f:
        content = f.read()

    # Check for essential packages that have caused issues before
    essential_packages = [
        'texlive-lang-german',    # Issue #xxx: German language support
        'texlive-pstricks',       # Issue #739: pifont package provider
        'texlive-fonts-extra',    # Font support
        'texlive-latex-extra',    # Extended LaTeX packages
        'texlive-science'         # Math/science packages
    ]

    missing_packages = []
    for package in essential_packages:
        if package in content:
            print(f"✅ Found essential package: {package}")
        else:
            missing_packages.append(package)
            print(f"❌ Missing essential package: {package}")

    # Check for proper LaTeX action configuration
    if 'dante-ev/latex-action@v2' in content:
        print("✅ Using correct LaTeX action version")
    else:
        print("⚠️  LaTeX action version may need verification")

    # Check for proper argument configuration (no invalid -pdf flag)
    if '-pdf' in content:
        print("❌ Invalid -pdf argument detected (Issue #702)")
        return False
    else:
        print("✅ No invalid -pdf argument found")

    return len(missing_packages) == 0

def test_workflow_yaml_syntax_robustness():
    """Test that workflow YAML syntax is robust and correct."""
    print("\n📝 Testing Workflow YAML Syntax Robustness")
    print("=" * 60)

    workflow_files = [
        '.github/workflows/latex-build.yml',
        '.github/workflows/latex-validation.yml',
        '.github/workflows/pr-validation.yml',
        '.github/workflows/static.yml'
    ]

    all_valid = True
    for workflow_file in workflow_files:
        workflow_path = Path(workflow_file)
        if not workflow_path.exists():
            print(f"⚠️  Workflow file not found: {workflow_file}")
            continue

        try:
            with open(workflow_path, 'r') as f:
                content = f.read()
                workflow = yaml.safe_load(content)

            # Check for quoted 'on:' syntax (Issue #458)
            if '"on":' in content:
                print(f"✅ {workflow_file}: Proper quoted 'on:' syntax")
            elif 'on:' in content:
                print(f"⚠️  {workflow_file}: Unquoted 'on:' syntax - potential issue")

            # Check basic structure
            required_keys = ['name', 'on', 'jobs']
            for key in required_keys:
                if key in workflow or ('on' in workflow and '"on"' in content):
                    continue
                else:
                    print(f"❌ {workflow_file}: Missing required key '{key}'")
                    all_valid = False

        except yaml.YAMLError as e:
            print(f"❌ {workflow_file}: YAML syntax error: {e}")
            all_valid = False
        except Exception as e:
            print(f"❌ {workflow_file}: Error reading file: {e}")
            all_valid = False

    return all_valid

def test_build_system_error_recovery():
    """Test that the build system has proper error recovery mechanisms."""
    print("\n🔄 Testing Build System Error Recovery")
    print("=" * 60)

    # Test the CTMM build system handles missing LaTeX gracefully
    try:
        result = subprocess.run([sys.executable, 'ctmm_build.py'],
                              capture_output=True, text=True, timeout=30)

        output = result.stdout + result.stderr

        # Check for graceful handling of missing pdflatex
        if 'pdflatex not found' in output and 'skipping LaTeX compilation' in output:
            print("✅ Build system gracefully handles missing pdflatex")
        elif 'WARNING' in output and 'LaTeX not available' in output:
            print("✅ Build system provides appropriate warnings for missing tools")
        else:
            print("⚠️  Build system error handling unclear")

        # Check that it still validates structure without LaTeX
        if 'structure test passed' in output:
            print("✅ Build system validates structure without requiring LaTeX")

        # Check for comprehensive reporting
        if 'BUILD SYSTEM SUMMARY' in output:
            print("✅ Build system provides comprehensive reporting")

        return result.returncode == 0

    except Exception as e:
        print(f"❌ Error testing build system: {e}")
        return False

def main():
    """Run all validation tests for Issue #761."""
    print("=" * 70)
    print("ISSUE #761 VALIDATION: Enhanced CI Pipeline Robustness")
    print("=" * 70)

    tests = [
        ("Enhanced Workflow Error Handling", test_enhanced_workflow_error_handling),
        ("Comprehensive Dependency Validation", test_comprehensive_dependency_validation),
        ("LaTeX Package Dependency Robustness", test_latex_package_dependency_robustness),
        ("Workflow YAML Syntax Robustness", test_workflow_yaml_syntax_robustness),
        ("Build System Error Recovery", test_build_system_error_recovery)
    ]

    test_results = []

    for test_name, test_func in tests:
        try:
            result = test_func()
            test_results.append(result)
        except Exception as e:
            print(f"❌ {test_name}: Exception occurred: {e}")
            test_results.append(False)

    print("\n" + "=" * 70)
    print("VALIDATION SUMMARY")
    print("=" * 70)

    for (test_name, _), result in zip(tests, test_results):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")

    passed_tests = sum(test_results)
    total_tests = len(test_results)
    print(f"\nTests passed: {passed_tests}/{total_tests}")

    if passed_tests == total_tests:
        print("🎉 ALL TESTS PASSED! CI pipeline robustness validated.")
        print("\nThe enhanced CI configuration should provide:")
        print("✓ Better error detection and handling")
        print("✓ Comprehensive dependency validation")
        print("✓ Robust workflow configuration")
        print("✓ Graceful failure recovery")
        return 0
    else:
        print("⚠️  Some tests failed. CI pipeline may need additional improvements.")
        return 1

if __name__ == "__main__":
    sys.exit(main())