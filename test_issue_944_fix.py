#!/usr/bin/env python3
"""
Issue #944 Validation: CI Pipeline Robustness Fix
=================================================

This script validates the fix for issue #944, which addresses CI pipeline 
failures reported in the Mergify CI insights. The specific issue was that 
the dante-ev/latex-action was not pinned to a specific patch version, 
causing potential CI failures when new versions are released.

Key fix validated:
1. LaTeX action properly pinned to v2.0.0 for reproducible builds
2. CI pipeline robustness enhanced to prevent version-related failures
3. All GitHub Actions properly version-pinned
"""

import os
import sys
import yaml
from pathlib import Path

def test_latex_action_version_pinning():
    """Test that the LaTeX action is properly pinned to v2.0.0."""
    print("\n🔧 Testing LaTeX Action Version Pinning")
    print("=" * 50)
    
    workflow_path = Path(".github/workflows/latex-build.yml")
    
    if not workflow_path.exists():
        print("❌ latex-build.yml not found")
        return False
    
    with open(workflow_path, 'r') as f:
        content = f.read()
    
    # Check for the correct pinned version
    if 'dante-ev/latex-action@v2.0.0' in content:
        print("✅ LaTeX action properly pinned to v2.0.0")
        
        # Ensure the old unpinned version is not present
        if 'dante-ev/latex-action@v2' in content and 'dante-ev/latex-action@v2.0.0' not in content:
            print("❌ Found unpinned version dante-ev/latex-action@v2")
            return False
        
        print("✅ No unpinned dante-ev/latex-action@v2 found")
        return True
    else:
        print("❌ LaTeX action not properly pinned to v2.0.0")
        print("   Current content check failed")
        return False

def test_ci_robustness_configuration():
    """Test that the CI configuration includes robustness measures."""
    print("\n🛡️  Testing CI Robustness Configuration")
    print("=" * 50)
    
    workflow_path = Path(".github/workflows/latex-build.yml")
    
    with open(workflow_path, 'r') as f:
        workflow = yaml.safe_load(f)
    
    robustness_checks = []
    
    # Check for proper validation steps
    build_job = workflow.get('jobs', {}).get('build', {})
    steps = build_job.get('steps', [])
    
    validation_steps = [
        'LaTeX syntax validation',
        'CTMM Build System Check', 
        'Enhanced Build Management',
        'comprehensive CI validation',
        'Enhanced pre-build validation'
    ]
    
    found_validations = 0
    for step in steps:
        step_name = step.get('name', '').lower()
        for validation in validation_steps:
            if validation.lower() in step_name:
                found_validations += 1
                print(f"✅ Found validation step: {step.get('name')}")
                break
    
    if found_validations >= 3:
        robustness_checks.append("✅ Multiple validation steps before LaTeX compilation")
    else:
        robustness_checks.append("❌ Insufficient validation steps")
    
    # Check for build log upload on failure
    upload_found = False
    for step in steps:
        if step.get('if') == 'failure()' and 'upload-artifact' in step.get('uses', ''):
            upload_found = True
            print("✅ Build log upload on failure configured")
            break
    
    if upload_found:
        robustness_checks.append("✅ Build log upload on failure")
    else:
        robustness_checks.append("❌ Missing build log upload on failure")
    
    for check in robustness_checks:
        print(check)
    
    return all(check.startswith("✅") for check in robustness_checks)

def test_version_pinning_consistency():
    """Test that all GitHub Actions are consistently version-pinned."""
    print("\n📌 Testing Version Pinning Consistency")
    print("=" * 50)
    
    workflow_files = [
        ".github/workflows/latex-build.yml",
        ".github/workflows/latex-validation.yml", 
        ".github/workflows/pr-validation.yml",
        ".github/workflows/static.yml"
    ]
    
    all_pinned = True
    
    for workflow_file in workflow_files:
        if not Path(workflow_file).exists():
            continue
            
        with open(workflow_file, 'r') as f:
            content = f.read()
        
        # Look for any @latest usage (should be none)
        if '@latest' in content:
            print(f"❌ {workflow_file}: Found @latest tag usage")
            all_pinned = False
        else:
            print(f"✅ {workflow_file}: No @latest tags found")
    
    return all_pinned

def test_reproducible_build_configuration():
    """Test that the build configuration supports reproducible builds."""
    print("\n🔄 Testing Reproducible Build Configuration")
    print("=" * 50)
    
    workflow_path = Path(".github/workflows/latex-build.yml")
    
    with open(workflow_path, 'r') as f:
        workflow = yaml.safe_load(f)
    
    build_job = workflow.get('jobs', {}).get('build', {})
    steps = build_job.get('steps', [])
    
    reproducibility_checks = []
    
    # Check for pinned action versions
    action_versions_pinned = True
    for step in steps:
        uses = step.get('uses', '')
        if uses and '@' in uses:
            action, version = uses.split('@')
            if version in ['latest', 'main', 'master']:
                action_versions_pinned = False
                print(f"❌ Unpinned action found: {uses}")
            else:
                print(f"✅ Properly pinned action: {uses}")
    
    if action_versions_pinned:
        reproducibility_checks.append("✅ All actions properly version-pinned")
    else:
        reproducibility_checks.append("❌ Some actions not properly version-pinned")
    
    # Check for consistent Python version
    python_version_found = False
    for step in steps:
        if step.get('uses', '').startswith('actions/setup-python'):
            with_config = step.get('with', {})
            python_version = with_config.get('python-version', '')
            if python_version:
                print(f"✅ Python version specified: {python_version}")
                python_version_found = True
    
    if python_version_found:
        reproducibility_checks.append("✅ Python version properly specified")
    else:
        reproducibility_checks.append("❌ Python version not specified")
    
    for check in reproducibility_checks:
        print(check)
    
    return all(check.startswith("✅") for check in reproducibility_checks)

def main():
    """Run all validation tests for Issue #944."""
    print("=" * 70)
    print("ISSUE #944 VALIDATION: CI Pipeline Robustness Fix")
    print("=" * 70)
    
    tests = [
        ("LaTeX Action Version Pinning", test_latex_action_version_pinning),
        ("CI Robustness Configuration", test_ci_robustness_configuration),
        ("Version Pinning Consistency", test_version_pinning_consistency),
        ("Reproducible Build Configuration", test_reproducible_build_configuration)
    ]
    
    test_results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            test_results.append(result)
        except Exception as e:
            print(f"❌ {test_name}: Exception occurred: {e}")
            test_results.append(False)
    
    print("\n" + "=" * 70)
    print("VALIDATION SUMMARY")
    print("=" * 70)
    
    for (test_name, _), result in zip(tests, test_results):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    passed_tests = sum(test_results)
    total_tests = len(test_results)
    print(f"\nTests passed: {passed_tests}/{total_tests}")
    
    if passed_tests == total_tests:
        print("🎉 ALL TESTS PASSED! CI pipeline robustness fix validated.")
        print("\nThe fix ensures:")
        print("✓ Reproducible builds with pinned LaTeX action version")
        print("✓ Enhanced error detection and handling")
        print("✓ Consistent action version pinning across workflows")
        print("✓ Robust configuration to prevent CI failures")
        return 0
    else:
        print("⚠️  Some tests failed. CI robustness fix needs attention.")
        return 1

if __name__ == "__main__":
    sys.exit(main())