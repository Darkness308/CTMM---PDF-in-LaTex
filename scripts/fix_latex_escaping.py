#!/usr/bin/env python3
"""
CTMM LaTeX Escaping Fix Script
Fixes the over-escaping issue with \textbackslash{} sequences in LaTeX files.
This script can run without external dependencies like pandoc.
"""

import os
import re
import sys
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def clean_latex_escaping(latex_content):
    """
    Clean excessive LaTeX escaping from converted content.
    Fixes the \textbackslash{} over-escaping issue.
    """
    logger.info("Cleaning LaTeX escaping...")
    
    # Track how many fixes we make
    original_escapes = len(re.findall(r'\\textbackslash\{\}', latex_content))
    
    # Step 1: Replace all \textbackslash{} with simple backslash
    latex_content = re.sub(r'\\textbackslash\{\}', r'\\', latex_content)
    
    # Step 2: Fix remaining escaped braces
    # The pattern \{content\} should become {content}
    # But we need to be careful not to break actual escaped braces in LaTeX
    
    # Replace \\{ at the start of a group with {
    latex_content = re.sub(r'\\{', r'{', latex_content)
    
    # Replace \\} at the end of a group with }
    latex_content = re.sub(r'\\}', r'}', latex_content)
    
    # Step 3: Fix specific patterns like {\\% to {%
    latex_content = re.sub(r'{\\\%', r'{%', latex_content)
    
    remaining_escapes = len(re.findall(r'\\textbackslash\{\}', latex_content))
    fixes_made = original_escapes - remaining_escapes
    
    if fixes_made > 0:
        logger.info(f"Fixed {fixes_made} over-escaped LaTeX commands")
    else:
        logger.info("No over-escaping issues found")
    
    return latex_content


def create_sample_over_escaped_content():
    """Create sample over-escaped content to demonstrate the fix."""
    return """\\textbackslash{}hypertarget\\textbackslash{}{tool-23-trigger-management\\textbackslash{}}\\textbackslash{}{\\textbackslash{}%
\\textbackslash{}section\\textbackslash{}{\\textbackslash{}texorpdfstring\\textbackslash{}{📄 \\textbackslash{}textbf\\textbackslash{}{TOOL 23: TRIGGER-MANAGEMENT\\textbackslash{}}\\textbackslash{}}\\textbackslash{}{📄 TOOL 23: TRIGGER-MANAGEMENT\\textbackslash{}}\\textbackslash{}}\\textbackslash{}label\\textbackslash{}{tool-23-trigger-management\\textbackslash{}}\\textbackslash{}}

🧩 \\textbackslash{}emph\\textbackslash{}{\\textbackslash{}textbf\\textbackslash{}{Modul zur Selbsthilfe \\textbackslash{}\\textbackslash{}& Co-Regulation -- Klartextversion für beide Partner\\textbackslash{}}\\textbackslash{}}

\\textbackslash{}hypertarget\\textbackslash{}{ziel-nutzen\\textbackslash{}}\\textbackslash{}{\\textbackslash{}%
\\textbackslash{}subsection\\textbackslash{}{\\textbackslash{}texorpdfstring\\textbackslash{}{🎯 \\textbackslash{}textbf\\textbackslash{}{\\textbackslash{}ul\\textbackslash{}{ZIEL \\textbackslash{}\\textbackslash{}& NUTZEN\\textbackslash{}}\\textbackslash{}}\\textbackslash{}}\\textbackslash{}{🎯 ZIEL \\textbackslash{}\\textbackslash{}& NUTZEN\\textbackslash{}}\\textbackslash{}}\\textbackslash{}label\\textbackslash{}{ziel-nutzen\\textbackslash{}}\\textbackslash{}}

\\textbackslash{}textbf\\textbackslash{}{Trigger besser verstehen\\textbackslash{}}, körperliche/emotionale/mentale Reaktionen erkennen, passende Skills zuordnen -- zur Selbsthilfe, für Gespräche mit Therapeuten oder Partner.

\\textbackslash{}begin\\textbackslash{}{itemize\\textbackslash{}}
\\textbackslash{}tightlist
\\textbackslash{}item
  🟢 \\textbackslash{}textbf\\textbackslash{}{Grün\\textbackslash{}} = Alltag \\textbackslash{}\\textbackslash{}& Prävention → Kapitel \\textbackslash{}textbf\\textbackslash{}{2.2\\textbackslash{}}, \\textbackslash{}textbf\\textbackslash{}{2.4\\textbackslash{}}, \\textbackslash{}textbf\\textbackslash{}{Tool 24\\textbackslash{}}
\\textbackslash{}end\\textbackslash{}{itemize\\textbackslash{}}"""


