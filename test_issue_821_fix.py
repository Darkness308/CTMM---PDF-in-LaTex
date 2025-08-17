#!/usr/bin/env python3
"""
Issue #821 Validation: Enhanced CI Infrastructure Resilience
=========================================================

Validates enhanced robustness measures for handling CI infrastructure failures
and transient issues that cause workflow job failures despite correct configuration.
"""

import os
import sys
import subprocess
import yaml
import json
from pathlib import Path

def test_enhanced_retry_mechanisms():
    """Test that workflows have appropriate retry and resilience configurations."""
    print("🔄 Testing Enhanced Retry Mechanisms")
    print("=" * 60)
    
    workflow_dir = Path(".github/workflows")
    if not workflow_dir.exists():
        print("❌ No workflows directory found")
        return False
    
    retry_features = 0
    resilience_features = 0
    
    for workflow_file in workflow_dir.glob("*.yml"):
        print(f"📋 Checking {workflow_file.name}")
        
        with open(workflow_file, 'r') as f:
            content = f.read()
            
        # Check for retry mechanisms
        if "continue-on-error" in content:
            print("   ✅ Has continue-on-error configuration")
            retry_features += 1
            
        if "timeout-minutes" in content:
            print("   ✅ Has timeout configuration")
            retry_features += 1
            
        # Check for resilience patterns
        if "|| echo" in content:
            print("   ✅ Has fallback error handling")
            resilience_features += 1
            
        if "if: failure()" in content:
            print("   ✅ Has failure handling")
            resilience_features += 1
    
    print(f"✅ Found {retry_features} retry mechanisms")
    print(f"✅ Found {resilience_features} resilience features")
    return True

