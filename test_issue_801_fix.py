#!/usr/bin/env python3

"""
Test script to validate the resolution of Issue #801.
Verifies that all PR overview requirements for CI LaTeX build failure fixes are implemented.
"""

import os
import yaml
import subprocess
import sys
from pathlib import Path

def test_github_actions_syntax():
    """Test that GitHub Actions workflows have correct syntax."""
    print("\n🔧 Testing GitHub Actions workflow syntax...")
    
    workflow_files = [
        '.github/workflows/latex-build.yml',
        '.github/workflows/latex-validation.yml', 
        '.github/workflows/static.yml'
    ]
    
    for workflow_file in workflow_files:
        if not os.path.exists(workflow_file):
            print(f"❌ FAILED: Missing workflow file {workflow_file}")
            return False
            
        with open(workflow_file, 'r') as f:
            content = f.read()
            
        # Check for quoted "on:" syntax
        if '"on":' not in content:
            print(f"❌ FAILED: {workflow_file} does not use quoted 'on:' syntax")
            return False
            
        # Validate YAML syntax
        try:
            yaml.safe_load(content)
        except yaml.YAMLError as e:
            print(f"❌ FAILED: {workflow_file} has invalid YAML syntax: {e}")
            return False
            
    print("✅ SUCCESS: All workflow files have correct syntax")
    return True

def test_latex_action_version():
    """Test that dante-ev/latex-action uses correct version."""
    print("\n📦 Testing LaTeX action version...")
    
    with open('.github/workflows/latex-build.yml', 'r') as f:
        content = f.read()
    
    # Should use v2, not v2.0.0
    if 'dante-ev/latex-action@v2.0.0' in content:
        print("❌ FAILED: Using incorrect version v2.0.0 (should be v2)")
        return False
        
    if 'dante-ev/latex-action@v2' not in content:
        print("❌ FAILED: dante-ev/latex-action@v2 not found")
        return False
        
    print("✅ SUCCESS: Using correct LaTeX action version v2")
    return True

def test_pdflatex_arguments():
    """Test that pdflatex arguments are correct (no invalid -pdf)."""
    print("\n⚙️  Testing pdflatex arguments...")
    
    with open('.github/workflows/latex-build.yml', 'r') as f:
        content = f.read()
    
    # Check that -pdf argument is NOT present
    lines = content.split('\n')
    for line in lines:
        if 'args:' in line and '-pdf' in line:
            print(f"❌ FAILED: Found invalid -pdf argument in: {line.strip()}")
            return False
    
    # Check that required arguments are present
    expected_args = ['-interaction=nonstopmode', '-halt-on-error', '-shell-escape']
    args_line = None
    for line in lines:
        if 'args:' in line:
            args_line = line.strip()
            break
    
    if not args_line:
        print("❌ FAILED: No args line found in workflow")
        return False
        
    for arg in expected_args:
        if arg not in args_line:
            print(f"❌ FAILED: Missing required argument {arg}")
            return False
    
    print("✅ SUCCESS: pdflatex arguments are correct")
    return True

def test_german_language_support():
    """Test that German language packages are included."""
    print("\n🇩🇪 Testing German language support...")
    
    with open('.github/workflows/latex-build.yml', 'r') as f:
        content = f.read()
    
    required_packages = [
        'texlive-lang-german',
        'texlive-fonts-recommended',
        'texlive-latex-recommended',
        'texlive-pstricks'
    ]
    
    for package in required_packages:
        if package not in content:
            print(f"❌ FAILED: Missing required package {package}")
            return False
    
    print("✅ SUCCESS: All German language packages are included")
    return True

def test_pdflatex_availability_checks():
    """Test that build system includes pdflatex availability checks."""
    print("\n🔍 Testing pdflatex availability checks...")
    
    if not os.path.exists('ctmm_build.py'):
        print("❌ FAILED: ctmm_build.py not found")
        return False
        
    with open('ctmm_build.py', 'r') as f:
        content = f.read()
    
    # Check for pdflatex availability detection
    if "subprocess.run(['pdflatex', '--version']" not in content:
        print("❌ FAILED: No pdflatex availability check found")
        return False
        
    if 'pdflatex not found' not in content:
        print("❌ FAILED: No pdflatex not found handling")
        return False
        
    print("✅ SUCCESS: pdflatex availability checks are implemented")
    return True

