#!/usr/bin/env python3
"""
Enhanced verification script for Issue #673: Comprehensive Copilot Review Fix

This script demonstrates that Issue #673 has been resolved by providing:
1. Infrastructure upgrades (GitHub Actions LaTeX action upgrade)
2. Comprehensive verification system
3. Meaningful changes for Copilot to review
4. Complete validation of all repository systems

Addresses the root cause from PR #653 where merge conflicts prevented Copilot review.
"""

import subprocess
import sys
import json
import os
from pathlib import Path

def run_command(cmd, description="", capture_output=True):
    """Run a command and return success status and output."""
    try:
        if description:
            print(f"🔧 {description}")
        
        result = subprocess.run(cmd, shell=True, capture_output=capture_output, text=True)
        
        if result.returncode == 0:
            if description:
                print(f"✅ SUCCESS: {description}")
            return True, result.stdout.strip() if capture_output else ""
        else:
            if description:
                print(f"❌ FAILED: {description}")
                if capture_output and result.stderr:
                    print(f"   Error: {result.stderr.strip()}")
            return False, result.stderr.strip() if capture_output else ""
    except Exception as e:
        if description:
            print(f"❌ ERROR: {description} - {e}")
        return False, str(e)

def check_repository_health():
    """Verify repository is in good state for Copilot review."""
    print("\n📋 REPOSITORY HEALTH CHECK")
    print("-" * 50)
    
    # Check git status
    success, output = run_command("git status --porcelain", "Check repository cleanliness")
    if not success:
        return False
    
    if output.strip():
        print(f"📝 Uncommitted changes detected: {len(output.strip().split())} items")
        print("   This is expected for a work-in-progress PR")
    else:
        print("📋 Repository is clean (no uncommitted changes)")
    
    # Check for meaningful changes vs base branch
    # Try different base options in order of preference
    base_options = ["origin/main", "main", "HEAD~1", "HEAD^"]
    actual_base = None
    output = ""
    
    for base in base_options:
        success, temp_output = run_command(f"git diff {base} --numstat 2>/dev/null", 
                                         f"Check changes vs {base}")
        if success and temp_output.strip():
            actual_base = base
            output = temp_output
            print(f"📊 Comparing against {base}")
            break
        elif success:
            print(f"📋 No changes found vs {base}")
    
    if not actual_base:
        print("⚠️  Could not find suitable base for comparison, checking working directory...")
        success, output = run_command("git status --porcelain", "Check working directory status")
        if success and output.strip():
            print("📝 Uncommitted changes detected in working directory")
            return True
        else:
            print("📋 No changes detected")
            return False
    
    if output.strip():
        lines = output.strip().split('\n')
        total_files = len([line for line in lines if line.strip() and '\t' in line])
        total_added = 0
        total_deleted = 0
        
        for line in lines:
            if line.strip() and '\t' in line:
                parts = line.split('\t')
                if len(parts) >= 2:
                    try:
                        added = int(parts[0]) if parts[0].isdigit() else 0
                        deleted = int(parts[1]) if parts[1].isdigit() else 0
                        total_added += added
                        total_deleted += deleted
                    except (ValueError, IndexError):
                        continue
        
        print(f"📊 Change Summary:")
        print(f"   📁 Files changed: {total_files}")
        print(f"   ➕ Lines added: {total_added}")
        print(f"   ➖ Lines deleted: {total_deleted}")
        
        if total_files > 0 and total_added > 0:
            print("✅ MEANINGFUL CHANGES: Copilot can review these changes")
            return True
        else:
            print("❌ NO SUBSTANTIAL CHANGES: Copilot may not be able to review")
            return False
    else:
        print("📋 No changes detected")
        return False

def validate_github_actions_upgrade():
    """Verify that the GitHub Actions LaTeX action has been upgraded."""
    print("\n🚀 GITHUB ACTIONS UPGRADE VERIFICATION")
    print("-" * 50)
    
    workflow_file = Path(".github/workflows/latex-build.yml")
    if not workflow_file.exists():
        print("❌ LaTeX build workflow file not found")
        return False
    
    content = workflow_file.read_text()
    
    # Check for the upgraded action
    if "dante-ev/latex-action@v2" in content:
        print("✅ UPGRADE CONFIRMED: dante-ev/latex-action@v2 detected")
        print("   Enhanced LaTeX compilation capabilities active")
        
        # Extract the full action configuration
        lines = content.split('\n')
        in_latex_step = False
        for i, line in enumerate(lines):
            if "dante-ev/latex-action@v2" in line:
                print(f"   📄 Configuration at line {i+1}:")
                # Show the action and its parameters
                for j in range(max(0, i-2), min(len(lines), i+8)):
                    if j == i:
                        print(f"   ➤  {lines[j].strip()}")
                    else:
                        print(f"      {lines[j].strip()}")
                break
        
        return True
    elif "dante-ev/latex-action@v0.2" in content:
        print("❌ OLD VERSION: dante-ev/latex-action@v0.2 detected")
        print("   Upgrade to v2 required for enhanced capabilities")
        return False
    elif "dante-ev/latex-action@latest" in content:
        print("⚠️  UNPINNED VERSION: @latest detected")
        print("   Consider pinning to specific version for reproducibility")
        return True
    else:
        print("❓ UNKNOWN STATE: dante-ev/latex-action not found")
        return False

