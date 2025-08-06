#!/usr/bin/env python3
"""
CTMM LaTeX Build Manager

Automated tool to manage LaTeX build process, detect missing files,
create templates, and test modules incrementally.

Author: CTMM Team
"""

import os
import re
import sys
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import List, Dict, Tuple, Optional

class CTMMBuildManager:
    def __init__(self, main_tex_file: str = "main.tex"):
        self.main_tex_file = main_tex_file
        self.project_root = Path.cwd()
        self.backup_suffix = ".backup"
        self.missing_files = []
        self.build_log = []
        
    def scan_references(self) -> Dict[str, List[str]]:
        """Scan main.tex for all \\usepackage{style/...} and \\input{modules/...} commands"""
        references = {
            'style_packages': [],
            'module_inputs': []
        }
        
        with open(self.main_tex_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find \\usepackage{style/...} commands
        style_pattern = r'\\usepackage\{style/([^}]+)\}'
        style_matches = re.findall(style_pattern, content)
        references['style_packages'] = [f"style/{match}.sty" for match in style_matches]
        
        # Find \\input{modules/...} commands
        input_pattern = r'\\input\{modules/([^}]+)\}'
        input_matches = re.findall(input_pattern, content)
        references['module_inputs'] = [f"modules/{match}.tex" for match in input_matches]
        
        return references
    
    def check_file_existence(self, references: Dict[str, List[str]]) -> Dict[str, List[str]]:
        """Check which referenced files exist and which are missing"""
        missing = {
            'style_packages': [],
            'module_inputs': []
        }
        
        for category, files in references.items():
            for file_path in files:
                if not os.path.exists(file_path):
                    missing[category].append(file_path)
                    self.missing_files.append(file_path)
        
        return missing
    
    def create_style_template(self, file_path: str) -> None:
        """Create a minimal style package template"""
        package_name = Path(file_path).stem
        
        template = f"""% Generated template for {package_name}.sty
% TODO: Add actual package content
% Issue: Content needs to be added for {package_name}

\\NeedsTeXFormat{{LaTeX2e}}
\\ProvidesPackage{{{package_name}}}[\\today\\space CTMM Style Package - Template]

% TODO: Add package requirements
% \\RequirePackage{{...}}

% TODO: Add package options
% \\DeclareOption{{...}}{{...}}
% \\ProcessOptions\\relax

% TODO: Add package definitions
% Example:
% \\newcommand{{\\placeholder}}{{\\textcolor{{red}}{{[{package_name.upper()} CONTENT NEEDED]}}}}

% TODO: Remove this placeholder when actual content is added
\\newcommand{{\\{package_name}Placeholder}}{{\\textcolor{{red}}{{[{package_name.upper()} TEMPLATE - NEEDS CONTENT]}}}}

\\endinput
"""
        
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(template)
        print(f"Created style template: {file_path}")
    
    def create_module_template(self, file_path: str) -> None:
        """Create a minimal module template with section"""
        module_name = Path(file_path).stem.replace('-', ' ').title()
        section_label = Path(file_path).stem.lower()
        
        template = f"""% Generated template for {Path(file_path).name}
% TODO: Add actual module content
% Issue: Content needs to be added for {module_name}

\\section{{{module_name}}}
\\label{{sec:{section_label}}}

% TODO: Add actual module content here
\\begin{{center}}
\\textcolor{{red}}{{\\textbf{{[{module_name.upper()} - CONTENT NEEDED]}}}}
\\end{{center}}

\\vspace{{1cm}}

% TODO: Replace this placeholder with actual content:
% - Add relevant text and explanations
% - Include forms, exercises, or worksheets as needed
% - Add proper cross-references to other sections
% - Include any necessary graphics or diagrams

\\textcolor{{gray}}{{
\\textit{{This is an automatically generated template for the {module_name} module. 
Please replace this content with the actual module materials.}}
}}

% TODO: Remove this placeholder when actual content is added
"""
        
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(template)
        print(f"Created module template: {file_path}")
    
    def create_missing_templates(self, missing_files: Dict[str, List[str]]) -> None:
        """Create templates for all missing files"""
        for style_file in missing_files['style_packages']:
            self.create_style_template(style_file)
        
        for module_file in missing_files['module_inputs']:
            self.create_module_template(module_file)
    
    def backup_main_tex(self) -> str:
        """Create a backup of main.tex"""
        backup_file = f"{self.main_tex_file}{self.backup_suffix}"
        shutil.copy2(self.main_tex_file, backup_file)
        return backup_file
    
    def restore_main_tex(self, backup_file: str) -> None:
        """Restore main.tex from backup"""
        if os.path.exists(backup_file):
            shutil.copy2(backup_file, self.main_tex_file)
            os.remove(backup_file)
    
    def comment_out_inputs(self, module_files: List[str]) -> str:
        """Comment out specified \\input commands in main.tex"""
        backup_file = self.backup_main_tex()
        
        with open(self.main_tex_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        for module_file in module_files:
            module_name = Path(module_file).stem
            pattern = rf"\\input\{{modules/{module_name}\}}"
            replacement = rf"% COMMENTED FOR TESTING: \\input{{modules/{module_name}}}"
            content = re.sub(pattern, replacement, content)
        
        with open(self.main_tex_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return backup_file
    
    def uncomment_input(self, module_file: str) -> None:
        """Uncomment a specific \\input command"""
        module_name = Path(module_file).stem
        
        with open(self.main_tex_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        pattern = rf"% COMMENTED FOR TESTING: \\input\{{modules/{module_name}\}}"
        replacement = rf"\\input{{modules/{module_name}}}"
        content = re.sub(pattern, replacement, content)
        
        with open(self.main_tex_file, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def test_latex_build(self) -> Tuple[bool, str]:
        """Test LaTeX build and return success status and log"""
        try:
            result = subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', self.main_tex_file],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                timeout=60
            )
            
            success = result.returncode == 0
            log_output = result.stdout + result.stderr
            
            return success, log_output
        
        except subprocess.TimeoutExpired:
            return False, "Build timed out"
        except FileNotFoundError:
            return False, (
                "pdflatex not found - LaTeX is not installed.\n"
                "To install LaTeX, follow the instructions for your system:\n"
                "  - Ubuntu/Debian: sudo apt install texlive-latex-base\n"
                "  - macOS (with Homebrew): brew install mactex\n"
                "  - Windows: Download and install MiKTeX from https://miktex.org/download\n"
                "Ensure 'pdflatex' is in your PATH after installation."
            )
    def test_basic_framework(self) -> bool:
        """Test build with all modules commented out"""
        references = self.scan_references()
        module_files = references['module_inputs']
        
        print("\n=== Testing Basic Framework (no modules) ===")
        backup_file = self.comment_out_inputs(module_files)
        
        try:
            success, log = self.test_latex_build()
            if success:
                print("✓ Basic framework builds successfully")
                self.build_log.append("Basic framework: SUCCESS")
            else:
                print("✗ Basic framework build failed")
                print("Error log:")
                print(log[-500:])  # Show last 500 chars of log
                self.build_log.append("Basic framework: FAILED")
            
            return success
        
        finally:
            self.restore_main_tex(backup_file)
    
    def test_modules_incrementally(self) -> Dict[str, bool]:
        """Test modules one by one"""
        references = self.scan_references()
        module_files = references['module_inputs']
        results = {}
        
        print("\n=== Testing Modules Incrementally ===")
        
        # Start with all modules commented out
        backup_file = self.comment_out_inputs(module_files)
        
        try:
            for i, module_file in enumerate(module_files, 1):
                module_name = Path(module_file).stem
                print(f"\n[{i}/{len(module_files)}] Testing module: {module_name}")
                
                # Uncomment this module
                self.uncomment_input(module_file)
                
                # Test build
                success, log = self.test_latex_build()
                results[module_file] = success
                
                if success:
                    print(f"✓ {module_name} builds successfully")
                    self.build_log.append(f"{module_name}: SUCCESS")
                else:
                    print(f"✗ {module_name} caused build failure")
                    self.build_log.append(f"{module_name}: FAILED")
                    
                    # Show relevant error info
                    error_lines = [line for line in log.split('\n') 
                                 if 'error' in line.lower() or 'undefined' in line.lower()]
                    if error_lines:
                        print("Error details:")
                        for line in error_lines[:5]:  # Show first 5 error lines
                            print(f"  {line.strip()}")
        
        finally:
            self.restore_main_tex(backup_file)
        
        return results
    
    def generate_build_report(self, test_results: Dict[str, bool]) -> None:
        """Generate a comprehensive build report"""
        report_file = "build_report.md"
        
        total_modules = len(test_results)
        successful_modules = sum(test_results.values())
        failed_modules = total_modules - successful_modules
        
        report = f"""# CTMM LaTeX Build Report

Generated on: {datetime.datetime.now().strftime('%a %b %d %H:%M:%S %Y')}

## Summary
- **Total modules tested**: {total_modules}
- **Successful builds**: {successful_modules}
- **Failed builds**: {failed_modules}
- **Success rate**: {(successful_modules/total_modules*100):.1f}%

## Module Test Results

### ✅ Successful Modules
"""
        
        for module_file, success in test_results.items():
            module_name = Path(module_file).stem
            if success:
                report += f"- `{module_name}` - Builds without errors\n"
        
        report += "\n### ❌ Failed Modules\n"
        
        for module_file, success in test_results.items():
            module_name = Path(module_file).stem
            if not success:
                report += f"- `{module_name}` - **NEEDS ATTENTION**\n"
        
        report += f"""
## Missing Files Created
{len(self.missing_files)} missing files were found and templates were created:
"""
        
        for missing_file in self.missing_files:
            report += f"- `{missing_file}` - Template created with TODO comments\n"
        
        report += """
## Next Steps
1. Review failed modules and fix LaTeX errors
2. Complete template content for missing files  
3. Add proper section labels for cross-references
4. Test full build again

## Build Log
```
"""
        report += "\n".join(self.build_log)
        report += "\n```\n"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\n[REPORT] Build report generated: {report_file}")
    
    def run_complete_analysis(self) -> None:
        """Run the complete build analysis process"""
        print("[INFO] CTMM LaTeX Build Manager")
        print("=" * 50)
        
        # Step 1: Scan references
        print("\n1. Scanning file references...")
        references = self.scan_references()
        print(f"Found {len(references['style_packages'])} style packages")
        print(f"Found {len(references['module_inputs'])} module inputs")
        
        # Step 2: Check file existence
        print("\n2. Checking file existence...")
        missing_files = self.check_file_existence(references)
        total_missing = len(missing_files['style_packages']) + len(missing_files['module_inputs'])
        
        if total_missing > 0:
            print(f"Found {total_missing} missing files")
            print("\n3. Creating templates for missing files...")
            self.create_missing_templates(missing_files)
        else:
            print("✓ All referenced files exist")
        
        # Step 3: Test basic framework
        print("\n4. Testing basic framework...")
        framework_success = self.test_basic_framework()
        
        if not framework_success:
            print("⚠️  Basic framework has issues. Please fix before testing modules.")
            return
        
        # Step 4: Test modules incrementally
        print("\n5. Testing modules incrementally...")
        test_results = self.test_modules_incrementally()
        
        # Step 5: Generate report
        print("\n6. Generating build report...")
        self.generate_build_report(test_results)
        
        print("\n✅ Build analysis complete!")
        print("Check build_report.md for detailed results.")

def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        main_tex_file = sys.argv[1]
    else:
        main_tex_file = "main.tex"
    
    if not os.path.exists(main_tex_file):
        print(f"Error: {main_tex_file} not found")
        sys.exit(1)
    
    manager = CTMMBuildManager(main_tex_file)
    manager.run_complete_analysis()

if __name__ == "__main__":
    main()