#!/usr/bin/env python3
"""
CI Failure Pattern Analysis - Issue #1064
Analyzes common CI failure patterns and provides mitigation strategies.
"""

import os
import yaml
import subprocess
import time
from typing import Dict, List, Tuple, Optional

def analyze_timeout_patterns() -> Dict[str, any]:
    """Analyze timeout configuration patterns across workflows."""
    print("[TIMER]  Analyzing Timeout Patterns")
    print("-" * 40)

    workflow_files = [
        '.github/workflows/latex-build.yml',
        '.github/workflows/latex-validation.yml',
        '.github/workflows/pr-validation.yml'
    ]

    timeout_analysis = {
        'total_steps': 0,
        'steps_with_timeout': 0,
        'timeout_ranges': {},
        'issues': []
    }

    for workflow_file in workflow_files:
        if not os.path.exists(workflow_file):
            continue

        print(f"[TEST] Checking {workflow_file}...")

        try:
            with open(workflow_file, 'r') as f:
                workflow_data = yaml.safe_load(f)

            jobs = workflow_data.get('jobs', {})
            for job_name, job_data in jobs.items():
                steps = job_data.get('steps', [])
                for step in steps:
                    timeout_analysis['total_steps'] += 1
                    step_name = step.get('name', 'Unnamed step')

                    if 'timeout-minutes' in step:
                        timeout_analysis['steps_with_timeout'] += 1
                        timeout_val = step['timeout-minutes']
                        timeout_range = f"{timeout_val}min"

                        if timeout_range not in timeout_analysis['timeout_ranges']:
                            timeout_analysis['timeout_ranges'][timeout_range] = 0
                        timeout_analysis['timeout_ranges'][timeout_range] += 1

                        print(f"  [PASS] {step_name}: {timeout_val} minutes")

                        # Check for potential timeout issues
                        if timeout_val > 20:
                            timeout_analysis['issues'].append(f"Long timeout in {step_name}: {timeout_val}min")
                    else:
                        print(f"  [WARN]  {step_name}: No timeout")
                        timeout_analysis['issues'].append(f"Missing timeout in {step_name}")

        except Exception as e:
            print(f"[FAIL] Error analyzing {workflow_file}: {e}")

    coverage = (timeout_analysis['steps_with_timeout'] / timeout_analysis['total_steps'] * 100) if timeout_analysis['total_steps'] > 0 else 0
    print(f"\n[SUMMARY] Timeout Coverage: {timeout_analysis['steps_with_timeout']}/{timeout_analysis['total_steps']} ({coverage:.1f}%)")

    return timeout_analysis

def analyze_resource_patterns() -> Dict[str, any]:
    """Analyze resource usage patterns and potential constraints."""
    print("\n[SAVE] Analyzing Resource Usage Patterns")
    print("-" * 40)

    resource_analysis = {
        'memory_checks': 0,
        'disk_checks': 0,
        'cpu_checks': 0,
        'issues': []
    }

    # Check for resource monitoring in workflows
    workflow_files = [
        '.github/workflows/latex-build.yml',
        '.github/workflows/latex-validation.yml'
    ]

    for workflow_file in workflow_files:
        if not os.path.exists(workflow_file):
            continue

        print(f"[TEST] Checking {workflow_file}...")

        with open(workflow_file, 'r') as f:
            content = f.read()

        if 'df -h' in content:
            resource_analysis['disk_checks'] += 1
            print("  [PASS] Disk space monitoring found")

        if 'free -h' in content:
            resource_analysis['memory_checks'] += 1
            print("  [PASS] Memory monitoring found")

        if 'nproc' in content or 'cpu' in content.lower():
            resource_analysis['cpu_checks'] += 1
            print("  [PASS] CPU monitoring found")

        # Check for resource-intensive operations
        if 'pdflatex' in content and 'resources' not in content:
            resource_analysis['issues'].append(f"LaTeX compilation without resource check in {workflow_file}")

    return resource_analysis

def analyze_action_version_patterns() -> Dict[str, any]:
    """Analyze GitHub Actions version patterns for potential issues."""
    print("\n[PACKAGE] Analyzing Action Version Patterns")
    print("-" * 40)

    # Run the action version validator
    try:
        result = subprocess.run(
            ['python3', 'validate_action_versions.py'],
            capture_output=True,
            text=True,
            timeout=30
        )

        version_analysis = {
            'validation_success': result.returncode == 0,
            'output': result.stdout,
            'errors': result.stderr if result.returncode != 0 else None
        }

        if result.returncode == 0:
            print("[PASS] Action version validation passed")
        else:
            print("[FAIL] Action version validation failed")
            if result.stderr:
                print(f"  Error: {result.stderr[:200]}...")

    except subprocess.TimeoutExpired:
        version_analysis = {
            'validation_success': False,
            'output': '',
            'errors': 'Validation timeout'
        }
        print("[TIMER]  Action version validation timed out")
    except FileNotFoundError:
        version_analysis = {
            'validation_success': False,
            'output': '',
            'errors': 'validate_action_versions.py not found'
        }
        print("[FAIL] Action version validator not found")

    return version_analysis

