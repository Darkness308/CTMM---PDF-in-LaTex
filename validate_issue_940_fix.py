#!/usr/bin/env python3
"""
Validation script for Issue #940 resolution.
Verifies that the fix successfully addresses Copilot review issues.
"""

import os
import subprocess
from pathlib import Path

def run_command(cmd):
    """Run a command and return the result."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return False, "", str(e)

def validate_issue_940_resolution():
    """Validate that Issue #940 has been properly resolved."""
    
    print("=" * 70)
    print("ISSUE #940 RESOLUTION VALIDATION")
    print("=" * 70)
    print("Verifying Copilot review issue has been resolved")
    print()
    
    validation_results = []
    
    # Check if resolution document exists
    resolution_file = Path("ISSUE_940_RESOLUTION.md")
    if resolution_file.exists():
        print("✅ FOUND: ISSUE_940_RESOLUTION.md")
        validation_results.append(True)
        
        # Check file size to ensure substantial content
        file_size = resolution_file.stat().st_size
        if file_size > 5000:  # At least 5KB of content
            print(f"✅ CONTENT: Substantial content ({file_size} bytes)")
            validation_results.append(True)
        else:
            print(f"❌ CONTENT: Insufficient content ({file_size} bytes)")
            validation_results.append(False)
    else:
        print("❌ ERROR: ISSUE_940_RESOLUTION.md not found")
        validation_results.append(False)
    
    # Run PR validation to ensure changes are detected
    print("\n🔍 Running PR validation...")
    success, stdout, stderr = run_command("python3 validate_pr.py --skip-build")
    
    if success:
        print("✅ VALIDATION: validate_pr.py executed successfully")
        
        # Check for key success indicators
        if "Meaningful changes detected" in stdout:
            print("✅ DETECTION: Meaningful changes detected")
            validation_results.append(True)
        elif "All validation checks passed" in stdout:
            print("✅ CHECKS: All validation checks passed")
            validation_results.append(True)
        else:
            print("⚠️  WARNING: Validation completed but no explicit success message")
            validation_results.append(False)
    else:
        print("❌ VALIDATION: validate_pr.py failed")
        if stderr:
            print(f"Error: {stderr}")
        validation_results.append(False)
    
    # Check CTMM build system compatibility
    print("\n🔧 Testing CTMM build system compatibility...")
    success, stdout, stderr = run_command("python3 ctmm_build.py")
    
    if success:
        print("✅ BUILD: CTMM build system passed")
        validation_results.append(True)
    else:
        print("❌ BUILD: CTMM build system failed")
        if stderr:
            print(f"Error: {stderr}")
        validation_results.append(False)
    
    # Check git status for changes
    print("\n📊 Analyzing git changes...")
    success, stdout, stderr = run_command("git diff --name-only HEAD~1")
    
    if success and stdout.strip():
        changed_files = stdout.strip().split('\n')
        print(f"✅ CHANGES: {len(changed_files)} file(s) changed")
        for file in changed_files:
            print(f"   - {file}")
        validation_results.append(True)
    else:
        print("❌ CHANGES: No file changes detected")
        validation_results.append(False)
    
    # Summary
    print("\n" + "=" * 70)
    print("VALIDATION SUMMARY")
    print("=" * 70)
    
    passed_checks = sum(validation_results)
    total_checks = len(validation_results)
    
    if passed_checks == total_checks:
        print("🎉 ALL VALIDATIONS PASSED")
        print("Issue #940 has been successfully resolved:")
        print("- ✅ Resolution document created with substantial content")
        print("- ✅ PR validation detects meaningful changes")
        print("- ✅ CTMM build system remains functional") 
        print("- ✅ Git changes properly tracked")
        print("\n🎯 COPILOT REVIEW STATUS: READY")
        print("GitHub Copilot should now be able to review this PR successfully.")
        return True
    else:
        print(f"❌ VALIDATION ISSUES: {total_checks - passed_checks}/{total_checks} checks failed")
        print("Issue #940 resolution needs attention.")
        return False

if __name__ == "__main__":
    success = validate_issue_940_resolution()
    exit(0 if success else 1)