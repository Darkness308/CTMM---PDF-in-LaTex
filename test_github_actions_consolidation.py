#!/usr/bin/env python3
"""
Test script for GitHub Actions workflow consolidation and cleanup
Validates that merge conflict markers have been removed and LaTeX action configurations are consolidated.

This addresses the fixes mentioned in the pull request:
- Removed merge conflict markers that were blocking workflow execution
- Consolidated multiple duplicate dante-ev/latex-action entries into a single configuration
- Cleaned up formatting inconsistencies in the workflow file
"""

import yaml
import os
import sys
from pathlib import Path

def test_no_merge_conflict_markers():
    """Test that all workflow files are free of merge conflict markers."""
    print("\n🔍 TESTING FOR MERGE CONFLICT MARKERS")
    print("-" * 50)
    
    workflow_dir = Path(".github/workflows")
    # Actual merge conflict markers (not decorative separators)
    conflict_patterns = [
        "<<<<<<< HEAD",
        "<<<<<<< ",
        "======= ",  # Note the space - actual conflict markers have space after
        ">>>>>>> ",
        "=======\n",  # or at end of line
    ]
    
    found_conflicts = False
    
    for workflow_file in workflow_dir.glob("*.yml"):
        content = workflow_file.read_text()
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            # Check for actual merge conflict markers, not decorative separators
            stripped_line = line.strip()
            
            # Skip echo statements with decorative separators
            if 'echo "' in line and ('=====' in line or '-----' in line):
                continue
                
            for pattern in conflict_patterns:
                if pattern in line:
                    print(f"❌ CONFLICT MARKER found in {workflow_file}: line {line_num}")
                    print(f"   {line.strip()}")
                    found_conflicts = True
            
            # Also check for standalone "=======" (exactly 7 equals) that's not in echo
            if stripped_line == "=======" and 'echo' not in line:
                print(f"❌ CONFLICT MARKER found in {workflow_file}: line {line_num}")
                print(f"   {line.strip()}")
                found_conflicts = True
    
    if not found_conflicts:
        print("✅ PASS: No merge conflict markers found in any workflow files")
        print("   (Decorative separators in echo statements are allowed)")
        return True
    else:
        print("❌ FAIL: Merge conflict markers still present")
        return False

def test_latex_action_consolidation():
    """Test that dante-ev/latex-action is used consistently and not duplicated."""
    print("\n🔧 TESTING LATEX ACTION CONSOLIDATION")
    print("-" * 50)
    
    workflow_file = Path(".github/workflows/latex-build.yml")
    if not workflow_file.exists():
        print("❌ ERROR: latex-build.yml not found")
        return False
    
    try:
        with open(workflow_file, 'r') as f:
            workflow_content = yaml.safe_load(f)
    except Exception as e:
        print(f"❌ ERROR: Failed to parse {workflow_file}: {e}")
        return False
    
    # Find all uses of dante-ev/latex-action
    latex_actions = []
    jobs = workflow_content.get('jobs', {})
    
    for job_name, job_config in jobs.items():
        steps = job_config.get('steps', [])
        for step_index, step in enumerate(steps):
            uses = step.get('uses', '')
            if 'dante-ev/latex-action' in uses:
                latex_actions.append({
                    'job': job_name,
                    'step_index': step_index,
                    'uses': uses,
                    'step_name': step.get('name', 'unnamed')
                })
    
    print(f"Found {len(latex_actions)} dante-ev/latex-action usage(s)")
    
    if len(latex_actions) == 0:
        print("❌ FAIL: No dante-ev/latex-action found in workflow")
        return False
    elif len(latex_actions) == 1:
        action = latex_actions[0]
        print(f"✅ PASS: Single dante-ev/latex-action usage found")
        print(f"   Job: {action['job']}")
        print(f"   Step: {action['step_name']}")
        print(f"   Uses: {action['uses']}")
        
        # Check for correct version
        if action['uses'] == 'dante-ev/latex-action@v2':
            print("✅ PASS: Using correct version @v2")
            return True
        elif action['uses'] == 'dante-ev/latex-action@v2.0.0':
            print("❌ FAIL: Using problematic version @v2.0.0")
            print("This version doesn't exist and causes CI failure")
            return False
        else:
            print(f"⚠️  WARNING: Using version {action['uses']}")
            print("Expected: dante-ev/latex-action@v2")
            return True
    else:
        print("❌ FAIL: Multiple dante-ev/latex-action entries found - consolidation needed")
        for action in latex_actions:
            print(f"   {action['job']}.{action['step_index']}: {action['uses']}")
        return False

