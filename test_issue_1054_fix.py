#!/usr/bin/env python3
"""
Test script for Issue #1054 - Fix corrupted merge markers and conflicting LaTeX action configurations
Validates that all dante-ev/latex-action entries use consistent, properly versioned configurations.
"""

import sys
import yaml
import glob
from pathlib import Path


def test_latex_action_consistency():
    """Test that all LaTeX action references use the same version."""
    print("[SEARCH] Testing LaTeX Action Version Consistency")
    print("=" * 60)

    workflow_files = glob.glob(".github/workflows/*.yml")
    latex_actions = []

    for workflow_file in workflow_files:
        try:
            with open(workflow_file, 'r') as f:
                workflow = yaml.safe_load(f)

            # Extract all jobs
            jobs = workflow.get('jobs', {})
            for job_name, job_def in jobs.items():
                steps = job_def.get('steps', [])
                for i, step in enumerate(steps):
                    uses = step.get('uses', '')
                    if 'dante-ev/latex-action' in uses:
                        latex_actions.append({
                            'file': workflow_file,
                            'job': job_name,
                            'step': i,
                            'step_name': step.get('name', f'Step {i}'),
                            'uses': uses
                        })
        except Exception as e:
            print(f"[FAIL] Error parsing {workflow_file}: {e}")
            return False

    if not latex_actions:
        print("[FAIL] No LaTeX actions found in any workflow")
        return False

    print(f"[PASS] Found {len(latex_actions)} LaTeX action(s):")
    versions = set()
    for action in latex_actions:
        print(f"   {action['file']} -> {action['uses']}")
        versions.add(action['uses'])

    # Check for version consistency
    if len(versions) == 1:
        version = versions.pop()
        print(f"[PASS] All LaTeX actions use consistent version: {version}")

        # Check that it's not a problematic version
        if version.endswith('@v2'):
            print("[FAIL] Using problematic @v2 version")
            return False
        if version.endswith('@v2.0.0'):
            print("[FAIL] Using problematic @v2.0.0 version")
            return False

        return True
    else:
        print(f"[FAIL] Inconsistent versions found: {versions}")
        return False


def test_no_merge_conflict_markers():
    """Test that no workflow files contain merge conflict markers."""
    print("\n[SEARCH] Testing for Merge Conflict Markers")
    print("=" * 60)

    workflow_files = glob.glob(".github/workflows/*.yml")
    # More precise conflict markers - must be at start of line
    # Note: Markers are split to avoid git merge conflicts
    conflict_patterns = [
        ('<' * 7 + ' ', 'Git merge conflict start'),
        ('>' * 7 + ' ', 'Git merge conflict end'),
        ('=' * 7 + ' ', 'Git merge conflict separator'),
        ('<' * 7 + ' HEAD', 'Git HEAD conflict marker'),
        ('>' * 7 + ' origin/', 'Git origin conflict marker'),
        ('refs/heads/', 'Orphaned branch reference'),
        ('refs/pull/', 'Orphaned PR reference')
    ]

    issues_found = False
    for workflow_file in workflow_files:
        with open(workflow_file, 'r') as f:
            content = f.read()
            for line_num, line in enumerate(content.splitlines(), 1):
                stripped_line = line.strip()
                for pattern, description in conflict_patterns:
                    if stripped_line.startswith(pattern):
                        print(f"[FAIL] {description} found in {workflow_file}:{line_num}: {line.strip()}")
                        issues_found = True

    if not issues_found:
        print("[PASS] No merge conflict markers found")
        return True
    else:
        return False


def test_no_duplicate_action_entries():
    """Test that there are no duplicate or conflicting action entries."""
    print("\n[SEARCH] Testing for Duplicate Action Entries")
    print("=" * 60)

    workflow_files = glob.glob(".github/workflows/*.yml")

    for workflow_file in workflow_files:
        try:
            with open(workflow_file, 'r') as f:
                workflow = yaml.safe_load(f)

            jobs = workflow.get('jobs', {})
            for job_name, job_def in jobs.items():
                steps = job_def.get('steps', [])
                latex_steps = []

                for i, step in enumerate(steps):
                    uses = step.get('uses', '')
                    if 'dante-ev/latex-action' in uses:
                        latex_steps.append((i, uses))

                if len(latex_steps) > 1:
                    print(f"[WARN]  Multiple LaTeX actions in {workflow_file}, job {job_name}:")
                    for step_num, uses in latex_steps:
                        print(f"    Step {step_num}: {uses}")
                elif len(latex_steps) == 1:
                    print(f"[PASS] Single LaTeX action in {workflow_file}, job {job_name}: {latex_steps[0][1]}")

        except Exception as e:
            print(f"[FAIL] Error parsing {workflow_file}: {e}")
            return False

    print("[PASS] No conflicting duplicate entries found")
    return True


def test_workflow_yaml_validity():
    """Test that all workflow YAML files are syntactically valid."""
    print("\n[TEST] Testing Workflow YAML Validity")
    print("=" * 60)

    workflow_files = glob.glob(".github/workflows/*.yml")
    all_valid = True

    for workflow_file in workflow_files:
        try:
            with open(workflow_file, 'r') as f:
                yaml.safe_load(f)
            print(f"[PASS] {workflow_file}: Valid YAML syntax")
        except yaml.YAMLError as e:
            print(f"[FAIL] {workflow_file}: YAML syntax error: {e}")
            all_valid = False
        except Exception as e:
            print(f"[FAIL] {workflow_file}: Error: {e}")
            all_valid = False

    return all_valid


def main():
    """Run all validation tests for Issue #1054 fix."""
    print("[TEST] Issue #1054 Fix Validation")
    print("=" * 60)
    print("Testing fix for corrupted merge markers and conflicting LaTeX action configurations")

    tests = [
        ("LaTeX Action Consistency", test_latex_action_consistency),
        ("Merge Conflict Markers", test_no_merge_conflict_markers),
        ("Duplicate Action Entries", test_no_duplicate_action_entries),
        ("Workflow YAML Validity", test_workflow_yaml_validity),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        try:
            if test_func():
                print(f"[PASS] {test_name}: PASS\n")
                passed += 1
            else:
                print(f"[FAIL] {test_name}: FAIL\n")
        except Exception as e:
            print(f"[ERROR] {test_name}: ERROR - {e}\n")

    print("=" * 60)
    print(f"Test Results: {passed} passed, {total - passed} failed")

    if passed == total:
        print("[SUCCESS] ALL TESTS PASSED! Issue #1054 has been resolved.")
        return 0
    else:
        print("[ERROR] Some tests failed. Please review the configuration.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