def fix_existing_latex_file(tex_path):
    """Fix over-escaping in an existing LaTeX file."""
    try:
        with open(tex_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if the file has over-escaping issues
        if '\\textbackslash{}' in content:
            logger.info(f"Fixing over-escaping in {tex_path}")
            cleaned_content = clean_latex_escaping(content)
            
            # Create backup
            backup_path = str(tex_path) + '.backup'
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info(f"Created backup at {backup_path}")
            
            # Write cleaned content
            with open(tex_path, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)
            
            logger.info(f"Successfully fixed {tex_path}")
            return True
        else:
            logger.info(f"No over-escaping found in {tex_path}")
            return True
            
    except Exception as e:
        logger.error(f"Error fixing {tex_path}: {e}")
        return False


def create_sample_files():
    """Create sample files demonstrating the issue and the fix."""
    # Create converted directory
    output_dir = Path('converted')
    output_dir.mkdir(exist_ok=True)
    
    # Create sample files with over-escaped content based on the PR comments
    sample_files = {
        'Tool 23 Trigger Management.tex': create_sample_over_escaped_content(),
        'Tool 22 Safewords Signalsysteme CTMM.tex': """\\textbackslash{}hypertarget\\textbackslash{}{tool-22-safe-words-signalsysteme-ctmm-modul\\textbackslash{}}\\textbackslash{}{\\textbackslash{}%
\\textbackslash{}section\\textbackslash{}{\\textbackslash{}texorpdfstring\\textbackslash{}{\\textbackslash{}textbf\\textbackslash{}{🛑 TOOL 22 -- SAFE-WORDS \\textbackslash{}\\textbackslash{}& SIGNALSYSTEME (CTMM-MODUL)\\textbackslash{}}\\textbackslash{}}\\textbackslash{}{🛑 TOOL 22 -- SAFE-WORDS \\textbackslash{}\\textbackslash{}& SIGNALSYSTEME (CTMM-MODUL)\\textbackslash{}}\\textbackslash{}}\\textbackslash{}label\\textbackslash{}{tool-22-safe-words-signalsysteme-ctmm-modul\\textbackslash{}}\\textbackslash{}}

\\textbackslash{}begin\\textbackslash{}{quote\\textbackslash{}}
🧠 \\textbackslash{}textbf\\textbackslash{}{\\textbackslash{}ul\\textbackslash{}{Worum geht's hier -- für Freunde?\\textbackslash{}}\\textbackslash{}}\\textbackslash{}\\textbackslash{}
Safe-Words sind vereinbarte Codes oder Zeichen, die sofort signalisieren:
\\textbackslash{}end\\textbackslash{}{quote\\textbackslash{}}

\\textbackslash{}begin\\textbackslash{}{itemize\\textbackslash{}}
\\textbackslash{}item
  \\textbackslash{}begin\\textbackslash{}{quote\\textbackslash{}}
  \\textbackslash{}textbf\\textbackslash{}{„Ich kann nicht mehr``\\textbackslash{}}
  \\textbackslash{}end\\textbackslash{}{quote\\textbackslash{}}
\\textbackslash{}end\\textbackslash{}{itemize\\textbackslash{}}""",
        'README.tex': """\\textbackslash{}hypertarget\\textbackslash{}{ctmm-system\\textbackslash{}}\\textbackslash{}{\\textbackslash{}%
\\textbackslash{}section\\textbackslash{}{CTMM-System\\textbackslash{}}\\textbackslash{}label\\textbackslash{}{ctmm-system\\textbackslash{}}\\textbackslash{}}

Ein modulares LaTeX-Framework für Catch-Track-Map-Match Therapiematerialien.

\\textbackslash{}hypertarget\\textbackslash{}{uxfcberblick\\textbackslash{}}\\textbackslash{}{\\textbackslash{}%
\\textbackslash{}subsection\\textbackslash{}{Überblick\\textbackslash{}}\\textbackslash{}label\\textbackslash{}{uxfcberblick\\textbackslash{}}\\textbackslash{}}

Dieses Repository enthält ein vollständiges LaTeX-System zur Erstellung von CTMM-Therapiedokumenten, einschließlich:
- Depression \\textbackslash{}\\textbackslash{}& Stimmungstief Module
- Trigger-Management
- Bindungsdynamik
- Formularelemente für therapeutische Dokumentation"""
    }
    
    for filename, content in sample_files.items():
        file_path = output_dir / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        logger.info(f"Created sample file {file_path}")
    
    return list(sample_files.keys())


def demonstrate_fix():
    """Demonstrate the fix by creating sample files and fixing them."""
    logger.info("=== CTMM LaTeX Escaping Fix Demonstration ===")
    
    # Create sample files with over-escaping issues
    created_files = create_sample_files()
    
    # Show the issue exists
    logger.info("Sample files created with over-escaping issues.")
    
    # Fix each file
    output_dir = Path('converted')
    for filename in created_files:
        file_path = output_dir / filename
        if file_path.exists():
            fix_existing_latex_file(file_path)
    
    logger.info("=== Fix demonstration complete ===")


def main():
    """Main function - can be used to fix existing files or demonstrate the fix."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Fix LaTeX over-escaping issues')
    parser.add_argument('--demo', action='store_true', help='Create demo files and fix them')
    parser.add_argument('--fix-dir', type=str, help='Directory containing .tex files to fix')
    parser.add_argument('--fix-file', type=str, help='Specific .tex file to fix')
    
    args = parser.parse_args()
    
    if args.demo:
        demonstrate_fix()
    elif args.fix_dir:
        dir_path = Path(args.fix_dir)
        if not dir_path.exists():
            logger.error(f"Directory {dir_path} does not exist")
            return False
        
        fixed_count = 0
        for tex_file in dir_path.glob('*.tex'):
            if fix_existing_latex_file(tex_file):
                fixed_count += 1
        
        logger.info(f"Fixed {fixed_count} files in {dir_path}")
    elif args.fix_file:
        file_path = Path(args.fix_file)
        if not file_path.exists():
            logger.error(f"File {file_path} does not exist")
            return False
        
        fix_existing_latex_file(file_path)
    else:
        # Default: fix any existing converted files
        output_dir = Path('converted')
        if output_dir.exists():
            fixed_count = 0
            for tex_file in output_dir.glob('*.tex'):
                if fix_existing_latex_file(tex_file):
                    fixed_count += 1
            
            if fixed_count > 0:
                logger.info(f"Fixed {fixed_count} files in {output_dir}")
            else:
                logger.info("No files needed fixing")
        else:
            logger.info("No converted directory found. Use --demo to create sample files.")
    
    return True


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)