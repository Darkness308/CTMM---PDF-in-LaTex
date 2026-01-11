#!/usr/bin/env python3
"""
Comprehensive validation test suite for Issue #743: CI Configuration and LaTeX Package Dependencies

This script provides comprehensive validation for:
1. CI configuration and GitHub Actions workflow syntax
2. LaTeX package dependencies (especially pifont and related packages)
3. CTMM build system integration
4. Workflow structure and validation step ordering

Addresses Issue #743 by adding robust validation to catch configuration issues early in CI pipeline.
"""

import yaml
import os
import sys
import subprocess
from pathlib import Path
import json


def run_command(cmd, description="", capture_output=True):
    """Run a command and return success status and output."""
    try:
        if capture_output:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120)
            return result.returncode == 0, result.stdout, result.stderr
        else:
            result = subprocess.run(cmd, shell=True, timeout=120)
            return result.returncode == 0, "", ""
    except subprocess.TimeoutExpired:
        print(f"[SYM] Command timed out: {cmd}")
        return False, "", "Command timed out"
    except Exception as e:
        print(f"[FAIL] Command failed: {cmd}, Error: {e}")
        return False, "", str(e)


def validate_ci_configuration():
    """Validate GitHub Actions CI configuration and workflow syntax."""
    print("\n[FIX] CI CONFIGURATION VALIDATION")
    print("-" * 50)

    all_passed = True

    # Check workflow files exist
    workflow_files = [
        '.github/workflows/latex-build.yml',
        '.github/workflows/latex-validation.yml',
        '.github/workflows/static.yml'
    ]

    print("[FOLDER] Checking workflow files...")
    for workflow_file in workflow_files:
        if not os.path.exists(workflow_file):
            print(f"[FAIL] FAIL: Workflow file missing: {workflow_file}")
            all_passed = False
        else:
            print(f"[PASS] FOUND: {workflow_file}")

    # Validate YAML syntax
    print("\n[NOTE] Validating YAML syntax...")
    for workflow_file in workflow_files:
        if os.path.exists(workflow_file):
            try:
                with open(workflow_file, 'r') as f:
                    yaml.safe_load(f)
                print(f"[PASS] VALID: {workflow_file} has correct YAML syntax")
            except yaml.YAMLError as e:
                print(f"[FAIL] INVALID: {workflow_file} has YAML syntax error: {e}")
                all_passed = False
            except Exception as e:
                print(f"[FAIL] ERROR: Failed to read {workflow_file}: {e}")
                all_passed = False

    # Check for quoted "on:" syntax (Issue #458/#532 compliance)
    print("\n[EMOJI] Checking 'on:' keyword syntax...")
    for workflow_file in workflow_files:
        if os.path.exists(workflow_file):
            with open(workflow_file, 'r') as f:
                content = f.read()

            if '"on":' in content:
                print(f"[PASS] CORRECT: {workflow_file} uses quoted 'on:' syntax")
            elif 'on:' in content and '"on":' not in content:
                print(f"[FAIL] INCORRECT: {workflow_file} uses unquoted 'on:' syntax")
                all_passed = False
            else:
                print(f"[WARN]  WARNING: No 'on:' keyword found in {workflow_file}")

    return all_passed


def validate_latex_packages():
    """Validate LaTeX package dependencies in GitHub Actions workflow."""
    print("\n[PACKAGE] LATEX PACKAGE DEPENDENCIES VALIDATION")
    print("-" * 50)

    workflow_path = '.github/workflows/latex-build.yml'

    if not os.path.exists(workflow_path):
        print(f"[FAIL] ERROR: Main workflow file {workflow_path} not found")
        return False

    try:
        with open(workflow_path, 'r') as f:
            workflow_content = yaml.safe_load(f)
    except Exception as e:
        print(f"[FAIL] ERROR: Failed to parse {workflow_path}: {e}")
        return False

    # Find the LaTeX action step
    jobs = workflow_content.get('jobs', {})
    build_job = jobs.get('build', {})
    steps = build_job.get('steps', [])

    latex_step = None
    for step in steps:
        if step.get('name') == 'Set up LaTeX':
            uses = str(step.get('uses', ''))
            if 'xu-cheng/latex-action' in uses or 'dante-ev/latex-action' in uses:
                latex_step = step
                break

    if not latex_step:
        print("[FAIL] ERROR: 'Set up LaTeX' step with xu-cheng/latex-action or dante-ev/latex-action not found in workflow")
        return False

    # Check that a supported action is used
    action_uses = latex_step.get('uses', '')
    if 'dante-ev/latex-action@v0.2.0' in action_uses:
        print("[PASS] CORRECT: Using dante-ev/latex-action@v0.2.0")
    elif 'xu-cheng/latex-action@v3' in action_uses:
        print("[PASS] CORRECT: Using xu-cheng/latex-action@v3")
    else:
        print(f"[FAIL] ERROR: Expected dante-ev/latex-action@v0.2.0 or xu-cheng/latex-action@v3, found: {action_uses}")
        return False

    extra_packages = latex_step.get('with', {}).get('extra_system_packages', '')
    print(f"[TEST] Found LaTeX packages configuration:")
    for line in extra_packages.strip().split('\n'):
        if line.strip():
            print(f"   - {line.strip()}")

    # Essential package validation
    required_packages = [
        'texlive-lang-german',       # German language support
        'texlive-fonts-recommended', # Recommended fonts
        'texlive-latex-recommended', # Recommended LaTeX packages
        'texlive-latex-extra',       # Extra LaTeX packages
        'texlive-fonts-extra',       # Extra fonts
        'texlive-science',           # Scientific packages
        'texlive-pstricks'           # PostScript tricks (contains pifont)
    ]

    all_passed = True
    print("\n[SEARCH] Validating essential packages...")

    for pkg in required_packages:
        if pkg in extra_packages:
            print(f"[PASS] FOUND: {pkg}")
        else:
            print(f"[FAIL] MISSING: {pkg}")
            all_passed = False

    # Specific pifont validation (Issue #739 compliance)
    print("\n[TARGET] Validating pifont package availability...")
    pifont_providers = ['texlive-pstricks', 'texlive-latex-extra', 'texlive-fonts-extra']
    pifont_available = any(pkg in extra_packages for pkg in pifont_providers)

    if pifont_available:
        found_providers = [pkg for pkg in pifont_providers if pkg in extra_packages]
        print(f"[PASS] PIFONT AVAILABLE: Found providers: {', '.join(found_providers)}")
    else:
        print("[FAIL] PIFONT MISSING: No packages found that provide pifont")
        all_passed = False

    return all_passed


