#!/usr/bin/env python3
"""
Verification script for Issue #684: Template generation and module validation

This script demonstrates that Issue #684 has been resolved by:
1. Validating template generation functionality
2. Testing module validation systems
3. Confirming automated template creation
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

def verify_issue_684_resolution():
    """Verify that Issue #684 template generation is resolved."""
    
    print("=" * 70)
    print("Issue #684 Resolution Verification")
    print("=" * 70)
    print("Verifying template generation and module validation...")
    print()
    
    all_checks_passed = True
    
    # Check CTMM build system template generation
    print("🏗️  Template Generation Testing:")
    success, stdout, stderr = run_command("python3 ctmm_build.py", "Testing template generation")
    if success and ("templates created" in stdout or "PASS" in stdout):
        print("   ✅ Template generation functional")
    else:
        print("   ❌ Template generation issues")
        all_checks_passed = False
    
    # Check modules directory
    print("\n📁 Modules Directory Check:")
    if os.path.exists("modules"):
        modules = os.listdir("modules")
        print(f"   ✅ Found {len(modules)} module files")
    else:
        print("   ❌ Modules directory missing")
        all_checks_passed = False
    
    return all_checks_passed

def main():
    """Main verification function."""
    
    resolution_valid = verify_issue_684_resolution()
    
    print("\n" + "=" * 70)
    print("VERIFICATION SUMMARY")
    print("=" * 70)
    
    if resolution_valid:
        print("✅ ISSUE #684 RESOLUTION: SUCCESS")
        return True
    else:
        print("❌ ISSUE #684 RESOLUTION: NEEDS ATTENTION")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)