def validate_verification_infrastructure():
    """Test that all verification scripts and systems work correctly."""
    print("\n🛠️  VERIFICATION INFRASTRUCTURE TEST")
    print("-" * 50)
    
    # Test core validation scripts
    scripts_to_test = [
        ("validate_pr.py", "PR validation system"),
        ("ctmm_build.py", "CTMM build system"),
        ("validate_workflow_syntax.py", "Workflow syntax validation"),
        ("validate_workflow_versions.py", "Workflow version validation")
    ]
    
    all_passed = True
    for script, description in scripts_to_test:
        if Path(script).exists():
            success, output = run_command(f"python3 {script}", f"Test {description}")
            if not success:
                all_passed = False
                print(f"   ⚠️  {script} reported issues")
        else:
            print(f"❌ MISSING: {script} not found")
            all_passed = False
    
    return all_passed

def check_issue_documentation():
    """Verify that Issue #673 documentation exists and is complete."""
    print("\n📚 ISSUE DOCUMENTATION VERIFICATION")
    print("-" * 50)
    
    doc_file = Path("ISSUE_673_RESOLUTION.md")
    if not doc_file.exists():
        print("❌ MISSING: ISSUE_673_RESOLUTION.md not found")
        return False
    
    content = doc_file.read_text()
    
    # Check for required sections
    required_sections = [
        "Problem Statement",
        "Root Cause Analysis", 
        "Solution Implemented",
        "Results and Validation",
        "Copilot Review Status"
    ]
    
    missing_sections = []
    for section in required_sections:
        if section not in content:
            missing_sections.append(section)
    
    if missing_sections:
        print(f"❌ INCOMPLETE: Missing sections: {', '.join(missing_sections)}")
        return False
    
    # Check for issue references
    if "#673" in content:
        print("✅ DOCUMENTATION COMPLETE: ISSUE_673_RESOLUTION.md found with all required sections")
        print(f"   📖 Document size: {len(content)} characters")
        
        # Count lines for different sections
        lines = content.split('\n')
        print(f"   📄 Document structure: {len(lines)} lines")
        
        return True
    else:
        print("❌ INCORRECT REFERENCE: Document doesn't reference Issue #673")
        return False

def comprehensive_system_test():
    """Run a comprehensive test of all systems to ensure everything works."""
    print("\n🎯 COMPREHENSIVE SYSTEM TEST")
    print("-" * 50)
    
    tests = [
        ("Git repository health", check_repository_health),
        ("GitHub Actions upgrade", validate_github_actions_upgrade), 
        ("Verification infrastructure", validate_verification_infrastructure),
        ("Issue documentation", check_issue_documentation)
    ]
    
    results = {}
    for test_name, test_func in tests:
        print(f"\n🧪 Testing: {test_name}")
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ TEST ERROR: {e}")
            results[test_name] = False
    
    return results

def main():
    """Main verification function for Issue #673."""
    
    print("="*70)
    print("ISSUE #673 COMPREHENSIVE VERIFICATION")
    print("Enhanced Copilot Review Infrastructure")
    print("="*70)
    
    # Change to repository directory
    repo_path = Path(__file__).parent
    os.chdir(repo_path)
    
    # Run comprehensive system test
    test_results = comprehensive_system_test()
    
    # Generate final report
    print("\n" + "="*70)
    print("VERIFICATION SUMMARY")
    print("="*70)
    
    all_passed = True
    for test_name, result in test_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if not result:
            all_passed = False
    
    print(f"\n📋 OVERALL STATUS: {'✅ ALL SYSTEMS OPERATIONAL' if all_passed else '❌ ISSUES DETECTED'}")
    
    if all_passed:
        print("\n🎉 ISSUE #673 SUCCESSFULLY RESOLVED")
        print("\n📝 Summary of Achievements:")
        print("   ✅ Infrastructure upgraded (GitHub Actions LaTeX action)")
        print("   ✅ Comprehensive verification system implemented")
        print("   ✅ Complete documentation provided")
        print("   ✅ Meaningful changes created for Copilot review")
        print("   ✅ All validation systems operational")
        
        print("\n🤖 COPILOT REVIEW STATUS:")
        print("   🎯 READY FOR REVIEW")
        print("   📊 Meaningful changes detected")
        print("   🛠️  All systems validated")
        print("   📚 Complete documentation available")
        
        print("\n🚀 Next Steps:")
        print("   1. Submit PR for Copilot review")
        print("   2. Verify Copilot can successfully analyze changes")
        print("   3. Apply lessons learned to future PRs")
        
    else:
        print("\n⚠️  RESOLUTION INCOMPLETE")
        print("   Please address the failed tests above")
        print("   Re-run this script to verify fixes")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)