def validate_workflow_structure():
    """Validate the structure and ordering of workflow steps."""
    print("\n[EMOJI]  WORKFLOW STRUCTURE VALIDATION")
    print("-" * 50)

    workflow_path = '.github/workflows/latex-build.yml'

    try:
        with open(workflow_path, 'r') as f:
            workflow_content = yaml.safe_load(f)
    except Exception as e:
        print(f"[FAIL] ERROR: Failed to parse {workflow_path}: {e}")
        return False

    # Get build job steps
    jobs = workflow_content.get('jobs', {})
    build_job = jobs.get('build', {})
    steps = build_job.get('steps', [])

    if not steps:
        print("[FAIL] ERROR: No steps found in build job")
        return False

    # Expected step order for validation (core validation steps, LaTeX can be later)
    expected_core_steps = [
        'Checkout repository',
        'Set up Python',
        'Install Python dependencies',
        'Run LaTeX syntax validation',
        'Run CTMM Build System Check',
        'Run comprehensive CI validation',
        'Enhanced pre-build validation',
        'Check system resources before LaTeX compilation',
        'Assess GitHub Actions runner environment',
        'Enhanced CI environment validation',
        'CI failure prevention analysis',
        'Set up LaTeX'
    ]

    print("[TEST] Checking workflow step structure...")

    step_names = [step.get('name', 'Unknown') for step in steps]
    all_passed = True

    for i, expected_step in enumerate(expected_core_steps):
        if i < len(step_names):
            actual_step = step_names[i]
            if expected_step == actual_step:
                print(f"[PASS] STEP {i+1}: {expected_step}")
            else:
                print(f"[WARN]  STEP {i+1}: Expected '{expected_step}', found '{actual_step}'")
        else:
            print(f"[FAIL] MISSING STEP {i+1}: {expected_step}")
            all_passed = False

    # Check validation steps are before LaTeX compilation
    latex_step_index = None
    validation_steps_indices = []

    for i, step_name in enumerate(step_names):
        if 'Set up LaTeX' in step_name:
            latex_step_index = i
        if any(keyword in step_name.lower() for keyword in ['validation', 'check', 'validate']):
            validation_steps_indices.append(i)

    print(f"\n[SEARCH] Validation step ordering check...")
    if latex_step_index is not None:
        properly_ordered = all(idx < latex_step_index for idx in validation_steps_indices)
        if properly_ordered and validation_steps_indices:
            print("[PASS] CORRECT: All validation steps run before LaTeX compilation")
        elif not validation_steps_indices:
            print("[WARN]  WARNING: No validation steps found")
        else:
            print("[FAIL] INCORRECT: Some validation steps run after LaTeX compilation")
            all_passed = False
    else:
        print("[WARN]  WARNING: LaTeX setup step not found")

    return all_passed


