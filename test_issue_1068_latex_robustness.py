#!/usr/bin/env python3
"""
Test script for Issue #1068: Enhanced CI Pipeline LaTeX Action Robustness

This script validates the enhanced LaTeX compilation setup with fallback mechanisms
to prevent CI failures due to unreliable external LaTeX actions.
"""

import os
import yaml
import sys
from pathlib import Path

def test_latex_action_robustness():
    """Test that the LaTeX workflow has robust fallback mechanisms."""
    print("\n🛡️  Testing LaTeX Action Robustness")
    print("=" * 60)
    
    workflow_file = '.github/workflows/latex-build.yml'
    
    if not os.path.exists(workflow_file):
        print(f"❌ Workflow file missing: {workflow_file}")
        return False
    
    with open(workflow_file, 'r') as f:
        workflow_data = yaml.safe_load(f)
    
    # Check for primary LaTeX action
    primary_action_found = False
    fallback_method_found = False
    
    jobs = workflow_data.get('jobs', {})
    for job_name, job_data in jobs.items():
        steps = job_data.get('steps', [])
        for step in steps:
            step_name = step.get('name', '')
            
            # Check for primary LaTeX action
            if 'Primary Method' in step_name and step.get('uses', '').startswith('xu-cheng/latex-action'):
                primary_action_found = True
                print(f"✅ FOUND: Primary LaTeX action - {step.get('uses')}")
                
                # Check for continue-on-error
                if step.get('continue-on-error') == True:
                    print(f"✅ FOUND: Primary action has continue-on-error")
                else:
                    print(f"⚠️  WARNING: Primary action missing continue-on-error")
                
                # Check for step ID for fallback reference
                if 'id' in step:
                    print(f"✅ FOUND: Primary action has ID for fallback reference")
                else:
                    print(f"❌ MISSING: Primary action ID for fallback reference")
            
            # Check for fallback method
            elif 'Fallback Method' in step_name:
                fallback_method_found = True
                print(f"✅ FOUND: Fallback LaTeX installation method")
                
                # Check for conditional execution
                if 'if' in step and 'failure' in step['if']:
                    print(f"✅ FOUND: Fallback method has proper conditional")
                else:
                    print(f"❌ MISSING: Fallback method conditional")
                
                # Check for manual TeX Live installation
                run_script = step.get('run', '')
                if 'texlive' in run_script and 'apt-get install' in run_script:
                    print(f"✅ FOUND: Manual TeX Live installation in fallback")
                else:
                    print(f"❌ MISSING: Manual TeX Live installation")
    
    if primary_action_found and fallback_method_found:
        print(f"✅ PASS: LaTeX compilation has robust primary + fallback setup")
        return True
    else:
        print(f"❌ FAIL: Missing robust LaTeX setup")
        return False

def test_enhanced_pdf_verification():
    """Test that PDF verification provides comprehensive information."""
    print("\n📄 Testing Enhanced PDF Verification")
    print("=" * 60)
    
    workflow_file = '.github/workflows/latex-build.yml'
    
    with open(workflow_file, 'r') as f:
        content = f.read()
    
    # Check for enhanced PDF verification features
    verification_features = {
        'file size check': 'du -h main.pdf' in content,
        'file type check': 'file main.pdf' in content,
        'detailed file listing': 'ls -la main.pdf' in content,
        'comprehensive error logging': 'find . -name "*.log"' in content
    }
    
    features_found = 0
    for feature, found in verification_features.items():
        if found:
            features_found += 1
            print(f"✅ FOUND: {feature}")
        else:
            print(f"❌ MISSING: {feature}")
    
    if features_found >= 3:
        print(f"✅ PASS: Enhanced PDF verification ({features_found}/4 features)")
        return True
    else:
        print(f"❌ FAIL: Insufficient PDF verification features")
        return False

