#!/usr/bin/env python3
"""
Verification script for Issue #614: Build system improvements

This script demonstrates that Issue #614 has been resolved by:
1. Validating build system enhancements
2. Testing improved build processes
3. Confirming build reliability and robustness
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

def verify_issue_614_resolution():
    """Verify that Issue #614 build system improvements are resolved."""
    
    print("=" * 70)
    print("Issue #614 Resolution Verification")
    print("=" * 70)
    print("Verifying build system improvements...")
    print()
    
    all_checks_passed = True
    
    # 1. Check resolution documentation
    print("📄 Resolution Documentation Check:")
    if os.path.exists("ISSUE_614_RESOLUTION.md"):
        print("   ✅ ISSUE_614_RESOLUTION.md exists")
    else:
        print("   ⚠️  ISSUE_614_RESOLUTION.md not found")
    
    # 2. Test CTMM build system
    print("\n🏗️  CTMM Build System Testing:")
    success, stdout, stderr = run_command("python3 ctmm_build.py", "Testing CTMM build")
    if success and ("PASS" in stdout or "✓" in stdout):
        print("   ✅ CTMM build system passes")
    else:
        print("   ❌ CTMM build system issues")
        all_checks_passed = False
    
    # 3. Test build system components
    print("\n⚙️  Build Components Testing:")
    components = ["build_system.py", "ctmm_unified_tool.py"]
    for component in components:
        if os.path.exists(component):
            print(f"   ✅ {component} exists")
        else:
            print(f"   ❌ {component} missing")
            all_checks_passed = False
    
    # 4. Test Makefile functionality
    print("\n📋 Makefile Testing:")
    success, stdout, stderr = run_command("make check", "Testing make check")
    if success:
        print("   ✅ Make check passes")
    else:
        print("   ❌ Make check failed")
        all_checks_passed = False
    
    return all_checks_passed

def main():
    """Main verification function."""
    
    resolution_valid = verify_issue_614_resolution()
    
    print("\n" + "=" * 70)
    print("VERIFICATION SUMMARY")
    print("=" * 70)
    
    if resolution_valid:
        print("✅ ISSUE #614 RESOLUTION: SUCCESS")
        return True
    else:
        print("❌ ISSUE #614 RESOLUTION: NEEDS ATTENTION")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)