#!/usr/bin/env python3
"""
Test script for Issue #882 - CI LaTeX Build Failure Fix
Validates the comprehensive fix for GitHub Actions LaTeX build failures.
"""

import sys
import yaml
from pathlib import Path


def test_latex_action_version_fix():
    """Test that LaTeX action uses a working version instead of problematic @v2."""
    print("🔧 Testing LaTeX Action Version Fix")
    print("=" * 60)
    
    workflow_path = Path(".github/workflows/latex-build.yml")
    if not workflow_path.exists():
        print("❌ latex-build.yml not found")
        return False
        
    with open(workflow_path, 'r') as f:
        workflow = yaml.safe_load(f)
    
    build_job = workflow.get('jobs', {}).get('build', {})
    steps = build_job.get('steps', [])
    
    latex_step = None
    for step in steps:
        uses = step.get('uses', '')
        if 'dante-ev/latex-action' in uses:
            latex_step = step
            break
    
    if not latex_step:
        print("❌ dante-ev/latex-action step not found")
        return False
    
    uses = latex_step.get('uses', '')
    print(f"✅ Found LaTeX action: {uses}")
    
    # Check that we're not using the problematic @v2 version
    if '@v2' in uses and not '@v2.' in uses:  # @v2 but not @v2.x.x
        print("❌ Still using problematic @v2 version")
        return False
    
    # Check for valid working versions
    working_versions = ['@latest', '@v0.2', '@v1', '@master', '@main']
    is_working = any(version in uses for version in working_versions)
    
    if not is_working:
        print(f"⚠️  Warning: Using version that may not be tested: {uses}")
        print("   Known working versions: @latest, @v0.2, @v1, @master, @main")
        return False
    
    print(f"✅ LaTeX action version is working: {uses}")
    return True


def test_comprehensive_package_dependencies():
    """Test that all required LaTeX packages are present for German language support."""
    print("\n📦 Testing Comprehensive Package Dependencies")
    print("=" * 60)
    
    workflow_path = Path(".github/workflows/latex-build.yml")
    with open(workflow_path, 'r') as f:
        content = f.read()
    
    # Essential packages for CTMM system
    required_packages = [
        'texlive-lang-german',     # German language support
        'texlive-fonts-recommended', # Core fonts
        'texlive-latex-recommended', # Core LaTeX packages
        'texlive-fonts-extra',     # Extended fonts
        'texlive-latex-extra',     # Extended LaTeX packages
        'texlive-science',         # Math/science packages
        'texlive-pstricks',        # Contains pifont for checkboxes
    ]
    
    missing_packages = []
    for package in required_packages:
        if package in content:
            print(f"✅ Found required package: {package}")
        else:
            missing_packages.append(package)
            print(f"❌ Missing required package: {package}")
    
    if missing_packages:
        print(f"❌ Missing {len(missing_packages)} essential packages")
        return False
    
    print(f"✅ All {len(required_packages)} required packages present")
    return True


def test_yaml_syntax_compliance():
    """Test that all workflow files have proper YAML syntax."""
    print("\n📋 Testing YAML Syntax Compliance")
    print("=" * 60)
    
    workflow_files = [
        ".github/workflows/latex-build.yml",
        ".github/workflows/latex-validation.yml", 
        ".github/workflows/static.yml"
    ]
    
    all_valid = True
    for workflow_file in workflow_files:
        workflow_path = Path(workflow_file)
        if not workflow_path.exists():
            print(f"⚠️  {workflow_file} not found (optional)")
            continue
            
        try:
            with open(workflow_path, 'r') as f:
                workflow = yaml.safe_load(f)
            
            # Check that 'on' is properly quoted
            if 'on' not in workflow:
                print(f"❌ {workflow_file}: Missing 'on' trigger configuration")
                all_valid = False
                continue
                
            print(f"✅ {workflow_file}: Valid YAML syntax with proper 'on' trigger")
            
        except yaml.YAMLError as e:
            print(f"❌ {workflow_file}: YAML syntax error - {e}")
            all_valid = False
    
    return all_valid


