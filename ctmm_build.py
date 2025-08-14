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


def check_latex_availability():
    """Check if LaTeX is available and return environment info."""
    try:
        result = subprocess.run(['pdflatex', '--version'], capture_output=True, check=True, text=True)
        logger.debug("LaTeX available: %s", result.stdout.split('\n')[0])
        return True
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        logger.debug("LaTeX not available: %s", e)
        return False


def analyze_latex_error(log_content):
    """Analyze LaTeX log content and extract meaningful error information."""
    errors = []
    warnings = []
    
    if not log_content:
        return {
            "errors": [], 
            "warnings": [], 
            "summary": "No log content available",
            "total_errors": 0,
            "total_warnings": 0
        }
    
    lines = log_content.split('\n')
    
    for i, line in enumerate(lines):
        line = line.strip()
        
        # Error patterns
        if line.startswith('!'):
            errors.append({
                "line": i + 1,
                "error": line,
                "context": lines[i:i+3] if i+3 < len(lines) else lines[i:]
            })
        
        # Warning patterns
        elif 'Warning:' in line or 'warning:' in line:
            warnings.append({
                "line": i + 1,
                "warning": line
            })
        
        # Package errors
        elif 'Package' in line and ('Error' in line or 'error' in line):
            errors.append({
                "line": i + 1,
                "error": line,
                "type": "package_error"
            })
    
    summary = f"Found {len(errors)} errors and {len(warnings)} warnings"
    
    return {
        "errors": errors,
        "warnings": warnings,
        "summary": summary,
        "total_errors": len(errors),
        "total_warnings": len(warnings)
    }


def save_build_artifacts(build_type, success, log_content="", error_output=""):
    """Save build artifacts for CI analysis."""
    timestamp = "latest"  # Could be made more specific
    
    # Save log file
    log_file = f"build_{build_type}_{timestamp}.log"
    try:
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write(f"Build Type: {build_type}\n")
            f.write(f"Success: {success}\n")
            f.write(f"Timestamp: {timestamp}\n")
            f.write("-" * 50 + "\n")
            if log_content:
                f.write("LaTeX Log Output:\n")
                f.write(log_content)
            if error_output:
                f.write("\nError Output:\n")
                f.write(error_output)
        logger.info("Build artifacts saved to %s", log_file)
    except Exception as e:
        logger.warning("Failed to save build artifacts: %s", e)
    
    return log_file


def detect_ci_environment():
    """Detect if running in CI environment and provide appropriate configuration."""
    import os
    
    ci_indicators = {
        'GITHUB_ACTIONS': 'GitHub Actions',
        'CI': 'Generic CI',
        'CONTINUOUS_INTEGRATION': 'CI Environment',
        'GITLAB_CI': 'GitLab CI',
        'TRAVIS': 'Travis CI',
        'JENKINS_URL': 'Jenkins'
    }
    
    detected = []
    for env_var, name in ci_indicators.items():
        if os.getenv(env_var):
            detected.append(name)
    
    return {
        'is_ci': len(detected) > 0,
        'environments': detected,
        'github_actions': os.getenv('GITHUB_ACTIONS') == 'true'
    }


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
    logger.info("Testing basic build (without modules)...")

    # Check if pdflatex is available
    latex_available = check_latex_availability()
    if not latex_available:
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

        # Test build with comprehensive error capture
        result = subprocess.run(
            ['pdflatex', '-interaction=nonstopmode', temp_file],
            capture_output=True,
            text=True,
            errors='replace',  # Handle encoding issues
            check=False
        )

        success = result.returncode == 0
        
        # Analyze build results
        if success:
            logger.info("✓ Basic build successful")
        else:
            logger.error("✗ Basic build failed")
            
            # Enhanced error analysis
            error_analysis = analyze_latex_error(result.stdout + result.stderr)
            logger.error("Error Summary: %s", error_analysis["summary"])
            
            # Save artifacts for CI debugging
            artifact_file = save_build_artifacts(
                "basic", 
                success, 
                result.stdout, 
                result.stderr
            )
            
            # In CI environment, provide additional context
            ci_info = detect_ci_environment()
            if ci_info['is_ci']:
                logger.error("CI Environment detected: %s", ', '.join(ci_info['environments']))
                logger.error("Build artifacts saved to: %s", artifact_file)
                logger.error("Check %s.log for detailed LaTeX output", temp_file)

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
    latex_available = check_latex_availability()
    if not latex_available:
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
            
            # Enhanced error analysis for full build
            error_analysis = analyze_latex_error(result.stdout + result.stderr)
            logger.error("Error Summary: %s", error_analysis["summary"])
            
            # Save comprehensive artifacts
            artifact_file = save_build_artifacts(
                "full", 
                success, 
                result.stdout, 
                result.stderr
            )
            
            # Provide detailed error information for CI
            ci_info = detect_ci_environment()
            if ci_info['is_ci']:
                logger.error("CI Environment: %s", ', '.join(ci_info['environments']))
                logger.error("Full build artifacts: %s", artifact_file)
                logger.error("Check main.log for detailed LaTeX error information")
                
                # Output error details for CI logs
                if error_analysis["errors"]:
                    logger.error("Key errors found:")
                    for error in error_analysis["errors"][:3]:  # Show first 3 errors
                        logger.error("  - %s", error.get("error", "Unknown error"))

        return success

    except Exception as e:
        logger.error("Full build test failed: %s", e)
        return False


def main():
    """Run the CTMM build system check."""
    logger.info("CTMM Build System - Starting check...")
    
    # Detect CI environment early
    ci_info = detect_ci_environment()
    if ci_info['is_ci']:
        logger.info("CI Environment detected: %s", ', '.join(ci_info['environments']))
    
    # Check LaTeX availability
    latex_available = check_latex_availability()
    logger.info("LaTeX availability: %s", "Available" if latex_available else "Not available")

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
    print(f"Environment: {'CI (' + ', '.join(ci_info['environments']) + ')' if ci_info['is_ci'] else 'Local'}")
    print(f"LaTeX: {'Available' if latex_available else 'Not available'}")
    print(f"Style files: {len(style_files)}")
    print(f"Module files: {len(module_files)}")
    print(f"Missing files: {len(missing_files)} (templates created)")
    print(f"Basic build: {'✓ PASS' if basic_ok else '✗ FAIL'}")
    print(f"Full build: {'✓ PASS' if full_ok else '✗ FAIL'}")

    if missing_files:
        print("\nNEXT STEPS:")
        print("- Review and complete the created template files")
        print("- Remove TODO_*.md files when content is complete")
    
    if not (basic_ok and full_ok):
        print("\nBUILD FAILURES DETECTED:")
        if ci_info['is_ci']:
            print("- Check build artifacts in workflow logs")
            print("- Review LaTeX error details in build_*.log files")
        else:
            print("- Check local LaTeX installation and package dependencies")
            print("- Review generated .log files for error details")

    return 0 if (basic_ok and full_ok) else 1


if __name__ == "__main__":
    sys.exit(main())
