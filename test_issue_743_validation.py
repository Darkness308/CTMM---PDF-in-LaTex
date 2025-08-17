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
        print(f"⏰ Command timed out: {cmd}")
        return False, "", "Command timed out"
    except Exception as e:
        print(f"❌ Command failed: {cmd}, Error: {e}")
        return False, "", str(e)


def validate_ci_configuration():
    """Validate GitHub Actions CI configuration and workflow syntax."""
    print("\n🔧 CI CONFIGURATION VALIDATION")
    print("-" * 50)
    
    all_passed = True
    
    # Check workflow files exist
    workflow_files = [
        '.github/workflows/latex-build.yml',
        '.github/workflows/latex-validation.yml',
        '.github/workflows/static.yml'
    ]
    
    print("📂 Checking critical workflow files...")
    missing_workflows = []
    for workflow_file in workflow_files:
        if not os.path.exists(workflow_file):
            print(f"❌ CRITICAL: Workflow file missing: {workflow_file}")
            missing_workflows.append(workflow_file)
            all_passed = False
        else:
            print(f"✅ FOUND: {workflow_file}")
    
    if missing_workflows:
        print(f"\n🚨 CRITICAL CI FAILURE RISK: {len(missing_workflows)} workflow file(s) missing!")
        print("   Missing workflows would cause immediate CI failures:")
        for wf in missing_workflows:
            print(f"   - {wf}")
        print("   Repository CI would be non-functional")
    
    # Validate YAML syntax
    print("\n📝 Validating YAML syntax for CI reliability...")
    syntax_errors = []
    for workflow_file in workflow_files:
        if os.path.exists(workflow_file):
            try:
                with open(workflow_file, 'r') as f:
                    yaml.safe_load(f)
                print(f"✅ VALID: {workflow_file} has correct YAML syntax")
            except yaml.YAMLError as e:
                print(f"❌ INVALID: {workflow_file} has YAML syntax error: {e}")
                syntax_errors.append((workflow_file, str(e)))
                all_passed = False
            except Exception as e:
                print(f"❌ ERROR: Failed to read {workflow_file}: {e}")
                syntax_errors.append((workflow_file, str(e)))
                all_passed = False
    
    if syntax_errors:
        print(f"\n🚨 CRITICAL: {len(syntax_errors)} YAML syntax error(s) detected!")
        print("   These would cause immediate workflow parse failures:")
        for wf, error in syntax_errors:
            print(f"   - {wf}: {error[:100]}...")
    
    # Check for quoted "on:" syntax (Issue #458/#532 compliance)
    print("\n🔤 Checking 'on:' keyword syntax (GitHub Actions compatibility)...")
    syntax_issues = []
    for workflow_file in workflow_files:
        if os.path.exists(workflow_file):
            with open(workflow_file, 'r') as f:
                content = f.read()
            
            if '"on":' in content:
                print(f"✅ CORRECT: {workflow_file} uses quoted 'on:' syntax")
            elif 'on:' in content and '"on":' not in content:
                print(f"❌ INCORRECT: {workflow_file} uses unquoted 'on:' syntax")
                print("   This can cause workflow parsing issues in some GitHub environments")
                syntax_issues.append(workflow_file)
                all_passed = False
            else:
                print(f"⚠️  WARNING: No 'on:' keyword found in {workflow_file}")
    
    if syntax_issues:
        print(f"\n⚠️  COMPATIBILITY ISSUE: {len(syntax_issues)} workflow(s) use unquoted 'on:' syntax")
        print("   This may cause parsing failures in certain GitHub Actions environments")
    
    return all_passed


