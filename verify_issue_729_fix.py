#!/usr/bin/env python3
"""
Verification script for Issue #729: Integration testing infrastructure

This script demonstrates that Issue #729 has been resolved by:
1. Validating integration testing capabilities
2. Testing test infrastructure
3. Confirming testing framework functionality
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

def verify_issue_729_resolution():
    """Verify that Issue #729 integration testing is resolved."""
    
    print("=" * 70)
    print("Issue #729 Resolution Verification")
    print("=" * 70)
    print("Verifying integration testing infrastructure...")
    print()
    
    all_checks_passed = True
    
    # Check integration test files
    print("🧪 Integration Test Files Check:")
    test_files = ["test_integration.py", "test_ctmm_build.py"]
    for test_file in test_files:
        if os.path.exists(test_file):
            print(f"   ✅ {test_file} exists")
        else:
            print(f"   ❌ {test_file} missing")
            all_checks_passed = False
    
    # Test integration testing
    print("\n⚙️  Integration Testing:")
    success, stdout, stderr = run_command("python3 test_integration.py", "Running integration tests")
    if success:
        print("   ✅ Integration tests pass")
    else:
        print("   ❌ Integration tests failed")
        all_checks_passed = False
    
    return all_checks_passed

def main():
    """Main verification function."""
    
    resolution_valid = verify_issue_729_resolution()
    
    print("\n" + "=" * 70)
    print("VERIFICATION SUMMARY")
    print("=" * 70)
    
    if resolution_valid:
        print("✅ ISSUE #729 RESOLUTION: SUCCESS")
        return True
    else:
        print("❌ ISSUE #729 RESOLUTION: NEEDS ATTENTION")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)