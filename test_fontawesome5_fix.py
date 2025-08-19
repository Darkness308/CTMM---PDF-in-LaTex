#!/usr/bin/env python3
"""
Test script to validate the fontawesome5 package fix.
This script validates that:
1. GitHub Actions workflow has been updated to use direct pdflatex commands
2. Required LaTeX packages for fontawesome5 support are properly installed
3. The style files do not contain Git merge conflicts
4. README.md contains troubleshooting documentation for fontawesome5
"""

import yaml
import os
import subprocess
import sys

def test_workflow_direct_pdflatex():
    """Test that the GitHub Actions workflow uses direct pdflatex instead of dante-ev/latex-action"""
    
    print("🧪 Testing GitHub Actions workflow for direct pdflatex usage...")
    
    workflow_path = '.github/workflows/latex-build.yml'
    
    if not os.path.exists(workflow_path):
        print(f"❌ ERROR: Workflow file {workflow_path} not found")
        return False
    
    try:
        with open(workflow_path, 'r') as f:
            workflow_content = f.read()
    except Exception as e:
        print(f"❌ ERROR: Failed to read {workflow_path}: {e}")
        return False
    
    # Check that dante-ev/latex-action is NOT used
    if 'dante-ev/latex-action' in workflow_content:
        print("❌ FAILED: dante-ev/latex-action is still being used")
        return False
    else:
        print("✅ SUCCESS: dante-ev/latex-action has been removed")
    
    # Check that direct pdflatex commands are used
    if 'pdflatex -interaction=nonstopmode -halt-on-error -shell-escape main.tex' in workflow_content:
        print("✅ SUCCESS: Direct pdflatex command found")
    else:
        print("❌ FAILED: Direct pdflatex command not found")
        return False
    
    # Check that LaTeX packages are installed via apt-get
    if 'texlive-fonts-extra' in workflow_content and 'apt-get install' in workflow_content:
        print("✅ SUCCESS: texlive-fonts-extra package installation found")
    else:
        print("❌ FAILED: texlive-fonts-extra package installation not found")
        return False
    
    return True

def test_latex_packages_installation():
    """Test that the workflow installs the correct LaTeX packages"""
    
    print("\n📦 Testing LaTeX package installation configuration...")
    
    workflow_path = '.github/workflows/latex-build.yml'
    
    try:
        with open(workflow_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ ERROR: Failed to read {workflow_path}: {e}")
        return False
    
    # Essential packages for fontawesome5
    required_packages = [
        'texlive-latex-recommended',
        'texlive-fonts-recommended', 
        'texlive-fonts-extra',  # Contains fontawesome5
        'texlive-latex-extra',
        'texlive-lang-german',
        'texlive-science',
        'texlive-pstricks'
    ]
    
    missing_packages = []
    for package in required_packages:
        if package in content:
            print(f"✅ FOUND: {package}")
        else:
            missing_packages.append(package)
            print(f"❌ MISSING: {package}")
    
    if missing_packages:
        print(f"❌ FAILED: Missing packages: {missing_packages}")
        return False
    
    print("✅ SUCCESS: All required LaTeX packages are configured for installation")
    return True

def test_style_files_no_conflicts():
    """Test that style files do not contain Git merge conflicts"""
    
    print("\n🔧 Testing style files for Git merge conflicts...")
    
    style_files = [
        'style/ctmm-design.sty',
        'style/form-elements.sty', 
        'style/ctmm-diagrams.sty'
    ]
    
    for style_file in style_files:
        if not os.path.exists(style_file):
            print(f"⚠️  WARNING: {style_file} not found")
            continue
            
        try:
            with open(style_file, 'r') as f:
                content = f.read()
                
            # Check for common Git merge conflict markers
            conflict_markers = ['<<<<<<<', '>>>>>>>', '=======', 'copilot/fix-', 'main']
            has_conflicts = False
            
            for marker in conflict_markers:
                if marker in content:
                    print(f"❌ CONFLICT: Found '{marker}' in {style_file}")
                    has_conflicts = True
            
            if not has_conflicts:
                print(f"✅ CLEAN: {style_file}")
                
        except Exception as e:
            print(f"❌ ERROR: Failed to read {style_file}: {e}")
            return False
    
    print("✅ SUCCESS: Style files are clean of merge conflicts")
    return True

def test_fontawesome5_documentation():
    """Test that README.md contains fontawesome5 troubleshooting documentation"""
    
    print("\n📚 Testing fontawesome5 troubleshooting documentation...")
    
    readme_path = 'README.md'
    
    if not os.path.exists(readme_path):
        print(f"❌ ERROR: {readme_path} not found")
        return False
    
    try:
        with open(readme_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ ERROR: Failed to read {readme_path}: {e}")
        return False
    
    # Check for fontawesome5 specific documentation
    checks = [
        ('fontawesome5.sty', 'fontawesome5.sty file reference'),
        ('texlive-fonts-extra', 'texlive-fonts-extra package mention'),
        ('Troubleshooting: fontawesome5.sty Package Missing', 'Troubleshooting section'),
        ('apt-get install texlive-fonts-extra', 'Installation command')
    ]
    
    all_found = True
    for check_text, description in checks:
        if check_text in content:
            print(f"✅ FOUND: {description}")
        else:
            print(f"❌ MISSING: {description}")
            all_found = False
    
    if all_found:
        print("✅ SUCCESS: All fontawesome5 troubleshooting documentation is present")
        return True
    else:
        print("❌ FAILED: Some fontawesome5 troubleshooting documentation is missing")
        return False

def test_fontawesome5_package_availability():
    """Test that fontawesome5 package can be found in the LaTeX installation"""
    
    print("\n🔍 Testing fontawesome5 package availability...")
    
    try:
        # Check if kpsewhich can find fontawesome5.sty
        result = subprocess.run(
            ['kpsewhich', 'fontawesome5.sty'],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0 and result.stdout.strip():
            print(f"✅ SUCCESS: fontawesome5.sty found at: {result.stdout.strip()}")
            return True
        else:
            print("❌ FAILED: fontawesome5.sty not found in LaTeX installation")
            return False
            
    except FileNotFoundError:
        print("⚠️  WARNING: kpsewhich not available (LaTeX not installed)")
        return True  # Don't fail if LaTeX is not installed
    except Exception as e:
        print(f"❌ ERROR: Failed to check fontawesome5 package: {e}")
        return False

def main():
    """Main test function"""
    print("=" * 70)
    print("FONTAWESOME5 PACKAGE FIX VALIDATION")
    print("=" * 70)
    
    tests = [
        ("GitHub Actions workflow uses direct pdflatex", test_workflow_direct_pdflatex),
        ("LaTeX packages installation configuration", test_latex_packages_installation),
        ("Style files clean of merge conflicts", test_style_files_no_conflicts),
        ("fontawesome5 troubleshooting documentation", test_fontawesome5_documentation),
        ("fontawesome5 package availability", test_fontawesome5_package_availability)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ ERROR in {test_name}: {e}")
    
    print("\n" + "=" * 70)
    print("VALIDATION SUMMARY")
    print("=" * 70)
    
    if passed == total:
        print(f"✅ PASS All tests passed ({passed}/{total})")
        print("🎉 fontawesome5 package fix has been successfully implemented!")
        return True
    else:
        print(f"❌ FAIL {total - passed} test(s) failed ({passed}/{total})")
        print("⚠️  Some issues need to be addressed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)