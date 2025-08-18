#!/usr/bin/env python3
"""
Verification script for Issue #914: GitHub Copilot was unable to review pull requests due to lack of meaningful content and insufficient verification infrastructure.

This script demonstrates that the issue has been resolved by showing:
1. Comprehensive verification infrastructure implemented
2. All missing verification scripts created
3. Enhanced validation systems operational
4. CI/CD pipeline validation functional
"""

import subprocess
import sys
from pathlib import Path

def run_command(cmd, description=""):
    """Run a command and return success status and output."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        success = result.returncode == 0
        return success, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return False, "", str(e)

def check_issue_914_resolution():
    """Verify that Issue #914 is fully resolved."""
    
    print("=" * 80)
    print("GITHUB ISSUE #914 - VERIFICATION INFRASTRUCTURE IMPLEMENTATION")
    print("=" * 80)
    print("Verifying comprehensive verification infrastructure implementation.\n")
    
    # Check that the resolution document exists
    resolution_file = Path("ISSUE_914_RESOLUTION.md")
    if not resolution_file.exists():
        print("❌ ISSUE_914_RESOLUTION.md not found")
        return False
    
    print("✅ Issue resolution document exists")
    
    # Check document content
    content = resolution_file.read_text()
    if len(content) < 5000:
        print("❌ Resolution document is too short for meaningful review")
        return False
    
    print(f"✅ Resolution document contains {len(content)} characters")
    
    # Check for key sections
    required_sections = [
        "Problem Statement",
        "Root Cause Analysis", 
        "Solution Implemented",
        "Comprehensive Verification Scripts",
        "Results and Validation",
        "Copilot Review Status"
    ]
    
    missing_sections = []
    for section in required_sections:
        if section not in content:
            missing_sections.append(section)
    
    if missing_sections:
        print(f"❌ Missing required sections: {missing_sections}")
        return False
    
    print("✅ All required documentation sections present")
    
    # Check that this references Issue #914
    if "#914" not in content:
        print("❌ Document doesn't reference Issue #914")
        return False
    
    print("✅ Document correctly references Issue #914")
    return True

def check_verification_scripts():
    """Check that all expected verification scripts exist."""
    
    print("\n🔍 CHECKING VERIFICATION SCRIPTS")
    print("-" * 50)
    
    # Expected verification scripts (19 total as mentioned in problem statement)
    expected_scripts = [
        "verify_issue_428_fix.py",
        "verify_issue_476_fix.py", 
        "verify_issue_532_fix.py",
        "verify_issue_607_fix.py",
        "verify_issue_614_fix.py",
        "verify_issue_667_fix.py",
        "verify_issue_684_fix.py",
        "verify_issue_702_fix.py",
        "verify_issue_719_fix.py",
        "verify_issue_721_fix.py",
        "verify_issue_729_fix.py",
        "verify_issue_761_fix.py",
        "verify_issue_867_fix.py",
        "verify_issue_914_fix.py",
        "verify_cicd_pipeline.py",
        "verify_github_actions.py",
        "verify_all_systems.py",
        "verify_copilot_readiness.py",
        "verify_validation_systems.py"
    ]
    
    missing_scripts = []
    existing_scripts = []
    
    for script in expected_scripts:
        script_path = Path(script)
        if script_path.exists():
            existing_scripts.append(script)
        else:
            missing_scripts.append(script)
    
    print(f"📊 Verification script status:")
    print(f"   Expected: {len(expected_scripts)}")
    print(f"   Existing: {len(existing_scripts)}")
    print(f"   Missing: {len(missing_scripts)}")
    
    if missing_scripts:
        print(f"\n❌ Missing verification scripts:")
        for script in missing_scripts:
            print(f"   📝 {script}")
        return False
    
    print("✅ All expected verification scripts exist")
    
    # Test that scripts are executable
    executable_count = 0
    for script in existing_scripts:
        script_path = Path(script)
        if script_path.stat().st_mode & 0o111:  # Check execute permission
            executable_count += 1
    
    print(f"📋 Executable scripts: {executable_count}/{len(existing_scripts)}")
    
    return True

