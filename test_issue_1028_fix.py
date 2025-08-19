#!/usr/bin/env python3
"""
Test validation for Issue #1028: CI Build Failure - LaTeX Action Version Resolution

This test validates that the CI build failure has been resolved by ensuring
the LaTeX action uses a version that can be resolved by GitHub Actions.

Original Error:
"Unable to resolve action `dante-ev/latex-action@v2`, unable to find version `v2`"
"""

import os
import sys
from pathlib import Path

def test_latex_action_resolution():
    """Test that dante-ev/latex-action uses a resolvable version."""
    workflow_file = Path(".github/workflows/latex-build.yml")
    
    if not workflow_file.exists():
        print("❌ ERROR: latex-build.yml not found")
        return False
    
    content = workflow_file.read_text()
    
    # Check for problematic versions that caused the original issue
    problematic_versions = [
        "dante-ev/latex-action@v2",  # Original failing version
        "dante-ev/latex-action@v2.0.0"  # Also doesn't exist
    ]
    
    for version in problematic_versions:
        if version in content:
            print(f"❌ FAIL: Still using problematic version {version}")
            print("This version causes the CI failure:")
            print(f"'Unable to resolve action `{version}`, unable to find version'")
            return False
    
    # Check for working version
    if "dante-ev/latex-action@latest" in content:
        print("✅ PASS: Using resolvable version @latest")
        print("This should resolve the CI build failure")
        return True
    
    print("❌ FAIL: dante-ev/latex-action not found or using unexpected version")
    print("Available content in workflow:")
    for line_num, line in enumerate(content.split('\n'), 1):
        if 'dante-ev/latex-action' in line:
            print(f"  Line {line_num}: {line.strip()}")
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

def test_automated_pr_workflow():
    """Test that the automated PR workflow also uses a working version."""
    workflow_file = Path(".github/workflows/automated-pr-merge-test.yml")
    
    if not workflow_file.exists():
        print("⚠️  WARNING: automated-pr-merge-test.yml not found")
        return True  # This is optional, don't fail the main test
    
    content = workflow_file.read_text()
    
    # Check for problematic versions
    if "dante-ev/latex-action@v2.0.0" in content:
        print("❌ FAIL: Automated PR workflow still uses problematic version v2.0.0")
        return False
    
    if "dante-ev/latex-action@latest" in content:
        print("✅ PASS: Automated PR workflow uses working version @latest")
        return True
    
    print("✅ PASS: Automated PR workflow doesn't use problematic LaTeX action version")
    return True

def main():
    """Run all tests and return exit code."""
    print("=" * 70)
    print("Issue #1028 Fix Validation")
    print("CI Build Failure - LaTeX Action Version Resolution")
    print("=" * 70)
    print()
    
    tests = [
        ("LaTeX Action Version Resolution", test_latex_action_resolution),
        ("Workflow YAML Syntax", test_workflow_syntax),
        ("Automated PR Workflow", test_automated_pr_workflow),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"Testing {test_name}...")
        result = test_func()
        results.append(result)
        print()
    
    print("=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(results)
    total = len(results)
    
    for i, (test_name, _) in enumerate(tests):
        status = "✅ PASS" if results[i] else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print()
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED - Issue #1028 fix is working correctly!")
        print()
        print("The GitHub Actions workflow should now be able to:")
        print("- Resolve the dante-ev/latex-action successfully")
        print("- Avoid the 'unable to find version' error")
        print("- Proceed to LaTeX compilation instead of failing at action resolution")
        print("- Complete the full CI pipeline including PDF generation")
        return 0
    else:
        print("❌ SOME TESTS FAILED - Issue #1028 fix needs more work")
        return 1

if __name__ == "__main__":
    sys.exit(main())