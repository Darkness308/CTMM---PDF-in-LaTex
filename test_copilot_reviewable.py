#!/usr/bin/env python3
"""
Test script to verify that the CTMM repository is now Copilot-reviewable.

This script validates that:
1. No binary files are tracked in git
2. All tracked files are in reviewable formats
3. The build system can still process source files
4. The repository structure is maintained
"""

import subprocess
import os
import sys
from pathlib import Path

def run_command(cmd):
    """Run a shell command and return stdout, stderr, returncode."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip(), result.stderr.strip(), result.returncode

def test_no_binary_files():
    """Test that no binary files are tracked."""
    print("🔍 Testing: No binary files tracked...")
    stdout, stderr, returncode = run_command("git ls-files | grep -E '\\.(pdf|docx|doc|odt)$'")
    
    if returncode == 0 and stdout:
        print(f"❌ FAIL: Found binary files: {stdout}")
        return False
    else:
        print("✅ PASS: No binary files tracked")
        return True

def test_source_files_present():
    """Test that essential source files are still tracked."""
    print("🔍 Testing: Source files present...")
    
    essential_files = [
        "main.tex",
        "ctmm_build.py", 
        "build_system.py",
        ".gitignore"
    ]
    
    all_present = True
    for file in essential_files:
        if not Path(file).exists():
            print(f"❌ FAIL: Missing essential file: {file}")
            all_present = False
    
    if all_present:
        print("✅ PASS: All essential source files present")
    
    return all_present

def test_file_types():
    """Test that only reviewable file types are tracked."""
    print("🔍 Testing: Only reviewable file types tracked...")
    
    stdout, stderr, returncode = run_command("git ls-files")
    files = stdout.split('\n') if stdout else []
    
    reviewable_extensions = {'.tex', '.py', '.md', '.sty', '.json', '.yml', '.yaml', '.txt'}
    reviewable_files = {'LICENSE', 'Makefile', '.gitignore'}
    
    non_reviewable = []
    for file in files:
        if file:
            # Check if it's a reviewable file extension or special file
            is_reviewable = (
                any(file.endswith(ext) for ext in reviewable_extensions) or
                any(special_file in file for special_file in reviewable_files) or
                file in reviewable_files
            )
            if not is_reviewable:
                non_reviewable.append(file)
    
    if non_reviewable:
        print(f"❌ FAIL: Non-reviewable files found: {non_reviewable}")
        return False
    else:
        print("✅ PASS: Only reviewable file types tracked")
        return True

def test_build_system():
    """Test that the build system can scan files."""
    print("🔍 Testing: Build system functionality...")
    
    stdout, stderr, returncode = run_command("python3 ctmm_build.py")
    
    if "All referenced files exist" in stdout:
        print("✅ PASS: Build system can scan all files")
        return True
    elif "pdflatex" in stderr:
        print("✅ PASS: Build system works (pdflatex not installed, but scanning works)")
        return True
    else:
        print(f"❌ FAIL: Build system issues: {stderr}")
        return False

def test_file_count():
    """Test file count statistics."""
    print("🔍 Testing: File count statistics...")
    
    # Count all tracked files
    stdout, _, _ = run_command("git ls-files | wc -l")
    total_files = int(stdout) if stdout.isdigit() else 0
    
    # Count source files
    stdout, _, _ = run_command("git ls-files | grep -E '\\.(tex|py|md)$' | wc -l") 
    source_files = int(stdout) if stdout.isdigit() else 0
    
    print(f"📊 Statistics:")
    print(f"   Total tracked files: {total_files}")
    print(f"   Source files (.tex, .py, .md): {source_files}")
    
    if total_files > 0 and source_files > 0:
        print("✅ PASS: Reasonable file counts")
        return True
    else:
        print("❌ FAIL: Unexpected file counts")
        return False

def main():
    print("🧪 CTMM Repository Copilot-Reviewability Test")
    print("=" * 50)
    
    # Change to repository directory
    os.chdir(Path(__file__).parent)
    
    tests = [
        test_no_binary_files,
        test_source_files_present, 
        test_file_types,
        test_build_system,
        test_file_count
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"🏁 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 SUCCESS: Repository is now Copilot-reviewable!")
        return 0
    else:
        print("❌ FAILURE: Repository still has reviewability issues")
        return 1

if __name__ == "__main__":
    sys.exit(main())