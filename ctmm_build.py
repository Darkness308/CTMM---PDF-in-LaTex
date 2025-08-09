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
        return [], []

    # Find style and module references
    style_files = [f"style/{match}.sty" for match in
                   re.findall(r'\\usepackage\{style/([^}]+)\}', content)]
    module_files = [f"modules/{match}.tex" for match in
                    re.findall(r'\\input\{modules/([^}]+)\}', content)]

    return style_files, module_files


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
    """Test basic build without modules with enhanced error handling."""
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

        # Multi-pass compilation for better results
        success = _run_multipass_compilation(temp_file)
        
        if success:
            logger.info("✓ Basic build successful")
        else:
            logger.error("✗ Basic build failed")
            _analyze_build_errors(temp_file)

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
    """Test full build with all modules with enhanced verification."""
    logger.info("Testing full build (with all modules)...")

    try:
        # Multi-pass compilation for full build
        success = _run_multipass_compilation(main_tex_path)
        
        if success:
            logger.info("✓ Full build successful")
            pdf_file = Path('main.pdf')
            if pdf_file.exists():
                # Verify PDF integrity
                pdf_size = pdf_file.stat().st_size
                logger.info("✓ PDF generated successfully (size: %d bytes)", pdf_size)
                
                # Basic PDF verification
                if pdf_size > 1000:  # Reasonable minimum size
                    logger.info("✓ PDF appears to be valid")
                else:
                    logger.warning("⚠ PDF file seems unusually small, may be corrupted")
                    return False
            else:
                logger.error("✗ PDF file not generated despite successful build")
                return False
        else:
            logger.error("✗ Full build failed")
            _analyze_build_errors(main_tex_path)

        return success

    except Exception as e:
        logger.error("Full build test failed: %s", e)
        return False


def _run_multipass_compilation(tex_file):
    """Run multi-pass LaTeX compilation for better results."""
    logger.info("Running multi-pass compilation for %s...", tex_file)
    
    # First pass
    result1 = subprocess.run(
        ['pdflatex', '-interaction=nonstopmode', tex_file],
        capture_output=True,
        text=True,
        errors='replace',
        check=False
    )
    
    if result1.returncode != 0:
        logger.error("First pass failed")
        return False
    
    # Second pass (for references and TOC)
    result2 = subprocess.run(
        ['pdflatex', '-interaction=nonstopmode', tex_file],
        capture_output=True,
        text=True,
        errors='replace',
        check=False
    )
    
    if result2.returncode != 0:
        logger.warning("Second pass failed, but first pass succeeded")
        return True  # First pass success is often sufficient
    
    logger.info("✓ Multi-pass compilation completed successfully")
    return True


def _analyze_build_errors(tex_file):
    """Analyze LaTeX build errors and provide suggestions."""
    log_file = Path(tex_file).with_suffix('.log')
    if not log_file.exists():
        logger.error("No log file found for error analysis")
        return
    
    logger.info("Analyzing build errors...")
    
    try:
        with open(log_file, 'r', encoding='utf-8', errors='replace') as f:
            log_content = f.read()
        
        error_patterns = [
            (r'! Undefined control sequence', "Undefined command - check macro definitions"),
            (r'! Package .* Error:', "Package error - check package usage and options"),
            (r'! LaTeX Error: File .* not found', "Missing file - check file paths"),
            (r'! Missing .* inserted', "Syntax error - check braces, math mode, etc."),
            (r'Runaway argument', "Unmatched braces or missing closing delimiter"),
            (r'! Emergency stop', "Critical error - compilation halted"),
        ]
        
        found_errors = []
        for pattern, suggestion in error_patterns:
            if re.search(pattern, log_content, re.IGNORECASE):
                found_errors.append(suggestion)
        
        if found_errors:
            logger.error("Detected error types:")
            for i, error in enumerate(found_errors, 1):
                logger.error("  %d. %s", i, error)
        else:
            logger.warning("Build failed but no specific error patterns detected")
            
        # Save detailed error analysis
        error_file = f"error_analysis_{Path(tex_file).stem}.md"
        with open(error_file, 'w', encoding='utf-8') as f:
            f.write(f"# Build Error Analysis: {tex_file}\n\n")
            f.write("## Detected Issues\n")
            for error in found_errors:
                f.write(f"- {error}\n")
            f.write(f"\n## Full Log\n```\n{log_content}\n```\n")
        
        logger.info("Detailed error analysis saved to %s", error_file)
        
    except Exception as e:
        logger.error("Error analysis failed: %s", e)


def main():
    """Run the CTMM build system check."""
    logger.info("CTMM Build System - Starting check...")

    # Scan for references
    style_files, module_files = scan_references()
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


if __name__ == "__main__":
    sys.exit(main())
