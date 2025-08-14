#!/usr/bin/env python3
"""
LaTeX Escaping Fix Tool

This script fixes excessive escaping issues in LaTeX files that were created
by document conversion tools (like pandoc) that over-escape LaTeX commands.

The main problem addressed:
- Excessive \textbackslash{} sequences that make LaTeX code unreadable
- Over-escaped LaTeX commands that prevent proper compilation

Usage:
    python3 fix_latex_escaping.py [file_or_directory]
    python3 fix_latex_escaping.py --check [file_or_directory]  # Check only, don't fix
    python3 fix_latex_escaping.py --backup [file_or_directory] # Create backups
"""

import os
import re
import sys
import shutil
import argparse
from pathlib import Path
from typing import List, Tuple, Dict


class LaTeXEscapingFixer:
    """Fix excessive escaping in LaTeX files."""
    
    def __init__(self, create_backup: bool = False, dry_run: bool = False):
        self.create_backup = create_backup
        self.dry_run = dry_run
        self.fixes_applied = 0
        self.files_processed = 0
        
        # Common over-escaping patterns to fix
        self.escaping_patterns = [
            # Fix \textbackslash{} followed by actual LaTeX commands
            (r'\\textbackslash\{\}([a-zA-Z]+)\\textbackslash\{\}', r'\\\1'),
            
            # Fix \textbackslash{} at the start of LaTeX commands
            (r'\\textbackslash\{\}\\textbackslash\{\}([a-zA-Z]+)', r'\\\1'),
            
            # Fix double-escaped LaTeX commands
            (r'\\textbackslash\{\}([a-zA-Z]+)', r'\\\1'),
            
            # Fix over-escaped braces
            (r'\\textbackslash\{\}([{}])', r'\\\1'),
            
            # Fix specific patterns from the problematic files mentioned in PR
            (r'\\textbackslash\{\}hypertarget\\textbackslash\{\}', r'\\hypertarget'),
            (r'\\textbackslash\{\}section\\textbackslash\{\}', r'\\section'),
            (r'\\textbackslash\{\}subsection\\textbackslash\{\}', r'\\subsection'),
            (r'\\textbackslash\{\}begin\\textbackslash\{\}', r'\\begin'),
            (r'\\textbackslash\{\}end\\textbackslash\{\}', r'\\end'),
            (r'\\textbackslash\{\}textbf\\textbackslash\{\}', r'\\textbf'),
            (r'\\textbackslash\{\}emph\\textbackslash\{\}', r'\\emph'),
            (r'\\textbackslash\{\}item\\textbackslash\{\}', r'\\item'),
            (r'\\textbackslash\{\}label\\textbackslash\{\}', r'\\label'),
            (r'\\textbackslash\{\}texorpdfstring\\textbackslash\{\}', r'\\texorpdfstring'),
            (r'\\textbackslash\{\}ul\\textbackslash\{\}', r'\\ul'),
            (r'\\textbackslash\{\}texttt\\textbackslash\{\}', r'\\texttt'),
            (r'\\textbackslash\{\}tightlist\\textbackslash\{\}', r'\\tightlist'),
            
            # Fix escaped line breaks
            (r'\\textbackslash\{\}\\textbackslash\{\}', r'\\\\'),
            
            # Fix escaped percentages in comments
            (r'\\textbackslash\{\}%', r'%'),
        ]
    
    def fix_file_content(self, content: str) -> Tuple[str, int]:
        """Fix escaping issues in file content."""
        fixes_count = 0
        
        for pattern, replacement in self.escaping_patterns:
            new_content = re.sub(pattern, replacement, content)
            if new_content != content:
                matches = len(re.findall(pattern, content))
                fixes_count += matches
                content = new_content
                
        return content, fixes_count
    
    def process_file(self, file_path: Path) -> bool:
        """Process a single LaTeX file."""
        if not file_path.exists():
            print(f"Error: File {file_path} does not exist")
            return False
            
        if file_path.suffix.lower() not in self.LATEX_EXTENSIONS:
            print(f"Skipping non-LaTeX file: {file_path}")
            return True
            
        try:
            # Read file with UTF-8 encoding
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
        except UnicodeDecodeError:
            # Try with different encoding
            with open(file_path, 'r', encoding='latin-1') as f:
                original_content = f.read()
                
        # Fix escaping issues
        fixed_content, fixes_in_file = self.fix_file_content(original_content)
        
        if fixes_in_file > 0:
            print(f"Fixed {fixes_in_file} escaping issues in {file_path}")
            
            if not self.dry_run:
                # Create backup if requested
                if self.create_backup:
                    backup_path = file_path.with_suffix(file_path.suffix + '.backup')
                    shutil.copy2(file_path, backup_path)
                    print(f"  Created backup: {backup_path}")
                
                # Write fixed content
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                    
            self.fixes_applied += fixes_in_file
        else:
            print(f"No escaping issues found in {file_path}")
            
        self.files_processed += 1
        return True
    
    def process_directory(self, dir_path: Path) -> bool:
        """Process all LaTeX files in a directory."""
        if not dir_path.exists():
            print(f"Error: Directory {dir_path} does not exist")
            return False
            
        tex_files = list(dir_path.glob('**/*.tex')) + list(dir_path.glob('**/*.sty'))
        
        if not tex_files:
            print(f"No LaTeX files found in {dir_path}")
            return True
            
        print(f"Processing {len(tex_files)} LaTeX files in {dir_path}")
        
        for tex_file in tex_files:
            self.process_file(tex_file)
            
        return True
    
    def process(self, path: str) -> bool:
        """Process a file or directory."""
        path_obj = Path(path)
        
        if path_obj.is_file():
            return self.process_file(path_obj)
        elif path_obj.is_dir():
            return self.process_directory(path_obj)
        else:
            print(f"Error: {path} is neither a file nor a directory")
            return False
    
    def print_summary(self):
        """Print processing summary."""
        print(f"\n{'='*50}")
        print("LaTeX Escaping Fix Summary")
        print(f"{'='*50}")
        print(f"Files processed: {self.files_processed}")
        print(f"Total fixes applied: {self.fixes_applied}")
        
        if self.dry_run:
            print("Note: This was a dry run. No files were modified.")
        elif self.create_backup:
            print("Note: Backup files were created for modified files.")


