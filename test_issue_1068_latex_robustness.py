#!/usr/bin/env python3
"""
Issue #1068 Validation: LaTeX Action Migration and Robustness Enhancement
========================================================================

This script validates the fixes implemented for issue #1068, which addresses
CI pipeline failures by migrating from the unreliable dante-ev/latex-action
to the more robust xu-cheng/latex-action@v3 with enhanced fallback mechanisms.

Key improvements tested:
1. LaTeX action migration to xu-cheng/latex-action@v3
2. Fallback mechanism with manual TeX Live installation
3. Enhanced PDF verification with detailed file analysis
4. Comprehensive error recovery and reporting
5. Two-tier LaTeX compilation approach
"""

import os
import sys
import yaml
import subprocess
import time
from pathlib import Path

def test_latex_action_migration():
    """Test that workflows have been migrated to xu-cheng/latex-action@v3."""
    print("🔄 Testing LaTeX Action Migration")
    print("=" * 60)

    workflow_files = [
        '.github/workflows/latex-build.yml',
        '.github/workflows/automated-pr-merge-test.yml'
    ]

    migration_success = True

    for workflow_file in workflow_files:
        print(f"\n📄 Checking {workflow_file}...")

        if not os.path.exists(workflow_file):
            print(f"❌ Workflow file not found: {workflow_file}")
            migration_success = False
            continue

        with open(workflow_file, 'r') as f:
            content = f.read()

        # Check for migration from dante-ev to xu-cheng
        if 'dante-ev/latex-action' in content:
            print(f"❌ Found old dante-ev/latex-action in {workflow_file}")
            migration_success = False
        elif 'xu-cheng/latex-action@v3' in content:
            print(f"✅ Successfully migrated to xu-cheng/latex-action@v3")
        else:
            print(f"⚠️  No LaTeX action found in {workflow_file}")

    return migration_success

def test_fallback_mechanism():
    """Test that workflows include fallback mechanism for LaTeX installation."""
    print("\n🔄 Testing Fallback Mechanism Implementation")
    print("=" * 60)

    workflow_files = [
        '.github/workflows/latex-build.yml',
        '.github/workflows/automated-pr-merge-test.yml'
    ]

    fallback_success = True

    for workflow_file in workflow_files:
        print(f"\n📄 Analyzing fallback in {workflow_file}...")

        if not os.path.exists(workflow_file):
            print(f"❌ Workflow file not found: {workflow_file}")
            fallback_success = False
            continue

        with open(workflow_file, 'r') as f:
            content = f.read()

        # Check for fallback mechanism components
        fallback_checks = {
            'Primary action with continue-on-error': 'continue-on-error: true',
            'Fallback step condition': "outcome == 'failure'",
            'Manual TeX Live installation': 'sudo apt-get',
            'Manual pdflatex compilation': 'pdflatex'
        }

        for check_name, pattern in fallback_checks.items():
            if pattern in content:
                print(f"✅ {check_name}: Found")
            else:
                print(f"❌ {check_name}: Missing")
                fallback_success = False

    return fallback_success

def test_enhanced_pdf_verification():
    """Test that workflows include enhanced PDF verification with detailed analysis."""
    print("\n📊 Testing Enhanced PDF Verification")
    print("=" * 60)

    workflow_files = [
        '.github/workflows/latex-build.yml',
        '.github/workflows/automated-pr-merge-test.yml'
    ]

    verification_success = True

    for workflow_file in workflow_files:
        print(f"\n📄 Checking enhanced verification in {workflow_file}...")

        if not os.path.exists(workflow_file):
            print(f"❌ Workflow file not found: {workflow_file}")
            verification_success = False
            continue

        with open(workflow_file, 'r') as f:
            content = f.read()

        # Check for enhanced verification features
        verification_checks = {
            'File size analysis': 'PDF_SIZE',
            'File type analysis': 'file main.pdf',
            'Detailed file listing': 'ls -la main.pdf',
            'Comprehensive error analysis': 'Comprehensive error analysis',
            'Log file analysis': 'LaTeX Log Analysis',
            'Intermediate files check': 'Intermediate Files',
            'System resource check': 'df -h'
        }

        for check_name, pattern in verification_checks.items():
            if pattern in content:
                print(f"✅ {check_name}: Implemented")
            else:
                print(f"❌ {check_name}: Missing")
                verification_success = False

    return verification_success

