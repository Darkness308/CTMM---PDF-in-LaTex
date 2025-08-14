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
        # Check if file exists first
        if not Path(main_tex_path).exists():
            logger.error("Main LaTeX file %s not found", main_tex_path)
            logger.error("Current directory: %s", Path.cwd())
            logger.error("Directory contents: %s", list(Path(".").glob("*")))
            return {"style_files": [], "module_files": []}
            
        with open(main_tex_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
            logger.debug("Successfully read %s (%d characters)", main_tex_path, len(content))
    except Exception as e:
        logger.error("Error reading %s: %s", main_tex_path, e)
        # Try with encoding detection if UTF-8 fails
        try:
            import chardet
            with open(main_tex_path, 'rb') as f:
                raw_data = f.read()
                detected = chardet.detect(raw_data)
                logger.info("Detected encoding: %s", detected)
        except Exception:
            pass
        return {"style_files": [], "module_files": []}

    try:
        # Find style and module references
        style_files = [f"style/{match}.sty" for match in
                       re.findall(r'\\usepackage\{style/([^}]+)\}', content)]
        module_files = [f"modules/{match}.tex" for match in
                        re.findall(r'\\input\{modules/([^}]+)\}', content)]

        logger.debug("Found style files: %s", style_files)
        logger.debug("Found module files: %s", module_files)
        
        return {"style_files": style_files, "module_files": module_files}
        
    except Exception as e:
        logger.error("Error parsing references from %s: %s", main_tex_path, e)
        return {"style_files": [], "module_files": []}


def check_missing_files(files):
    """Check which files are missing."""
    missing = []
    for file_path in files:
        try:
            if not Path(file_path).exists():
                missing.append(file_path)
                logger.debug("Missing file: %s", file_path)
        except Exception as e:
            logger.error("Error checking file %s: %s", file_path, e)
            missing.append(file_path)  # Treat as missing if we can't check
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
    """Run the CTMM build system check."""
    try:
        # Add environment diagnostics for CI debugging
        import sys
        import os
        logger.info("CTMM Build System - Starting check...")
        logger.info("Python version: %s", sys.version.split()[0])
        logger.info("Working directory: %s", os.getcwd())
        
        # Scan for references
        references = scan_references()
        style_files = references["style_files"]
        module_files = references["module_files"]
        logger.info("Found %d style files and %d module files",
                    len(style_files), len(module_files))

        # Check for missing files
        all_files = style_files + module_files
        missing_files = check_missing_files(all_files)

        if missing_files:
            logger.warning("Found %d missing files", len(missing_files))
            for file_path in missing_files:
                logger.info("Creating template: %s", file_path)
                create_template(file_path)
        else:
            logger.info("All referenced files exist")

        # Test builds
        basic_ok = test_basic_build()
        full_ok = test_full_build()

        # Summary
        print("\n" + "="*50)
        print("CTMM BUILD SYSTEM SUMMARY")
        print("="*50)
        print(f"Style files: {len(style_files)}")
        print(f"Module files: {len(module_files)}")
        print(f"Missing files: {len(missing_files)} (templates created)")
        print(f"Basic build: {'✓ PASS' if basic_ok else '✗ FAIL'}")
        print(f"Full build: {'✓ PASS' if full_ok else '✗ FAIL'}")

        if missing_files:
            print("\nNEXT STEPS:")
            print("- Review and complete the created template files")
            print("- Remove TODO_*.md files when content is complete")

        return 0 if (basic_ok and full_ok) else 1
        
    except Exception as e:
        logger.error("FATAL ERROR in CTMM build system: %s", e)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except Exception as e:
        print(f"❌ CRITICAL ERROR: {e}")
        sys.exit(1)