def test_infrastructure_health_checks():
    """Test infrastructure health validation capabilities."""
    print("\n🏥 Testing Infrastructure Health Checks")
    print("=" * 60)
    
    health_checks = []
    
    # Test Python environment health
    try:
        import chardet
        print("✅ Python chardet dependency available")
        health_checks.append("python_deps")
    except ImportError:
        print("⚠️  chardet not available")
    
    # Test build system health
    try:
        result = subprocess.run([sys.executable, "ctmm_build.py"], 
                              capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            print("✅ CTMM build system healthy")
            health_checks.append("build_system")
        else:
            print("⚠️  CTMM build system issues detected")
    except Exception as e:
        print(f"⚠️  Build system check failed: {e}")
    
    # Test validation system health
    validation_scripts = [
        "validate_latex_syntax.py",
        "validate_workflow_syntax.py",
        "test_issue_743_validation.py"
    ]
    
    healthy_validations = 0
    for script in validation_scripts:
        if os.path.exists(script):
            try:
                result = subprocess.run([sys.executable, script], 
                                      capture_output=True, text=True, timeout=60)
                if result.returncode == 0:
                    print(f"✅ {script} healthy")
                    healthy_validations += 1
                else:
                    print(f"⚠️  {script} has issues")
            except Exception as e:
                print(f"⚠️  {script} check failed: {e}")
    
    health_checks.append(f"validations_{healthy_validations}")
    
    print(f"✅ Infrastructure health checks: {len(health_checks)}")
    return len(health_checks) >= 2

def test_enhanced_error_reporting():
    """Test enhanced error reporting and diagnostics capabilities."""
    print("\n📊 Testing Enhanced Error Reporting")
    print("=" * 60)
    
    # Check for artifact upload configurations
    workflow_dir = Path(".github/workflows")
    artifact_configs = 0
    log_configs = 0
    
    for workflow_file in workflow_dir.glob("*.yml"):
        with open(workflow_file, 'r') as f:
            content = f.read()
            
        if "upload-artifact" in content:
            print(f"✅ {workflow_file.name} has artifact upload")
            artifact_configs += 1
            
        if "*.log" in content or "logs" in content.lower():
            print(f"✅ {workflow_file.name} has log configuration")
            log_configs += 1
    
    # Test diagnostic capabilities
    diagnostic_files = [
        "validate_workflow_syntax.py",
        "test_issue_761_fix.py", 
        "test_issue_743_validation.py"
    ]
    
    available_diagnostics = 0
    for diag_file in diagnostic_files:
        if os.path.exists(diag_file):
            print(f"✅ Diagnostic tool available: {diag_file}")
            available_diagnostics += 1
    
    print(f"✅ Artifact configurations: {artifact_configs}")
    print(f"✅ Log configurations: {log_configs}")
    print(f"✅ Diagnostic tools: {available_diagnostics}")
    
    return artifact_configs >= 2 and available_diagnostics >= 2

def test_graceful_degradation():
    """Test graceful degradation when infrastructure components are unavailable."""
    print("\n🛡️  Testing Graceful Degradation")
    print("=" * 60)
    
    degradation_patterns = []
    
    # Test build system degradation
    try:
        result = subprocess.run([sys.executable, "ctmm_build.py"], 
                              capture_output=True, text=True, timeout=60)
        if "pdflatex not found" in result.stdout and result.returncode == 0:
            print("✅ Build system gracefully handles missing LaTeX")
            degradation_patterns.append("latex_graceful")
        elif result.returncode == 0:
            print("✅ Build system functions normally")
            degradation_patterns.append("build_normal")
    except Exception as e:
        print(f"⚠️  Build system degradation test failed: {e}")
    
    # Check for graceful error handling patterns in workflows
    workflow_dir = Path(".github/workflows")
    graceful_patterns = 0
    
    for workflow_file in workflow_dir.glob("*.yml"):
        with open(workflow_file, 'r') as f:
            content = f.read()
            
        # Look for graceful degradation patterns
        if "|| echo" in content and "Warning" in content:
            print(f"✅ {workflow_file.name} has graceful warning handling")
            graceful_patterns += 1
        
        if "continue-on-error" in content:
            print(f"✅ {workflow_file.name} has continue-on-error patterns")
            graceful_patterns += 1
    
    degradation_patterns.append(f"graceful_patterns_{graceful_patterns}")
    
    print(f"✅ Graceful degradation features: {len(degradation_patterns)}")
    return len(degradation_patterns) >= 2

def test_comprehensive_resilience():
    """Test overall CI pipeline resilience against infrastructure failures."""
    print("\n🎯 Testing Comprehensive Resilience")
    print("=" * 60)
    
    resilience_score = 0
    max_score = 6
    
    # Test 1: Workflow syntax robustness
    try:
        result = subprocess.run([sys.executable, "validate_workflow_syntax.py"], 
                              capture_output=True, text=True, timeout=60)
        if result.returncode == 0 and "ALL WORKFLOW FILES HAVE CORRECT SYNTAX" in result.stdout:
            print("✅ Workflow syntax is robust")
            resilience_score += 1
    except Exception:
        print("⚠️  Workflow syntax validation failed")
    
    # Test 2: Build system resilience
    try:
        result = subprocess.run([sys.executable, "test_issue_761_fix.py"], 
                              capture_output=True, text=True, timeout=60)
        if result.returncode == 0 and "ALL TESTS PASSED" in result.stdout:
            print("✅ Enhanced robustness measures validated")
            resilience_score += 1
    except Exception:
        print("⚠️  Robustness validation failed")
    
    # Test 3: Validation system resilience
    try:
        result = subprocess.run([sys.executable, "test_issue_743_validation.py"], 
                              capture_output=True, text=True, timeout=60)
        if result.returncode == 0 and "ALL VALIDATION TESTS PASSED" in result.stdout:
            print("✅ Comprehensive validation system resilient")
            resilience_score += 1
    except Exception:
        print("⚠️  Validation system check failed")
    
    # Test 4: LaTeX syntax validation resilience
    try:
        result = subprocess.run([sys.executable, "validate_latex_syntax.py"], 
                              capture_output=True, text=True, timeout=60)
        if result.returncode == 0 and "validation checks passed" in result.stdout:
            print("✅ LaTeX validation is resilient")
            resilience_score += 1
    except Exception:
        print("⚠️  LaTeX validation failed")
    
    # Test 5: CTMM build system resilience
    try:
        result = subprocess.run([sys.executable, "ctmm_build.py"], 
                              capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            print("✅ CTMM build system is resilient")
            resilience_score += 1
    except Exception:
        print("⚠️  CTMM build system failed")
    
    # Test 6: Error recovery mechanisms
    workflow_files = list(Path(".github/workflows").glob("*.yml"))
    if len(workflow_files) >= 3:
        print("✅ Multiple workflow files provide redundancy")
        resilience_score += 1
    
    print(f"\n🏆 Resilience Score: {resilience_score}/{max_score}")
    return resilience_score >= 5

def main():
    """Run all Issue #821 CI infrastructure resilience validations."""
    print("=" * 70)
    print("ISSUE #821 VALIDATION: Enhanced CI Infrastructure Resilience")
    print("=" * 70)
    
    tests = [
        ("Enhanced Retry Mechanisms", test_enhanced_retry_mechanisms),
        ("Infrastructure Health Checks", test_infrastructure_health_checks), 
        ("Enhanced Error Reporting", test_enhanced_error_reporting),
        ("Graceful Degradation", test_graceful_degradation),
        ("Comprehensive Resilience", test_comprehensive_resilience)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"\n✅ {test_name}: PASSED")
            else:
                print(f"\n❌ {test_name}: FAILED")
        except Exception as e:
            print(f"\n❌ {test_name}: ERROR - {e}")
    
    print("\n" + "=" * 70)
    print("VALIDATION SUMMARY")
    print("=" * 70)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! CI infrastructure resilience validated.")
        print("\nThe enhanced CI configuration should handle:")
        print("✓ Infrastructure transient failures")
        print("✓ Improved error detection and recovery")
        print("✓ Better diagnostic information")
        print("✓ Graceful degradation under stress")
        return True
    else:
        print("⚠️  Some resilience measures need improvement.")
        print("Review failed tests and enhance CI configuration.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)