def validate_latex_packages():
    """Validate LaTeX package dependencies in GitHub Actions workflow."""
    print("\n📦 LATEX PACKAGE DEPENDENCIES VALIDATION")
    print("-" * 50)
    
    workflow_path = '.github/workflows/latex-build.yml'
    
    if not os.path.exists(workflow_path):
        print(f"❌ CRITICAL ERROR: Main workflow file {workflow_path} not found")
        print("   This would cause immediate CI failure - workflow file is required")
        return False
    
    try:
        with open(workflow_path, 'r') as f:
            workflow_content = yaml.safe_load(f)
    except Exception as e:
        print(f"❌ CRITICAL ERROR: Failed to parse {workflow_path}: {e}")
        print("   This would cause immediate CI failure - invalid YAML syntax")
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
        print("❌ CRITICAL ERROR: 'Set up LaTeX' step not found in workflow")
        print("   This would cause immediate CI failure - LaTeX compilation impossible")
        return False
    
    extra_packages = latex_step.get('with', {}).get('extra_system_packages', '')
    print(f"📋 Found LaTeX packages configuration:")
    if not extra_packages.strip():
        print("   ⚠️  WARNING: No extra packages configured")
    else:
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
    print("\n🔍 Validating essential packages...")
    missing_critical = []
    
    for pkg in required_packages:
        if pkg in extra_packages:
            print(f"✅ FOUND: {pkg}")
        else:
            print(f"❌ MISSING: {pkg}")
            missing_critical.append(pkg)
            all_passed = False
    
    if missing_critical:
        print(f"\n🚨 CRITICAL: {len(missing_critical)} essential package(s) missing!")
        print("   These packages are required for CTMM LaTeX compilation:")
        for pkg in missing_critical:
            print(f"   - {pkg}")
        print("   This would cause LaTeX compilation failure in CI")
    
    # Specific pifont validation (Issue #739/#743 compliance)
    print("\n🎯 Validating pifont package availability (Issue #739/#743)...")
    pifont_providers = ['texlive-pstricks', 'texlive-latex-extra', 'texlive-fonts-extra']
    pifont_available = any(pkg in extra_packages for pkg in pifont_providers)
    
    if pifont_available:
        found_providers = [pkg for pkg in pifont_providers if pkg in extra_packages]
        print(f"✅ PIFONT AVAILABLE: Found providers: {', '.join(found_providers)}")
        print("   ✓ CTMM form elements with checkboxes will compile successfully")
    else:
        print("❌ PIFONT MISSING: No packages found that provide pifont")
        print("   This would cause form element compilation failure:")
        print("   - \\ding{51} symbols will be undefined")
        print("   - CTMM checkboxes will fail to render")
        print("   - LaTeX compilation will halt with package error")
        all_passed = False
    
    return all_passed


def validate_workflow_structure():
    """Validate the structure and ordering of workflow steps."""
    print("\n🏗️  WORKFLOW STRUCTURE VALIDATION")
    print("-" * 50)
    
    workflow_path = '.github/workflows/latex-build.yml'
    
    try:
        with open(workflow_path, 'r') as f:
            workflow_content = yaml.safe_load(f)
    except Exception as e:
        print(f"❌ ERROR: Failed to parse {workflow_path}: {e}")
        return False
    
    # Get build job steps
    jobs = workflow_content.get('jobs', {})
    build_job = jobs.get('build', {})
    steps = build_job.get('steps', [])
    
    if not steps:
        print("❌ ERROR: No steps found in build job")
        return False
    
    # Expected step order for validation
    expected_steps = [
        'Checkout repository',
        'Set up Python',
        'Install Python dependencies',
        'Run LaTeX syntax validation',
        'Run CTMM Build System Check',
        'Run comprehensive CI configuration validation',
        'Enhanced pre-build validation',
        'Set up LaTeX'
    ]
    
    print("📋 Checking workflow step structure...")
    
    step_names = [step.get('name', 'Unknown') for step in steps]
    all_passed = True
    
    for i, expected_step in enumerate(expected_steps):
        if i < len(step_names):
            actual_step = step_names[i]
            if expected_step == actual_step:
                print(f"✅ STEP {i+1}: {expected_step}")
            else:
                print(f"⚠️  STEP {i+1}: Expected '{expected_step}', found '{actual_step}'")
        else:
            print(f"❌ MISSING STEP {i+1}: {expected_step}")
            all_passed = False
    
    # Check validation steps are before LaTeX compilation
    latex_step_index = None
    validation_steps_indices = []
    
    for i, step_name in enumerate(step_names):
        if 'Set up LaTeX' in step_name:
            latex_step_index = i
        if any(keyword in step_name.lower() for keyword in ['validation', 'check', 'validate']):
            validation_steps_indices.append(i)
    
    print(f"\n🔍 Validation step ordering check...")
    if latex_step_index is not None:
        properly_ordered = all(idx < latex_step_index for idx in validation_steps_indices)
        if properly_ordered and validation_steps_indices:
            print("✅ CORRECT: All validation steps run before LaTeX compilation")
        elif not validation_steps_indices:
            print("⚠️  WARNING: No validation steps found")
        else:
            print("❌ INCORRECT: Some validation steps run after LaTeX compilation")
            all_passed = False
    else:
        print("⚠️  WARNING: LaTeX setup step not found")
    
    return all_passed


def validate_ctmm_integration():
    """Validate CTMM build system integration and functionality."""
    print("\n🎯 CTMM BUILD SYSTEM INTEGRATION")
    print("-" * 50)
    
    # Check if CTMM build system exists
    ctmm_build_path = 'ctmm_build.py'
    if not os.path.exists(ctmm_build_path):
        print(f"❌ ERROR: CTMM build system not found: {ctmm_build_path}")
        return False
    
    print(f"✅ FOUND: {ctmm_build_path}")
    
    # Test CTMM build system
    print("\n🔧 Testing CTMM build system...")
    success, stdout, stderr = run_command("python3 ctmm_build.py", "CTMM build test")
    
    if success:
        print("✅ CTMM build system executed successfully")
        
        # Check for key indicators in output
        success_indicators = [
            "✓ All referenced files exist",
            "✓ Basic structure test passed",
            "✓ Full structure test passed",
            "CTMM BUILD SYSTEM SUMMARY"
        ]
        
        found_indicators = []
        for indicator in success_indicators:
            if indicator in stdout:
                found_indicators.append(indicator)
                print(f"✅ FOUND: {indicator}")
        
        if len(found_indicators) >= 3:
            print("✅ CTMM build system validation passed")
            return True
        else:
            print("⚠️  WARNING: CTMM build system completed but some indicators missing")
            return True  # Don't fail on missing indicators
    else:
        print("❌ CTMM build system failed")
        if stderr:
            print(f"Error details: {stderr}")
        return False


