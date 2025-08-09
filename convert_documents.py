#!/usr/bin/env python3
"""
CTMM Document Conversion Tool
Converts .docx files to clean, readable LaTeX without over-escaping issues.

This script addresses the LaTeX over-escaping problem identified in PR #3,
where conversion tools were producing unreadable LaTeX with excessive 
\textbackslash{} escaping.
"""

import os
import re
import subprocess
import sys
from pathlib import Path
import tempfile
import shutil
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def clean_latex_escaping(latex_content):
    """
    Clean over-escaped LaTeX commands to produce readable, maintainable code.
    
    Fixes the specific over-escaping issue where:
    \\textbackslash{}hypertarget\\textbackslash{}{tool-23}
    becomes:
    \\hypertarget{tool-23}
    """
    
    # Fix over-escaped LaTeX commands
    # Pattern: \textbackslash{}command\textbackslash{} -> \command
    latex_content = re.sub(r'\\textbackslash\{\}([a-zA-Z]+)\\textbackslash\{\}', r'\\\1', latex_content)
    
    # Fix over-escaped braces: \textbackslash{}{content\textbackslash{}} -> {content}
    latex_content = re.sub(r'\\textbackslash\{\}\{([^}]*?)\\textbackslash\{\}\}', r'{\1}', latex_content)
    
    # Fix remaining textbackslash patterns
    latex_content = re.sub(r'\\textbackslash\{\}', '', latex_content)
    
    # Fix double backslashes in regular text (not LaTeX commands)
    latex_content = re.sub(r'(?<!\\)\\\\(?!\\)', r'\\', latex_content)
    
    # Handle Unicode characters that cause LaTeX issues
    # Replace emojis and special Unicode with LaTeX-compatible alternatives
    unicode_replacements = {
        # Common emojis to simple text or basic symbols
        '📄': '[Document]',
        '🎯': '[Target]',
        '🧭': '[Navigation]',
        '🟢': '\\textcolor{green}{$\\bullet$}',
        '🟠': '\\textcolor{orange}{$\\bullet$}',
        '🔴': '\\textcolor{red}{$\\bullet$}',
        '💡': '[Idea]',
        '🧩': '[Module]',
        '🧠': '[Brain]',
        '🛑': '[Stop]',
        '📘': '[Book]',
        '🗓️': '[Calendar]',
        '📝': '[Note]',
        '✅': '[Check]',
        '❌': '[X]',
        '🔄': '[Refresh]',
        '📞': '[Phone]',
        '💬': '[Chat]',
        '⚠️': '[Warning]',
        '✋': '[Hand]',
        '🔢': '[Numbers]',
        '📊': '[Chart]',
        '📈': '[Graph]',
        '💪': '[Strength]',
        '🏠': '[Home]',
        '👥': '[People]',
        '💚': '[Green Heart]',
        '💙': '[Blue Heart]',
        '❤️': '[Red Heart]',
        '💛': '[Yellow Heart]',
        '🔗': '[Link]',
        '📋': '[List]',
        '🎨': '[Art]',
        '⭐': '[Star]',
        '🔍': '[Search]',
        '📌': '[Pin]',
        '🚨': '[Alert]',
        '🎪': '[Circus]',
        '🌟': '[Star]',
        # Arrows and symbols
        '→': '$\\rightarrow$',
        '↔': '$\\leftrightarrow$',
        '←': '$\\leftarrow$',
        '↑': '$\\uparrow$',
        '↓': '$\\downarrow$',
        '•': '$\\bullet$',
        '◦': '$\\circ$',
        '–': '--',
        '—': '---',
        '"': '``',
        '"': "''",
        ''': '`',
        ''': "'",
        '…': '\\ldots',
        '§': '\\S',
        '°': '$^\\circ$',
        '±': '$\\pm$',
        '×': '$\\times$',
        '÷': '$\\div$',
        '≤': '$\\leq$',
        '≥': '$\\geq$',
        '≠': '$\\neq$',
        '≈': '$\\approx$',
        '∞': '$\\infty$',
        '√': '$\\sqrt{}$',
        '²': '$^2$',
        '³': '$^3$',
        '¼': '$\\frac{1}{4}$',
        '½': '$\\frac{1}{2}$',
        '¾': '$\\frac{3}{4}$',
    }
    
    for unicode_char, latex_replacement in unicode_replacements.items():
        latex_content = latex_content.replace(unicode_char, latex_replacement)
    
    # Remove any remaining problematic Unicode characters (emojis, etc.)
    # This regex matches emoji and other non-standard Unicode characters
    import unicodedata
    
    # Remove characters that are not in basic Latin, Latin-1 Supplement, 
    # Latin Extended-A/B, or mathematical symbols
    def is_safe_unicode(char):
        # Allow basic ASCII, Latin characters, and common mathematical symbols
        code = ord(char)
        return (
            code < 0x0300 or  # Basic Latin + Latin-1
            (0x0370 <= code <= 0x03FF) or  # Greek
            (0x2000 <= code <= 0x206F) or  # General Punctuation
            (0x2070 <= code <= 0x209F) or  # Superscripts/Subscripts
            (0x20A0 <= code <= 0x20CF) or  # Currency Symbols
            (0x2100 <= code <= 0x214F) or  # Letterlike Symbols
            (0x2190 <= code <= 0x21FF) or  # Arrows
            (0x2200 <= code <= 0x22FF) or  # Mathematical Operators
            unicodedata.category(char)[0] in 'LN'  # Letters and Numbers
        )
    
    # Filter out unsafe Unicode characters
    filtered_chars = []
    for char in latex_content:
        if is_safe_unicode(char):
            filtered_chars.append(char)
        else:
            # Replace with a generic placeholder for debugging
            filtered_chars.append('[?]')
    
    latex_content = ''.join(filtered_chars)
    
    # Clean up excessive whitespace and newlines
    latex_content = re.sub(r'\n\s*\n\s*\n', '\n\n', latex_content)
    
    return latex_content


