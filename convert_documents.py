#!/usr/bin/env python3
"""
CTMM Document Converter

Converts Word documents and Markdown files to clean LaTeX format
without over-escaping issues. This addresses the conversion problems
mentioned in PR #3.

Features:
- Safe conversion of .docx and .md files to LaTeX
- Proper LaTeX command generation (no over-escaping)
- Preservation of document structure
- German language support
- CTMM-specific formatting

Usage:
    python3 convert_documents.py therapie-material/
"""

import re
import sys
import os
from pathlib import Path
import argparse
import logging
import zipfile
import xml.etree.ElementTree as ET

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def clean_text_for_latex(text):
    """Clean and escape text properly for LaTeX without over-escaping."""
    if not text:
        return ""
    
    # Handle special characters properly
    replacements = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '^': r'\textasciicircum{}',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '\\': r'\textbackslash{}',
        '„': r'"`',  # German opening quote
        '"': r'"\'',  # German closing quote
        '–': r'--',   # en-dash
        '—': r'---',  # em-dash
    }
    
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)
    
    return text


def extract_text_from_docx(docx_path):
    """Extract text from a Word document (.docx)."""
    try:
        with zipfile.ZipFile(docx_path, 'r') as zip_file:
            # Read the main document
            xml_content = zip_file.read('word/document.xml')
            root = ET.fromstring(xml_content)
            
            # Define namespace
            namespace = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            
            # Extract text from paragraphs
            paragraphs = []
            for para in root.findall('.//w:p', namespace):
                para_text = ""
                for text_elem in para.findall('.//w:t', namespace):
                    if text_elem.text:
                        para_text += text_elem.text
                
                if para_text.strip():
                    paragraphs.append(para_text.strip())
            
            return paragraphs
            
    except Exception as e:
        logger.error(f"Error extracting text from {docx_path}: {e}")
        return []


def convert_markdown_to_latex(md_content):
    """Convert Markdown content to LaTeX."""
    lines = md_content.split('\n')
    latex_lines = []
    
    for line in lines:
        line = line.strip()
        if not line:
            latex_lines.append('')
            continue
        
        # Headers
        if line.startswith('# '):
            title = clean_text_for_latex(line[2:])
            latex_lines.append(f'\\section{{{title}}}')
        elif line.startswith('## '):
            title = clean_text_for_latex(line[3:])
            latex_lines.append(f'\\subsection{{{title}}}')
        elif line.startswith('### '):
            title = clean_text_for_latex(line[4:])
            latex_lines.append(f'\\subsubsection{{{title}}}')
        elif line.startswith('- '):
            # List item
            text = clean_text_for_latex(line[2:])
            if not any(l.strip().startswith('\\begin{itemize}') for l in latex_lines[-3:]):
                latex_lines.append('\\begin{itemize}')
            latex_lines.append(f'\\item {text}')
        elif line.startswith('**') and line.endswith('**'):
            # Bold text
            text = clean_text_for_latex(line[2:-2])
            latex_lines.append(f'\\textbf{{{text}}}')
        else:
            # Regular paragraph
            text = clean_text_for_latex(line)
            latex_lines.append(text)
    
    # Close any open itemize
    if any('\\begin{itemize}' in line for line in latex_lines) and not any('\\end{itemize}' in line for line in latex_lines):
        latex_lines.append('\\end{itemize}')
    
    return '\n'.join(latex_lines)


