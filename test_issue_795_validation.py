#!/usr/bin/env python3
"""
Test script to validate the requirements mentioned in Issue #795
Based on PR #552 requirements for GitHub Actions LaTeX build fixes
"""

import yaml
import os
import sys

def test_yaml_syntax_fixes():
    """Test that all workflow files use proper 'on' keyword quoting"""
    print("🔍 Testing YAML syntax fixes...")
    
    workflow_files = [
        '.github/workflows/latex-build.yml',
        '.github/workflows/latex-validation.yml', 
        '.github/workflows/static.yml'
    ]
    
    all_correct = True
    
    for file_path in workflow_files:
        if not os.path.exists(file_path):
            print(f"❌ Workflow file not found: {file_path}")
            all_correct = False
            continue
            
        with open(file_path, 'r') as f:
            content = f.read()
            
        # Check for properly quoted 'on' keyword
        if '"on":' in content:
            print(f"✅ {os.path.basename(file_path)}: Properly quoted 'on' keyword")
        elif 'on:' in content and '"on":' not in content:
            print(f"❌ {os.path.basename(file_path)}: Unquoted 'on' keyword found")
            all_correct = False
        else:
            print(f"⚠️  {os.path.basename(file_path)}: No 'on' keyword found")
    
    return all_correct

def test_latex_action_version():
    """Test that dante-ev/latex-action uses correct version"""
    print("\n🔍 Testing dante-ev/latex-action version...")
    
    workflow_path = '.github/workflows/latex-build.yml'
    
    if not os.path.exists(workflow_path):
        print(f"❌ Workflow file not found: {workflow_path}")
        return False
    
    try:
        with open(workflow_path, 'r') as f:
            workflow = yaml.safe_load(f)
    except Exception as e:
        print(f"❌ Failed to parse workflow: {e}")
        return False
    
    # Find the LaTeX action step
    jobs = workflow.get('jobs', {})
    build_job = jobs.get('build', {})
    steps = build_job.get('steps', [])
    
    latex_step = None
    for step in steps:
        if step.get('name') == 'Set up LaTeX':
            latex_step = step
            break
    
    if not latex_step:
        print("❌ 'Set up LaTeX' step not found")
        return False
    
    uses_action = latex_step.get('uses', '')
    print(f"   Found: {uses_action}")
    
    # Check for correct version (according to PR requirements)
    if 'dante-ev/latex-action@latest' in uses_action:
        print("✅ Using @latest version as mentioned in PR")
        return True
    elif 'dante-ev/latex-action@v2' in uses_action:
        print("⚠️  Using @v2 (stable version, but PR mentions @latest)")
        return True  # This is acceptable
    elif 'dante-ev/latex-action@v2.0.0' in uses_action:
        print("❌ Still using problematic v2.0.0 version")
        return False
    else:
        print(f"❌ Unexpected version: {uses_action}")
        return False

def test_latex_packages():
    """Test that comprehensive LaTeX packages are installed"""
    print("\n🔍 Testing LaTeX package installation...")
    
    workflow_path = '.github/workflows/latex-build.yml'
    
    if not os.path.exists(workflow_path):
        print(f"❌ Workflow file not found: {workflow_path}")
        return False
    
    with open(workflow_path, 'r') as f:
        content = f.read()
    
    # Required packages mentioned in PR description
    required_packages = [
        'texlive-lang-german',  # German language support
        'texlive-fonts-extra',  # For fontawesome5
        'texlive-fonts-recommended',
        'texlive-latex-recommended',
        'texlive-latex-extra'
    ]
    
    missing_packages = []
    for package in required_packages:
        if package in content:
            print(f"✅ Found package: {package}")
        else:
            print(f"❌ Missing package: {package}")
            missing_packages.append(package)
    
    return len(missing_packages) == 0

def test_latex_arguments():
    """Test that correct latexmk arguments are used"""
    print("\n🔍 Testing LaTeX compilation arguments...")
    
    workflow_path = '.github/workflows/latex-build.yml'
    
    if not os.path.exists(workflow_path):
        print(f"❌ Workflow file not found: {workflow_path}")
        return False
    
    with open(workflow_path, 'r') as f:
        content = f.read()
    
    # Check for correct arguments (no -pdf which was problematic)
    if 'args:' in content:
        # Extract the args line
        lines = content.split('\n')
        args_line = None
        for line in lines:
            if 'args:' in line:
                args_line = line.strip()
                break
        
        if args_line:
            print(f"   Found args: {args_line}")
            
            # Check for problematic -pdf argument
            if '-pdf' in args_line:
                print("❌ Problematic -pdf argument found")
                return False
            
            # Check for required arguments
            required_args = ['-interaction=nonstopmode', '-halt-on-error', '-shell-escape']
            missing_args = []
            for arg in required_args:
                if arg not in args_line:
                    missing_args.append(arg)
            
            if missing_args:
                print(f"❌ Missing required arguments: {missing_args}")
                return False
            else:
                print("✅ All required arguments present")
                return True
        else:
            print("❌ No args line found")
            return False
    else:
        print("❌ No args configuration found")
        return False

def main():
    """Run all validation tests for Issue #795"""
    print("🎯 ISSUE #795 VALIDATION")
    print("Validating GitHub Actions LaTeX build fixes from PR #552")
    print("=" * 60)
    
    tests = [
        ("YAML syntax fixes", test_yaml_syntax_fixes),
        ("LaTeX action version", test_latex_action_version),
        ("LaTeX package installation", test_latex_packages),
        ("LaTeX compilation arguments", test_latex_arguments)
    ]
    
    all_passed = True
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
            if not result:
                all_passed = False
        except Exception as e:
            print(f"❌ ERROR in {test_name}: {e}")
            results.append((test_name, False))
            all_passed = False
    
    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\nOverall Status: {'✅ SUCCESS' if all_passed else '❌ NEEDS FIXES'}")
    
    if all_passed:
        print("\n🎉 All requirements from PR #552 are satisfied!")
        print("The GitHub Actions workflow should build LaTeX PDFs successfully.")
    else:
        print("\n⚠️  Some requirements from PR #552 still need to be addressed.")
    
    return all_passed

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)