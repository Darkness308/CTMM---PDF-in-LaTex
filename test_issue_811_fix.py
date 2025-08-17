#!/usr/bin/env python3
"""
Test Issue #811 Fix: CI Build Failure Prevention

This test validates that the CI configuration is robust against the type of build failures
reported in Mergify CI Insights. It ensures:
1. All workflow steps are correctly ordered and validated
2. Enhanced robustness checks are in place
3. LaTeX action version is correct and stable
4. Comprehensive validation runs before expensive operations
"""

import os
import sys
import yaml
import subprocess
from pathlib import Path


def test_ci_build_failure_prevention():
    """Test that CI configuration prevents the type of build failures reported in issue #811."""
    print("\n🎯 Testing CI Build Failure Prevention (Issue #811)")
    print("=" * 60)
    
    workflow_path = Path(".github/workflows/latex-build.yml")
    
    if not workflow_path.exists():
        print("❌ ERROR: LaTeX build workflow not found")
        return False
        
    try:
        with open(workflow_path, 'r') as f:
            workflow = yaml.safe_load(f)
    except Exception as e:
        print(f"❌ ERROR: Failed to parse workflow YAML: {e}")
        return False
    
    # Test 1: Validate workflow structure integrity
    print("\n📋 Testing workflow structure integrity...")
    jobs = workflow.get('jobs', {})
    build_job = jobs.get('build', {})
    steps = build_job.get('steps', [])
    
    if len(steps) < 8:
        print(f"❌ ERROR: Expected at least 8 steps, found {len(steps)}")
        return False
    
    step_names = [step.get('name', 'Unknown') for step in steps]
    print(f"✅ Found {len(steps)} workflow steps")
    
    # Test 2: Validate critical validation steps are present
    print("\n🔍 Testing critical validation steps...")
    required_validation_steps = [
        'Run LaTeX syntax validation',
        'Run CTMM Build System Check', 
        'Run comprehensive CI validation',
        'Enhanced pre-build validation'
    ]
    
    missing_validations = []
    for required_step in required_validation_steps:
        if not any(required_step in step_name for step_name in step_names):
            missing_validations.append(required_step)
    
    if missing_validations:
        print(f"❌ ERROR: Missing validation steps: {missing_validations}")
        return False
    
    print("✅ All critical validation steps present")
    
    # Test 3: Validate LaTeX action version is stable
    print("\n🔧 Testing LaTeX action version stability...")
    latex_step = None
    for step in steps:
        if step.get('name') == 'Set up LaTeX':
            latex_step = step
            break
    
    if not latex_step:
        print("❌ ERROR: LaTeX setup step not found")
        return False
    
    latex_action = latex_step.get('uses', '')
    if 'dante-ev/latex-action@v2' not in latex_action:
        print(f"❌ ERROR: Unexpected LaTeX action version: {latex_action}")
        return False
    
    # Specifically check that it's NOT using the problematic v2.0.0
    if 'v2.0.0' in latex_action:
        print(f"❌ ERROR: Using problematic v2.0.0 version (see issue #735)")
        return False
    
    print(f"✅ Using stable LaTeX action version: {latex_action}")
    
    # Test 4: Validate validation steps run before LaTeX
    print("\n⚡ Testing validation-before-compilation ordering...")
    latex_step_index = None
    validation_indices = []
    
    for i, step_name in enumerate(step_names):
        if 'Set up LaTeX' in step_name:
            latex_step_index = i
        if any(keyword in step_name.lower() for keyword in ['validation', 'check', 'validate']):
            validation_indices.append(i)
    
    if latex_step_index is None:
        print("❌ ERROR: LaTeX setup step not found")
        return False
    
    early_validations = [i for i in validation_indices if i < latex_step_index]
    if len(early_validations) < 4:
        print(f"❌ ERROR: Only {len(early_validations)} validation steps before LaTeX")
        return False
    
    print(f"✅ {len(early_validations)} validation steps run before LaTeX compilation")
    
    # Test 5: Validate error handling and artifact collection
    print("\n📦 Testing error handling and artifact collection...")
    artifact_steps = [step for step in steps if 'upload' in step.get('name', '').lower()]
    
    if len(artifact_steps) < 2:
        print("❌ ERROR: Insufficient artifact collection steps")
        return False
    
    # Check for failure-specific artifact collection
    failure_upload = any('failure' in step.get('if', '') for step in artifact_steps)
    if not failure_upload:
        print("❌ ERROR: No failure-specific artifact upload found")
        return False
    
    print("✅ Error handling and artifact collection properly configured")
    
    return True


def test_enhanced_robustness_integration():
    """Test that enhanced robustness features from issue #761 are properly integrated."""
    print("\n🛡️  Testing Enhanced Robustness Integration")
    print("=" * 60)
    
    # Test that robustness test itself is working
    print("🧪 Testing robustness validation script...")
    try:
        result = subprocess.run([sys.executable, 'test_issue_761_fix.py'], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            print(f"❌ ERROR: Robustness test failed: {result.stderr[:200]}")
            return False
        
        if "ALL TESTS PASSED" not in result.stdout:
            print(f"❌ ERROR: Robustness validation incomplete")
            return False
            
        print("✅ Enhanced robustness validation working correctly")
        
    except subprocess.TimeoutExpired:
        print("❌ ERROR: Robustness test timed out")
        return False
    except Exception as e:
        print(f"❌ ERROR: Failed to run robustness test: {e}")
        return False
    
    return True


def test_comprehensive_validation_chain():
    """Test that the comprehensive validation chain prevents CI failures."""
    print("\n🔗 Testing Comprehensive Validation Chain")
    print("=" * 60)
    
    validation_scripts = [
        'validate_latex_syntax.py',
        'ctmm_build.py',
        'test_issue_743_validation.py',
        'test_issue_761_fix.py'
    ]
    
    print("🧪 Testing all validation scripts execute successfully...")
    
    for script in validation_scripts:
        if not Path(script).exists():
            print(f"❌ ERROR: Missing validation script: {script}")
            return False
        
        try:
            result = subprocess.run([sys.executable, script], 
                                  capture_output=True, text=True, timeout=60)
            if result.returncode != 0:
                print(f"❌ ERROR: {script} failed with exit code {result.returncode}")
                print(f"   stderr: {result.stderr[:150]}...")
                return False
            
            print(f"✅ {script} executes successfully")
            
        except subprocess.TimeoutExpired:
            print(f"❌ ERROR: {script} timed out")
            return False
        except Exception as e:
            print(f"❌ ERROR: Failed to run {script}: {e}")
            return False
    
    print("✅ All validation scripts in chain working correctly")
    return True


def main():
    """Run all tests for issue #811 fix validation."""
    print("======================================================================")
    print("ISSUE #811 VALIDATION: CI Build Failure Prevention")
    print("======================================================================")
    
    tests = [
        test_ci_build_failure_prevention,
        test_enhanced_robustness_integration,
        test_comprehensive_validation_chain
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                print(f"\n❌ {test.__name__} FAILED")
        except Exception as e:
            print(f"\n❌ {test.__name__} ERROR: {e}")
    
    print("\n" + "=" * 70)
    print("VALIDATION SUMMARY")
    print("=" * 70)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! CI build failure prevention validated.")
        print("\nThe enhanced CI configuration provides:")
        print("✓ Comprehensive pre-build validation")
        print("✓ Stable LaTeX action version")
        print("✓ Proper error handling and artifact collection")
        print("✓ Robust validation chain")
        print("✓ Protection against known failure modes")
        return True
    else:
        print(f"❌ {total - passed} test(s) failed. CI configuration needs attention.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)