#!/usr/bin/env python3
"""
Character Issue Checker for CTMM LaTeX Project

This script scans all text files in the repository for problematic characters
that could cause issues in LaTeX compilation or git operations.

Usage:
    python3 check_character_issues.py

Exit codes:
    0 - No issues found
    1 - Issues found
"""

import os
import sys
import re
from pathlib import Path


# Characters that are problematic in LaTeX
PROBLEMATIC_CHARS = {
    # Invisible Unicode characters
    '\u00A0': 'Non-breaking space (U+00A0) - use ~ or \\nobreakspace in LaTeX',
    '\u200B': 'Zero-width space (U+200B) - invisible character',
    '\u200C': 'Zero-width non-joiner (U+200C) - invisible character',
    '\u200D': 'Zero-width joiner (U+200D) - invisible character',
    '\u00AD': 'Soft hyphen (U+00AD) - use \\- in LaTeX',
    '\uFEFF': 'BOM/Zero-width no-break space (U+FEFF) - remove from file',
    # Typographic characters (common in copy-pasted text)
    '\u2018': "Left single quotation mark (U+2018) - use ` in LaTeX",
    '\u2019': "Right single quotation mark (U+2019) - use ' in LaTeX",
    '\u201A': "German opening single quote (U+201A) - use ` in LaTeX",
    '\u201C': 'Left double quotation mark (U+201C) - use `` in LaTeX',
    '\u201D': 'Right double quotation mark (U+201D) - use \'\' in LaTeX',
    '\u201E': 'German opening double quote (U+201E) - use `` in LaTeX',
    '\u2013': 'En dash (U+2013) - use -- in LaTeX or regular hyphen',
    '\u2014': 'Em dash (U+2014) - use --- in LaTeX or regular hyphen',
    '\u2026': 'Horizontal ellipsis (U+2026) - use \\ldots in LaTeX',
    '\u00AB': 'Left-pointing double angle quotation (U+00AB) - check context',
    '\u00BB': 'Right-pointing double angle quotation (U+00BB) - check context',
    '\u2022': 'Bullet (U+2022) - use \\textbullet in LaTeX',
}

# File extensions to check
FILE_EXTENSIONS = ('.tex', '.sty', '.py', '.md', '.sh', '.yml', '.yaml', '.txt')

# Directories to skip
SKIP_DIRS = {'.git', 'build', '__pycache__', 'node_modules', '.venv'}


class CharacterChecker:
    """Checks files for problematic characters"""
    
    def __init__(self, root_dir='.'):
        self.root_dir = Path(root_dir)
        self.issues = []
        self.files_scanned = 0
        self.lines_scanned = 0
    
    def scan_repository(self):
        """Scan all text files in the repository"""
        print(f"🔍 Scanning repository: {self.root_dir.absolute()}\n")
        
        for root, dirs, files in os.walk(self.root_dir):
            # Remove skip directories from dirs list (modifies in-place)
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            
            for filename in files:
                if filename.endswith(FILE_EXTENSIONS):
                    filepath = Path(root) / filename
                    self.scan_file(filepath)
        
        return len(self.issues) == 0
    
    def scan_file(self, filepath):
        """Scan a single file for problematic characters"""
        self.files_scanned += 1
        
        try:
            with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                lines = f.readlines()
            
            self.lines_scanned += len(lines)
            
            for line_num, line in enumerate(lines, 1):
                # Check for merge conflict markers at start of line
                if self._check_merge_conflicts(line, filepath, line_num):
                    continue
                
                # Check for problematic invisible characters
                self._check_invisible_chars(line, filepath, line_num)
                
                # Check for control characters
                self._check_control_chars(line, filepath, line_num)
        
        except Exception as e:
            self.issues.append({
                'file': str(filepath),
                'line': 0,
                'type': 'error',
                'message': f'Error reading file: {e}'
            })
    
    def _check_merge_conflicts(self, line, filepath, line_num):
        """Check for git merge conflict markers"""
        if re.match(r'^<{7}(\s|$)', line):
            self.issues.append({
                'file': str(filepath),
                'line': line_num,
                'type': 'merge_conflict',
                'message': 'Git merge conflict marker: <<<<<<<',
                'content': line.strip()
            })
            return True
        elif re.match(r'^>{7}(\s|$)', line):
            self.issues.append({
                'file': str(filepath),
                'line': line_num,
                'type': 'merge_conflict',
                'message': 'Git merge conflict marker: >>>>>>>',
                'content': line.strip()
            })
            return True
        elif re.match(r'^={7}(\s|$)', line):
            self.issues.append({
                'file': str(filepath),
                'line': line_num,
                'type': 'merge_conflict',
                'message': 'Git merge conflict separator: =======',
                'content': line.strip()
            })
            return True
        return False
    
    def _check_invisible_chars(self, line, filepath, line_num):
        """Check for problematic invisible Unicode characters"""
        for char, description in PROBLEMATIC_CHARS.items():
            if char in line:
                char_pos = line.index(char)
                context_start = max(0, char_pos - 10)
                context_end = min(len(line), char_pos + 10)
                context = line[context_start:context_end]
                
                self.issues.append({
                    'file': str(filepath),
                    'line': line_num,
                    'type': 'invisible_char',
                    'message': description,
                    'content': repr(context)
                })
    
    def _check_control_chars(self, line, filepath, line_num):
        """Check for control characters (except tab, newline, carriage return)"""
        for i, char in enumerate(line):
            if ord(char) < 0x20 and char not in '\n\r\t':
                context_start = max(0, i - 10)
                context_end = min(len(line), i + 10)
                context = line[context_start:context_end]
                
                self.issues.append({
                    'file': str(filepath),
                    'line': line_num,
                    'type': 'control_char',
                    'message': f'Control character (U+{ord(char):04X})',
                    'content': repr(context)
                })
                break  # Only report first occurrence per line
    
    def print_report(self):
        """Print scan results"""
        print(f"📊 Scan Results:")
        print(f"   Files scanned: {self.files_scanned}")
        print(f"   Lines scanned: {self.lines_scanned}")
        print()
        
        if not self.issues:
            print("✅ SUCCESS: Repository is clean!")
            print("   ✓ No merge conflict markers")
            print("   ✓ No invisible Unicode characters")
            print("   ✓ No problematic control characters")
            print()
            print("The repository is ready for LaTeX compilation.")
            return True
        else:
            print(f"⚠️  WARNING: Found {len(self.issues)} issue(s):\n")
            
            # Group issues by type
            by_type = {}
            for issue in self.issues:
                issue_type = issue['type']
                if issue_type not in by_type:
                    by_type[issue_type] = []
                by_type[issue_type].append(issue)
            
            # Print issues by type
            for issue_type, type_issues in by_type.items():
                print(f"  {issue_type.upper().replace('_', ' ')} ({len(type_issues)} issues):")
                for issue in type_issues[:10]:  # Show first 10 of each type
                    print(f"    📄 {issue['file']}:{issue['line']}")
                    print(f"       {issue['message']}")
                    if 'content' in issue:
                        print(f"       Content: {issue['content']}")
                    print()
                
                if len(type_issues) > 10:
                    print(f"    ... and {len(type_issues) - 10} more issues of this type\n")
            
            return False


def main():
    """Main entry point"""
    print("=" * 70)
    print("CTMM Character Issue Checker")
    print("=" * 70)
    print()
    
    checker = CharacterChecker()
    is_clean = checker.scan_repository()
    checker.print_report()
    
    sys.exit(0 if is_clean else 1)


if __name__ == '__main__':
    main()
