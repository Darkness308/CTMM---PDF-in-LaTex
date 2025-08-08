#!/usr/bin/env python3
"""
CTMM Build Manager - Enhanced LaTeX Build System
Provides safe package name handling and dynamic command generation with sanitization.
"""

import re
import subprocess
import sys
from pathlib import Path
import logging
from typing import List, Dict, Set

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def sanitize_package_name(package_name: str) -> str:
    """
    Sanitize package name for safe use in LaTeX command names.
    
    LaTeX command names can only contain letters (a-z, A-Z).
    This function converts package names like 'ctmm-design' to 'ctmmDesign'.
    
    Args:
        package_name: Original package name (may contain hyphens, underscores, etc.)
        
    Returns:
        Sanitized package name safe for use in LaTeX commands
        
    Examples:
        'ctmm-design' -> 'ctmmDesign'
        'form-elements' -> 'formElements'
        'ctmm_diagrams' -> 'ctmmDiagrams'
    """
    # Remove file extensions
    clean_name = package_name
    if '.' in clean_name:
        clean_name = clean_name.split('.')[0]
    
    # Split on hyphens and underscores, then camelCase
    parts = re.split(r'[-_]+', clean_name)
    if not parts:
        return 'defaultPackage'
    
    # First part stays lowercase, rest are capitalized
    sanitized = parts[0].lower()
    for part in parts[1:]:
        if part:  # Skip empty parts
            sanitized += part.capitalize()
    
    # Ensure it starts with a letter and contains only letters
    sanitized = re.sub(r'[^a-zA-Z]', '', sanitized)
    
    # Ensure it's not empty and starts with a letter
    if not sanitized or not sanitized[0].isalpha():
        sanitized = 'pkg' + sanitized
    
    return sanitized


def generate_placeholder_command(package_name: str) -> str:
    """
    Generate a safe LaTeX placeholder command for a package.
    
    This addresses the security concern about invalid LaTeX command names
    when package_name contains special characters.
    
    Args:
        package_name: Original package name
        
    Returns:
        LaTeX command definition string with sanitized command name
    """
    safe_name = sanitize_package_name(package_name)
    
    # Generate the LaTeX command with sanitized name
    command = f"""\\newcommand{{\\{safe_name}Placeholder}}{{\\textcolor{{red}}{{[{package_name.upper()} TEMPLATE - NEEDS CONTENT]}}}}"""
    
    return command


def generate_package_template(package_path: str) -> str:
    """
    Generate a complete LaTeX package template with safe placeholder commands.
    
    Args:
        package_path: Path to the package file
        
    Returns:
        Complete LaTeX package template content
    """
    path = Path(package_path)
    package_name = path.stem
    safe_name = sanitize_package_name(package_name)
    
    template = f"""% {path.name} - CTMM Style Package
% TODO: Add content for this style package
% Created automatically by CTMM Build System

\\NeedsTeXFormat{{LaTeX2e}}[1995/12/01]
\\ProvidesPackage{{{package_name}}}[2024/01/01 CTMM {package_name} package - TODO: Add content]

% TODO: Add package dependencies here
% \\RequirePackage{{xcolor}}
% \\RequirePackage{{tikz}}

% TODO: Add color definitions here
% \\definecolor{{ctmmBlue}}{{RGB}}{{52, 152, 219}}

% Placeholder command (safe for LaTeX)
{generate_placeholder_command(package_name)}

% TODO: Add commands and environments here
% \\newcommand{{\\{safe_name}Command}}[1]{{\\textcolor{{ctmmBlue}}{{#1}}}}

% End of package - TODO: Complete implementation
"""
    
    return template