def test_build_system_robustness():
    """Test that the build system runs successfully."""
    print("\n🏗️  Testing build system robustness...")
    
    try:
        result = subprocess.run(
            ['python3', 'ctmm_build.py'],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode != 0:
            print(f"❌ FAILED: Build system exited with code {result.returncode}")
            print(f"Error: {result.stderr}")
            return False
        
        # Check for success indicators in both stdout and stderr
        full_output = result.stdout + result.stderr
        
        if 'CTMM BUILD SYSTEM SUMMARY' not in full_output:
            print("❌ FAILED: Build system summary not found")
            return False
            
        if 'test passed' not in full_output:
            print("❌ FAILED: Structure tests did not pass")
            return False
            
        print("✅ SUCCESS: Build system runs successfully")
        return True
        
    except subprocess.TimeoutExpired:
        print("❌ FAILED: Build system timed out")
        return False
    except Exception as e:
        print(f"❌ FAILED: Error running build system: {e}")
        return False

def test_comprehensive_validation():
    """Test that comprehensive validation suite works."""
    print("\n🧪 Testing comprehensive validation suite...")
    
    validation_files = [
        'validate_latex_syntax.py',
        'validate_workflow_syntax.py',
        'test_issue_743_validation.py'
    ]
    
    for val_file in validation_files:
        if not os.path.exists(val_file):
            print(f"❌ FAILED: Missing validation file {val_file}")
            return False
    
    # Test LaTeX syntax validation
    try:
        result = subprocess.run(
            ['python3', 'validate_latex_syntax.py'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
            print(f"❌ FAILED: LaTeX syntax validation failed")
            return False
            
        if '✅ All validation checks passed!' not in result.stdout:
            print("❌ FAILED: LaTeX validation did not pass all checks")
            return False
            
    except Exception as e:
        print(f"❌ FAILED: Error running LaTeX validation: {e}")
        return False
    
    print("✅ SUCCESS: Comprehensive validation suite works")
    return True

def test_unit_test_coverage():
    """Test that unit tests pass."""
    print("\n🧮 Testing unit test coverage...")
    
    try:
        result = subprocess.run(
            ['python3', 'test_ctmm_build.py'],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode != 0:
            print(f"❌ FAILED: Unit tests failed with code {result.returncode}")
            return False
            
        # Check for test completion - Unit tests can have stderr output but still pass
        stderr_output = result.stderr.lower() if result.stderr else ""
        stdout_output = result.stdout.lower() if result.stdout else ""
        
        if result.returncode != 0:
            print(f"❌ FAILED: Unit tests failed with return code {result.returncode}")
            return False
            
        # Look for success indicators in both stdout and stderr
        success_indicators = ['ok', 'ran', 'tests']
        if not any(indicator in stdout_output or indicator in stderr_output for indicator in success_indicators):
            print("❌ FAILED: Unit tests did not show completion indicators")
            return False
            
        # Check for test count and results
        if 'ran' in stdout_output and 'ok' in stdout_output:
            lines = result.stdout.split('\n') + result.stderr.split('\n')
            for line in lines:
                if 'Ran' in line and 'tests' in line:
                    print(f"✅ SUCCESS: {line.strip()}")
                    return True
        
        print("✅ SUCCESS: Unit tests completed successfully")
        return True
        
    except subprocess.TimeoutExpired:
        print("❌ FAILED: Unit tests timed out")
        return False
    except Exception as e:
        print(f"❌ FAILED: Error running unit tests: {e}")
        return False

def main():
    """Main test function for Issue #801 validation."""
    print("=" * 80)
    print("ISSUE #801 VALIDATION SUITE")
    print("Pull Request Overview - CI LaTeX Build Failure Fixes")
    print("=" * 80)
    
    tests = [
        ("GitHub Actions Syntax", test_github_actions_syntax),
        ("LaTeX Action Version", test_latex_action_version),
        ("PDFLaTeX Arguments", test_pdflatex_arguments),
        ("German Language Support", test_german_language_support),
        ("PDFLaTeX Availability Checks", test_pdflatex_availability_checks),
        ("Build System Robustness", test_build_system_robustness),
        ("Comprehensive Validation", test_comprehensive_validation),
        ("Unit Test Coverage", test_unit_test_coverage)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\n{'=' * 60}")
        print(f"TESTING: {test_name}")
        print('=' * 60)
        
        try:
            if test_func():
                passed += 1
                print(f"✅ PASSED: {test_name}")
            else:
                failed += 1
                print(f"❌ FAILED: {test_name}")
        except Exception as e:
            failed += 1
            print(f"❌ ERROR in {test_name}: {e}")
    
    print("\n" + "=" * 80)
    print("ISSUE #801 VALIDATION SUMMARY")
    print("=" * 80)
    print(f"✅ Tests Passed: {passed}")
    print(f"❌ Tests Failed: {failed}")
    print(f"📊 Success Rate: {passed}/{passed + failed} ({100 * passed / (passed + failed):.1f}%)")
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED!")
        print("Issue #801 PR overview requirements are fully implemented.")
        print("CI LaTeX build failure fixes are working correctly.")
        return True
    else:
        print(f"\n⚠️  {failed} TESTS FAILED")
        print("Some PR overview requirements may not be fully implemented.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)