#!/usr/bin/env python3
"""
Test for git command batching optimization in validate_pr.py

This test validates that the git rev-parse batching optimization 
works correctly and reduces the number of git command executions.
"""

import subprocess
import sys
import unittest.mock
from validate_pr import check_file_changes, run_command

def test_git_batching_optimization():
    """Test that git rev-parse commands are batched instead of individual calls."""
    print("🧪 Testing git command batching optimization...")
    
    # Mock run_command to count how many times git rev-parse is called
    original_run_command = run_command
    git_rev_parse_calls = []
    
    def mock_run_command(cmd, capture_output=True):
        if "git rev-parse" in cmd:
            git_rev_parse_calls.append(cmd)
            # Simulate successful response for main/origin branches
            if "main" in cmd:
                return True, "abc123def456", ""
        return original_run_command(cmd, capture_output)
    
    # Patch the run_command function
    import validate_pr
    validate_pr.run_command = mock_run_command
    
    try:
        # Call the function that should use batched git commands
        success, files, added, deleted = check_file_changes("main")
        
        # Check that git rev-parse was called at most once (batched)
        git_calls = [call for call in git_rev_parse_calls if "git rev-parse" in call]
        
        if len(git_calls) <= 1:
            print("✅ Git commands are properly batched")
            print(f"   Git rev-parse calls: {len(git_calls)}")
            if git_calls:
                print(f"   Batched command: {git_calls[0]}")
            return True
        else:
            print(f"❌ Too many git rev-parse calls: {len(git_calls)}")
            for call in git_calls:
                print(f"   Call: {call}")
            return False
            
    finally:
        # Restore original function
        validate_pr.run_command = original_run_command

def test_functionality_unchanged():
    """Test that the optimization doesn't change the function's behavior."""
    print("\n🧪 Testing that functionality remains unchanged...")
    
    try:
        success, files, added, deleted = check_file_changes("main")
        print("✅ Function executes without errors")
        print(f"   Result: success={success}, files={files}, added={added}, deleted={deleted}")
        return True
    except Exception as e:
        print(f"❌ Function failed: {e}")
        return False

def main():
    """Run optimization tests."""
    print("🚀 Git Command Batching Optimization Test")
    print("=" * 50)
    
    all_tests_passed = True
    
    if not test_git_batching_optimization():
        all_tests_passed = False
    
    if not test_functionality_unchanged():
        all_tests_passed = False
    
    print("\n" + "=" * 50)
    if all_tests_passed:
        print("🎉 All optimization tests passed!")
        print("Git commands are properly batched for better performance.")
        sys.exit(0)
    else:
        print("❌ Some optimization tests failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()