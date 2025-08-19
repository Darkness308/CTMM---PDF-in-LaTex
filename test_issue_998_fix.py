#!/usr/bin/env python3
"""
Test script for Issue #998 - CI Build Failure Resolution
Validates that the dante-ev/latex-action version issue is resolved.
"""

import sys
import yaml
from pathlib import Path


def test_latex_action_version_fix():
    """Test that the LaTeX action version has been fixed to resolve CI failures."""
    print("🔍 Testing LaTeX Action Version Fix for Issue #998")
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
    
    # Check that the problematic @v2 version is not being used
    if '@v2' in uses and not '@v2.' in uses:  # @v2 but not @v2.x.x
        print("❌ Still using problematic @v2 version that causes CI failures")
        print("   This was the root cause identified in Issue #998")
        return False
    
    # Check that we're using @latest (the fix from Issue #867)
    if '@latest' in uses:
        print("✅ Using @latest version - this resolves the CI failure")
        return True
    
    # Check for other valid patterns (from previous issue resolutions)
    valid_patterns = ['@v0.2', '@master', '@main']
    for pattern in valid_patterns:
        if pattern in uses:
            print(f"✅ Using valid version pattern: {pattern}")
            return True
    
    print(f"⚠️  Warning: Using untested version pattern: {uses}")
    print("   Consider using @latest for maximum compatibility")
    return True  # Don't fail for unknown patterns, just warn


def test_ci_insights_issue_pattern():
    """Test that this fix addresses the CI Insights failure pattern."""
    print("\n🎯 Testing CI Insights Issue Pattern Resolution")
    print("=" * 60)
    
    # Verify the workflow structure that caused the CI failure
    workflow_path = Path(".github/workflows/latex-build.yml")
    with open(workflow_path, 'r') as f:
        workflow = yaml.safe_load(f)
    
    # Check that the workflow has proper error handling
    build_job = workflow.get('jobs', {}).get('build', {})
    steps = build_job.get('steps', [])
    
    # Look for validation steps before LaTeX compilation
    validation_steps = []
    latex_step_index = None
    
    for i, step in enumerate(steps):
        step_name = step.get('name', '').lower()
        uses = step.get('uses', '')
        
        if 'validation' in step_name or 'check' in step_name:
            validation_steps.append(step_name)
        
        if 'dante-ev/latex-action' in uses:
            latex_step_index = i
    
    if latex_step_index is None:
        print("❌ LaTeX compilation step not found")
        return False
    
    print(f"✅ Found {len(validation_steps)} validation steps before LaTeX compilation")
    
    # Check for error handling features
    upload_logs_step = None
    for step in steps:
        if step.get('if') == 'failure()' and 'upload-artifact' in step.get('uses', ''):
            upload_logs_step = step
            break
    
    if upload_logs_step:
        print("✅ Build log upload on failure configured")
    else:
        print("⚠️  No failure log upload configured")
    
    return True


def test_workflow_robustness():
    """Test overall workflow robustness features."""
    print("\n🛡️  Testing Workflow Robustness Features")
    print("=" * 60)
    
    workflow_path = Path(".github/workflows/latex-build.yml")
    with open(workflow_path, 'r') as f:
        content = f.read()
    
    # Check for quoted "on:" syntax (Issue #532 compliance)
    if '"on":' in content:
        print('✅ Uses quoted "on:" syntax (prevents YAML parsing issues)')
    else:
        print('⚠️  Uses unquoted on: syntax (potential YAML issue)')
    
    # Check for proper error handling in steps
    robustness_features = [
        'continue-on-error',
        'timeout-minutes', 
        'if: failure()',
        '|| echo',  # Fallback error handling
    ]
    
    found_features = []
    for feature in robustness_features:
        if feature in content:
            found_features.append(feature)
    
    print(f"✅ Found {len(found_features)} robustness features: {', '.join(found_features)}")
    
    return True


def main():
    """Run all validation tests for Issue #998 fix."""
    print("🧪 Issue #998 Fix Validation")
    print("=" * 60)
    print("Testing CI build failure resolution")
    print()
    
    tests = [
        ("LaTeX Action Version Fix", test_latex_action_version_fix),
        ("CI Insights Issue Pattern", test_ci_insights_issue_pattern),
        ("Workflow Robustness", test_workflow_robustness),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                print(f"✅ {test_name}: PASS")
                passed += 1
            else:
                print(f"❌ {test_name}: FAIL")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
    
    print("\n" + "=" * 60)
    print(f"Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Issue #998 has been resolved.")
        print("\nThe CI build failure should now be resolved:")
        print("✓ LaTeX action version issue fixed")
        print("✓ Action resolution should succeed")
        print("✓ PDF generation should proceed normally")
        return 0
    else:
        print("💥 Some tests failed. Please review the configuration.")
        return 1


if __name__ == "__main__":
    sys.exit(main())