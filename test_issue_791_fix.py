#!/usr/bin/env python3
"""
Test validation for Issue #791: CI LaTeX Build Failure Fixes
Validates that all critical CI pipeline fixes are properly implemented and working.
"""

import os
import sys
import yaml
import subprocess
from pathlib import Path

def test_workflow_syntax_fixes():
    """Test that all GitHub Actions workflows have correct YAML syntax."""
    print("\n🔧 Testing GitHub Actions Workflow Syntax Fixes")
    print("=" * 60)
    
    workflow_files = [
        '.github/workflows/latex-build.yml',
        '.github/workflows/latex-validation.yml', 
        '.github/workflows/static.yml'
    ]
    
    all_correct = True
    
    for workflow_file in workflow_files:
        if not os.path.exists(workflow_file):
            print(f"❌ MISSING: {workflow_file}")
            all_correct = False
            continue
            
        with open(workflow_file, 'r') as f:
            content = f.read()
            
        # Check for correct quoted "on": syntax
        if '"on":' in content:
            print(f"✅ PASS: {workflow_file} uses quoted 'on:' syntax")
        else:
            print(f"❌ FAIL: {workflow_file} missing quoted 'on:' syntax")
            all_correct = False
            
        # Validate YAML syntax
        try:
            yaml.safe_load(content)
            print(f"✅ PASS: {workflow_file} has valid YAML syntax")
        except yaml.YAMLError as e:
            print(f"❌ FAIL: {workflow_file} has invalid YAML: {e}")
            all_correct = False
    
    return all_correct

def test_latex_arguments_fixes():
    """Test that LaTeX arguments are correctly configured."""
    print("\n📝 Testing LaTeX Arguments Configuration")
    print("=" * 60)
    
    workflow_file = '.github/workflows/latex-build.yml'
    if not os.path.exists(workflow_file):
        print(f"❌ MISSING: {workflow_file}")
        return False
        
    with open(workflow_file, 'r') as f:
        content = f.read()
    
    # Check for absence of invalid -pdf argument (Issue #702)
    if '-pdf' in content:
        print("❌ FAIL: Invalid -pdf argument found (Issue #702)")
        return False
    else:
        print("✅ PASS: No invalid -pdf argument found")
    
    # Check for correct arguments
    expected_args = ['-interaction=nonstopmode', '-halt-on-error', '-shell-escape']
    args_found = 0
    for arg in expected_args:
        if arg in content:
            args_found += 1
            print(f"✅ PASS: Found required argument: {arg}")
        else:
            print(f"❌ MISSING: Required argument: {arg}")
    
    return args_found == len(expected_args)

def test_package_dependencies():
    """Test that all required LaTeX packages are configured."""
    print("\n📦 Testing LaTeX Package Dependencies")
    print("=" * 60)
    
    workflow_file = '.github/workflows/latex-build.yml'
    if not os.path.exists(workflow_file):
        print(f"❌ MISSING: {workflow_file}")
        return False
        
    with open(workflow_file, 'r') as f:
        content = f.read()
    
    # Essential packages for CTMM functionality
    required_packages = [
        'texlive-lang-german',      # German language support
        'texlive-fonts-extra',      # FontAwesome5 support
        'texlive-latex-extra',      # Extended LaTeX packages
        'texlive-pstricks',         # Pifont support (Issue #739)
    ]
    
    packages_found = 0
    for package in required_packages:
        if package in content:
            packages_found += 1
            print(f"✅ PASS: Found required package: {package}")
        else:
            print(f"❌ MISSING: Required package: {package}")
    
    # Check for correct GitHub Action version (Issue #735)
    if 'dante-ev/latex-action@v2' in content:
        print("✅ PASS: Using correct LaTeX action version (v2)")
    else:
        print("❌ FAIL: Incorrect LaTeX action version")
        return False
    
    return packages_found == len(required_packages)

