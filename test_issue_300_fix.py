#!/usr/bin/env python3
"""
Test script for Issue #300: Fix missing LaTeX packages and dante-ev/latex-action version.
This validates that the GitHub Actions workflows use the correct action version and include required packages.
"""

import os
import re
import sys

def test_workflow_action_versions():
    """Test that both workflow files use the correct dante-ev/latex-action version."""
    print("\n🔍 Testing workflow action versions...")
    
    issues_found = []
    fixes_verified = []
    
    workflow_files = [
        '.github/workflows/latex-build.yml',
        '.github/workflows/automated-pr-merge-test.yml'
    ]
    
    expected_version = "v0.2.0"
    problematic_version = "v2.3.0"
    
    for workflow_file in workflow_files:
        if not os.path.exists(workflow_file):
            issues_found.append(f"❌ Workflow file missing: {workflow_file}")
            continue
            
        with open(workflow_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for problematic version
        if f"dante-ev/latex-action@{problematic_version}" in content:
            issues_found.append(f"❌ Found problematic version {problematic_version} in {workflow_file}")
        else:
            fixes_verified.append(f"✅ No problematic version {problematic_version} found in {workflow_file}")
        
        # Check for correct version
        if f"dante-ev/latex-action@{expected_version}" in content:
            fixes_verified.append(f"✅ Found correct version {expected_version} in {workflow_file}")
        else:
            issues_found.append(f"❌ Expected version {expected_version} not found in {workflow_file}")
    
    return issues_found, fixes_verified

def test_latex_packages():
    """Test that required LaTeX packages are included in workflows."""
    print("\n📦 Testing LaTeX package dependencies...")
    
    required_packages = [
        'texlive-lang-german',
        'texlive-fonts-recommended',
        'texlive-latex-recommended', 
        'texlive-fonts-extra',  # Critical for fontawesome5
        'texlive-latex-extra',
        'texlive-science',
        'texlive-pstricks'
    ]
    
    workflow_files = [
        '.github/workflows/latex-build.yml',
        '.github/workflows/automated-pr-merge-test.yml'
    ]
    
    issues_found = []
    fixes_verified = []
    
    for workflow_file in workflow_files:
        if not os.path.exists(workflow_file):
            issues_found.append(f"❌ Workflow file missing: {workflow_file}")
            continue
            
        with open(workflow_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        for package in required_packages:
            if package in content:
                if package == 'texlive-fonts-extra':
                    fixes_verified.append(f"✅ CRITICAL: {package} found in {workflow_file} (fixes fontawesome5)")
                else:
                    fixes_verified.append(f"✅ Required package {package} found in {workflow_file}")
            else:
                issues_found.append(f"❌ Required package {package} missing from {workflow_file}")
    
    return issues_found, fixes_verified

def test_troubleshooting_documentation():
    """Test that troubleshooting documentation is updated."""
    print("\n📚 Testing troubleshooting documentation...")
    
    issues_found = []
    fixes_verified = []
    
    doc_file = "BUILD_TROUBLESHOOTING.md"
    
    if not os.path.exists(doc_file):
        issues_found.append(f"❌ Documentation file missing: {doc_file}")
        return issues_found, fixes_verified
        
    with open(doc_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for fontawesome5 troubleshooting
    if "fontawesome5.sty" in content:
        fixes_verified.append("✅ Troubleshooting includes fontawesome5.sty guidance")
    else:
        issues_found.append("❌ Missing fontawesome5.sty troubleshooting guidance")
    
    # Check for texlive-fonts-extra solution
    if "texlive-fonts-extra" in content:
        fixes_verified.append("✅ Troubleshooting includes texlive-fonts-extra solution")
    else:
        issues_found.append("❌ Missing texlive-fonts-extra solution in troubleshooting")
    
    # Check for correct action version in examples
    if "dante-ev/latex-action@v0.2.0" in content:
        fixes_verified.append("✅ Documentation uses correct action version v0.2.0")
    else:
        issues_found.append("❌ Documentation doesn't show correct action version")
    
    # Check for problematic version
    if "dante-ev/latex-action@v2.3.0" in content:
        issues_found.append("❌ Documentation still shows problematic version v2.3.0")
    else:
        fixes_verified.append("✅ No problematic version v2.3.0 in documentation")
    
    return issues_found, fixes_verified

def main():
    """Main test function."""
    print("=" * 60)
    print("🧪 ISSUE #300 FIX VALIDATION")
    print("=" * 60)
    print("Testing fixes for missing LaTeX packages and workflow configuration...")
    
    all_issues = []
    all_fixes = []
    
    # Test 1: Workflow action versions
    issues, fixes = test_workflow_action_versions()
    all_issues.extend(issues)
    all_fixes.extend(fixes)
    
    # Test 2: LaTeX packages
    issues, fixes = test_latex_packages()
    all_issues.extend(issues)
    all_fixes.extend(fixes)
    
    # Test 3: Documentation
    issues, fixes = test_troubleshooting_documentation()
    all_issues.extend(issues)
    all_fixes.extend(fixes)
    
    # Print results
    print("\n" + "=" * 60)
    print("📋 VALIDATION RESULTS")
    print("=" * 60)
    
    if all_fixes:
        print("\n✅ FIXES VERIFIED:")
        for fix in all_fixes:
            print(f"   {fix}")
    
    if all_issues:
        print("\n❌ ISSUES FOUND:")
        for issue in all_issues:
            print(f"   {issue}")
        print(f"\n❌ VALIDATION FAILED: {len(all_issues)} issues found")
        return 1
    else:
        print(f"\n🎉 VALIDATION SUCCESSFUL: All {len(all_fixes)} checks passed!")
        print("\n✅ Issue #300 fixes are working correctly:")
        print("   • dante-ev/latex-action version corrected to v0.2.0")
        print("   • texlive-fonts-extra included for fontawesome5 support")
        print("   • Troubleshooting documentation is up to date")
        return 0

if __name__ == "__main__":
    sys.exit(main())