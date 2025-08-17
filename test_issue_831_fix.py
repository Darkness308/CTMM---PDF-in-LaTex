#!/usr/bin/env python3
"""
Test validation for Issue #831: CI Build Failure Fix

This test validates that the GitHub Actions workflow uses correct and existing
action versions, preventing the error:
"Unable to resolve action `dante-ev/latex-action@v2.3.0`, unable to find version `v2.3.0`"

The test ensures:
1. dante-ev/latex-action uses valid version (@v2)
2. No problematic -pdf argument is present 
3. Workflow structure is valid for GitHub Actions
"""

import yaml
import os
import sys

def test_dante_action_version():
    """Test that GitHub Actions workflow uses valid dante-ev/latex-action version"""
    workflow_path = '.github/workflows/latex-build.yml'
    
    if not os.path.exists(workflow_path):
        print(f"❌ ERROR: Workflow file {workflow_path} not found")
        return False
    
    print(f"🔍 Testing dante-ev/latex-action version in {workflow_path}")
    
    with open(workflow_path, 'r') as f:
        content = f.read()
    
    try:
        workflow = yaml.safe_load(content)
    except yaml.YAMLError as e:
        print(f"❌ ERROR: Invalid YAML syntax: {e}")
        return False
    
    # Find LaTeX setup step
    build_job = workflow.get('jobs', {}).get('build', {})
    steps = build_job.get('steps', [])
    
    latex_step = None
    for step in steps:
        if step.get('uses', '').startswith('dante-ev/latex-action'):
            latex_step = step
            break
    
    if not latex_step:
        print("❌ ERROR: No dante-ev/latex-action step found")
        return False
    
    uses_action = latex_step.get('uses')
    print(f"📋 Found action: {uses_action}")
    
    # Check for valid version patterns
    if uses_action == 'dante-ev/latex-action@v2':
        print("✅ CORRECT: Using dante-ev/latex-action@v2 (recommended)")
        return True
    elif uses_action == 'dante-ev/latex-action@v2.0.0':
        print("⚠️  WARNING: v2.0.0 specific version - should use @v2 for latest v2.x")
        return True
    elif uses_action == 'dante-ev/latex-action@v2.3.0':
        print("❌ CRITICAL: dante-ev/latex-action@v2.3.0 does not exist!")
        print("   This will cause GitHub Actions to fail with:")
        print("   'Unable to resolve action `dante-ev/latex-action@v2.3.0`, unable to find version `v2.3.0`'")
        return False
    elif uses_action == 'dante-ev/latex-action@v2.4.0':
        print("❌ CRITICAL: dante-ev/latex-action@v2.4.0 does not exist!")
        return False
    else:
        print(f"❓ UNKNOWN: Unexpected version pattern: {uses_action}")
        return False

def test_no_pdf_argument():
    """Test that the problematic -pdf argument is not present"""
    workflow_path = '.github/workflows/latex-build.yml'
    
    print(f"🔍 Testing for absence of problematic -pdf argument")
    
    with open(workflow_path, 'r') as f:
        workflow = yaml.safe_load(f)
    
    # Find LaTeX setup step
    build_job = workflow.get('jobs', {}).get('build', {})
    steps = build_job.get('steps', [])
    
    latex_step = None
    for step in steps:
        if step.get('uses', '').startswith('dante-ev/latex-action'):
            latex_step = step
            break
    
    if not latex_step:
        print("❌ ERROR: No dante-ev/latex-action step found")
        return False
    
    args = latex_step.get('with', {}).get('args', '')
    print(f"📋 LaTeX args: {args}")
    
    if '-pdf' in args:
        print("❌ CRITICAL: Found problematic -pdf argument!")
        print("   This will cause pdflatex to fail as it doesn't recognize -pdf")
        print("   Expected args: -interaction=nonstopmode -halt-on-error -shell-escape")
        return False
    else:
        print("✅ CORRECT: No -pdf argument found")
        return True

def test_workflow_structure():
    """Test overall workflow structure validity"""
    workflow_path = '.github/workflows/latex-build.yml'
    
    print(f"🔍 Testing workflow structure validity")
    
    with open(workflow_path, 'r') as f:
        workflow = yaml.safe_load(f)
    
    required_fields = ['name', 'on', 'jobs']
    missing = [field for field in required_fields if field not in workflow]
    
    if missing:
        print(f"❌ ERROR: Missing required fields: {missing}")
        return False
    
    # Check build job structure
    build_job = workflow.get('jobs', {}).get('build', {})
    if not build_job:
        print("❌ ERROR: No 'build' job found")
        return False
    
    if 'runs-on' not in build_job:
        print("❌ ERROR: No 'runs-on' specified for build job")
        return False
    
    if 'steps' not in build_job:
        print("❌ ERROR: No 'steps' specified for build job")
        return False
    
    print("✅ CORRECT: Workflow structure is valid")
    return True

def test_validation_steps_order():
    """Test that validation steps come before LaTeX compilation"""
    workflow_path = '.github/workflows/latex-build.yml'
    
    print(f"🔍 Testing validation step ordering")
    
    with open(workflow_path, 'r') as f:
        workflow = yaml.safe_load(f)
    
    build_job = workflow.get('jobs', {}).get('build', {})
    steps = build_job.get('steps', [])
    
    latex_step_index = None
    validation_step_indices = []
    
    for i, step in enumerate(steps):
        step_name = step.get('name', '').lower()
        if 'latex' in step_name and 'set up' in step_name:
            latex_step_index = i
        elif any(keyword in step_name for keyword in ['validation', 'check', 'validate']):
            validation_step_indices.append(i)
    
    if latex_step_index is None:
        print("⚠️  WARNING: No LaTeX setup step found")
        return True
    
    if not validation_step_indices:
        print("⚠️  WARNING: No validation steps found")
        return True
    
    early_validation = all(idx < latex_step_index for idx in validation_step_indices)
    
    if early_validation:
        print("✅ CORRECT: All validation steps run before LaTeX compilation")
        return True
    else:
        print("❌ WARNING: Some validation steps run after LaTeX compilation")
        return False

def run_all_tests():
    """Run all Issue #831 validation tests"""
    print("=" * 60)
    print("ISSUE #831 CI BUILD FAILURE VALIDATION")
    print("=" * 60)
    
    tests = [
        ("dante-ev/latex-action version", test_dante_action_version),
        ("No problematic -pdf argument", test_no_pdf_argument),
        ("Workflow structure validity", test_workflow_structure),
        ("Validation step ordering", test_validation_steps_order),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🧪 Running test: {test_name}")
        print("-" * 50)
        try:
            result = test_func()
            results.append((test_name, result))
            if result:
                print(f"✅ PASS: {test_name}")
            else:
                print(f"❌ FAIL: {test_name}")
        except Exception as e:
            print(f"💥 ERROR in {test_name}: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED - Issue #831 fix is valid!")
        print("\nThe workflow should:")
        print("- Use dante-ev/latex-action@v2 (existing version)")
        print("- Exclude the problematic -pdf argument")
        print("- Run validation before LaTeX compilation")
        print("- Pass all GitHub Actions structure requirements")
        return True
    else:
        print(f"\n⚠️  {total - passed} TEST(S) FAILED - Issue #831 needs attention")
        return False

if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)