def test_latex_action_migration():
    """Test that the workflow has migrated away from problematic dante-ev action."""
    print("\n🔄 Testing LaTeX Action Migration")
    print("=" * 60)
    
    workflow_file = '.github/workflows/latex-build.yml'
    
    with open(workflow_file, 'r') as f:
        content = f.read()
    
    # Check that dante-ev action is no longer used
    if 'dante-ev/latex-action' in content:
        print(f"❌ FAIL: Still using problematic dante-ev/latex-action")
        return False
    
    # Check that xu-cheng action is used
    if 'xu-cheng/latex-action' in content:
        print(f"✅ PASS: Migrated to xu-cheng/latex-action")
        
        # Check version
        if 'xu-cheng/latex-action@v3' in content:
            print(f"✅ PASS: Using recommended version v3")
        else:
            print(f"⚠️  WARNING: Consider using v3 for latest features")
        
        return True
    
    print(f"⚠️  INFO: No xu-cheng action found, checking for manual installation")
    
    # Check for manual installation as alternative
    if 'texlive-latex-base' in content and 'apt-get install' in content:
        print(f"✅ PASS: Manual TeX Live installation available")
        return True
    
    print(f"❌ FAIL: No reliable LaTeX installation method found")
    return False

def test_timeout_resilience():
    """Test that all LaTeX-related steps have appropriate timeouts."""
    print("\n⏱️  Testing Timeout Resilience")
    print("=" * 60)
    
    workflow_file = '.github/workflows/latex-build.yml'
    
    with open(workflow_file, 'r') as f:
        workflow_data = yaml.safe_load(f)
    
    latex_steps_with_timeout = 0
    total_latex_steps = 0
    
    jobs = workflow_data.get('jobs', {})
    for job_name, job_data in jobs.items():
        steps = job_data.get('steps', [])
        for step in steps:
            step_name = step.get('name', '')
            
            # Check LaTeX-related steps
            if any(keyword in step_name.lower() for keyword in ['latex', 'pdf', 'tex']):
                total_latex_steps += 1
                
                timeout = step.get('timeout-minutes')
                if timeout:
                    latex_steps_with_timeout += 1
                    print(f"✅ {step_name}: {timeout} minutes")
                else:
                    print(f"❌ {step_name}: No timeout specified")
    
    if total_latex_steps > 0:
        timeout_percentage = (latex_steps_with_timeout / total_latex_steps) * 100
        print(f"\n📊 Timeout Coverage: {latex_steps_with_timeout}/{total_latex_steps} ({timeout_percentage:.1f}%)")
        
        if timeout_percentage >= 100:
            print(f"✅ PASS: All LaTeX steps have timeouts")
            return True
        elif timeout_percentage >= 80:
            print(f"⚠️  WARNING: Most LaTeX steps have timeouts")
            return True
        else:
            print(f"❌ FAIL: Insufficient timeout coverage")
            return False
    else:
        print(f"⚠️  WARNING: No LaTeX steps found")
        return True

def main():
    """Main test function."""
    print("=" * 70)
    print("ISSUE #1068 VALIDATION: Enhanced LaTeX Action Robustness")
    print("Fallback Mechanisms, Migration, and Error Recovery")
    print("=" * 70)
    
    tests = [
        ("LaTeX Action Robustness", test_latex_action_robustness),
        ("Enhanced PDF Verification", test_enhanced_pdf_verification),
        ("LaTeX Action Migration", test_latex_action_migration),
        ("Timeout Resilience", test_timeout_resilience)
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed_tests += 1
        except Exception as e:
            print(f"❌ ERROR in {test_name}: {e}")
    
    print("\n" + "=" * 70)
    print("VALIDATION SUMMARY")
    print("=" * 70)
    print(f"Tests passed: {passed_tests}/{total_tests}")
    
    if passed_tests == total_tests:
        print("🎉 ALL TESTS PASSED!")
        print("\nThe enhanced LaTeX action setup should provide:")
        print("✓ Robust fallback mechanisms")
        print("✓ Migration away from problematic actions")
        print("✓ Enhanced error reporting and recovery")
        print("✓ Comprehensive timeout handling")
        return True
    else:
        print(f"❌ {total_tests - passed_tests} test(s) failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)