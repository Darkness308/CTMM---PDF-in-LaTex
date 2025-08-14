#!/usr/bin/env python3
"""
Comprehensive Final Validation for Issue #534

This script runs all validation components to provide a final assessment
of GitHub Actions workflow configuration and German LaTeX support.
"""

import subprocess
import sys
import os
from pathlib import Path

def run_validation_script(script_name, description):
    """Run a validation script and return success status."""
    print(f"\n{'='*60}")
    print(f"Running {description}")
    print('='*60)
    
    try:
        result = subprocess.run(
            [sys.executable, script_name],
            capture_output=False,
            text=True,
            check=False
        )
        return result.returncode == 0
    except Exception as e:
        print(f"Error running {script_name}: {e}")
        return False

def main():
    """Run comprehensive validation suite."""
    
    print("🔍 COMPREHENSIVE VALIDATION SUITE - ISSUE #534")
    print("=" * 80)
    print("Running all validation components for final assessment\n")
    
    # Define validation scripts and their descriptions
    validations = [
        ('validate_github_actions_standards.py', 'GitHub Actions Standards Validation'),
        ('validate_german_latex_support.py', 'German LaTeX Support Validation'),
        ('validate_issue_532.py', 'YAML Syntax Validation (Issue #532)'),
        ('validate_workflow_syntax.py', 'Workflow Structure Validation'),
        ('ctmm_build.py', 'CTMM Build System Test')
    ]
    
    results = []
    
    for script, description in validations:
        if os.path.exists(script):
            success = run_validation_script(script, description)
            results.append((description, success))
        else:
            print(f"\n⚠️  Skipping {description} - script not found: {script}")
            results.append((description, False))
    
    # Final summary
    print(f"\n{'='*80}")
    print("FINAL VALIDATION SUMMARY - ISSUE #534")
    print('='*80)
    
    all_passed = True
    for description, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {description}")
        if not success:
            all_passed = False
    
    print()
    
    if all_passed:
        print("🎉 COMPREHENSIVE VALIDATION: SUCCESS")
        print("✅ All validation components passed")
        print("✅ GitHub Actions workflows are properly configured")
        print("✅ German LaTeX support is validated") 
        print("✅ CTMM build system integration confirmed")
        print("✅ CI/CD execution standards are met")
        print("\n📋 STATUS: ISSUE #534 FULLY RESOLVED")
        print("🚀 Repository is ready for reliable GitHub Actions execution")
    else:
        print("⚠️  COMPREHENSIVE VALIDATION: ISSUES DETECTED")
        print("❌ Some validation components failed")
        print("🔧 Review individual validation results above")
    
    print('='*80)
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)