#!/usr/bin/env python3
"""
LaTeX Document Conversion Workflow for CTMM Project

This script creates a workflow that addresses the systematic over-escaping
issue mentioned in GitHub issue #217. It demonstrates the conversion from
problematic over-escaped LaTeX to clean, readable LaTeX.

Usage:
    python3 conversion_workflow.py
"""

import os
import sys
from pathlib import Path
import logging

# Import our de-escaping tool
from fix_latex_escaping import LaTeXDeEscaper

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def create_sample_over_escaped_files():
    """Create sample files demonstrating the over-escaping issue."""
    
    converted_dir = Path('converted')
    converted_dir.mkdir(exist_ok=True)
    
    # Sample README file with over-escaping
    readme_content = """\\textbackslash{}hypertarget\\textbackslash{}{ctmm-system\\textbackslash{}}\\textbackslash{}{\\textbackslash{}%
\\textbackslash{}section\\textbackslash{}{CTMM-System\\textbackslash{}}\\textbackslash{}label\\textbackslash{}{ctmm-system\\textbackslash{}}\\textbackslash{}}

Ein modulares LaTeX-Framework f√ºr Catch-Track-Map-Match Therapiematerialien.

\\textbackslash{}hypertarget\\textbackslash{}{uxfcberblick\\textbackslash{}}\\textbackslash{}{\\textbackslash{}%
\\textbackslash{}subsection\\textbackslash{}{√úberblick\\textbackslash{}}\\textbackslash{}label\\textbackslash{}{uxfcberblick\\textbackslash{}}\\textbackslash{}}

Dieses Repository enth√§lt ein vollst√§ndiges LaTeX-System zur Erstellung von CTMM-Therapiedokumenten, einschlie√ülich:
- Depression \\textbackslash{}\\textbackslash{}& Stimmungstief Module
- Trigger-Management
- Bindungsdynamik
- Formularelemente f√ºr therapeutische Dokumentation

\\textbackslash{}hypertarget\\textbackslash{}{verwendung\\textbackslash{}}\\textbackslash{}{\\textbackslash{}%
\\textbackslash{}subsection\\textbackslash{}{Verwendung\\textbackslash{}}\\textbackslash{}label\\textbackslash{}{verwendung\\textbackslash{}}\\textbackslash{}}

\\textbackslash{}begin\\textbackslash{}{enumerate\\textbackslash{}}
\\textbackslash{}def\\textbackslash{}labelenumi\\textbackslash{}{\\textbackslash{}arabic\\textbackslash{}{enumi\\textbackslash{}}.\\textbackslash{}}
\\textbackslash{}tightlist
\\textbackslash{}item
  Klone das Repository
\\textbackslash{}item
  Kompiliere main.tex mit einem LaTeX-Editor
\\textbackslash{}item
  Oder √∂ffne das Projekt in einem GitHub Codespace
\\textbackslash{}end\\textbackslash{}{enumerate\\textbackslash{}}

\\textbackslash{}hypertarget\\textbackslash{}{struktur\\textbackslash{}}\\textbackslash{}{\\textbackslash{}%
\\textbackslash{}subsection\\textbackslash{}{Struktur\\textbackslash{}}\\textbackslash{}label\\textbackslash{}{struktur\\textbackslash{}}\\textbackslash{}}

\\textbackslash{}begin\\textbackslash{}{itemize\\textbackslash{}}
\\textbackslash{}tightlist
\\textbackslash{}item
  \\textbackslash{}texttt\\textbackslash{}{/style/\\textbackslash{}} - Design-Dateien und gemeinsam verwendete Komponenten
\\textbackslash{}item
  \\textbackslash{}texttt\\textbackslash{}{/modules/\\textbackslash{}} - Individuelle CTMM-Module als separate .tex-Dateien
\\textbackslash{}item
  \\textbackslash{}texttt\\textbackslash{}{/assets/\\textbackslash{}} - Diagramme und visuelle Elemente
\\textbackslash{}end\\textbackslash{}{itemize\\textbackslash{}}

\\textbackslash{}hypertarget\\textbackslash{}{anforderungen\\textbackslash{}}\\textbackslash{}{\\textbackslash{}%
\\textbackslash{}subsection\\textbackslash{}{Anforderungen\\textbackslash{}}\\textbackslash{}label\\textbackslash{}{anforderungen\\textbackslash{}}\\textbackslash{}}"""

    # Sample Safewords file with over-escaping
    safewords_content = """\\textbackslash{}hypertarget\\textbackslash{}{tool-22-safe-words-signalsysteme-ctmm-modul\\textbackslash{}}\\textbackslash{}{\\textbackslash{}%
\\textbackslash{}section\\textbackslash{}{\\textbackslash{}texorpdfstring\\textbackslash{}{\\textbackslash{}textbf\\textbackslash{}{üõë TOOL 22 -- SAFE-WORDS \\textbackslash{}\\textbackslash{}& SIGNALSYSTEME (CTMM-MODUL)\\textbackslash{}}\\textbackslash{}}\\textbackslash{}{üõë TOOL 22 -- SAFE-WORDS \\textbackslash{}\\textbackslash{}& SIGNALSYSTEME (CTMM-MODUL)\\textbackslash{}}\\textbackslash{}}\\textbackslash{}label\\textbackslash{}{tool-22-safe-words-signalsysteme-ctmm-modul\\textbackslash{}}\\textbackslash{}}

\\textbackslash{}begin\\textbackslash{}{quote\\textbackslash{}}
üß† \\textbackslash{}textbf\\textbackslash{}{\\textbackslash{}ul\\textbackslash{}{Worum geht's hier -- f√ºr Freunde?\\textbackslash{}}\\textbackslash{}}\\textbackslash{}\\textbackslash{}
Safe-Words sind vereinbarte Codes oder Zeichen, die sofort signalisieren:
\\textbackslash{}end\\textbackslash{}{quote\\textbackslash{}}

\\textbackslash{}begin\\textbackslash{}{itemize\\textbackslash{}}
\\textbackslash{}item
  \\textbackslash{}begin\\textbackslash{}{quote\\textbackslash{}}
  \\textbackslash{}textbf\\textbackslash{}{‚ÄûIch kann nicht mehr``\\textbackslash{}}
  \\textbackslash{}end\\textbackslash{}{quote\\textbackslash{}}
\\textbackslash{}item
  \\textbackslash{}begin\\textbackslash{}{quote\\textbackslash{}}
  \\textbackslash{}textbf\\textbackslash{}{‚ÄûIch brauch Ruhe`` oder\\textbackslash{}}
  \\textbackslash{}end\\textbackslash{}{quote\\textbackslash{}}
\\textbackslash{}item
  \\textbackslash{}begin\\textbackslash{}{quote\\textbackslash{}}
  \\textbackslash{}textbf\\textbackslash{}{‚ÄûStopp -- das wird mir zu viel``\\textbackslash{}}
  \\textbackslash{}end\\textbackslash{}{quote\\textbackslash{}}
\\textbackslash{}end\\textbackslash{}{itemize\\textbackslash{}}

\\textbackslash{}begin\\textbackslash{}{quote\\textbackslash{}}
Sie sch√ºtzen vor Eskalation, √úberforderung, R√ºckzug oder Missverst√§ndnissen -- ohne viele Worte.
\\textbackslash{}end\\textbackslash{}{quote\\textbackslash{}}

üß© \\textbackslash{}textbf\\textbackslash{}{Zentraler Bestandteil der Eskalationspr√§vention -- mit Symbol- und Notfallsystem\\textbackslash{}}

\\textbackslash{}hypertarget\\textbackslash{}{kapitelzuordnung-im-ctmm-system\\textbackslash{}}\\textbackslash{}{\\textbackslash{}%"""

    # Write the sample files
    with open(converted_dir / 'README.tex', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    with open(converted_dir / 'Tool_22_Safewords_Signalsysteme_CTMM.tex', 'w', encoding='utf-8') as f:
        f.write(safewords_content)
    
    logger.info(f"Created sample over-escaped files in {converted_dir}")
    return converted_dir

def demonstrate_workflow():
    """Demonstrate the complete workflow for fixing over-escaped LaTeX files."""
    
    print("="*60)
    print("CTMM LaTeX De-escaping Workflow Demonstration")
    print("="*60)
    
    # Step 1: Create sample files demonstrating the problem
    print("\n1. Creating sample files with over-escaping issues...")
    converted_dir = create_sample_over_escaped_files()
    
    # List the files before processing
    tex_files = list(converted_dir.glob('*.tex'))
    print(f"   Found {len(tex_files)} files to process:")
    for file in tex_files:
        print(f"   - {file.name}")
    
    # Step 2: Show a sample of the problematic content
    print("\n2. Example of over-escaped content (first few lines):")
    sample_file = tex_files[0]
    with open(sample_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()[:5]
    for i, line in enumerate(lines, 1):
        print(f"   {i:2d}: {line.rstrip()}")
    
    print("\n   ‚ùå Problem: Excessive \\textbackslash{} escaping makes code unreadable")
    
    # Step 3: Apply the fix
    print("\n3. Applying de-escaping fixes...")
    de_escaper = LaTeXDeEscaper()
    stats = de_escaper.process_directory(converted_dir)
    
    # Step 4: Show the fixed content
    print("\n4. Fixed content (first few lines):")
    with open(sample_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()[:5]
    for i, line in enumerate(lines, 1):
        print(f"   {i:2d}: {line.rstrip()}")
    
    print("\n   ‚úÖ Result: Clean, readable LaTeX code")
    
    # Step 5: Summary
    print("\n5. Processing Summary:")
    print(f"   Files processed: {stats['files_processed']}")
    print(f"   Files changed: {stats['files_changed']}")
    print(f"   Total replacements: {stats['total_replacements']}")
    
    # Step 6: Validation
    print("\n6. Validation:")
    for tex_file in tex_files:
        issues = de_escaper.validate_latex_syntax(tex_file)
        status = "‚úÖ OK" if not issues else f"‚ö†Ô∏è  {', '.join(issues)}"
        print(f"   {tex_file.name}: {status}")
    
    print("\n" + "="*60)
    print("Workflow completed successfully!")
    print("="*60)
    
    print("\nNext steps:")
    print("- Review the fixed files in the converted/ directory")
    print("- Test compilation with your LaTeX environment")
    print("- Apply this workflow to other converted documents")
    print("- Configure conversion tools to prevent over-escaping")

if __name__ == '__main__':
    try:
        demonstrate_workflow()
    except Exception as e:
        logger.error(f"Workflow failed: {e}")
        sys.exit(1)