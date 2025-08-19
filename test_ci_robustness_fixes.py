#!/usr/bin/env python3
"""
Test script to validate CI robustness improvements implemented for issue #1048.
This script validates the enhanced error handling, timeout mechanisms, and retry logic.
"""

import yaml
import sys
from pathlib import Path
import subprocess
import time


def test_workflow_timeout_configuration():
    """Test that workflow steps have appropriate timeout configurations."""
    print("\n🕐 Testing Workflow Timeout Configuration")
    print("=" * 60)
    
    workflow_path = Path(".github/workflows/latex-build.yml")
    with open(workflow_path, 'r') as f:
        workflow = yaml.safe_load(f)
    
    build_job = workflow.get('jobs', {}).get('build', {})
    steps = build_job.get('steps', [])
    
    timeout_steps = []
    for step in steps:
        step_name = step.get('name', '')
        if 'timeout-minutes' in step:
            timeout_value = step['timeout-minutes']
            timeout_steps.append((step_name, timeout_value))
            print(f"✅ {step_name}: {timeout_value} minutes timeout")
    
    if len(timeout_steps) >= 3:
        print(f"✅ Found {len(timeout_steps)} steps with timeout configuration")
        return True
    else:
        print(f"❌ Only {len(timeout_steps)} steps have timeout configuration")
        return False


def test_retry_mechanism():
    """Test that retry mechanisms are properly configured."""
    print("\n🔄 Testing Retry Mechanism Configuration")
    print("=" * 60)
    
    workflow_path = Path(".github/workflows/latex-build.yml")
    with open(workflow_path, 'r') as f:
        content = f.read()
    
    # Check for retry step
    if 'LaTeX compilation retry' in content:
        print("✅ LaTeX compilation retry step found")
    else:
        print("❌ LaTeX compilation retry step missing")
        return False
    
    # Check for failure condition
    if 'if: failure()' in content:
        print("✅ Retry mechanism triggered on failure")
    else:
        print("❌ Retry mechanism not properly configured")
        return False
    
    # Check for cleanup in retry
    if 'rm -f main.pdf' in content:
        print("✅ Cleanup mechanism in retry found")
    else:
        print("❌ Cleanup mechanism missing")
        return False
    
    return True


def test_enhanced_error_logging():
    """Test that enhanced error logging is configured."""
    print("\n📋 Testing Enhanced Error Logging")
    print("=" * 60)
    
    workflow_path = Path(".github/workflows/latex-build.yml")
    with open(workflow_path, 'r') as f:
        content = f.read()
    
    error_logging_features = []
    
    # Check for comprehensive log upload
    if 'build_logs_${{ github.run_id }}' in content:
        error_logging_features.append("Unique build log naming")
        print("✅ Unique build log naming with run ID")
    
    # Check for failure summary
    if 'Generate failure summary' in content:
        error_logging_features.append("Failure summary generation")
        print("✅ Failure summary generation step found")
    
    # Check for comprehensive artifact paths
    if '*.aux' in content and '*.fls' in content:
        error_logging_features.append("Comprehensive artifact collection")
        print("✅ Comprehensive artifact collection configured")
    
    # Check for system information collection
    if 'SYSTEM INFORMATION' in content:
        error_logging_features.append("System information collection")
        print("✅ System information collection in failure summary")
    
    print(f"✅ Error logging features: {len(error_logging_features)}/4")
    return len(error_logging_features) >= 3


def test_system_preparation_steps():
    """Test that system preparation steps are configured."""
    print("\n🔧 Testing System Preparation Steps")
    print("=" * 60)
    
    workflow_path = Path(".github/workflows/latex-build.yml")
    with open(workflow_path, 'r') as f:
        content = f.read()
    
    preparation_features = []
    
    # Check for disk space monitoring
    if 'df -h' in content:
        preparation_features.append("Disk space monitoring")
        print("✅ Disk space monitoring configured")
    
    # Check for memory monitoring
    if 'free -h' in content:
        preparation_features.append("Memory monitoring")
        print("✅ Memory monitoring configured")
    
    # Check for file cleanup
    if 'rm -f main.pdf main.aux' in content:
        preparation_features.append("Artifact cleanup")
        print("✅ Build artifact cleanup configured")
    
    # Check for permission setting
    if 'chmod 644' in content:
        preparation_features.append("Permission management")
        print("✅ File permission management configured")
    
    print(f"✅ System preparation features: {len(preparation_features)}/4")
    return len(preparation_features) >= 3


