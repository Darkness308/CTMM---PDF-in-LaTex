#!/usr/bin/env python3
"""
LaTeX De-escaping Tool for CTMM Project

This script fixes systematic over-escaping issues in converted LaTeX files.
It removes excessive \textbackslash{} escaping to produce clean, readable LaTeX.

Usage:
    python3 fix_latex_escaping.py [input_dir] [output_dir]
    python3 fix_latex_escaping.py --help

Examples:
    python3 fix_latex_escaping.py converted/ fixed/
    python3 fix_latex_escaping.py converted/  # fixes files in-place
"""

import re
import os
import sys
import argparse
import shutil
from pathlib import Path
from typing import Dict, List, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class LaTeXDeEscaper:
    """Fixes over-escaped LaTeX commands in converted documents."""
    
    def __init__(self):
        # Define the systematic over-escaping patterns and their fixes
        self.escaping_patterns = [
            # Main LaTeX command patterns
            (r'\\textbackslash\{\}([a-zA-Z]+)\\textbackslash\{\}', r'\\\1'),
            
            # Section and subsection patterns
            (r'\\textbackslash\{\}section\\textbackslash\{\}\\textbackslash\{\}\\textbackslash\{\}texorpdfstring\\textbackslash\{\}', r'\\section{\\texorpdfstring'),
            (r'\\textbackslash\{\}subsection\\textbackslash\{\}\\textbackslash\{\}\\textbackslash\{\}texorpdfstring\\textbackslash\{\}', r'\\subsection{\\texorpdfstring'),
            
            # Hypertarget patterns
            (r'\\textbackslash\{\}hypertarget\\textbackslash\{\}', r'\\hypertarget'),
            
            # Environment patterns
            (r'\\textbackslash\{\}begin\\textbackslash\{\}', r'\\begin'),
            (r'\\textbackslash\{\}end\\textbackslash\{\}', r'\\end'),
            
            # Label patterns
            (r'\\textbackslash\{\}label\\textbackslash\{\}', r'\\label'),
            
            # Text formatting patterns
            (r'\\textbackslash\{\}textbf\\textbackslash\{\}', r'\\textbf'),
            (r'\\textbackslash\{\}textit\\textbackslash\{\}', r'\\textit'),
            (r'\\textbackslash\{\}emph\\textbackslash\{\}', r'\\emph'),
            (r'\\textbackslash\{\}ul\\textbackslash\{\}', r'\\ul'),
            (r'\\textbackslash\{\}texttt\\textbackslash\{\}', r'\\texttt'),
            
            # Item and list patterns
            (r'\\textbackslash\{\}item', r'\\item'),
            (r'\\textbackslash\{\}tightlist', r'\\tightlist'),
            
            # Quote patterns  
            (r'\\textbackslash\{\}texorpdfstring\\textbackslash\{\}', r'\\texorpdfstring'),
            
            # Parameter braces - fix excessive bracing patterns
            (r'\\textbackslash\{\}\{([^}]*?)\\textbackslash\{\}\}', r'{\1}'),
            
            # Simple brace escaping
            (r'\\textbackslash\{\}\{', r'{'),
            (r'\\textbackslash\{\}\}', r'}'),
            
            # Double backslash patterns (line breaks)
            (r'\\textbackslash\{\}\\textbackslash\{\}', r'\\\\'),
            
            # Percentage signs
            (r'\\textbackslash\{\}%', r'%'),
            
            # Additional common commands
            (r'\\textbackslash\{\}def\\textbackslash\{\}', r'\\def'),
            (r'\\textbackslash\{\}deflabelenumi\\textbackslash\{\}', r'\\deflabelenumi'),
            (r'\\textbackslash\{\}arabic\\textbackslash\{\}', r'\\arabic'),
            
            # Math mode patterns
            (r'\\textbackslash\{\}\$', r'$'),
            
            # Ampersand patterns (table separators)
            (r'\\textbackslash\{\}\&', r'\\&'),
            
            # More environment patterns
            (r'\\textbackslash\{\}enumerate\\textbackslash\{\}', r'enumerate'),
            (r'\\textbackslash\{\}itemize\\textbackslash\{\}', r'itemize'),
            (r'\\textbackslash\{\}quote\\textbackslash\{\}', r'quote'),
            
            # Additional LaTeX commands often over-escaped by converters
            (r'\\textbackslash\{\}newpage\\textbackslash\{\}', r'\\newpage'),
            (r'\\textbackslash\{\}clearpage\\textbackslash\{\}', r'\\clearpage'),
            (r'\\textbackslash\{\}newline\\textbackslash\{\}', r'\\newline'),
            (r'\\textbackslash\{\}linebreak\\textbackslash\{\}', r'\\linebreak'),
            
            # Table-related commands
            (r'\\textbackslash\{\}hline\\textbackslash\{\}', r'\\hline'),
            (r'\\textbackslash\{\}cline\\textbackslash\{\}', r'\\cline'),
            (r'\\textbackslash\{\}multicolumn\\textbackslash\{\}', r'\\multicolumn'),
            
            # Figure and graphics commands
            (r'\\textbackslash\{\}includegraphics\\textbackslash\{\}', r'\\includegraphics'),
            (r'\\textbackslash\{\}caption\\textbackslash\{\}', r'\\caption'),
            (r'\\textbackslash\{\}centering\\textbackslash\{\}', r'\\centering'),
            
            # Bibliography and citation commands
            (r'\\textbackslash\{\}cite\\textbackslash\{\}', r'\\cite'),
            (r'\\textbackslash\{\}bibliography\\textbackslash\{\}', r'\\bibliography'),
            (r'\\textbackslash\{\}bibliographystyle\\textbackslash\{\}', r'\\bibliographystyle'),
            
            # Font and size commands
            (r'\\textbackslash\{\}tiny\\textbackslash\{\}', r'\\tiny'),
            (r'\\textbackslash\{\}small\\textbackslash\{\}', r'\\small'),
            (r'\\textbackslash\{\}large\\textbackslash\{\}', r'\\large'),
            (r'\\textbackslash\{\}Large\\textbackslash\{\}', r'\\Large'),
            (r'\\textbackslash\{\}huge\\textbackslash\{\}', r'\\huge'),
            (r'\\textbackslash\{\}Huge\\textbackslash\{\}', r'\\Huge'),
        ]
        
        # Additional cleanup patterns
        self.cleanup_patterns = [
            # Remove redundant braces around single arguments
            (r'\{\\textbackslash\{\}\}', r'{}'),
            
            # Fix texorpdfstring patterns with remaining issues
            (r'\\texorpdfstring\{([^}]*?)\}\{([^}]*?)\}\\label\{([^}]*?)\}', r'\\texorpdfstring{\1}{\2}}\\label{\3}'),
            (r'\\texorpdfstring\{([^}]*?)\}\{([^}]*?)\}\{([^}]*?)\}', r'\\texorpdfstring{\1}{\2}}{\3}'),
            
            # Clean up multiple consecutive braces
            (r'\{\{\{', r'{'),
            (r'\}\}\}', r'}'),
            (r'\{\{', r'{'),
            (r'\}\}', r'}'),
            
            # Fix section/subsection brace patterns - more comprehensive
            (r'\\section\{\\texorpdfstring\{([^}]*?)\}\{([^}]*?)\}\\label\{([^}]*?)\}', r'\\section{\\texorpdfstring{\1}{\2}}\\label{\3}'),
            (r'\\subsection\{\\texorpdfstring\{([^}]*?)\}\{([^}]*?)\}\\label\{([^}]*?)\}', r'\\subsection{\\texorpdfstring{\1}{\2}}\\label{\3}'),
            
            # Fix hypertarget patterns
            (r'\\hypertarget\{([^}]*?)\}\{%', r'\\hypertarget{\1}{%'),
            
            # Remove empty text formatting
            (r'\\textbf\{\}', r''),
            (r'\\emph\{\}', r''),
            (r'\\ul\{\}', r''),
            
            # Fix malformed closing braces after texorpdfstring
            (r'(\{[^}]*?\})(\{[^}]*?\})\\label\{([^}]*?)\}', r'\1\2}\\label{\3}'),
            
            # Fix missing closing braces for commands
            (r'\\emph\{\\textbf\{([^}]*?)\}([^}]*?)$', r'\\emph{\\textbf{\1}}\2'),
            
            # Fix broken section commands
            (r'\\section\{\\texorpdfstring\{([^}]*?)\}\{([^}]*?)\}$', r'\\section{\\texorpdfstring{\1}{\2}}'),
            (r'\\subsection\{\\texorpdfstring\{([^}]*?)\}\{([^}]*?)\}$', r'\\subsection{\\texorpdfstring{\1}{\2}}'),
            
            # Additional cleanup patterns for edge cases
            (r'\\textbackslash\{\}\s*\\textbackslash\{\}', r'\\\\'),  # Double backslashes with whitespace
            (r'\{\\textbackslash\{\}\\textbackslash\{\}\}', r'{}'),   # Braced double backslashes
            
            # Fix corrupted environment patterns
            (r'\\begin\{\\textbackslash\{\}([^}]*?)\\textbackslash\{\}\}', r'\\begin{\1}'),
            (r'\\end\{\\textbackslash\{\}([^}]*?)\\textbackslash\{\}\}', r'\\end{\1}'),
            
            # Clean up over-escaped command sequences
            (r'\\textbackslash\{\}\\textbackslash\{\}([a-zA-Z]+)', r'\\\1'),
            
            # Fix spacing issues around escapes
            (r'\s+\\textbackslash\{\}\s+', r' '),
            (r'\\textbackslash\{\}\s+', r''),
            (r'\s+\\textbackslash\{\}', r''),
        ]
        
        self.stats = {
            'files_processed': 0,
            'files_changed': 0,
            'total_replacements': 0
        }
    
    def process_file(self, input_path: Path, output_path: Path = None) -> Tuple[bool, int]:
        """
        Process a single LaTeX file to fix over-escaping.
        
        Args:
            input_path: Path to input .tex file
            output_path: Path for output (None for in-place)
            
        Returns:
            Tuple of (file_changed, num_replacements)
        """
        if output_path is None:
            output_path = input_path
            
        try:
            # Read the file with UTF-8 encoding
            with open(input_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            replacements_made = 0
            
            # Apply all escaping pattern fixes
            for pattern, replacement in self.escaping_patterns:
                content, count = re.subn(pattern, replacement, content)
                replacements_made += count
                if count > 0:
                    logger.debug(f"Pattern '{pattern}' replaced {count} times")
            
            # Apply cleanup patterns
            for pattern, replacement in self.cleanup_patterns:
                content, count = re.subn(pattern, replacement, content)
                replacements_made += count
                if count > 0:
                    logger.debug(f"Cleanup pattern '{pattern}' replaced {count} times")
            
            # Check if content changed
            content_changed = content != original_content
            
            if content_changed:
                # Write the fixed content
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                logger.info(f"Fixed {input_path} -> {output_path} ({replacements_made} replacements)")
            else:
                logger.info(f"No changes needed for {input_path}")
            
            return content_changed, replacements_made
            
        except Exception as e:
            logger.error(f"Error processing {input_path}: {e}")
            return False, 0
    
    def process_directory(self, input_dir: Path, output_dir: Path = None) -> Dict:
        """
        Process all .tex files in a directory.
        
        Args:
            input_dir: Directory containing .tex files
            output_dir: Output directory (None for in-place)
            
        Returns:
            Dictionary with processing statistics
        """
        if output_dir and output_dir != input_dir:
            output_dir.mkdir(parents=True, exist_ok=True)
        
        tex_files = list(input_dir.glob('*.tex'))
        logger.info(f"Found {len(tex_files)} .tex files in {input_dir}")
        
        for tex_file in tex_files:
            self.stats['files_processed'] += 1
            
            if output_dir and output_dir != input_dir:
                output_file = output_dir / tex_file.name
            else:
                output_file = None
            
            changed, replacements = self.process_file(tex_file, output_file)
            
            if changed:
                self.stats['files_changed'] += 1
            self.stats['total_replacements'] += replacements
        
        return self.stats
    
    def validate_latex_syntax(self, file_path: Path) -> List[str]:
        """
        Enhanced validation of LaTeX syntax in the fixed file.
        
        Args:
            file_path: Path to the LaTeX file
            
        Returns:
            List of potential issues found
        """
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for remaining over-escaped commands
            if r'\textbackslash{}' in content:
                issues.append("Still contains over-escaped commands")
            
            # Check for unmatched braces (but allow some tolerance for content)
            brace_count = content.count('{') - content.count('}')
            if abs(brace_count) > 5:  # Allow some tolerance for embedded content
                issues.append(f"Significant brace mismatch (difference: {brace_count})")
            
            # Check for malformed commands (but exclude valid LaTeX sequences)
            malformed_commands = re.findall(r'\\[a-zA-Z]+\\[a-zA-Z]', content)
            # Filter out valid patterns like \\& (escaped ampersand)
            valid_patterns = {r'\\&', r'\\\\', r'\\_', r'\\%', r'\\$', r'\\#'}
            filtered_malformed = [cmd for cmd in malformed_commands 
                                 if not any(pattern in cmd for pattern in valid_patterns)]
            if filtered_malformed:
                issues.append(f"Potential malformed commands: {set(filtered_malformed)}")
            
            # Check for common problematic patterns
            if re.search(r'\\textbackslash\{\}[a-zA-Z]+', content):
                issues.append("Contains partially escaped commands")
            
            # Check for incomplete command fixes
            if re.search(r'\\[a-zA-Z]+\\textbackslash\{\}', content):
                issues.append("Contains commands with trailing escapes")
                
        except Exception as e:
            issues.append(f"Error reading file: {e}")
        
        return issues


def main():
    parser = argparse.ArgumentParser(
        description="Fix over-escaped LaTeX commands in converted CTMM files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s converted/                    # Fix files in-place
  %(prog)s converted/ fixed/            # Create fixed copies
  %(prog)s --validate converted/        # Validate fixed files
  %(prog)s --verbose converted/         # Show detailed output
        """
    )
    
    parser.add_argument('input_dir', help='Directory containing .tex files to fix')
    parser.add_argument('output_dir', nargs='?', help='Output directory (optional, default: in-place)')
    parser.add_argument('--validate', action='store_true', help='Validate LaTeX syntax after fixing')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show verbose output')
    parser.add_argument('--backup', action='store_true', help='Create .bak backup files')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    input_dir = Path(args.input_dir)
    if not input_dir.exists() or not input_dir.is_dir():
        logger.error(f"Input directory {input_dir} does not exist or is not a directory")
        sys.exit(1)
    
    output_dir = Path(args.output_dir) if args.output_dir else input_dir
    
    # Create backup files if requested
    if args.backup and output_dir == input_dir:
        for tex_file in input_dir.glob('*.tex'):
            backup_file = tex_file.with_suffix('.tex.bak')
            shutil.copy2(tex_file, backup_file)
            logger.info(f"Created backup: {backup_file}")
    
    # Process files
    de_escaper = LaTeXDeEscaper()
    stats = de_escaper.process_directory(input_dir, output_dir)
    
    # Print summary
    print("\n" + "="*50)
    print("LATEX DE-ESCAPING SUMMARY")
    print("="*50)
    print(f"Files processed: {stats['files_processed']}")
    print(f"Files changed: {stats['files_changed']}")
    print(f"Total replacements: {stats['total_replacements']}")
    
    # Validate if requested
    if args.validate:
        print("\nVALIDATION RESULTS:")
        print("-" * 20)
        for tex_file in output_dir.glob('*.tex'):
            issues = de_escaper.validate_latex_syntax(tex_file)
            if issues:
                print(f"{tex_file.name}: {', '.join(issues)}")
            else:
                print(f"{tex_file.name}: OK")
    
    print(f"\nProcess completed. Files {'updated in-place' if output_dir == input_dir else f'saved to {output_dir}'}.")


if __name__ == '__main__':
    main()