def convert_docx_to_latex(docx_path, output_path):
    """
    Convert a .docx file to clean LaTeX using pandoc and post-processing.
    """
    try:
        # Use pandoc to convert .docx to LaTeX
        cmd = [
            'pandoc',
            str(docx_path),
            '-f', 'docx',
            '-t', 'latex',
            '--wrap=none',
            '--no-highlight',
            '-o', str(output_path)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        # Read the generated LaTeX
        with open(output_path, 'r', encoding='utf-8') as f:
            latex_content = f.read()
        
        # Clean the over-escaping
        clean_content = clean_latex_escaping(latex_content)
        
        # Write back the cleaned content
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(clean_content)
        
        logger.info(f"✓ Converted {docx_path.name} -> {output_path.name}")
        return True
        
    except subprocess.CalledProcessError as e:
        logger.error(f"✗ Pandoc conversion failed for {docx_path.name}: {e}")
        return False
    except Exception as e:
        logger.error(f"✗ Error converting {docx_path.name}: {e}")
        return False


def convert_markdown_to_latex(md_path, output_path):
    """
    Convert a .md file to clean LaTeX using pandoc.
    """
    try:
        cmd = [
            'pandoc',
            str(md_path),
            '-f', 'markdown',
            '-t', 'latex',
            '--wrap=none',
            '--no-highlight',
            '-o', str(output_path)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        # Read and clean the LaTeX
        with open(output_path, 'r', encoding='utf-8') as f:
            latex_content = f.read()
        
        clean_content = clean_latex_escaping(latex_content)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(clean_content)
        
        logger.info(f"✓ Converted {md_path.name} -> {output_path.name}")
        return True
        
    except Exception as e:
        logger.error(f"✗ Error converting {md_path.name}: {e}")
        return False


def main():
    """
    Main conversion process.
    """
    logger.info("🔄 Starting CTMM Document Conversion...")
    
    # Create converted directory
    converted_dir = Path("converted")
    converted_dir.mkdir(exist_ok=True)
    
    # Find source documents
    therapie_material_dir = Path("therapie-material")
    
    if not therapie_material_dir.exists():
        logger.error("therapie-material directory not found!")
        return 1
    
    # Convert .docx files
    docx_files = list(therapie_material_dir.glob("*.docx"))
    converted_count = 0
    
    for docx_file in docx_files:
        output_name = docx_file.stem + ".tex"
        output_path = converted_dir / output_name
        
        if convert_docx_to_latex(docx_file, output_path):
            converted_count += 1
    
    # Convert .md files
    md_files = [Path("README.md")]  # Add other MD files as needed
    
    for md_file in md_files:
        if md_file.exists():
            output_name = md_file.stem + ".tex"
            output_path = converted_dir / output_name
            
            if convert_markdown_to_latex(md_file, output_path):
                converted_count += 1
    
    # Summary
    total_files = len(docx_files) + len([f for f in md_files if f.exists()])
    logger.info(f"")
    logger.info(f"🎯 Conversion Summary:")
    logger.info(f"   Total files: {total_files}")
    logger.info(f"   Converted: {converted_count}")
    logger.info(f"   Success rate: {converted_count/total_files*100:.1f}%")
    logger.info(f"   Output directory: {converted_dir.absolute()}")
    
    return 0 if converted_count > 0 else 1


if __name__ == "__main__":
    sys.exit(main())