def main():
    parser = argparse.ArgumentParser(
        description='Fix excessive LaTeX escaping issues',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 fix_latex_escaping.py converted/
  python3 fix_latex_escaping.py --check modules/
  python3 fix_latex_escaping.py --backup file.tex
        """
    )
    
    parser.add_argument('path', nargs='?', default='.',
                       help='File or directory to process (default: current directory)')
    parser.add_argument('--check', action='store_true',
                       help='Check for issues without fixing (dry run)')
    parser.add_argument('--backup', action='store_true',
                       help='Create backup files before fixing')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Verbose output')
    
    args = parser.parse_args()
    
    # Create fixer instance
    fixer = LaTeXEscapingFixer(
        create_backup=args.backup,
        dry_run=args.check
    )
    
    # Process the specified path
    print(f"LaTeX Escaping Fixer - Processing: {args.path}")
    if args.check:
        print("Running in CHECK mode - no files will be modified")
    
    success = fixer.process(args.path)
    fixer.print_summary()
    
    if not success:
        sys.exit(1)
    
    if fixer.fixes_applied > 0 and not args.check:
        print(f"\n✓ Successfully fixed {fixer.fixes_applied} escaping issues!")
        print("You should now test your LaTeX files to ensure they compile correctly.")
    elif fixer.fixes_applied > 0 and args.check:
        print(f"\n⚠ Found {fixer.fixes_applied} escaping issues that need fixing.")
        print("Run without --check to apply the fixes.")
    else:
        print("\n✓ No escaping issues found!")


if __name__ == "__main__":
    main()