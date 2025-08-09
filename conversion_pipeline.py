#!/usr/bin/env python3
"""
CTMM Document Conversion Pipeline
Converts therapy documents from Word/Markdown to LaTeX format.

This script provides automated conversion capabilities for therapy materials,
ensuring consistent formatting and structure across all CTMM documents.
"""

import os
import re
import sys
import argparse
import logging
from pathlib import Path
from typing import List, Dict, Optional
import subprocess

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('conversion_pipeline.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class CTMMDocumentConverter:
    """Convert various document formats to CTMM-compatible LaTeX."""
    
    def __init__(self, output_dir: str = "converted"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.converted_count = 0
        
    def convert_markdown_to_latex(self, md_file: Path) -> Optional[Path]:
        """Convert Markdown file to LaTeX with CTMM formatting."""
        logger.info(f"Converting Markdown: {md_file}")
        
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            logger.error(f"Error reading {md_file}: {e}")
            return None
        
        # Convert basic Markdown to LaTeX
        latex_content = self._markdown_to_latex_conversion(content, md_file.stem)
        
        # Save converted file
        output_file = self.output_dir / f"{md_file.stem}.tex"
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(latex_content)
            logger.info(f"Converted to: {output_file}")
            self.converted_count += 1
            return output_file
        except Exception as e:
            logger.error(f"Error saving {output_file}: {e}")
            return None
    
    def convert_docx_to_latex(self, docx_file: Path) -> Optional[Path]:
        """Convert Word document to LaTeX using pandoc if available."""
        logger.info(f"Converting Word document: {docx_file}")
        
        # Check if pandoc is available
        try:
            subprocess.run(['pandoc', '--version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.warning("Pandoc not available, skipping Word conversion")
            return None
        
        output_file = self.output_dir / f"{docx_file.stem}.tex"
        
        try:
            # Use pandoc to convert
            result = subprocess.run([
                'pandoc',
                str(docx_file),
                '-o', str(output_file),
                '--to=latex',
                '--standalone'
            ], capture_output=True, text=True, check=True)
            
            # Post-process the converted file
            self._post_process_latex_file(output_file)
            
            logger.info(f"Converted to: {output_file}")
            self.converted_count += 1
            return output_file
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Pandoc conversion failed: {e}")
            return None
    
    def _markdown_to_latex_conversion(self, content: str, title: str) -> str:
        """Convert Markdown content to CTMM-styled LaTeX."""
        
        # Basic template
        latex_template = f"""% {title}.tex - CTMM Therapy Module
% Converted from Markdown by CTMM Conversion Pipeline

\\section{{{title.replace('_', ' ').replace('-', ' ').title()}}}
\\label{{sec:{title.replace(' ', '-').lower()}}}

"""
        
        # Convert headers
        content = re.sub(r'^# (.+)$', r'\\section{\1}', content, flags=re.MULTILINE)
        content = re.sub(r'^## (.+)$', r'\\subsection{\1}', content, flags=re.MULTILINE)
        content = re.sub(r'^### (.+)$', r'\\subsubsection{\1}', content, flags=re.MULTILINE)
        
        # Convert bold and italic
        content = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', content)
        content = re.sub(r'\*(.+?)\*', r'\\textit{\1}', content)
        
        # Convert lists
        content = re.sub(r'^- (.+)$', r'\\item \1', content, flags=re.MULTILINE)
        content = re.sub(r'^(\d+)\. (.+)$', r'\\item \2', content, flags=re.MULTILINE)
        
        # Wrap list items in itemize/enumerate environments
        content = self._wrap_lists(content)
        
        # Add CTMM-specific elements
        content = self._add_ctmm_elements(content)
        
        return latex_template + content + "\n\n% End of converted module\n"
    
    def _wrap_lists(self, content: str) -> str:
        """Wrap consecutive list items in LaTeX list environments."""
        lines = content.split('\n')
        result = []
        in_list = False
        
        for line in lines:
            if line.strip().startswith('\\item'):
                if not in_list:
                    result.append('\\begin{itemize}')
                    in_list = True
                result.append(line)
            else:
                if in_list:
                    result.append('\\end{itemize}')
                    in_list = False
                result.append(line)
        
        if in_list:
            result.append('\\end{itemize}')
        
        return '\n'.join(result)
    
    def _add_ctmm_elements(self, content: str) -> str:
        """Add CTMM-specific LaTeX elements and styling."""
        
        # Add checkboxes for interactive elements
        content = re.sub(r'\[ \]', r'\\checkbox', content)
        content = re.sub(r'\[x\]', r'\\checkedbox', content)
        
        # Convert trigger-related content to colored boxes
        if 'trigger' in content.lower():
            content = content.replace('Trigger', '\\textcolor{ctmmBlue}{Trigger}')
        
        # Add CTMM color highlights for key terms
        key_terms = ['CTMM', 'Catch', 'Track', 'Map', 'Match']
        for term in key_terms:
            content = content.replace(term, f'\\textcolor{{ctmmBlue}}{{{term}}}')
        
        return content
    
    def _post_process_latex_file(self, latex_file: Path) -> None:
        """Post-process converted LaTeX file for CTMM compatibility."""
        try:
            with open(latex_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Remove standalone document class and preamble if present
            content = re.sub(r'\\documentclass.*?\\begin{document}', '', content, flags=re.DOTALL)
            content = re.sub(r'\\end{document}', '', content)
            
            # Clean up and add CTMM formatting
            content = self._add_ctmm_elements(content)
            
            with open(latex_file, 'w', encoding='utf-8') as f:
                f.write(content)
                
        except Exception as e:
            logger.error(f"Error post-processing {latex_file}: {e}")
    
    def create_therapy_tool_template(self, tool_name: str, tool_number: int = None) -> Path:
        """Create a template for a new therapy tool."""
        if tool_number:
            filename = f"Tool {tool_number} {tool_name}.tex"
        else:
            filename = f"{tool_name.replace(' ', '_')}.tex"
        
        output_file = self.output_dir / filename
        
        template_content = f"""% {filename} - CTMM Therapy Tool
% Created by CTMM Conversion Pipeline

\\section{{Tool: {tool_name}}}
\\label{{sec:tool-{tool_name.lower().replace(' ', '-')}}}

\\begin{{ctmmBlueBox}}{{{tool_name}}}
This therapy tool provides structured guidance for {tool_name.lower()} activities within the CTMM system.
\\end{{ctmmBlueBox}}

\\subsection{{Overview}}
% TODO: Add tool overview and purpose

\\subsection{{Instructions}}
% TODO: Add step-by-step instructions

\\begin{{enumerate}}
\\item Step 1: \\checkbox~
\\item Step 2: \\checkbox~
\\item Step 3: \\checkbox~
\\end{{enumerate}}

\\subsection{{Reflection Questions}}
% TODO: Add reflection questions

\\begin{{itemize}}
\\item Question 1: \\textit{{Add your response here}}
\\item Question 2: \\textit{{Add your response here}}
\\end{{itemize}}

\\subsection{{Notes}}
% Space for additional notes and observations

\\vspace{{2cm}}

% End of therapy tool
"""
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(template_content)
            logger.info(f"Created therapy tool template: {output_file}")
            self.converted_count += 1
            return output_file
        except Exception as e:
            logger.error(f"Error creating template {output_file}: {e}")
            return None
    
    def batch_convert_directory(self, source_dir: Path) -> int:
        """Convert all supported files in a directory."""
        logger.info(f"Batch converting files from: {source_dir}")
        
        if not source_dir.exists():
            logger.error(f"Source directory does not exist: {source_dir}")
            return 0
        
        converted = 0
        
        # Convert Markdown files
        for md_file in source_dir.glob("*.md"):
            if self.convert_markdown_to_latex(md_file):
                converted += 1
        
        # Convert Word documents
        for docx_file in source_dir.glob("*.docx"):
            if self.convert_docx_to_latex(docx_file):
                converted += 1
        
        logger.info(f"Converted {converted} files from {source_dir}")
        return converted
    
    def generate_conversion_report(self) -> str:
        """Generate a report of the conversion process."""
        report = f"""
CTMM Document Conversion Report
==============================

## Summary
- Total files converted: {self.converted_count}
- Output directory: {self.output_dir}

## Converted Files
"""
        
        if self.output_dir.exists():
            for tex_file in sorted(self.output_dir.glob("*.tex")):
                file_size = tex_file.stat().st_size
                report += f"- {tex_file.name} ({file_size:,} bytes)\n"
        
        report += """
## Next Steps
1. Review converted files for accuracy
2. Test compilation with CTMM build system
3. Integrate approved files into main document
4. Update documentation as needed

## Notes
- Converted files may require manual review and adjustment
- CTMM-specific formatting has been applied where possible
- Interactive elements have been converted to LaTeX form elements
"""
        
        return report

def main():
    """Main conversion pipeline entry point."""
    parser = argparse.ArgumentParser(description='CTMM Document Conversion Pipeline')
    parser.add_argument('--source', type=str, help='Source directory or file to convert')
    parser.add_argument('--output', type=str, default='converted', help='Output directory')
    parser.add_argument('--tool', type=str, help='Create therapy tool template with given name')
    parser.add_argument('--tool-number', type=int, help='Tool number for therapy tool template')
    parser.add_argument('--batch', action='store_true', help='Batch convert all files in source directory')
    
    args = parser.parse_args()
    
    converter = CTMMDocumentConverter(args.output)
    
    if args.tool:
        # Create therapy tool template
        converter.create_therapy_tool_template(args.tool, args.tool_number)
    elif args.source:
        source_path = Path(args.source)
        
        if args.batch:
            # Batch convert directory
            converter.batch_convert_directory(source_path)
        elif source_path.suffix.lower() == '.md':
            # Convert single Markdown file
            converter.convert_markdown_to_latex(source_path)
        elif source_path.suffix.lower() == '.docx':
            # Convert single Word document
            converter.convert_docx_to_latex(source_path)
        else:
            logger.error(f"Unsupported file format: {source_path.suffix}")
            return 1
    else:
        logger.error("No source specified. Use --source or --tool option.")
        return 1
    
    # Generate and save report
    report = converter.generate_conversion_report()
    report_file = Path(args.output) / "conversion_report.md"
    
    try:
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        logger.info(f"Conversion report saved to: {report_file}")
    except Exception as e:
        logger.error(f"Error saving report: {e}")
    
    print(report)
    return 0

if __name__ == "__main__":
    sys.exit(main())