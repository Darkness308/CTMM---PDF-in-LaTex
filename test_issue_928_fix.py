#!/usr/bin/env python3
"""
Issue #928 Fix Validation: Enhanced CI Pipeline Robustness
==========================================================

This script validates the fixes implemented for issue #928, which addresses
CI Insights Report showing build failures in the "Build LaTeX PDF" workflow.

Key improvements tested:
1. Enhanced CI environment validation
2. Retry mechanisms for LaTeX compilation
3. Comprehensive error diagnostics
4. Improved failure artifact collection
5. Resource monitoring and validation
"""

import os
import sys
import yaml
import subprocess
from pathlib import Path


def test_enhanced_ci_validation():
    """Test that enhanced CI validation script exists and works."""
    print("\n🚀 Testing Enhanced CI Validation")
    print("=" * 60)
    
    script_path = Path("test_ci_robustness.py")
    if not script_path.exists():
        print("❌ Enhanced CI validation script not found")
        return False
    
    # Test the script executes successfully
    try:
        result = subprocess.run([
            sys.executable, str(script_path)
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Enhanced CI validation script executes successfully")
            
            # Check for key validation components
            output = result.stdout
            required_checks = [
                "System Resources",
                "Python Environment", 
                "File Permissions",
                "LaTeX Environment",
                "Build System Robustness",
                "Network Connectivity"
            ]
            
            passed_checks = 0
            for check in required_checks:
                if check in output:
                    print(f"✅ Found validation: {check}")
                    passed_checks += 1
                else:
                    print(f"❌ Missing validation: {check}")
            
            if passed_checks == len(required_checks):
                print(f"✅ All {len(required_checks)} validation checks present")
                return True
            else:
                print(f"❌ Only {passed_checks}/{len(required_checks)} checks found")
                return False
        else:
            print(f"❌ Enhanced CI validation failed: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Enhanced CI validation timed out")
        return False
    except Exception as e:
        print(f"❌ Error running enhanced CI validation: {e}")
        return False


def test_workflow_retry_mechanisms():
    """Test that the workflow has retry mechanisms for LaTeX compilation."""
    print("\n🔄 Testing Workflow Retry Mechanisms")
    print("=" * 60)
    
    workflow_path = Path(".github/workflows/latex-build.yml")
    if not workflow_path.exists():
        print("❌ LaTeX build workflow not found")
        return False
    
    with open(workflow_path, 'r') as f:
        content = f.read()
    
    # Check for retry logic
    retry_indicators = [
        "MAX_ATTEMPTS",
        "retry",
        "ATTEMPT",
        "while [ $ATTEMPT",
        "sleep 10"
    ]
    
    found_retry_features = 0
    for indicator in retry_indicators:
        if indicator in content:
            print(f"✅ Found retry mechanism: {indicator}")
            found_retry_features += 1
    
    if found_retry_features >= 3:
        print(f"✅ Comprehensive retry mechanism implemented ({found_retry_features} features)")
        return True
    else:
        print(f"❌ Insufficient retry mechanisms ({found_retry_features} features)")
        return False


def test_enhanced_error_diagnostics():
    """Test that the workflow has enhanced error diagnostics."""
    print("\n🔍 Testing Enhanced Error Diagnostics")
    print("=" * 60)
    
    workflow_path = Path(".github/workflows/latex-build.yml")
    with open(workflow_path, 'r') as f:
        content = f.read()
    
    # Check for enhanced diagnostic features
    diagnostic_features = [
        "Enhanced LaTeX compilation with retry",
        "Verify PDF generation with enhanced diagnostics",
        "Generate failure summary",
        "PDF_SIZE",
        "PDF file format validation",
        "system resources",
        "LATEX LOG TAIL"
    ]
    
    found_diagnostics = 0
    for feature in diagnostic_features:
        if feature in content:
            print(f"✅ Found diagnostic feature: {feature}")
            found_diagnostics += 1
    
    if found_diagnostics >= 5:
        print(f"✅ Comprehensive diagnostics implemented ({found_diagnostics} features)")
        return True
    else:
        print(f"❌ Insufficient diagnostic features ({found_diagnostics} features)")
        return False


def test_artifact_collection_enhancements():
    """Test that artifact collection has been enhanced for debugging."""
    print("\n📦 Testing Artifact Collection Enhancements")
    print("=" * 60)
    
    workflow_path = Path(".github/workflows/latex-build.yml")
    with open(workflow_path, 'r') as f:
        content = f.read()
    
    # Check for enhanced artifact collection
    artifact_features = [
        "build_logs_and_diagnostics",
        "*.aux",
        "*.out",
        "*.toc",
        "*.synctex.gz",
        "retention-days",
        "main.pdf"
    ]
    
    found_features = 0
    for feature in artifact_features:
        if feature in content:
            print(f"✅ Found artifact feature: {feature}")
            found_features += 1
    
    if found_features >= 5:
        print(f"✅ Enhanced artifact collection implemented ({found_features} features)")
        return True
    else:
        print(f"❌ Insufficient artifact collection ({found_features} features)")
        return False


def test_ci_environment_robustness_step():
    """Test that CI environment robustness check is added to workflow."""
    print("\n🏗️  Testing CI Environment Robustness Step")
    print("=" * 60)
    
    workflow_path = Path(".github/workflows/latex-build.yml")
    with open(workflow_path, 'r') as f:
        workflow = yaml.safe_load(f)
    
    # Find the CI robustness check step
    build_job = workflow.get('jobs', {}).get('build', {})
    steps = build_job.get('steps', [])
    
    robustness_step = None
    for step in steps:
        if 'CI Environment Robustness Check' in step.get('name', ''):
            robustness_step = step
            break
    
    if robustness_step:
        print("✅ CI Environment Robustness Check step found")
        
        # Check the step configuration
        run_command = robustness_step.get('run', '')
        if 'test_ci_robustness.py' in run_command:
            print("✅ Robustness check script properly configured")
            return True
        else:
            print("❌ Robustness check script not found in step")
            return False
    else:
        print("❌ CI Environment Robustness Check step not found")
        return False


def test_workflow_yaml_validity():
    """Test that the enhanced workflow file is still valid YAML."""
    print("\n📝 Testing Workflow YAML Validity")
    print("=" * 60)
    
    workflow_path = Path(".github/workflows/latex-build.yml")
    
    try:
        with open(workflow_path, 'r') as f:
            workflow = yaml.safe_load(f)
        
        # Check basic workflow structure
        if 'name' in workflow and 'on' in workflow and 'jobs' in workflow:
            print("✅ Workflow YAML structure is valid")
            
            # Check jobs structure
            jobs = workflow.get('jobs', {})
            if 'build' in jobs:
                print("✅ Build job is present")
                
                build_job = jobs['build']
                if 'steps' in build_job:
                    step_count = len(build_job['steps'])
                    print(f"✅ Build job has {step_count} steps")
                    return True
                else:
                    print("❌ Build job missing steps")
                    return False
            else:
                print("❌ Build job not found")
                return False
        else:
            print("❌ Invalid workflow structure")
            return False
            
    except yaml.YAMLError as e:
        print(f"❌ YAML parsing error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error reading workflow: {e}")
        return False


def run_issue_928_validation():
    """Run all Issue #928 fix validation tests."""
    print("=" * 70)
    print("ISSUE #928 VALIDATION: Enhanced CI Pipeline Robustness")
    print("Addressing 'Build LaTeX PDF' workflow failures")
    print("=" * 70)
    
    tests = [
        ("Enhanced CI Validation", test_enhanced_ci_validation),
        ("Workflow Retry Mechanisms", test_workflow_retry_mechanisms),
        ("Enhanced Error Diagnostics", test_enhanced_error_diagnostics),
        ("Artifact Collection Enhancements", test_artifact_collection_enhancements),
        ("CI Environment Robustness Step", test_ci_environment_robustness_step),
        ("Workflow YAML Validity", test_workflow_yaml_validity)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                print(f"\n✅ PASS {test_name}")
                passed += 1
            else:
                print(f"\n❌ FAIL {test_name}")
        except Exception as e:
            print(f"\n❌ ERROR {test_name}: {e}")
    
    print("\n" + "=" * 70)
    print("VALIDATION SUMMARY")
    print("=" * 70)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Issue #928 fix implemented successfully.")
        print("\nEnhanced CI robustness features:")
        print("✓ Comprehensive CI environment validation")
        print("✓ Retry mechanisms for transient failures")
        print("✓ Enhanced error diagnostics and logging")
        print("✓ Improved artifact collection for debugging")
        print("✓ Resource monitoring and validation")
        return True
    else:
        print(f"⚠️  {total - passed} test(s) failed. Additional work needed.")
        return False


def main():
    """Main entry point."""
    try:
        success = run_issue_928_validation()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nValidation interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nUnexpected error during validation: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()