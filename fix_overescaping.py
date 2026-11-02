#!/usr/bin/env python3
r"""
Fix over-escaped LaTeX commands in converted files.

This script fixes the systematic over-escaping issue where LaTeX commands
like \section are converted to \textbackslash{}section\textbackslash{}.
"""

import os
import re
import sys
import glob

def fix_overescaping(content):
    """
    Fix over-escaped LaTeX commands by converting \textbackslash{} patterns
    back to proper LaTeX backslashes.
    """

    # First, handle the most common LaTeX commands that got over-escaped
    latex_commands = [
        'section', 'subsection', 'subsubsection', 'chapter',
        'textbf', 'textit', 'emph', 'ul',
        'begin', 'end', 'item', 'label',
        'hypertarget', 'texorpdfstring',
        'texttt', 'textcolor',
        'tightlist', 'arabic', 'labelenumi', 'def'
    ]

    # Fix over-escaped LaTeX commands
    for cmd in latex_commands:
        # Pattern: \textbackslash{}command\textbackslash{} -> \command
        pattern = r'\\textbackslash\{\}' + re.escape(cmd) + r'\\textbackslash\{\}'
        replacement = '\\' + cmd
        content = re.sub(pattern, replacement, content)

        # Pattern: \textbackslash{}command{ -> \command{
        pattern = r'\\textbackslash\{\}' + re.escape(cmd) + r'\{'
        replacement = '\\' + cmd + '{'
        content = re.sub(pattern, replacement, content)

    # Fix over-escaped braces in LaTeX commands
    # Pattern: \textbackslash{}{content\textbackslash{}} -> {content}
    content = re.sub(r'\\textbackslash\{\}\{([^}]*?)\\textbackslash\{\}\}', r'{\1}', content)

    # Fix remaining standalone \textbackslash{} that should be \
    # But be careful not to break legitimate uses
    # Only fix those that are clearly LaTeX command separators
    content = re.sub(r'\\textbackslash\{\}([a-zA-Z]+)', r'\\\1', content)

    # Fix escaped ampersands in LaTeX context (\\& should be \&)
    content = re.sub(r'\\\\&', r'\\&', content)

    # Fix double backslashes that got mangled
    content = re.sub(r'\\textbackslash\{\}\\textbackslash\{\}', r'\\\\', content)

    return content

def process_file(filepath):
    """Process a single .tex file to fix over-escaping."""
    print(f"Processing {filepath}...")

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            original_content = f.read()

        fixed_content = fix_overescaping(original_content)

        # Only write back if content changed
        if fixed_content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            print(f"  [OK] Fixed over-escaping in {filepath}")
            return True
        else:
            print(f"  - No changes needed in {filepath}")
            return False

    except Exception as e:
        print(f"  [X] Error processing {filepath}: {e}")
        return False

def main():
    """Main function to process all converted .tex files."""

    if not os.path.exists('converted'):
        print("No 'converted' directory found. Nothing to fix.")
        return 0

    # Find all .tex files in the converted directory
    tex_files = glob.glob('converted/*.tex')

    if not tex_files:
        print("No .tex files found in converted directory.")
        return 0

    print(f"Found {len(tex_files)} .tex files to process...")

    processed = 0
    fixed = 0

    for tex_file in tex_files:
        processed += 1
        if process_file(tex_file):
            fixed += 1

    print(f"\nSummary:")
    print(f"  Files processed: {processed}")
    print(f"  Files fixed: {fixed}")
    print(f"  Files unchanged: {processed - fixed}")

    return 0

if __name__ == '__main__':
    sys.exit(main())
