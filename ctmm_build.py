#!/usr/bin/env python3
"""
CTMM Build System - Simplified Version with Security Enhancements
Handles missing files and basic build testing with robust error handling.
Now includes package name sanitization to prevent invalid LaTeX command generation.
"""

import re
import subprocess
import sys
from pathlib import Path
import logging

# Import the sanitizer for secure command generation
try:
    from build_manager import PackageNameSanitizer
    SANITIZER_AVAILABLE = True
except ImportError:
    SANITIZER_AVAILABLE = False
    print("Warning: Enhanced security sanitizer not available. Using basic templates.")

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
    """Create a minimal template for a missing file with secure command generation."""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    if file_path.endswith('.sty'):
        package_name = path.stem
        
        # Use secure command generation if available
        if SANITIZER_AVAILABLE:
            sanitizer = PackageNameSanitizer()
            sanitized_name = sanitizer.sanitize_package_name(package_name)
            safe_command = sanitizer.generate_safe_command_name(package_name)
            
            # Validate the command
            if not sanitizer.validate_latex_command_name(safe_command):
                logger.warning(f"Generated command \\{safe_command} may be invalid, using fallback")
                safe_command = "safePlaceholder"
            
            security_note = f"""
% SECURITY: Package name sanitization applied
% Original name: {package_name} → Sanitized: {sanitized_name}
% Generated safe command: \\{safe_command}
\\newcommand{{\\{safe_command}}}{{\\textcolor{{red}}{{[{package_name.upper()} TEMPLATE - NEEDS CONTENT]}}}}
"""
        else:
            # Fallback to basic template without package-specific commands
            security_note = f"""
% TODO: Add package-specific commands here
% Note: Use only valid LaTeX command names (letters and numbers only)
"""

        content = f"""% {path.name} - CTMM Style Package
% TODO: Add content for this style package

\\NeedsTeXFormat{{LaTeX2e}}
\\ProvidesPackage{{{package_name}}}[2024/01/01 CTMM {package_name} package]
{security_note}
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

    # Create TODO file with security information
    todo_path = path.parent / f"TODO_{path.stem}.md"
    
    security_info = ""
    if SANITIZER_AVAILABLE and file_path.endswith('.sty'):
        sanitizer = PackageNameSanitizer()
        sanitized_name = sanitizer.sanitize_package_name(path.stem)
        security_info = f"""
## Security Features
- ✅ Package name sanitization applied: `{path.stem}` → `{sanitized_name}`
- ✅ Safe LaTeX command generation used
- ✅ Command name validation performed
"""
    
    todo_content = f"""# TODO: Complete {path.name}

**Status:** Template created with security enhancements, needs content
{security_info}
## Tasks
- [ ] Add proper content
- [ ] Review and test functionality
- [ ] Update documentation

Created by CTMM Build System with Security Enhancements
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
    """Run the CTMM build system check with security enhancements."""
    logger.info("CTMM Build System with Security Enhancements - Starting check...")
    
    if SANITIZER_AVAILABLE:
        logger.info("✅ Enhanced security sanitization is ACTIVE")
    else:
        logger.warning("⚠️ Enhanced security sanitization is NOT available")

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
            logger.info("Creating secure template: %s", file_path)
            create_template(file_path)
    else:
        logger.info("All referenced files exist")

    # Test builds
    basic_ok = test_basic_build()
    full_ok = test_full_build()

    # Security validation if available
    security_status = "N/A"
    if SANITIZER_AVAILABLE:
        try:
            sanitizer = PackageNameSanitizer()
            # Check existing style files for security
            security_issues = 0
            for style_file in style_files:
                package_name = Path(style_file).stem
                safe_command = sanitizer.generate_safe_command_name(package_name)
                if not sanitizer.validate_latex_command_name(safe_command):
                    security_issues += 1
            
            security_status = f"✅ SECURE ({security_issues} issues)" if security_issues == 0 else f"⚠️ {security_issues} ISSUES"
        except Exception as e:
            security_status = f"❌ ERROR: {e}"

    # Summary
    print("\n" + "="*50)
    print("CTMM BUILD SYSTEM SUMMARY")
    print("="*50)
    print(f"Style files: {len(style_files)}")
    print(f"Module files: {len(module_files)}")
    print(f"Missing files: {len(missing_files)} (secure templates created)")
    print(f"Basic build: {'✓ PASS' if basic_ok else '✗ FAIL'}")
    print(f"Full build: {'✓ PASS' if full_ok else '✗ FAIL'}")
    print(f"Security status: {security_status}")

    if missing_files:
        print("\nNEXT STEPS:")
        print("- Review and complete the created secure template files")
        print("- Remove TODO_*.md files when content is complete")
        if SANITIZER_AVAILABLE:
            print("- All templates include security enhancements")

    return 0 if (basic_ok and full_ok) else 1


if __name__ == "__main__":
    sys.exit(main())
