#!/usr/bin/env python3
"""
Verification script for PR #489 resolution
Confirms all files are clean and ready for merge
"""

import os
import re
import sys
from pathlib import Path

def check_file_for_issues(filepath):
    """Check a single file for problematic characters"""
    issues = []
    
    try:
        with open(filepath, 'rb') as f:
            content = f.read()
        
        # Check for null bytes
        if b'\x00' in content:
            issues.append('[FAIL] Contains null bytes')
        
        # Try UTF-8 decode
        try:
            text = content.decode('utf-8')
            
            # Check for BOM
            if text.startswith('\ufeff'):
                issues.append('[WARN]️  Has BOM (Byte Order Mark) at start')
            
            # Check for zero-width characters
            zero_width = re.findall(r'[\u200B-\u200D\uFEFF]', text)
            if zero_width:
                issues.append(f'[WARN]️  Contains {len(zero_width)} zero-width character(s)')
            
            # Check for control characters (except standard whitespace)
            control_chars = re.findall(r'[\x01-\x08\x0B\x0C\x0E-\x1F]', text)
            if control_chars:
                issues.append(f'[WARN]️  Contains {len(control_chars)} control character(s)')
            
            # Check for merge conflict markers at line start
            if re.search(r'^<<<<<<< ', text, re.MULTILINE):
                issues.append('[FAIL] Contains merge conflict markers (<<<<<<< )')
            if re.search(r'^>>>>>>> ', text, re.MULTILINE):
                issues.append('[FAIL] Contains merge conflict markers (>>>>>>> )')
            if re.search(r'^=======$', text, re.MULTILINE):
                issues.append('[FAIL] Contains merge conflict markers (=======)')
            
        except UnicodeDecodeError as e:
            issues.append(f'[FAIL] Invalid UTF-8 encoding: {e}')
        
    except Exception as e:
        issues.append(f'[FAIL] Error reading file: {e}')
    
    return issues

def main():
    print("=" * 80)
    print("PR #489 Resolution Verification")
    print("=" * 80)
    print()
    
    # Key files to check that are modified by PR #489
    key_files = [
        '.github/copilot-instructions.md',
        'README.md',
        'main.tex',
    ]
    
    print("[SEARCH] Checking key files for problematic characters...")
    print()
    
    all_clean = True
    for filepath in key_files:
        if not os.path.exists(filepath):
            print(f"[WARN]️  {filepath}: File not found")
            continue
        
        issues = check_file_for_issues(filepath)
        
        if issues:
            all_clean = False
            print(f"[FAIL] {filepath}:")
            for issue in issues:
                print(f"  {issue}")
        else:
            # Get file stats
            with open(filepath, 'rb') as f:
                content = f.read()
            text = content.decode('utf-8')
            lines = len(text.splitlines())
            size = len(content)
            
            print(f"[PASS] {filepath}")
            print(f"  [SUMMARY] Size: {size:,} bytes, Lines: {lines:,}")
    
    print()
    print("=" * 80)
    
    if all_clean:
        print("[PASS] VERIFICATION PASSED: All files are clean and ready for merge!")
        print()
        print("[TEST] Summary:")
        print("  • No null bytes found")
        print("  • No merge conflict markers")
        print("  • No problematic Unicode characters")
        print("  • All files have valid UTF-8 encoding")
        print()
        print("[TARGET] Next Step:")
        print("  Change PR #489 base branch from 'copilot/fix-99' to 'main'")
        print("  via GitHub web interface at:")
        print("  https://github.com/Darkness308/CTMM---PDF-in-LaTex/pull/489")
        return 0
    else:
        print("[FAIL] VERIFICATION FAILED: Some files have issues")
        print()
        print("Please review and fix the issues listed above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
