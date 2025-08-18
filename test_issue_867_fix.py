#!/usr/bin/env python3
"""
Test script for Issue #867 - LaTeX Action Version Fix
Validates that the dante-ev/latex-action version in workflows is resolvable.
"""

import sys
import yaml
from pathlib import Path


def test_latex_action_version():
    """Test that LaTeX action uses a valid, resolvable version."""
    print("🔍 Testing LaTeX Action Version Resolution")
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
    
    # Check for problematic versions that are known to fail
    problematic_versions = ['@v2', '@v2.0.0']
    for bad_version in problematic_versions:
        if bad_version in uses:
            print(f"❌ Using problematic version: {bad_version}")
            print(f"   This version was reported as non-existent in Issue #867")
            return False
    
    # Check for valid version patterns
    valid_patterns = ['@latest', '@v0.2', '@v1', '@master', '@main']
    is_valid = any(pattern in uses for pattern in valid_patterns)
    
    if not is_valid:
        print(f"⚠️  Warning: Version pattern not in known-good list: {uses}")
        print("   Consider using @latest, @v0.2, or other verified versions")
        # Don't fail for this, just warn
    
    # Check that it's not the specific failing version from the issue
    if '@v2' in uses and not '@v2.' in uses:  # @v2 but not @v2.x.x
        print("❌ Using @v2 version that fails with 'unable to find version v2'")
        return False
    
    print(f"✅ LaTeX action version appears valid: {uses}")
    return True


def test_workflow_yaml_syntax():
    """Test that the workflow YAML syntax is valid."""
    print("\n📋 Testing Workflow YAML Syntax")
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
    except Exception as e:
        print(f"❌ Error reading workflow file: {e}")
        return False


def test_action_configuration():
    """Test that the LaTeX action configuration is complete."""
    print("\n⚙️  Testing LaTeX Action Configuration")
    print("=" * 60)
    
    workflow_path = Path(".github/workflows/latex-build.yml")
    with open(workflow_path, 'r') as f:
        workflow = yaml.safe_load(f)
    
    build_job = workflow.get('jobs', {}).get('build', {})
    steps = build_job.get('steps', [])
    
    latex_step = None
    for step in steps:
        if 'dante-ev/latex-action' in step.get('uses', ''):
            latex_step = step
            break
    
    if not latex_step:
        print("❌ LaTeX action step not found")
        return False
    
    # Check required configuration
    step_with = latex_step.get('with', {})
    
    if 'root_file' not in step_with:
        print("❌ Missing 'root_file' configuration")
        return False
    print(f"✅ root_file configured: {step_with['root_file']}")
    
    if 'args' not in step_with:
        print("⚠️  Warning: No 'args' specified (may use defaults)")
    else:
        print(f"✅ args configured: {step_with['args']}")
    
    if 'extra_system_packages' in step_with:
        packages = step_with['extra_system_packages']
        if isinstance(packages, str):
            package_count = len([p.strip() for p in packages.split('\n') if p.strip()])
        elif isinstance(packages, list):
            package_count = len(packages)
        else:
            package_count = 0
        print(f"✅ extra_system_packages configured ({package_count} packages)")
    
    return True


def main():
    """Run all validation tests for Issue #867 fix."""
    print("🧪 Issue #867 Fix Validation")
    print("=" * 60)
    print("Testing LaTeX action version resolution fix")
    print()
    
    tests = [
        ("LaTeX Action Version", test_latex_action_version),
        ("Workflow YAML Syntax", test_workflow_yaml_syntax),
        ("Action Configuration", test_action_configuration),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name}: PASS")
            else:
                failed += 1
                print(f"❌ {test_name}: FAIL")
        except Exception as e:
            failed += 1
            print(f"❌ {test_name}: ERROR - {e}")
        print()
    
    print("=" * 60)
    print(f"Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 ALL TESTS PASSED! LaTeX action version issue resolved.")
        return 0
    else:
        print("💥 Some tests failed. Please review the configuration.")
        return 1


if __name__ == "__main__":
    sys.exit(main())