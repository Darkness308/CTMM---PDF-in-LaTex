#!/usr/bin/env python3
"""
Issue #996 Validation: Comprehensive CI LaTeX Build Robustness Enhancement
==========================================================================

This script validates the comprehensive fixes implemented for issue #996,
which addresses critical CI LaTeX build failures through enhanced package
dependencies, workflow configuration improvements, and build system robustness.

Key improvements tested:
1. LaTeX package dependencies (German language + FontAwesome support)
2. GitHub Actions workflow syntax and configuration
3. Enhanced build system with pdflatex availability checks
4. Comprehensive validation framework with error recovery
"""

import os
import sys
import yaml
import subprocess
from pathlib import Path

def test_latex_package_dependencies():
    """Test that all required LaTeX packages are configured in GitHub Actions."""
    print("\n📦 LATEX PACKAGE DEPENDENCIES VALIDATION")
    print("=" * 60)
    
    workflow_path = '.github/workflows/latex-build.yml'
    
    if not os.path.exists(workflow_path):
        print(f"❌ ERROR: Workflow file {workflow_path} not found")
        return False
    
    try:
        with open(workflow_path, 'r') as f:
            workflow = yaml.safe_load(f)
    except Exception as e:
        print(f"❌ ERROR: Failed to parse {workflow_path}: {e}")
        return False
    
    # Find LaTeX setup step
    latex_step = None
    for job in workflow.get('jobs', {}).values():
        for step in job.get('steps', []):
            if step.get('name') == 'Set up LaTeX':
                latex_step = step
                break
    
    if not latex_step:
        print("❌ ERROR: 'Set up LaTeX' step not found")
        return False
    
    packages = latex_step.get('with', {}).get('extra_system_packages', '')
    
    # Required packages for Issue #996
    required_packages = [
        'texlive-lang-german',       # German language support
        'texlive-fonts-recommended', # Recommended fonts
        'texlive-fonts-extra',       # Extra fonts (FontAwesome)
        'texlive-latex-extra',       # Extra LaTeX packages
        'texlive-pstricks'           # PostScript tricks (pifont)
    ]
    
    print("📋 Checking required packages...")
    all_found = True
    for pkg in required_packages:
        if pkg in packages:
            print(f"✅ FOUND: {pkg}")
        else:
            print(f"❌ MISSING: {pkg}")
            all_found = False
    
    # FontAwesome validation
    print("\n🎨 Validating FontAwesome support...")
    if 'texlive-fonts-extra' in packages:
        print("✅ FontAwesome support available through texlive-fonts-extra")
    else:
        print("❌ FontAwesome support missing")
        all_found = False
    
    return all_found