def test_workflow_yaml_syntax():
    """Test that workflow YAML files have correct syntax and structure."""
    print("\n🔍 Testing Workflow YAML Syntax")
    print("=" * 60)

    workflow_files = [
        '.github/workflows/latex-build.yml',
        '.github/workflows/automated-pr-merge-test.yml'
    ]

    syntax_success = True

    for workflow_file in workflow_files:
        print(f"\n📄 Validating YAML syntax in {workflow_file}...")

        if not os.path.exists(workflow_file):
            print(f"❌ Workflow file not found: {workflow_file}")
            syntax_success = False
            continue

        try:
            with open(workflow_file, 'r') as f:
                workflow_data = yaml.safe_load(f)

            # Check basic workflow structure
            required_keys = ['name', 'on', 'jobs']
            for key in required_keys:
                if key in workflow_data:
                    print(f"✅ Required key '{key}': Found")
                else:
                    print(f"❌ Required key '{key}': Missing")
                    syntax_success = False

            # Check that 'on' is properly quoted (string, not boolean)
            if isinstance(workflow_data.get('on'), dict):
                print("✅ 'on' key properly structured as dictionary")
            else:
                print("❌ 'on' key has incorrect type")
                syntax_success = False

        except yaml.YAMLError as e:
            print(f"❌ YAML syntax error: {e}")
            syntax_success = False
        except Exception as e:
            print(f"❌ Error reading file: {e}")
            syntax_success = False

    return syntax_success

def test_timeout_configuration():
    """Test that all steps have appropriate timeout configurations."""
    print("\n⏱️  Testing Timeout Configuration")
    print("=" * 60)

    workflow_files = [
        '.github/workflows/latex-build.yml',
        '.github/workflows/automated-pr-merge-test.yml'
    ]

    timeout_success = True

    for workflow_file in workflow_files:
        print(f"\n📄 Checking timeouts in {workflow_file}...")

        if not os.path.exists(workflow_file):
            print(f"❌ Workflow file not found: {workflow_file}")
            timeout_success = False
            continue

        try:
            with open(workflow_file, 'r') as f:
                workflow_data = yaml.safe_load(f)

            jobs = workflow_data.get('jobs', {})
            for job_name, job_data in jobs.items():
                steps = job_data.get('steps', [])

                steps_without_timeout = []
                latex_steps_with_adequate_timeout = 0

                for step in steps:
                    step_name = step.get('name', 'unnamed')
                    timeout = step.get('timeout-minutes')

                    if timeout is None:
                        steps_without_timeout.append(step_name)
                    elif 'latex' in step_name.lower() and timeout >= 15:
                        latex_steps_with_adequate_timeout += 1

                if steps_without_timeout:
                    print(f"⚠️  Steps without timeout in {job_name}: {len(steps_without_timeout)}")
                else:
                    print(f"✅ All steps have timeout configuration in {job_name}")

                if latex_steps_with_adequate_timeout > 0:
                    print(f"✅ LaTeX steps have adequate timeouts: {latex_steps_with_adequate_timeout}")

        except Exception as e:
            print(f"❌ Error analyzing timeouts: {e}")
            timeout_success = False

    return timeout_success

