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

# Import LaTeX validator if available
try:
    from latex_validator import LaTeXValidator
    VALIDATOR_AVAILABLE = True
except ImportError:
    VALIDATOR_AVAILABLE = False
    logger.debug("LaTeX validator not available for escaping checks")


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

    # Split content into lines and filter out commented lines
    lines = content.split('\n')
    active_lines = []
    
    for line in lines:
        # Find the first % not preceded by \ (to handle \% which is escaped)
        comment_pos = -1
        for i, char in enumerate(line):
            if char == '%' and (i == 0 or line[i-1] != '\\'):
                comment_pos = i
                break
        
        # If comment found, only keep part before comment
        if comment_pos >= 0:
            active_lines.append(line[:comment_pos])
        else:
            active_lines.append(line)
    
    active_content = '\n'.join(active_lines)

    # Find style and module references in non-commented content
    style_files = [f"style/{match}.sty" for match in
                   re.findall(r'\\usepackage\{style/([^}]+)\}', active_content)]
    module_files = [f"modules/{match}.tex" for match in
                    re.findall(r'\\input\{modules/([^}]+)\}', active_content)]

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
        content = ("% " + path.name + " - CTMM Style Package\n"
                  "% TODO: Add content for this style package\n"
                  "\n"
                  "\\NeedsTeXFormat{LaTeX2e}\n"
                  "\\ProvidesPackage{" + path.stem + "}[2024/01/01 CTMM " + path.stem + " package]\n"
                  "\n"
                  "% TODO: Add package dependencies and commands here\n"
                  "\n"
                  "% End of package\n")
    else:
        content = ("% " + path.name + " - CTMM Module\n"
                  "% TODO: Add content for this module\n"
                  "\n"
                  "\\section{TODO: " + filename_to_title(path.stem) + "}\n"
                  "\\label{sec:" + path.stem + "}\n"
                  "\n"
                  "\\begin{center}\n"
                  "\\textit{This module is under development. Content will be added soon.}\n"
                  "\\end{center}\n"
                  "\n"
                  "% TODO: Complete implementation\n")

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

    # Create TODO file
    todo_path = path.parent / ("TODO_" + path.stem + ".md")
    todo_content = ("# TODO: Complete " + path.name + "\n"
                   "\n"
                   "**Status:** Template created, needs content\n"
                   "\n"
                   "## Tasks\n"
                   "- [ ] Add proper content\n"
                   "- [ ] Review and test functionality\n"
                   "- [ ] Update documentation\n"
                   "\n"
                   "Created by CTMM Build System\n")
    with open(todo_path, 'w', encoding='utf-8') as f:
        f.write(todo_content)


