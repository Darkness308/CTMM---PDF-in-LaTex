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


def sanitize_latex_command_name(package_name):
    """
    Sanitize a package name for use in LaTeX command names.
    
    LaTeX command names must only contain letters (a-z, A-Z) and cannot start with numbers.
    This function converts special characters to valid alternatives while preserving readability.
    
    Args:
        package_name (str): The original package name (e.g., "ctmm-design", "form_elements")
    
    Returns:
        str: A sanitized name safe for use in LaTeX commands (e.g., "ctmmDashDesign", "formUnderscoreElements")
    
    Examples:
        >>> sanitize_latex_command_name("ctmm-design")
        'ctmmDashDesign'
        >>> sanitize_latex_command_name("form_elements")
        'formUnderscoreElements'
        >>> sanitize_latex_command_name("123test")
        'numTest'
    """
    if not package_name or not package_name.strip():
        return "placeholder"
    
    # Split the name into parts to preserve capitalization
    import re
    
    # Replace special characters with descriptive words, preserving word boundaries
    replacements = [
        ('-', 'Dash'),
        ('_', 'Underscore'),
        ('.', 'Dot'),
        ('+', 'Plus'),
        ('=', 'Equals'),
        ('@', 'At'),
        ('#', 'Hash'),
        ('$', 'Dollar'),
        ('%', 'Percent'),
        ('&', 'And'),
        ('*', 'Star'),
        ('!', 'Exclamation'),
        ('?', 'Question'),
    ]
    
    # Start with the original name
    result = package_name.strip()
    
    # Handle leading numbers BEFORE removing non-letters
    leading_nums_match = re.match(r'^(\d+)', result)
    if leading_nums_match:
        leading_nums = leading_nums_match.group(1)
        rest = result[len(leading_nums):]
        # Replace with 'num' and capitalize the rest
        result = 'num' + (rest[0].upper() + rest[1:] if rest else '')
    
    # Apply replacements in a way that preserves word boundaries
    for char, replacement in replacements:
        if char in result:
            # Split by the character and rejoin with replacement
            parts = result.split(char)
            # Capitalize the first letter of each part except the first
            processed_parts = []
            for i, part in enumerate(parts):
                if part:  # Only process non-empty parts
                    if i == 0:
                        processed_parts.append(part)
                    else:
                        # Add replacement and capitalize the part
                        processed_parts.append(replacement + (part[0].upper() + part[1:] if part else ''))
                elif i > 0:  # Empty part in the middle means consecutive special chars
                    processed_parts.append(replacement)
            result = ''.join(processed_parts)
    
    # Remove any remaining non-letter characters and whitespace
    result = re.sub(r'[^a-zA-Z]', '', result)
    
    # Ensure we have at least something
    if not result:
        result = 'placeholder'
    
    # Ensure first letter is lowercase for consistency with LaTeX naming conventions
    return result[0].lower() + result[1:] if len(result) > 1 else result.lower()


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
        # Sanitize package name for use in LaTeX commands
        sanitized_name = sanitize_latex_command_name(path.stem)
        
        content = f"""% {path.name} - CTMM Style Package
% TODO: Add content for this style package

\\NeedsTeXFormat{{LaTeX2e}}
\\ProvidesPackage{{{path.stem}}}[2024/01/01 CTMM {path.stem} package]

% TODO: Add package dependencies and commands here
% \\RequirePackage{{xcolor}}
% \\RequirePackage{{tikz}}

% TODO: Add color definitions here
% \\definecolor{{ctmmBlue}}{{RGB}}{{52, 152, 219}}

% TODO: Add commands and environments here
% Example placeholder command (using sanitized name for LaTeX compatibility)
\\newcommand{{\\{sanitized_name}Placeholder}}{{\\textcolor{{red}}{{[{path.stem.upper()} TEMPLATE - NEEDS CONTENT]}}}}

% TODO: Remove the placeholder command above when actual content is added
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
