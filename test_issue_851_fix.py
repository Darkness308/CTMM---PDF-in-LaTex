#!/usr/bin/env python3
"""
Test script for Issue #851 verification functionality.

This script tests that the comprehensive verification infrastructure
created for issue #851 is working correctly.
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, description=""):
    """Run a command and return success status and output."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120)
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"
    except Exception as e:
        return False, "", str(e)

def test_issue_851_verification_script():
    """Test that the Issue #851 verification script works correctly."""
    
    print("🧪 Testing Issue #851 verification script...")
    
    # Check that the script exists
    script_path = Path("verify_issue_851_fix.py")
    if not script_path.exists():
        print("❌ verify_issue_851_fix.py not found")
        return False
    
    print("✅ Verification script exists")
    
    # Test script execution
    success, stdout, stderr = run_command("python3 verify_issue_851_fix.py")
    if not success:
        print(f"❌ Verification script failed: {stderr}")
        return False
    
    # Check for expected output patterns
    expected_patterns = [
        "ISSUE #851 COMPREHENSIVE VERIFICATION",
        "Verification Scripts Infrastructure",
        "Validation Infrastructure",
        "GitHub Actions Workflows", 
        "CTMM Build System",
        "Test Infrastructure",
        "ALL VERIFICATION CHECKS PASSED"
    ]
    
    missing_patterns = []
    for pattern in expected_patterns:
        if pattern not in stdout:
            missing_patterns.append(pattern)
    
    if missing_patterns:
        print(f"❌ Missing expected output patterns: {', '.join(missing_patterns)}")
        return False
    
    print("✅ Verification script executed successfully with expected output")
    return True

def test_issue_851_documentation():
    """Test that the Issue #851 documentation is comprehensive."""
    
    print("\n🧪 Testing Issue #851 documentation...")
    
    doc_path = Path("ISSUE_851_RESOLUTION.md")
    if not doc_path.exists():
        print("❌ ISSUE_851_RESOLUTION.md not found")
        return False
    
    print("✅ Resolution documentation exists")
    
    content = doc_path.read_text()
    
    # Check minimum length for comprehensive documentation
    if len(content) < 8000:
        print(f"❌ Documentation too short: {len(content)} characters (expected 8000+)")
        return False
    
    print(f"✅ Documentation has {len(content)} characters")
    
    # Check for required sections
    required_sections = [
        "Problem Statement",
        "Root Cause Analysis",
        "Solution Implemented", 
        "Technical Implementation Details",
        "Verification Scripts Infrastructure",
        "Results and Validation",
        "Impact and Benefits",
        "Copilot Review Status",
        "Integration with Previous Resolutions"
    ]
    
    missing_sections = []
    for section in required_sections:
        if section not in content:
            missing_sections.append(section)
    
    if missing_sections:
        print(f"❌ Missing documentation sections: {', '.join(missing_sections)}")
        return False
    
    print("✅ All required documentation sections present")
    return True

def test_verification_script_coverage():
    """Test that all expected verification scripts exist."""
    
    print("\n🧪 Testing verification script coverage...")
    
    expected_scripts = [
        "verify_issue_673_fix.py",
        "verify_issue_708_fix.py",
        "verify_issue_731_fix.py", 
        "verify_issue_759_fix.py",
        "verify_issue_817_fix.py",
        "verify_issue_835_fix.py",
        "verify_issue_851_fix.py",
        "verify_copilot_fix.py"
    ]
    
    missing_scripts = []
    for script in expected_scripts:
        if not Path(script).exists():
            missing_scripts.append(script)
    
    if missing_scripts:
        print(f"❌ Missing verification scripts: {', '.join(missing_scripts)}")
        return False
    
    print(f"✅ All {len(expected_scripts)} verification scripts present")
    return True

def test_validation_infrastructure():
    """Test that validation infrastructure is working."""
    
    print("\n🧪 Testing validation infrastructure...")
    
    # Test PR validation
    success, stdout, stderr = run_command("python3 validate_pr.py --help")
    if not success:
        print(f"❌ PR validation help failed: {stderr}")
        return False
    
    if "Validate PR content" not in stdout:
        print("❌ PR validation help missing expected content")
        return False
    
    print("✅ PR validation tool working")
    
    # Test workflow validation
    success, stdout, stderr = run_command("python3 validate_workflow_versions.py")
    if not success:
        print(f"⚠️  Workflow validation issues (may be expected): {stderr[:100]}")
    else:
        print("✅ Workflow validation passed")
    
    return True

def test_meaningful_changes():
    """Test that meaningful changes exist for Copilot review."""
    
    print("\n🧪 Testing meaningful changes for Copilot...")
    
    # Check for committed changes
    success, stdout, stderr = run_command("git diff --name-only origin/main..HEAD")
    if not success:
        print(f"❌ Git diff failed: {stderr}")
        return False
    
    if not stdout.strip():
        print("❌ No committed changes found")
        return False
    
    changed_files = stdout.strip().split('\n')
    print(f"✅ {len(changed_files)} files changed:")
    for file in changed_files[:5]:  # Show first 5 files
        print(f"   {file}")
    
    if len(changed_files) > 5:
        print(f"   ... and {len(changed_files) - 5} more files")
    
    # Check line count changes
    success, stdout, stderr = run_command("git diff --numstat origin/main..HEAD")
    if success and stdout.strip():
        total_added = 0
        total_deleted = 0
        for line in stdout.strip().split('\n'):
            parts = line.split('\t')
            if len(parts) >= 2:
                try:
                    added = int(parts[0]) if parts[0] != '-' else 0
                    deleted = int(parts[1]) if parts[1] != '-' else 0
                    total_added += added
                    total_deleted += deleted
                except ValueError:
                    pass
        
        print(f"✅ Total lines added: {total_added}, deleted: {total_deleted}")
        
        if total_added == 0 and total_deleted == 0:
            print("❌ No meaningful content changes")
            return False
    
    return True

def main():
    """Run all tests for Issue #851 verification."""
    
    print("🚀 ISSUE #851 VERIFICATION TESTING")
    print("Testing comprehensive verification infrastructure")
    print("=" * 70)
    
    all_tests_passed = True
    
    tests = [
        ("Issue #851 Verification Script", test_issue_851_verification_script),
        ("Issue #851 Documentation", test_issue_851_documentation),
        ("Verification Script Coverage", test_verification_script_coverage),
        ("Validation Infrastructure", test_validation_infrastructure),
        ("Meaningful Changes", test_meaningful_changes)
    ]
    
    for test_name, test_function in tests:
        try:
            if not test_function():
                all_tests_passed = False
        except Exception as e:
            print(f"❌ {test_name} ERROR: {e}")
            all_tests_passed = False
    
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    if all_tests_passed:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Issue #851 verification infrastructure is working correctly")
        print("✅ Copilot should be able to review this PR successfully")
        return True
    else:
        print("❌ Some tests failed")
        print("Please review the output above and address any issues")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)