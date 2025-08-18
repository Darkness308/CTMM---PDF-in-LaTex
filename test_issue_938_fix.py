#!/usr/bin/env python3
"""
Test script to validate the comprehensive GitHub Actions CI fixes for Issue #938.
Verifies LaTeX build configuration, package dependencies, and workflow syntax.
"""

import yaml
import subprocess
import sys
import os
from pathlib import Path

def test_fontawesome_package_dependency():
    """Test that the fontawesome package dependency is properly configured."""
    print("\n🎨 Testing FontAwesome Package Dependencies")
    print("=" * 60)
    
    workflow_path = Path('.github/workflows/latex-build.yml')
    if not workflow_path.exists():
        print("❌ FAILED: latex-build.yml not found")
        return False
    
    try:
        with open(workflow_path, 'r') as f:
            workflow = yaml.safe_load(f)
        
        # Check if fontawesome package is included
        latex_step = None
        for step in workflow['jobs']['build']['steps']:
            if 'dante-ev/latex-action' in step.get('uses', ''):
                latex_step = step
                break
        
        if not latex_step:
            print("❌ FAILED: dante-ev/latex-action step not found")
            return False
        
        packages = latex_step.get('with', {}).get('extra_system_packages', '')
        
        # Check for fontawesome package
        if 'fonts-fork-awesome' in packages:
            print("✅ PASS: fonts-fork-awesome package found in workflow")
        else:
            print("❌ FAILED: fonts-fork-awesome package missing from workflow")
            return False
        
        # Check for German language support
        if 'texlive-lang-german' in packages:
            print("✅ PASS: German language support (texlive-lang-german) found")
        else:
            print("❌ FAILED: German language support missing")
            return False
        
        # Check for essential packages
        essential_packages = [
            'texlive-fonts-extra',
            'texlive-latex-extra', 
            'texlive-pstricks'
        ]
        
        for package in essential_packages:
            if package in packages:
                print(f"✅ PASS: Essential package {package} found")
            else:
                print(f"❌ FAILED: Essential package {package} missing")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ FAILED: Error reading workflow: {e}")
        return False

def test_latex_arguments_correctness():
    """Test that LaTeX compilation arguments are correct."""
    print("\n🔧 Testing LaTeX Compilation Arguments")
    print("=" * 60)
    
    workflow_path = Path('.github/workflows/latex-build.yml')
    
    try:
        with open(workflow_path, 'r') as f:
            workflow = yaml.safe_load(f)
        
        # Find LaTeX action step
        latex_step = None
        for step in workflow['jobs']['build']['steps']:
            if 'dante-ev/latex-action' in step.get('uses', ''):
                latex_step = step
                break
        
        if not latex_step:
            print("❌ FAILED: LaTeX action step not found")
            return False
        
        args = latex_step.get('with', {}).get('args', '')
        
        # Check for correct arguments
        required_args = [
            '-interaction=nonstopmode',
            '-halt-on-error',
            '-shell-escape'
        ]
        
        for arg in required_args:
            if arg in args:
                print(f"✅ PASS: Required argument {arg} found")
            else:
                print(f"❌ FAILED: Required argument {arg} missing")
                return False
        
        # Check that problematic -pdf argument is not present
        if '-pdf' in args:
            print("❌ FAILED: Problematic -pdf argument found (should be removed)")
            return False
        else:
            print("✅ PASS: No problematic -pdf argument found")
        
        return True
        
    except Exception as e:
        print(f"❌ FAILED: Error checking arguments: {e}")
        return False

def test_workflow_yaml_syntax():
    """Test that all workflow files have correct YAML syntax."""
    print("\n📝 Testing Workflow YAML Syntax")
    print("=" * 60)
    
    workflow_files = [
        '.github/workflows/latex-build.yml',
        '.github/workflows/latex-validation.yml',
        '.github/workflows/static.yml'
    ]
    
    all_valid = True
    for workflow_file in workflow_files:
        workflow_path = Path(workflow_file)
        if not workflow_path.exists():
            print(f"⚠️  Workflow file not found: {workflow_file}")
            continue
            
        try:
            with open(workflow_path, 'r') as f:
                content = f.read()
                workflow = yaml.safe_load(content)
            
            # Check for quoted 'on:' syntax (Issue #458)
            if '"on":' in content:
                print(f"✅ {workflow_file}: Proper quoted 'on:' syntax")
            elif 'on:' in content:
                print(f"⚠️  {workflow_file}: Unquoted 'on:' syntax - potential issue")
            
            # Check basic structure
            required_keys = ['name', 'jobs']
            on_key_exists = 'on' in workflow or '"on"' in content
            
            if not on_key_exists:
                print(f"❌ {workflow_file}: Missing 'on:' trigger configuration")
                all_valid = False
            
            for key in required_keys:
                if key not in workflow:
                    print(f"❌ {workflow_file}: Missing required key '{key}'")
                    all_valid = False
                    
        except yaml.YAMLError as e:
            print(f"❌ {workflow_file}: YAML syntax error: {e}")
            all_valid = False
        except Exception as e:
            print(f"❌ {workflow_file}: Error reading file: {e}")
            all_valid = False
    
    return all_valid

