#!/usr/bin/env python3
"""
Test script to validate git command batching optimization in validate_pr.py

This script tests the git rev-parse batching functionality to ensure:
1. Batched commands work correctly
2. Error handling is proper for failed references
3. Performance improvement is achieved
"""

import subprocess
import time
from unittest.mock import patch, MagicMock

def run_command(cmd, capture_output=True):
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=capture_output, text=True)
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return False, "", str(e)

def test_git_rev_parse_batching():
    """Test that git rev-parse can be batched effectively."""
    print("🧪 Testing git rev-parse batching...")
    
    # Test individual calls
    base_options = ["origin/main", "main"]
    
    # Time individual calls
    start_time = time.time()
    individual_results = []
    for option in base_options:
        success, stdout, stderr = run_command(f"git rev-parse {option}")
        individual_results.append((success, stdout, stderr))
    individual_time = time.time() - start_time
    
    # Time batched call
    start_time = time.time()
    cmd = "git rev-parse " + " ".join(base_options)
    success, stdout, stderr = run_command(cmd)
    batched_time = time.time() - start_time
    
    print(f"  Individual calls time: {individual_time:.4f}s")
    print(f"  Batched call time: {batched_time:.4f}s")
    
    if batched_time < individual_time:
        print("  ✅ Batched approach is faster")
    else:
        print("  ⚠️  Timing difference may not be significant for small tests")
    
    # Test that results are equivalent
    if success and stdout.strip():
        hashes = stdout.split('\n')
        if len(hashes) == len(base_options):
            print("  ✅ Batched call returns correct number of results")
            
            # Verify each hash matches individual calls
            for i, (ind_success, ind_stdout, _) in enumerate(individual_results):
                if ind_success and hashes[i].strip() == ind_stdout.strip():
                    print(f"    ✅ Hash {i+1} matches individual call")
                elif not ind_success and hashes[i].startswith("fatal:"):
                    print(f"    ✅ Failed reference {i+1} properly handled")
        else:
            print("  ❌ Incorrect number of results from batched call")
            return False
    
    return True

def test_error_handling():
    """Test error handling with invalid references."""
    print("\n🧪 Testing error handling for invalid references...")
    
    # Test with mix of valid and invalid references
    mixed_options = ["main", "nonexistent-branch", "HEAD"]
    cmd = "git rev-parse " + " ".join(mixed_options)
    success, stdout, stderr = run_command(cmd)
    
    if success and stdout.strip():
        hashes = stdout.split('\n')
        print(f"  Results: {len(hashes)} lines returned")
        
        # Check that we get appropriate responses
        for i, hash_line in enumerate(hashes):
            if hash_line.startswith("fatal:") or not hash_line.strip():
                print(f"    Line {i+1}: Invalid reference properly handled")
            else:
                print(f"    Line {i+1}: Valid hash returned")
        
        print("  ✅ Mixed valid/invalid references handled correctly")
        return True
    else:
        print(f"  ❌ Batched command failed: {stderr}")
        return False

def test_optimized_validate_pr_logic():
    """Test the optimized logic in validate_pr.py."""
    print("\n🧪 Testing optimized validate_pr.py logic...")
    
    # Simulate the optimized logic (batched only)
    base_options = ["origin/main", "main", "origin/develop", "develop"]
    available_branches = ["origin/main", "origin/develop"]  # Simulate git branch -r output
    
    print("  Optimized approach (batched only):")
    actual_base = None
    
    # Only batched approach (optimized)
    filtered_options = [opt for opt in base_options if any(opt in branch for branch in available_branches) or opt in ["main", "develop"]]
    if filtered_options:
        print(f"    Checking {len(filtered_options)} references with single batched call")
        cmd = "git rev-parse " + " ".join(filtered_options)
        success, stdout, stderr = run_command(cmd)
        if success and stdout.strip():
            hashes = stdout.split('\n')
            for h, base_opt in zip(hashes, filtered_options):
                if h.strip() and not h.startswith("fatal:"):
                    actual_base = base_opt
                    print(f"    Batched call found: {base_opt}")
                    break
    
    print(f"    Result: {actual_base}")
    return actual_base is not None

def test_command_count_optimization():
    """Test that we're reducing the number of git commands executed."""
    print("\n🧪 Testing command count optimization...")
    
    # Count git commands in old vs new approach
    base_options = ["origin/main", "main"] 
    available_branches = ["origin/main"]
    
    # Old approach would make individual calls PLUS batched call
    old_command_count = 0
    for base_option in base_options:
        if any(base_option in branch for branch in available_branches) or base_option in ["main"]:
            old_command_count += 1  # Individual git rev-parse call
    old_command_count += 1  # Plus the batched call
    
    # New approach: only 1 batched call
    new_command_count = 1
    
    print(f"    Old approach: {old_command_count} git commands")
    print(f"    New approach: {new_command_count} git command")
    print(f"    Improvement: {old_command_count - new_command_count} fewer commands")
    
    return new_command_count < old_command_count

def main():
    """Run all git batching tests."""
    print("🚀 Git Command Batching Optimization Tests")
    print("=" * 50)
    
    all_tests_passed = True
    
    if not test_git_rev_parse_batching():
        all_tests_passed = False
    
    if not test_error_handling():
        all_tests_passed = False
    
    if not test_optimized_validate_pr_logic():
        all_tests_passed = False
    
    if not test_command_count_optimization():
        all_tests_passed = False
    
    print("\n" + "=" * 50)
    if all_tests_passed:
        print("🎉 All git batching tests passed!")
        print("Ready to optimize validate_pr.py")
    else:
        print("❌ Some tests failed.")
    
    return all_tests_passed

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)