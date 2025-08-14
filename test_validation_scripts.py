#!/usr/bin/env python3
"""
Test suite for CI validation scripts to ensure they work correctly.
This helps prevent future CI failures by testing the validation logic.
"""

import subprocess
import sys
import tempfile
import os
from pathlib import Path


def test_validation_script():
    """Test that validate_latex_syntax.py works correctly."""
    print("Testing validate_latex_syntax.py...")
    
    try:
        # Test normal case
        result = subprocess.run([
            sys.executable, 'validate_latex_syntax.py'
        ], capture_output=True, text=True, check=False)
        
        if result.returncode == 0:
            print("  ✅ Normal validation passed")
        else:
            print(f"  ❌ Normal validation failed: {result.stderr}")
            return False
            
        # Test missing file case
        with tempfile.TemporaryDirectory() as tmpdir:
            # Change to empty directory
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            
            try:
                result = subprocess.run([
                    sys.executable, 
                    os.path.join(original_cwd, 'validate_latex_syntax.py')
                ], capture_output=True, text=True, check=False)
                
                if result.returncode == 1:
                    print("  ✅ Missing file case handled correctly")
                else:
                    print(f"  ❌ Missing file case not handled: returncode={result.returncode}")
                    return False
                    
            finally:
                os.chdir(original_cwd)
        
        return True
        
    except Exception as e:
        print(f"  ❌ Test failed with exception: {e}")
        return False


def test_ctmm_build_script():
    """Test that ctmm_build.py works correctly."""
    print("Testing ctmm_build.py...")
    
    try:
        # Test normal case
        result = subprocess.run([
            sys.executable, 'ctmm_build.py'
        ], capture_output=True, text=True, check=False)
        
        if result.returncode == 0:
            print("  ✅ Normal build check passed")
        else:
            print(f"  ❌ Normal build check failed: {result.stderr}")
            return False
            
        return True
        
    except Exception as e:
        print(f"  ❌ Test failed with exception: {e}")
        return False


def test_script_imports():
    """Test that all required modules can be imported."""
    print("Testing script imports...")
    
    try:
        # Test validate_latex_syntax imports
        import validate_latex_syntax
        print("  ✅ validate_latex_syntax imports successfully")
        
        # Test ctmm_build imports  
        import ctmm_build
        print("  ✅ ctmm_build imports successfully")
        
        # Test required dependencies
        import chardet
        print("  ✅ chardet dependency available")
        
        return True
        
    except ImportError as e:
        print(f"  ❌ Import failed: {e}")
        return False
    except Exception as e:
        print(f"  ❌ Test failed with exception: {e}")
        return False


def main():
    """Run all tests."""
    print("="*60)
    print("CI VALIDATION SCRIPTS TEST SUITE")
    print("="*60)
    
    tests = [
        test_script_imports,
        test_validation_script,
        test_ctmm_build_script,
    ]
    
    passed = 0
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                print(f"❌ {test.__name__} failed")
        except Exception as e:
            print(f"❌ {test.__name__} failed with exception: {e}")
    
    print("\n" + "="*60)
    print(f"TEST RESULTS: {passed}/{len(tests)} tests passed")
    print("="*60)
    
    if passed == len(tests):
        print("✅ All tests passed! CI validation scripts should work correctly.")
        return 0
    else:
        print("❌ Some tests failed. CI validation may have issues.")
        return 1


if __name__ == "__main__":
    sys.exit(main())