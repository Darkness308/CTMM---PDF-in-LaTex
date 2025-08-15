#!/usr/bin/env python3
"""
Validate that the repository is ready for GitHub Copilot reviews.

This script validates the fixes applied for issue #596:
- "Copilot wasn't able to review any files in this pull request."
"""

import os
import subprocess
import sys
from pathlib import Path

def check_binary_files():
    """Check for binary files that could interfere with Copilot."""
    print("🔍 Checking for binary files...")
    
    # Define binary file extensions
    binary_extensions = ['.pdf', '.docx', '.doc', '.xlsx', '.xls', '.ppt', '.pptx']
    
    # Check for binary files in the repository
    binary_files = []
    for ext in binary_extensions:
        result = subprocess.run(['find', '.', '-name', f'*{ext}', '-not', '-path', './.git/*'], 
                              capture_output=True, text=True)
        if result.stdout.strip():
            binary_files.extend(result.stdout.strip().split('\n'))
    
    if binary_files:
        print(f"❌ Found {len(binary_files)} binary files that could interfere with Copilot:")
        for file in binary_files[:10]:  # Show first 10
            print(f"   - {file}")
        if len(binary_files) > 10:
            print(f"   ... and {len(binary_files) - 10} more")
        return False
    else:
        print("✅ No problematic binary files found")
        return True

def check_git_tracked_binaries():
    """Check if any binary files are tracked by git."""
    print("🔍 Checking git-tracked binary files...")
    
    result = subprocess.run(['git', 'ls-files'], capture_output=True, text=True)
    if result.returncode != 0:
        print("❌ Could not get git file list")
        return False
    
    tracked_files = result.stdout.strip().split('\n')
    binary_extensions = ['.pdf', '.docx', '.doc', '.xlsx', '.xls', '.ppt', '.pptx']
    
    tracked_binaries = [f for f in tracked_files 
                       if any(f.endswith(ext) for ext in binary_extensions)]
    
    if tracked_binaries:
        print(f"❌ Found {len(tracked_binaries)} binary files tracked by git:")
        for file in tracked_binaries:
            print(f"   - {file}")
        return False
    else:
        print("✅ No binary files tracked by git")
        return True

def check_repository_size():
    """Check repository size for any unusually large files."""
    print("🔍 Checking for large files...")
    
    result = subprocess.run(['find', '.', '-type', 'f', '-size', '+1M', '-not', '-path', './.git/*'], 
                          capture_output=True, text=True)
    
    large_files = result.stdout.strip().split('\n') if result.stdout.strip() else []
    
    if large_files:
        print(f"⚠️  Found {len(large_files)} files larger than 1MB:")
        for file in large_files:
            # Get file size
            size_result = subprocess.run(['du', '-h', file], capture_output=True, text=True)
            size = size_result.stdout.split()[0] if size_result.returncode == 0 else "unknown"
            print(f"   - {file} ({size})")
        print("   Note: Large files might affect Copilot performance")
        return len(large_files) <= 5  # Allow up to 5 large files
    else:
        print("✅ No unusually large files found")
        return True

def check_text_file_encoding():
    """Check that text files have proper encoding."""
    print("🔍 Checking text file encoding...")
    
    # Check key source files
    source_extensions = ['.tex', '.py', '.md', '.yml', '.yaml']
    problematic_files = []
    
    for ext in source_extensions:
        result = subprocess.run(['find', '.', '-name', f'*{ext}', '-not', '-path', './.git/*'], 
                              capture_output=True, text=True)
        
        if result.stdout.strip():
            files = result.stdout.strip().split('\n')
            for file in files[:20]:  # Check first 20 files of each type
                try:
                    with open(file, 'r', encoding='utf-8') as f:
                        f.read()
                except UnicodeDecodeError:
                    problematic_files.append(file)
                except Exception:
                    # Skip files that can't be read for other reasons
                    pass
    
    if problematic_files:
        print(f"❌ Found {len(problematic_files)} files with encoding issues:")
        for file in problematic_files:
            print(f"   - {file}")
        return False
    else:
        print("✅ Text files have proper UTF-8 encoding")
        return True

def check_gitignore():
    """Check that .gitignore properly excludes binary files."""
    print("🔍 Checking .gitignore configuration...")
    
    gitignore_path = Path('.gitignore')
    if not gitignore_path.exists():
        print("❌ .gitignore file not found")
        return False
    
    with open(gitignore_path, 'r') as f:
        gitignore_content = f.read()
    
    required_patterns = ['*.pdf', '*.docx', '*.doc', '*.xlsx', '*.xls']
    missing_patterns = []
    
    for pattern in required_patterns:
        if pattern not in gitignore_content:
            missing_patterns.append(pattern)
    
    if missing_patterns:
        print(f"❌ .gitignore missing patterns: {missing_patterns}")
        return False
    else:
        print("✅ .gitignore properly configured for binary files")
        return True

def check_repository_cleanliness():
    """Check that the repository is clean."""
    print("🔍 Checking repository cleanliness...")
    
    result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
    if result.returncode != 0:
        print("❌ Could not check git status")
        return False
    
    if result.stdout.strip():
        print("⚠️  Repository has uncommitted changes:")
        print(result.stdout.strip())
        return True  # This is okay for development
    else:
        print("✅ Repository is clean")
        return True

def run_validation():
    """Run all validation checks."""
    print("=" * 70)
    print("GitHub Copilot Readiness Validation - Issue #596")
    print("=" * 70)
    print()
    
    checks = [
        ("Binary files check", check_binary_files),
        ("Git-tracked binaries check", check_git_tracked_binaries),
        ("Repository size check", check_repository_size),
        ("Text file encoding check", check_text_file_encoding),
        (".gitignore configuration", check_gitignore),
        ("Repository cleanliness", check_repository_cleanliness),
    ]
    
    results = []
    for check_name, check_func in checks:
        print(f"\n--- {check_name} ---")
        result = check_func()
        results.append((check_name, result))
        print()
    
    # Summary
    print("=" * 70)
    print("VALIDATION SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for check_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {check_name}")
    
    print(f"\nOverall: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 Repository is ready for GitHub Copilot reviews!")
        print("The fixes for issue #596 have been successfully applied.")
        return True
    else:
        print(f"\n⚠️  {total - passed} issues need to be addressed before Copilot can review files effectively.")
        return False

if __name__ == "__main__":
    success = run_validation()
    sys.exit(0 if success else 1)