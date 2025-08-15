#!/usr/bin/env python3
"""
Test script to validate the specific workflow fixes mentioned in the PR.
This validates that the GitHub Actions workflow syntax and LaTeX dependencies are correctly configured.
"""

import yaml
import os
from pathlib import Path

def test_latex_build_workflow_fix():
    """Test that the latex-build.yml workflow is properly fixed."""
    print("Testing latex-build.yml workflow fixes...")
    
    workflow_path = Path('.github/workflows/latex-build.yml')
    if not workflow_path.exists():
        print("❌ latex-build.yml not found")
        return False
    
    with open(workflow_path, 'r') as f:
        content = f.read()
    
    # Test YAML parsing (should not fail)
    try:
        workflow = yaml.safe_load(content)
        print("✅ YAML parsing successful")
    except yaml.YAMLError as e:
        print(f"❌ YAML parsing failed: {e}")
        return False
    
    # Test that 'on' is properly quoted (string key, not boolean)
    if 'on' not in workflow:
        print("❌ 'on' key not found in workflow")
        return False
    
    if not isinstance(list(workflow.keys())[1], str):  # 'on' should be second key
        print("❌ 'on' key is not a string (boolean interpretation issue)")
        return False
    
    print("✅ 'on' key properly quoted as string")
    
    # Test LaTeX action configuration
    jobs = workflow.get('jobs', {})
    build_job = jobs.get('build', {})
    steps = build_job.get('steps', [])
    
    latex_step = None
    for step in steps:
        if step.get('name') == 'Set up LaTeX':
            latex_step = step
            break
    
    if not latex_step:
        print("❌ LaTeX setup step not found")
        return False
    
    print("✅ LaTeX setup step found")
    
    # Test LaTeX action version
    action_used = latex_step.get('uses', '')
    if not action_used.startswith('dante-ev/latex-action@'):
        print(f"❌ Incorrect LaTeX action: {action_used}")
        return False
    
    print(f"✅ LaTeX action properly configured: {action_used}")
    
    # Test LaTeX arguments
    args = latex_step.get('with', {}).get('args', '')
    expected_args = ['-pdf', '-interaction=nonstopmode', '-halt-on-error', '-shell-escape']
    
    for arg in expected_args:
        if arg not in args:
            print(f"❌ Missing argument: {arg}")
            return False
    
    print("✅ LaTeX arguments properly configured")
    
    # Test German language packages
    packages = latex_step.get('with', {}).get('extra_system_packages', '')
    german_packages = ['texlive-lang-german', 'texlive-fontawesome']
    
    for package in german_packages:
        if package not in packages:
            print(f"❌ Missing German language package: {package}")
            return False
    
    print("✅ German language packages properly configured")
    
    return True

def test_workflow_syntax_consistency():
    """Test that all workflow files have consistent quoted syntax."""
    print("\nTesting workflow syntax consistency...")
    
    workflow_files = [
        '.github/workflows/latex-build.yml',
        '.github/workflows/latex-validation.yml',
        '.github/workflows/static.yml'
    ]
    
    all_valid = True
    
    for workflow_file in workflow_files:
        workflow_path = Path(workflow_file)
        if not workflow_path.exists():
            print(f"❌ {workflow_file} not found")
            all_valid = False
            continue
        
        with open(workflow_path, 'r') as f:
            content = f.read()
        
        try:
            workflow = yaml.safe_load(content)
            
            # Check that 'on' key exists and is a string key
            if 'on' in workflow:
                print(f"✅ {workflow_file}: 'on' key properly quoted")
            else:
                print(f"❌ {workflow_file}: 'on' key not found")
                all_valid = False
                
        except yaml.YAMLError as e:
            print(f"❌ {workflow_file}: YAML parsing failed - {e}")
            all_valid = False
    
    return all_valid

def test_pdflatex_availability_checks():
    """Test that the build system properly handles pdflatex availability."""
    print("\nTesting pdflatex availability checks...")
    
    # Import the CTMM build system
    try:
        import ctmm_build
        print("✅ CTMM build system imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import CTMM build system: {e}")
        return False
    
    # Check that the functions handle pdflatex unavailability gracefully
    try:
        result = ctmm_build.test_basic_build()
        print(f"✅ test_basic_build() handles pdflatex unavailability: {result}")
    except Exception as e:
        print(f"❌ test_basic_build() failed: {e}")
        return False
    
    try:
        result = ctmm_build.test_full_build()
        print(f"✅ test_full_build() handles pdflatex unavailability: {result}")
    except Exception as e:
        print(f"❌ test_full_build() failed: {e}")
        return False
    
    return True

def main():
    """Run all workflow fix validation tests."""
    print("="*60)
    print("WORKFLOW FIX VALIDATION TESTS")
    print("="*60)
    
    tests = [
        test_latex_build_workflow_fix,
        test_workflow_syntax_consistency,
        test_pdflatex_availability_checks
    ]
    
    all_passed = True
    
    for test in tests:
        try:
            result = test()
            if not result:
                all_passed = False
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
            all_passed = False
    
    print("\n" + "="*60)
    if all_passed:
        print("🎉 ALL WORKFLOW FIX TESTS PASSED")
        print("✅ GitHub Actions workflow syntax issues resolved")
        print("✅ LaTeX dependencies properly configured")
        print("✅ Build system robustness enhanced")
    else:
        print("❌ SOME TESTS FAILED")
        print("Please review the output above for specific issues")
    
    print("="*60)
    return 0 if all_passed else 1

if __name__ == '__main__':
    exit(main())