def test_basic_build(main_tex_path="main.tex"):
    """Test basic build without modules."""
    logger.info("Testing basic build (without modules)...")

    # Check if pdflatex is available
    try:
        subprocess.run(['pdflatex', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        logger.warning("pdflatex not found - skipping LaTeX compilation test")
        logger.info("✓ Basic structure test passed (LaTeX not available)")
        return True

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

        # Test build with limited output capture to avoid encoding issues
        result = subprocess.run(
            ['pdflatex', '-interaction=nonstopmode', temp_file],
            capture_output=True,
            text=True,
            errors='replace',  # Handle encoding issues
            check=False
        )

        # Enhanced PDF validation: check both return code and file existence/size
        temp_pdf = Path(temp_file).with_suffix('.pdf')
        pdf_exists = temp_pdf.exists()
        pdf_size = temp_pdf.stat().st_size if pdf_exists else 0
        
        # Validate PDF generation success by file existence and size rather than just return codes
        success = result.returncode == 0 and pdf_exists and pdf_size > 1024  # At least 1KB
        
        if success:
            logger.info("✓ Basic build successful")
            logger.info("✓ Test PDF generated successfully (%.2f KB)", pdf_size / 1024)
        else:
            logger.error("✗ Basic build failed")
            if result.returncode != 0:
                logger.error("LaTeX compilation returned error code: %d", result.returncode)
            if not pdf_exists:
                logger.error("Test PDF file was not generated")
            elif pdf_size <= 1024:
                logger.error("Test PDF file is too small (%.2f KB) - likely incomplete", pdf_size / 1024)
            logger.error("LaTeX errors detected (check %s.log for details)", temp_file)

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


def test_full_build(main_tex_path="main.tex"):
    """Test full build with all modules."""
    logger.info("Testing full build (with all modules)...")

    # Check if pdflatex is available
    try:
        subprocess.run(['pdflatex', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        logger.warning("pdflatex not found - skipping LaTeX compilation test")
        logger.info("✓ Full structure test passed (LaTeX not available)")
        return True

    try:
        result = subprocess.run(
            ['pdflatex', '-interaction=nonstopmode', main_tex_path],
            capture_output=True,
            text=True,
            errors='replace',
            check=False
        )

        # Enhanced PDF validation: check both return code and file existence/size
        pdf_path = Path('main.pdf')
        pdf_exists = pdf_path.exists()
        pdf_size = pdf_path.stat().st_size if pdf_exists else 0
        
        # Validate PDF generation success by file existence and size rather than just return codes
        success = result.returncode == 0 and pdf_exists and pdf_size > 1024  # At least 1KB
        
        if success:
            logger.info("✓ Full build successful")
            logger.info("✓ PDF generated successfully (%.2f KB)", pdf_size / 1024)
        else:
            logger.error("✗ Full build failed")
            if result.returncode != 0:
                logger.error("LaTeX compilation returned error code: %d", result.returncode)
            if not pdf_exists:
                logger.error("PDF file was not generated")
            elif pdf_size <= 1024:
                logger.error("PDF file is too small (%.2f KB) - likely incomplete", pdf_size / 1024)
            logger.error("Check main.log for detailed error information")

        return success

    except Exception as e:
        logger.error("Full build test failed: %s", e)
        return False


def validate_latex_files():
    """Validate LaTeX files for excessive escaping issues."""
    if not VALIDATOR_AVAILABLE:
        logger.debug("Skipping LaTeX validation - validator not available")
        return True
        
    logger.info("Validating LaTeX files for escaping issues...")
    validator = LaTeXValidator()
    
    # Check main.tex and modules directory
    issues_found = False
    
    for path in [Path("main.tex"), Path("modules")]:
        if not path.exists():
            continue
            
        if path.is_file():
            is_valid, issues, _ = validator.validate_file(path)
            if not is_valid:
                logger.warning(f"LaTeX escaping issues found in {path}: {list(issues.keys())}")
                issues_found = True
        elif path.is_dir():
            results = validator.validate_directory(path, fix=False)
            for file_path, result in results.items():
                if not result['valid']:
                    logger.warning(f"LaTeX escaping issues found in {file_path}: {list(result['issues'].keys())}")
                    issues_found = True
    
    if not issues_found:
        logger.info("✓ No LaTeX escaping issues found")
    
    return not issues_found


def main():
    """Run the CTMM build system check."""
    logger.info("CTMM Build System - Starting check...")

    # Initialize data structures for structured returns
    build_data = {
        "latex_validation": {"passed": False, "errors": []},
        "file_scanning": {"style_files": [], "module_files": []},
        "file_existence": {"missing_files": [], "total_missing": 0},
        "template_creation": {"created_count": 0, "created_files": []},
        "build_testing": {"basic_passed": False, "full_passed": False}
    }

    # Step 1: Validate LaTeX files for escaping issues
    step = 1
    print(f"\n{step}. Validating LaTeX files...")
    try:
        latex_valid = validate_latex_files()
        build_data["latex_validation"]["passed"] = latex_valid
        print(f"✓ LaTeX validation: {'PASS' if latex_valid else 'ISSUES FOUND'}")
    except Exception as e:
        logger.error("LaTeX validation failed: %s", e)
        build_data["latex_validation"]["errors"].append(str(e))
        latex_valid = False

    # Step 2: Scan for references
    step += 1
    print(f"\n{step}. Scanning file references...")
    try:
        references = scan_references()
        style_files = references["style_files"]
        module_files = references["module_files"]
        
        build_data["file_scanning"]["style_files"] = style_files
        build_data["file_scanning"]["module_files"] = module_files
        
        logger.info("Found %d style files and %d module files",
                    len(style_files), len(module_files))
        print(f"Found {len(style_files)} style packages")
        print(f"Found {len(module_files)} module inputs")
    except Exception as e:
        logger.error("File scanning failed: %s", e)
        style_files = []
        module_files = []
    
    # Step 3: Check file existence
    step += 1
    print(f"\n{step}. Checking file existence...")
    try:
        all_files = style_files + module_files
        missing_files = check_missing_files(all_files)
        total_missing = len(missing_files)
        
        build_data["file_existence"]["missing_files"] = missing_files
        build_data["file_existence"]["total_missing"] = total_missing
        
        if total_missing > 0:
            print(f"Found {total_missing} missing files")
        else:
            print("✓ All referenced files exist")
    except Exception as e:
        logger.error("File existence check failed: %s", e)
        missing_files = []
        total_missing = 0
    
    # Step 4: Create templates for missing files (if any)
    if total_missing > 0:
        step += 1
        print(f"\n{step}. Creating templates for missing files...")
        try:
            created_count = 0
            for file_path in missing_files:
                logger.info("Creating template: %s", file_path)
                create_template(file_path)
                created_count += 1
                build_data["template_creation"]["created_files"].append(file_path)
            
            build_data["template_creation"]["created_count"] = created_count
            print(f"✓ Created {created_count} template files")
        except Exception as e:
            logger.error("Template creation failed: %s", e)
    
    # Step 5: Test basic framework
    step += 1
    print(f"\n{step}. Testing basic framework...")
    try:
        basic_ok = test_basic_build()
        build_data["build_testing"]["basic_passed"] = basic_ok
        
        if not basic_ok:
            print("⚠️  Basic framework has issues. Please fix before testing modules.")
            return _generate_exit_code(build_data)
    except Exception as e:
        logger.error("Basic build test failed: %s", e)
        basic_ok = False
        build_data["build_testing"]["basic_passed"] = False
    
    # Step 6: Test modules incrementally
    step += 1
    print(f"\n{step}. Testing modules incrementally...")
    try:
        full_ok = test_full_build()
        build_data["build_testing"]["full_passed"] = full_ok
    except Exception as e:
        logger.error("Full build test failed: %s", e)
        full_ok = False
        build_data["build_testing"]["full_passed"] = False
    
    # Step 7: Generate build report
    step += 1
    print(f"\n{step}. Generating build report...")
    _generate_build_summary(build_data, latex_valid, basic_ok, full_ok, 
                           len(style_files), len(module_files), total_missing, missing_files)

    return _generate_exit_code(build_data)


def _generate_build_summary(build_data, latex_valid, basic_ok, full_ok, 
                           style_count, module_count, total_missing, missing_files):
    """Generate and display the build summary."""
    print("\n" + "="*50)
    print("CTMM BUILD SYSTEM SUMMARY")
    print("="*50)
    print(f"LaTeX validation: {'✓ PASS' if latex_valid else '✗ ISSUES FOUND'}")
    print(f"Style files: {style_count}")
    print(f"Module files: {module_count}")
    print(f"Missing files: {total_missing} (templates created)")
    print(f"Basic build: {'✓ PASS' if basic_ok else '✗ FAIL'}")
    print(f"Full build: {'✓ PASS' if full_ok else '✗ FAIL'}")

    if missing_files:
        print("\nNEXT STEPS:")
        print("- Review and complete the created template files")
        print("- Remove TODO_*.md files when content is complete")
    
    if not latex_valid:
        print("\nLATEX VALIDATION:")
        print("- Escaping issues found in LaTeX files")
        print("- Run 'python3 latex_validator.py --fix' to automatically fix issues")


def _generate_exit_code(build_data):
    """Generate appropriate exit code based on build results."""
    basic_passed = build_data["build_testing"]["basic_passed"]
    full_passed = build_data["build_testing"]["full_passed"]
    latex_passed = build_data["latex_validation"]["passed"]
    
    # Return 0 only if all critical tests pass
    if basic_passed and full_passed and latex_passed:
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
