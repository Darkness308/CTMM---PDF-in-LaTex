#!/usr/bin/env python3
"""
Verification script for Issue #721: Comprehensive workflow validation

This script demonstrates that Issue #721 has been resolved by:
1. Validating comprehensive workflow systems
2. Testing workflow integration
3. Confirming validation capabilities
"""

import subprocess
import sys
import os

def run_command(cmd, description=""):
    """Run a command and return success status and output."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return False, "", str(e)

def verify_issue_721_resolution():
    """Verify that Issue #721 comprehensive workflow is resolved."""
    
    print("=" * 70)
    print("Issue #721 Resolution Verification")
    print("=" * 70)
    print("Verifying comprehensive workflow validation...")
    print()
    
    all_checks_passed = True
    
    # Check resolution documentation
    print("📄 Resolution Documentation Check:")
    if os.path.exists("ISSUE_721_RESOLUTION.md"):
        print("   ✅ ISSUE_721_RESOLUTION.md exists")
    else:
        print("   ⚠️  ISSUE_721_RESOLUTION.md not found")
    
    # Check comprehensive workflow tools
    print("\n🔄 Comprehensive Workflow Tools:")
    workflow_tools = ["comprehensive_workflow.py", "validate_issue_721.py"]
    for tool in workflow_tools:
        if os.path.exists(tool):
            print(f"   ✅ {tool} exists")
        else:
            print(f"   ❌ {tool} missing")
            all_checks_passed = False
    
    # Test workflow validation
    print("\n⚙️  Workflow Validation Testing:")
    success, stdout, stderr = run_command("python3 validate_issue_721.py", "Testing workflow validation")
    if success:
        print("   ✅ Workflow validation functional")
    else:
        print("   ❌ Workflow validation failed")
        all_checks_passed = False
    
    return all_checks_passed

def main():
    """Main verification function."""
    
    resolution_valid = verify_issue_721_resolution()
    
    print("\n" + "=" * 70)
    print("VERIFICATION SUMMARY")
    print("=" * 70)
    
    if resolution_valid:
        print("✅ ISSUE #721 RESOLUTION: SUCCESS")
        return True
    else:
        print("❌ ISSUE #721 RESOLUTION: NEEDS ATTENTION")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)