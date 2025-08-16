#!/usr/bin/env python3
"""
Enhanced PR Validation with Improved Error Handling - Issue #765

This script provides enhanced validation with better error messages and guidance
for contributors when validation fails, particularly for empty PR scenarios.
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, description=""):
    """Run a command and return success status and output."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"
    except Exception as e:
        return False, "", str(e)

def enhanced_empty_pr_feedback():
    """Provide enhanced feedback for empty PR scenarios."""
    print("🔍 EMPTY PR DETECTED")
    print("=" * 50)
    print("GitHub Copilot requires meaningful changes to perform reviews.")
    print()
    print("📋 RESOLUTION OPTIONS:")
    print("1. Add substantial code or documentation changes")
    print("2. Review existing issue resolutions for patterns:")
    print("   - ISSUE_409_RESOLUTION.md (original solution)")
    print("   - ISSUE_731_RESOLUTION.md (recent example)")
    print("   - ISSUE_765_RESOLUTION.md (this issue's solution)")
    print("3. Ensure at least 50+ lines of meaningful content")
    print()
    print("✅ SUCCESSFUL PATTERN: Add comprehensive documentation")
    print("   with technical implementation details")
    print()
    print("📖 HELPFUL RESOURCES:")
    print("   - Repository has 10+ successful issue resolutions")
    print("   - Each follows similar pattern: documentation + validation")
    print("   - Previous resolutions: #409, #476, #667, #673, #708, #731")
    print()
    print("🔧 NEXT STEPS:")
    print("1. Create meaningful file changes (code, docs, or improvements)")
    print("2. Ensure changes provide value to the repository")
    print("3. Run validation again: python3 validate_pr_enhanced.py")
    print("4. Verify with: python3 verify_issue_765_fix.py")

def enhanced_validation_feedback(files_changed, added_lines, deleted_lines):
    """Provide enhanced feedback for validation results."""
    print("📊 VALIDATION SUMMARY")
    print("=" * 50)
    print(f"Files Changed: {files_changed}")
    print(f"Lines Added: {added_lines}")
    print(f"Lines Deleted: {deleted_lines}")
    print()
    
    if files_changed == 0 and added_lines == 0:
        print("❌ COPILOT REVIEW STATUS: Cannot review empty changes")
        enhanced_empty_pr_feedback()
        return False
    elif files_changed > 0 and added_lines >= 50:
        print("✅ COPILOT REVIEW STATUS: Ready for meaningful review")
        print("🎯 Substantial changes detected - Copilot can analyze these modifications")
        return True
    elif files_changed > 0 and added_lines < 50:
        print("⚠️  COPILOT REVIEW STATUS: Minimal changes detected")
        print(f"   Consider adding more substantial content ({added_lines} lines may be insufficient)")
        print("   Recommended: 50+ lines of meaningful additions")
        return True  # Still reviewable, but guidance provided
    else:
        print("❓ COPILOT REVIEW STATUS: Uncertain - unusual change pattern")
        return True

def check_file_changes(base_branch="main"):
    """Enhanced file change detection with better error handling."""
    print("🔍 ENHANCED FILE CHANGE ANALYSIS")
    print("=" * 50)
    
    # Try multiple base branch options with better error handling
    base_options = [f"origin/{base_branch}", base_branch, "origin/main", "main"]
    actual_base = None
    
    for base_option in base_options:
        success, _, _ = run_command(f"git rev-parse {base_option}")
        if success:
            actual_base = base_option
            print(f"✓ Using base branch: {actual_base}")
            break
    
    if not actual_base:
        print("⚠️  No suitable base branch found, checking working directory changes...")
        success, stdout, stderr = run_command("git diff --name-only")
        if not success:
            print(f"❌ Error checking changes: {stderr}")
            return False, 0, 0, 0
        actual_base = ""
    
    # Get file changes with enhanced error handling
    if actual_base:
        success, stdout, stderr = run_command(f"git diff --name-only {actual_base}..HEAD")
        if not success:
            print(f"❌ Error checking file changes: {stderr}")
            return False, 0, 0, 0
    else:
        success, stdout, stderr = run_command("git diff --name-only")
        if not success:
            print(f"❌ Error checking working directory changes: {stderr}")
            return False, 0, 0, 0
    
    changed_files = len(stdout.split('\n')) if stdout.strip() else 0
    
    # Get line statistics with enhanced error handling
    if actual_base:
        success, stdout, stderr = run_command(f"git diff --numstat {actual_base}..HEAD")
    else:
        success, stdout, stderr = run_command("git diff --numstat")
    
    added_lines = 0
    deleted_lines = 0
    
    if success and stdout.strip():
        for line in stdout.split('\n'):
            if line.strip():
                parts = line.split('\t')
                if len(parts) >= 2:
                    try:
                        added_lines += int(parts[0]) if parts[0] != '-' else 0
                        deleted_lines += int(parts[1]) if parts[1] != '-' else 0
                    except ValueError:
                        continue
    
    print(f"📁 Files analyzed: {changed_files}")
    print(f"➕ Lines added: {added_lines}")
    print(f"➖ Lines deleted: {deleted_lines}")
    
    return True, changed_files, added_lines, deleted_lines

def validate_ctmm_integration():
    """Validate integration with CTMM build system."""
    print("\n🔧 CTMM INTEGRATION VALIDATION")
    print("=" * 50)
    
    success, stdout, stderr = run_command("python3 ctmm_build.py")
    if success:
        print("✅ CTMM build system: PASS")
        return True
    else:
        print("❌ CTMM build system: FAIL")
        print(f"   Error: {stderr}")
        return False

def main():
    """Enhanced main validation function with improved feedback."""
    print("🔍 ENHANCED CTMM PR VALIDATION - Issue #765")
    print("=" * 70)
    print("Enhanced validation with improved error handling and guidance")
    print()
    
    # Change to repository directory
    repo_path = Path(__file__).parent
    os.chdir(repo_path)
    
    all_passed = True
    
    # 1. Enhanced file change analysis
    success, files_changed, added_lines, deleted_lines = check_file_changes()
    if not success:
        all_passed = False
    else:
        validation_passed = enhanced_validation_feedback(files_changed, added_lines, deleted_lines)
        if not validation_passed:
            all_passed = False
    
    # 2. CTMM integration validation
    if not validate_ctmm_integration():
        all_passed = False
    
    # 3. Final summary with enhanced feedback
    print("\n" + "=" * 70)
    if all_passed and files_changed > 0 and added_lines > 0:
        print("✅ ENHANCED VALIDATION: ALL CHECKS PASSED")
        print("🎯 Ready for Copilot review with meaningful changes")
        print()
        print("📋 VALIDATION SUMMARY:")
        print(f"   ✓ Files changed: {files_changed}")
        print(f"   ✓ Lines added: {added_lines}")
        print(f"   ✓ CTMM integration: PASS")
        print(f"   ✓ Copilot review: READY")
    else:
        print("❌ ENHANCED VALIDATION: ISSUES DETECTED")
        print("Please address the issues above before proceeding.")
        print()
        print("💡 TIP: Review successful issue resolutions in this repository:")
        print("   - ISSUE_409_RESOLUTION.md")
        print("   - ISSUE_731_RESOLUTION.md") 
        print("   - ISSUE_765_RESOLUTION.md")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)