def analyze_concurrency_patterns() -> Dict[str, any]:
    """Analyze workflow concurrency patterns for potential conflicts."""
    print("\n[SYNC] Analyzing Concurrency Patterns")
    print("-" * 40)

    concurrency_analysis = {
        'workflows_with_concurrency': 0,
        'total_workflows': 0,
        'potential_conflicts': []
    }

    workflow_files = [f for f in os.listdir('.github/workflows') if f.endswith('.yml')]
    concurrency_analysis['total_workflows'] = len(workflow_files)

    for workflow_file in workflow_files:
        workflow_path = os.path.join('.github/workflows', workflow_file)

        try:
            with open(workflow_path, 'r') as f:
                workflow_data = yaml.safe_load(f)

            if 'concurrency' in workflow_data:
                concurrency_analysis['workflows_with_concurrency'] += 1
                print(f"  [PASS] {workflow_file}: Has concurrency control")
            else:
                print(f"  [WARN]  {workflow_file}: No concurrency control")
                concurrency_analysis['potential_conflicts'].append(workflow_file)

        except Exception as e:
            print(f"  [FAIL] Error analyzing {workflow_file}: {e}")

    coverage = (concurrency_analysis['workflows_with_concurrency'] / concurrency_analysis['total_workflows'] * 100) if concurrency_analysis['total_workflows'] > 0 else 0
    print(f"\n[SUMMARY] Concurrency Coverage: {concurrency_analysis['workflows_with_concurrency']}/{concurrency_analysis['total_workflows']} ({coverage:.1f}%)")

    return concurrency_analysis

def run_validation_tests() -> Dict[str, any]:
    """Run validation tests to check for common failure points."""
    print("\n[TEST] Running Validation Tests")
    print("-" * 40)

    validation_results = {
        'tests_run': 0,
        'tests_passed': 0,
        'test_details': []
    }

    # Test 1: CTMM Build System
    print("[FIX] Testing CTMM build system...")
    try:
        start_time = time.time()
        result = subprocess.run(
            ['python3', 'ctmm_build.py'],
            capture_output=True,
            text=True,
            timeout=60
        )
        duration = time.time() - start_time

        validation_results['tests_run'] += 1
        if result.returncode == 0:
            validation_results['tests_passed'] += 1
            print(f"  [PASS] CTMM build system passed ({duration:.1f}s)")
        else:
            print(f"  [FAIL] CTMM build system failed ({duration:.1f}s)")

        validation_results['test_details'].append({
            'name': 'CTMM Build System',
            'passed': result.returncode == 0,
            'duration': duration,
            'output': result.stdout[:200] + '...' if len(result.stdout) > 200 else result.stdout
        })

    except subprocess.TimeoutExpired:
        print("  [TIMER]  CTMM build system timed out")
        validation_results['tests_run'] += 1
    except Exception as e:
        print(f"  [FAIL] CTMM build system error: {e}")
        validation_results['tests_run'] += 1

    # Test 2: Workflow syntax validation
    print("[TEST] Testing workflow syntax...")
    try:
        start_time = time.time()
        result = subprocess.run(
            ['python3', 'validate_workflow_syntax.py'],
            capture_output=True,
            text=True,
            timeout=30
        )
        duration = time.time() - start_time

        validation_results['tests_run'] += 1
        if result.returncode == 0:
            validation_results['tests_passed'] += 1
            print(f"  [PASS] Workflow syntax validation passed ({duration:.1f}s)")
        else:
            print(f"  [FAIL] Workflow syntax validation failed ({duration:.1f}s)")

        validation_results['test_details'].append({
            'name': 'Workflow Syntax',
            'passed': result.returncode == 0,
            'duration': duration
        })

    except Exception as e:
        print(f"  [FAIL] Workflow syntax validation error: {e}")
        validation_results['tests_run'] += 1

    return validation_results

def analyze_failure_patterns():
    """Main function to analyze CI failure patterns."""
    print("=" * 70)
    print("CI FAILURE PATTERN ANALYSIS - Issue #1064")
    print("=" * 70)

    analyses = {}

    # Run all pattern analyses
    analyses['timeout'] = analyze_timeout_patterns()
    analyses['resource'] = analyze_resource_patterns()
    analyses['action_versions'] = analyze_action_version_patterns()
    analyses['concurrency'] = analyze_concurrency_patterns()
    analyses['validation'] = run_validation_tests()

    # Generate summary
    print("\n" + "=" * 70)
    print("FAILURE PATTERN ANALYSIS SUMMARY")
    print("=" * 70)

    total_issues = 0
    for analysis_name, analysis_data in analyses.items():
        if 'issues' in analysis_data:
            issue_count = len(analysis_data['issues'])
            total_issues += issue_count
            if issue_count > 0:
                print(f"[WARN]  {analysis_name.title()}: {issue_count} issues identified")
            else:
                print(f"[PASS] {analysis_name.title()}: No issues found")

    # Validation test summary
    validation = analyses['validation']
    if validation['tests_run'] > 0:
        success_rate = (validation['tests_passed'] / validation['tests_run']) * 100
        print(f"[TEST] Validation Tests: {validation['tests_passed']}/{validation['tests_run']} passed ({success_rate:.1f}%)")

    # Overall health assessment
    print(f"\n[TARGET] Total Issues Identified: {total_issues}")

    if total_issues == 0:
        print("[SUCCESS] EXCELLENT: No failure patterns detected")
        return True
    elif total_issues <= 3:
        print("[PASS] GOOD: Minor issues identified, low failure risk")
        return True
    elif total_issues <= 6:
        print("[WARN]  WARNING: Several issues identified, moderate failure risk")
        return True
    else:
        print("[RED] CRITICAL: Many issues identified, high failure risk")
        return False

if __name__ == "__main__":
    success = analyze_failure_patterns()
    exit(0 if success else 1)
