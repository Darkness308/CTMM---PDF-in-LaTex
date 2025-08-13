#!/usr/bin/env python3
"""
CTMM File Validation Script
Validates files to ensure they are compatible with GitHub tools including Copilot.
"""

import os
import sys
from pathlib import Path
import chardet


def check_file_encoding(file_path):
    """Check if file has proper UTF-8 encoding."""
    try:
        with open(file_path, 'rb') as f:
            raw_data = f.read()
            if len(raw_data) == 0:
                return False, "Empty file"
            
            result = chardet.detect(raw_data)
            encoding = result.get('encoding', 'unknown').lower()
            confidence = result.get('confidence', 0)
            
            # Accept UTF-8 or ASCII (ASCII is subset of UTF-8)
            if encoding in ['utf-8', 'ascii']:
                return True, f"Valid encoding: {encoding}"
            else:
                return False, f"Problematic encoding: {encoding} (confidence: {confidence:.2f})"
    except Exception as e:
        return False, f"Error reading file: {e}"


def check_filename_issues(file_path):
    """Check for problematic characters in filename."""
    filename = file_path.name
    issues = []
    
    # Check for spaces
    if ' ' in filename:
        issues.append("Contains spaces")
    
    # Check for special characters that might cause issues
    problematic_chars = ['<', '>', ':', '"', '|', '?', '*']
    for char in problematic_chars:
        if char in filename:
            issues.append(f"Contains problematic character: {char}")
    
    return issues


def validate_repository():
    """Validate all files in the repository."""
    print("CTMM Repository File Validation")
    print("=" * 50)
    
    issues_found = 0
    files_checked = 0
    
    # File extensions to check
    text_extensions = {'.tex', '.sty', '.py', '.md', '.yml', '.yaml', '.txt', '.json'}
    
    for root, dirs, files in os.walk('.'):
        # Skip .git directory
        if '.git' in dirs:
            dirs.remove('.git')
            
        for file in files:
            file_path = Path(root) / file
            
            # Skip hidden files and build artifacts
            if file.startswith('.') and file not in ['.gitignore', '.gitattributes']:
                continue
                
            if file_path.suffix.lower() in text_extensions:
                files_checked += 1
                
                # Check encoding
                encoding_ok, encoding_msg = check_file_encoding(file_path)
                if not encoding_ok:
                    print(f"❌ {file_path}: {encoding_msg}")
                    issues_found += 1
                
                # Check filename
                filename_issues = check_filename_issues(file_path)
                if filename_issues:
                    print(f"⚠️  {file_path}: Filename issues: {', '.join(filename_issues)}")
                    issues_found += 1
    
    print("\n" + "=" * 50)
    print(f"Validation complete: {files_checked} files checked")
    
    if issues_found == 0:
        print("✅ No issues found! Repository should be compatible with GitHub tools.")
        return True
    else:
        print(f"❌ {issues_found} issues found that may affect GitHub tool compatibility.")
        return False


if __name__ == "__main__":
    success = validate_repository()
    sys.exit(0 if success else 1)