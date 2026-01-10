#!/usr/bin/env python3
"""
Test script to validate FontAwesome package dependency fixes.

This script validates that:
1. The GitHub Actions workflow includes proper installation of texlive-fonts-extra
2. The workflow uses direct pdflatex compilation instead of LaTeX actions
3. FontAwesome package support is properly documented in README
4. Main.tex correctly uses the fontawesome5 package
"""

import os
import yaml
import sys

def test_workflow_uses_direct_pdflatex():
    """Test that workflow uses direct pdflatex compilation instead of LaTeX actions."""
    print("🔍 Testing workflow uses direct pdflatex compilation...")

    workflow_path = '.github/workflows/latex-build.yml'
    if not os.path.exists(workflow_path):
        print(f"❌ Workflow file {workflow_path} not found")
        return False

    with open(workflow_path, 'r') as f:
        content = f.read()

    # Check that workflow doesn't use LaTeX actions
    latex_actions = ['dante-ev/latex-action', 'xu-cheng/latex-action']
    for action in latex_actions:
        if action in content:
            print(f"❌ Workflow still uses LaTeX action: {action}")
            return False

    # Check that workflow uses direct pdflatex compilation
    if 'pdflatex -interaction=nonstopmode -halt-on-error -shell-escape main.tex' not in content:
        print("❌ Workflow doesn't use direct pdflatex compilation")
        return False

    print("✅ Workflow uses direct pdflatex compilation")
    return True

def test_texlive_fonts_extra_installation():
    """Test that workflow installs texlive-fonts-extra for FontAwesome support."""
    print("🔍 Testing texlive-fonts-extra installation...")

    workflow_path = '.github/workflows/latex-build.yml'
    with open(workflow_path, 'r') as f:
        content = f.read()

    required_packages = [
        'texlive-fonts-extra',  # Essential for FontAwesome
        'texlive-latex-base',
        'texlive-latex-extra',
        'texlive-fonts-recommended',
        'texlive-lang-german'
    ]

    missing_packages = []
    for package in required_packages:
        if package not in content:
            missing_packages.append(package)

    if missing_packages:
        print(f"❌ Missing required packages: {', '.join(missing_packages)}")
        return False

    print("✅ All required LaTeX packages are included")
    return True

def test_fontawesome_documentation():
    """Test that README includes FontAwesome troubleshooting documentation."""
    print("🔍 Testing FontAwesome documentation...")

    readme_path = 'README.md'
    if not os.path.exists(readme_path):
        print("❌ README.md not found")
        return False

    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()

    required_sections = [
        'FontAwesome Package Issues',
        'texlive-fonts-extra',
        'fontawesome5',
        'Troubleshooting'
    ]

    missing_sections = []
    for section in required_sections:
        if section not in content:
            missing_sections.append(section)

    if missing_sections:
        print(f"❌ Missing documentation sections: {', '.join(missing_sections)}")
        return False

    print("✅ FontAwesome documentation is complete")
    return True

def test_main_tex_fontawesome_usage():
    """Test that main.tex properly uses fontawesome5 package."""
    print("🔍 Testing main.tex FontAwesome usage...")

    main_tex_path = 'main.tex'
    if not os.path.exists(main_tex_path):
        print("❌ main.tex not found")
        return False

    with open(main_tex_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check that fontawesome5 package is loaded
    if '\\usepackage{fontawesome5}' not in content:
        print("❌ fontawesome5 package not loaded in main.tex")
        return False

    # Check that FontAwesome icons are used (e.g., \faCompass)
    if '\\faCompass' not in content:
        print("⚠️  Warning: No FontAwesome icons found in main.tex")
    else:
        print("✅ FontAwesome icons are used in main.tex")

    print("✅ main.tex properly uses fontawesome5 package")
    return True

def test_yaml_syntax():
    """Test that workflow YAML syntax is valid."""
    print("🔍 Testing workflow YAML syntax...")

    workflow_path = '.github/workflows/latex-build.yml'
    try:
        with open(workflow_path, 'r') as f:
            yaml.safe_load(f)
        print("✅ Workflow YAML syntax is valid")
        return True
    except yaml.YAMLError as e:
        print(f"❌ YAML syntax error: {e}")
        return False

def main():
    """Run all FontAwesome dependency fix tests."""
    print("🧪 Testing FontAwesome Package Dependency Fixes")
    print("=" * 60)

    tests = [
        test_workflow_uses_direct_pdflatex,
        test_texlive_fonts_extra_installation,
        test_fontawesome_documentation,
        test_main_tex_fontawesome_usage,
        test_yaml_syntax
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        try:
            if test():
                passed += 1
            print()  # Add spacing between tests
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
            print()

    print("=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("✅ All FontAwesome dependency fixes are working correctly!")
        return 0
    else:
        print("❌ Some tests failed. Please review the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
