#!/usr/bin/env python3
"""
CTMM Document Converter
Converts Word documents and other formats to clean LaTeX without over-escaping.

This script fixes the over-escaping issue identified in PR #3 where LaTeX commands
were excessively escaped with \textbackslash{} sequences.
"""

import re
import sys
import subprocess
import os
from pathlib import Path
import logging
from typing import Dict, List
import tempfile

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


class CTMMDocumentConverter:
    """Converts documents to clean LaTeX for CTMM system."""
    
    def __init__(self, output_dir: str = "converted"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # LaTeX special characters mapping for proper escaping
        self.latex_special_chars = {
            # Basic escaping rules (minimal, proper escaping)
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
        }
        
        # Define patterns that should NOT be over-escaped
        self.latex_commands_pattern = re.compile(
            r'\\(section|subsection|subsubsection|textbf|textit|emph|item|begin|end|'
            r'hypertarget|label|texorpdfstring|ul|texttt|quad|hspace|vspace|newline|'
            r'tableofcontents|newpage|centering|par)'
        )
    
    def clean_over_escaped_latex(self, content: str) -> str:
        """Fix over-escaped LaTeX content by removing excessive escaping."""
        
        # Remove excessive \textbackslash{} escaping of LaTeX commands
        # Replace \textbackslash{}command with \command
        content = re.sub(r'\\textbackslash\{\}([a-zA-Z]+)', r'\\\1', content)
        
        # Fix over-escaped braces in commands
        # Replace \textbackslash{}{arg\textbackslash{}} with {arg}
        content = re.sub(r'\\textbackslash\{\}\{([^}]*?)\\textbackslash\{\}\}', r'{\1}', content)
        
        # Fix escaped braces that should be normal braces
        content = re.sub(r'\\textbackslash\{\}([{}])', r'\1', content)
        
        # Remove redundant escaping around standard LaTeX environments
        content = re.sub(r'\\textbackslash\{\}(begin|end)\\textbackslash\{\}\{([^}]+)\}\\textbackslash\{\}', 
                        r'\\\1{\2}', content)
        
        # Fix specific over-escaping patterns found in PR comments
        # Fix hypertarget escaping
        content = re.sub(
            r'\\textbackslash\{\}hypertarget\\textbackslash\{\}\{([^}]+)\\textbackslash\{\}\}\\textbackslash\{\}\{\\textbackslash\{\}%',
            r'\\hypertarget{\1}{%',
            content
        )
        
        # Fix section command escaping  
        content = re.sub(
            r'\\textbackslash\{\}section\\textbackslash\{\}\{([^}]+)\}\\textbackslash\{\}label\\textbackslash\{\}\{([^}]+)\}\\textbackslash\{\}\}',
            r'\\section{\1}\\label{\2}',
            content
        )
        
        # Fix texorpdfstring escaping
        content = re.sub(
            r'\\textbackslash\{\}texorpdfstring\\textbackslash\{\}\{([^}]+)\}\\textbackslash\{\}\{([^}]+)\}\\textbackslash\{\}',
            r'\\texorpdfstring{\1}{\2}',
            content
        )
        
        # Fix double braces in texorpdfstring (common issue)
        content = re.sub(r'\\texorpdfstring\{([^}]+)\}\{\{([^}]+)\}\}', r'\\texorpdfstring{\1}{\2}', content)
        
        # Fix item and other list escaping
        content = re.sub(r'\\textbackslash\{\}(item|tightlist)', r'\\\1', content)
        
        # Fix quote environment escaping
        content = re.sub(r'\\textbackslash\{\}(begin|end)\\textbackslash\{\}\{quote\\textbackslash\{\}\}', 
                        r'\\\1{quote}', content)
        
        # Fix itemize environment escaping
        content = re.sub(r'\\textbackslash\{\}(begin|end)\\textbackslash\{\}\{itemize\\textbackslash\{\}\}', 
                        r'\\\1{itemize}', content)
        
        # Fix textbf escaping
        content = re.sub(r'\\textbackslash\{\}textbf\\textbackslash\{\}\{([^}]+)\\textbackslash\{\}\}', 
                        r'\\textbf{\1}', content)
        
        # Fix emph escaping  
        content = re.sub(r'\\textbackslash\{\}emph\\textbackslash\{\}\{([^}]+)\\textbackslash\{\}\}', 
                        r'\\emph{\1}', content)
        
        # Fix texttt escaping
        content = re.sub(r'\\textbackslash\{\}texttt\\textbackslash\{\}\{([^}]+)\\textbackslash\{\}\}', 
                        r'\\texttt{\1}', content)
        
        # Clean up any remaining isolated \textbackslash{} that aren't part of proper escaping
        content = re.sub(r'\\textbackslash\{\}([^a-zA-Z\\])', r'\\\1', content)
        
        # Fix double escaping in line breaks
        content = re.sub(r'\\textbackslash\{\}\\textbackslash\{\}&', r'\\\\&', content)
        content = re.sub(r'\\textbackslash\{\}\\textbackslash\{\}', r'\\\\', content)
        
        # Clean up remaining isolated textbackslash sequences
        content = re.sub(r'\\textbackslash\{\}\\?', r'\\', content)
        
        return content
    
    def convert_word_document(self, docx_path: Path) -> str:
        """Convert Word document to clean LaTeX using pandoc."""
        try:
            # First try to convert with pandoc if available
            result = subprocess.run([
                'pandoc', 
                str(docx_path), 
                '-t', 'latex',
                '--wrap=none'
            ], capture_output=True, text=True, check=False)
            
            if result.returncode == 0:
                latex_content = result.stdout
                # Clean up the over-escaping
                clean_content = self.clean_over_escaped_latex(latex_content)
                return clean_content
            else:
                logger.warning(f"Pandoc conversion failed for {docx_path}: {result.stderr}")
                return self.create_placeholder_latex(docx_path)
                
        except FileNotFoundError:
            logger.warning("Pandoc not found, creating placeholder LaTeX")
            return self.create_placeholder_latex(docx_path)
    
    def create_placeholder_latex(self, original_path: Path) -> str:
        """Create a placeholder LaTeX file when conversion fails."""
        title = self.filename_to_title(original_path.stem)
        return f"""% Converted from {original_path.name}
% Note: Automatic conversion was not available, manual conversion needed

\\section{{{title}}}
\\label{{sec:{original_path.stem.lower().replace(' ', '-')}}}

\\begin{{center}}
\\textit{{Dieses Modul wurde aus {original_path.name} konvertiert.\\\\
Automatische Konvertierung war nicht verfügbar - manuelle Überarbeitung erforderlich.}}
\\end{{center}}

% TODO: Manual conversion of content from {original_path.name}
% Original file: {original_path}

\\subsection{{Placeholder-Inhalt}}

Dieser Inhalt muss manuell aus der ursprünglichen Datei übertragen werden.

\\begin{{itemize}}
\\item Bitte öffnen Sie die originale Datei: \\texttt{{{original_path.name}}}
\\item Übertragen Sie den Inhalt manuell in LaTeX-Format
\\item Entfernen Sie diese Platzhalter-Nachricht
\\end{{itemize}}
"""
    
    def filename_to_title(self, filename: str) -> str:
        """Convert filename to a readable title."""
        # Replace common separators with spaces
        title = filename.replace('_', ' ').replace('-', ' ')
        # Capitalize words properly
        return ' '.join(word.capitalize() for word in title.split())
    
    def convert_all_documents(self, source_dir: str = "therapie-material") -> List[str]:
        """Convert all Word documents in the source directory."""
        source_path = Path(source_dir)
        if not source_path.exists():
            logger.error(f"Source directory {source_dir} does not exist")
            return []
        
        converted_files = []
        
        # Find all Word documents
        docx_files = list(source_path.glob("*.docx"))
        if not docx_files:
            logger.warning(f"No .docx files found in {source_dir}")
            return []
        
        logger.info(f"Found {len(docx_files)} Word documents to convert")
        
        for docx_file in docx_files:
            logger.info(f"Converting {docx_file.name}...")
            
            # Convert to LaTeX
            latex_content = self.convert_word_document(docx_file)
            
            # Create output filename
            output_name = docx_file.stem + ".tex"
            output_path = self.output_dir / output_name
            
            # Write cleaned LaTeX content
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(latex_content)
            
            converted_files.append(str(output_path))
            logger.info(f"✓ Converted to {output_path}")
        
        return converted_files
    
    def create_integrated_file(self, converted_files: List[str]) -> str:
        """Create a single integrated LaTeX file from all converted documents."""
        integrated_path = self.output_dir / "all_converted_documents.tex"
        
        with open(integrated_path, 'w', encoding='utf-8') as f:
            f.write("% Integrated CTMM Documents - All Converted Content\n")
            f.write("% This file combines all converted therapy materials\n\n")
            
            for converted_file in converted_files:
                file_path = Path(converted_file)
                f.write(f"\n% ===== Content from {file_path.name} =====\n")
                
                try:
                    with open(converted_file, 'r', encoding='utf-8') as content_file:
                        content = content_file.read()
                        # Remove document class and preamble if present
                        content = re.sub(r'\\documentclass.*?\\begin\{document\}', '', content, flags=re.DOTALL)
                        content = re.sub(r'\\end\{document\}', '', content)
                        f.write(content)
                        f.write(f"\n% ===== End of {file_path.name} =====\n\n")
                except Exception as e:
                    logger.error(f"Error reading {converted_file}: {e}")
                    f.write(f"% Error including content from {file_path.name}: {e}\n\n")
        
        logger.info(f"✓ Created integrated file: {integrated_path}")
        return str(integrated_path)


def main():
    """Main conversion workflow."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Convert CTMM documents to clean LaTeX')
    parser.add_argument('--source', default='therapie-material', 
                       help='Source directory containing Word documents')
    parser.add_argument('--output', default='converted', 
                       help='Output directory for LaTeX files')
    parser.add_argument('--clean', action='store_true',
                       help='Clean existing over-escaped LaTeX files')
    parser.add_argument('--file', help='Convert single file')
    
    args = parser.parse_args()
    
    converter = CTMMDocumentConverter(args.output)
    
    if args.clean:
        # Clean existing files in output directory
        logger.info("Cleaning existing over-escaped LaTeX files...")
        tex_files = list(Path(args.output).glob("*.tex"))
        for tex_file in tex_files:
            logger.info(f"Cleaning {tex_file.name}...")
            with open(tex_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            cleaned_content = converter.clean_over_escaped_latex(content)
            
            with open(tex_file, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)
            
            logger.info(f"✓ Cleaned {tex_file.name}")
        
        logger.info("✓ Cleaning completed")
        return
    
    if args.file:
        # Convert single file
        file_path = Path(args.file)
        if not file_path.exists():
            logger.error(f"File {args.file} does not exist")
            return 1
        
        logger.info(f"Converting single file: {file_path.name}")
        latex_content = converter.convert_word_document(file_path)
        
        output_name = file_path.stem + ".tex"
        output_path = converter.output_dir / output_name
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(latex_content)
        
        logger.info(f"✓ Converted to {output_path}")
        return
    
    # Convert all documents
    logger.info("CTMM Document Converter - Starting conversion...")
    converted_files = converter.convert_all_documents(args.source)
    
    if converted_files:
        integrated_file = converter.create_integrated_file(converted_files)
        
        print("\n" + "="*60)
        print("CTMM DOCUMENT CONVERSION SUMMARY")
        print("="*60)
        print(f"Source directory: {args.source}")
        print(f"Output directory: {args.output}")
        print(f"Files converted: {len(converted_files)}")
        print(f"Integrated file: {integrated_file}")
        print("\nConverted files:")
        for file_path in converted_files:
            print(f"  ✓ {Path(file_path).name}")
        
        print("\nNext steps:")
        print("- Review converted LaTeX files for accuracy")
        print("- Include relevant files in main.tex")
        print("- Test compilation with LaTeX build system")
    else:
        logger.error("No files were converted")
        return 1


if __name__ == "__main__":
    sys.exit(main() or 0)