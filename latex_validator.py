#!/usr/bin/env python3
"""
LaTeX Validator for CTMM System
Detects and fixes excessive escaping issues in LaTeX documents.
"""

import re
import sys
from pathlib import Path
from typing import List, Dict, Tuple
import argparse
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


class LaTeXValidator:
    """Validates and cleans LaTeX files from excessive escaping."""
    
    def __init__(self):
        # Patterns for detecting over-escaped content
        self.problematic_patterns = {
            'textbackslash_escape': r'\\textbackslash\{\}',
            'hypertarget_overuse': r'\\hypertarget\{[^}]+\}\{%\s*\\section',
            'texorpdfstring_overuse': r'\\texorpdfstring\{[^}]*\\textbf\{[^}]*\}\}',
            'excessive_backslashes': r'\\\\&',  # Double backslashes before &
            'auto_generated_labels': r'\\label\{[a-z]+-\d+.*\}',  # Auto-generated labels
        }
        
        # Patterns for proper LaTeX structure
        self.preferred_patterns = {
            'simple_section': r'\\section\{([^}]+)\}',
            'simple_subsection': r'\\subsection\{([^}]+)\}',
            'clean_labels': r'\\label\{sec:[a-zA-Z][a-zA-Z0-9_-]*\}',
        }
    
    def detect_issues(self, content: str) -> Dict[str, List[str]]:
        """Detect escaping and formatting issues in LaTeX content."""
        issues = {}
        
        for issue_name, pattern in self.problematic_patterns.items():
            matches = re.findall(pattern, content)
            if matches:
                issues[issue_name] = matches
        
        return issues
    
    def clean_excessive_escaping(self, content: str) -> str:
        """Clean excessive escaping from LaTeX content."""
        cleaned = content
        
        # Fix textbackslash escaping
        cleaned = re.sub(r'\\textbackslash\{\}', r'\\', cleaned)
        
        # Simplify over-complex section headers
        # Convert: \hypertarget{...}{\section{\texorpdfstring{...}{...}\label{...}}
        # To: \section{Simple Title}\label{sec:clean-name}
        def simplify_section(match):
            # Extract simple title from complex structure
            full_match = match.group(0)
            
            # Try to extract meaningful title
            title_match = re.search(r'\\textbf\{([^}]+)\}', full_match)
            if title_match:
                title = title_match.group(1)
                # Clean title of excessive formatting
                title = re.sub(r'\\[a-zA-Z]+\{([^}]*)\}', r'\1', title)
                title = title.replace('\\\\', ' ').replace('&', '').strip()
                
                # Generate clean label
                label = re.sub(r'[^a-zA-Z0-9-]', '-', title.lower())
                label = re.sub(r'-+', '-', label).strip('-')
                
                return f'\\section{{{title}}}\\label{{sec:{label}}}'
            
            return full_match
        
        # Apply section simplification
        cleaned = re.sub(
            r'\\hypertarget\{[^}]+\}\{%\s*\\section\{\\texorpdfstring\{[^}]*\\textbf\{[^}]*\}\}[^}]*\}\\label\{[^}]+\}\}',
            simplify_section,
            cleaned
        )
        
        # Simplify subsections similarly
        def simplify_subsection(match):
            full_match = match.group(0)
            title_match = re.search(r'\\textbf\{([^}]+)\}', full_match)
            if title_match:
                title = title_match.group(1)
                title = re.sub(r'\\[a-zA-Z]+\{([^}]*)\}', r'\1', title)
                title = title.replace('\\\\', ' ').replace('&', '').strip()
                return f'\\subsection{{{title}}}'
            return full_match
        
        # Handle subsections with texorpdfstring
        cleaned = re.sub(
            r'\\hypertarget\{[^}]+\}\{%\s*\\subsection\{\\texorpdfstring\{[^}]*\\textbf\{[^}]*\}\}[^}]*\}\\label\{[^}]+\}\}',
            simplify_subsection,
            cleaned
        )
        
        # Remove standalone hypertargets and texorpdfstring wrappers
        cleaned = re.sub(
            r'\\hypertarget\{[^}]+\}\{%\s*\\subsection\{\\texorpdfstring\{([^}]+)\}\{[^}]+\}\\label\{[^}]+\}\}',
            r'\\subsection{\1}',
            cleaned
        )
        
        # Fix double backslash before ampersand
        cleaned = re.sub(r'\\\\&', r' \\& ', cleaned)
        
        # Remove empty hypertargets and sections
        cleaned = re.sub(r'\\hypertarget\{section[^}]*\}\{%\s*\\subsection\{\}\\label\{section[^}]*\}\}', '', cleaned)
        
        # Clean up excessive whitespace
        cleaned = re.sub(r'\n\s*\n\s*\n', '\n\n', cleaned)
        
        return cleaned
    
    def validate_file(self, file_path: Path) -> Tuple[bool, Dict[str, List[str]], str]:
        """Validate a single LaTeX file."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
        except Exception as e:
            logger.error(f"Error reading {file_path}: {e}")
            return False, {}, ""
        
        issues = self.detect_issues(content)
        cleaned_content = self.clean_excessive_escaping(content)
        
        is_valid = len(issues) == 0
        return is_valid, issues, cleaned_content
    
    def validate_directory(self, directory: Path, fix: bool = False) -> Dict[str, Dict]:
        """Validate all LaTeX files in a directory."""
        results = {}
        
        for tex_file in directory.glob('**/*.tex'):
            logger.info(f"Validating {tex_file}")
            is_valid, issues, cleaned_content = self.validate_file(tex_file)
            
            results[str(tex_file)] = {
                'valid': is_valid,
                'issues': issues,
                'original_size': len(open(tex_file, 'r', encoding='utf-8', errors='replace').read()),
                'cleaned_size': len(cleaned_content)
            }
            
            if not is_valid:
                logger.warning(f"Issues found in {tex_file}: {list(issues.keys())}")
                
                if fix:
                    # Backup original file
                    backup_path = tex_file.with_suffix('.tex.backup')
                    tex_file.rename(backup_path)
                    logger.info(f"Backed up original to {backup_path}")
                    
                    # Write cleaned content
                    with open(tex_file, 'w', encoding='utf-8') as f:
                        f.write(cleaned_content)
                    logger.info(f"Fixed escaping issues in {tex_file}")
            else:
                logger.info(f"✓ {tex_file} is properly formatted")
        
        return results
    
    def create_sample_problematic_file(self, output_path: Path) -> None:
        """Create a sample file with escaping issues for testing."""
        problematic_content = """
