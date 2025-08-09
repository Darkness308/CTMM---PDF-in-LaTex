#!/usr/bin/env python3
"""
CTMM Document Conversion Script
Converts Word documents (.docx) and Markdown files to clean LaTeX format.
Fixes the over-escaping issue with \textbackslash{} sequences.
"""

import os
import re
import subprocess
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
    # Fix over-escaped LaTeX commands
    # Replace \textbackslash{} with \
    latex_content = re.sub(r'\\textbackslash\{\}', r'\\', latex_content)
    
    # Fix over-escaped curly braces
    # Replace \\{ and \\} with { and }
    latex_content = re.sub(r'\\textbackslash\{', r'\\{', latex_content)
    latex_content = re.sub(r'\\textbackslash\}', r'\\}', latex_content)
    
    # Clean up multiple consecutive backslashes
    latex_content = re.sub(r'\\\\\\+', r'\\\\', latex_content)
    
    # Fix common LaTeX command patterns that get over-escaped
    patterns_to_fix = [
        (r'\\textbackslash\{\}hypertarget', r'\\hypertarget'),
        (r'\\textbackslash\{\}section', r'\\section'),
        (r'\\textbackslash\{\}subsection', r'\\subsection'),
        (r'\\textbackslash\{\}begin', r'\\begin'),
        (r'\\textbackslash\{\}end', r'\\end'),
        (r'\\textbackslash\{\}textbf', r'\\textbf'),
        (r'\\textbackslash\{\}emph', r'\\emph'),
        (r'\\textbackslash\{\}item', r'\\item'),
        (r'\\textbackslash\{\}label', r'\\label'),
        (r'\\textbackslash\{\}texorpdfstring', r'\\texorpdfstring'),
        (r'\\textbackslash\{\}ul', r'\\ul'),
        (r'\\textbackslash\{\}texttt', r'\\texttt'),
        (r'\\textbackslash\{\}tightlist', r'\\tightlist'),
        (r'\\textbackslash\{\}def', r'\\def'),
        (r'\\textbackslash\{\}labelenumi', r'\\labelenumi'),
        (r'\\textbackslash\{\}arabic', r'\\arabic'),
    ]
    
    for pattern, replacement in patterns_to_fix:
        latex_content = re.sub(pattern, replacement, latex_content)
    
    # Fix escaped braces in command arguments
    # Replace patterns like \textbackslash{}{command\textbackslash{}} with {command}
    latex_content = re.sub(r'\\textbackslash\{\}\{([^}]+)\\textbackslash\{\}\}', r'{\1}', latex_content)
    
    return latex_content


def convert_docx_to_latex(docx_path, output_path):
    """Convert a DOCX file to LaTeX using pandoc."""
    try:
        # Check if pandoc is available
        subprocess.run(['pandoc', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        logger.error("Pandoc is not available. Please install pandoc to convert DOCX files.")
        return False
    
    try:
        # Convert using pandoc with clean LaTeX output
        cmd = [
            'pandoc',
            str(docx_path),
            '-f', 'docx',
            '-t', 'latex',
            '--wrap=none',  # Don't wrap lines
            '--standalone',  # Include document structure
            '-o', str(output_path)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        # Read the generated file and clean it
        with open(output_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Clean the excessive escaping
        cleaned_content = clean_latex_escaping(content)
        
        # Write the cleaned content back
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)
        
        logger.info(f"Successfully converted {docx_path} to {output_path}")
        return True
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Error converting {docx_path}: {e}")
        if e.stderr:
            logger.error(f"Error output: {e.stderr}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error converting {docx_path}: {e}")
        return False


def convert_markdown_to_latex(md_path, output_path):
    """Convert a Markdown file to LaTeX using pandoc."""
    try:
        # Check if pandoc is available
        subprocess.run(['pandoc', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        logger.error("Pandoc is not available. Please install pandoc to convert Markdown files.")
        return False
    
    try:
        # Convert using pandoc
        cmd = [
            'pandoc',
            str(md_path),
            '-f', 'markdown',
            '-t', 'latex',
            '--wrap=none',
            '--standalone',
            '-o', str(output_path)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        # Read and clean the content
        with open(output_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        cleaned_content = clean_latex_escaping(content)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)
        
        logger.info(f"Successfully converted {md_path} to {output_path}")
        return True
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Error converting {md_path}: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error converting {md_path}: {e}")
        return False


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


def main():
    """Main conversion function."""
    # Create output directory
    output_dir = Path('converted')
    output_dir.mkdir(exist_ok=True)
    
    # Find source materials
    source_dir = Path('therapie-material')
    if not source_dir.exists():
        logger.error(f"Source directory {source_dir} not found")
        return False
    
    success_count = 0
    total_count = 0
    
    # Convert DOCX files
    for docx_file in source_dir.glob('*.docx'):
        total_count += 1
        output_file = output_dir / (docx_file.stem + '.tex')
        if convert_docx_to_latex(docx_file, output_file):
            success_count += 1
    
    # Convert Markdown files
    for md_file in source_dir.glob('*.md'):
        total_count += 1
        output_file = output_dir / (md_file.stem + '.tex')
        if convert_markdown_to_latex(md_file, output_file):
            success_count += 1
    
    # Also convert README.md if it exists
    readme_path = Path('README.md')
    if readme_path.exists():
        total_count += 1
        output_file = output_dir / 'README.tex'
        if convert_markdown_to_latex(readme_path, output_file):
            success_count += 1
    
    # Fix any existing converted files that have over-escaping
    for tex_file in output_dir.glob('*.tex'):
        fix_existing_latex_file(tex_file)
    
    logger.info(f"Conversion complete: {success_count}/{total_count} files converted successfully")
    return success_count == total_count


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)