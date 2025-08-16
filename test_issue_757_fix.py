#!/usr/bin/env python3
"""
Test validation for Issue #757 - Comprehensive CI LaTeX Build System Fixes
Validates that all critical CI issues have been resolved.
"""

import os
import yaml
import subprocess
import sys

def test_comprehensive_ci_fixes():
    """Test that all comprehensive CI fixes are working correctly."""
    
    print("=" * 60)
    print("Issue #757 Comprehensive CI Fix Validation")
    print("=" * 60)
    print("Testing all critical CI LaTeX build fixes...\n")
    
    tests_passed = 0
    total_tests = 6
    
    # Test 1: GitHub Actions Version Pinning
    print("1. Testing GitHub Actions version pinning...")
    try:
        with open('.github/workflows/latex-build.yml', 'r') as f:
            workflow_content = f.read()
        
        if 'dante-ev/latex-action@v2' in workflow_content:
            print("✅ PASS: GitHub Actions using correct version v2")
            tests_passed += 1
        else:
            print("❌ FAIL: GitHub Actions version not correctly pinned")
    except Exception as e:
        print(f"❌ FAIL: Error reading workflow file: {e}")
    
    # Test 2: LaTeX Package Dependencies 
    print("\n2. Testing LaTeX package dependencies...")
    try:
        with open('.github/workflows/latex-build.yml', 'r') as f:
            workflow_content = f.read()
        
        required_packages = [
            'texlive-lang-german',
            'texlive-fonts-recommended', 
            'texlive-latex-recommended',
            'texlive-latex-extra',
            'texlive-pstricks'  # Critical for pifont
        ]
        
        all_packages_found = all(pkg in workflow_content for pkg in required_packages)
        
        if all_packages_found:
            print("✅ PASS: All required LaTeX packages included")
            tests_passed += 1
        else:
            missing = [pkg for pkg in required_packages if pkg not in workflow_content]
            print(f"❌ FAIL: Missing packages: {missing}")
    except Exception as e:
        print(f"❌ FAIL: Error checking packages: {e}")
    
    # Test 3: YAML Syntax (quoted 'on:' keywords)
    print("\n3. Testing YAML syntax fixes...")
    workflow_files = [
        '.github/workflows/latex-build.yml',
        '.github/workflows/latex-validation.yml',
        '.github/workflows/static.yml'
    ]
    
    yaml_syntax_ok = True
    for workflow_file in workflow_files:
        try:
            with open(workflow_file, 'r') as f:
                content = f.read()
            
            # Check for quoted 'on:' syntax
            if '"on":' not in content:
                print(f"❌ FAIL: {workflow_file} missing quoted 'on:' syntax")
                yaml_syntax_ok = False
            
            # Validate YAML parsing
            yaml.safe_load(content)
            
        except Exception as e:
            print(f"❌ FAIL: YAML syntax error in {workflow_file}: {e}")
            yaml_syntax_ok = False
    
    if yaml_syntax_ok:
        print("✅ PASS: All workflow files have correct YAML syntax")
        tests_passed += 1
    
    # Test 4: Build System Error Handling
    print("\n4. Testing build system robustness...")
    try:
        result = subprocess.run(['python3', 'ctmm_build.py'], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0 and "CTMM BUILD SYSTEM SUMMARY" in result.stdout:
            print("✅ PASS: Build system executes successfully with error handling")
            tests_passed += 1
        else:
            print(f"❌ FAIL: Build system failed: {result.stderr}")
    except Exception as e:
        print(f"❌ FAIL: Error testing build system: {e}")
    
    # Test 5: Validation Infrastructure  
    print("\n5. Testing validation infrastructure...")
    validation_files = [
        'test_issue_743_validation.py',
        'validate_latex_syntax.py',
        'validate_workflow_versions.py'
    ]
    
    validation_ok = True
    for val_file in validation_files:
        if not os.path.exists(val_file):
            print(f"❌ FAIL: Missing validation file: {val_file}")
            validation_ok = False
    
    if validation_ok:
        print("✅ PASS: All validation infrastructure files present")
        tests_passed += 1
    
    # Test 6: Unit Test Coverage
    print("\n6. Testing unit test coverage...")
    try:
        result = subprocess.run(['python3', 'test_ctmm_build.py'], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0 and "OK" in result.stderr:
            # Count tests run
            if "Ran" in result.stderr:
                print("✅ PASS: Unit tests execute successfully") 
                tests_passed += 1
            else:
                print("❌ FAIL: Unit test output unclear")
        else:
            print(f"❌ FAIL: Unit tests failed: {result.stderr}")
    except Exception as e:
        print(f"❌ FAIL: Error running unit tests: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Tests passed: {tests_passed}/{total_tests}")
    
    if tests_passed == total_tests:
        print("\n🎉 ALL TESTS PASSED - Issue #757 fix is working correctly!")
        print("\nThe comprehensive CI LaTeX build system fixes are validated:")
        print("  ✓ GitHub Actions version pinning resolved")
        print("  ✓ LaTeX package dependencies complete")  
        print("  ✓ YAML syntax issues fixed")
        print("  ✓ Build system robustness enhanced")
        print("  ✓ Validation infrastructure in place")
        print("  ✓ Unit test coverage maintained")
        print("\nThe CI pipeline is ready for reliable PDF generation!")
        return True
    else:
        print(f"\n⚠️  {total_tests - tests_passed} test(s) failed")
        print("Some aspects of the comprehensive fix need attention.")
        return False

if __name__ == "__main__":
    success = test_comprehensive_ci_fixes()
    sys.exit(0 if success else 1)