#!/usr/bin/env python3
"""
Test for Issue #855 Fix: CI Build Failure - Invalid dante-ev/latex-action Version

This test validates that the latex-build.yml workflow uses a valid version
of dante-ev/latex-action that exists in the GitHub repository.
"""

import yaml
import re
from pathlib import Path

def test_latex_action_version():
    """Test that latex-build.yml uses a valid dante-ev/latex-action version."""
    print("🔧 Testing LaTeX Action Version Fix for Issue #855")
    print("=" * 60)
    
    workflow_path = Path(".github/workflows/latex-build.yml")
    if not workflow_path.exists():
        print("❌ latex-build.yml not found")
        return False
        
    with open(workflow_path, 'r') as f:
        content = f.read()
        workflow = yaml.safe_load(content)
    
    # Find LaTeX action usage
    latex_action_found = False
    latex_action_version = None
    
    build_job = workflow.get('jobs', {}).get('build', {})
    steps = build_job.get('steps', [])
    
    for step in steps:
        uses = step.get('uses', '')
        if 'dante-ev/latex-action' in uses:
            latex_action_found = True
            latex_action_version = uses
            break
    
    if not latex_action_found:
        print("❌ dante-ev/latex-action not found in workflow")
        return False
    
    print(f"✅ Found LaTeX action: {latex_action_version}")
    
    # Known valid versions for dante-ev/latex-action
    valid_versions = [
        'dante-ev/latex-action@v0.2.0',
        'dante-ev/latex-action@v0.1.0', 
        'dante-ev/latex-action@2025-A',
        'dante-ev/latex-action@2024-B',
        'dante-ev/latex-action@2024-A',
        'dante-ev/latex-action@2023-A'
    ]
    
    # Check for problematic versions
    problematic_patterns = [
        r'dante-ev/latex-action@v2$',         # @v2 without patch version
        r'dante-ev/latex-action@v2\.',        # @v2.x.x (doesn't exist)
        r'dante-ev/latex-action@latest$'      # @latest (unpinned)
    ]
    
    for pattern in problematic_patterns:
        if re.search(pattern, latex_action_version):
            print(f"❌ Problematic version pattern detected: {latex_action_version}")
            print(f"   Pattern: {pattern}")
            return False
    
    # Check if version is in known valid list
    if latex_action_version in valid_versions:
        print(f"✅ Using valid version: {latex_action_version}")
        print("✅ Version exists in dante-ev/latex-action repository")
        return True
    else:
        print(f"⚠️  Version not in known valid list: {latex_action_version}")
        print("   Known valid versions:")
        for v in valid_versions:
            print(f"     - {v}")
        return False

def test_workflow_syntax():
    """Test that the workflow file has valid YAML syntax."""
    print("\n🔧 Testing Workflow YAML Syntax")
    print("=" * 60)
    
    workflow_path = Path(".github/workflows/latex-build.yml")
    
    try:
        with open(workflow_path, 'r') as f:
            yaml.safe_load(f)
        print("✅ YAML syntax is valid")
        return True
    except yaml.YAMLError as e:
        print(f"❌ YAML syntax error: {e}")
        return False

def main():
    """Run all tests for Issue #855 fix."""
    print("🧪 Issue #855 Fix Validation")
    print("Testing CI build failure fix for dante-ev/latex-action version")
    print("=" * 80)
    
    tests = [
        ("LaTeX Action Version", test_latex_action_version),
        ("Workflow YAML Syntax", test_workflow_syntax),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 Running: {test_name}")
        result = test_func()
        results.append((test_name, result))
        print(f"{'✅ PASS' if result else '❌ FAIL'}: {test_name}")
    
    print("\n" + "=" * 80)
    print("ISSUE #855 FIX VALIDATION SUMMARY")
    print("=" * 80)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Issue #855 fix is validated.")
        return True
    else:
        print("❌ SOME TESTS FAILED! Issue #855 fix needs attention.")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)