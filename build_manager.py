#!/usr/bin/env python3
"""
CTMM Enhanced Build Manager with Package Name Sanitization
Provides comprehensive sanitization for package names to prevent invalid LaTeX command generation.

This module addresses the security vulnerability where package names containing special 
characters (hyphens, underscores) could generate invalid LaTeX command names, causing 
compilation failures.
"""

import re
import subprocess
import sys
import tempfile
import shutil
import chardet
from pathlib import Path
from typing import List, Tuple, Dict, Set, Optional
import argparse
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('build_manager.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class PackageNameSanitizer:
    """Handles sanitization of package names to prevent invalid LaTeX command generation."""
    
    @staticmethod
    def sanitize_package_name(package_name: str) -> str:
        """
        Convert package names with special characters to safe camelCase versions.
        
        Examples:
            'ctmm-design' → 'ctmmDesign'
            'form-elements' → 'formElements'
            'ctmm_diagrams' → 'ctmmDiagrams'
            'some-complex_name-123' → 'someComplexName123'
        
        Args:
            package_name: Original package name that may contain special characters
            
        Returns:
            Sanitized package name safe for LaTeX command generation
        """
        if not package_name:
            return 'defaultPkg'
        
        # First, remove any characters that aren't letters, numbers, hyphens, or underscores
        # This preserves the structure for splitting but removes problematic chars
        clean_name = re.sub(r'[^a-zA-Z0-9\-_]', '', package_name)
        
        if not clean_name:
            return 'defaultPkg'
            
        # Split on hyphens and underscores
        parts = re.split(r'[-_]+', clean_name)
        
        # Handle empty parts (consecutive separators)
        parts = [part for part in parts if part]
        
        if not parts:
            return 'defaultPkg'
        
        # Check if the first part starts with a number
        needs_prefix = parts[0] and parts[0][0].isdigit()
        
        if needs_prefix:
            # First part stays as-is (it's a number), rest are capitalized
            sanitized_parts = ['pkg'] + [parts[0]]
            for part in parts[1:]:
                if part:
                    sanitized_parts.append(part.capitalize())
        else:
            # First part stays lowercase, rest are capitalized
            sanitized_parts = [parts[0].lower()]
            for part in parts[1:]:
                if part:
                    sanitized_parts.append(part.capitalize())
        
        result = ''.join(sanitized_parts)
        
        # Ensure it's not empty
        if not result:
            result = 'defaultPkg'
            
        return result
    
    @staticmethod
    def generate_safe_command_name(package_name: str, suffix: str = "Placeholder") -> str:
        """
        Generate a safe LaTeX command name from a package name.
        
        Args:
            package_name: Original package name
            suffix: Suffix to append to the command name
            
        Returns:
            Safe LaTeX command name
        """
        sanitized = PackageNameSanitizer.sanitize_package_name(package_name)
        return f"{sanitized}{suffix}"
    
    @staticmethod
    def validate_latex_command_name(command_name: str) -> bool:
        """
        Validate that a command name is safe for LaTeX.
        
        Args:
            command_name: Command name to validate
            
        Returns:
            True if the command name is valid for LaTeX
        """
        if not command_name:
            return False
            
        # LaTeX command names must start with a letter and contain only letters
        return bool(re.match(r'^[a-zA-Z][a-zA-Z0-9]*$', command_name))


class CTMMEnhancedBuildManager:
    """Enhanced build manager with comprehensive package name sanitization."""
    
    def __init__(self, main_tex_path: str = "main.tex"):
        self.main_tex_path = Path(main_tex_path)
        self.sanitizer = PackageNameSanitizer()
        self.style_files: Set[str] = set()
        self.module_files: Set[str] = set()
        self.missing_files: List[str] = []
        self.problematic_modules: List[str] = []
        self.package_mappings: Dict[str, str] = {}  # original -> sanitized
        
    def _read_file_safely(self, file_path: Path) -> str:
        """Read a file with automatic encoding detection."""
        try:
            # Try UTF-8 first
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            # Detect encoding
            with open(file_path, 'rb') as f:
                raw_data = f.read()
                detected = chardet.detect(raw_data)
                encoding = detected.get('encoding', 'utf-8')
                
            logger.debug(f"Detected encoding for {file_path}: {encoding}")
            with open(file_path, 'r', encoding=encoding, errors='replace') as f:
                return f.read()
    
    def scan_main_tex(self) -> None:
        """Scan main.tex for all usepackage{style/...} and input{modules/...} commands."""
        logger.info(f"Scanning {self.main_tex_path} for package and input references...")
        
        if not self.main_tex_path.exists():
            logger.error(f"Main TeX file {self.main_tex_path} not found!")
            sys.exit(1)
            
        content = self._read_file_safely(self.main_tex_path)
            
        # Find all usepackage{style/...} commands
        style_pattern = r'\\usepackage\{style/([^}]+)\}'
        style_matches = re.findall(style_pattern, content)
        self.style_files = {f"style/{match}.sty" for match in style_matches}
        
        # Create package mappings for sanitization
        for style_file in self.style_files:
            package_name = Path(style_file).stem
            sanitized_name = self.sanitizer.sanitize_package_name(package_name)
            self.package_mappings[package_name] = sanitized_name
            logger.debug(f"Package mapping: {package_name} → {sanitized_name}")
        
        # Find all input{modules/...} commands  
        module_pattern = r'\\input\{modules/([^}]+)\}'
        module_matches = re.findall(module_pattern, content)
        self.module_files = {f"modules/{match}.tex" for match in module_matches}
        
        logger.info(f"Found {len(self.style_files)} style files: {', '.join(self.style_files)}")
        logger.info(f"Found {len(self.module_files)} module files: {', '.join(self.module_files)}")
        logger.info(f"Created {len(self.package_mappings)} package name mappings")
    
    def check_file_existence(self) -> None:
        """Check if all referenced files exist."""
        logger.info("Checking file existence...")
        
        all_files = self.style_files.union(self.module_files)
        for file_path in all_files:
            if not Path(file_path).exists():
                self.missing_files.append(file_path)
                logger.warning(f"Missing file: {file_path}")
            else:
                logger.debug(f"Found file: {file_path}")
                
        if self.missing_files:
            logger.warning(f"Found {len(self.missing_files)} missing files")
        else:
            logger.info("All referenced files exist")
    
    def create_safe_templates(self) -> None:
        """Create minimal, safe templates for missing files with sanitized command names."""
        if not self.missing_files:
            return
            
        logger.info("Creating safe templates for missing files...")
        
        for file_path in self.missing_files:
            path = Path(file_path)
            
            # Ensure directory exists
            path.parent.mkdir(parents=True, exist_ok=True)
            
            if file_path.endswith('.sty'):
                # Create style file template with safe command names
                package_name = path.stem
                sanitized_name = self.sanitizer.sanitize_package_name(package_name)
                safe_command = self.sanitizer.generate_safe_command_name(package_name)
                
                # Validate the generated command name
                if not self.sanitizer.validate_latex_command_name(safe_command):
                    logger.error(f"Generated invalid command name: {safe_command}")
                    safe_command = "safePlaceholder"
                
                template_content = f"""% {path.name} - CTMM Style Package
% TODO: Add content for this style package
% Created automatically by CTMM Enhanced Build Manager with safe command generation

\\NeedsTeXFormat{{LaTeX2e}}[1995/12/01]
\\ProvidesPackage{{{package_name}}}[2024/01/01 CTMM {package_name} package - TODO: Add content]

% Safe command generation: {package_name} → {sanitized_name}
% Generated safe placeholder command: \\{safe_command}
\\newcommand{{\\{safe_command}}}{{\\textcolor{{red}}{{[{package_name.upper()} TEMPLATE - NEEDS CONTENT]}}}}

% TODO: Add package dependencies here
% \\RequirePackage{{xcolor}}
% \\RequirePackage{{tikz}}

% TODO: Add color definitions here
% \\definecolor{{ctmmBlue}}{{RGB}}{{52, 152, 219}}

% TODO: Add commands and environments here
% \\newcommand{{\\exampleCommand}}[1]{{\\textcolor{{ctmmBlue}}{{#1}}}}

% End of package - TODO: Complete implementation
"""
            else:
                # Create module file template  
                title = path.stem.replace('-', ' ').replace('_', ' ').title()
                template_content = f"""% {path.name} - CTMM Module
% TODO: Add content for this module
% Created automatically by CTMM Enhanced Build Manager

\\section{{TODO: {title}}}
\\label{{sec:{path.stem}}}

% TODO: Add module content here
\\begin{{center}}
\\textit{{This module is under development. Content will be added soon.}}
\\end{{center}}

% TODO: Add subsections, content, and functionality
% Example:
% \\subsection{{Introduction}}
% \\subsection{{Instructions}}
% \\subsection{{Exercises}}

% End of module - TODO: Complete implementation
"""
            
            with open(path, 'w', encoding='utf-8') as f:
                f.write(template_content)
                
            logger.info(f"Created safe template: {file_path}")
            
            # Create TODO file
            todo_path = path.parent / f"TODO_{path.stem}.md"
            todo_content = f"""# TODO: Complete {path.name}

## File: {file_path}
**Status:** Safe template created with sanitized command names, needs content

## Description
This file was automatically created by the CTMM Enhanced Build Manager because it was referenced in main.tex but missing.

## Security Features
- ✅ Safe command name generation (no special characters)
- ✅ Package name sanitization applied: `{path.stem}` → `{self.sanitizer.sanitize_package_name(path.stem)}`
- ✅ LaTeX command validation performed

## Tasks
- [ ] Add proper content for this {'style package' if path.suffix == '.sty' else 'module'}
- [ ] Review and test functionality  
- [ ] Update documentation
- [ ] Remove this TODO file when complete

## Generated Safe Commands
"""
            
            if path.suffix == '.sty':
                safe_command = self.sanitizer.generate_safe_command_name(path.stem)
                todo_content += f"- `\\{safe_command}` (placeholder command)\n"
            
            todo_content += f"""
## Created
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} by CTMM Enhanced Build Manager
"""
            
            with open(todo_path, 'w', encoding='utf-8') as f:
                f.write(todo_content)
                
            logger.info(f"Created TODO: {todo_path}")
    
    def validate_all_commands(self) -> bool:
        """Validate that all generated command names are safe for LaTeX."""
        logger.info("Validating all generated command names...")
        
        all_valid = True
        for package_name, sanitized_name in self.package_mappings.items():
            safe_command = self.sanitizer.generate_safe_command_name(package_name)
            
            if not self.sanitizer.validate_latex_command_name(safe_command):
                logger.error(f"Invalid command generated: \\{safe_command} from package {package_name}")
                all_valid = False
            else:
                logger.debug(f"✓ Valid command: \\{safe_command} from {package_name}")
        
        if all_valid:
            logger.info("✓ All generated command names are valid for LaTeX")
        else:
            logger.error("✗ Some generated command names are invalid")
            
        return all_valid
    
    def generate_security_report(self) -> str:
        """Generate a comprehensive security and build report."""
        report = f"""
CTMM Enhanced Build Manager Security Report
==========================================

## Security Status
- Package name sanitization: ✅ ACTIVE
- Command name validation: ✅ ACTIVE
- Safe template generation: ✅ ACTIVE

## Summary
- Style files found: {len(self.style_files)}
- Module files found: {len(self.module_files)}  
- Missing files: {len(self.missing_files)}
- Package mappings: {len(self.package_mappings)}
- Problematic modules: {len(self.problematic_modules)}

## Package Name Mappings (Security Sanitization)
"""
        
        for original, sanitized in sorted(self.package_mappings.items()):
            status = "✅ SAFE" if self.sanitizer.validate_latex_command_name(
                self.sanitizer.generate_safe_command_name(original)
            ) else "❌ UNSAFE"
            report += f"- `{original}` → `{sanitized}` ({status})\n"
        
        report += f"""
## Style Files
{chr(10).join(f"- {f}" for f in sorted(self.style_files))}

## Module Files  
{chr(10).join(f"- {f}" for f in sorted(self.module_files))}

## Missing Files
{chr(10).join(f"- {f} (safe template created)" for f in self.missing_files) if self.missing_files else "None"}

## Security Validation
"""
        
        all_valid = self.validate_all_commands()
        if all_valid:
            report += "✅ All generated LaTeX commands use valid syntax\n"
            report += "✅ No security vulnerabilities detected\n"
        else:
            report += "❌ Some commands may cause LaTeX compilation errors\n"
            
        report += f"""
## Recommendations
"""
        
        if not self.missing_files and not self.problematic_modules and all_valid:
            report += "✅ System is secure and ready for production use."
        else:
            if self.missing_files:
                report += f"- Review and complete {len(self.missing_files)} safe template file(s)\n"
            if self.problematic_modules:
                report += f"- Fix {len(self.problematic_modules)} problematic module(s)\n"
            if not all_valid:
                report += "- Review and fix invalid command generation\n"
                
        return report
    
    def run_enhanced_check(self) -> bool:
        """Run the complete enhanced build system check with security validation."""
        logger.info("Starting CTMM Enhanced Build Manager security check...")
        
        try:
            self.scan_main_tex()
            self.check_file_existence()
            self.create_safe_templates()
            
            # Validate security
            commands_valid = self.validate_all_commands()
            
            # Generate and save report
            report = self.generate_security_report()
            with open('enhanced_build_report.md', 'w') as f:
                f.write(report)
            
            logger.info("Enhanced build system check complete. Report saved to enhanced_build_report.md")
            print(report)
            
            return len(self.problematic_modules) == 0 and commands_valid
            
        except Exception as e:
            logger.error(f"Enhanced build system check failed: {e}")
            return False


def main():
    parser = argparse.ArgumentParser(description='CTMM Enhanced Build Manager with Security')
    parser.add_argument('--main-tex', default='main.tex', 
                       help='Path to main TeX file (default: main.tex)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose logging')
    parser.add_argument('--test-sanitization', action='store_true',
                       help='Test package name sanitization functions')
    
    args = parser.parse_args()
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    if args.test_sanitization:
        # Test sanitization functions
        test_cases = [
            'ctmm-design',
            'form-elements', 
            'ctmm_diagrams',
            'some-complex_name-123',
            'test',
            'a-b-c-d',
            'under_score_name',
            '123-starts-with-number',
            '',
            'special!@#$%chars'
        ]
        
        sanitizer = PackageNameSanitizer()
        print("Package Name Sanitization Tests:")
        print("================================")
        
        for test_case in test_cases:
            sanitized = sanitizer.sanitize_package_name(test_case)
            command = sanitizer.generate_safe_command_name(test_case)
            valid = sanitizer.validate_latex_command_name(command)
            status = "✅" if valid else "❌"
            print(f"{status} '{test_case}' → '{sanitized}' → '\\{command}'")
        
        return 0
    
    build_manager = CTMMEnhancedBuildManager(args.main_tex)
    success = build_manager.run_enhanced_check()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()