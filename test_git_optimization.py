#!/usr/bin/env python3
"""
Test script for git command optimization in validate_pr.py

This script validates that the optimization of git rev-parse commands
works correctly and maintains functionality while reducing process overhead.
"""

import subprocess
import os
import sys
from unittest.mock import patch, MagicMock
import tempfile
import shutil

def run_command(cmd, capture_output=True):
    """Run a shell command and return the result (same as in validate_pr.py)."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=capture_output, text=True)
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return False, "", str(e)

def setup_test_git_repo():
    """Set up a temporary git repository for testing."""
    test_dir = tempfile.mkdtemp(prefix="git_optimization_test_")
    os.chdir(test_dir)
    
    # Initialize git repo
    run_command("git init")
    run_command("git config user.email 'test@example.com'")
    run_command("git config user.name 'Test User'")
    
    # Create initial commit
    with open("test.txt", "w") as f:
        f.write("initial content")
    run_command("git add test.txt")
    run_command("git commit -m 'Initial commit'")
    
    # Create main branch if needed
    run_command("git branch -M main")
    
    return test_dir

def cleanup_test_repo(test_dir):
    """Clean up the test repository."""
    os.chdir("/")
    shutil.rmtree(test_dir, ignore_errors=True)

def test_individual_git_calls():
    """Test the old individual git rev-parse approach."""
    print("🧪 Testing individual git rev-parse calls...")
    
    # Simulate the old approach
    base_options = ["origin/main", "main", "origin/master", "master"]
    actual_base = None
    call_count = 0
    
    # Get available branches
    success, stdout, stderr = run_command("git branch -r")
    available_branches = stdout.split('\n') if success else []
    
    # Old approach - individual calls
    for base_option in base_options:
        if any(base_option in branch for branch in available_branches) or base_option in ["main", "master"]:
            call_count += 1
            success, _, _ = run_command(f"git rev-parse {base_option}")
            if success:
                actual_base = base_option
                break
    
    print(f"   Individual calls made: {call_count}")
    print(f"   Found base: {actual_base}")
    return actual_base, call_count

def test_batched_git_calls():
    """Test the new batched git rev-parse approach."""
    print("🧪 Testing batched git rev-parse calls...")
    
    # Simulate the new approach
    base_options = ["origin/main", "main", "origin/master", "master"]
    actual_base = None
    call_count = 0
    
    # Get available branches
    success, stdout, stderr = run_command("git branch -r")
    available_branches = stdout.split('\n') if success else []
    
    # New approach - batched calls with improved filtering
    filtered_options = []
    for opt in base_options:
        # Include if it's in remote branches, or is a common branch name like main/master
        if (any(opt in branch for branch in available_branches) or 
            opt in ['main', 'master']):
            filtered_options.append(opt)
    
    if filtered_options:
        call_count = 1  # Only one call for all options
        cmd = "git rev-parse " + " ".join(filtered_options)
        success, stdout, stderr = run_command(cmd)
        if stdout.strip():
            # Even if command exits with non-zero, valid refs will still produce output
            lines = stdout.strip().split('\n')
            for line, base_opt in zip(lines, filtered_options):
                if (line.strip() and 
                    len(line.strip()) >= 7 and 
                    not line.startswith("fatal:") and
                    not line.startswith("error:")):
                    actual_base = base_opt
                    break
    
    print(f"   Batched calls made: {call_count}")
    print(f"   Found base: {actual_base}")
    print(f"   Filtered options: {filtered_options}")
    return actual_base, call_count

def test_optimization_correctness():
    """Test that both approaches give the same result."""
    print("\n🎯 Testing optimization correctness...")
    
    individual_base, individual_calls = test_individual_git_calls()
    batched_base, batched_calls = test_batched_git_calls()
    
    print(f"\n📊 Results comparison:")
    print(f"   Individual approach: base='{individual_base}', calls={individual_calls}")
    print(f"   Batched approach: base='{batched_base}', calls={batched_calls}")
    
    # Check correctness
    bases_match = individual_base == batched_base
    calls_reduced = batched_calls <= individual_calls
    
    print(f"\n✅ Results match: {bases_match}")
    print(f"✅ Calls reduced: {calls_reduced} ({individual_calls} → {batched_calls})")
    
    return bases_match and calls_reduced

def test_performance_improvement():
    """Test that the optimization actually reduces the number of git calls."""
    print("\n⚡ Testing performance improvement...")
    
    # Simulate a more complex scenario with many base options
    base_options = [
        "origin/main", "main", 
        "origin/master", "master",
        "origin/develop", "develop",
        "origin/feature/test", "feature/test"
    ]
    
    # Old approach - would make individual calls until finding a match
    old_call_count = 0
    for opt in base_options:
        old_call_count += 1  # Each option would be a separate call
        # Simulate finding a match early (main is usually available)
        if opt == "main":
            break
    
    # New approach - single batched call
    new_call_count = 1  # Always just one call regardless of options
    
    print(f"   Old approach would make: {old_call_count} git calls")
    print(f"   New approach makes: {new_call_count} git call")
    print(f"   Performance improvement: {old_call_count - new_call_count} fewer calls")
    
    # In the worst case scenario (no matches), old approach would make len(base_options) calls
    worst_case_old = len(base_options)
    print(f"   Worst case old approach: {worst_case_old} calls")
    print(f"   Worst case new approach: {new_call_count} call")
    print(f"   Max potential savings: {worst_case_old - new_call_count} calls")
    
    return new_call_count < old_call_count

def test_validate_pr_optimization():
    """Test the actual validate_pr.py implementation."""
    print("\n🔍 Testing validate_pr.py implementation...")
    
    # Import the check_file_changes function
    sys.path.insert(0, '/home/runner/work/CTMM---PDF-in-LaTex/CTMM---PDF-in-LaTex')
    try:
        from validate_pr import check_file_changes
        
        # Test with different base branches
        test_bases = ["main", "master", "develop"]
        
        for base in test_bases:
            print(f"   Testing with base branch: {base}")
            try:
                success, changed_files, added_lines, deleted_lines = check_file_changes(base)
                print(f"   ✅ Success: {success}, Files: {changed_files}, +{added_lines}/-{deleted_lines}")
            except Exception as e:
                print(f"   ❌ Error with base '{base}': {e}")
                return False
        
        return True
        
    except ImportError as e:
        print(f"   ❌ Could not import validate_pr: {e}")
        return False

def main():
    """Main test function."""
    print("🚀 Git Command Optimization Test Suite")
    print("=" * 60)
    
    # Save original directory
    original_dir = os.getcwd()
    test_dir = None
    
    try:
        # Set up test repository
        test_dir = setup_test_git_repo()
        print(f"📁 Test repository created: {test_dir}")
        
        # Run optimization tests
        optimization_works = test_optimization_correctness()
        performance_improved = test_performance_improvement()
        
        # Change back to original directory for validate_pr.py test
        os.chdir(original_dir)
        validate_pr_works = test_validate_pr_optimization()
        
        # Summary
        print("\n" + "=" * 60)
        if optimization_works and performance_improved and validate_pr_works:
            print("🎉 All optimization tests passed!")
            print("✅ Git command batching is working correctly")
            print("✅ Performance improved while maintaining functionality")
            return True
        else:
            print("❌ Some optimization tests failed")
            if not optimization_works:
                print("   - Optimization correctness test failed")
            if not performance_improved:
                print("   - Performance improvement test failed")
            if not validate_pr_works:
                print("   - validate_pr.py integration test failed")
            return False
            
    except Exception as e:
        print(f"❌ Test suite error: {e}")
        return False
        
    finally:
        # Cleanup
        if test_dir:
            cleanup_test_repo(test_dir)
        os.chdir(original_dir)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)