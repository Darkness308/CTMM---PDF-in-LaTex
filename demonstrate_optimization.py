#!/usr/bin/env python3
"""
Demonstration script showing the git command optimization in validate_pr.py

This script shows the performance difference between the old individual 
git rev-parse calls vs the new batched approach.
"""

import subprocess
import time
import os
import tempfile
import shutil

def run_command(cmd):
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return False, "", str(e)

def setup_test_repo():
    """Set up a test git repository."""
    test_dir = tempfile.mkdtemp(prefix="optimize_demo_")
    os.chdir(test_dir)
    
    run_command("git init")
    run_command("git config user.email 'test@example.com'")
    run_command("git config user.name 'Test User'")
    
    with open("test.txt", "w") as f:
        f.write("test content")
    run_command("git add test.txt")
    run_command("git commit -m 'Initial commit'")
    run_command("git branch -M main")
    
    return test_dir

def simulate_old_approach():
    """Simulate the old individual git rev-parse approach."""
    base_options = [
        "origin/main", "main", 
        "origin/master", "master",
        "origin/develop", "develop",
        "origin/feature/test", "feature/test"
    ]
    
    start_time = time.time()
    call_count = 0
    actual_base = None
    
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
    
    end_time = time.time()
    return actual_base, call_count, end_time - start_time

def simulate_new_approach():
    """Simulate the new batched git rev-parse approach."""
    base_options = [
        "origin/main", "main", 
        "origin/master", "master",
        "origin/develop", "develop",
        "origin/feature/test", "feature/test"
    ]
    
    start_time = time.time()
    call_count = 0
    actual_base = None
    
    # Get available branches
    success, stdout, stderr = run_command("git branch -r")
    available_branches = stdout.split('\n') if success else []
    
    # New approach - batched calls
    filtered_options = []
    for opt in base_options:
        if (any(opt in branch for branch in available_branches) or 
            opt in ['main', 'master']):
            filtered_options.append(opt)
    
    if filtered_options:
        call_count = 1  # Only one call for all options
        cmd = "git rev-parse " + " ".join(filtered_options)
        success, stdout, stderr = run_command(cmd)
        if stdout.strip():
            lines = stdout.strip().split('\n')
            for line, base_opt in zip(lines, filtered_options):
                if (line.strip() and 
                    len(line.strip()) >= 7 and 
                    not line.startswith("fatal:") and
                    not line.startswith("error:")):
                    actual_base = base_opt
                    break
    
    end_time = time.time()
    return actual_base, call_count, end_time - start_time

def main():
    """Main demonstration."""
    print("🚀 Git Command Optimization Demonstration")
    print("=" * 60)
    print("This demonstrates the performance improvement from batching")
    print("git rev-parse commands in validate_pr.py")
    print()
    
    original_dir = os.getcwd()
    test_dir = None
    
    try:
        # Set up test repository
        test_dir = setup_test_repo()
        print(f"📁 Created test repository: {test_dir}")
        
        # Run multiple iterations to get average performance
        iterations = 10
        print(f"🔄 Running {iterations} iterations for performance measurement...")
        
        old_times = []
        new_times = []
        old_calls_total = 0
        new_calls_total = 0
        
        for i in range(iterations):
            # Test old approach
            base, calls, time_taken = simulate_old_approach()
            old_times.append(time_taken)
            old_calls_total += calls
            
            # Test new approach
            base, calls, time_taken = simulate_new_approach()
            new_times.append(time_taken)
            new_calls_total += calls
        
        # Calculate averages
        avg_old_time = sum(old_times) / len(old_times)
        avg_new_time = sum(new_times) / len(new_times)
        avg_old_calls = old_calls_total / iterations
        avg_new_calls = new_calls_total / iterations
        
        # Show results
        print(f"\n📊 Performance Results (average over {iterations} iterations):")
        print(f"   Old approach:")
        print(f"     - Git calls: {avg_old_calls:.1f}")
        print(f"     - Time: {avg_old_time*1000:.2f}ms")
        print(f"   New approach:")
        print(f"     - Git calls: {avg_new_calls:.1f}")
        print(f"     - Time: {avg_new_time*1000:.2f}ms")
        print(f"\n💡 Improvement:")
        if avg_old_time > 0:
            time_improvement = ((avg_old_time - avg_new_time) / avg_old_time) * 100
            print(f"     - Call reduction: {avg_old_calls - avg_new_calls:.1f} fewer calls")
            print(f"     - Time improvement: {time_improvement:.1f}% faster")
        else:
            print(f"     - Call reduction: {avg_old_calls - avg_new_calls:.1f} fewer calls")
            print(f"     - Time improvement: Unmeasurable (too fast)")
        
        print(f"\n🎯 In larger repositories with more remote branches,")
        print(f"   the performance improvement would be even more significant!")
        
    except Exception as e:
        print(f"❌ Error during demonstration: {e}")
        
    finally:
        # Cleanup
        os.chdir(original_dir)
        if test_dir:
            shutil.rmtree(test_dir, ignore_errors=True)

if __name__ == "__main__":
    main()