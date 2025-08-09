#!/usr/bin/env python3
"""
CTMM Over-Escaping Fixer
Systematically fixes over-escaping issues in LaTeX documents that may occur 
during document conversion pipelines.

Common over-escaping patterns:
1. Double-escaped ampersands
2. hypertarget/texorpdfstring commands (pandoc artifacts)
3. Unnecessary quote wrapping in lists
4. Double backticks instead of proper quotes
5. ul{} commands that may not be defined
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple


def fix_over_escaping(content: str) -> Tuple[str, List[str]]:
    """
    Fix common over-escaping patterns in LaTeX content.
    Returns: (fixed_content, list_of_changes_made)
    """
    changes = []
    original_content = content
    
    # 1. Fix double-escaped ampersands (double backslash & -> single backslash &)
    if '\\\\&' in content:
        content = re.sub(r'\\\\&', r'\\&', content)
        changes.append("Fixed double-escaped ampersands")
    
    # 2. Remove hypertarget wrapper commands (pandoc artifacts)
    hypertarget_pattern = r'\\hypertarget\{[^}]*\}\{%\s*\n(.*?)\}\s*\\label\{[^}]*\}'
    if re.search(hypertarget_pattern, content, re.DOTALL):
        content = re.sub(hypertarget_pattern, r'\1', content, flags=re.DOTALL)
        changes.append("Removed hypertarget wrapper commands")
    
    # 3. Remove texorpdfstring wrapper (keep the first argument)
    texorpdf_pattern = r'\\texorpdfstring\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
    if re.search(texorpdf_pattern, content):
        content = re.sub(texorpdf_pattern, r'\1', content)
        changes.append("Removed texorpdfstring wrapper commands")
    
    # 4. Fix unnecessary quote wrapping in list items
    quote_list_pattern = r'\\item\s*\n\s*\\begin\{quote\}\s*\n\s*(.*?)\s*\n\s*\\end\{quote\}'
    if re.search(quote_list_pattern, content, re.DOTALL):
        content = re.sub(quote_list_pattern, r'\\item \1', content, flags=re.DOTALL)
        changes.append("Removed unnecessary quote wrapping in list items")
    
    # 5. Fix double backticks to proper quotes (more aggressive pattern)
    # Handle various backtick patterns
    content = re.sub(r'(["`]+)([^"`]*?)(["`]+)', lambda m: f'"{m.group(2)}"', content)
    if '``' in original_content or '""' in original_content:
        changes.append("Fixed quote formatting issues")
    
    # 6. Replace ul{} with underline{} (more standard)
    if r'\ul{' in content:
        content = re.sub(r'\\ul\{', r'\\underline{', content)
        changes.append("Replaced ul{} with underline{}")
    
    # 7. Normalize section commands to use proper CTMM styling
    section_pattern = r'\\section\{\\textbf\{([^}]*)\}\}'
    if re.search(section_pattern, content):
        # This would need more context about the specific CTMM styling
        # For now, just flag it
        changes.append("Found section with textbf wrapper (may need CTMM styling)")
    
    return content, changes


def process_file(file_path: Path, dry_run: bool = False) -> bool:
    """
    Process a single LaTeX file for over-escaping issues.
    Returns True if changes were made.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return False
    
    fixed_content, changes = fix_over_escaping(original_content)
    
    if changes:
        print(f"\nFile: {file_path}")
        for change in changes:
            print(f"  - {change}")
        
        if not dry_run:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                print(f"  ✓ Applied fixes to {file_path}")
            except Exception as e:
                print(f"  ✗ Error writing to {file_path}: {e}")
                return False
        else:
            print(f"  (Dry run - no changes applied)")
        
        return True
    
    return False


def main():
    """Main function to process LaTeX files."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Fix over-escaping in LaTeX files')
    parser.add_argument('files', nargs='*', help='LaTeX files to process (default: all .tex files in modules/)')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be changed without applying fixes')
    parser.add_argument('--recursive', '-r', action='store_true', help='Process files recursively')
    
    args = parser.parse_args()
    
    if args.files:
        files_to_process = [Path(f) for f in args.files]
    else:
        # Default: process all .tex files in modules/
        modules_dir = Path('modules')
        if modules_dir.exists():
            pattern = '**/*.tex' if args.recursive else '*.tex'
            files_to_process = list(modules_dir.glob(pattern))
        else:
            print("No modules/ directory found and no files specified")
            return 1
    
    if not files_to_process:
        print("No LaTeX files found to process")
        return 1
    
    print(f"Processing {len(files_to_process)} files...")
    if args.dry_run:
        print("DRY RUN MODE - no changes will be applied")
    
    files_changed = 0
    for file_path in files_to_process:
        if file_path.suffix == '.tex' and file_path.exists():
            if process_file(file_path, args.dry_run):
                files_changed += 1
    
    print(f"\nProcessing complete. {files_changed} files had over-escaping issues.")
    if args.dry_run and files_changed > 0:
        print("Run without --dry-run to apply the fixes.")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())