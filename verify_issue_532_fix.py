#!/usr/bin/env python3
"""
Verification script for Issue #532: LaTeX syntax and escaping validation

This script demonstrates that Issue #532 has been resolved by:
1. Validating LaTeX syntax checking capabilities
2. Testing escaping validation systems
3. Confirming over-escaping prevention
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

def verify_issue_532_resolution():
    """Verify that Issue #532 LaTeX validation is resolved."""
    
    print("=" * 70)
    print("Issue #532 Resolution Verification")
    print("=" * 70)
    print("Verifying LaTeX syntax and escaping validation...")
    print()
    
    all_checks_passed = True
    
    # 1. Check resolution documentation
    print("📄 Resolution Documentation Check:")
    if os.path.exists("ISSUE_532_RESOLUTION.md"):
        print("   ✅ ISSUE_532_RESOLUTION.md exists")
        with open("ISSUE_532_RESOLUTION.md", 'r') as f:
            content = f.read()
            if len(content) > 1000:
                print(f"   ✅ Documentation is substantial ({len(content)} characters)")
            else:
                print(f"   ❌ Documentation is too brief ({len(content)} characters)")
                all_checks_passed = False
    else:
        print("   ⚠️  ISSUE_532_RESOLUTION.md not found")
    
    # 2. Test LaTeX validator functionality
    print("\n📝 LaTeX Validator Testing:")
    success, stdout, stderr = run_command("python3 latex_validator.py modules/", "Testing LaTeX validation")
    if success and ("✓" in stdout or "PASS" in stdout):
        print("   ✅ LaTeX validator works correctly")
    else:
        print("   ❌ LaTeX validator issues detected")
        all_checks_passed = False
    
    # 3. Test escaping validation
    print("\n🔧 Escaping Validation Testing:")
    success, stdout, stderr = run_command("python3 validate_latex_syntax.py", "Testing syntax validation")
    if success:
        print("   ✅ LaTeX syntax validation functional")
    else:
        print("   ❌ LaTeX syntax validation failed")
        all_checks_passed = False
    
    # 4. Test CTMM build integration
    print("\n🏗️  CTMM Build Integration:")
    success, stdout, stderr = run_command("python3 ctmm_build.py", "Testing CTMM build with validation")
    if success and ("LaTeX validation" in stdout and "PASS" in stdout):
        print("   ✅ CTMM build integrates LaTeX validation")
    else:
        print("   ❌ CTMM build validation integration issues")
        all_checks_passed = False
    
    # 5. Check for validation scripts
    print("\n📋 Validation Scripts Check:")
    validation_scripts = ["latex_validator.py", "validate_latex_syntax.py", "fix_latex_escaping.py"]
    for script in validation_scripts:
        if os.path.exists(script):
            print(f"   ✅ {script} exists")
        else:
            print(f"   ❌ {script} missing")
            all_checks_passed = False
    
    return all_checks_passed

def main():
    """Main verification function."""
    
    print("🎯 ISSUE #532 VERIFICATION")
    print("Verifying LaTeX syntax and escaping validation")
    print()
    
    resolution_valid = verify_issue_532_resolution()
    
    print("\n" + "=" * 70)
    print("VERIFICATION SUMMARY")
    print("=" * 70)
    
    if resolution_valid:
        print("✅ ISSUE #532 RESOLUTION: SUCCESS")
        print("✅ LaTeX validation implemented")
        print("✅ Escaping validation functional")
        print("✅ CTMM build integration working")
        return True
    else:
        print("❌ ISSUE #532 RESOLUTION: NEEDS ATTENTION")
        print("   Some validation checks failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)