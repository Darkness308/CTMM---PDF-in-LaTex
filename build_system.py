#!/usr/bin/env python3
"""
CTMM LaTeX Build System
Scalable, modular and efficient build process with automatic error detection and handling.

This script:
1. Scans main.tex for all usepackage{style/...} and input{modules/...} commands
2. Checks if referenced files exist, creates minimal templates if missing
3. Tests build with temporarily commented input lines  
4. Gradually reactivates input lines to identify problematic modules
5. Creates TODO comments and issues for new files
6. Logs all operations for debugging
"""

import os
import re
import subprocess
import sys
import tempfile
import shutil
import chardet
from pathlib import Path
from typing import List, Tuple, Dict, Set
import argparse
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('build_system.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class CTMMBuildSystem:
    def __init__(self, main_tex_path: str = "main.tex"):
        self.main_tex_path = Path(main_tex_path)
        self.style_files: Set[str] = set()
        self.module_files: Set[str] = set()
        self.missing_files: List[str] = []
        self.problematic_modules: List[str] = []
        
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
        
        # Find all input{modules/...} commands  
        module_pattern = r'\\input\{modules/([^}]+)\}'
        module_matches = re.findall(module_pattern, content)
        self.module_files = {f"modules/{match}.tex" for match in module_matches}
        
        logger.info(f"Found {len(self.style_files)} style files: {', '.join(self.style_files)}")
        logger.info(f"Found {len(self.module_files)} module files: {', '.join(self.module_files)}")
    
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
    
    def create_minimal_templates(self) -> None:
        """Create minimal, commented templates for missing files."""
        if not self.missing_files:
            return
            
        logger.info("Creating minimal templates for missing files...")
        
        for file_path in self.missing_files:
            path = Path(file_path)
            
            # Ensure directory exists
            path.parent.mkdir(parents=True, exist_ok=True)
            
            if file_path.endswith('.sty'):
                # Create style file template
                template_content = f"""% {path.name} - CTMM Style Package
% TODO: Add content for this style package
% Created automatically by CTMM Build System

\\NeedsTeXFormat{{LaTeX2e}}[1995/12/01]
\\ProvidesPackage{{{path.stem}}}[2024/01/01 CTMM {path.stem} package - TODO: Add content]

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
                template_content = f"""% {path.name} - CTMM Module
% TODO: Add content for this module
% Created automatically by CTMM Build System

\\section{{TODO: {path.stem.replace('-', ' ').title()}}}
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
                
            logger.info(f"Created template: {file_path}")
            
            # Create TODO file
            todo_path = path.parent / f"TODO_{path.stem}.md"
            todo_content = f"""# TODO: Complete {path.name}

## File: {file_path}
**Status:** Template created, needs content

## Description
This file was automatically created by the CTMM Build System because it was referenced in main.tex but missing.

## Tasks
- [ ] Add proper content for this {'style package' if path.suffix == '.sty' else 'module'}
- [ ] Review and test functionality  
- [ ] Update documentation
- [ ] Remove this TODO file when complete

## Created
{datetime.fromtimestamp(path.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S') if path.exists() else 'Just now'} by CTMM Build System
"""
            with open(todo_path, 'w', encoding='utf-8') as f:
                f.write(todo_content)
                
            logger.info(f"Created TODO: {todo_path}")
    
    def test_basic_build(self) -> bool:
        """Test build with all input lines temporarily commented out."""
        logger.info("Testing basic build with modules commented out...")
        
        # Test build with all input lines temporarily commented out
        content = self._read_file_safely(self.main_tex_path)
            
        # Comment out all input{modules/...} lines
        modified_content = re.sub(
            r'(\\input\{modules/[^}]+\})',
            r'% \1  % Temporarily commented by build system',
            content
        )
        
        temp_file = self.main_tex_path.with_suffix('.temp.tex')
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(modified_content)
            
        try:
            # Test build
            result = subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', temp_file.name],
                capture_output=True,
                text=True,
                cwd=str(self.main_tex_path.parent)
            )
            
            success = result.returncode == 0
            if success:
                logger.info("Basic build (without modules) successful")
            else:
                logger.error("Basic build failed even without modules")
                logger.error(f"Error output: {result.stderr}")
                
            return success
            
        finally:
            # Clean up
            if temp_file.exists():
                temp_file.unlink()
            # Remove auxiliary files
            for ext in ['.aux', '.log', '.out', '.toc']:
                aux_file = temp_file.with_suffix(ext)
                if aux_file.exists():
                    aux_file.unlink()
    
    def test_modules_incrementally(self) -> None:
        """Gradually reactivate input lines to identify problematic modules."""
        if not self.module_files:
            logger.info("No modules to test")
            return
            
        logger.info("Testing modules incrementally...")
        
        original_content = self._read_file_safely(self.main_tex_path)
            
        module_list = sorted(list(self.module_files))
        
        for i, current_module in enumerate(module_list):
            logger.info(f"Testing with modules 0-{i}: {' '.join(module_list[:i+1])}")
            
            # Create content with modules 0 to i enabled
            modified_content = original_content
            for j, module in enumerate(module_list):
                module_pattern = f"modules/{Path(module).stem}"
                input_pattern = f"\\input{{{module_pattern}}}"
                
                if j <= i:
                    # Keep this module enabled
                    continue
                else:
                    # Comment out this module
                    modified_content = re.sub(
                        f'(\\\\input\\{{{module_pattern}\\}})',
                        r'% \1  % Disabled for incremental testing',
                        modified_content
                    )
            
            # Test build with current module set
            temp_file = self.main_tex_path.with_suffix(f'.test_{i}.tex')
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(modified_content)
                
            try:
                result = subprocess.run(
                    ['pdflatex', '-interaction=nonstopmode', temp_file.name],
                    capture_output=True,
                    text=True,
                    cwd=str(self.main_tex_path.parent)
                )
                
                if result.returncode == 0:
                    logger.info(f"✓ Build successful with {current_module}")
                else:
                    logger.error(f"✗ Build failed when adding {current_module}")
                    self.problematic_modules.append(current_module)
                    
                    # Log error details
                    error_log = f"build_error_{Path(current_module).stem}.log"
                    with open(error_log, 'w') as f:
                        f.write(f"Build error when testing {current_module}\n")
                        f.write(f"Return code: {result.returncode}\n\n")
                        f.write("STDOUT:\n")
                        f.write(result.stdout)
                        f.write("\n\nSTDERR:\n")
                        f.write(result.stderr)
                    
                    logger.error(f"Error details saved to {error_log}")
                    
            finally:
                # Clean up
                if temp_file.exists():
                    temp_file.unlink()
                for ext in ['.aux', '.log', '.out', '.toc', '.pdf']:
                    aux_file = temp_file.with_suffix(ext)
                    if aux_file.exists():
                        aux_file.unlink()
    
    def generate_report(self) -> str:
        """Generate a comprehensive build report."""
        report = f"""
CTMM Build System Report
========================

## Summary
- Style files found: {len(self.style_files)}
- Module files found: {len(self.module_files)}  
- Missing files: {len(self.missing_files)}
- Problematic modules: {len(self.problematic_modules)}

## Style Files
{chr(10).join(f"- {f}" for f in sorted(self.style_files))}

## Module Files  
{chr(10).join(f"- {f}" for f in sorted(self.module_files))}

## Missing Files
{chr(10).join(f"- {f} (template created)" for f in self.missing_files) if self.missing_files else "None"}

## Problematic Modules
{chr(10).join(f"- {f}" for f in self.problematic_modules) if self.problematic_modules else "None"}

## Recommendations
"""
        
        if not self.missing_files and not self.problematic_modules:
            report += "✓ All files exist and build successfully. No action needed."
        else:
            if self.missing_files:
                report += f"- Review and complete {len(self.missing_files)} template file(s)\n"
            if self.problematic_modules:
                report += f"- Fix {len(self.problematic_modules)} problematic module(s)\n"
                
        return report
    
    def run_full_check(self) -> bool:
        """Run the complete build system check."""
        logger.info("Starting CTMM Build System full check...")
        
        try:
            self.scan_main_tex()
            self.check_file_existence()
            self.create_minimal_templates()
            
            basic_build_ok = self.test_basic_build()
            if basic_build_ok:
                self.test_modules_incrementally()
            
            # Generate and save report
            report = self.generate_report()
            with open('build_report.md', 'w') as f:
                f.write(report)
            
            logger.info("Build system check complete. Report saved to build_report.md")
            print(report)
            
            return len(self.problematic_modules) == 0
            
        except Exception as e:
            logger.error(f"Build system check failed: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(description='CTMM LaTeX Build System')
    parser.add_argument('--main-tex', default='main.tex', 
                       help='Path to main TeX file (default: main.tex)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose logging')
    
    args = parser.parse_args()
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    build_system = CTMMBuildSystem(args.main_tex)
    success = build_system.run_full_check()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()