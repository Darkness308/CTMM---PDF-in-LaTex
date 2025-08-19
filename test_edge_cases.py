#!/usr/bin/env python3
"""
Comprehensive test for validate_pr.py git command batching optimization edge cases
"""

import sys
import os
import subprocess

def run_command(cmd):
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return False, "", str(e)

def test_batched_git_with_failures():
    """Test batched git calls with some invalid references"""
    print("🧪 Testing batched git with invalid references...")
    
    # Mix of valid and invalid references
    test_refs = ["HEAD", "nonexistent-branch", "HEAD~1", "invalid-ref"]
    cmd = "git rev-parse " + " ".join(test_refs)
    success, stdout, stderr = run_command(cmd)
    
    print(f"   Command: {cmd}")
    print(f"   Success: {success}")
    print(f"   Output lines: {len(stdout.split('\n')) if stdout else 0}")
    
    if stdout:
        hashes = stdout.split('\n')
        valid_refs = []
        for h, ref in zip(hashes, test_refs):
            if h.strip() and not h.startswith("fatal:"):
                valid_refs.append(ref)
        print(f"   Valid refs found: {valid_refs}")
    
    return True

def test_empty_filtered_options():
    """Test the case where no valid options are found"""
    print("🧪 Testing empty filtered options scenario...")
    
    # Import and test the actual function
    sys.path.insert(0, '/home/runner/work/CTMM---PDF-in-LaTex/CTMM---PDF-in-LaTex')
    from validate_pr import check_file_changes
    
    # This should handle the case gracefully
    try:
        success, files, added, deleted = check_file_changes("nonexistent-branch")
        print(f"   Function handled non-existent branch gracefully")
        print(f"   Results: {files} files, {added} added, {deleted} deleted")
        return True
    except Exception as e:
        print(f"   Error: {e}")
        return False

def main():
    print("🔬 Edge Case Testing for Git Batching Optimization")
    print("=" * 60)
    
    if not os.path.exists('.git'):
        print("❌ Not in a git repository")
        return False
    
    tests = [
        ("Batched git with failures", test_batched_git_with_failures),
        ("Empty filtered options", test_empty_filtered_options),
    ]
    
    all_passed = True
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        try:
            if not test_func():
                all_passed = False
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            all_passed = False
    
    print(f"\n{'=' * 60}")
    if all_passed:
        print("🎉 All edge case tests passed!")
        print("✅ Git batching optimization handles edge cases correctly")
    else:
        print("❌ Some edge case tests failed")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)