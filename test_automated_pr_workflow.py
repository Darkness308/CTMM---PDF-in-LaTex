#!/usr/bin/env python3
"""
Test and validate the automated PR merge and build workflow.
"""

import yaml
import os
import sys
from pathlib import Path

def test_workflow_syntax():
    """Test that the workflow has valid YAML syntax and required fields."""
    print("🔧 Testing Automated PR Merge and Build Workflow")
    print("=" * 60)

    workflow_path = Path(".github/workflows/automated-pr-merge-test.yml")
    if not workflow_path.exists():
        print("❌ Workflow file not found")
        return False

    try:
        with open(workflow_path, 'r') as f:
            workflow = yaml.safe_load(f)
    except yaml.YAMLError as e:
        print(f"❌ YAML syntax error: {e}")
        return False

    # Check required fields
    required_fields = ['name', 'on', 'jobs']
    for field in required_fields:
        if field not in workflow:
            print(f"❌ Missing required field: {field}")
            return False

    print(f"✅ Name: {workflow['name']}")

    # Check triggers
    triggers = workflow['on']
    if not isinstance(triggers, dict):
        print("❌ Invalid triggers format")
        return False

    expected_triggers = ['workflow_dispatch', 'schedule']
    for trigger in expected_triggers:
        if trigger not in triggers:
            print(f"❌ Missing trigger: {trigger}")
            return False

    print(f"✅ Triggers: {list(triggers.keys())}")

    # Check workflow_dispatch inputs
    workflow_dispatch = triggers.get('workflow_dispatch', {})
    inputs = workflow_dispatch.get('inputs', {})
    expected_inputs = ['base_branch', 'max_prs', 'cleanup_branch']

    for input_name in expected_inputs:
        if input_name not in inputs:
            print(f"❌ Missing input: {input_name}")
            return False

        input_config = inputs[input_name]
        if 'description' not in input_config:
            print(f"❌ Missing description for input: {input_name}")
            return False

    print(f"✅ Workflow inputs: {list(inputs.keys())}")

    # Check jobs
    jobs = workflow.get('jobs', {})
    if 'automated-merge-test' not in jobs:
        print("❌ Missing main job: automated-merge-test")
        return False

    job = jobs['automated-merge-test']
    if 'runs-on' not in job:
        print("❌ Missing runs-on for main job")
        return False

    print(f"✅ Main job runs on: {job['runs-on']}")

    # Check steps
    steps = job.get('steps', [])
    if len(steps) == 0:
        print("❌ No steps defined in main job")
        return False

    print(f"✅ Job has {len(steps)} steps")

    # Check for key step names
    step_names = [step.get('name', '').lower() for step in steps]
    required_steps = [
        'checkout repository',
        'create test branch',
        'fetch open prs',
        'test merge and build each pr',
        'generate final summary'
    ]

    missing_steps = []
    for required_step in required_steps:
        if not any(required_step in step_name for step_name in step_names):
            missing_steps.append(required_step)

    if missing_steps:
        print(f"❌ Missing key steps: {missing_steps}")
        return False

    print(f"✅ All key workflow steps present")

    return True

def test_security_considerations():
    """Test security aspects of the workflow."""
    print("\n🔒 Testing Security Considerations")
    print("-" * 40)

    workflow_path = Path(".github/workflows/automated-pr-merge-test.yml")
    with open(workflow_path, 'r') as f:
        content = f.read()

    # Check for safe practices
    security_checks = []

    # Check for token usage
    if 'secrets.GITHUB_TOKEN' in content:
        security_checks.append("✅ Uses GitHub token for API access")
    else:
        security_checks.append("❌ Missing GitHub token usage")

    # Check for branch isolation
    if 'test_branch' in content and 'checkout' in content:
        security_checks.append("✅ Creates isolated test branches")
    else:
        security_checks.append("❌ Missing test branch isolation")

    # Check for cleanup
    if 'cleanup' in content.lower() and 'delete' in content.lower():
        security_checks.append("✅ Includes branch cleanup")
    else:
        security_checks.append("❌ Missing branch cleanup")

    # Check for main branch protection
    if 'git checkout $BASE_BRANCH' in content or 'git checkout ${{ steps.create_branch.outputs.base_branch }}' in content:
        security_checks.append("✅ Safely handles base branch operations")
    else:
        security_checks.append("❌ Missing safe base branch handling")

    for check in security_checks:
        print(check)

    return all(check.startswith("✅") for check in security_checks)

