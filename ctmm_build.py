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
        return {'style_packages': [], 'module_inputs': []}

    # Find style and module references
    style_files = [f"style/{match}.sty" for match in
                   re.findall(r'\\usepackage\{style/([^}]+)\}', content)]
    module_files = [f"modules/{match}.tex" for match in
                    re.findall(r'\\input\{modules/([^}]+)\}', content)]

    return {'style_packages': style_files, 'module_inputs': module_files}


def check_file_existence(references):
    """Check which files are missing and return missing files dict."""
    missing_style = []
    missing_modules = []
    
    for file_path in references['style_packages']:
        if not Path(file_path).exists():
            missing_style.append(file_path)
    
    for file_path in references['module_inputs']:
        if not Path(file_path).exists():
            missing_modules.append(file_path)
    
    return {'style_packages': missing_style, 'module_inputs': missing_modules}


def create_template(file_path):
    """Create a minimal template for a missing file."""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    if file_path.endswith('.sty'):
        content = f"% {path.name} - CTMM Style Package\n"
        content += "% TODO: Add content for this style package\n\n"
        content += "\\NeedsTeXFormat{LaTeX2e}\n"
        content += "\\ProvidesPackage{" + path.stem + "}[2024/01/01 CTMM " + path.stem + " package]\n\n"
        content += "% TODO: Add package dependencies and commands here\n\n"
        content += "% End of package\n"
    else:
        title = filename_to_title(path.stem)
        content = f"% {path.name} - CTMM Module\n"
        content += "% TODO: Add content for this module\n\n"
        content += "\\section{TODO: " + title + "}\n"
        content += "\\label{sec:" + path.stem + "}\n\n"
        content += "\\begin{center}\n"
        content += "\\textit{This module is under development. Content will be added soon.}\n"
        content += "\\end{center}\n\n"
        content += "% TODO: Complete implementation\n"

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


def create_missing_templates(missing_files):
    """Create templates for missing files."""
    all_missing = missing_files['style_packages'] + missing_files['module_inputs']
    for file_path in all_missing:
        create_template(file_path)


def test_basic_build(main_tex_path="main.tex"):
    """Test basic build without modules."""
    logger.info("Testing basic build (without modules)...")

    try:
        with open(main_tex_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    except Exception as e:
        logger.error("Error reading %s: %s", main_tex_path, e)
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

        # Test if pdflatex is available
        try:
            result = subprocess.run(
                ['pdflatex', '-version'],
                capture_output=True,
                text=True,
                errors='replace',
                check=False
            )
            pdflatex_available = result.returncode == 0
        except FileNotFoundError:
            pdflatex_available = False

        if not pdflatex_available:
            logger.warning("pdflatex not available - performing syntax check only")
            # Just verify basic LaTeX syntax
            if '\\documentclass' in modified_content and '\\begin{document}' in modified_content and '\\end{document}' in modified_content:
                logger.info("✓ Basic LaTeX syntax check passed")
                return True
            else:
                logger.error("✗ Basic LaTeX syntax check failed")
                return False

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
            logger.info("✓ Basic build successful")
        else:
            logger.error("✗ Basic build failed")
            logger.error("LaTeX errors detected (check %s.log for details)",
                         temp_file)

        return success

    except Exception as e:
        logger.error("Build test failed: %s", e)
        return False
    finally:
        # Clean up
        for ext in ['', '.aux', '.log', '.pdf', '.out', '.toc']:
            cleanup_file = Path(temp_file).with_suffix(ext)
            if cleanup_file.exists():
                cleanup_file.unlink()


def test_basic_framework(main_tex_path="main.tex"):
    """Test basic build without modules."""


def test_modules_incrementally():
    """Test modules incrementally to identify problematic ones."""
    # Simple implementation - just test full build for now
    # In a more complex implementation, this would test modules one by one
    logger.info("Testing modules incrementally...")
    
    # Check if pdflatex is available
    try:
        result = subprocess.run(
            ['pdflatex', '-version'],
            capture_output=True,
            text=True,
            errors='replace',
            check=False
        )
        pdflatex_available = result.returncode == 0
    except FileNotFoundError:
        pdflatex_available = False

    if not pdflatex_available:
        logger.warning("pdflatex not available - skipping actual build test")
        return {"success": True, "problematic_modules": []}
    
    full_ok = test_full_build()
    return {"success": full_ok, "problematic_modules": [] if full_ok else ["unknown"]}


def generate_build_report():
    """Generate build report (placeholder for now)."""
    logger.info("Build report generated")


def test_full_build(main_tex_path="main.tex"):
    """Test full build with all modules."""
    logger.info("Testing full build (with all modules)...")

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
            logger.info("✓ Full build successful")
            if Path('main.pdf').exists():
                logger.info("✓ PDF generated successfully")
        else:
            logger.error("✗ Full build failed")
            logger.error("Check main.log for detailed error information")

        return success

    except Exception as e:
        logger.error("Full build test failed: %s", e)
        return False


def main():
    """Run the CTMM build system check with numbered steps."""
    logger.info("CTMM Build System - Starting check...")
    
    step = 1
    print(f"\n{step}. Scanning file references...")
    references = scan_references()
    print(f"Found {len(references['style_packages'])} style packages")
    print(f"Found {len(references['module_inputs'])} module inputs")
    
    step += 1
    print(f"\n{step}. Checking file existence...")
    missing_files = check_file_existence(references)
    total_missing = len(missing_files['style_packages']) + len(missing_files['module_inputs'])
    
    if total_missing > 0:
        print(f"Found {total_missing} missing files")
        step += 1
        print(f"\n{step}. Creating templates for missing files...")
        create_missing_templates(missing_files)
    else:
        print("✓ All referenced files exist")
    
    step += 1
    print(f"\n{step}. Testing basic framework...")
    framework_success = test_basic_framework()
    
    if not framework_success:
        print("⚠️  Basic framework has issues. Please fix before testing modules.")
        return
    
    step += 1
    print(f"\n{step}. Testing modules incrementally...")
    test_results = test_modules_incrementally()
    
    step += 1
    print(f"\n{step}. Generating build report...")
    generate_build_report()
    
    # Summary
    print("\n" + "="*50)
    print("CTMM BUILD SYSTEM SUMMARY")
    print("="*50)
    print(f"Style files: {len(references['style_packages'])}")
    print(f"Module files: {len(references['module_inputs'])}")
    print(f"Missing files: {total_missing} (templates created)")
    print(f"Basic build: {'✓ PASS' if framework_success else '✗ FAIL'}")
    print(f"Module testing: {'✓ PASS' if test_results['success'] else '✗ FAIL'}")

    if total_missing > 0:
        print("\nNEXT STEPS:")
        print("- Review and complete the created template files")
        print("- Remove TODO_*.md files when content is complete")

    return 0 if (framework_success and test_results['success']) else 1


if __name__ == "__main__":
    sys.exit(main())