def test_fontawesome_usage_in_project():
    """Test that FontAwesome usage in project is consistent."""
    print("\n🎯 Testing FontAwesome Usage in Project")
    print("=" * 60)
    
    # Check that main.tex loads fontawesome5
    main_tex_path = Path('main.tex')
    if not main_tex_path.exists():
        print("❌ FAILED: main.tex not found")
        return False
    
    try:
        with open(main_tex_path, 'r') as f:
            content = f.read()
        
        if '\\usepackage{fontawesome5}' in content:
            print("✅ PASS: fontawesome5 package loaded in main.tex")
        else:
            print("❌ FAILED: fontawesome5 package not loaded in main.tex")
            return False
        
        # Check for FontAwesome usage in modules
        fa_usage_count = content.count('\\fa')
        if fa_usage_count > 0:
            print(f"✅ PASS: FontAwesome icons used {fa_usage_count} times in main.tex")
        
        # Check modules for FontAwesome usage
        modules_path = Path('modules')
        if modules_path.exists():
            total_fa_usage = 0
            for module_file in modules_path.glob('*.tex'):
                try:
                    with open(module_file, 'r') as f:
                        module_content = f.read()
                    fa_count = module_content.count('\\fa')
                    total_fa_usage += fa_count
                except Exception:
                    continue
            
            print(f"✅ PASS: FontAwesome icons used {total_fa_usage} times across all modules")
            if total_fa_usage > 50:  # Threshold based on grep results showing extensive usage
                print("✅ PASS: Extensive FontAwesome usage detected - package dependency critical")
        
        return True
        
    except Exception as e:
        print(f"❌ FAILED: Error checking FontAwesome usage: {e}")
        return False

def test_build_system_robustness():
    """Test that the build system has proper error handling."""
    print("\n🛠️  Testing Build System Robustness")
    print("=" * 60)
    
    # Test that ctmm_build.py executes successfully
    try:
        result = subprocess.run([
            'python3', 'ctmm_build.py'
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✅ PASS: ctmm_build.py executes successfully")
            
            # Check for pdflatex availability handling
            if "pdflatex not found" in result.stdout and "skipping LaTeX compilation test" in result.stdout:
                print("✅ PASS: Build system gracefully handles missing pdflatex")
            elif "pdflatex not found" not in result.stdout:
                print("✅ PASS: pdflatex available and working")
            
            # Check for validation passes
            if "LaTeX validation: ✓ PASS" in result.stdout:
                print("✅ PASS: LaTeX validation successful")
            
            if "Basic build: ✓ PASS" in result.stdout:
                print("✅ PASS: Basic build test successful")
            
            return True
        else:
            print(f"❌ FAILED: ctmm_build.py failed with return code {result.returncode}")
            print(f"Error output: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ FAILED: Error running build system: {e}")
        return False

def main():
    """Main test function."""
    print("=" * 70)
    print("ISSUE #938 VALIDATION: Comprehensive CI LaTeX Build Fixes")
    print("=" * 70)
    
    tests = [
        ("FontAwesome Package Dependencies", test_fontawesome_package_dependency),
        ("LaTeX Compilation Arguments", test_latex_arguments_correctness),
        ("Workflow YAML Syntax", test_workflow_yaml_syntax),
        ("FontAwesome Usage Consistency", test_fontawesome_usage_in_project),
        ("Build System Robustness", test_build_system_robustness)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running: {test_name}")
        try:
            if test_func():
                print(f"✅ PASS: {test_name}")
                passed += 1
            else:
                print(f"❌ FAIL: {test_name}")
        except Exception as e:
            print(f"❌ ERROR in {test_name}: {e}")
    
    print("\n" + "=" * 70)
    print("VALIDATION SUMMARY")
    print("=" * 70)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Issue #938 fixes are properly implemented.")
        print("\nThe comprehensive GitHub Actions CI fixes include:")
        print("✓ FontAwesome package dependency (fonts-fork-awesome)")
        print("✓ Correct LaTeX compilation arguments")
        print("✓ Proper YAML syntax in all workflows") 
        print("✓ Robust build system with error handling")
        print("✓ German language support maintained")
        return True
    else:
        print(f"❌ {total - passed} test(s) failed. Please review the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)