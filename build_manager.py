#!/usr/bin/env python3
"""
CTMM Comprehensive Automated Build Management System

This script implements a sophisticated build management system that:
1. Scans main.tex for all usepackage{style/...} and input{modules/...} references
2. Automatically detects missing files and creates minimal, well-structured templates
3. Implements incremental testing strategy that isolates module-specific build errors
4. Generates comprehensive build reports in build_report.md
5. Provides robust error handling with helpful installation guidance

Key Features:
- Automated template generation for missing files
- Incremental module testing to identify problematic modules
- Comprehensive error reporting and logging
- Installation guidance for missing dependencies
- CI/CD integration with main_final.tex
"""

import os
import re
import subprocess
import sys
import datetime
import shutil
from pathlib import Path
from typing import List, Tuple, Dict, Set, Optional
import argparse
import logging

# Configure logging with consistent [INFO] style formatting
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('build_manager.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class CTMMBuildManager:
    """Comprehensive build management system for CTMM LaTeX project."""
    
    def __init__(self, main_tex_path: str = "main.tex"):
        self.main_tex_path = Path(main_tex_path)
        self.style_files: Set[str] = set()
        self.module_files: Set[str] = set()
        self.missing_files: List[str] = []
        self.problematic_modules: List[str] = []
        self.build_success: bool = False
        self.build_errors: List[str] = []
        
    def _read_file_safely(self, file_path: Path) -> str:
        """Read a file with UTF-8 encoding and error handling."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            logger.warning(f"UTF-8 decode error for {file_path}, trying with error replacement")
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Failed to read {file_path}: {e}")
            return ""
    
    def scan_main_tex(self) -> None:
        """Scan main.tex for all package and module references."""
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
        
        logger.info(f"Found {len(self.style_files)} style files and {len(self.module_files)} module files")
        
    def check_file_existence(self) -> None:
        """Check if all referenced files exist and identify missing files."""
        logger.info("Checking file existence...")
        
        all_files = self.style_files.union(self.module_files)
        for file_path in all_files:
            if not Path(file_path).exists():
                self.missing_files.append(file_path)
                logger.warning(f"Missing file: {file_path}")
                
        if self.missing_files:
            logger.warning(f"Found {len(self.missing_files)} missing files")
        else:
            logger.info("All referenced files exist")
    
    def create_minimal_templates(self) -> None:
        """Create minimal, well-structured templates for missing files."""
        if not self.missing_files:
            return
            
        logger.info("Creating minimal templates for missing files...")
        
        for file_path in self.missing_files:
            path = Path(file_path)
            
            # Ensure directory exists
            path.parent.mkdir(parents=True, exist_ok=True)
            
            if file_path.endswith('.sty'):
                # Create style package template
                template_content = f"""\\NeedsTeXFormat{{LaTeX2e}}
\\ProvidesPackage{{{path.stem}}}[{datetime.datetime.now().strftime('%Y/%m/%d')} {path.stem.replace('-', ' ').title()} Package - Template]

% TODO: Add package dependencies here
% \\RequirePackage{{xcolor}}
% \\RequirePackage{{tikz}}

% TODO: Add package content here

% End of package
"""
            else:
                # Create module template  
                template_content = f"""\\section{{{path.stem.replace('-', ' ').title()}}}
\\label{{sec:{path.stem}}}

% TODO: Add actual module content

\\begin{{center}}
\\textit{{This module is under development. Content will be added soon.}}
\\end{{center}}

% TODO: Complete implementation
"""
            
            with open(path, 'w', encoding='utf-8') as f:
                f.write(template_content)
                
            logger.info(f"Created template: {file_path}")
            
            # Create TODO file
            todo_path = path.parent / f"TODO_{path.stem}.md"
            todo_content = f"""# TODO: Complete {path.name}

**Status:** Template created, needs content

## Tasks
- [ ] Add proper content
- [ ] Review and test functionality
- [ ] Update documentation

Created by CTMM Build Manager on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
            with open(todo_path, 'w', encoding='utf-8') as f:
                f.write(todo_content)
                
            logger.info(f"Created TODO: {todo_path}")
    
    def test_basic_build(self, target_file: Optional[str] = None) -> bool:
        """Test basic build with modules temporarily commented out."""
        test_file = target_file or str(self.main_tex_path)
        logger.info(f"Testing basic build (without modules) for {test_file}...")
        
        content = self._read_file_safely(Path(test_file))
            
        # Comment out all input{modules/...} lines
        modified_content = re.sub(
            r'(\\input\{modules/[^}]+\})',
            r'% \1  % Temporarily commented by build manager',
            content
        )
        
        temp_file = Path(test_file).with_suffix('.basic_test.tex')
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(modified_content)
            
        try:
            # Test build
            result = subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', temp_file.name],
                capture_output=True,
                text=True,
                errors='replace'
            )
            
            success = result.returncode == 0
            if success:
                logger.info("✓ Basic build successful")
            else:
                logger.error("✗ Basic build failed")
                self.build_errors.append(f"Basic build failed: {result.stderr}")
                
            return success
            
        except Exception as e:
            logger.error(f"Build test failed: {e}")
            return False
        finally:
            # Clean up temporary files
            self._cleanup_build_files(temp_file)
    
    def test_incremental_modules(self) -> None:
        """Implement incremental testing strategy to isolate module-specific build errors."""
        if not self.module_files:
            logger.info("No modules to test incrementally")
            return
            
        logger.info("Starting incremental module testing...")
        
        original_content = self._read_file_safely(self.main_tex_path)
        module_list = sorted(list(self.module_files))
        
        for i, current_module in enumerate(module_list):
            logger.info(f"Testing with modules 0-{i}: adding {current_module}")
            
            # Create content with modules 0 to i enabled
            modified_content = original_content
            for j, module in enumerate(module_list):
                module_name = Path(module).stem
                if j > i:
                    # Comment out modules beyond current index
                    pattern = f"\\\\input\\{{modules/{module_name}\\}}"
                    modified_content = re.sub(
                        pattern,
                        f"% \\\\input{{modules/{module_name}}}  % Disabled for incremental testing",
                        modified_content
                    )
            
            # Test build with current module set
            temp_file = Path(f"main_test_{i:02d}.tex")
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(modified_content)
                
            try:
                result = subprocess.run(
                    ['pdflatex', '-interaction=nonstopmode', temp_file.name],
                    capture_output=True,
                    text=True,
                    errors='replace'
                )
                
                if result.returncode == 0:
                    logger.info(f"✓ Build successful with {current_module}")
                else:
                    logger.error(f"✗ Build failed when adding {current_module}")
                    self.problematic_modules.append(current_module)
                    
                    # Save detailed error log
                    error_log = f"build_error_{Path(current_module).stem}.log"
                    with open(error_log, 'w') as f:
                        f.write(f"Build error when testing {current_module}\\n")
                        f.write(f"Return code: {result.returncode}\\n\\n")
                        f.write("STDOUT:\\n")
                        f.write(result.stdout)
                        f.write("\\n\\nSTDERR:\\n")
                        f.write(result.stderr)
                    
                    logger.error(f"Error details saved to {error_log}")
                    
            except Exception as e:
                logger.error(f"Incremental test failed for {current_module}: {e}")
                self.problematic_modules.append(current_module)
            finally:
                self._cleanup_build_files(temp_file)
    
    def test_full_build(self, target_file: Optional[str] = None) -> bool:
        """Test full build with all modules enabled."""
        test_file = target_file or str(self.main_tex_path)
        logger.info(f"Testing full build for {test_file}...")
        
        try:
            result = subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', test_file],
                capture_output=True,
                text=True,
                errors='replace'
            )
            
            success = result.returncode == 0
            if success:
                logger.info("✓ Full build successful")
                pdf_path = Path(test_file).with_suffix('.pdf')
                if pdf_path.exists():
                    logger.info(f"✓ PDF generated: {pdf_path}")
            else:
                logger.error("✗ Full build failed")
                self.build_errors.append(f"Full build failed: {result.stderr}")
                
            self.build_success = success
            return success
            
        except Exception as e:
            logger.error(f"Full build test failed: {e}")
            return False
    
    def _cleanup_build_files(self, base_file: Path) -> None:
        """Clean up auxiliary files from build process."""
        extensions = ['.aux', '.log', '.out', '.toc', '.pdf']
        for ext in extensions:
            aux_file = base_file.with_suffix(ext)
            if aux_file.exists():
                aux_file.unlink()
        
        # Remove the test file itself
        if base_file.exists():
            base_file.unlink()
    
    def check_latex_installation(self) -> bool:
        """Check if LaTeX is properly installed with required packages."""
        logger.info("Checking LaTeX installation...")
        
        # Check if pdflatex is available
        try:
            result = subprocess.run(['pdflatex', '--version'], 
                                 capture_output=True, text=True)
            if result.returncode != 0:
                logger.error("pdflatex not found")
                return False
            logger.info("✓ pdflatex found")
        except FileNotFoundError:
            logger.error("pdflatex not found in PATH")
            self._provide_installation_guidance()
            return False
        
        # Check for required packages by trying a minimal document
        test_doc = r"""\documentclass{article}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage[ngerman]{babel}
\usepackage{xcolor}
\usepackage{hyperref}
\usepackage{tcolorbox}
\usepackage{fontawesome5}
\usepackage{amssymb}
\begin{document}
Test
\end{document}"""
        
        test_file = Path('latex_test.tex')
        try:
            with open(test_file, 'w') as f:
                f.write(test_doc)
            
            result = subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', 'latex_test.tex'],
                capture_output=True, text=True
            )
            
            if result.returncode == 0:
                logger.info("✓ Required LaTeX packages available")
                return True
            else:
                logger.error("✗ Missing required LaTeX packages")
                self._provide_installation_guidance()
                return False
                
        finally:
            self._cleanup_build_files(test_file)
    
    def _provide_installation_guidance(self) -> None:
        """Provide helpful installation guidance for missing dependencies."""
        guidance = """
[INFO] LaTeX Installation Guidance:

Ubuntu/Debian:
  sudo apt-get install texlive-latex-base texlive-latex-extra \\
                       texlive-fonts-recommended texlive-lang-german

macOS (with Homebrew):
  brew install --cask mactex

Windows:
  Download and install MiKTeX from https://miktex.org/

Additional packages may be required:
  - fontawesome5: sudo apt-get install texlive-fonts-extra
  - tcolorbox: Usually included in texlive-latex-extra

After installation, run 'python3 build_manager.py' again.
"""
        logger.info(guidance)
    
    def generate_comprehensive_report(self) -> str:
        """Generate comprehensive build report in markdown format."""
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        report = f"""# CTMM Build System Report

Generated: {timestamp}

## Summary
- **Style files found**: {len(self.style_files)}
- **Module files found**: {len(self.module_files)}
- **Missing files**: {len(self.missing_files)}
- **Problematic modules**: {len(self.problematic_modules)}
- **Build status**: {'✓ SUCCESS' if self.build_success else '✗ FAILED'}

## File Analysis

### Style Files
"""
        for style_file in sorted(self.style_files):
            status = "✓ EXISTS" if Path(style_file).exists() else "✗ MISSING"
            report += f"- {style_file} - {status}\\n"

        report += f"""
### Module Files
"""
        for module_file in sorted(self.module_files):
            status = "✓ EXISTS" if Path(module_file).exists() else "✗ MISSING"
            if module_file in self.problematic_modules:
                status += " (PROBLEMATIC)"
            report += f"- {module_file} - {status}\\n"

        if self.missing_files:
            report += f"""
### Missing Files (Templates Created)
"""
            for missing_file in self.missing_files:
                report += f"- {missing_file}\\n"

        if self.problematic_modules:
            report += f"""
### Problematic Modules
"""
            for problem_module in self.problematic_modules:
                report += f"- {problem_module}\\n"

        if self.build_errors:
            report += f"""
### Build Errors
"""
            for error in self.build_errors:
                report += f"- {error}\\n"

        report += f"""
## Recommendations

"""
        if not self.missing_files and not self.problematic_modules and self.build_success:
            report += "✅ **System is healthy!** All files exist and build successfully."
        else:
            if self.missing_files:
                report += f"1. **Complete template files**: Review and add content to {len(self.missing_files)} generated templates\\n"
                report += "2. **Remove TODO files**: Delete TODO_*.md files when templates are complete\\n"
            
            if self.problematic_modules:
                report += f"3. **Fix problematic modules**: Address issues in {len(self.problematic_modules)} modules\\n"
                report += "4. **Check error logs**: Review build_error_*.log files for details\\n"
            
            if not self.build_success:
                report += "5. **Resolve build errors**: Check main.log for detailed error information\\n"

        report += f"""
## Next Steps

1. Run `make build` to build the PDF
2. Use `make analyze` for detailed module analysis  
3. Run `make clean` to remove build artifacts
4. Check individual error logs for specific issues

---
*Report generated by CTMM Build Manager v1.0*
"""
        return report
    
    def run_complete_analysis(self) -> bool:
        """Run the complete build analysis workflow."""
        logger.info("Starting CTMM Build Manager comprehensive analysis...")
        
        try:
            # Step 1: Check LaTeX installation
            if not self.check_latex_installation():
                return False
            
            # Step 2: Scan main.tex
            self.scan_main_tex()
            
            # Step 3: Check file existence
            self.check_file_existence()
            
            # Step 4: Create templates for missing files
            self.create_minimal_templates()
            
            # Step 5: Test basic build
            basic_build_ok = self.test_basic_build()
            
            # Step 6: If basic build works, test incremental modules
            if basic_build_ok:
                self.test_incremental_modules()
            
            # Step 7: Test full build
            full_build_ok = self.test_full_build()
            
            # Step 8: Generate comprehensive report
            report = self.generate_comprehensive_report()
            
            # Save report
            with open('build_report.md', 'w') as f:
                f.write(report)
            
            logger.info("Build analysis complete. Report saved to build_report.md")
            print("\\n" + "="*60)
            print("CTMM BUILD MANAGER SUMMARY")
            print("="*60)
            print(f"Style files: {len(self.style_files)}")
            print(f"Module files: {len(self.module_files)}")
            print(f"Missing files: {len(self.missing_files)}")
            print(f"Problematic modules: {len(self.problematic_modules)}")
            print(f"Build status: {'✓ SUCCESS' if self.build_success else '✗ FAILED'}")
            
            if self.missing_files or self.problematic_modules:
                print("\\n📋 See build_report.md for detailed analysis and recommendations")
            
            return self.build_success and len(self.problematic_modules) == 0
            
        except Exception as e:
            logger.error(f"Build analysis failed: {e}")
            return False

def main():
    """Main entry point for CTMM Build Manager."""
    parser = argparse.ArgumentParser(description='CTMM Comprehensive Build Management System')
    parser.add_argument('--main-tex', default='main.tex', 
                       help='Path to main TeX file (default: main.tex)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose logging')
    parser.add_argument('--test-file', 
                       help='Test specific file instead of main.tex')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    build_manager = CTMMBuildManager(args.main_tex)
    
    # If testing specific file, just test that file
    if args.test_file:
        logger.info(f"Testing specific file: {args.test_file}")
        basic_ok = build_manager.test_basic_build(args.test_file)
        full_ok = build_manager.test_full_build(args.test_file)
        success = basic_ok and full_ok
    else:
        # Run complete analysis
        success = build_manager.run_complete_analysis()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()