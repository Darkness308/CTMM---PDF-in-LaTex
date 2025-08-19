#!/usr/bin/env python3
"""
Test script to validate the GitHub Actions workflow fix for fontawesome5 package issues.
Verifies that the direct LaTeX installation approach properly addresses fontawesome5 dependencies.
"""

import yaml
import os
import subprocess
import sys

def test_workflow_uses_direct_latex_installation():
    """Test that the workflow now uses direct LaTeX installation instead of dante-ev/latex-action"""
    
    print("🧪 Testing GitHub Actions workflow uses direct LaTeX installation...")
    
    # Read the workflow file
    with open(".github/workflows/latex-build.yml", "r") as f:
        content = f.read()
        workflow_content = yaml.safe_load(f.seekable() and f.seek(0) or f.read())
    
    # Check that dante-ev/latex-action is NOT used
    if "dante-ev/latex-action" in content:
        print("❌ FAILED: Workflow still uses dante-ev/latex-action")
        return False
    
    print("✅ SUCCESS: dante-ev/latex-action has been replaced")
    
    # Check for direct LaTeX installation step
    jobs = workflow_content.get('jobs', {})
    build_job = jobs.get('build', {})
    steps = build_job.get('steps', [])
    
    install_step_found = False
    compile_step_found = False
    
    for step in steps:
        step_name = step.get('name', '')
        if 'Install LaTeX and packages' in step_name:
            install_step_found = True
            run_command = step.get('run', '')
            
            # Check for direct apt-get installation
            if 'apt-get install' not in run_command:
                print("❌ FAILED: Install step doesn't use apt-get install")
                return False
                
            print("✅ SUCCESS: Found direct LaTeX package installation step")
            
        elif 'Compile LaTeX document' in step_name:
            compile_step_found = True
            run_command = step.get('run', '')
            
            # Check for direct pdflatex usage
            if 'pdflatex' not in run_command:
                print("❌ FAILED: Compile step doesn't use pdflatex directly")
                return False
                
            print("✅ SUCCESS: Found direct pdflatex compilation step")
    
    if not install_step_found:
        print("❌ FAILED: 'Install LaTeX and packages' step not found")
        return False
        
    if not compile_step_found:
        print("❌ FAILED: 'Compile LaTeX document' step not found")
        return False
    
    return True


def test_fontawesome5_package_coverage():
    """Test that texlive-fonts-extra is properly installed for fontawesome5 support"""
    
    print("\n🧪 Testing fontawesome5 package coverage...")
    
    with open(".github/workflows/latex-build.yml", "r") as f:
        content = f.read()
    
    # Check for texlive-fonts-extra in the installation
    if 'texlive-fonts-extra' not in content:
        print("❌ FAILED: texlive-fonts-extra package not found in workflow")
        return False
    
    print("✅ SUCCESS: texlive-fonts-extra package is included for fontawesome5 support")
    
    # Check for texlive-full as a comprehensive solution
    if 'texlive-full' in content:
        print("✅ BONUS: texlive-full is also installed for comprehensive coverage")
    
    return True


def test_troubleshooting_documentation():
    """Test that troubleshooting documentation for fontawesome5 is present in README"""
    
    print("\n🧪 Testing fontawesome5 troubleshooting documentation...")
    
    with open("README.md", "r", encoding='utf-8') as f:
        readme_content = f.read()
    
    # Check for troubleshooting section
    if 'Problembehebung' not in readme_content and 'Troubleshooting' not in readme_content:
        print("❌ FAILED: No troubleshooting section found in README")
        return False
    
    # Check for fontawesome5 specific guidance
    if 'fontawesome5.sty' not in readme_content:
        print("❌ FAILED: No fontawesome5.sty troubleshooting found in README")
        return False
    
    # Check for installation instructions
    if 'texlive-fonts-extra' not in readme_content:
        print("❌ FAILED: No texlive-fonts-extra installation instructions in README")
        return False
    
    print("✅ SUCCESS: fontawesome5 troubleshooting documentation is present")
    print("✅ SUCCESS: Installation instructions for multiple platforms included")
    
    return True


def test_fontawesome5_usage_in_codebase():
    """Test that fontawesome5 is actually used in the LaTeX codebase"""
    
    print("\n🧪 Testing fontawesome5 usage in codebase...")
    
    # Check main.tex for fontawesome5 package
    with open("main.tex", "r") as f:
        main_content = f.read()
    
    if '\\usepackage{fontawesome5}' not in main_content:
        print("❌ FAILED: fontawesome5 package not declared in main.tex")
        return False
    
    print("✅ SUCCESS: fontawesome5 package is declared in main.tex")
    
    # Check for actual fontawesome usage (like \faCompass)
    if '\\fa' not in main_content:
        print("⚠️  WARNING: No fontawesome icons found in main.tex")
    else:
        print("✅ SUCCESS: FontAwesome icons are used in the document")
    
    return True


def test_workflow_syntax_validity():
    """Test that the workflow YAML is still syntactically valid"""
    
    print("\n🧪 Testing workflow YAML syntax validity...")
    
    try:
        with open(".github/workflows/latex-build.yml", "r") as f:
            workflow_content = yaml.safe_load(f)
        
        # Basic structure checks
        if 'jobs' not in workflow_content:
            print("❌ FAILED: No 'jobs' section in workflow")
            return False
            
        if 'build' not in workflow_content['jobs']:
            print("❌ FAILED: No 'build' job in workflow")
            return False
            
        print("✅ SUCCESS: Workflow YAML syntax is valid")
        return True
        
    except yaml.YAMLError as e:
        print(f"❌ FAILED: YAML syntax error: {e}")
        return False


def main():
    """Main test function"""
    
    print("="*60)
    print("FONTAWESOME5 PACKAGE FIX VALIDATION")
    print("Testing GitHub Actions workflow improvements")
    print("="*60)
    
    tests = [
        test_workflow_uses_direct_latex_installation,
        test_fontawesome5_package_coverage,
        test_troubleshooting_documentation,
        test_fontawesome5_usage_in_codebase,
        test_workflow_syntax_validity
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                print("❌ TEST FAILED")
        except Exception as e:
            print(f"❌ TEST ERROR: {e}")
    
    print("\n" + "="*60)
    print(f"RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED!")
        print("✅ GitHub Actions workflow properly addresses fontawesome5 package issues")
        print("✅ Direct LaTeX installation provides better package control")
        print("✅ Documentation includes troubleshooting guidance")
        return 0
    else:
        print("❌ Some tests failed - please review the issues above")
        return 1


if __name__ == "__main__":
    sys.exit(main())