#!/usr/bin/env python3
r"""
CTMM LaTeX Escaping Fix Tool

This tool addresses the over-escaping issue mentioned in PR #3, where LaTeX commands
are excessively escaped with \textbackslash{} sequences making code unreadable.

Problem example:
\\textbackslash{}section\\textbackslash{}{Title\\textbackslash{}}

Should be:
\section{Title}

Usage:
    python3 fix_latex_escaping.py [file_or_directory]
"""

import re
import sys
import os
from pathlib import Path
import argparse
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def fix_latex_escaping(content):
    r"""
    Fix over-escaped LaTeX commands in content.
    
    Converts patterns like:
    \\textbackslash{}command\\textbackslash{}{argument\\textbackslash{}}
    
    Back to proper LaTeX:
    \command{argument}
    """
    # Track changes made
    original_length = len(content)
    
    # Pattern 1: Fix \\textbackslash{}command\\textbackslash{}{
    # Matches: \\textbackslash{}COMMAND\\textbackslash{}{
    content = re.sub(
        r'\\textbackslash\{\}([a-zA-Z]+)\\textbackslash\{\}\{',
        r'\\\1{',
        content
    )
    
    # Pattern 2: Fix argument endings \\textbackslash{}}
    # Matches: argument\\textbackslash{}}
    content = re.sub(
        r'([^\\])\\textbackslash\{\}\}',
        r'\1}',
        content
    )
    
    # Pattern 3: Fix standalone \\textbackslash{} at the end of lines
    content = re.sub(
        r'\\textbackslash\{\}$',
        r'\\',
        content,
        flags=re.MULTILINE
    )
    
    # Pattern 4: Fix escaped line breaks \\textbackslash{}\\textbackslash{}
    content = re.sub(
        r'\\textbackslash\{\}\\textbackslash\{\}',
        r'\\\\',
        content
    )
    
    # Pattern 5: Fix nested commands like \\textbackslash{}textbf\\textbackslash{}{
    content = re.sub(
        r'\\textbackslash\{\}([a-zA-Z]+)\\textbackslash\{\}\{([^}]+)\\textbackslash\{\}\}',
        r'\\\1{\2}',
        content
    )
    
    changes_made = original_length != len(content)
    return content, changes_made


def process_file(file_path):
    """Process a single LaTeX file to fix escaping issues."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        # Skip files that don't contain over-escaping
        if '\\textbackslash{}' not in original_content:
            logger.debug(f"Skipping {file_path} - no escaping issues found")
            return False
        
        fixed_content, changes_made = fix_latex_escaping(original_content)
        
        if changes_made:
            # Create backup
            backup_path = file_path.with_suffix(file_path.suffix + '.backup')
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(original_content)
            
            # Write fixed content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            
            logger.info(f"Fixed escaping in {file_path} (backup: {backup_path})")
            return True
        else:
            logger.debug(f"No changes needed for {file_path}")
            return False
            
    except Exception as e:
        logger.error(f"Error processing {file_path}: {e}")
        return False


def process_directory(directory_path):
    """Process all .tex files in a directory recursively."""
    tex_files = list(directory_path.rglob("*.tex"))
    
    if not tex_files:
        logger.warning(f"No .tex files found in {directory_path}")
        return 0
    
    fixed_count = 0
    for tex_file in tex_files:
        if process_file(tex_file):
            fixed_count += 1
    
    return fixed_count


def main():
    parser = argparse.ArgumentParser(
        description="Fix over-escaped LaTeX commands in .tex files"
    )
    parser.add_argument(
        'path',
        nargs='?',
        default='.',
        help='File or directory to process (default: current directory)'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be changed without making changes'
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    path = Path(args.path)
    
    if not path.exists():
        logger.error(f"Path does not exist: {path}")
        return 1
    
    if path.is_file():
        if args.dry_run:
            logger.info(f"Would process file: {path}")
            return 0
        
        success = process_file(path)
        return 0 if success else 1
    
    elif path.is_dir():
        if args.dry_run:
            tex_files = list(path.rglob("*.tex"))
            logger.info(f"Would process {len(tex_files)} .tex files in {path}")
            for tex_file in tex_files:
                with open(tex_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                if '\\textbackslash{}' in content:
                    logger.info(f"  - {tex_file} (has escaping issues)")
                else:
                    logger.debug(f"  - {tex_file} (clean)")
            return 0
        
        fixed_count = process_directory(path)
        logger.info(f"Fixed escaping in {fixed_count} files")
        return 0
    
    else:
        logger.error(f"Path is neither file nor directory: {path}")
        return 1


if __name__ == "__main__":
    sys.exit(main())