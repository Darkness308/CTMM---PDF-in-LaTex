#!/usr/bin/env python3
"""
Fix problematic LaTeX patterns in converted/ directory files.
This script removes disturbing characters and patterns identified by latex_validator.py.
"""

import re
import sys
from pathlib import Path
from typing import Tuple
import shutil

def clean_latex_patterns(content: str) -> str:
    r"""
    Clean problematic LaTeX patterns in converted files.

    Fixes:
    - hypertarget_overuse: \hypertarget{id}{%\section{Title}}\label{id}
    - texorpdfstring_overuse: \texorpdfstring{text}{pdf-text}
    - excessive_backslashes: \\& instead of \&
    - auto_generated_labels: section-1, unnumbered-45, etc.
    """
    cleaned = content

    # 1. Fix hypertarget + section/subsection pattern
    # Pattern: \hypertarget{id}{%\section{Title}}\label{id}
    # The closing } for hypertarget comes AFTER the section
    # Structure: \hypertarget{id}{%\n\section{...}}\label{id}
    # Need to handle nested braces in section title (e.g., \textbf{...})
    cleaned = re.sub(
        r'\\hypertarget\{([^}]+)\}\{%\s*(\\(?:section|subsection|subsubsection)\{[^}]*(?:\{[^}]*\}[^}]*)*\})\}\s*\\label\{\1\}',
        r'\2\n\\label{\1}',
        cleaned,
        flags=re.MULTILINE | re.DOTALL
    )

    # 2. Fix double backslashes before ampersand
    cleaned = re.sub(r'\\\\&', r' \\& ', cleaned)

    # 3. Fix auto-generated labels (e.g., section-1, unnumbered-45)
    def replace_label(match):
        section_type = match.group(1)
        title = match.group(2)
        old_label = match.group(3)

        # Only replace if label looks auto-generated
        if re.match(r'^(section|unnumbered|subsection|subsubsection)-\d+', old_label):
            # Generate clean label from title
            label_base = re.sub(r'[^a-zA-Z0-9äöüß-]', '-', title.lower())
            label_base = re.sub(r'-+', '-', label_base).strip('-')

            # Determine prefix
            prefix_map = {
                'section': 'sec',
                'subsection': 'subsec',
                'subsubsection': 'subsubsec'
            }
            prefix = prefix_map.get(section_type, 'sec')

            new_label = f'{prefix}:{label_base}'
            return f'\\{section_type}{{{title}}}\\label{{{new_label}}}'
        else:
            return match.group(0)

    cleaned = re.sub(
        r'\\(section|subsection|subsubsection)\{([^}]+)\}\\label\{([^}]+)\}',
        replace_label,
        cleaned
    )

    # 4. Remove texorpdfstring wrappers when used with simple text/textbf
    # Pattern: \texorpdfstring{\textbf{Title}}{Title}
    # Convert to: \textbf{Title}
    cleaned = re.sub(
        r'\\texorpdfstring\{(\\textbf\{[^}]+\})\}\{[^}]*\}',
        r'\1',
        cleaned
    )

    # Also handle simpler cases
    cleaned = re.sub(
        r'\\texorpdfstring\{([^{}]+)\}\{[^}]*\}',
        r'\1',
        cleaned
    )

    # 5. Clean up excessive whitespace
    cleaned = re.sub(r'\n\s*\n\s*\n+', '\n\n', cleaned)

    return cleaned


def fix_file(file_path: Path, dry_run: bool = False) -> Tuple[bool, int]:
    """
    Fix problematic patterns in a single file.

    Args:
        file_path: Path to the file to fix
        dry_run: If True, don't write changes

    Returns:
        Tuple of (success, number_of_changes)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}", file=sys.stderr)
        return False, 0

    # Clean the content
    cleaned_content = clean_latex_patterns(original_content)

    # Count changes
    if original_content == cleaned_content:
        print(f"✓ {file_path}: No changes needed")
        return True, 0

    # Count differences
    original_lines = original_content.split('\n')
    cleaned_lines = cleaned_content.split('\n')
    changes = sum(1 for o, c in zip(original_lines, cleaned_lines) if o != c)
    changes += abs(len(original_lines) - len(cleaned_lines))

    if dry_run:
        print(f"Would fix {file_path}: {changes} line(s) would change")
        return True, changes

    # Create backup
    backup_path = file_path.with_suffix(file_path.suffix + '.backup')
    shutil.copy2(file_path, backup_path)

    # Write cleaned content
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)
        print(f"✓ Fixed {file_path}: {changes} line(s) changed (backup: {backup_path.name})")
        return True, changes
    except Exception as e:
        print(f"Error writing {file_path}: {e}", file=sys.stderr)
        # Restore from backup
        shutil.copy2(backup_path, file_path)
        return False, 0


def main():
    """Main function to fix all problematic files."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Fix problematic LaTeX patterns in converted/ directory'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be changed without making changes'
    )
    parser.add_argument(
        'files',
        nargs='*',
        help='Specific files to fix (default: all in converted/)'
    )

    args = parser.parse_args()

    # Determine files to process
    if args.files:
        files_to_fix = [Path(f) for f in args.files]
    else:
        converted_dir = Path('converted')
        if not converted_dir.exists():
            print(f"Error: {converted_dir} directory not found", file=sys.stderr)
            return 1

        files_to_fix = sorted(converted_dir.glob('*.tex'))
        # Exclude backup files
        files_to_fix = [f for f in files_to_fix if not f.name.endswith('.backup')]

    if not files_to_fix:
        print("No files to process")
        return 0

    print(f"Processing {len(files_to_fix)} file(s)...")
    if args.dry_run:
        print("DRY RUN - No changes will be made\n")
    print()

    # Process files
    total_changes = 0
    failed_files = []

    for file_path in files_to_fix:
        if not file_path.exists():
            print(f"Warning: {file_path} not found", file=sys.stderr)
            failed_files.append(file_path)
            continue

        success, changes = fix_file(file_path, dry_run=args.dry_run)
        if not success:
            failed_files.append(file_path)
        total_changes += changes

    # Summary
    print()
    print("=" * 60)
    print(f"Summary:")
    print(f"  Files processed: {len(files_to_fix)}")
    print(f"  Files changed: {sum(1 for f in files_to_fix if f not in failed_files and total_changes > 0)}")
    print(f"  Total line changes: {total_changes}")
    print(f"  Failed: {len(failed_files)}")

    if failed_files:
        print(f"\nFailed files:")
        for f in failed_files:
            print(f"  - {f}")
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
