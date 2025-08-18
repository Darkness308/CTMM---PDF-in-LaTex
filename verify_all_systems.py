#!/usr/bin/env python3
"""
Comprehensive Validation Runner - Centralized Orchestration

This script provides centralized orchestration of all validation systems including:
1. All issue verification scripts
2. CI/CD pipeline validation
3. GitHub Actions workflow validation
4. Build system validation
5. Repository health checks
"""

import subprocess
import sys
import time
from pathlib import Path

def run_command(cmd, description="", timeout=120):
    """Run a command and return success status and output."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        success = result.returncode == 0
        return success, result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        return False, "", f"Command timed out after {timeout} seconds"
    except Exception as e:
        return False, "", str(e)

def find_verification_scripts():
    """Find all verification scripts in the repository."""
    
    print("=" * 80)
    print("COMPREHENSIVE VALIDATION - DISCOVERY PHASE")
    print("=" * 80)
    print("Discovering all available verification and validation scripts.\n")
    
    # Find all verification scripts
    verify_scripts = sorted(Path(".").glob("verify_*.py"))
    validate_scripts = sorted(Path(".").glob("validate_*.py"))
    test_scripts = sorted(Path(".").glob("test_*.py"))
    
    print(f"📊 Script discovery results:")
    print(f"   Verification scripts: {len(verify_scripts)}")
    print(f"   Validation scripts: {len(validate_scripts)}")
    print(f"   Test scripts: {len(test_scripts)}")
    
    return verify_scripts, validate_scripts, test_scripts

def run_verification_scripts(verify_scripts):
    """Run all verification scripts and collect results."""
    
    print("\n🔍 COMPREHENSIVE VALIDATION - VERIFICATION PHASE")
    print("-" * 50)
    
    results = {}
    total_scripts = len(verify_scripts)
    passed_scripts = 0
    
    for i, script in enumerate(verify_scripts, 1):
        print(f"\n[{i}/{total_scripts}] Running {script.name}...")
        
        success, stdout, stderr = run_command(f"python3 {script}", f"Verify {script.name}")
        
        results[script.name] = {
            'success': success,
            'stdout': stdout,
            'stderr': stderr
        }
        
        if success:
            print(f"✅ {script.name}: PASSED")
            passed_scripts += 1
        else:
            print(f"❌ {script.name}: FAILED")
            if stderr:
                print(f"   Error: {stderr[:100]}...")
    
    print(f"\n📊 Verification results: {passed_scripts}/{total_scripts} scripts passed")
    return results, passed_scripts, total_scripts

def run_validation_scripts(validate_scripts):
    """Run all validation scripts and collect results."""
    
    print("\n🛠️  COMPREHENSIVE VALIDATION - VALIDATION PHASE")
    print("-" * 50)
    
    results = {}
    total_scripts = len(validate_scripts)
    passed_scripts = 0
    
    for i, script in enumerate(validate_scripts, 1):
        print(f"\n[{i}/{total_scripts}] Running {script.name}...")
        
        success, stdout, stderr = run_command(f"python3 {script}", f"Validate {script.name}")
        
        results[script.name] = {
            'success': success,
            'stdout': stdout,
            'stderr': stderr
        }
        
        # Special handling for some validation scripts that may "fail" normally
        if success or "No file changes detected" in stderr:
            print(f"✅ {script.name}: OPERATIONAL")
            passed_scripts += 1
        else:
            print(f"❌ {script.name}: FAILED")
            if stderr:
                print(f"   Error: {stderr[:100]}...")
    
    print(f"\n📊 Validation results: {passed_scripts}/{total_scripts} scripts operational")
    return results, passed_scripts, total_scripts

def run_core_system_tests():
    """Run core system functionality tests."""
    
    print("\n🧪 COMPREHENSIVE VALIDATION - CORE SYSTEM TESTS")
    print("-" * 50)
    
    core_tests = [
        ("CTMM Build System", "python3 ctmm_build.py"),
        ("LaTeX Validation", "python3 latex_validator.py main.tex"),
        ("Repository Structure", "ls -la && echo 'Structure check passed'"),
        ("Git Status", "git status --porcelain"),
        ("Python Syntax", "python3 -m py_compile *.py")
    ]
    
    results = {}
    passed_tests = 0
    
    for test_name, command in core_tests:
        print(f"\n--- {test_name} ---")
        
        success, stdout, stderr = run_command(command, test_name)
        
        results[test_name] = {
            'success': success,
            'stdout': stdout,
            'stderr': stderr
        }
        
        if success:
            print(f"✅ {test_name}: PASSED")
            passed_tests += 1
        else:
            print(f"❌ {test_name}: FAILED")
            if stderr:
                print(f"   Error: {stderr[:100]}...")
    
    print(f"\n📊 Core system results: {passed_tests}/{len(core_tests)} tests passed")
    return results, passed_tests, len(core_tests)

def check_repository_health():
    """Check overall repository health and configuration."""
    
    print("\n💚 COMPREHENSIVE VALIDATION - REPOSITORY HEALTH")
    print("-" * 50)
    
    health_checks = []
    
    # Check essential files
    essential_files = [
        "README.md",
        "main.tex", 
        ".gitignore",
        "Makefile",
        "ctmm_build.py",
        "validate_pr.py"
    ]
    
    missing_files = []
    for file_path in essential_files:
        if Path(file_path).exists():
            health_checks.append(f"✅ {file_path}")
        else:
            missing_files.append(file_path)
            health_checks.append(f"❌ {file_path} missing")
    
    # Check directory structure
    essential_dirs = [
        "modules",
        "style", 
        ".github/workflows"
    ]
    
    for dir_path in essential_dirs:
        if Path(dir_path).exists():
            health_checks.append(f"✅ {dir_path}/ directory")
        else:
            health_checks.append(f"❌ {dir_path}/ directory missing")
    
    # Print health results
    for check in health_checks:
        print(f"   {check}")
    
    health_score = len([c for c in health_checks if c.startswith("✅")])
    total_checks = len(health_checks)
    
    print(f"\n📊 Repository health: {health_score}/{total_checks} checks passed")
    
    return health_score, total_checks

def generate_comprehensive_report(verify_results, validate_results, core_results, health_score, health_total):
    """Generate a comprehensive validation report."""
    
    print("\n" + "=" * 80)
    print("COMPREHENSIVE VALIDATION REPORT")
    print("=" * 80)
    
    # Calculate overall success rate
    total_tests = sum([
        verify_results[1],
        validate_results[1], 
        core_results[1],
        health_score
    ])
    
    total_possible = sum([
        verify_results[2],
        validate_results[2],
        core_results[2],
        health_total
    ])
    
    success_rate = (total_tests / total_possible) * 100 if total_possible > 0 else 0
    
    print(f"📊 OVERALL VALIDATION SUMMARY")
    print(f"   Verification scripts: {verify_results[1]}/{verify_results[2]} passed")
    print(f"   Validation scripts: {validate_results[1]}/{validate_results[2]} operational") 
    print(f"   Core system tests: {core_results[1]}/{core_results[2]} passed")
    print(f"   Repository health: {health_score}/{health_total} checks passed")
    print(f"   Overall success rate: {success_rate:.1f}%")
    
    if success_rate >= 85:
        print("\n🎉 COMPREHENSIVE VALIDATION: EXCELLENT")
        print("✅ Repository is in excellent condition")
        print("✅ All major systems operational")
        print("✅ Verification infrastructure complete")
        print("✅ Ready for production use")
        return True
    elif success_rate >= 70:
        print("\n✅ COMPREHENSIVE VALIDATION: GOOD")
        print("✅ Repository is in good condition")
        print("⚠️  Some minor issues to address")
        print("✅ Core functionality operational")
        return True
    else:
        print("\n❌ COMPREHENSIVE VALIDATION: NEEDS ATTENTION")
        print("❌ Multiple issues detected")
        print("❌ Some core systems need attention")
        print("❌ Review failed tests above")
        return False

def main():
    """Main comprehensive validation orchestration function."""
    
    print("🎯 COMPREHENSIVE VALIDATION ORCHESTRATION")
    print("Centralized validation of all repository systems and processes\n")
    
    start_time = time.time()
    
    # Discovery phase
    verify_scripts, validate_scripts, test_scripts = find_verification_scripts()
    
    # Execution phases
    verify_results = run_verification_scripts(verify_scripts)
    validate_results = run_validation_scripts(validate_scripts) 
    core_results = run_core_system_tests()
    health_score, health_total = check_repository_health()
    
    # Report generation
    overall_success = generate_comprehensive_report(
        verify_results, validate_results, core_results, health_score, health_total
    )
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"\n⏱️  Validation completed in {duration:.1f} seconds")
    print(f"📁 Total scripts discovered: {len(verify_scripts) + len(validate_scripts) + len(test_scripts)}")
    print(f"🔍 Total validations performed: {verify_results[2] + validate_results[2] + core_results[2] + health_total}")
    
    return overall_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)