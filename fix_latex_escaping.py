#!/usr/bin/env python3
"""
LaTeX Escaping Fix Script for CTMM System

This script detects and fixes excessive LaTeX escaping patterns that can occur
during document conversion processes, particularly:
1. Over-escaped \textbackslash{} sequences
2. Redundant \texorpdfstring usage
3. Excessive hyperref escaping
4. Complex section header escaping

Author: CTMM Team
License: MIT
"""

import re
import sys
import os
import argparse
import shutil
from pathlib import Path
from typing import List, Tuple, Dict


class LaTeXEscapingFixer:
    """Fixes excessive LaTeX escaping patterns in .tex files."""
    
    def __init__(self, dry_run: bool = False, verbose: bool = False):
        self.dry_run = dry_run
        self.verbose = verbose
        self.issues_found = 0
        self.files_processed = 0
        
        # Define problematic patterns and their fixes
        self.escaping_patterns = [
            # Pattern 1: Over-escaped textbackslash sequences
            {
                'pattern': r'\\textbackslash\{\}([\\])',
                'replacement': r'\\\1',
                'description': 'Remove redundant \\textbackslash{} before backslashes'
            },
            
            # Pattern 2: Redundant texorpdfstring with simple text
            {
                'pattern': r'\\texorpdfstring\{([^{}]*)\}\{([^{}]*)\}',
                'replacement': lambda m: self._simplify_texorpdfstring(m.group(1), m.group(2)),
                'description': 'Simplify unnecessary \\texorpdfstring usage'
            },
            
            # Pattern 3: Over-escaped section titles
            {
                'pattern': r'\\hypertarget\{([^}]+)\}\{\s*%\s*\\section\{\\texorpdfstring\{([^}]+)\}\{([^}]+)\}\\label\{([^}]+)\}\}',
                'replacement': r'\\section{{\2}}\\label{{\4}}',
                'description': 'Simplify over-escaped section headers'
            },
            
            # Pattern 4: Double-escaped underscores
            {
                'pattern': r'\\textbackslash\{\}\\_',
                'replacement': r'\\_',
                'description': 'Fix double-escaped underscores'
            },
            
            # Pattern 5: Excessive line break escaping
            {
                'pattern': r'\\textbackslash\{\}\\\\',
                'replacement': r'\\\\',
                'description': 'Fix double-escaped line breaks'
            },
            
            # Pattern 6: Clean up redundant emph and textbf nesting
            {
                'pattern': r'\\emph\{\\textbf\{([^}]+)\}\}',
                'replacement': r'\\textbf{\\emph{\1}}',
                'description': 'Normalize emphasis and bold formatting'
            },
            
            # Pattern 7: Simplify complex subsection patterns
            {
                'pattern': r'\\hypertarget\{([^}]+)\}\{\s*%\s*\\subsection\{\\texorpdfstring\{([^}]+)\}\{([^}]+)\}\\label\{([^}]+)\}\}',
                'replacement': r'\\subsection{{\2}}\\label{{\4}}',
                'description': 'Simplify over-escaped subsection headers'
            },
        ]
    
    def _simplify_texorpdfstring(self, tex_version: str, pdf_version: str) -> str:
        """Decide whether texorpdfstring is necessary."""
        # Remove LaTeX commands from both versions for comparison
        tex_clean = re.sub(r'\\[a-zA-Z]+\{?([^}]*)\}?', r'\1', tex_version)
        pdf_clean = re.sub(r'\\[a-zA-Z]+\{?([^}]*)\}?', r'\1', pdf_version)
        
        # If the cleaned versions are similar, use the simpler one
        if tex_clean.strip() == pdf_clean.strip():
            # Use PDF version if it's simpler (fewer LaTeX commands)
            if len(re.findall(r'\\[a-zA-Z]+', pdf_version)) <= len(re.findall(r'\\[a-zA-Z]+', tex_version)):
                return pdf_version
            return tex_version
        else:
            # Keep texorpdfstring if versions are significantly different
            return f"\\texorpdfstring{{{tex_version}}}{{{pdf_version}}}"
    
    def detect_issues(self, content: str) -> List[Tuple[str, int]]:
        """Detect escaping issues in content."""
        issues = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            for pattern_info in self.escaping_patterns:
                pattern = pattern_info['pattern']
                if re.search(pattern, line):
                    issues.append((pattern_info['description'], i))
        
        return issues
    
    def fix_content(self, content: str) -> Tuple[str, int]:
        """Fix escaping issues in content."""
        fixed_content = content
        fixes_applied = 0
        
        for pattern_info in self.escaping_patterns:
            pattern = pattern_info['pattern']
            replacement = pattern_info['replacement']
            description = pattern_info['description']
            
            if callable(replacement):
                # Handle complex replacements
                def repl_func(match):
                    nonlocal fixes_applied
                    fixes_applied += 1
                    if self.verbose:
                        print(f"  - Applied: {description}")
                    return replacement(match)
                
                fixed_content = re.sub(pattern, repl_func, fixed_content)
            else:
                # Handle simple string replacements
                matches = len(re.findall(pattern, fixed_content))
                if matches > 0:
                    fixed_content = re.sub(pattern, replacement, fixed_content)
                    fixes_applied += matches
                    if self.verbose:
                        print(f"  - Applied {matches}x: {description}")
        
        return fixed_content, fixes_applied
    
    def process_file(self, file_path: Path) -> bool:
        """Process a single .tex file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return False
        
        self.files_processed += 1
        
        # Detect issues
        issues = self.detect_issues(original_content)
        if not issues and self.verbose:
            print(f"✓ {file_path}: No escaping issues found")
            return True
        
        if issues:
            print(f"Found {len(issues)} potential escaping issues in {file_path}:")
            for desc, line_num in issues:
                print(f"  Line {line_num}: {desc}")
        
        # Fix content
        fixed_content, fixes_applied = self.fix_content(original_content)
        
        if fixes_applied == 0:
            if self.verbose:
                print(f"✓ {file_path}: No fixes needed")
            return True
        
        self.issues_found += fixes_applied
        
        if self.dry_run:
            print(f"[DRY RUN] Would apply {fixes_applied} fixes to {file_path}")
            return True
        
        # Create backup
        backup_path = file_path.with_suffix('.tex.backup')
        shutil.copy2(file_path, backup_path)
        
        # Write fixed content
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            print(f"✓ Applied {fixes_applied} fixes to {file_path} (backup: {backup_path})")
            return True
        except Exception as e:
            print(f"Error writing {file_path}: {e}")
            # Restore from backup
            shutil.copy2(backup_path, file_path)
            return False
    
    def process_directory(self, directory: Path, recursive: bool = True) -> bool:
        """Process all .tex files in a directory."""
        if not directory.exists():
            print(f"Directory {directory} does not exist")
            return False
        
        pattern = "**/*.tex" if recursive else "*.tex"
        tex_files = list(directory.glob(pattern))
        
        if not tex_files:
            print(f"No .tex files found in {directory}")
            return True
        
        print(f"Processing {len(tex_files)} .tex files...")
        
        success = True
        for tex_file in sorted(tex_files):
            if not self.process_file(tex_file):
                success = False
        
        return success
    
    def generate_report(self) -> str:
        """Generate a summary report."""
        return f"""
