#!/usr/bin/env python3
"""
Test script to validate Issue #825 fix: CI Build Failures Resolution
Verifies that the GitHub Actions workflow uses @latest and comprehensive LaTeX packages
"""

import yaml
import os
import sys

def test_dante_action_latest_version():
    """Test that the GitHub Actions workflow uses dante-ev/latex-action@latest"""
    
    workflow_path = '.github/workflows/latex-build.yml'
    
    if not os.path.exists(workflow_path):
        print(f"❌ ERROR: Workflow file {workflow_path} not found")
        return False
    
    try:
        with open(workflow_path, 'r') as f:
            workflow_content = yaml.safe_load(f)
    except Exception as e:
        print(f"❌ ERROR: Failed to parse {workflow_path}: {e}")
        return False
    
    # Find the LaTeX action step
    jobs = workflow_content.get('jobs', {})
    build_job = jobs.get('build', {})
    steps = build_job.get('steps', [])
    
    latex_step = None
    for step in steps:
        if step.get('name') == 'Set up LaTeX':
            latex_step = step
            break
    
    if not latex_step:
        print("❌ ERROR: 'Set up LaTeX' step not found in workflow")
        return False
    
    uses_action = latex_step.get('uses', '')
    
    print(f"Found LaTeX action: {uses_action}")
    
    # Check that it's using @latest version
    if uses_action == 'dante-ev/latex-action@latest':
        print("✅ PASS: Using latest version for improved stability")
        return True
    elif uses_action == 'dante-ev/latex-action@v2':
        print("❌ FAIL: Still using v2 instead of @latest")
        print("Expected: dante-ev/latex-action@latest")
        return False
    else:
        print(f"❌ ERROR: Unexpected action: {uses_action}")
        return False

def test_comprehensive_latex_packages():
    """Test that comprehensive LaTeX packages including fontawesome5 support are included"""
    
    workflow_path = '.github/workflows/latex-build.yml'
    
    try:
        with open(workflow_path, 'r') as f:
            workflow_content = yaml.safe_load(f)
    except Exception as e:
        print(f"❌ ERROR: Failed to parse {workflow_path}: {e}")
        return False
    
    # Find the LaTeX action step
    jobs = workflow_content.get('jobs', {})
    build_job = jobs.get('build', {})
    steps = build_job.get('steps', [])
    
    latex_step = None
    for step in steps:
        if step.get('name') == 'Set up LaTeX':
            latex_step = step
            break
    
    if not latex_step:
        print("❌ ERROR: 'Set up LaTeX' step not found in workflow")
        return False
    
    extra_packages = latex_step.get('with', {}).get('extra_system_packages', '')
    print(f"📋 Found LaTeX packages configuration:")
    for line in extra_packages.strip().split('\n'):
        if line.strip():
            print(f"   - {line.strip()}")
    
    # Essential packages validation including fontawesome5 support
    required_packages = [
        'texlive-lang-german',       # German language support
        'texlive-fonts-recommended', # Recommended fonts  
        'texlive-latex-recommended', # Recommended LaTeX packages
        'texlive-latex-extra',       # Extra LaTeX packages
        'texlive-fonts-extra',       # Extra fonts (includes fontawesome5)
        'texlive-science',           # Scientific packages
        'texlive-pstricks'           # PostScript tricks (contains pifont)
    ]
    
    # Additional packages for enhanced compatibility
    enhanced_packages = [
        'texlive-pictures',          # Picture-related packages
        'texlive-plain-generic'      # Plain TeX and generic packages
    ]
    
    all_passed = True
    
    print("\n🔍 Validating essential packages...")
    for pkg in required_packages:
        if pkg in extra_packages:
            print(f"✅ FOUND: {pkg}")
        else:
            print(f"❌ MISSING: {pkg}")
            all_passed = False
    
    print("\n🔍 Validating enhanced packages...")
    for pkg in enhanced_packages:
        if pkg in extra_packages:
            print(f"✅ FOUND: {pkg}")
        else:
            print(f"⚠️  MISSING: {pkg} (optional but recommended)")
    
    # Specific fontawesome5 validation
    print("\n🎯 Validating fontawesome5 package availability...")
    fontawesome_providers = ['texlive-fonts-extra']
    fontawesome_available = any(pkg in extra_packages for pkg in fontawesome_providers)
    
    if fontawesome_available:
        found_providers = [pkg for pkg in fontawesome_providers if pkg in extra_packages]
        print(f"✅ FONTAWESOME5 AVAILABLE: Found providers: {', '.join(found_providers)}")
    else:
        print("❌ FONTAWESOME5 MISSING: No packages found that provide fontawesome5")
        all_passed = False
    
    return all_passed

def test_workflow_syntax():
    """Test that the workflow file has valid syntax"""
    
    workflow_path = '.github/workflows/latex-build.yml'
    
    try:
        with open(workflow_path, 'r') as f:
            yaml.safe_load(f)
        print("✅ PASS: Workflow YAML syntax is valid")
        return True
    except yaml.YAMLError as e:
        print(f"❌ FAIL: Invalid YAML syntax: {e}")
        return False
    except Exception as e:
        print(f"❌ ERROR: Failed to read workflow file: {e}")
        return False

def main():
    """Run all tests for Issue #825 fix"""
    
    print("=" * 60)
    print("Issue #825 Fix Validation: CI Build Failures Resolution")
    print("=" * 60)
    
    tests = [
        ("dante-ev/latex-action version", test_dante_action_latest_version),
        ("Comprehensive LaTeX packages", test_comprehensive_latex_packages),
        ("Workflow YAML syntax", test_workflow_syntax)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\nTesting {test_name}...")
        result = test_func()
        results.append(result)
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    for i, (test_name, _) in enumerate(tests):
        status = "✅ PASS" if results[i] else "❌ FAIL"
        print(f"{status} {test_name}")
    
    passed = sum(results)
    total = len(results)
    
    print(f"\nTests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED - Issue #825 fix is working correctly!")
        print("\nThe GitHub Actions workflow should now:")
        print("- Use the latest dante-ev/latex-action for improved stability")
        print("- Have comprehensive LaTeX package support including fontawesome5")
        print("- Handle German language support and scientific packages")
        print("- Provide robust CI build capabilities")
    else:
        print("❌ SOME TESTS FAILED - Issue #825 fix needs attention")
    
    return passed == total

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)