\\hypertarget{tool-23-trigger-management}{%
\\section{\\texorpdfstring{📄 \\textbf{TOOL 23: TRIGGER-MANAGEMENT}}{📄 TOOL 23: TRIGGER-MANAGEMENT}\\label{tool-23-trigger-management}}

🧩 \\emph{\\textbf{Modul zur Selbsthilfe \\textbackslash{}\\textbackslash{}& Co-Regulation -- Klartextversion für beide Partner}}

\\hypertarget{ziel-nutzen}{%
\\subsection{\\texorpdfstring{🎯 \\textbf{\\ul{ZIEL \\textbackslash{}\\textbackslash{}& NUTZEN}}}{🎯 ZIEL \\textbackslash{}\\textbackslash{}& NUTZEN}\\label{ziel-nutzen}}

\\textbf{Trigger besser verstehen}, körperliche/emotionale/mentale Reaktionen erkennen, passende Skills zuordnen.

\\hypertarget{section}{%
\\subsection{}\\label{section}}

\\hypertarget{section-1}{%
\\subsection{}\\label{section-1}}

\\begin{itemize}
\\item 🟢 \\textbf{Grün} = Alltag \\textbackslash{}\\textbackslash{}& Prävention
\\item 🟠 \\textbf{Orange} = Akutphase \\textbackslash{}\\textbackslash{}& Regulation  
\\end{itemize}
"""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(problematic_content)
        
        logger.info(f"Created sample problematic file: {output_path}")


def main():
    parser = argparse.ArgumentParser(description='LaTeX Validator for CTMM System')
    parser.add_argument('path', nargs='?', default='.', 
                       help='Path to file or directory to validate')
    parser.add_argument('--fix', action='store_true',
                       help='Fix issues found (creates backups)')
    parser.add_argument('--create-sample', metavar='FILE',
                       help='Create a sample file with escaping issues')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose logging')
    
    args = parser.parse_args()
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    validator = LaTeXValidator()
    
    if args.create_sample:
        sample_path = Path(args.create_sample)
        validator.create_sample_problematic_file(sample_path)
        return 0
    
    path = Path(args.path)
    
    if path.is_file():
        is_valid, issues, cleaned_content = validator.validate_file(path)
        
        if is_valid:
            print(f"✓ {path} is properly formatted")
            return 0
        else:
            print(f"✗ Issues found in {path}:")
            for issue_type, matches in issues.items():
                print(f"  - {issue_type}: {len(matches)} occurrence(s)")
            
            if args.fix:
                backup_path = path.with_suffix('.tex.backup')
                path.rename(backup_path)
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(cleaned_content)
                print(f"Fixed issues and created backup: {backup_path}")
            
            return 1
    
    elif path.is_dir():
        results = validator.validate_directory(path, fix=args.fix)
        
        valid_files = sum(1 for r in results.values() if r['valid'])
        total_files = len(results)
        
        print(f"\nValidation Summary:")
        print(f"  Valid files: {valid_files}/{total_files}")
        
        if valid_files < total_files:
            print(f"  Files with issues:")
            for file_path, result in results.items():
                if not result['valid']:
                    print(f"    - {file_path}: {list(result['issues'].keys())}")
        
        return 0 if valid_files == total_files else 1
    
    else:
        print(f"Error: {path} is not a valid file or directory")
        return 1


if __name__ == "__main__":
    sys.exit(main())