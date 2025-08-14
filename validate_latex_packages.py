#!/usr/bin/env python3
"""
LaTeX Package Validation Script for CTMM System
Validates that all required LaTeX packages are available in the CI environment.
"""

import subprocess
import sys
from pathlib import Path


def validate_latex_installation():
    """Check if LaTeX is properly installed."""
    print("="*60)
    print("LATEX INSTALLATION VALIDATION")
    print("="*60)
    
    try:
        result = subprocess.run(
            ["pdflatex", "--version"], 
            capture_output=True, 
            text=True,
            check=True
        )
        print("✅ pdflatex is available")
        print(f"Version: {result.stdout.split()[1] if result.stdout else 'unknown'}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ pdflatex not found")
        print("Please install a LaTeX distribution (TeX Live, MiKTeX, etc.)")
        return False


def test_package(package_name, test_options=""):
    """Test if a specific LaTeX package is available."""
    test_content = f"""\\documentclass{{article}}
\\usepackage{test_options}{{{package_name}}}
\\begin{{document}}
Package {package_name} test.
\\end{{document}}"""
    
    test_file = f"test_{package_name.replace('/', '_')}.tex"
    
    try:
        # Write test file
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(test_content)
        
        # Test compilation
        result = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", test_file],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # Clean up files
        for ext in ['.tex', '.aux', '.log', '.out', '.pdf']:
            Path(test_file.replace('.tex', ext)).unlink(missing_ok=True)
        
        if result.returncode == 0:
            print(f"✅ {package_name}")
            return True
        else:
            # Check for specific error messages
            if "! LaTeX Error: File" in result.stdout:
                print(f"❌ {package_name} - Package not found")
            elif "! Package" in result.stdout and "Error:" in result.stdout:
                print(f"⚠️  {package_name} - Package found but has issues")
                print(f"   Error details in: {test_file.replace('.tex', '.log')}")
            else:
                print(f"❌ {package_name} - Compilation failed")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏱️  {package_name} - Test timed out")
        return False
    except Exception as e:
        print(f"❌ {package_name} - Test failed: {e}")
        return False


def validate_required_packages():
    """Validate all packages required by the CTMM system."""
    print("\n" + "="*60)
    print("REQUIRED PACKAGE VALIDATION")
    print("="*60)
    
    # Core LaTeX packages
    core_packages = [
        ("fontenc", "[T1]"),
        ("inputenc", "[utf8]"),
        ("babel", "[ngerman]"),
        ("geometry", ""),
        ("hyperref", ""),
        ("xcolor", ""),
        ("amssymb", ""),
        ("tabularx", ""),
    ]
    
    print("\n📦 Core LaTeX packages:")
    core_results = []
    for package, options in core_packages:
        result = test_package(package, options)
        core_results.append(result)
    
    # Font and graphics packages
    font_graphics_packages = [
        ("fontawesome5", ""),
        ("tcolorbox", ""),
        ("tikz", ""),
        ("pifont", ""),
    ]
    
    print("\n🎨 Font and graphics packages:")
    font_results = []
    for package, options in font_graphics_packages:
        result = test_package(package, options)
        font_results.append(result)
    
    # Utility packages
    utility_packages = [
        ("ifthen", ""),
        ("calc", ""),
        ("forloop", ""),
    ]
    
    print("\n🔧 Utility packages:")
    utility_results = []
    for package, options in utility_packages:
        result = test_package(package, options)
        utility_results.append(result)
    
    # Summary
    total_packages = len(core_packages) + len(font_graphics_packages) + len(utility_packages)
    total_successful = sum(core_results) + sum(font_results) + sum(utility_results)
    
    print("\n" + "="*60)
    print("PACKAGE VALIDATION SUMMARY")
    print("="*60)
    print(f"Total packages tested: {total_packages}")
    print(f"Successful: {total_successful}")
    print(f"Failed: {total_packages - total_successful}")
    
    if total_successful == total_packages:
        print("🎉 All required packages are available!")
        return True
    else:
        print("⚠️  Some packages are missing or have issues.")
        print("\nRecommended actions:")
        print("1. Install missing packages using your LaTeX package manager")
        print("2. For Ubuntu/Debian: apt-get install texlive-full")
        print("3. For CI/CD: Update workflow with missing package dependencies")
        return False


def suggest_ci_packages():
    """Suggest TeXLive packages for CI environments."""
    print("\n" + "="*60)
    print("CI/CD PACKAGE RECOMMENDATIONS")
    print("="*60)
    print("For GitHub Actions with dante-ev/latex-action, include:")
    print("```yaml")
    print("extra_system_packages: |")
    print("  texlive-lang-german")
    print("  texlive-fonts-recommended")
    print("  texlive-latex-recommended")
    print("  texlive-fonts-extra        # for fontawesome5, pifont")
    print("  texlive-latex-extra        # for tcolorbox, advanced packages")
    print("  texlive-science            # for additional math/science packages")
    print("  texlive-pictures           # for tikz and graphics")
    print("  texlive-plain-generic      # for basic utilities")
    print("```")


def main():
    """Main validation function."""
    print("CTMM LaTeX Package Validation")
    print("Checking LaTeX environment for CTMM system compatibility...\n")
    
    # Check LaTeX installation
    if not validate_latex_installation():
        print("\n❌ LaTeX installation check failed.")
        suggest_ci_packages()
        return 1
    
    # Validate packages
    if not validate_required_packages():
        print("\n❌ Package validation failed.")
        suggest_ci_packages()
        return 1
    
    print("\n✅ All validation checks passed!")
    print("Your LaTeX environment is ready for the CTMM system.")
    return 0


if __name__ == "__main__":
    sys.exit(main())