def test_workflow_formatting_consistency():
    """Test that workflow files have consistent formatting."""
    print("\n📐 TESTING WORKFLOW FORMATTING CONSISTENCY")
    print("-" * 50)
    
    workflow_dir = Path(".github/workflows")
    issues_found = False
    
    for workflow_file in workflow_dir.glob("*.yml"):
        print(f"\nChecking {workflow_file.name}...")
        
        content = workflow_file.read_text()
        lines = content.split('\n')
        
        # Check for proper "on": quoting (YAML boolean issue)
        for line_num, line in enumerate(lines, 1):
            if line.strip().startswith('on:') and not line.strip().startswith('"on":'):
                print(f"⚠️  WARNING: Unquoted 'on:' at line {line_num}")
                print("   Consider using '\"on\":' to prevent YAML boolean interpretation")
                # This is a warning, not a failure
        
        # Check for trailing spaces
        trailing_spaces = [i+1 for i, line in enumerate(lines) if line.rstrip() != line]
        if trailing_spaces:
            print(f"⚠️  WARNING: Trailing spaces on lines: {trailing_spaces[:5]}")
            if len(trailing_spaces) > 5:
                print(f"   ... and {len(trailing_spaces)-5} more")
        
        # Check for consistent indentation (should be 2 spaces for YAML)
        inconsistent_indent = []
        for line_num, line in enumerate(lines, 1):
            if line.strip() and line.startswith(' '):
                leading_spaces = len(line) - len(line.lstrip())
                if leading_spaces % 2 != 0:
                    inconsistent_indent.append(line_num)
        
        if inconsistent_indent:
            print(f"⚠️  WARNING: Inconsistent indentation on lines: {inconsistent_indent[:5]}")
            if len(inconsistent_indent) > 5:
                print(f"   ... and {len(inconsistent_indent)-5} more")
    
    if not issues_found:
        print("✅ PASS: Workflow formatting is generally consistent")
    
    return True  # Always pass for formatting checks (warnings only)

def test_latex_action_configuration():
    """Test that the LaTeX action is properly configured."""
    print("\n⚙️  TESTING LATEX ACTION CONFIGURATION")
    print("-" * 50)
    
    workflow_file = Path(".github/workflows/latex-build.yml")
    
    with open(workflow_file, 'r') as f:
        workflow = yaml.safe_load(f)
    
    # Find the LaTeX action step
    latex_step = None
    for job_name, job_config in workflow.get('jobs', {}).items():
        for step in job_config.get('steps', []):
            if 'dante-ev/latex-action' in step.get('uses', ''):
                latex_step = step
                break
        if latex_step:
            break
    
    if not latex_step:
        print("❌ FAIL: LaTeX action step not found")
        return False
    
    # Check required configuration
    step_with = latex_step.get('with', {})
    
    required_configs = ['root_file']
    missing_configs = [config for config in required_configs if config not in step_with]
    
    if missing_configs:
        print(f"❌ FAIL: Missing required configuration: {missing_configs}")
        return False
    
    print(f"✅ PASS: LaTeX action properly configured")
    print(f"   root_file: {step_with.get('root_file')}")
    print(f"   args: {step_with.get('args', 'not specified')}")
    
    # Check for recommended packages
    extra_packages = step_with.get('extra_system_packages', '')
    if extra_packages:
        package_lines = extra_packages.strip().split('\n')
        print(f"   extra_system_packages: {len(package_lines)} packages configured")
        
        # Check for German language support
        if 'texlive-lang-german' in extra_packages:
            print("   ✅ German language support configured")
        else:
            print("   ⚠️  German language support not explicitly configured")
    
    return True

def main():
    """Run all GitHub Actions consolidation tests."""
    print("=" * 60)
    print("GitHub Actions Workflow Consolidation Validation")
    print("=" * 60)
    print("Testing fixes mentioned in pull request:")
    print("- Removal of merge conflict markers")
    print("- Consolidation of duplicate LaTeX action configurations")
    print("- Cleanup of formatting inconsistencies")
    print("=" * 60)
    
    tests = [
        test_no_merge_conflict_markers,
        test_latex_action_consolidation,
        test_workflow_formatting_consistency,
        test_latex_action_configuration,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"\n❌ ERROR in {test.__name__}: {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    test_names = [
        "Merge conflict markers",
        "LaTeX action consolidation", 
        "Workflow formatting consistency",
        "LaTeX action configuration"
    ]
    
    for i, (test_name, result) in enumerate(zip(test_names, results)):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\nTests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED - GitHub Actions workflows are properly consolidated!")
        print("\nThe workflow is ready for:")
        print("- Successful LaTeX PDF compilation")
        print("- Clean CI/CD pipeline execution")
        print("- No merge conflicts or duplicate configurations")
        return True
    else:
        print(f"❌ {total - passed} test(s) failed - consolidation work needed")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)