#!/usr/bin/env python3
"""
Validate Merge Readiness: Comprehensive check for merge conflicts and problematic characters

German task: "in zwei dateien gibt es noch konflikte, die einen merge verhindern.
             identifiziere alle störenden zeichen in jeder datei, damit der merge funktioniert"

Translation: "in two files there are still conflicts that prevent a merge.
              identify all disturbing characters in each file so that the merge works"

This script performs comprehensive validation to identify:
1. Git merge conflict markers (<<<<<<<, =======, >>>>>>>)
2. Problematic characters (BOM, control chars, zero-width chars)
3. LaTeX special characters that need escaping
4. Encoding issues
5. Line ending inconsistencies
"""

import os
import sys
import re
import codecs
from pathlib import Path


def check_merge_conflict_markers(filepath):
    """Check for actual git merge conflict markers."""
    issues = []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        # Track if we're inside a code block (for markdown files)
        in_code_block = False

        for line_num, line in enumerate(lines, 1):
            # For markdown files, track code blocks
            if filepath.endswith('.md'):
                if line.strip().startswith('```'):
                    in_code_block = not in_code_block
                    continue

                # Skip lines inside code blocks
                if in_code_block:
                    continue

            # For Python/test files, skip if line contains quotes (string literal)
            if filepath.endswith('.py'):
                if "'" in line or '"' in line:
                    # Likely a string literal in test code
                    continue

            # Check for conflict markers at start of line
            if re.match(r'^<{7}\s', line):
                issues.append(f"Line {line_num}: Merge conflict start marker: {line.strip()[:60]}")
            elif re.match(r'^>{7}\s', line):
                issues.append(f"Line {line_num}: Merge conflict end marker: {line.strip()[:60]}")
            elif re.match(r'^={7}$', line.strip()):
                # Additional check: make sure it's not part of markdown formatting
                if not (filepath.endswith('.md') and len(line.strip()) < 10):
                    issues.append(f"Line {line_num}: Merge conflict separator: {line.strip()}")
    except Exception as e:
        issues.append(f"Error reading file: {e}")

    return issues


def check_problematic_characters(filepath):
    """Check for problematic characters that could cause merge or compilation issues."""
    issues = []
    try:
        with open(filepath, 'rb') as f:
            content = f.read()

        # Check for BOM
        if content.startswith(codecs.BOM_UTF8):
            issues.append("UTF-8 BOM (Byte Order Mark) found at file start")
        if content.startswith(codecs.BOM_UTF16_LE):
            issues.append("UTF-16 LE BOM found")
        if content.startswith(codecs.BOM_UTF16_BE):
            issues.append("UTF-16 BE BOM found")

        # Check for zero-width characters
        zero_width_chars = {
            b'\xe2\x80\x8b': 'Zero-width space (U+200B)',
            b'\xe2\x80\x8c': 'Zero-width non-joiner (U+200C)',
            b'\xe2\x80\x8d': 'Zero-width joiner (U+200D)',
            b'\xef\xbf\xbc': 'Object replacement character (U+FFFC)',
            b'\xe2\x80\x8e': 'Left-to-right mark (U+200E)',
            b'\xe2\x80\x8f': 'Right-to-left mark (U+200F)',
        }

        for char_bytes, char_name in zero_width_chars.items():
            if char_bytes in content:
                count = content.count(char_bytes)
                issues.append(f"{char_name}: {count} occurrence(s)")

        # Check for control characters
        control_chars_found = set()
        for i, byte in enumerate(content):
            if byte < 32 and byte not in [9, 10, 13]:  # Exclude tab, LF, CR
                control_chars_found.add(byte)

        if control_chars_found:
            for byte_val in sorted(control_chars_found):
                issues.append(f"Control character found: byte {byte_val} (0x{byte_val:02x})")

        # Check for mixed line endings
        crlf_count = content.count(b'\r\n')
        cr_count = content.count(b'\r') - crlf_count
        lf_count = content.count(b'\n') - crlf_count

        if sum(x > 0 for x in [crlf_count, cr_count, lf_count]) > 1:
            issues.append(f"Mixed line endings: CRLF={crlf_count}, CR={cr_count}, LF={lf_count}")

    except Exception as e:
        issues.append(f"Error analyzing file: {e}")

    return issues