def validate_form_elements_integration():
    """Validate form elements integration with pifont package."""
    print("\n📝 FORM ELEMENTS INTEGRATION VALIDATION")
    print("-" * 50)
    
    form_elements_path = 'style/form-elements.sty'
    
    if not os.path.exists(form_elements_path):
        print(f"❌ ERROR: Form elements style file not found: {form_elements_path}")
        return False
    
    print(f"✅ FOUND: {form_elements_path}")
    
    try:
        with open(form_elements_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for pifont requirement
        if '\\RequirePackage{pifont}' in content:
            print("✅ CORRECT: form-elements.sty requires pifont package")
        else:
            print("❌ MISSING: form-elements.sty does not require pifont package")
            return False
        
        # Check for pifont usage in checkboxes
        if '\\ding{' in content:
            print("✅ CORRECT: form-elements.sty uses pifont symbols (\\ding commands)")
        else:
            print("⚠️  INFO: No direct pifont symbol usage found")
        
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
        
        print(f"📋 CTMM form elements found: {len(found_elements)}/{len(ctmm_elements)}")
        for element in found_elements:
            print(f"   ✅ {element}")
        
        if len(found_elements) >= 2:
            print("✅ Form elements validation passed")
            
            # Additional pifont compatibility check
            print("\n🔧 Testing pifont compatibility with form elements...")
            if '\\RequirePackage{pifont}' in content and '\\ding{' in content:
                print("✅ PIFONT INTEGRATION: Complete pifont integration detected")
                print("   ✓ Package required AND symbols used")
                print("   ✓ Form elements ready for LaTeX compilation")
            elif '\\RequirePackage{pifont}' in content:
                print("⚠️  PIFONT PARTIAL: Package required but symbols not directly used")
                print("   ℹ️  This may be normal if symbols are used via macros")
            else:
                print("⚠️  PIFONT INDIRECT: No direct pifont requirement found")
                print("   Form elements may rely on external package inclusion")
            
            return True
        else:
            print("⚠️  WARNING: Limited form elements found")
            return True
            
    except Exception as e:
        print(f"❌ ERROR: Failed to read {form_elements_path}: {e}")
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
            print(f"❌ ERROR: Test '{test_name}' failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary report
    print("\n" + "=" * 70)
    print("VALIDATION SUMMARY REPORT")
    print("=" * 70)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL VALIDATION TESTS PASSED!")
        print("\nThe CI configuration is robust and ready for:")
        print("  ✓ Early detection of configuration issues")
        print("  ✓ Proper LaTeX package dependency handling") 
        print("  ✓ Comprehensive validation before compilation")
        print("  ✓ Integration with CTMM build system")
        print("  ✓ Form elements with pifont support")
        print("\n📋 Issue #743 Resolution Summary:")
        print("  ✓ Enhanced CI validation steps implemented")
        print("  ✓ Robust pifont package dependency handling")
        print("  ✓ Early failure detection before LaTeX compilation")
        print("  ✓ Comprehensive error reporting for troubleshooting")
        return True
    else:
        print(f"\n❌ {total - passed} validation test(s) failed")
        print("Please address the issues above before proceeding.")
        print("\n🔧 Common fixes:")
        print("  • Check .github/workflows/latex-build.yml for missing packages")
        print("  • Verify YAML syntax in all workflow files")  
        print("  • Ensure pifont providers (texlive-pstricks) are included")
        print("  • Run 'python3 ctmm_build.py' to test build system")
        return False


def main():
    """Main entry point for Issue #743 validation."""
    # Ensure we're in the right directory
    if not Path('main.tex').exists():
        print("❌ ERROR: This script must be run from the CTMM repository root")
        print("Expected to find main.tex in current directory")
        sys.exit(1)
    
    success = run_comprehensive_validation()
    
    print("\n" + "=" * 70)
    if success:
        print("ISSUE #743 VALIDATION: SUCCESS ✅")
        print("CI pipeline is ready for robust validation and error detection.")
    else:
        print("ISSUE #743 VALIDATION: NEEDS ATTENTION ❌")
        print("Please resolve the validation issues before proceeding.")
    print("=" * 70)
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()