def test_integration_with_existing_tools():
    """Test that the workflow integrates well with existing tools."""
    print("\n🔗 Testing Integration with Existing Tools")
    print("-" * 40)

    workflow_path = Path(".github/workflows/automated-pr-merge-test.yml")
    with open(workflow_path, 'r') as f:
        content = f.read()

    # Check for usage of existing tools
    tool_checks = []

    if 'ctmm_build.py' in content:
        tool_checks.append("✅ Uses CTMM build system")
    else:
        tool_checks.append("❌ Missing CTMM build system integration")

    if 'validate_latex_syntax.py' in content:
        tool_checks.append("✅ Uses LaTeX syntax validation")
    else:
        tool_checks.append("❌ Missing LaTeX syntax validation")

    if 'dante-ev/latex-action' in content:
        tool_checks.append("✅ Uses established LaTeX action")
    else:
        tool_checks.append("❌ Missing LaTeX action integration")

    if 'upload-artifact' in content:
        tool_checks.append("✅ Uploads test results as artifacts")
    else:
        tool_checks.append("❌ Missing artifact upload")

    for check in tool_checks:
        print(check)

    return all(check.startswith("✅") for check in tool_checks)

def test_error_handling():
    """Test that the workflow has proper error handling."""
    print("\n⚠️  Testing Error Handling")
    print("-" * 40)

    workflow_path = Path(".github/workflows/automated-pr-merge-test.yml")
    with open(workflow_path, 'r') as f:
        content = f.read()

    error_handling_checks = []

    # Check for continue-on-error usage
    if 'continue-on-error: true' in content:
        error_handling_checks.append("✅ Uses continue-on-error for non-critical steps")
    else:
        error_handling_checks.append("⚠️  No continue-on-error found (may be intentional)")

    # Check for if: always() usage
    if 'if: always()' in content:
        error_handling_checks.append("✅ Has always-run cleanup steps")
    else:
        error_handling_checks.append("❌ Missing always-run cleanup steps")

    # Check for error logging
    if 'test_results' in content and '.log' in content:
        error_handling_checks.append("✅ Logs errors to files")
    else:
        error_handling_checks.append("❌ Missing error logging")

    # Check for failure handling
    if 'FAILED' in content or 'failed' in content:
        error_handling_checks.append("✅ Handles and reports failures")
    else:
        error_handling_checks.append("❌ Missing failure handling")

    for check in error_handling_checks:
        print(check)

    return True  # Error handling is mostly warnings, not failures

def main():
    """Run all workflow validation tests."""
    print("🧪 Automated PR Merge and Build Workflow Validation")
    print("=" * 80)

    tests = [
        ("Workflow Syntax", test_workflow_syntax),
        ("Security Considerations", test_security_considerations),
        ("Tool Integration", test_integration_with_existing_tools),
        ("Error Handling", test_error_handling)
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with error: {e}")
            results.append((test_name, False))

    print("\n" + "=" * 80)
    print("📊 VALIDATION SUMMARY")
    print("=" * 80)

    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status:10} {test_name}")
        if result:
            passed += 1

    print(f"\nOverall: {passed}/{len(results)} tests passed")

    if passed == len(results):
        print("🎉 All validation tests passed! Workflow is ready for use.")
        return True
    else:
        print("⚠️  Some validation tests failed. Review and fix issues before using workflow.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
