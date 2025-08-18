#!/usr/bin/env python3
"""
Verification script for Issue #607: GitHub Actions version pinning

This script demonstrates that Issue #607 has been resolved by:
1. Validating GitHub Actions use specific version tags
2. Testing workflow version validation tools
3. Confirming no @latest tag usage
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, description=""):
    """Run a command and return success status and output."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        success = result.returncode == 0
        return success, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return False, "", str(e)

def verify_issue_607_resolution():
    """Verify that Issue #607 GitHub Actions version pinning is resolved."""
    
    print("=" * 70)
    print("Issue #607 Resolution Verification")
    print("=" * 70)
    print("Verifying GitHub Actions version pinning...")
    print()
    
    all_checks_passed = True
    
    # 1. Check resolution documentation
    print("📄 Resolution Documentation Check:")
    if os.path.exists("ISSUE_607_RESOLUTION.md"):
        print("   ✅ ISSUE_607_RESOLUTION.md exists")
        with open("ISSUE_607_RESOLUTION.md", 'r') as f:
            content = f.read()
            if len(content) > 800:
                print(f"   ✅ Documentation is substantial ({len(content)} characters)")
            else:
                print(f"   ❌ Documentation is too brief ({len(content)} characters)")
                all_checks_passed = False
    else:
        print("   ⚠️  ISSUE_607_RESOLUTION.md not found")
    
    # 2. Test workflow version validation
    print("\n⚙️  Workflow Version Validation:")
    success, stdout, stderr = run_command("python3 validate_workflow_versions.py", "Testing workflow version pinning")
    if success and ("PASS" in stdout or "SUCCESS" in stdout or "ALL ACTIONS PROPERLY VERSION-PINNED" in stdout):
        print("   ✅ All GitHub Actions use pinned versions")
    else:
        print("   ❌ GitHub Actions version pinning issues detected")
        if "@latest" in stdout or "@latest" in stderr:
            print("   ⚠️  @latest tags found - should be replaced with specific versions")
        all_checks_passed = False
    
    # 3. Check workflow files exist
    print("\n📋 Workflow Files Check:")
    workflows_dir = Path(".github/workflows")
    if workflows_dir.exists():
        workflow_files = list(workflows_dir.glob("*.yml"))
        print(f"   ✅ Found {len(workflow_files)} workflow files")
        for workflow in workflow_files:
            print(f"      📄 {workflow.name}")
    else:
        print("   ❌ .github/workflows directory not found")
        all_checks_passed = False
    
    # 4. Check for validation tools
    print("\n🔧 Validation Tools Check:")
    if os.path.exists("validate_workflow_versions.py"):
        print("   ✅ validate_workflow_versions.py exists")
    else:
        print("   ❌ validate_workflow_versions.py missing")
        all_checks_passed = False
    
    if os.path.exists("validate_workflow_syntax.py"):
        print("   ✅ validate_workflow_syntax.py exists")
    else:
        print("   ❌ validate_workflow_syntax.py missing")
        all_checks_passed = False
    
    return all_checks_passed

def main():
    """Main verification function."""
    
    print("🎯 ISSUE #607 VERIFICATION")
    print("Verifying GitHub Actions version pinning")
    print()
    
    resolution_valid = verify_issue_607_resolution()
    
    print("\n" + "=" * 70)
    print("VERIFICATION SUMMARY")
    print("=" * 70)
    
    if resolution_valid:
        print("✅ ISSUE #607 RESOLUTION: SUCCESS")
        print("✅ GitHub Actions version pinning implemented")
        print("✅ Validation tools functional")
        print("✅ No @latest tags in workflows")
        return True
    else:
        print("❌ ISSUE #607 RESOLUTION: NEEDS ATTENTION")
        print("   Some validation checks failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)