#!/usr/bin/env python3
"""
Issue #795 Resolution Validation - GitHub Actions LaTeX Build Fixes
Validates that PR #552 requirements have been properly implemented.
"""

import yaml
import os
import sys
import subprocess

def verify_yaml_syntax_fix():
    """Verify that YAML syntax is correct with properly quoted 'on' keyword"""
    print("🔧 VERIFYING: YAML Syntax Fix")
    print("-" * 50)
    
    workflow_files = [
        '.github/workflows/latex-build.yml',
        '.github/workflows/latex-validation.yml', 
        '.github/workflows/static.yml'
    ]
    
    all_correct = True
    
    for file_path in workflow_files:
        if not os.path.exists(file_path):
            print(f"❌ Missing workflow file: {file_path}")
            all_correct = False
            continue
            
        with open(file_path, 'r') as f:
            content = f.read()
            
        # Check YAML structure
        try:
            workflow = yaml.safe_load(content)
            if 'on' in workflow and isinstance(workflow['on'], dict):
                print(f"✅ {os.path.basename(file_path)}: Valid YAML with properly quoted 'on' keyword")
            else:
                print(f"❌ {os.path.basename(file_path)}: Invalid YAML structure")
                all_correct = False
        except yaml.YAMLError as e:
            print(f"❌ {os.path.basename(file_path)}: YAML parsing error: {e}")
            all_correct = False
    
    return all_correct

def verify_latex_action_update():
    """Verify dante-ev/latex-action has been updated to @latest"""
    print("\n🔧 VERIFYING: LaTeX Action Version Update")
    print("-" * 50)
    
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
    print(f"   Current action: {uses_action}")
    
    if 'dante-ev/latex-action@latest' in uses_action:
        print("✅ Successfully updated to @latest version")
        print("   This matches PR #552 requirement: 'Updated dante-ev/latex-action from v2.0.0 to @latest'")
        return True
    else:
        print("❌ Action not updated to @latest")
        return False

def verify_latex_packages():
    """Verify comprehensive LaTeX package installation including German support and fontawesome5"""
    print("\n🔧 VERIFYING: Comprehensive LaTeX Package Installation")
    print("-" * 50)
    
    workflow_path = '.github/workflows/latex-build.yml'
    
    if not os.path.exists(workflow_path):
        print(f"❌ Workflow file not found: {workflow_path}")
        return False
    
    with open(workflow_path, 'r') as f:
        content = f.read()
    
    # Check for required packages from PR description
    required_packages = {
        'texlive-lang-german': 'German language support',
        'texlive-fonts-extra': 'Includes fontawesome5 support',
        'texlive-fonts-recommended': 'Recommended font packages',
        'texlive-latex-recommended': 'Recommended LaTeX packages',
        'texlive-latex-extra': 'Additional LaTeX packages'
    }
    
    all_found = True
    
    for package, description in required_packages.items():
        if package in content:
            print(f"✅ {package}: {description}")
        else:
            print(f"❌ Missing {package}: {description}")
            all_found = False
    
    # Check for fontawesome5 specific support
    if 'texlive-fonts-extra' in content:
        print("✅ fontawesome5 support: Available through texlive-fonts-extra")
    else:
        print("❌ fontawesome5 support: texlive-fonts-extra package missing")
        all_found = False
    
    return all_found

def verify_latexmk_arguments():
    """Verify correct latexmk arguments are used"""
    print("\n🔧 VERIFYING: Correct Latexmk Arguments")
    print("-" * 50)
    
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
    
    step_with = latex_step.get('with', {})
    args = step_with.get('args', '')
    
    print(f"   Current args: {args}")
    
    # Check for correct arguments and absence of problematic ones
    required_args = ['-interaction=nonstopmode', '-halt-on-error', '-shell-escape']
    problematic_args = ['-pdf']  # This was causing issues in previous versions
    
    all_correct = True
    
    for arg in required_args:
        if arg in args:
            print(f"✅ Required argument present: {arg}")
        else:
            print(f"❌ Missing required argument: {arg}")
            all_correct = False
    
    for arg in problematic_args:
        if arg in args:
            print(f"❌ Problematic argument found: {arg}")
            all_correct = False
        else:
            print(f"✅ Problematic argument avoided: {arg}")
    
    return all_correct

def verify_workflow_functionality():
    """Test that the workflow files pass basic validation"""
    print("\n🔧 VERIFYING: Workflow Functionality")
    print("-" * 50)
    
    # Test workflow structure
    try:
        result = subprocess.run(['python3', 'test_workflow_structure.py'], 
                              capture_output=True, text=True, cwd='.')
        if result.returncode == 0:
            print("✅ Workflow structure validation: PASSED")
        else:
            print("❌ Workflow structure validation: FAILED")
            print(f"   Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Workflow structure test error: {e}")
        return False
    
    # Test CTMM build system
    try:
        result = subprocess.run(['python3', 'ctmm_build.py'], 
                              capture_output=True, text=True, cwd='.')
        if result.returncode == 0:
            print("✅ CTMM build system: PASSED")
        else:
            print("❌ CTMM build system: FAILED")
            print(f"   Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ CTMM build system test error: {e}")
        return False
    
    return True

def main():
    """Run comprehensive validation for Issue #795 resolution"""
    print("🎯 ISSUE #795 RESOLUTION VALIDATION")
    print("GitHub Actions LaTeX Build Fixes - PR #552 Implementation")
    print("=" * 80)
    print()
    
    # List of PR #552 requirements to validate
    print("📋 PR #552 REQUIREMENTS:")
    print("  1. Fixed YAML syntax by properly quoting the 'on' keyword in workflow files")
    print("  2. Updated dante-ev/latex-action from v2.0.0 to @latest with correct latexmk arguments") 
    print("  3. Added comprehensive LaTeX package installation including German language support and fontawesome5")
    print()
    
    tests = [
        ("YAML syntax fixes", verify_yaml_syntax_fix),
        ("LaTeX action version update", verify_latex_action_update),
        ("LaTeX package installation", verify_latex_packages),
        ("Latexmk arguments", verify_latexmk_arguments),
        ("Workflow functionality", verify_workflow_functionality)
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
    
    print("\n" + "=" * 80)
    print("🏁 FINAL VALIDATION RESULTS")
    print("=" * 80)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\nOverall Status: {'🎉 SUCCESS' if all_passed else '❌ NEEDS ATTENTION'}")
    
    if all_passed:
        print("\n🎊 ISSUE #795 RESOLUTION: COMPLETE")
        print("✅ All PR #552 requirements have been successfully implemented")
        print("✅ GitHub Actions workflow should now build LaTeX PDFs without errors")
        print("✅ YAML syntax is correct")
        print("✅ LaTeX action uses @latest version") 
        print("✅ Comprehensive LaTeX packages are installed")
        print("✅ Correct compilation arguments are used")
        print("\nThe repository is ready for successful CI builds! 🚀")
    else:
        print("\n⚠️  Some issues still need to be addressed before the resolution is complete.")
    
    return all_passed

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)