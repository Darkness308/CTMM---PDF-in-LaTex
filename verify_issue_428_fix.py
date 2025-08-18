#!/usr/bin/env python3
"""
Verification script for Issue #428: Version pinning and dependencies validation

This script demonstrates that Issue #428 has been resolved by:
1. Validating that version pinning is properly implemented
2. Testing dependency management systems
3. Confirming build system stability
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

def verify_issue_428_resolution():
    """Verify that Issue #428 version pinning is resolved."""
    
    print("=" * 70)
    print("Issue #428 Resolution Verification")
    print("=" * 70)
    print("Verifying version pinning and dependency management...")
    print()
    
    all_checks_passed = True
    
    # 1. Check resolution documentation
    print("📄 Resolution Documentation Check:")
    if os.path.exists("ISSUE_428_RESOLUTION.md"):
        print("   ✅ ISSUE_428_RESOLUTION.md exists")
        with open("ISSUE_428_RESOLUTION.md", 'r') as f:
            content = f.read()
            if len(content) > 1000:
                print(f"   ✅ Documentation is substantial ({len(content)} characters)")
            else:
                print(f"   ❌ Documentation is too brief ({len(content)} characters)")
                all_checks_passed = False
    else:
        print("   ⚠️  ISSUE_428_RESOLUTION.md not found (may be addressed in other documentation)")
    
    # 2. Check version pinning in GitHub Actions
    print("\n⚙️  GitHub Actions Version Pinning:")
    success, stdout, stderr = run_command("python3 validate_workflow_versions.py", "Checking workflow versions")
    if success and ("PASS" in stdout or "SUCCESS" in stdout):
        print("   ✅ GitHub Actions use pinned versions")
    else:
        print("   ❌ GitHub Actions version pinning issues detected")
        all_checks_passed = False
    
    # 3. Check dependency management
    print("\n📦 Dependency Management:")
    
    # Check for Python dependencies
    if os.path.exists("requirements.txt"):
        print("   ✅ requirements.txt exists for Python dependencies")
    else:
        print("   ⚠️  No requirements.txt found (dependencies managed via other means)")
    
    # Check ctmm_build.py dependencies
    success, stdout, stderr = run_command("python3 ctmm_build.py", "Testing build system dependencies")
    if success:
        print("   ✅ CTMM build system dependencies satisfied")
    else:
        print("   ❌ CTMM build system dependency issues")
        all_checks_passed = False
    
    # 4. Check LaTeX dependencies
    print("\n📝 LaTeX Dependencies:")
    success, stdout, stderr = run_command("python3 latex_validator.py --help", "Testing LaTeX validator")
    if success or "usage:" in stderr:
        print("   ✅ LaTeX validation tools functional")
    else:
        print("   ❌ LaTeX dependency issues")
        all_checks_passed = False
    
    return all_checks_passed

def main():
    """Main verification function."""
    
    print("🎯 ISSUE #428 VERIFICATION")
    print("Verifying version pinning and dependency management")
    print()
    
    resolution_valid = verify_issue_428_resolution()
    
    print("\n" + "=" * 70)
    print("VERIFICATION SUMMARY")
    print("=" * 70)
    
    if resolution_valid:
        print("✅ ISSUE #428 RESOLUTION: SUCCESS")
        print("✅ Version pinning implemented correctly")
        print("✅ Dependencies properly managed")
        print("✅ Build system stable")
        return True
    else:
        print("❌ ISSUE #428 RESOLUTION: NEEDS ATTENTION")
        print("   Some validation checks failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)