def test_build_system_robustness():
    """Test that build system gracefully handles missing LaTeX installation."""
    print("\n🏗️  Testing Build System Robustness")
    print("=" * 60)
    
    import subprocess
    
    try:
        # Test that ctmm_build.py works without LaTeX
        result = subprocess.run(['python3', 'ctmm_build.py'], 
                              capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✅ ctmm_build.py executes successfully without LaTeX")
            
            # Check for graceful LaTeX handling
            if "pdflatex not found" in result.stdout and "PASS" in result.stdout:
                print("✅ Build system gracefully handles missing LaTeX")
                return True
            elif "pdflatex not found" not in result.stdout:
                print("✅ Build system works (LaTeX may be available)")
                return True
            else:
                print("❌ Build system doesn't handle missing LaTeX gracefully")
                return False
        else:
            print(f"❌ ctmm_build.py failed with exit code {result.returncode}")
            print(f"STDERR: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ ctmm_build.py timed out")
        return False
    except Exception as e:
        print(f"❌ Error testing build system: {e}")
        return False


def test_no_invalid_arguments():
    """Test that no invalid LaTeX arguments are present."""
    print("\n⚙️  Testing LaTeX Arguments")
    print("=" * 60)
    
    workflow_path = Path(".github/workflows/latex-build.yml")
    with open(workflow_path, 'r') as f:
        content = f.read()
    
    # Check for invalid arguments that have caused issues before
    invalid_args = ['-pdf']  # Issue #702: -pdf is invalid for pdflatex
    
    found_invalid = []
    for arg in invalid_args:
        if arg in content:
            found_invalid.append(arg)
            print(f"❌ Found invalid argument: {arg}")
    
    if found_invalid:
        print(f"❌ Found {len(found_invalid)} invalid arguments")
        return False
    
    # Check for required arguments
    required_args = ['-interaction=nonstopmode', '-halt-on-error', '-shell-escape']
    missing_args = []
    
    for arg in required_args:
        if arg in content:
            print(f"✅ Found required argument: {arg}")
        else:
            missing_args.append(arg)
            print(f"❌ Missing required argument: {arg}")
    
    if missing_args:
        print(f"❌ Missing {len(missing_args)} required arguments")
        return False
    
    print("✅ All LaTeX arguments are valid and complete")
    return True


def main():
    """Run all validation tests for Issue #882 fix."""
    print("🧪 Issue #882 Fix Validation")
    print("=" * 70)
    print("Testing comprehensive CI LaTeX build failure fix")
    print("=" * 70)
    
    tests = [
        ("LaTeX Action Version Fix", test_latex_action_version_fix),
        ("Comprehensive Package Dependencies", test_comprehensive_package_dependencies),
        ("YAML Syntax Compliance", test_yaml_syntax_compliance),
        ("Build System Robustness", test_build_system_robustness),
        ("LaTeX Arguments Validation", test_no_invalid_arguments),
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name}: Test failed with exception: {e}")
            results[test_name] = False
    
    print("\n" + "=" * 70)
    print("Test Results Summary")
    print("=" * 70)
    
    passed = 0
    failed = 0
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print(f"\nTests passed: {passed}, failed: {failed}")
    
    if failed == 0:
        print("🎉 ALL TESTS PASSED! Issue #882 fix validated successfully.")
        print("\nThe CI LaTeX build failures should now be resolved:")
        print("✓ LaTeX action version fixed from problematic @v2 to working version")
        print("✓ Comprehensive LaTeX package dependencies ensured")
        print("✓ YAML syntax compliance verified")
        print("✓ Build system robustness confirmed")
        print("✓ Invalid LaTeX arguments removed")
        return True
    else:
        print("💥 Some tests failed. Please review the configuration.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)