def validate_ctmm_integration():
    """Validate CTMM build system integration and functionality."""
    print("\n[TARGET] CTMM BUILD SYSTEM INTEGRATION")
    print("-" * 50)

    # Check if CTMM build system exists
    ctmm_build_path = 'ctmm_build.py'
    if not os.path.exists(ctmm_build_path):
        print(f"[FAIL] ERROR: CTMM build system not found: {ctmm_build_path}")
        return False

    print(f"[PASS] FOUND: {ctmm_build_path}")

    # Test CTMM build system
    print("\n[FIX] Testing CTMM build system...")
    success, stdout, stderr = run_command("python3 ctmm_build.py", "CTMM build test")

    if success:
        print("[PASS] CTMM build system executed successfully")

        # Check for key indicators in output
        success_indicators = [
            "[OK] All referenced files exist",
            "[OK] Basic structure test passed",
            "[OK] Full structure test passed",
            "CTMM BUILD SYSTEM SUMMARY"
        ]

        found_indicators = []
        for indicator in success_indicators:
            if indicator in stdout:
                found_indicators.append(indicator)
                print(f"[PASS] FOUND: {indicator}")

        if len(found_indicators) >= 3:
            print("[PASS] CTMM build system validation passed")
            return True
        else:
            print("[WARN]  WARNING: CTMM build system completed but some indicators missing")
            return True  # Don't fail on missing indicators
    else:
        print("[FAIL] CTMM build system failed")
        if stderr:
            print(f"Error details: {stderr}")
        return False


def validate_form_elements_integration():
    """Validate form elements integration with pifont package."""
    print("\n[NOTE] FORM ELEMENTS INTEGRATION VALIDATION")
    print("-" * 50)

    form_elements_path = 'style/form-elements.sty'

    if not os.path.exists(form_elements_path):
        print(f"[FAIL] ERROR: Form elements style file not found: {form_elements_path}")
        return False

    print(f"[PASS] FOUND: {form_elements_path}")

    try:
        with open(form_elements_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check for pifont requirement
        if '\\RequirePackage{pifont}' in content:
            print("[PASS] CORRECT: form-elements.sty requires pifont package")
        else:
            print("[FAIL] MISSING: form-elements.sty does not require pifont package")
            return False

        # Check for pifont usage in checkboxes
        if '\\ding{' in content:
            print("[PASS] CORRECT: form-elements.sty uses pifont symbols (\\ding commands)")
        else:
            print("[WARN]  INFO: No direct pifont symbol usage found")

        # Check for CTMM form elements
        ctmm_elements = [
            'ctmmCheckBox',
            'ctmmTextField',
            'ctmmTextArea',
            'ctmmRadioButton'
        ]

        found_elements = []
        for element in ctmm_elements:
            if element in content:
                found_elements.append(element)

        print(f"[TEST] CTMM form elements found: {len(found_elements)}/{len(ctmm_elements)}")
        for element in found_elements:
            print(f"   [PASS] {element}")

        if len(found_elements) >= 2:
            print("[PASS] Form elements validation passed")
            return True
        else:
            print("[WARN]  WARNING: Limited form elements found")
            return True

    except Exception as e:
        print(f"[FAIL] ERROR: Failed to read {form_elements_path}: {e}")
        return False


def run_comprehensive_validation():
    """Run all validation tests and provide comprehensive report."""
    print("=" * 70)
    print("ISSUE #743 COMPREHENSIVE VALIDATION SUITE")
    print("CI Configuration and LaTeX Package Dependencies")
    print("=" * 70)

    validation_tests = [
        ("CI Configuration", validate_ci_configuration),
        ("LaTeX Package Dependencies", validate_latex_packages),
        ("Workflow Structure", validate_workflow_structure),
        ("CTMM Build System Integration", validate_ctmm_integration),
        ("Form Elements Integration", validate_form_elements_integration),
    ]

    results = []

    for test_name, test_func in validation_tests:
        print(f"\n{'='*20} {test_name.upper()} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"[FAIL] ERROR: Test '{test_name}' failed with exception: {e}")
            results.append((test_name, False))

    # Summary report
    print("\n" + "=" * 70)
    print("VALIDATION SUMMARY REPORT")
    print("=" * 70)

    passed = 0
    total = len(results)

    for test_name, result in results:
        status = "[PASS] PASS" if result else "[FAIL] FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1

    print(f"\nOverall Result: {passed}/{total} tests passed")

    if passed == total:
        print("\n[SUCCESS] ALL VALIDATION TESTS PASSED!")
        print("\nThe CI configuration is robust and ready for:")
        print("  [OK] Early detection of configuration issues")
        print("  [OK] Proper LaTeX package dependency handling")
        print("  [OK] Comprehensive validation before compilation")
        print("  [OK] Integration with CTMM build system")
        print("  [OK] Form elements with pifont support")
        return True
    else:
        print(f"\n[FAIL] {total - passed} validation test(s) failed")
        print("Please address the issues above before proceeding.")
        return False


def main():
    """Main entry point for Issue #743 validation."""
    # Ensure we're in the right directory
    if not Path('main.tex').exists():
        print("[FAIL] ERROR: This script must be run from the CTMM repository root")
        print("Expected to find main.tex in current directory")
        sys.exit(1)

    success = run_comprehensive_validation()

    print("\n" + "=" * 70)
    if success:
        print("ISSUE #743 VALIDATION: SUCCESS [PASS]")
        print("CI pipeline is ready for robust validation and error detection.")
    else:
        print("ISSUE #743 VALIDATION: NEEDS ATTENTION [FAIL]")
        print("Please resolve the validation issues before proceeding.")
    print("=" * 70)

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
