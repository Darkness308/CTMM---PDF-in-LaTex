#!/usr/bin/env python3
"""
Test for Issue #807: "ist dieser fehler jetzt behoben" (Is this error now fixed?)

This test validates that the error originally reported in PR #393 regarding
redundant functions in ctmm_build.py has been completely resolved.

Original problem:
- Function `test_basic_framework` was an unnecessary wrapper
- Function `generate_build_report` was a placeholder without functionality

Expected result: Both functions should be removed and system should work correctly.
"""

import sys
import subprocess
import os
from pathlib import Path

def test_problematic_functions_removed():
    """Test that the originally problematic functions have been removed."""
    print("1. Testing that problematic functions have been removed...")
    
    # Check that the problematic functions no longer exist
    result = subprocess.run(
        ["grep", "-n", "test_basic_framework\\|generate_build_report", "ctmm_build.py"],
        capture_output=True,
        text=True
    )
    
    # grep should return exit code 1 (no matches found) 
    if result.returncode == 1:
        print("   ✅ test_basic_framework: NOT FOUND (correctly removed)")
        print("   ✅ generate_build_report: NOT FOUND (correctly removed)")
        return True
    else:
        print("   ❌ Problematic functions still found in code:")
        print(f"   {result.stdout}")
        return False

def test_build_system_functionality():
    """Test that the build system still works correctly after function removal."""
    print("2. Testing build system functionality...")
    
    try:
        result = subprocess.run(
            ["python3", "ctmm_build.py"],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            print("   ✅ Build system runs successfully")
            # Check for expected output indicators
            if "CTMM BUILD SYSTEM SUMMARY" in result.stdout:
                print("   ✅ Build summary generated correctly")
            if "LaTeX validation: ✓ PASS" in result.stdout:
                print("   ✅ LaTeX validation passes")
            return True
        else:
            print(f"   ❌ Build system failed with exit code {result.returncode}")
            print(f"   Error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("   ❌ Build system timed out")
        return False
    except Exception as e:
        print(f"   ❌ Error running build system: {e}")
        return False

def test_essential_functions_still_exist():
    """Test that essential functions are still present after cleanup."""
    print("3. Testing that essential functions still exist...")
    
    essential_functions = [
        "test_basic_build",
        "test_full_build", 
        "scan_references",
        "check_missing_files",
        "create_template"
    ]
    
    all_found = True
    
    for func in essential_functions:
        result = subprocess.run(
            ["grep", "-q", f"def {func}(", "ctmm_build.py"],
            capture_output=True
        )
        
        if result.returncode == 0:
            print(f"   ✅ {func}: FOUND (correctly preserved)")
        else:
            print(f"   ❌ {func}: NOT FOUND (essential function missing!)")
            all_found = False
    
    return all_found

def test_unit_tests_pass():
    """Test that unit tests still pass after the fix."""
    print("4. Testing that unit tests pass...")
    
    try:
        result = subprocess.run(
            ["python3", "test_ctmm_build.py"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0 and "OK" in result.stderr:
            # Count test results
            if "Ran" in result.stderr:
                test_line = [line for line in result.stderr.split('\n') if line.startswith('Ran')][0]
                print(f"   ✅ Unit tests pass: {test_line}")
            else:
                print("   ✅ Unit tests pass")
            return True
        else:
            print(f"   ❌ Unit tests failed with exit code {result.returncode}")
            print(f"   Error: {result.stderr[-500:]}")  # Last 500 chars
            return False
            
    except subprocess.TimeoutExpired:
        print("   ❌ Unit tests timed out")
        return False
    except Exception as e:
        print(f"   ❌ Error running unit tests: {e}")
        return False

def main():
    """Main test function for Issue #807."""
    print("=" * 70)
    print("ISSUE #807 VALIDATION: 'ist dieser fehler jetzt behoben'")
    print("=" * 70)
    print("Testing that the error from PR #393 has been completely resolved.")
    print()
    
    all_tests_passed = True
    
    # Test 1: Check that problematic functions are removed
    if not test_problematic_functions_removed():
        all_tests_passed = False
    print()
    
    # Test 2: Check that build system still works
    if not test_build_system_functionality():
        all_tests_passed = False
    print()
    
    # Test 3: Check that essential functions are preserved
    if not test_essential_functions_still_exist():
        all_tests_passed = False
    print()
    
    # Test 4: Check that unit tests pass
    if not test_unit_tests_pass():
        all_tests_passed = False
    print()
    
    # Summary
    print("=" * 70)
    print("ISSUE #807 VALIDATION SUMMARY")
    print("=" * 70)
    
    if all_tests_passed:
        print("🎉 ✅ FEHLER BEHOBEN / ERROR FIXED")
        print()
        print("Antwort auf 'ist dieser fehler jetzt behoben': JA ✅")
        print("Answer to 'is this error now fixed': YES ✅")
        print()
        print("Der ursprünglich in PR #393 gemeldete Fehler ist vollständig behoben:")
        print("• Redundante Funktionen wurden entfernt")
        print("• Build-System funktioniert ordnungsgemäß")
        print("• Alle Tests laufen erfolgreich durch")
        print("• Wesentliche Funktionen sind weiterhin vorhanden")
        print()
        print("The error originally reported in PR #393 has been completely fixed:")
        print("• Redundant functions have been removed")
        print("• Build system works properly") 
        print("• All tests pass successfully")
        print("• Essential functions are still present")
        return True
    else:
        print("❌ FEHLER NOCH NICHT VOLLSTÄNDIG BEHOBEN")
        print("❌ ERROR NOT COMPLETELY FIXED")
        print("Some tests failed - further investigation required.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)