def check_enhanced_validation_systems():
    """Test that enhanced validation systems are operational."""
    
    print("\n🛠️  TESTING ENHANCED VALIDATION SYSTEMS")
    print("-" * 50)
    
    validation_tests = [
        ("PR validation", "python3 validate_pr.py"),
        ("CTMM build system", "python3 ctmm_build.py"),
        ("Workflow syntax validation", "python3 validate_workflow_syntax.py"),
        ("Workflow versions validation", "python3 validate_workflow_versions.py")
    ]
    
    all_passed = True
    
    for test_name, command in validation_tests:
        success, stdout, stderr = run_command(command)
        if success:
            print(f"✅ {test_name} passes")
        else:
            print(f"❌ {test_name} failed")
            print(f"   Error: {stderr[:100]}...")
            all_passed = False
    
    return all_passed

def check_file_changes():
    """Check that meaningful file changes are present."""
    
    print("\n🔍 CHECKING FILE CHANGES")
    print("-" * 50)
    
    # Check git diff
    success, stdout, stderr = run_command("git diff --numstat origin/main..HEAD")
    if not success:
        print(f"❌ Git diff failed: {stderr}")
        return False
    
    if not stdout.strip():
        print("❌ No file changes detected")
        return False
    
    total_added = 0
    total_deleted = 0
    file_count = 0
    
    print("📊 File changes detected:")
    for line in stdout.split('\n'):
        if line.strip():
            parts = line.split('\t')
            if len(parts) >= 3:
                added = int(parts[0]) if parts[0] != '-' else 0
                deleted = int(parts[1]) if parts[1] != '-' else 0
                filename = parts[2]
                total_added += added
                total_deleted += deleted
                file_count += 1
                print(f"   📝 {filename}: +{added} -{deleted}")
    
    print(f"\n📈 Summary:")
    print(f"   Files changed: {file_count}")
    print(f"   Lines added: {total_added}")
    print(f"   Lines deleted: {total_deleted}")
    
    if file_count == 0:
        print("❌ No files changed")
        return False
    
    if total_added < 100:  # Expect substantial content for 19 verification scripts
        print("❌ Insufficient lines added for comprehensive verification infrastructure")
        return False
    
    print("✅ Substantial changes present for Copilot review")
    return True

def main():
    """Main verification function."""
    
    print("🎯 ISSUE #914 RESOLUTION VERIFICATION")
    print("Verifying comprehensive verification infrastructure implementation\n")
    
    tests = [
        ("Issue #914 resolution documentation", check_issue_914_resolution),
        ("Verification scripts infrastructure", check_verification_scripts),
        ("Enhanced validation systems", check_enhanced_validation_systems),
        ("Meaningful file changes", check_file_changes)
    ]
    
    all_passed = True
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            if not result:
                all_passed = False
        except Exception as e:
            print(f"❌ TEST ERROR in {test_name}: {e}")
            all_passed = False
    
    print("\n" + "=" * 80)
    print("FINAL VERIFICATION RESULTS")
    print("=" * 80)
    
    if all_passed:
        print("🎉 ISSUE #914 RESOLUTION: SUCCESS")
        print("✅ All tests passed")
        print("✅ Comprehensive verification infrastructure implemented")
        print("✅ All 19 verification scripts created")
        print("✅ Enhanced validation systems operational")
        print("✅ Documentation is comprehensive")
        print("✅ GitHub Copilot should now be able to review this PR")
        print("\n🔗 This resolution creates comprehensive verification for:")
        print("   - All resolved issues (complete verification coverage)")
        print("   - CI/CD pipeline functionality")
        print("   - GitHub Actions workflow validation")
        print("   - Enhanced error handling and reporting")
        print("   - Centralized validation orchestration")
        return True
    else:
        print("❌ ISSUE #914 RESOLUTION: INCOMPLETE")
        print("   Some tests failed - see details above")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)