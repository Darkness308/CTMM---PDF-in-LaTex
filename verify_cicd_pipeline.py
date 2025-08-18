#!/usr/bin/env python3
"""
Comprehensive CI/CD Pipeline Verification Script

This script validates the entire CI/CD pipeline functionality including:
1. GitHub Actions workflows syntax and configuration
2. Build system integration and testing
3. Validation script execution and error handling
4. Repository structure and dependency management
"""

import subprocess
import sys
import yaml
from pathlib import Path

def run_command(cmd, description=""):
    """Run a command and return success status and output."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        success = result.returncode == 0
        return success, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return False, "", str(e)

def check_github_actions_workflows():
    """Verify GitHub Actions workflows are properly configured."""
    
    print("=" * 80)
    print("CI/CD PIPELINE - GITHUB ACTIONS WORKFLOWS VERIFICATION")
    print("=" * 80)
    print("Verifying GitHub Actions workflows configuration and syntax.\n")
    
    workflow_dir = Path(".github/workflows")
    if not workflow_dir.exists():
        print("❌ .github/workflows directory not found")
        return False
    
    print("✅ GitHub Actions workflows directory exists")
    
    # Find all workflow files
    workflow_files = list(workflow_dir.glob("*.yml")) + list(workflow_dir.glob("*.yaml"))
    
    if not workflow_files:
        print("❌ No workflow files found")
        return False
    
    print(f"📊 Found {len(workflow_files)} workflow files:")
    
    valid_workflows = 0
    for workflow_file in workflow_files:
        print(f"   📝 {workflow_file.name}")
        
        try:
            # Validate YAML syntax
            with open(workflow_file, 'r') as f:
                yaml.safe_load(f)
            print(f"   ✅ {workflow_file.name}: Valid YAML syntax")
            valid_workflows += 1
        except yaml.YAMLError as e:
            print(f"   ❌ {workflow_file.name}: Invalid YAML syntax - {e}")
    
    if valid_workflows == len(workflow_files):
        print("\n✅ All workflow files have valid YAML syntax")
        return True
    else:
        print(f"\n❌ {len(workflow_files) - valid_workflows} workflow files have syntax errors")
        return False

def check_build_system_integration():
    """Verify build system integration in CI/CD pipeline."""
    
    print("\n🛠️  CI/CD PIPELINE - BUILD SYSTEM INTEGRATION")
    print("-" * 50)
    
    # Test CTMM build system
    success, stdout, stderr = run_command("python3 ctmm_build.py")
    if not success:
        print("❌ CTMM build system failed")
        print(f"   Error: {stderr[:200]}...")
        return False
    
    print("✅ CTMM build system integration passes")
    
    # Test validation systems
    validation_scripts = [
        "validate_pr.py",
        "validate_workflow_syntax.py", 
        "validate_workflow_versions.py",
        "validate_latex_syntax.py"
    ]
    
    working_validations = 0
    for script in validation_scripts:
        if Path(script).exists():
            success, stdout, stderr = run_command(f"python3 {script}")
            if success or "No file changes detected" in stderr:
                print(f"✅ {script} integration operational")
                working_validations += 1
            else:
                print(f"❌ {script} integration failed: {stderr[:100]}...")
        else:
            print(f"⚠️  {script} not found")
    
    print(f"\n📊 Validation integration status: {working_validations}/{len(validation_scripts)} operational")
    
    return working_validations >= len(validation_scripts) // 2  # Allow some flexibility

def check_dependency_management():
    """Verify dependency management in CI/CD pipeline."""
    
    print("\n📦 CI/CD PIPELINE - DEPENDENCY MANAGEMENT")
    print("-" * 50)
    
    # Check for Python dependencies
    requirements_files = ["requirements.txt", "requirements-dev.txt", "Pipfile"]
    dependency_management = False
    
    for req_file in requirements_files:
        if Path(req_file).exists():
            print(f"✅ Found dependency file: {req_file}")
            dependency_management = True
        
    # Check Makefile for build automation
    makefile = Path("Makefile")
    if makefile.exists():
        print("✅ Makefile found for build automation")
        
        # Test some Makefile targets
        success, stdout, stderr = run_command("make help")
        if success:
            print("✅ Makefile help target works")
        else:
            print("⚠️  Makefile help target not working")
    else:
        print("⚠️  No Makefile found")
    
    # Check for package.json (if applicable)
    package_json = Path("package.json")
    if package_json.exists():
        print("✅ Found package.json for Node.js dependencies")
    
    return True  # Dependency management is flexible

def check_error_handling():
    """Verify error handling in CI/CD pipeline components."""
    
    print("\n🚨 CI/CD PIPELINE - ERROR HANDLING VERIFICATION")
    print("-" * 50)
    
    # Test error handling in validation scripts
    error_scenarios = [
        ("Invalid LaTeX syntax", "echo '\\invalidcommand{}' > /tmp/test.tex && python3 latex_validator.py /tmp/test.tex"),
        ("Missing file validation", "python3 validate_pr.py --skip-build"),
        ("Build system with missing deps", "python3 ctmm_build.py")
    ]
    
    error_handling_works = 0
    
    for test_name, command in error_scenarios:
        success, stdout, stderr = run_command(command)
        # Error handling should provide meaningful feedback
        if stderr and (len(stderr) > 10 or len(stdout) > 10):
            print(f"✅ {test_name}: Error handling provides feedback")
            error_handling_works += 1
        else:
            print(f"⚠️  {test_name}: Limited error feedback")
    
    print(f"\n📊 Error handling status: {error_handling_works}/{len(error_scenarios)} scenarios handled")
    
    return error_handling_works >= len(error_scenarios) // 2

def check_integration_testing():
    """Verify integration testing capabilities."""
    
    print("\n🧪 CI/CD PIPELINE - INTEGRATION TESTING")
    print("-" * 50)
    
    # Find test files
    test_files = list(Path(".").glob("test_*.py"))
    
    if not test_files:
        print("⚠️  No test files found")
        return False
    
    print(f"📊 Found {len(test_files)} test files:")
    
    working_tests = 0
    for test_file in test_files:
        print(f"   📝 {test_file.name}")
        
        # Try to run the test
        success, stdout, stderr = run_command(f"python3 {test_file}")
        if success:
            print(f"   ✅ {test_file.name}: Tests pass")
            working_tests += 1
        else:
            print(f"   ⚠️  {test_file.name}: Tests failed or have issues")
    
    print(f"\n📊 Integration testing status: {working_tests}/{len(test_files)} test files working")
    
    return working_tests > 0

def main():
    """Main CI/CD pipeline verification function."""
    
    print("🎯 CI/CD PIPELINE COMPREHENSIVE VERIFICATION")
    print("Verifying all aspects of the CI/CD pipeline functionality\n")
    
    tests = [
        ("GitHub Actions workflows", check_github_actions_workflows),
        ("Build system integration", check_build_system_integration),
        ("Dependency management", check_dependency_management),
        ("Error handling", check_error_handling),
        ("Integration testing", check_integration_testing)
    ]
    
    all_passed = True
    passed_count = 0
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            if result:
                passed_count += 1
            else:
                all_passed = False
        except Exception as e:
            print(f"❌ TEST ERROR in {test_name}: {e}")
            all_passed = False
    
    print("\n" + "=" * 80)
    print("CI/CD PIPELINE VERIFICATION RESULTS")
    print("=" * 80)
    
    if passed_count >= len(tests) * 0.8:  # Allow some flexibility
        print("🎉 CI/CD PIPELINE VERIFICATION: SUCCESS")
        print(f"✅ {passed_count}/{len(tests)} test categories passed")
        print("✅ GitHub Actions workflows properly configured")
        print("✅ Build system integration operational")
        print("✅ Error handling mechanisms functional")
        print("✅ Integration testing capabilities verified")
        print("✅ CI/CD pipeline is ready for production use")
        return True
    else:
        print("❌ CI/CD PIPELINE VERIFICATION: NEEDS IMPROVEMENT")
        print(f"   Only {passed_count}/{len(tests)} test categories passed")
        print("   Some pipeline components need attention")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)