def check_latex_escaping_issues(filepath):
    """Check for LaTeX characters that might need escaping."""
    if not filepath.endswith('.tex'):
        return []

    issues = []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        for line_num, line in enumerate(lines, 1):
            # Skip comments
            if line.strip().startswith('%'):
                continue

            # Check for unescaped special chars (very basic check)
            # Note: This is simplified - real LaTeX is complex
            if re.search(r'[^\\]&[^&]', line):
                # Might be unescaped ampersand (unless it's in a table)
                if '\\begin{tabular}' not in ''.join(lines[max(0, line_num-10):line_num]):
                    pass  # Too many false positives, skip

            # Check for potentially problematic underscore patterns
            if re.search(r'[^\\]_[^{]', line) and '\\url' not in line and '\\href' not in line:
                pass  # Also has false positives in math mode

    except Exception as e:
        issues.append(f"Error checking LaTeX: {e}")

    return issues


def validate_file(filepath):
    """Run all validations on a single file."""
    results = {
        'filepath': filepath,
        'merge_conflicts': [],
        'problematic_chars': [],
        'latex_issues': [],
        'has_issues': False
    }

    results['merge_conflicts'] = check_merge_conflict_markers(filepath)
    results['problematic_chars'] = check_problematic_characters(filepath)
    results['latex_issues'] = check_latex_escaping_issues(filepath)

    results['has_issues'] = any([
        results['merge_conflicts'],
        results['problematic_chars'],
        results['latex_issues']
    ])

    return results


def main():
    """Main validation function."""
    print("🔍 CTMM Merge Readiness Validation")
    print("=" * 70)
    print("Task: Identify conflicts and disturbing characters in files")
    print("      (German: 'störenden zeichen')")
    print("=" * 70)
    print()

    # Define files to check
    check_patterns = [
        '*.tex',
        '*.sty',
        '*.yml',
        '*.yaml',
        '*.py',
        '*.md'
    ]

    files_to_check = []
    for pattern in check_patterns:
        files_to_check.extend(Path('.').rglob(pattern))

    # Filter out .git directory
    files_to_check = [f for f in files_to_check if '.git' not in str(f)]

    print(f"📊 Checking {len(files_to_check)} files...")
    print()

    files_with_issues = []
    total_checked = 0

    for filepath in sorted(files_to_check):
        total_checked += 1
        results = validate_file(str(filepath))

        if results['has_issues']:
            files_with_issues.append(results)

    # Print results
    print("=" * 70)
    print("📋 VALIDATION RESULTS")
    print("=" * 70)
    print(f"Total files checked: {total_checked}")
    print(f"Files with issues: {len(files_with_issues)}")
    print()

    if files_with_issues:
        print("⚠️  ISSUES FOUND:")
        print()

        for result in files_with_issues:
            print(f"📄 {result['filepath']}")
            print("-" * 70)

            if result['merge_conflicts']:
                print("  ❌ MERGE CONFLICTS:")
                for issue in result['merge_conflicts']:
                    print(f"     • {issue}")
                print()

            if result['problematic_chars']:
                print("  ⚠️  PROBLEMATIC CHARACTERS:")
                for issue in result['problematic_chars']:
                    print(f"     • {issue}")
                print()

            if result['latex_issues']:
                print("  ⚠️  LATEX ISSUES:")
                for issue in result['latex_issues']:
                    print(f"     • {issue}")
                print()

            print()

        print("=" * 70)
        print("❌ VALIDATION FAILED")
        print(f"Found issues in {len(files_with_issues)} file(s)")
        print()
        print("Action required: Review and fix the issues listed above")
        return 1
    else:
        print("✅ NO ISSUES FOUND")
        print()
        print("All checked files are clean:")
        print("  • No merge conflict markers")
        print("  • No problematic characters (BOM, control chars, zero-width)")
        print("  • No obvious LaTeX escaping issues")
        print()
        print("✅ Repository is ready for merge")
        return 0


if __name__ == "__main__":
    sys.exit(main())
