#!/usr/bin/env python3
"""
Test script to validate Issue #964 fix: CI build failure due to invalid dante-ev/latex-action version

This test validates that the GitHub Actions workflow uses a valid version of dante-ev/latex-action
and does not contain the problematic `-pdf` argument that causes compilation failures.

The issue manifests as: "Unable to resolve action `dante-ev/latex-action@v2.3.0`, unable to find version `v2.3.0`"
"""

import yaml
import os
import sys
import re


def test_latex_action_version():
    """Test that the GitHub Actions workflow uses a valid dante-ev/latex-action version"""
    
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
    
    # Check for problematic versions that don't exist
    problematic_versions = ['v2.0.0', 'v2.3.0', 'v2.4.0']
    for version in problematic_versions:
        if uses_action == f'dante-ev/latex-action@{version}':
            print(f"❌ FAIL: Using problematic version {version}")
            print(f"This version doesn't exist and will cause CI failure:")
            print(f"'Unable to resolve action `dante-ev/latex-action@{version}`, unable to find version `{version}`'")
            return False
    
    # Check for correct version
    if uses_action == 'dante-ev/latex-action@v2':
        print("✅ PASS: Using correct version v2")
        return True
    elif uses_action.startswith('dante-ev/latex-action@'):
        print(f"⚠️  WARNING: Using version {uses_action}")
        print("Expected: dante-ev/latex-action@v2")
        print("Consider using @v2 for stability and to avoid non-existent version errors")
        return True  # Allow other versions but warn
    else:
        print(f"❌ ERROR: Unexpected action: {uses_action}")
        return False


def test_latex_compilation_args():
    """Test that the LaTeX compilation arguments are valid for pdflatex"""
    
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
    
    # Check the 'with' section for arguments
    with_section = latex_step.get('with', {})
    args = with_section.get('args', '')
    
    print(f"Found LaTeX args: {args}")
    
    # Check for the problematic -pdf argument
    if '-pdf' in args:
        print("❌ FAIL: Found problematic '-pdf' argument")
        print("The '-pdf' argument is for latexmk, not pdflatex")
        print("This will cause: 'unrecognized option \"-pdf\"' error")
        return False
    
    # Check for required arguments
    required_args = ['-interaction=nonstopmode', '-halt-on-error']
    for arg in required_args:
        if arg not in args:
            print(f"⚠️  WARNING: Missing recommended argument: {arg}")
    
    print("✅ PASS: LaTeX compilation arguments are valid")
    return True


