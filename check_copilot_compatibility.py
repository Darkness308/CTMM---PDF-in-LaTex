#!/usr/bin/env python3
"""
Test script to verify Copilot review functionality.
This script validates that files are properly formatted for Copilot reviews.
"""

import os
import re
from pathlib import Path

def should_ignore_path(path):
    """Check if path should be ignored based on common patterns."""
    ignore_patterns = [
        '.git',
        'therapie-material',
        '__pycache__',
        '.pdf',
        'build/'
    ]
    
    path_str = str(path)
    for pattern in ignore_patterns:
        if pattern in path_str:
            return True
    return False

def check_filename_conventions(directory="."):
    """Check that filenames follow Copilot-friendly conventions."""
    issues = []
    
    for root, dirs, files in os.walk(directory):
        # Skip ignored directories
        if should_ignore_path(root):
            continue
            
        for file in files:
            file_path = os.path.join(root, file)
            
            # Skip ignored files
            if should_ignore_path(file_path):
                continue
                
            # Check for spaces in filenames
            if ' ' in file:
                issues.append(f"File with spaces: {file_path}")
            
            # Check for problematic special characters
            if re.search(r'[#$@%&*]', file):
                issues.append(f"File with special chars: {file_path}")
    
    return issues

def check_file_encoding(file_path):
    """Check if file uses UTF-8 encoding."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            f.read()
        return True
    except UnicodeDecodeError:
        return False

def main():
    """Run Copilot review compatibility checks."""
    print("🔍 Checking Copilot Review Compatibility...")
    print("=" * 50)
    
    # Check filename conventions
    filename_issues = check_filename_conventions()
    if filename_issues:
        print("❌ Filename Issues Found:")
        for issue in filename_issues:
            print(f"  - {issue}")
    else:
        print("✅ All filenames follow conventions")
    
    # Check for large files
    large_files = []
    for file_path in Path('.').rglob('*'):
        if file_path.is_file() and file_path.stat().st_size > 100000:  # 100KB
            large_files.append(f"{file_path} ({file_path.stat().st_size:,} bytes)")
    
    if large_files:
        print("⚠️  Large files found (consider excluding from git):")
        for file in large_files:
            print(f"  - {file}")
    else:
        print("✅ No large files detected")
    
    # Check UTF-8 encoding for text files
    text_extensions = ['.tex', '.py', '.md', '.txt', '.sty']
    encoding_issues = []
    
    for file_path in Path('.').rglob('*'):
        if file_path.is_file() and file_path.suffix in text_extensions:
            if not check_file_encoding(file_path):
                encoding_issues.append(str(file_path))
    
    if encoding_issues:
        print("❌ Encoding Issues Found:")
        for issue in encoding_issues:
            print(f"  - {issue}")
    else:
        print("✅ All text files use UTF-8 encoding")
    
    print("\n" + "=" * 50)
    
    if not filename_issues and not encoding_issues:
        print("🎉 Repository is optimized for Copilot reviews!")
        return 0
    else:
        print("⚠️  Some issues found - see above for details")
        return 1

if __name__ == "__main__":
    exit(main())