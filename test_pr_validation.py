#!/usr/bin/env python3
"""
Test script to validate the PR validation system works correctly.
"""

import os
import subprocess
import tempfile
import sys

def run_command(cmd):
    """Run a command and return success status and output."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def test_validation_script():
    """Test that the validation script works."""
    print("🧪 Testing PR validation script...")

    # Test help command
    success, stdout, stderr = run_command("python3 validate_pr.py --help")
    if not success:
        print(f"❌ Help command failed: {stderr}")
        return False

    if "Validate PR content" not in stdout:
        print("❌ Help text doesn't contain expected content")
        return False

    print("✅ Help command works")

    # Test with skip-build flag (should work even without LaTeX)
    success, stdout, stderr = run_command("python3 validate_pr.py --skip-build")
    if not success:
        print(f"⚠️  Validation script failed (expected if no changes): {stderr}")
    else:
        print("✅ Validation script runs successfully")

    return True

def test_makefile_commands():
    """Test that relevant Makefile commands work."""
    print("\n🧪 Testing Makefile commands...")

    # Test check command
    success, stdout, stderr = run_command("make check")
    if not success:
        print(f"❌ 'make check' failed: {stderr}")
        return False

    print("✅ 'make check' works")

    # Test help command
    success, stdout, stderr = run_command("make help")
    if not success:
        print(f"❌ 'make help' failed: {stderr}")
        return False

    if "validate-pr" not in stdout:
        print("❌ 'make help' doesn't mention validate-pr")
        return False

    print("✅ 'make help' includes validate-pr")

    return True

def test_file_existence():
    """Test that all created files exist and have content."""
    print("\n🧪 Testing file existence...")

    files_to_check = [
        ".github/pull_request_template.md",
        ".github/workflows/pr-validation.yml",
        "validate_pr.py"
    ]

    for file_path in files_to_check:
        if not os.path.exists(file_path):
            print(f"❌ Required file missing: {file_path}")
            return False

        with open(file_path, 'r') as f:
            content = f.read()
            if len(content.strip()) < 10:
                print(f"❌ File appears to be empty: {file_path}")
                return False

    print("✅ All required files exist and have content")
    return True

def main():
    """Run all tests."""
    print("🚀 CTMM PR Validation System Test")
    print("=" * 50)

    all_tests_passed = True

    if not test_file_existence():
        all_tests_passed = False

    if not test_validation_script():
        all_tests_passed = False

    if not test_makefile_commands():
        all_tests_passed = False

    print("\n" + "=" * 50)
    if all_tests_passed:
        print("🎉 All tests passed! PR validation system is working correctly.")
        sys.exit(0)
    else:
        print("❌ Some tests failed. Please check the output above.")
        sys.exit(1)

if __name__ == "__main__":
    main()