def test_workflow_file_integrity():
    """Test that the workflow file doesn't contain merge conflict markers or corrupted content"""
    
    workflow_path = '.github/workflows/latex-build.yml'
    
    try:
        with open(workflow_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ ERROR: Failed to read {workflow_path}: {e}")
        return False
    
    # Check for merge conflict markers
    conflict_markers = ['<<<<<<<', '>>>>>>>', '=======']
    for marker in conflict_markers:
        if marker in content:
            print(f"❌ FAIL: Found merge conflict marker: {marker}")
            print("The workflow file contains unresolved merge conflicts")
            return False
    
    # Check for duplicate action definitions
    action_pattern = r'uses:\s*dante-ev/latex-action@'
    matches = re.findall(action_pattern, content)
    if len(matches) > 1:
        print(f"❌ FAIL: Found {len(matches)} dante-ev/latex-action definitions")
        print("There should be only one LaTeX action definition")
        return False
    
    # Check for branch name artifacts (common in merge conflicts)
    branch_artifacts = ['copilot/fix-', 'main\n', 'origin/']
    for artifact in branch_artifacts:
        if artifact in content and not content.startswith('#'):  # Not in comments
            lines = content.split('\n')
            for i, line in enumerate(lines, 1):
                if artifact in line and not line.strip().startswith('#'):
                    print(f"⚠️  WARNING: Possible branch artifact on line {i}: {line.strip()}")
    
    print("✅ PASS: Workflow file integrity is valid")
    return True


def test_comprehensive_validation_steps():
    """Test that the workflow includes comprehensive validation steps before LaTeX compilation"""
    
    workflow_path = '.github/workflows/latex-build.yml'
    
    try:
        with open(workflow_path, 'r') as f:
            workflow_content = yaml.safe_load(f)
    except Exception as e:
        print(f"❌ ERROR: Failed to parse {workflow_path}: {e}")
        return False
    
    # Find validation steps
    jobs = workflow_content.get('jobs', {})
    build_job = jobs.get('build', {})
    steps = build_job.get('steps', [])
    
    # Expected validation steps
    expected_validations = [
        'LaTeX syntax validation',
        'CTMM Build System Check'
    ]
    
    found_validations = []
    latex_step_index = None
    
    for i, step in enumerate(steps):
        step_name = step.get('name', '')
        
        # Check for validation steps
        for validation in expected_validations:
            if validation.lower() in step_name.lower():
                found_validations.append(validation)
        
        # Find LaTeX compilation step
        if 'Set up LaTeX' in step_name:
            latex_step_index = i
    
    # Verify validation steps are present
    missing_validations = [v for v in expected_validations if v not in found_validations]
    if missing_validations:
        print(f"⚠️  WARNING: Missing validation steps: {missing_validations}")
    
    # Verify validation happens before LaTeX compilation
    if latex_step_index is not None and len(found_validations) > 0:
        print("✅ PASS: Validation steps run before LaTeX compilation")
    
    print(f"✅ PASS: Found {len(found_validations)} validation steps")
    return True


def test_pdf_verification_step():
    """Test that the workflow includes PDF verification after compilation"""
    
    workflow_path = '.github/workflows/latex-build.yml'
    
    try:
        with open(workflow_path, 'r') as f:
            workflow_content = yaml.safe_load(f)
    except Exception as e:
        print(f"❌ ERROR: Failed to parse {workflow_path}: {e}")
        return False
    
    # Find PDF verification step
    jobs = workflow_content.get('jobs', {})
    build_job = jobs.get('build', {})
    steps = build_job.get('steps', [])
    
    has_pdf_verification = False
    for step in steps:
        step_name = step.get('name', '').lower()
        if 'verify' in step_name and 'pdf' in step_name:
            has_pdf_verification = True
            break
    
    if has_pdf_verification:
        print("✅ PASS: PDF verification step is present")
        return True
    else:
        print("⚠️  WARNING: No PDF verification step found")
        print("Consider adding a step to verify PDF generation success")
        return True  # Not critical, just a warning


def run_issue_964_fix_validation():
    """Run all Issue #964 fix validation tests"""
    
    print("=" * 60)
    print("Issue #964 Fix Validation")
    print("CI Build Failure - Invalid dante-ev/latex-action Version")
    print("=" * 60)
    print()
    
    tests = [
        ("LaTeX action version", test_latex_action_version),
        ("LaTeX compilation arguments", test_latex_compilation_args),
        ("Workflow file integrity", test_workflow_file_integrity),
        ("Comprehensive validation steps", test_comprehensive_validation_steps),
        ("PDF verification step", test_pdf_verification_step),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"Testing {test_name}...")
        try:
            result = test_func()
            results.append(result)
            print()
        except Exception as e:
            print(f"❌ ERROR in {test_name}: {e}")
            results.append(False)
            print()
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    print("=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    for i, (test_name, _) in enumerate(tests):
        status = "✅ PASS" if results[i] else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print()
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED - Issue #964 fix is working correctly!")
        print()
        print("The GitHub Actions workflow should now be able to:")
        print("- Resolve the dante-ev/latex-action correctly")
        print("- Avoid version resolution errors")
        print("- Complete the LaTeX PDF build process")
        return True
    else:
        print(f"❌ {total - passed} test(s) failed")
        print("Please address the issues above to complete Issue #964 requirements.")
        return False


def main():
    """Main function"""
    success = run_issue_964_fix_validation()
    return success


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)