def paragraphs_to_latex(paragraphs, title="Converted Document"):
    """Convert a list of paragraphs to LaTeX format."""
    latex_content = []
    
    # Document header
    latex_content.append(f'\\section{{{clean_text_for_latex(title)}}}')
    latex_content.append('')
    
    in_list = False
    
    for para in paragraphs:
        if not para.strip():
            continue
        
        # Detect headings (all caps, short lines)
        if para.isupper() and len(para) < 80:
            if in_list:
                latex_content.append('\\end{itemize}')
                in_list = False
            latex_content.append(f'\\subsection{{{clean_text_for_latex(para)}}}')
            latex_content.append('')
        
        # Detect list items (start with bullet or number)
        elif re.match(r'^[•·▪▫-]\s+', para) or re.match(r'^\d+[\.)]\s+', para):
            if not in_list:
                latex_content.append('\\begin{itemize}')
                in_list = True
            
            # Clean the bullet point
            item_text = re.sub(r'^[•·▪▫-]\s+', '', para)
            item_text = re.sub(r'^\d+[\.)]\s+', '', item_text)
            latex_content.append(f'\\item {clean_text_for_latex(item_text)}')
        
        # Regular paragraph
        else:
            if in_list:
                latex_content.append('\\end{itemize}')
                latex_content.append('')
                in_list = False
            
            # Check for bold formatting indicators
            if '**' in para or para.startswith('🎯') or para.startswith('📄'):
                latex_content.append(f'\\textbf{{{clean_text_for_latex(para)}}}')
            else:
                latex_content.append(clean_text_for_latex(para))
            latex_content.append('')
    
    if in_list:
        latex_content.append('\\end{itemize}')
    
    return '\n'.join(latex_content)


def convert_file(input_path, output_dir):
    """Convert a single file to LaTeX."""
    input_path = Path(input_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)
    
    # Generate output filename
    output_name = input_path.stem + '.tex'
    output_path = output_dir / output_name
    
    try:
        if input_path.suffix.lower() == '.docx':
            logger.info(f"Converting Word document: {input_path}")
            paragraphs = extract_text_from_docx(input_path)
            if not paragraphs:
                logger.warning(f"No content extracted from {input_path}")
                return False
            
            latex_content = paragraphs_to_latex(paragraphs, input_path.stem)
        
        elif input_path.suffix.lower() in ['.md', '.markdown']:
            logger.info(f"Converting Markdown document: {input_path}")
            with open(input_path, 'r', encoding='utf-8') as f:
                md_content = f.read()
            
            latex_content = convert_markdown_to_latex(md_content)
        
        else:
            logger.warning(f"Unsupported file type: {input_path}")
            return False
        
        # Write the converted content
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(latex_content)
        
        logger.info(f"Converted to: {output_path}")
        return True
        
    except Exception as e:
        logger.error(f"Error converting {input_path}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Convert Word documents and Markdown files to clean LaTeX"
    )
    parser.add_argument(
        'input_path',
        help='Input file or directory to convert'
    )
    parser.add_argument(
        '--output', '-o',
        default='converted',
        help='Output directory (default: converted/)'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    input_path = Path(args.input_path)
    output_dir = Path(args.output)
    
    if not input_path.exists():
        logger.error(f"Input path does not exist: {input_path}")
        return 1
    
    success_count = 0
    total_count = 0
    
    if input_path.is_file():
        total_count = 1
        if convert_file(input_path, output_dir):
            success_count = 1
    
    elif input_path.is_dir():
        # Find all supported files
        supported_extensions = ['.docx', '.md', '.markdown']
        files_to_convert = []
        
        for ext in supported_extensions:
            files_to_convert.extend(input_path.glob(f'*{ext}'))
        
        if not files_to_convert:
            logger.warning(f"No supported files found in {input_path}")
            return 1
        
        total_count = len(files_to_convert)
        for file_path in files_to_convert:
            if convert_file(file_path, output_dir):
                success_count += 1
    
    logger.info(f"Conversion complete: {success_count}/{total_count} files converted successfully")
    
    # Generate integration file
    if success_count > 0:
        integration_file = output_dir / 'converted_documents.tex'
        with open(integration_file, 'w', encoding='utf-8') as f:
            f.write('% Converted Documents - Include in main document\n')
            f.write('% Generated by CTMM Document Converter\n\n')
            
            for tex_file in output_dir.glob('*.tex'):
                if tex_file.name != 'converted_documents.tex':
                    f.write(f'\\input{{{output_dir.name}/{tex_file.stem}}}\n')
        
        logger.info(f"Integration file created: {integration_file}")
    
    return 0 if success_count > 0 else 1


if __name__ == "__main__":
    sys.exit(main())