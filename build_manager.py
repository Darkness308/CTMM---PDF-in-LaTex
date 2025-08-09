#!/usr/bin/env python3
"""
CTMM Build Manager - Comprehensive Automated Build Management System
Significantly improves CI/CD reliability and developer workflow for the CTMM LaTeX project.

This implementation addresses all code review feedback and provides sophisticated error detection,
template generation, and incremental testing capabilities.

Key Features:
- Scans main.tex for all \\usepackage{style/...} and \\input{modules/...} references
- Automatically detects missing files and creates minimal, well-structured templates
- Implements incremental testing strategy that isolates module-specific build errors
- Generates comprehensive build reports in build_report.md
- Provides robust error handling with helpful installation guidance
"""

import datetime
import logging
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import List, Tuple, Dict, Set, Optional
import argparse

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
    """Comprehensive automated build management system for CTMM LaTeX project."""
    
    def __init__(self, main_tex_path: str = "main.tex"):
        self.main_tex_path = Path(main_tex_path)
        self.style_files: Set[str] = set()
        self.module_files: Set[str] = set()
        self.missing_files: List[str] = []
        self.problematic_modules: List[str] = []
        self.build_successful: bool = False
        self.basic_build_successful: bool = False
        
    def _read_file_safely(self, file_path: Path) -> str:
        """Read a file with automatic encoding detection and error handling."""
        try:
            # Try UTF-8 first
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            # Fallback to latin-1 for older files
            logger.debug(f"[INFO] UTF-8 failed for {file_path}, trying latin-1")
            try:
                with open(file_path, 'r', encoding='latin-1') as f:
                    return f.read()
            except UnicodeDecodeError:
                logger.warning(f"[WARNING] Encoding issues with {file_path}, using error replacement")
                with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                    return f.read()
        except Exception as e:
            logger.error(f"[ERROR] Failed to read {file_path}: {e}")
            return ""
    
    def scan_main_tex(self) -> None:
        """Scan main.tex for all usepackage{style/...} and input{modules/...} commands."""
        logger.info(f"[INFO] Scanning {self.main_tex_path} for package and input references...")
        
        if not self.main_tex_path.exists():
            logger.error(f"[ERROR] Main TeX file {self.main_tex_path} not found!")
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
        
        logger.info(f"[INFO] Found {len(self.style_files)} style files and {len(self.module_files)} module files")
        for style_file in sorted(self.style_files):
            logger.debug(f"[INFO]   Style: {style_file}")
        for module_file in sorted(self.module_files):
            logger.debug(f"[INFO]   Module: {module_file}")
    
    def check_file_existence(self) -> None:
        """Check if all referenced files exist and identify missing ones."""
        logger.info("[INFO] Checking file existence...")
        
        all_files = self.style_files.union(self.module_files)
        for file_path in all_files:
            if not Path(file_path).exists():
                self.missing_files.append(file_path)
                logger.warning(f"[WARNING] Missing file: {file_path}")
            else:
                logger.debug(f"[INFO] Found file: {file_path}")
                
        if self.missing_files:
            logger.warning(f"[WARNING] Found {len(self.missing_files)} missing files")
        else:
            logger.info("[INFO] All referenced files exist")
    
    def create_template_files(self) -> None:
        """Create minimal, well-structured templates for missing files."""
        if not self.missing_files:
            return
            
        logger.info("[INFO] Creating minimal templates for missing files...")
        
        for file_path in self.missing_files:
            path = Path(file_path)
            
            # Ensure directory exists
            path.parent.mkdir(parents=True, exist_ok=True)
            
            if file_path.endswith('.sty'):
                # Create properly structured style file template
                package_name = path.stem
                template_content = f"""% {path.name} - CTMM Style Package
% Created automatically by CTMM Build Manager on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
% TODO: Add content for this style package

\\NeedsTeXFormat{{LaTeX2e}}
\\ProvidesPackage{{{package_name}}}[{datetime.datetime.now().strftime('%Y/%m/%d')} Package Description - Template]

% TODO: Add package dependencies here
% \\RequirePackage{{xcolor}}
% \\RequirePackage{{tikz}}
% \\RequirePackage{{tcolorbox}}

% TODO: Add color definitions here
% \\definecolor{{ctmmBlue}}{{RGB}}{{52, 152, 219}}
% \\definecolor{{ctmmOrange}}{{RGB}}{{243, 156, 18}}
% \\definecolor{{ctmmGreen}}{{RGB}}{{46, 204, 113}}
% \\definecolor{{ctmmPurple}}{{RGB}}{{155, 89, 182}}

% TODO: Add commands and environments here
% \\newcommand{{\\exampleCommand}}[1]{{\\textcolor{{ctmmBlue}}{{#1}}}}
% \\newenvironment{{exampleBox}}[1]{{%
%   \\begin{{tcolorbox}}[title=#1,colback=ctmmBlue!10,colframe=ctmmBlue]
% }}{{%
%   \\end{{tcolorbox}}
% }}

% End of package - TODO: Complete implementation
"""
            else:
                # Create properly structured module template
                module_name = path.stem.replace('-', ' ').replace('_', ' ').title()
                template_content = f"""% {path.name} - CTMM Module
% Created automatically by CTMM Build Manager on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
% TODO: Add content for this module

\\section{{{module_name}}}
\\label{{sec:{path.stem}}}

% TODO: Add module content here
\\begin{{center}}
\\textit{{This module is under development. Content will be added soon.}}
\\end{{center}}

% TODO: Add subsections and content
% \\subsection{{Introduction}}
% \\subsection{{Instructions}}
% \\subsection{{Exercises}}

% TODO: Add interactive elements if needed
% \\begin{{ctmmBlueBox}}{{Information}}
% Add informational content here.
% \\end{{ctmmBlueBox}}

% End of module - TODO: Complete implementation
"""
            
            with open(path, 'w', encoding='utf-8') as f:
                f.write(template_content)
                
            logger.info(f"[INFO] Created template: {file_path}")
            
            # Create comprehensive TODO file
            todo_path = path.parent / f"TODO_{path.stem}.md"
            file_type = 'style package' if path.suffix == '.sty' else 'module'
            todo_content = f"""# TODO: Complete {path.name}

## File Information
- **Path:** {file_path}
- **Type:** {file_type.title()}
- **Status:** Template created, needs content
- **Created:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} by CTMM Build Manager

## Description
This file was automatically created by the CTMM Build Manager because it was referenced in main.tex but missing.

## Tasks
- [ ] Add proper content for this {file_type}
- [ ] Review and test functionality  
- [ ] Update documentation if needed
- [ ] Remove this TODO file when complete

## Guidelines
{'- Follow CTMM style package conventions' if path.suffix == '.sty' else '- Use section/subsection structure'}
{'- Use \\ProvidesPackage and proper LaTeX package format' if path.suffix == '.sty' else '- Include labels for cross-referencing'}
{'- Define colors and commands consistently with CTMM design' if path.suffix == '.sty' else '- Add interactive elements as appropriate'}

## Next Steps
1. Open {file_path} in your LaTeX editor
2. Replace TODO comments with actual content
3. Test the {'package' if path.suffix == '.sty' else 'module'} by building main.tex
4. Update this TODO file or delete it when complete

---
Generated by CTMM Build Manager v1.0
"""
            with open(todo_path, 'w', encoding='utf-8') as f:
                f.write(todo_content)
                
            logger.info(f"[INFO] Created TODO: {todo_path}")
    
    def test_latex_installation(self) -> bool:
        """Test if LaTeX is properly installed and accessible."""
        try:
            result = subprocess.run(
                ['pdflatex', '--version'],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                logger.info("[INFO] LaTeX installation found and working")
                return True
            else:
                logger.error("[ERROR] LaTeX installation found but not working properly")
                return False
        except FileNotFoundError:
            logger.error("[ERROR] LaTeX (pdflatex) not found in system PATH")
            logger.info("[INFO] Installation guide:")
            logger.info("[INFO]   Ubuntu/Debian: sudo apt-get install texlive-latex-extra texlive-fonts-recommended")
            logger.info("[INFO]   macOS: brew install --cask mactex")
            logger.info("[INFO]   Windows: Install MiKTeX or TeX Live")
            return False
        except Exception as e:
            logger.error(f"[ERROR] Error checking LaTeX installation: {e}")
            return False
    
    def test_basic_build(self) -> bool:
        """Test build with all input lines temporarily commented out."""
        logger.info("[INFO] Testing basic build with modules commented out...")
        
        if not self.test_latex_installation():
            return False
        
        content = self._read_file_safely(self.main_tex_path)
            
        # Comment out all input{modules/...} lines
        modified_content = re.sub(
            r'(\\input\{modules/[^}]+\})',
            r'% \1  % Temporarily commented by build manager',
            content
        )
        
        temp_file = self.main_tex_path.with_suffix('.basic_test.tex')
        try:
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(modified_content)
                
            # Test build
            result = subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', temp_file.name],
                capture_output=True,
                text=True,
                cwd=str(self.main_tex_path.parent),
                timeout=120
            )
            
            success = result.returncode == 0
            if success:
                logger.info("[INFO] Basic build (without modules) successful")
                self.basic_build_successful = True
            else:
                logger.error("[ERROR] Basic build failed even without modules")
                logger.error(f"[ERROR] LaTeX error output: {result.stderr}")
                # Save error log for debugging
                error_log = "basic_build_error.log"
                with open(error_log, 'w') as f:
                    f.write("Basic build error details\n")
                    f.write("=========================\n\n")
                    f.write(f"Command: pdflatex -interaction=nonstopmode {temp_file.name}\n")
                    f.write(f"Return code: {result.returncode}\n\n")
                    f.write("STDOUT:\n")
                    f.write(result.stdout)
                    f.write("\n\nSTDERR:\n")
                    f.write(result.stderr)
                logger.info(f"[INFO] Error details saved to {error_log}")
                
            return success
            
        except subprocess.TimeoutExpired:
            logger.error("[ERROR] Basic build timed out after 120 seconds")
            return False
        except Exception as e:
            logger.error(f"[ERROR] Basic build test failed: {e}")
            return False
        finally:
            # Clean up temporary files
            self._cleanup_build_files(temp_file)
    
    def test_incremental_modules(self) -> None:
        """Gradually reactivate input lines to identify problematic modules."""
        if not self.module_files or not self.basic_build_successful:
            if not self.basic_build_successful:
                logger.warning("[WARNING] Skipping incremental testing due to basic build failure")
            else:
                logger.info("[INFO] No modules to test incrementally")
            return
            
        logger.info("[INFO] Testing modules incrementally to isolate build errors...")
        
        original_content = self._read_file_safely(self.main_tex_path)
        module_list = sorted(list(self.module_files))
        
        for i, current_module in enumerate(module_list):
            module_name = Path(current_module).stem
            logger.info(f"[INFO] Testing module {i+1}/{len(module_list)}: {module_name}")
            
            # Create content with modules 0 to i enabled
            modified_content = original_content
            for j, module in enumerate(module_list):
                module_pattern = f"modules/{Path(module).stem}"
                
                if j > i:
                    # Comment out modules beyond current test point
                    modified_content = re.sub(
                        f'(\\\\input\\{{{re.escape(module_pattern)}\\}})',
                        r'% \1  % Disabled for incremental testing',
                        modified_content
                    )
            
            # Test build with current module set
            temp_file = self.main_tex_path.with_suffix(f'.test_module_{i:02d}.tex')
            try:
                with open(temp_file, 'w', encoding='utf-8') as f:
                    f.write(modified_content)
                    
                result = subprocess.run(
                    ['pdflatex', '-interaction=nonstopmode', temp_file.name],
                    capture_output=True,
                    text=True,
                    cwd=str(self.main_tex_path.parent),
                    timeout=180
                )
                
                if result.returncode == 0:
                    logger.info(f"[INFO] ✓ Build successful with {module_name}")
                else:
                    logger.error(f"[ERROR] ✗ Build failed when adding {module_name}")
                    self.problematic_modules.append(current_module)
                    
                    # Save detailed error information
                    error_log = f"module_error_{module_name}.log"
                    with open(error_log, 'w') as f:
                        f.write(f"Module build error: {module_name}\n")
                        f.write("=" * 50 + "\n\n")
                        f.write(f"Failed when testing: {current_module}\n")
                        f.write(f"Command: pdflatex -interaction=nonstopmode {temp_file.name}\n")
                        f.write(f"Return code: {result.returncode}\n\n")
                        f.write("STDOUT:\n")
                        f.write(result.stdout)
                        f.write("\n\nSTDERR:\n")
                        f.write(result.stderr)
                    
                    logger.info(f"[INFO] Error details saved to {error_log}")
                    
            except subprocess.TimeoutExpired:
                logger.error(f"[ERROR] Build timed out when testing {module_name}")
                self.problematic_modules.append(current_module)
            except Exception as e:
                logger.error(f"[ERROR] Error testing {module_name}: {e}")
                self.problematic_modules.append(current_module)
            finally:
                # Clean up temporary files
                self._cleanup_build_files(temp_file)
    
    def test_full_build(self) -> bool:
        """Test complete build with all modules enabled."""
        logger.info("[INFO] Testing full build with all modules...")
        
        if not self.test_latex_installation():
            return False
        
        try:
            result = subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', self.main_tex_path.name],
                capture_output=True,
                text=True,
                cwd=str(self.main_tex_path.parent),
                timeout=300
            )
            
            success = result.returncode == 0
            if success:
                logger.info("[INFO] ✓ Full build successful")
                if Path('main.pdf').exists():
                    logger.info("[INFO] ✓ PDF generated successfully")
                self.build_successful = True
            else:
                logger.error("[ERROR] ✗ Full build failed")
                # Save error details
                error_log = "full_build_error.log"
                with open(error_log, 'w') as f:
                    f.write("Full build error details\n")
                    f.write("========================\n\n")
                    f.write(f"Command: pdflatex -interaction=nonstopmode {self.main_tex_path.name}\n")
                    f.write(f"Return code: {result.returncode}\n\n")
                    f.write("STDOUT:\n")
                    f.write(result.stdout)
                    f.write("\n\nSTDERR:\n")
                    f.write(result.stderr)
                logger.info(f"[INFO] Error details saved to {error_log}")
                
            return success
            
        except subprocess.TimeoutExpired:
            logger.error("[ERROR] Full build timed out after 300 seconds")
            return False
        except Exception as e:
            logger.error(f"[ERROR] Full build test failed: {e}")
            return False
    
    def _cleanup_build_files(self, base_file: Path) -> None:
        """Clean up temporary build files."""
        for ext in ['.aux', '.log', '.out', '.toc', '.pdf', '.fls', '.fdb_latexmk']:
            aux_file = base_file.with_suffix(ext)
            if aux_file.exists():
                try:
                    aux_file.unlink()
                except Exception as e:
                    logger.debug(f"[DEBUG] Could not remove {aux_file}: {e}")
        
        # Remove the base file itself if it's a temporary file
        if base_file.exists() and any(pattern in base_file.name for pattern in ['.test_', '.basic_test']):
            try:
                base_file.unlink()
            except Exception as e:
                logger.debug(f"[DEBUG] Could not remove {base_file}: {e}")
    
    def generate_comprehensive_report(self) -> str:
        """Generate a comprehensive build report in markdown format."""
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        report = f"""# CTMM Build Manager Report

**Generated:** {timestamp}  
**Main File:** {self.main_tex_path}

## Summary
- **Style files found:** {len(self.style_files)}
- **Module files found:** {len(self.module_files)}  
- **Missing files:** {len(self.missing_files)}
- **Problematic modules:** {len(self.problematic_modules)}
- **Basic build:** {'✓ PASS' if self.basic_build_successful else '✗ FAIL'}
- **Full build:** {'✓ PASS' if self.build_successful else '✗ FAIL'}

## Style Files
"""
        if self.style_files:
            for style_file in sorted(self.style_files):
                status = "✓ EXISTS" if Path(style_file).exists() else "✗ MISSING"
                report += f"- `{style_file}` - {status}\n"
        else:
            report += "- None found\n"

        report += f"""
## Module Files
"""
        if self.module_files:
            for module_file in sorted(self.module_files):
                status = "✓ EXISTS" if Path(module_file).exists() else "✗ MISSING"
                if module_file in self.problematic_modules:
                    status += " ⚠️ PROBLEMATIC"
                report += f"- `{module_file}` - {status}\n"
        else:
            report += "- None found\n"

        if self.missing_files:
            report += f"""
## Missing Files (Templates Created)
"""
            for missing_file in self.missing_files:
                report += f"- `{missing_file}` - Template and TODO file created\n"

        if self.problematic_modules:
            report += f"""
## Problematic Modules
"""
            for problematic_module in self.problematic_modules:
                module_name = Path(problematic_module).stem
                report += f"- `{problematic_module}` - Check `module_error_{module_name}.log` for details\n"

        report += f"""
## Recommendations

"""
        if not self.missing_files and not self.problematic_modules and self.build_successful:
            report += "✅ **All systems operational!** No action needed.\n"
        else:
            if not self.basic_build_successful:
                report += "🚨 **Critical:** Fix basic build issues first before addressing modules.\n"
            if self.missing_files:
                report += f"📝 **Templates:** Review and complete {len(self.missing_files)} template file(s).\n"
            if self.problematic_modules:
                report += f"🔧 **Modules:** Fix {len(self.problematic_modules)} problematic module(s).\n"
            if not self.build_successful and self.basic_build_successful:
                report += "🎯 **Focus:** Use incremental testing results to identify specific issues.\n"

        report += f"""
## Build System Usage

### Quick Commands
```bash
# Run comprehensive analysis
python3 build_manager.py
make analyze

# Standard builds  
make build        # Build main.tex
make build-ci     # Build main_final.tex for CI

# Cleanup
make clean        # Remove build artifacts
make clean-all    # Remove all generated files
```

### Next Steps
1. Review TODO files for missing templates
2. Fix any problematic modules identified
3. Test builds incrementally as you make changes
4. Remove TODO files when content is complete

---
*Generated by CTMM Build Manager v1.0*
"""
        return report
    
    def run_complete_analysis(self) -> bool:
        """Run the complete automated build management analysis."""
        logger.info("[INFO] Starting CTMM Build Manager comprehensive analysis...")
        
        try:
            # Core analysis steps
            self.scan_main_tex()
            self.check_file_existence()
            self.create_template_files()
            
            # Build testing
            basic_success = self.test_basic_build()
            if basic_success:
                self.test_incremental_modules()
            
            full_success = self.test_full_build()
            
            # Generate and save comprehensive report
            report = self.generate_comprehensive_report()
            with open('build_report.md', 'w', encoding='utf-8') as f:
                f.write(report)
            
            logger.info("[INFO] Build analysis complete. Report saved to build_report.md")
            
            # Print summary to console
            print("\n" + "="*60)
            print("CTMM BUILD MANAGER SUMMARY")
            print("="*60)
            print(f"Style files: {len(self.style_files)}")
            print(f"Module files: {len(self.module_files)}")
            print(f"Missing files: {len(self.missing_files)} (templates created)")
            print(f"Problematic modules: {len(self.problematic_modules)}")
            print(f"Basic build: {'✓ PASS' if basic_success else '✗ FAIL'}")
            print(f"Full build: {'✓ PASS' if full_success else '✗ FAIL'}")
            
            if self.missing_files or self.problematic_modules:
                print("\nNEXT STEPS:")
                if self.missing_files:
                    print("- Review and complete the created template files")
                    print("- Remove TODO_*.md files when content is complete")
                if self.problematic_modules:
                    print("- Fix problematic modules (check error logs)")
                    print("- Use incremental testing to isolate issues")
            else:
                print("\n🎉 All systems operational!")
            
            return basic_success and len(self.problematic_modules) == 0
            
        except Exception as e:
            logger.error(f"[ERROR] Build analysis failed: {e}")
            return False


def main():
    """Main entry point for CTMM Build Manager."""
    parser = argparse.ArgumentParser(
        description='CTMM Build Manager - Comprehensive Automated Build Management System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 build_manager.py                    # Run complete analysis
  python3 build_manager.py --main-tex doc.tex # Use different main file
  python3 build_manager.py --verbose          # Enable debug output
        """
    )
    parser.add_argument(
        '--main-tex', 
        default='main.tex', 
        help='Path to main TeX file (default: main.tex)'
    )
    parser.add_argument(
        '--verbose', '-v', 
        action='store_true',
        help='Enable verbose debug logging'
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("[DEBUG] Verbose logging enabled")
    
    build_manager = CTMMBuildManager(args.main_tex)
    success = build_manager.run_complete_analysis()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()