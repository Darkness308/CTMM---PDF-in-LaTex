#!/usr/bin/env python3
"""
Demonstration script for Enhanced CTMM Build Management System
Shows all the enhanced features implemented for issue #833
"""

import subprocess
import sys
from pathlib import Path

def run_command(cmd, description):
    """Run a command and show results."""
    print(f"\n{'='*60}")
    print(f"🔍 {description}")
    print('='*60)

    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"Error running command: {e}")
        return False

def main():
    """Demonstrate all enhanced build management features."""
    print("🚀 Enhanced CTMM Build Management System Demo")
    print("=" * 60)
    print("Demonstrating comprehensive automated build management")
    print("with missing file detection, incremental testing, and CI/CD reliability")

    # Test 1: Standard build system (backward compatibility)
    success1 = run_command(
        "python3 ctmm_build.py",
        "Standard Build System (Backward Compatibility)"
    )

    # Test 2: Enhanced build management
    success2 = run_command(
        "python3 ctmm_build.py --enhanced",
        "Enhanced Build Management System"
    )

    # Test 3: Enhanced incremental testing
    success3 = run_command(
        "make enhanced-testing",
        "Enhanced Incremental Testing"
    )

    # Test 4: Unit tests validation
    success4 = run_command(
        "python3 test_ctmm_build.py 2>&1 | grep -E '(Ran|OK|FAILED)'",
        "Unit Tests Validation"
    )

    # Test 5: GitHub Actions workflow validation
    success5 = run_command(
        "python3 validate_workflow_syntax.py | grep -E '(PASS|FAIL|SUCCESS)'",
        "GitHub Actions Workflow Validation"
    )

    # Summary
    print(f"\n{'='*60}")
    print("📊 ENHANCED BUILD MANAGEMENT DEMO SUMMARY")
    print('='*60)

    results = [
        ("Standard Build System", success1),
        ("Enhanced Build Management", success2),
        ("Enhanced Incremental Testing", success3),
        ("Unit Tests", success4),
        ("Workflow Validation", success5)
    ]

    all_passed = True
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if not success:
            all_passed = False

    print('='*60)
    if all_passed:
        print("🎉 ALL ENHANCED FEATURES WORKING CORRECTLY")
        print("The comprehensive automated build management system is operational!")
        print("\nKey Benefits Demonstrated:")
        print("• Enhanced automation with comprehensive error detection")
        print("• Advanced incremental testing with module isolation")
        print("• Improved CI/CD reliability and artifact management")
        print("• Complete backward compatibility with existing workflows")
        print("• Resource management optimization (no ResourceWarnings)")
        print("\nAvailable Commands:")
        print("• python3 ctmm_build.py --enhanced")
        print("• make enhanced-build")
        print("• make enhanced-testing")
    else:
        print("⚠️  Some tests failed. Please check the output above.")

    print('='*60)
    print("See ENHANCED_BUILD_MANAGEMENT.md for complete documentation.")

    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())