class CTMMBuildManager:
    """Enhanced build manager with safe package name handling."""
    
    def __init__(self, main_tex_path: str = "main.tex"):
        self.main_tex_path = Path(main_tex_path)
        self.style_files: Set[str] = set()
        self.module_files: Set[str] = set()
        self.missing_files: List[str] = []
        self.sanitized_names: Dict[str, str] = {}
    
    def scan_references(self) -> None:
        """Scan main.tex for style and module references."""
        if not self.main_tex_path.exists():
            logger.error("Main TeX file %s not found!", self.main_tex_path)
            sys.exit(1)
        
        try:
            with open(self.main_tex_path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
        except Exception as e:
            logger.error("Error reading %s: %s", self.main_tex_path, e)
            return
        
        # Find style and module references
        style_matches = re.findall(r'\\usepackage\{style/([^}]+)\}', content)
        self.style_files = {f"style/{match}.sty" for match in style_matches}
        
        module_matches = re.findall(r'\\input\{modules/([^}]+)\}', content)
        self.module_files = {f"modules/{match}.tex" for match in module_matches}
        
        # Generate sanitized names for all packages
        for style_file in self.style_files:
            package_name = Path(style_file).stem
            self.sanitized_names[package_name] = sanitize_package_name(package_name)
        
        logger.info("Found %d style files and %d module files", 
                   len(self.style_files), len(self.module_files))
        
        # Log sanitized names for verification
        if self.sanitized_names:
            logger.info("Package name sanitization:")
            for original, sanitized in self.sanitized_names.items():
                logger.info("  '%s' -> '%s'", original, sanitized)
    
    def check_missing_files(self) -> None:
        """Check which files are missing."""
        all_files = list(self.style_files) + list(self.module_files)
        self.missing_files = []
        
        for file_path in all_files:
            if not Path(file_path).exists():
                self.missing_files.append(file_path)
        
        if self.missing_files:
            logger.warning("Found %d missing files", len(self.missing_files))
        else:
            logger.info("All referenced files exist")
    
    def create_safe_templates(self) -> None:
        """Create templates with safe command generation."""
        if not self.missing_files:
            return
        
        logger.info("Creating safe templates for missing files...")
        
        for file_path in self.missing_files:
            path = Path(file_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            
            if file_path.endswith('.sty'):
                # Use safe template generation
                content = generate_package_template(file_path)
            else:
                # Module template
                content = f"""% {path.name} - CTMM Module
% TODO: Add content for this module
% Created automatically by CTMM Build System

\\section{{TODO: {path.stem.replace('-', ' ').title()}}}
\\label{{sec:{sanitize_package_name(path.stem)}}}

\\begin{{center}}
\\textit{{This module is under development. Content will be added soon.}}
\\end{{center}}

% TODO: Complete implementation
"""
            
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info("Created safe template: %s", file_path)
    
    def run_check(self) -> bool:
        """Run the enhanced build check with safe naming."""
        logger.info("CTMM Build Manager - Starting enhanced check...")
        
        try:
            self.scan_references()
            self.check_missing_files()
            self.create_safe_templates()
            
            # Generate summary
            print("\n" + "="*60)
            print("CTMM BUILD MANAGER SUMMARY")
            print("="*60)
            print(f"Style files: {len(self.style_files)}")
            print(f"Module files: {len(self.module_files)}")
            print(f"Missing files: {len(self.missing_files)} (safe templates created)")
            
            if self.sanitized_names:
                print("\nPackage Name Sanitization:")
                for original, sanitized in self.sanitized_names.items():
                    print(f"  {original} -> {sanitized}")
            
            if self.missing_files:
                print("\nNEXT STEPS:")
                print("- Review and complete the created template files")
                print("- All LaTeX commands use sanitized names (safe for LaTeX)")
            
            return True
            
        except Exception as e:
            logger.error("Build manager check failed: %s", e)
            return False


def main():
    """Run the CTMM build manager."""
    import argparse
    
    parser = argparse.ArgumentParser(description='CTMM Build Manager - Enhanced LaTeX Build System')
    parser.add_argument('--main-tex', default='main.tex', 
                       help='Path to main TeX file (default: main.tex)')
    parser.add_argument('--test-sanitization', action='store_true',
                       help='Test package name sanitization')
    
    args = parser.parse_args()
    
    if args.test_sanitization:
        # Test the sanitization function
        test_cases = [
            'ctmm-design',
            'form-elements', 
            'ctmm_diagrams',
            'test-package-name',
            'simple',
            'complex-name_with-mixed_separators',
            '123invalid',
            '-invalid-start',
            ''
        ]
        
        print("Testing package name sanitization:")
        print("="*50)
        for test_case in test_cases:
            sanitized = sanitize_package_name(test_case)
            safe = sanitized.isalpha() and sanitized[0].isalpha()
            status = "✓" if safe else "✗"
            print(f"{status} '{test_case}' -> '{sanitized}'")
        
        print("\nTesting placeholder command generation:")
        print("="*50)
        for test_case in ['ctmm-design', 'form-elements']:
            command = generate_placeholder_command(test_case)
            print(f"Package: {test_case}")
            print(f"Command: {command}")
            print()
        
        return 0
    
    build_manager = CTMMBuildManager(args.main_tex)
    success = build_manager.run_check()
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())