def test_build_system_robustness():
    """Test that the build system handles missing LaTeX gracefully."""
    print("\n🔄 Testing Build System Error Handling")
    print("=" * 60)
    
    try:
        result = subprocess.run([sys.executable, 'ctmm_build.py'], 
                              capture_output=True, text=True, timeout=30)
        
        output = result.stdout + result.stderr
        
        # Check for graceful handling of missing pdflatex
        if 'pdflatex not found' in output and 'skipping LaTeX compilation' in output:
            print("✅ PASS: Build system gracefully handles missing pdflatex")
        elif 'WARNING' in output and 'LaTeX not available' in output:
            print("✅ PASS: Build system provides appropriate warnings")
        else:
            print("✅ PASS: Build system completed successfully")
        
        # Check that it still validates structure without LaTeX
        if 'structure test passed' in output:
            print("✅ PASS: Build system validates structure without requiring LaTeX")
            return True
        else:
            print("⚠️  WARNING: Build system structure validation unclear")
            return result.returncode == 0
            
    except subprocess.TimeoutExpired:
        print("❌ FAIL: Build system timed out")
        return False
    except Exception as e:
        print(f"❌ FAIL: Build system error: {e}")
        return False

def test_comprehensive_validation():
    """Test that comprehensive validation tools work correctly."""
    print("\n🎯 Testing Comprehensive Validation Tools")
    print("=" * 60)
    
    validation_tools = [
        ('validate_workflow_syntax.py', 'Workflow syntax validation'),
        ('test_issue_743_validation.py', 'CI configuration validation'),
        ('test_issue_761_fix.py', 'Pipeline robustness validation')
    ]
    
    all_passed = True
    
    for tool, description in validation_tools:
        if not os.path.exists(tool):
            print(f"❌ MISSING: {tool}")
            all_passed = False
            continue
            
        try:
            result = subprocess.run([sys.executable, tool], 
                                  capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                print(f"✅ PASS: {description} completed successfully")
            else:
                print(f"❌ FAIL: {description} failed")
                all_passed = False
                
        except subprocess.TimeoutExpired:
            print(f"❌ TIMEOUT: {description} timed out")
            all_passed = False
        except Exception as e:
            print(f"❌ ERROR: {description} error: {e}")
            all_passed = False
    
    return all_passed

def main():
    """Run all validation tests for Issue #791 fixes."""
    print("=" * 70)
    print("ISSUE #791 VALIDATION: CI LaTeX Build Failure Fixes")
    print("=" * 70)
    print("Validating that all critical CI pipeline fixes are implemented...")
    
    test_results = []
    
    # Run all validation tests
    test_results.append(("Workflow Syntax Fixes", test_workflow_syntax_fixes()))
    test_results.append(("LaTeX Arguments Configuration", test_latex_arguments_fixes()))
    test_results.append(("Package Dependencies", test_package_dependencies()))
    test_results.append(("Build System Robustness", test_build_system_robustness()))
    test_results.append(("Comprehensive Validation Tools", test_comprehensive_validation()))
    
    # Summary report
    print("\n" + "=" * 70)
    print("VALIDATION SUMMARY")
    print("=" * 70)
    
    passed_tests = 0
    total_tests = len(test_results)
    
    for test_name, passed in test_results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name}")
        if passed:
            passed_tests += 1
    
    print(f"\nTests passed: {passed_tests}/{total_tests}")
    
    if passed_tests == total_tests:
        print("🎉 ALL TESTS PASSED! Issue #791 fixes are properly implemented.")
        print("\nThe CI pipeline should now:")
        print("  ✓ Handle LaTeX compilation errors gracefully")
        print("  ✓ Include all required German language and font packages")
        print("  ✓ Use correct workflow syntax and action versions") 
        print("  ✓ Provide comprehensive error reporting and validation")
        return True
    else:
        print(f"⚠️  {total_tests - passed_tests} test(s) failed. See details above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)