def test_pdf_validation_robustness():
    """Test that PDF validation is robust."""
    print("\n📄 Testing PDF Validation Robustness")
    print("=" * 60)
    
    workflow_path = Path(".github/workflows/latex-build.yml")
    with open(workflow_path, 'r') as f:
        content = f.read()
    
    validation_features = []
    
    # Check for file size validation
    if 'stat -c%s' in content:
        validation_features.append("File size validation")
        print("✅ PDF file size validation configured")
    
    # Check for minimum size threshold
    if '1024' in content:
        validation_features.append("Minimum size threshold")
        print("✅ Minimum PDF size threshold configured")
    
    # Check for file type validation
    if 'file main.pdf' in content:
        validation_features.append("File type validation")
        print("✅ PDF file type validation configured")
    
    # Check for file system sync wait
    if 'sleep 2' in content:
        validation_features.append("File system sync wait")
        print("✅ File system sync wait configured")
    
    print(f"✅ PDF validation features: {len(validation_features)}/4")
    return len(validation_features) >= 3


def test_workflow_syntax_validity():
    """Test that the enhanced workflow has valid YAML syntax."""
    print("\n📝 Testing Enhanced Workflow YAML Syntax")
    print("=" * 60)
    
    workflow_path = Path(".github/workflows/latex-build.yml")
    
    try:
        with open(workflow_path, 'r') as f:
            workflow = yaml.safe_load(f)
        print("✅ YAML syntax is valid")
        
        # Validate structure
        if 'jobs' in workflow and 'build' in workflow['jobs']:
            print("✅ Workflow structure is valid")
            
            build_job = workflow['jobs']['build']
            if 'steps' in build_job and len(build_job['steps']) > 10:
                print(f"✅ Build job has {len(build_job['steps'])} steps")
                return True
            else:
                print("❌ Build job missing steps or insufficient steps")
                return False
        else:
            print("❌ Invalid workflow structure")
            return False
            
    except yaml.YAMLError as e:
        print(f"❌ YAML syntax error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error reading workflow: {e}")
        return False


def main():
    """Run all CI robustness tests."""
    print("=" * 70)
    print("CI ROBUSTNESS VALIDATION - Issue #1048 Fixes")
    print("Enhanced Error Handling, Timeouts, and Retry Mechanisms")
    print("=" * 70)
    
    tests = [
        ("Workflow Timeout Configuration", test_workflow_timeout_configuration),
        ("Retry Mechanism", test_retry_mechanism),
        ("Enhanced Error Logging", test_enhanced_error_logging),
        ("System Preparation Steps", test_system_preparation_steps),
        ("PDF Validation Robustness", test_pdf_validation_robustness),
        ("Workflow YAML Syntax", test_workflow_syntax_validity),
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed_tests += 1
                print(f"✅ PASS: {test_name}")
            else:
                print(f"❌ FAIL: {test_name}")
        except Exception as e:
            print(f"❌ ERROR in {test_name}: {e}")
    
    print("\n" + "=" * 70)
    print("CI ROBUSTNESS VALIDATION SUMMARY")
    print("=" * 70)
    print(f"Tests passed: {passed_tests}/{total_tests}")
    
    if passed_tests == total_tests:
        print("🎉 ALL TESTS PASSED! CI robustness improvements validated.")
        print("\nThe enhanced CI configuration provides:")
        print("✓ Comprehensive timeout protection")
        print("✓ Automatic retry mechanisms with cleanup")
        print("✓ Enhanced error logging and diagnostics")
        print("✓ System preparation and monitoring")
        print("✓ Robust PDF validation with size checks")
        print("✓ Valid and well-structured workflow configuration")
        return True
    else:
        print(f"❌ {total_tests - passed_tests} test(s) failed.")
        print("CI robustness improvements need attention.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)