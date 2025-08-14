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
            # Section and subsection patterns (more specific first)
            (r'\\textbackslash\{\}section\\textbackslash\{\}\\textbackslash\{\}\\textbackslash\{\}texorpdfstring\\textbackslash\{\}', r'\\section{\\texorpdfstring'),
            (r'\\textbackslash\{\}subsection\\textbackslash\{\}\\textbackslash\{\}\\textbackslash\{\}texorpdfstring\\textbackslash\{\}', r'\\subsection{\\texorpdfstring'),
            (r'\\textbackslash\{\}subsubsection\\textbackslash\{\}\\textbackslash\{\}\\textbackslash\{\}texorpdfstring\\textbackslash\{\}', r'\\subsubsection{\\texorpdfstring'),
            (r'\\textbackslash\{\}paragraph\\textbackslash\{\}\\textbackslash\{\}\\textbackslash\{\}texorpdfstring\\textbackslash\{\}', r'\\paragraph{\\texorpdfstring'),
            (r'\\textbackslash\{\}section\\textbackslash\{\}', r'\\section'),
            (r'\\textbackslash\{\}subsection\\textbackslash\{\}', r'\\subsection'),
            (r'\\textbackslash\{\}subsubsection\\textbackslash\{\}', r'\\subsubsection'),
            (r'\\textbackslash\{\}paragraph\\textbackslash\{\}', r'\\paragraph'),
            
            # Hypertarget patterns
            (r'\\textbackslash\{\}hypertarget\\textbackslash\{\}', r'\\hypertarget'),
            
            # Environment patterns
            (r'\\textbackslash\{\}begin\\textbackslash\{\}', r'\\begin'),
            (r'\\textbackslash\{\}end\\textbackslash\{\}', r'\\end'),
            
            # Label and reference patterns
            (r'\\textbackslash\{\}label\\textbackslash\{\}', r'\\label'),
            (r'\\textbackslash\{\}ref\\textbackslash\{\}', r'\\ref'),
            (r'\\textbackslash\{\}pageref\\textbackslash\{\}', r'\\pageref'),
            (r'\\textbackslash\{\}autoref\\textbackslash\{\}', r'\\autoref'),
            (r'\\textbackslash\{\}nameref\\textbackslash\{\}', r'\\nameref'),
            
            # Text formatting patterns
            (r'\\textbackslash\{\}textbf\\textbackslash\{\}', r'\\textbf'),
            (r'\\textbackslash\{\}textit\\textbackslash\{\}', r'\\textit'),
            (r'\\textbackslash\{\}emph\\textbackslash\{\}', r'\\emph'),
            (r'\\textbackslash\{\}ul\\textbackslash\{\}', r'\\ul'),
            (r'\\textbackslash\{\}texttt\\textbackslash\{\}', r'\\texttt'),
            (r'\\textbackslash\{\}underline\\textbackslash\{\}', r'\\underline'),
            (r'\\textbackslash\{\}textsc\\textbackslash\{\}', r'\\textsc'),
            (r'\\textbackslash\{\}textsf\\textbackslash\{\}', r'\\textsf'),
            (r'\\textbackslash\{\}textrm\\textbackslash\{\}', r'\\textrm'),
            
            # Color and highlighting patterns
            (r'\\textbackslash\{\}textcolor\\textbackslash\{\}', r'\\textcolor'),
            (r'\\textbackslash\{\}colorbox\\textbackslash\{\}', r'\\colorbox'),
            (r'\\textbackslash\{\}fcolorbox\\textbackslash\{\}', r'\\fcolorbox'),
            (r'\\textbackslash\{\}highlight\\textbackslash\{\}', r'\\highlight'),
            
            # List and item patterns
            (r'\\textbackslash\{\}item', r'\\item'),
            (r'\\textbackslash\{\}tightlist', r'\\tightlist'),
            (r'\\textbackslash\{\}itemize\\textbackslash\{\}', r'\\itemize'),
            (r'\\textbackslash\{\}enumerate\\textbackslash\{\}', r'\\enumerate'),
            (r'\\textbackslash\{\}description\\textbackslash\{\}', r'\\description'),
            
            # Math mode patterns
            (r'\\textbackslash\{\}\$', r'$'),
            (r'\\textbackslash\{\}\\$', r'\\$'),
            (r'\\textbackslash\{\}\\textbackslash\{\}\[', r'\\['),
            (r'\\textbackslash\{\}\\textbackslash\{\}\]', r'\\]'),
            (r'\\textbackslash\{\}equation\\textbackslash\{\}', r'\\equation'),
            (r'\\textbackslash\{\}align\\textbackslash\{\}', r'\\align'),
            
            # Table and figure patterns
            (r'\\textbackslash\{\}table\\textbackslash\{\}', r'\\table'),
            (r'\\textbackslash\{\}figure\\textbackslash\{\}', r'\\figure'),
            (r'\\textbackslash\{\}caption\\textbackslash\{\}', r'\\caption'),
            (r'\\textbackslash\{\}includegraphics\\textbackslash\{\}', r'\\includegraphics'),
            (r'\\textbackslash\{\}tabular\\textbackslash\{\}', r'\\tabular'),
            (r'\\textbackslash\{\}longtable\\textbackslash\{\}', r'\\longtable'),
            
            # Quote and citation patterns  
            (r'\\textbackslash\{\}texorpdfstring\\textbackslash\{\}', r'\\texorpdfstring'),
            (r'\\textbackslash\{\}cite\\textbackslash\{\}', r'\\cite'),
            (r'\\textbackslash\{\}citep\\textbackslash\{\}', r'\\citep'),
            (r'\\textbackslash\{\}citet\\textbackslash\{\}', r'\\citet'),
            (r'\\textbackslash\{\}quote\\textbackslash\{\}', r'\\quote'),
            (r'\\textbackslash\{\}quotation\\textbackslash\{\}', r'\\quotation'),
            
            # Special character patterns
            (r'\\textbackslash\{\}\\&', r'\\&'),
            (r'\\textbackslash\{\}\\#', r'\\#'),
            (r'\\textbackslash\{\}\\_', r'\\_'),
            (r'\\textbackslash\{\}\\%', r'\\%'),
            (r'\\textbackslash\{\}\\\^', r'\\^'),
            (r'\\textbackslash\{\}\\~', r'\\~'),
            
            # Parameter braces - fix excessive bracing patterns
            (r'\\textbackslash\{\}\{([^}]*?)\\textbackslash\{\}\}', r'{\1}'),
            
            # Simple brace escaping
            (r'\\textbackslash\{\}\{', r'{'),
            (r'\\textbackslash\{\}\}', r'}'),
            
            # Double backslash patterns (line breaks)
            (r'\\textbackslash\{\}\\textbackslash\{\}', r'\\\\'),
            
            # Percentage signs
            (r'\\textbackslash\{\}%', r'%'),
            
            # Additional CTMM-specific patterns
            (r'\\textbackslash\{\}faCompass\\textbackslash\{\}', r'\\faCompass'),
            (r'\\textbackslash\{\}checkbox\\textbackslash\{\}', r'\\checkbox'),
            (r'\\textbackslash\{\}checkedbox\\textbackslash\{\}', r'\\checkedbox'),
            (r'\\textbackslash\{\}ctmmBlueBox\\textbackslash\{\}', r'\\ctmmBlueBox'),
            
            # Additional cleanup patterns for remaining cases
            (r'\\textbackslash\{\}', r''),
            
            # General LaTeX command patterns (must be last to catch remaining)
            (r'\\textbackslash\{\}([a-zA-Z]+)\\textbackslash\{\}', r'\\\1'),
        ]
        
        # Additional cleanup patterns
        self.cleanup_patterns = [
            # Remove redundant braces around single arguments
            (r'\{\\textbackslash\{\}\}', r'{}'),
            
            # Fix escaping around braces
            (r'\\textbackslash\{\}\\{', r'{'),
            (r'\\}\\textbackslash\{\}', r'}'),
            
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
        ]
        
        self.stats = {
            'files_processed': 0,
            'files_changed': 0,
            'total_replacements': 0,
            'validation_errors': 0,
            'validation_warnings': 0
        }
        
        # Improved validation patterns to reduce false positives
        self.validation_patterns = [
            # Check for unbalanced braces
            (r'(?<!\\)\{(?:[^{}]|\\[{}])*(?<!\\)\}', 'balanced_braces'),
            # Check for valid LaTeX commands
            (r'\\[a-zA-Z]+(?:\[[^\]]*\])?(?:\{[^}]*\})*', 'valid_commands'),
            # Check for valid environment structure
            (r'\\begin\{([^}]+)\}.*?\\end\{\1\}', 'environment_structure'),
            # Check for proper section hierarchy
            (r'\\(?:sub)?(?:sub)?section\{.*?\}', 'section_structure'),
        ]
    
    def validate_latex_content(self, content: str, filename: str = "file") -> Tuple[bool, List[str]]:
        """
        Validate LaTeX content for common issues that could indicate problems.
        
        Args:
            content: LaTeX content to validate
            filename: Name of file being validated (for error reporting)
            
        Returns:
            Tuple of (is_valid, list_of_issues)
        """
        issues = []
        
        # Check for unbalanced braces
        brace_count = 0
        escaped = False
        for i, char in enumerate(content):
            if escaped:
                escaped = False
                continue
            if char == '\\':
                escaped = True
                continue
            elif char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count < 0:
                    issues.append(f"Unmatched closing brace at position {i}")
                    break
        
        if brace_count > 0:
            issues.append(f"Unmatched opening braces: {brace_count} remaining")
        
        # Check for potentially problematic patterns that might indicate incomplete fixes
        problematic_patterns = [
            (r'\\textbackslash\{\}', "Still contains \\textbackslash{} patterns"),
            (r'\{\{\{', "Contains triple opening braces"),
            (r'\}\}\}', "Contains triple closing braces"),
            (r'\\\\\\\\', "Contains quadruple backslashes"),
            (r'\\begin\{[^}]*\}(?!.*\\end\{[^}]*\})', "Unmatched \\begin without \\end"),
        ]
        
        for pattern, description in problematic_patterns:
            matches = re.findall(pattern, content, re.DOTALL)
            if matches:
                issues.append(f"{description} ({len(matches)} occurrences)")
        
        # Update stats
        if issues:
            self.stats['validation_errors'] += len([i for i in issues if 'Unmatched' in i])
            self.stats['validation_warnings'] += len([i for i in issues if 'Unmatched' not in i])
        
        return len(issues) == 0, issues
    
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
                # Validate the fixed content
                is_valid, validation_issues = self.validate_latex_content(content, str(input_path))
                
                if validation_issues:
                    logger.warning(f"Validation issues in {input_path}:")
                    for issue in validation_issues:
                        logger.warning(f"  - {issue}")
                
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
        Basic validation of LaTeX syntax in the fixed file.
        
        Args:
            file_path: Path to the LaTeX file
            
        Returns:
            List of potential issues found
        """
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for common LaTeX syntax issues
            if '\\textbackslash{}' in content:
                issues.append("Still contains over-escaped commands")
            
            # Check for unmatched braces
            brace_count = content.count('{') - content.count('}')
            if brace_count != 0:
                issues.append(f"Unmatched braces (difference: {brace_count})")
            
            # Check for malformed commands
            malformed_commands = re.findall(r'\\[a-zA-Z]*\\', content)
            if malformed_commands:
                issues.append(f"Potential malformed commands: {set(malformed_commands)}")
            
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
    
    if 'validation_errors' in stats:
        print(f"Validation errors: {stats['validation_errors']}")
        print(f"Validation warnings: {stats['validation_warnings']}")
    
    # Validate if requested
    if args.validate:
        print("\nVALIDATION RESULTS:")
        print("-" * 20)
        validation_passed = 0
        validation_failed = 0
        
        for tex_file in output_dir.glob('*.tex'):
            issues = de_escaper.validate_latex_syntax(tex_file)
            if issues:
                print(f"❌ {tex_file.name}: {', '.join(issues)}")
                validation_failed += 1
            else:
                print(f"✅ {tex_file.name}: OK")
                validation_passed += 1
        
        print(f"\nValidation Summary: {validation_passed} passed, {validation_failed} failed")
    
    print(f"\nProcess completed. Files {'updated in-place' if output_dir == input_dir else f'saved to {output_dir}'}.")


if __name__ == '__main__':
    main()