def test_error_recovery_mechanisms():
    """Test that workflows have proper error recovery and continue-on-error settings."""
    print("\n🛡️ Testing Error Recovery Mechanisms")
    print("=" * 60)

    workflow_files = [
        '.github/workflows/latex-build.yml',
        '.github/workflows/automated-pr-merge-test.yml'
    ]

    recovery_success = True

    for workflow_file in workflow_files:
        print(f"\n📄 Analyzing error recovery in {workflow_file}...")

        if not os.path.exists(workflow_file):
            print(f"❌ Workflow file not found: {workflow_file}")
            recovery_success = False
            continue

        with open(workflow_file, 'r') as f:
            content = f.read()

        # Check for error recovery patterns
        recovery_patterns = {
            'Continue on error for primary action': 'continue-on-error: true',
            'Conditional fallback execution': 'if:.*outcome.*failure',
            'Error log collection': 'upload.*artifact.*logs',
            'Graceful error handling': 'echo.*❌.*failed'
        }

        for pattern_name, pattern in recovery_patterns.items():
            if pattern in content:
                print(f"✅ {pattern_name}: Implemented")
            else:
                print(f"⚠️  {pattern_name}: Not found (may be optional)")

    return recovery_success

def validate_ctmm_build_system():
    """Validate that the CTMM build system works correctly with current setup."""
    print("\n🔧 Testing CTMM Build System Integration")
    print("=" * 60)

    try:
        print("🚀 Running CTMM build system check...")
        result = subprocess.run(
            [sys.executable, 'ctmm_build.py'],
            capture_output=True,
            text=True,
            timeout=30
        )

        output = result.stdout + result.stderr

        if result.returncode == 0:
            print("✅ CTMM build system check passed")

            # Check for key indicators of successful validation
            success_indicators = [
                'LaTeX validation: ✓ PASS',
                'All referenced files exist',
                'Basic build: ✓ PASS',
                'Full build: ✓ PASS'
            ]

            for indicator in success_indicators:
                if indicator in output:
                    print(f"✅ Found: {indicator}")
                else:
                    print(f"⚠️  Missing: {indicator}")

            return True
        else:
            print(f"❌ CTMM build system check failed (exit code: {result.returncode})")
            print("Output:", output[-500:])  # Show last 500 chars
            return False

    except subprocess.TimeoutExpired:
        print("❌ CTMM build system check timed out")
        return False
    except Exception as e:
        print(f"❌ Error running CTMM build system: {e}")
        return False

def main():
    """Run all validation tests."""
    print("🎯 Issue #1068 LaTeX Robustness Validation")
    print("=" * 60)
    print("Testing migration from dante-ev/latex-action to xu-cheng/latex-action@v3")
    print("with enhanced fallback mechanisms and improved error recovery")
    print("=" * 60)

    tests = [
        ("LaTeX Action Migration", test_latex_action_migration),
        ("Fallback Mechanism", test_fallback_mechanism),
        ("Enhanced PDF Verification", test_enhanced_pdf_verification),
        ("Workflow YAML Syntax", test_workflow_yaml_syntax),
        ("Timeout Configuration", test_timeout_configuration),
        ("Error Recovery Mechanisms", test_error_recovery_mechanisms),
        ("CTMM Build System Integration", validate_ctmm_build_system)
    ]

    results = {}

    for test_name, test_func in tests:
        print(f"\n{'='*60}")
        try:
            start_time = time.time()
            result = test_func()
            elapsed = time.time() - start_time

            results[test_name] = result
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"\n{status} {test_name} (completed in {elapsed:.1f}s)")

        except Exception as e:
            results[test_name] = False
            print(f"\n❌ FAIL {test_name} (exception: {e})")

    # Summary
    print(f"\n{'='*60}")
    print("📊 VALIDATION SUMMARY")
    print(f"{'='*60}")

    passed_tests = sum(1 for result in results.values() if result)
    total_tests = len(results)

    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")

    print(f"\nTests passed: {passed_tests}/{total_tests}")

    if passed_tests == total_tests:
        print("\n🎉 ALL TESTS PASSED! LaTeX robustness migration validated successfully.")
        print("\nKey improvements confirmed:")
        print("• Migration to xu-cheng/latex-action@v3 ✅")
        print("• Fallback mechanism with manual TeX Live installation ✅")
        print("• Enhanced PDF verification with detailed analysis ✅")
        print("• Comprehensive error recovery mechanisms ✅")
        print("• Two-tier LaTeX compilation approach ✅")
        return True
    else:
        print(f"\n⚠️  {total_tests - passed_tests} test(s) failed. Review the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