def test_fontawesome_integration():
    """Test that FontAwesome5 package is properly integrated in main.tex."""
    print("\n🎨 FONTAWESOME INTEGRATION VALIDATION")
    print("=" * 60)
    
    main_tex_path = 'main.tex'
    
    if not os.path.exists(main_tex_path):
        print(f"❌ ERROR: {main_tex_path} not found")
        return False
    
    try:
        with open(main_tex_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ ERROR: Failed to read {main_tex_path}: {e}")
        return False
    
    # Check for FontAwesome package
    if '\\usepackage{fontawesome5}' in content:
        print("✅ FontAwesome5 package loaded in main.tex")
    else:
        print("❌ FontAwesome5 package not found in main.tex")
        return False
    
    # Check for FontAwesome usage
    if '\\faCompass' in content:
        print("✅ FontAwesome icons used in document (navigation)")
    else:
        print("⚠️  No FontAwesome icons found in main.tex")
    
    return True

def test_github_actions_workflow_syntax():
    """Test that GitHub Actions workflows use proper syntax."""
    print("\n🔧 GITHUB ACTIONS WORKFLOW SYNTAX VALIDATION")
    print("=" * 60)
    
    workflows = [
        '.github/workflows/latex-build.yml',
        '.github/workflows/latex-validation.yml', 
        '.github/workflows/static.yml'
    ]
    
    all_valid = True
    
    for workflow_file in workflows:
        if not os.path.exists(workflow_file):
            print(f"⚠️  {workflow_file} not found")
            continue
            
        try:
            with open(workflow_file, 'r') as f:
                content = f.read()
                workflow = yaml.safe_load(content)
            
            # Check for quoted "on:" syntax
            if '"on":' in content or "'on':" in content:
                print(f"✅ {workflow_file}: Proper quoted 'on:' syntax")
            else:
                print(f"❌ {workflow_file}: Missing quoted 'on:' syntax")
                all_valid = False
                
            # Check YAML validity
            if workflow:
                print(f"✅ {workflow_file}: Valid YAML syntax")
            else:
                print(f"❌ {workflow_file}: Invalid YAML syntax")
                all_valid = False
                
        except Exception as e:
            print(f"❌ {workflow_file}: Parse error - {e}")
            all_valid = False
    
    return all_valid

def test_build_system_pdflatex_checks():
    """Test that build system has pdflatex availability checks."""
    print("\n🔧 BUILD SYSTEM PDFLATEX AVAILABILITY VALIDATION")
    print("=" * 60)
    
    build_script = 'ctmm_build.py'
    
    if not os.path.exists(build_script):
        print(f"❌ ERROR: {build_script} not found")
        return False
    
    try:
        with open(build_script, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ ERROR: Failed to read {build_script}: {e}")
        return False
    
    # Check for pdflatex availability checks
    checks = [
        "subprocess.run(['pdflatex', '--version']",
        "pdflatex not found",
        "skipping LaTeX compilation",
        "LaTeX not available"
    ]
    
    found_checks = []
    for check in checks:
        if check in content:
            found_checks.append(check)
    
    if len(found_checks) >= 3:
        print("✅ pdflatex availability checks implemented")
        for check in found_checks:
            print(f"   - Found: {check}")
    else:
        print("❌ Insufficient pdflatex availability checks")
        return False
    
    return True

def test_comprehensive_validation_framework():
    """Test that comprehensive validation framework is in place."""
    print("\n📊 COMPREHENSIVE VALIDATION FRAMEWORK")
    print("=" * 60)
    
    validation_scripts = [
        'validate_latex_syntax.py',
        'test_issue_743_validation.py',
        'test_issue_761_fix.py',
        'ctmm_build.py'
    ]
    
    all_present = True
    for script in validation_scripts:
        if os.path.exists(script):
            print(f"✅ Found: {script}")
        else:
            print(f"❌ Missing: {script}")
            all_present = False
    
    return all_present

def test_build_system_execution():
    """Test that the build system executes successfully."""
    print("\n⚙️ BUILD SYSTEM EXECUTION TEST")
    print("=" * 60)
    
    try:
        result = subprocess.run(
            [sys.executable, 'ctmm_build.py'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        output = result.stdout + result.stderr
        
        # Check for success indicators
        success_indicators = [
            "LaTeX validation: ✓ PASS",
            "All referenced files exist",
            "CTMM BUILD SYSTEM SUMMARY"
        ]
        
        found_indicators = 0
        for indicator in success_indicators:
            if indicator in output:
                found_indicators += 1
        
        if found_indicators >= 2:
            print("✅ Build system executes successfully")
            print(f"   Found {found_indicators}/{len(success_indicators)} success indicators")
            return True
        else:
            print("❌ Build system execution issues")
            print(f"   Only found {found_indicators}/{len(success_indicators)} success indicators")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Build system execution timed out")
        return False
    except Exception as e:
        print(f"❌ Build system execution error: {e}")
        return False

def main():
    """Run comprehensive Issue #996 validation."""
    print("======================================================================")
    print("ISSUE #996 VALIDATION: Comprehensive CI LaTeX Build Robustness")
    print("======================================================================")
    
    tests = [
        ("LaTeX Package Dependencies", test_latex_package_dependencies),
        ("FontAwesome Integration", test_fontawesome_integration),
        ("GitHub Actions Workflow Syntax", test_github_actions_workflow_syntax),
        ("Build System pdflatex Checks", test_build_system_pdflatex_checks),
        ("Comprehensive Validation Framework", test_comprehensive_validation_framework),
        ("Build System Execution", test_build_system_execution)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name}: Exception - {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n======================================================================")
    print("VALIDATION SUMMARY")
    print("======================================================================")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\nTests passed: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Issue #996 fixes validated successfully.")
        print("\nThe comprehensive CI LaTeX build robustness enhancements are working:")
        print("✓ LaTeX package dependencies properly configured")
        print("✓ FontAwesome integration functional")
        print("✓ GitHub Actions workflows use correct syntax")
        print("✓ Build system has robust pdflatex availability checks")
        print("✓ Comprehensive validation framework in place")
        print("✓ Build system executes successfully")
    else:
        print(f"\n❌ {total - passed} tests failed. Issue #996 validation incomplete.")
        return 1
    
    print("\n======================================================================")
    print("ISSUE #996 VALIDATION: SUCCESS ✅")
    print("CI pipeline robustness enhancements validated and operational.")
    print("======================================================================")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())