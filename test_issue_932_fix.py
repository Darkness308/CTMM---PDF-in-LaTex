#!/usr/bin/env python3
"""
Test validation for Issue #932: CI Build Failure - LaTeX Action Version Fix

This test validates that the problematic dante-ev/latex-action versions
(v2.0.0 and v2) have been replaced with the correct @latest version that exists.
"""

import os
import sys
from pathlib import Path

def test_latex_action_version_fix():
    """Test that dante-ev/latex-action uses correct version @latest."""
    workflow_file = Path(".github/workflows/latex-build.yml")
    
    if not workflow_file.exists():
        print("❌ ERROR: latex-build.yml not found")
        return False
    
    content = workflow_file.read_text()
    
    # Check for problematic versions that don't exist
    problematic_versions = ["dante-ev/latex-action@v2.0.0", "dante-ev/latex-action@v2"]
    for version in problematic_versions:
        if version in content:
            print(f"❌ FAIL: Still using problematic version {version.split('@')[1]}")
            print("This version doesn't exist and causes CI failure:")
            print(f"'Unable to resolve action `{version}`, unable to find version `{version.split('@')[1]}`'")
            return False
    
    # Check for the correct version
    if "dante-ev/latex-action@latest" in content:
        print("✅ PASS: Using correct version @latest")
        return True
    
    print("❌ FAIL: dante-ev/latex-action not found or using unexpected version")
    return False

def test_workflow_syntax():
    """Test that the workflow YAML syntax is valid."""
    try:
        import yaml
        workflow_file = Path(".github/workflows/latex-build.yml")
        content = workflow_file.read_text()
        yaml.safe_load(content)
        print("✅ PASS: Workflow YAML syntax is valid")
        return True
    except Exception as e:
        print(f"❌ FAIL: Workflow YAML syntax error: {e}")
        return False

def main():
    """Run all tests and return exit code."""
    print("=" * 60)
    print("Issue #932 Fix Validation")
    print("CI Build Failure - LaTeX Action Version Fix")
    print("=" * 60)
    print()
    
    tests = [
        ("dante-ev/latex-action version", test_latex_action_version_fix),
        ("Workflow YAML syntax", test_workflow_syntax),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"Testing {test_name}...")
        result = test_func()
        results.append(result)
        print()
    
    print("=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    for i, (test_name, _) in enumerate(tests):
        status = "✅ PASS" if results[i] else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print()
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED - Issue #932 fix is working correctly!")
        print()
        print("The GitHub Actions workflow should now be able to:")
        print("- Resolve the dante-ev/latex-action@latest action successfully")
        print("- Avoid version resolution errors by using the stable @latest tag")
        print("- Complete the LaTeX PDF build process")
        return 0
    else:
        print("❌ SOME TESTS FAILED - Issue #932 fix needs more work")
        return 1

if __name__ == "__main__":
    sys.exit(main())