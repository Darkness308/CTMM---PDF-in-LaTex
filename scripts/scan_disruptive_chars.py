#!/usr/bin/env python3
"""
Disruptive Character Scanner for CTMM Repository

This script scans all text files in the repository for disruptive characters
that could cause issues with LaTeX compilation, Git operations, or cross-platform
compatibility.

Checks for:
- BOM (Byte Order Mark) at file start
- NULL bytes in text files
- Merge conflict markers at line start
- Zero-width invisible characters
- Directional marks
- Problematic Unicode quotes in code/LaTeX files
- Invalid control characters

Usage:
    python3 scan_disruptive_chars.py [--verbose]
"""

import os
import sys
import argparse
from pathlib import Path

# Define TEXT file extensions (not binary)
TEXT_EXTENSIONS = [
    '.tex', '.sty', '.md', '.py', '.txt',
    '.yml', '.yaml', '.json', '.sh', '.gitignore',
    '.js', '.css', '.html', '.xml', '.csv'
]

# Files that contain documentation about disruptive characters (can contain examples)
DOCUMENTATION_FILES = {
    'DISRUPTIVE_CHARACTERS_REMOVAL_REPORT.md',
    'PR_571_LOESUNG_DE.md',
    'PR_571_MERGE_FIX_REPORT.md',
    'STOERENDE_ZEICHEN_ENTFERNT_BERICHT.md',
    'TASK_COMPLETE_PR_571.md',
    'MERGE_FIX_COMPLETE.md',
    'QUICKSTART_PR_571_FIX.md'
}

# Directories to exclude from scanning
EXCLUDE_DIRS = {'.git', 'build', '__pycache__', '.vscode', '.devcontainer', 'node_modules'}

def scan_text_file(filepath, verbose=False):
    """
    Scan a text file for disruptive characters.

    Args:
        filepath: Path to the file to scan
        verbose: If True, show details for each check

    Returns:
        List of issues found, each as (issue_type, line_num, description)
    """
    issues = []

    try:
        with open(filepath, 'rb') as f:
            content_bytes = f.read()

        # 1. Check BOM at start
        if content_bytes.startswith(b'\xef\xbb\xbf'):
            issues.append(('BOM', 1, 'UTF-8 BOM at file start'))
            if verbose:
                print(f"  BOM found in {filepath}")

        # 2. Check NULL bytes (should not be in text files)
        if b'\x00' in content_bytes:
            issues.append(('NULL_BYTE', -1, 'NULL byte in text file'))
            if verbose:
                print(f"  NULL byte found in {filepath}")

        # Try to decode as UTF-8
        try:
            text = content_bytes.decode('utf-8')
        except UnicodeDecodeError as e:
            issues.append(('ENCODING', -1, f'Invalid UTF-8: {str(e)[:50]}'))
            if verbose:
                print(f"  Encoding error in {filepath}")
            return issues

        lines = text.split('\n')

        # 3. Check for actual merge conflict markers at line start
        for i, line in enumerate(lines, 1):
            if line.startswith('<<<<<<<') or line.startswith('>>>>>>>'):
                # Ignore if in documentation (backticks or code blocks)
                if '`' not in line and not line.strip().startswith('#'):
                    issues.append(('MERGE_CONFLICT', i, line.strip()[:60]))
                    if verbose:
                        print(f"  Merge conflict marker at {filepath}:{i}")

        # 4. Check for invisible characters
        zero_width = ['\u200b', '\ufeff', '\u200c', '\u200d']
        direction = ['\u200e', '\u200f']

        for i, line in enumerate(lines, 1):
            for char in zero_width:
                if char in line:
                    issues.append(('ZERO_WIDTH', i, f'U+{ord(char):04X}'))
                    if verbose:
                        print(f"  Zero-width char U+{ord(char):04X} at {filepath}:{i}")
            for char in direction:
                if char in line:
                    issues.append(('DIRECTION', i, f'U+{ord(char):04X}'))
                    if verbose:
                        print(f"  Direction mark U+{ord(char):04X} at {filepath}:{i}")

        # 5. Check for problematic quotes in code/LaTeX files
        if filepath.endswith(('.tex', '.sty', '.py', '.sh', '.json', '.yml', '.yaml')):
            problematic_quotes = ['\u201e', '\u201c', '\u201d', '\u2018', '\u2019']

            for i, line in enumerate(lines, 1):
                for char in problematic_quotes:
                    if char in line:
                        issues.append(('QUOTE', i, f'{char} (U+{ord(char):04X}) in: {line.strip()[:50]}'))
                        if verbose:
                            print(f"  Problematic quote at {filepath}:{i}")

        # 6. Check for invalid control characters (except tab, LF, CR)
        for i, line in enumerate(lines, 1):
            for char in line:
                code = ord(char)
                if 0 <= code < 32 and code not in [9, 10, 13]:  # Allow tab, LF, CR
                    issues.append(('CONTROL_CHAR', i, f'Invalid control U+{code:04X}'))
                    if verbose:
                        print(f"  Control char U+{code:04X} at {filepath}:{i}")

    except Exception as e:
        issues.append(('ERROR', -1, str(e)))
        if verbose:
            print(f"  Error scanning {filepath}: {e}")

    return issues


def main():
    """Main scanning function."""
    parser = argparse.ArgumentParser(description='Scan for disruptive characters in text files')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show verbose output')
    args = parser.parse_args()

    print("=" * 80)
    print("CTMM Disruptive Character Scanner")
    print("=" * 80)
    print()

    # Scan all text files
    all_issues = {}
    files_scanned = 0

    for root, dirs, files in os.walk('.'):
        # Remove excluded directories from traversal
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

        for file in files:
            # Only check text files
            if not any(file.endswith(ext) for ext in TEXT_EXTENSIONS):
                continue
            if file in DOCUMENTATION_FILES:
                continue

            filepath = os.path.join(root, file)
            files_scanned += 1

            if args.verbose:
                print(f"Scanning: {filepath}")

            issues = scan_text_file(filepath, args.verbose)
            if issues:
                all_issues[filepath] = issues

    print(f"\nScanned {files_scanned} text files (excluding documentation)")
    print(f"Found issues in {len(all_issues)} files\n")

    if all_issues:
        print("=" * 80)
        print("DISRUPTIVE CHARACTERS FOUND:")
        print("=" * 80)
        for filepath, issues in sorted(all_issues.items()):
            print(f"\n📄 {filepath}")
            for issue_type, line_num, description in issues:
                if line_num > 0:
                    print(f"   Line {line_num}: [{issue_type}] {description}")
                else:
                    print(f"   File-wide: [{issue_type}] {description}")

        print("\n" + "=" * 80)
        print(f"TOTAL: {sum(len(issues) for issues in all_issues.values())} issues in {len(all_issues)} files")
        print("\n⚠️  ACTION REQUIRED: These disruptive characters should be removed!")
        return 1  # Exit with error code
    else:
        print("✅ NO DISRUPTIVE CHARACTERS FOUND!")
        print("\n✓ All text files are clean:")
        print("  • No BOM markers")
        print("  • No NULL bytes")
        print("  • No merge conflict markers")
        print("  • No zero-width characters")
        print("  • No directional marks")
        print("  • No problematic Unicode quotes")
        print("  • No invalid control characters")
        print("\n✅ Repository is ready for PR!")
        return 0  # Success


if __name__ == '__main__':
    sys.exit(main())
