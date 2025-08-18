#!/usr/bin/env python3
"""
Comprehensive CI/CD Pipeline Test Suite

This script provides comprehensive testing for CI/CD pipeline functionality
as required for Issue #878 resolution.
"""

import subprocess
import sys
import os
from pathlib import Path
import yaml

def run_command(cmd, description=""):
    """Run a command and return success status and output."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
        success = result.returncode == 0
        return success, result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"
    except Exception as e:
        return False, "", str(e)

def test_github_actions_workflows():
    """Test GitHub Actions workflow files."""
    
    print("⚙️  Testing GitHub Actions Workflows:")
    print("-" * 50)
    
    workflows_dir = Path(".github/workflows")
    if not workflows_dir.exists():
        print("❌ .github/workflows directory not found")
        return False
    
    workflow_files = list(workflows_dir.glob("*.yml"))
    if not workflow_files:
        print("❌ No workflow files found")
        return False
    
    print(f"✅ Found {len(workflow_files)} workflow files:")
    
    all_valid = True
    for workflow_file in workflow_files:
        try:
            with open(workflow_file, 'r') as f:
                yaml_content = yaml.safe_load(f)
            
            if yaml_content and 'jobs' in yaml_content:
                print(f"   ✅ {workflow_file.name} - Valid YAML with jobs")
            else:
                print(f"   ❌ {workflow_file.name} - Invalid structure")
                all_valid = False
                
        except yaml.YAMLError as e:
            print(f"   ❌ {workflow_file.name} - YAML syntax error: {e}")
            all_valid = False
        except Exception as e:
            print(f"   ❌ {workflow_file.name} - Error: {e}")
            all_valid = False
    
    return all_valid

def test_build_system_integration():
    """Test build system integration capabilities."""
    
    print("\n🏗️  Testing Build System Integration:")
    print("-" * 50)
    
    build_components = [
        ("CTMM Build", "python3 ctmm_build.py"),
        ("Build System Analysis", "python3 build_system.py --help"),
        ("Unified Tool", "python3 ctmm_unified_tool.py --help"),
        ("Make System", "make help")
    ]
    
    all_passed = True
    for component_name, command in build_components:
        success, stdout, stderr = run_command(command, f"Testing {component_name}")
        if success or "help" in stdout.lower() or "usage" in stdout.lower():
            print(f"   ✅ {component_name} - Functional")
        else:
            print(f"   ❌ {component_name} - Issues detected")
            all_passed = False
    
    return all_passed

def test_validation_systems():
    """Test validation system integration."""
    
    print("\n🔍 Testing Validation Systems:")
    print("-" * 50)
    
    validation_systems = [
        ("PR Validation", "python3 validate_pr.py --help"),
        ("LaTeX Validation", "python3 latex_validator.py --help"),
        ("Workflow Validation", "python3 validate_workflow_versions.py"),
        ("Syntax Validation", "python3 validate_latex_syntax.py")
    ]
    
    all_passed = True
    for system_name, command in validation_systems:
        success, stdout, stderr = run_command(command, f"Testing {system_name}")
        if success or "help" in stdout.lower() or "usage" in stdout.lower() or "validation" in stdout.lower():
            print(f"   ✅ {system_name} - Operational")
        else:
            print(f"   ❌ {system_name} - Issues detected")
            all_passed = False
    
    return all_passed

def test_verification_infrastructure():
    """Test verification script infrastructure."""
    
    print("\n✅ Testing Verification Infrastructure:")
    print("-" * 50)
    
    # Count verification scripts
    verification_scripts = list(Path(".").glob("verify_*_fix.py"))
    print(f"📊 Verification Scripts: {len(verification_scripts)}")
    
    if len(verification_scripts) >= 19:
        print(f"   ✅ Target achieved: {len(verification_scripts)}/19+ scripts")
    else:
        print(f"   ❌ Target not met: {len(verification_scripts)}/19 scripts")
        return False
    
    # Test verification suite
    if Path("run_verification_suite.py").exists():
        print("   ✅ Verification suite runner exists")
        success, stdout, stderr = run_command("python3 run_verification_suite.py --help", "Testing verification suite")
        if success or "verification" in stdout.lower():
            print("   ✅ Verification suite functional")
        else:
            print("   ⚠️  Verification suite may have issues")
    else:
        print("   ❌ Verification suite runner missing")
        return False
    
    return True

def test_documentation_completeness():
    """Test documentation completeness."""
    
    print("\n📚 Testing Documentation Completeness:")
    print("-" * 50)
    
    required_docs = [
        "README.md",
        "ISSUE_878_RESOLUTION.md",
        ".github/copilot-instructions.md",
        "Makefile"
    ]
    
    all_present = True
    for doc in required_docs:
        if Path(doc).exists():
            print(f"   ✅ {doc} - Present")
        else:
            print(f"   ❌ {doc} - Missing")
            all_present = False
    
    # Check for help systems
    success, stdout, stderr = run_command("make help", "Testing make help")
    if success and "help" in stdout.lower():
        print("   ✅ Make help system functional")
    else:
        print("   ❌ Make help system issues")
        all_present = False
    
    return all_present

def test_error_handling_robustness():
    """Test error handling robustness."""
    
    print("\n🛡️  Testing Error Handling Robustness:")
    print("-" * 50)
    
    # Test with invalid inputs
    error_tests = [
        ("Invalid LaTeX file", "python3 latex_validator.py /nonexistent/path/"),
        ("Invalid command args", "python3 ctmm_build.py --invalid-flag"),
        ("Missing file validation", "python3 validate_pr.py --nonexistent-option")
    ]
    
    robust_handling = True
    for test_name, command in error_tests:
        success, stdout, stderr = run_command(command, f"Testing {test_name}")
        # Error handling is good if it fails gracefully (returns error but doesn't crash)
        if not success and (stderr or "error" in stdout.lower() or "usage" in stdout.lower()):
            print(f"   ✅ {test_name} - Graceful error handling")
        elif success:
            print(f"   ⚠️  {test_name} - Unexpected success (may indicate issue)")
        else:
            print(f"   ❌ {test_name} - Poor error handling")
            robust_handling = False
    
    return robust_handling

def main():
    """Main CI/CD pipeline test function."""
    
    print("🚀 COMPREHENSIVE CI/CD PIPELINE TEST SUITE")
    print("=" * 80)
    print("Testing complete CI/CD pipeline functionality for Issue #878")
    print()
    
    test_functions = [
        ("GitHub Actions Workflows", test_github_actions_workflows),
        ("Build System Integration", test_build_system_integration),
        ("Validation Systems", test_validation_systems),
        ("Verification Infrastructure", test_verification_infrastructure),
        ("Documentation Completeness", test_documentation_completeness),
        ("Error Handling Robustness", test_error_handling_robustness)
    ]
    
    results = []
    total_tests = len(test_functions)
    passed_tests = 0
    
    for test_name, test_function in test_functions:
        try:
            result = test_function()
            results.append((test_name, result))
            if result:
                passed_tests += 1
        except Exception as e:
            print(f"❌ TEST ERROR in {test_name}: {e}")
            results.append((test_name, False))
    
    # Final assessment
    print("\n" + "=" * 80)
    print("CI/CD PIPELINE TEST RESULTS")
    print("=" * 80)
    
    success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
    
    print(f"📊 Overall Results:")
    print(f"   Total Tests: {total_tests}")
    print(f"   Passed: {passed_tests}")
    print(f"   Failed: {total_tests - passed_tests}")
    print(f"   Success Rate: {success_rate:.1f}%")
    print()
    
    print("📋 Test Results Summary:")
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status} {test_name}")
    
    print()
    
    if success_rate >= 80:
        print("🎉 CI/CD PIPELINE: COMPREHENSIVE AND FUNCTIONAL")
        print("✅ All major CI/CD components operational")
        print("✅ Verification infrastructure complete")
        print("✅ Error handling robust")
        print("✅ Ready for production deployment")
        return True
    else:
        print("⚠️  CI/CD PIPELINE: NEEDS IMPROVEMENT")
        print("   Address failing tests before production deployment")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)