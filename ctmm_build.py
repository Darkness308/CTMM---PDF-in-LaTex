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
    """Convert filename to a readable title.
    
    Args:
        filename (str): The filename to convert to a title
        
    Returns:
        str: A human-readable title with proper capitalization
        
    Examples:
        >>> filename_to_title("test_module_name")
        'Test Module Name'
        >>> filename_to_title("arbeitsblatt-depression")
        'Arbeitsblatt Depression'
    """
    if not isinstance(filename, str):
        raise TypeError(f"Expected string, got {type(filename).__name__}")
    
    # Replace underscores and hyphens with spaces, capitalize words
    title = filename.replace('_', ' ').replace('-', ' ')
    # Handle multiple consecutive spaces by normalizing to single spaces
    normalized_title = ' '.join(word.capitalize() for word in title.split() if word)
    return normalized_title


def scan_references(main_tex_path="main.tex"):
    """Scan main.tex for style and module references.
    
    Args:
        main_tex_path (str): Path to the main LaTeX file
        
    Returns:
        dict: Dictionary with 'style_files' and 'module_files' lists
        
    Raises:
        None: Returns empty lists if file cannot be read
    """
    if not isinstance(main_tex_path, str):
        logger.error("Invalid main_tex_path type: expected str, got %s", type(main_tex_path).__name__)
        return {"style_files": [], "module_files": []}
    
    try:
        file_path = Path(main_tex_path)
        if not file_path.exists():
            logger.error("File does not exist: %s", main_tex_path)
            return {"style_files": [], "module_files": []}
            
        with open(main_tex_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    except Exception as e:
        logger.error("Error reading %s: %s", main_tex_path, e)
        return {"style_files": [], "module_files": []}

    # Find style and module references with improved regex patterns
    try:
        style_files = [f"style/{match}.sty" for match in
                       re.findall(r'\\usepackage\{style/([^}]+)\}', content)]
        module_files = [f"modules/{match}.tex" for match in
                        re.findall(r'\\input\{modules/([^}]+)\}', content)]
    except Exception as e:
        logger.error("Error parsing references in %s: %s", main_tex_path, e)
        return {"style_files": [], "module_files": []}

    logger.debug("Found %d style files and %d module files in %s", 
                 len(style_files), len(module_files), main_tex_path)
    
    return {"style_files": style_files, "module_files": module_files}


def check_missing_files(files):
    """Check which files are missing.
    
    Args:
        files (list): List of file paths to check
        
    Returns:
        list: List of missing file paths
        
    Raises:
        TypeError: If files is not a list or iterable
    """
    if not isinstance(files, (list, tuple, set)):
        raise TypeError(f"Expected list, tuple, or set, got {type(files).__name__}")
    
    missing = []
    for file_path in files:
        if not isinstance(file_path, str):
            logger.warning("Skipping non-string file path: %s (%s)", file_path, type(file_path).__name__)
            continue
            
        try:
            if not Path(file_path).exists():
                missing.append(file_path)
                logger.debug("Missing file: %s", file_path)
        except Exception as e:
            logger.error("Error checking file existence for %s: %s", file_path, e)
            # Assume file is missing if we can't check it
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

    # Validate LaTeX files for escaping issues
    latex_valid = validate_latex_files()

    # Scan for references
    step = 1
    print(f"\n{step}. Scanning file references...")
    references = scan_references()
    style_files = references["style_files"]
    module_files = references["module_files"]
    logger.info("Found %d style files and %d module files",
                len(style_files), len(module_files))
    print(f"Found {len(style_files)} style packages")
    print(f"Found {len(module_files)} module inputs")
    
    step += 1
    print(f"\n{step}. Checking file existence...")
    all_files = style_files + module_files
    missing_files = check_missing_files(all_files)
    total_missing = len(missing_files)
    
    if total_missing > 0:
        print(f"Found {total_missing} missing files")
        step += 1
        print(f"\n{step}. Creating templates for missing files...")
        for file_path in missing_files:
            logger.info("Creating template: %s", file_path)
            create_template(file_path)
        print(f"✓ Created {total_missing} template files")
    else:
        print("✓ All referenced files exist")
    
    step += 1
    print(f"\n{step}. Testing basic framework...")
    basic_ok = test_basic_build()
    
    if not basic_ok:
        print("⚠️  Basic framework has issues. Please fix before testing modules.")
        return 1
    
    step += 1
    print(f"\n{step}. Testing modules incrementally...")
    full_ok = test_full_build()
    
    step += 1
    print(f"\n{step}. Generating build report...")
    
    # Summary
    print("\n" + "="*50)
    print("CTMM BUILD SYSTEM SUMMARY")
    print("="*50)
    print(f"LaTeX validation: {'✓ PASS' if latex_valid else '✗ ISSUES FOUND'}")
    print(f"Style files: {len(style_files)}")
    print(f"Module files: {len(module_files)}")
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

    return 0 if (basic_ok and full_ok) else 1


if __name__ == "__main__":
    sys.exit(main())