LaTeX Escaping Fix Report
========================

Files processed: {self.files_processed}
Issues found and fixed: {self.issues_found}
Mode: {'DRY RUN' if self.dry_run else 'ACTUAL FIXES'}

Pattern fixes available:
{chr(10).join(f"- {p['description']}" for p in self.escaping_patterns)}
"""


def main():
    parser = argparse.ArgumentParser(
        description='Fix excessive LaTeX escaping in CTMM .tex files',
        epilog='Example: python3 fix_latex_escaping.py --target modules/ --recursive --verbose'
    )
    parser.add_argument(
        '--target', '-t',
        default='.',
        help='Target file or directory to process (default: current directory)'
    )
    parser.add_argument(
        '--recursive', '-r',
        action='store_true',
        help='Process directories recursively'
    )
    parser.add_argument(
        '--dry-run', '-n',
        action='store_true',
        help='Show what would be fixed without making changes'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed output'
    )
    parser.add_argument(
        '--backup-suffix',
        default='.backup',
        help='Suffix for backup files (default: .backup)'
    )
    
    args = parser.parse_args()
    
    # Initialize fixer
    fixer = LaTeXEscapingFixer(dry_run=args.dry_run, verbose=args.verbose)
    
    # Process target
    target_path = Path(args.target)
    
    if target_path.is_file():
        if not target_path.suffix == '.tex':
            print(f"Error: {target_path} is not a .tex file")
            sys.exit(1)
        success = fixer.process_file(target_path)
    elif target_path.is_dir():
        success = fixer.process_directory(target_path, args.recursive)
    else:
        print(f"Error: {target_path} does not exist")
        sys.exit(1)
    
    # Generate report
    print(fixer.generate_report())
    
    if not success:
        print("Some errors occurred during processing")
        sys.exit(1)
    
    if fixer.issues_found == 0:
        print("✓ No escaping issues found - LaTeX files are clean!")
    else:
        action = "would be fixed" if args.dry_run else "have been fixed"
        print(f"✓ {fixer.issues_found} escaping issues {action}")


if __name__ == '__main__':
    main()