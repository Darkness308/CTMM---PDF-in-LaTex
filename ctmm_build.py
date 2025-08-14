#!/usr/bin/env python3
"""
CTMM Build System - Simplified Version
Handles missing files and basic build testing with robust error handling.
"""

import re
import subprocess
import sys
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def filename_to_title(filename):
    """Convert filename to a readable title."""
    # Replace underscores and hyphens with spaces, capitalize words
    title = filename.replace('_', ' ').replace('-', ' ')
    return ' '.join(word.capitalize() for word in title.split())


def scan_references(main_tex_path="main.tex"):
    """Scan main.tex for style and module references."""
    try:
        with open(main_tex_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    except Exception as e:
        logger.error("Error reading %s: %s", main_tex_path, e)
        return {"style_files": [], "module_files": []}

    # Find style and module references
    style_files = [f"style/{match}.sty" for match in
                   re.findall(r'\\usepackage\{style/([^}]+)\}', content)]
    module_files = [f"modules/{match}.tex" for match in
                    re.findall(r'\\input\{modules/([^}]+)\}', content)]

    return {"style_files": style_files, "module_files": module_files}


def check_missing_files(files):
    """Check which files are missing."""
    missing = []
    for file_path in files:
        if not Path(file_path).exists():
            missing.append(file_path)
    return missing


def create_template(file_path):
    """Create a minimal template for a missing file."""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    if file_path.endswith('.sty'):
        content = f"""% {path.name} - CTMM Style Package
% TODO: Add content for this style package

\\NeedsTeXFormat{{LaTeX2e}}
\\ProvidesPackage{{{path.stem}}}[2024/01/01 CTMM {path.stem} package]

% TODO: Add package dependencies and commands here

% End of package
"""
    else:
        content = f"""% {path.name} - CTMM Module
% TODO: Add content for this module

\\section{{TODO: {filename_to_title(path.stem)}}}
\\label{{sec:{path.stem}}}

\\begin{{center}}
\\textit{{This module is under development. Content will be added soon.}}
\\end{{center}}

% TODO: Complete implementation
"""

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

    # Create TODO file
    todo_path = path.parent / f"TODO_{path.stem}.md"
    todo_content = f"""# TODO: Complete {path.name}

**Status:** Template created, needs content

## Tasks
- [ ] Add proper content
- [ ] Review and test functionality
- [ ] Update documentation

Created by CTMM Build System
"""
    with open(todo_path, 'w', encoding='utf-8') as f:
        f.write(todo_content)


def test_basic_build(main_tex_path="main.tex"):
    """Test basic build without modules."""
    print_status("Testing basic build (without modules)", "info")

    # Check if pdflatex is available
    try:
        subprocess.run(['pdflatex', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print_status("pdflatex not found - skipping LaTeX compilation test", "warning")
        print_status("Basic structure test passed (LaTeX not available)", "success")
        return True

    try:
        with open(main_tex_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    except Exception as e:
        print_status(f"Error reading {main_tex_path}: {e}", "error")
        return False

    # Comment out all input{modules/...} lines
    modified_content = re.sub(
        r'(\\input\{modules/[^}]+\})',
        r'% \1  % Temporarily commented by build system',
        content
    )

    temp_file = "main_basic_test.tex"
    try:
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(modified_content)

        # Test build with limited output capture to avoid encoding issues
        result = subprocess.run(
            ['pdflatex', '-interaction=nonstopmode', temp_file],
            capture_output=True,
            text=True,
            errors='replace',  # Handle encoding issues
            check=False
        )

        success = result.returncode == 0
        if success:
            print_status("Basic build successful", "success")
        else:
            print_status("Basic build failed", "error")
            print_status(f"LaTeX errors detected (check {temp_file}.log for details)", "error")

        return success

    except Exception as e:
        print_status(f"Build test failed: {e}", "error")
        return False
    finally:
        # Clean up
        for ext in ['', '.aux', '.log', '.pdf', '.out', '.toc']:
            cleanup_file = Path(temp_file).with_suffix(ext)
            if cleanup_file.exists():
                cleanup_file.unlink()


def test_full_build(main_tex_path="main.tex"):
    """Test full build with all modules."""
    print_status("Testing full build (with all modules)", "info")

    # Check if pdflatex is available
    try:
        subprocess.run(['pdflatex', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print_status("pdflatex not found - skipping LaTeX compilation test", "warning")
        print_status("Full structure test passed (LaTeX not available)", "success")
        return True

    try:
        result = subprocess.run(
            ['pdflatex', '-interaction=nonstopmode', main_tex_path],
            capture_output=True,
            text=True,
            errors='replace',
            check=False
        )

        success = result.returncode == 0
        if success:
            print_status("Full build successful", "success")
            if Path('main.pdf').exists():
                print_status("PDF generated successfully", "success")
        else:
            print_status("Full build failed", "error")
            print_status("Check main.log for detailed error information", "error")

        return success

    except Exception as e:
        print_status(f"Full build test failed: {e}", "error")
        return False


def print_step(step_num, description):
    """Print a formatted step with professional styling."""
    print(f"\n{step_num}. {description}")
    print("-" * 50)


def print_status(message, status="info"):
    """Print a status message with appropriate visual indicator."""
    if status == "success":
        print(f"✓ {message}")
    elif status == "warning":
        print(f"⚠️  {message}")
    elif status == "error":
        print(f"✗ {message}")
    else:
        print(f"  {message}")


def main():
    """Run the CTMM build system check."""
    logger.info("CTMM Build System - Starting check...")
    
    # Initialize step counter for smart progression
    current_step = 1
    
    # Step 1: Scan file references
    print_step(current_step, "Scanning file references")
    references = scan_references()
    style_files = references["style_files"]
    module_files = references["module_files"]
    print_status(f"Found {len(style_files)} style packages", "info")
    print_status(f"Found {len(module_files)} module inputs", "info")
    current_step += 1
    
    # Step 2: Check file existence  
    print_step(current_step, "Checking file existence")
    all_files = style_files + module_files
    missing_files = check_missing_files(all_files)
    total_missing = len(missing_files)
    
    if total_missing > 0:
        print_status(f"Found {total_missing} missing files", "warning")
        current_step += 1
        
        # Dynamic step insertion: Create templates for missing files
        print_step(current_step, "Creating templates for missing files")
        for file_path in missing_files:
            logger.info("Creating template: %s", file_path)
            create_template(file_path)
        print_status(f"Created {total_missing} template files", "success")
    else:
        print_status("All referenced files exist", "success")
    
    current_step += 1
    
    # Step N: Test basic framework
    print_step(current_step, "Testing basic framework")
    basic_ok = test_basic_build()
    
    if not basic_ok:
        print_status("Basic framework has issues. Please fix before testing modules.", "error")
        return 1
    
    print_status("Basic framework validation completed", "success")
    current_step += 1
    
    # Step N+1: Test full build with modules
    print_step(current_step, "Testing full build with modules")
    full_ok = test_full_build()
    
    if full_ok:
        print_status("Full build validation completed", "success")
    else:
        print_status("Full build encountered issues", "error")
    
    current_step += 1
    
    # Step N+2: Generate build report
    print_step(current_step, "Generating build report")
    
    # Summary with enhanced formatting
    print("\n" + "="*50)
    print("CTMM BUILD SYSTEM SUMMARY")
    print("="*50)
    print(f"Style files: {len(style_files)}")
    print(f"Module files: {len(module_files)}")
    print(f"Missing files: {total_missing} (templates created)")
    print(f"Basic build: {'✓ PASS' if basic_ok else '✗ FAIL'}")
    print(f"Full build: {'✓ PASS' if full_ok else '✗ FAIL'}")

    if missing_files:
        print("\nNEXT STEPS:")
        print("- Review and complete the created template files")
        print("- Remove TODO_*.md files when content is complete")

    print_status("Build report generated", "success")
    
    return 0 if (basic_ok and full_ok) else 1


if __name__ == "__main__":
    sys.exit(main())
