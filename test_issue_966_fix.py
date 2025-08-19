#!/usr/bin/env python3
"""
Test validation for Issue #966: GitHub Actions LaTeX Build CI improvements.

This test validates that the CI workflow configuration improvements are working
correctly and that the build system properly handles missing LaTeX installations.
"""

import subprocess
import sys
import yaml
from pathlib import Path


def test_yaml_syntax_and_linting():
    """Test that all core workflow files have proper YAML syntax and clean linting."""
    print("\n🔧 Testing YAML Syntax and Linting")
    print("=" * 60)
    
    core_workflows = [
        ".github/workflows/latex-build.yml",
        ".github/workflows/latex-validation.yml", 
        ".github/workflows/static.yml"
    ]
    
    all_pass = True
    
    for workflow_file in core_workflows:
        workflow_path = Path(workflow_file)
        
        # Test YAML syntax
        try:
            with open(workflow_path, 'r') as f:
                yaml_content = yaml.safe_load(f)
            print(f"✅ {workflow_file}: Valid YAML syntax")
        except yaml.YAMLError as e:
            print(f"❌ {workflow_file}: YAML syntax error - {e}")
            all_pass = False
            
        # Test "on" keyword is properly quoted
        with open(workflow_path, 'r') as f:
            content = f.read()
        
        if '"on":' in content:
            print(f"✅ {workflow_file}: Proper quoted 'on:' keyword")
        else:
            print(f"❌ {workflow_file}: Missing quoted 'on:' keyword")
            all_pass = False
    
    return all_pass


def test_latex_action_configuration():
    """Test that LaTeX action is properly configured with correct version and arguments."""
    print("\n📦 Testing LaTeX Action Configuration")
    print("=" * 60)
    
    workflow_path = Path(".github/workflows/latex-build.yml")
    with open(workflow_path, 'r') as f:
        content = f.read()
    
    # Test correct LaTeX action version
    if 'dante-ev/latex-action@v2' in content:
        print("✅ Using correct LaTeX action version (v2)")
    else:
        print("❌ LaTeX action version needs verification")
        return False
    
    # Test no invalid -pdf argument (issue from previous fixes)
    if '-pdf' in content:
        print("❌ Invalid -pdf argument detected")
        return False
    else:
        print("✅ No invalid -pdf argument found")
    
    # Test essential packages are included
    essential_packages = [
        'texlive-lang-german',
        'texlive-pstricks',
        'texlive-fonts-extra',
        'texlive-latex-extra',
        'texlive-science'
    ]
    
    for package in essential_packages:
        if package in content:
            print(f"✅ Essential package included: {package}")
        else:
            print(f"❌ Missing essential package: {package}")
            return False
    
    return True


def test_build_system_robustness():
    """Test that the build system handles missing LaTeX gracefully."""
    print("\n🔄 Testing Build System Robustness")
    print("=" * 60)
    
    try:
        result = subprocess.run([sys.executable, 'ctmm_build.py'], 
                              capture_output=True, text=True, timeout=30)
        
        output = result.stdout + result.stderr
        
        # Should gracefully handle missing pdflatex
        if 'pdflatex not found' in output and 'skipping LaTeX compilation' in output:
            print("✅ Build system gracefully handles missing pdflatex")
        elif 'WARNING' in output and 'LaTeX not available' in output:
            print("✅ Build system provides appropriate warnings")
        else:
            print("⚠️  Build system behavior unclear for missing LaTeX")
        
        # Should still validate structure
        if 'structure test passed' in output:
            print("✅ Build system validates structure without LaTeX")
        else:
            print("❌ Build system fails to validate structure")
            return False
            
        # Should exit successfully even without LaTeX
        if result.returncode == 0:
            print("✅ Build system exits successfully without LaTeX")
        else:
            print("❌ Build system fails without LaTeX")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Build system test failed: {e}")
        return False


def test_workflow_error_handling():
    """Test that workflows have proper error handling and artifact upload."""
    print("\n🛡️ Testing Workflow Error Handling")
    print("=" * 60)
    
    workflow_path = Path(".github/workflows/latex-build.yml")
    with open(workflow_path, 'r') as f:
        content = f.read()
    
    # Test for proper error handling
    if 'if: failure()' in content:
        print("✅ Workflow has failure condition handling")
    else:
        print("❌ Missing failure condition handling")
        return False
    
    # Test for artifact upload on failure
    if 'upload-artifact' in content and 'build_logs' in content:
        print("✅ Workflow uploads build logs on failure")
    else:
        print("❌ Missing build log upload on failure")
        return False
    
    # Test for comprehensive validation steps
    validation_steps = [
        'validate_latex_syntax.py',
        'ctmm_build.py',
        'test_issue_743_validation.py',
        'test_issue_761_fix.py'
    ]
    
    for step in validation_steps:
        if step in content:
            print(f"✅ Validation step included: {step}")
        else:
            print(f"⚠️  Validation step missing: {step}")
    
    return True


def main():
    """Run all tests for Issue #966 fix validation."""
    print("======================================================================")
    print("ISSUE #966 VALIDATION: GitHub Actions LaTeX Build CI Improvements")
    print("======================================================================")
    
    tests = [
        ("YAML Syntax and Linting", test_yaml_syntax_and_linting),
        ("LaTeX Action Configuration", test_latex_action_configuration),
        ("Build System Robustness", test_build_system_robustness),
        ("Workflow Error Handling", test_workflow_error_handling)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🎯 Testing {test_name}")
        print("=" * 60)
        
        try:
            if test_func():
                print(f"✅ PASS: {test_name}")
                passed += 1
            else:
                print(f"❌ FAIL: {test_name}")
        except Exception as e:
            print(f"❌ ERROR in {test_name}: {e}")
    
    print("\n" + "=" * 70)
    print("VALIDATION SUMMARY")
    print("=" * 70)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Issue #966 fixes validated successfully.")
        return True
    else:
        print(f"❌ {total - passed} test(s) failed. Please review the issues above.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)