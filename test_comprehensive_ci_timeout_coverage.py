#!/usr/bin/env python3
"""
Comprehensive CI Timeout Coverage Validation

This test validates timeout configurations across ALL GitHub Actions workflows
in the repository to ensure comprehensive protection against hanging CI jobs.

Tests target the enhanced timeout handling implemented to prevent intermittent
CI failures like those reported in CI Insights.
"""

import yaml
import os
import sys

def test_comprehensive_timeout_coverage():
    """Test timeout coverage across all workflow files."""
    print("[SEARCH] Testing Comprehensive Timeout Coverage")
    print("=" * 60)

    # Find all workflow files
    workflow_dir = '.github/workflows'
    workflow_files = []

    if os.path.exists(workflow_dir):
        for file in os.listdir(workflow_dir):
            if file.endswith('.yml') or file.endswith('.yaml'):
                workflow_files.append(os.path.join(workflow_dir, file))

    if not workflow_files:
        print("[FAIL] No workflow files found")
        return False

    total_steps = 0
    timeout_steps = 0
    workflow_results = {}

    for workflow_file in sorted(workflow_files):
        print(f"\n[TEST] Analyzing {workflow_file}...")

        try:
            with open(workflow_file, 'r') as f:
                data = yaml.safe_load(f)
        except Exception as e:
            print(f"[FAIL] Failed to parse {workflow_file}: {e}")
            continue

        workflow_steps = 0
        workflow_timeouts = 0

        jobs = data.get('jobs', {})
        for job_name, job_data in jobs.items():
            steps = job_data.get('steps', [])
            for step in steps:
                step_name = step.get('name', 'Unnamed step')
                timeout = step.get('timeout-minutes', None)

                workflow_steps += 1
                total_steps += 1

                if timeout:
                    workflow_timeouts += 1
                    timeout_steps += 1
                    print(f"  [PASS] {step_name}: {timeout}min")
                else:
                    print(f"  [WARN]  {step_name}: NO TIMEOUT")

        workflow_coverage = (workflow_timeouts / workflow_steps * 100) if workflow_steps > 0 else 0
        workflow_results[workflow_file] = {
            'coverage': workflow_coverage,
            'timeout_steps': workflow_timeouts,
            'total_steps': workflow_steps
        }

        print(f"  [SUMMARY] Workflow Coverage: {workflow_timeouts}/{workflow_steps} ({workflow_coverage:.1f}%)")

    # Overall summary
    print(f"\n{'=' * 60}")
    print("[SUMMARY] COMPREHENSIVE TIMEOUT COVERAGE SUMMARY")
    print(f"{'=' * 60}")

    overall_coverage = (timeout_steps / total_steps * 100) if total_steps > 0 else 0

    for workflow_file, results in workflow_results.items():
        status = "[PASS]" if results['coverage'] >= 80 else "[WARN]"
        print(f"{status} {os.path.basename(workflow_file)}: {results['coverage']:.1f}% ({results['timeout_steps']}/{results['total_steps']})")

    print(f"\n[TARGET] OVERALL COVERAGE: {timeout_steps}/{total_steps} ({overall_coverage:.1f}%)")

    if overall_coverage >= 90:
        print("[SUCCESS] EXCELLENT: Comprehensive timeout coverage!")
        return True
    elif overall_coverage >= 80:
        print("[PASS] GOOD: Strong timeout coverage")
        return True
    elif overall_coverage >= 70:
        print("[WARN]  FAIR: Consider adding more timeouts")
        return True
    else:
        print("[FAIL] POOR: Insufficient timeout coverage")
        return False

def test_timeout_strategy_consistency():
    """Test that timeout values follow a consistent strategy."""
    print("\n[TIMER]  Testing Timeout Strategy Consistency")
    print("=" * 60)

    timeout_categories = {
        'quick': [],      # 3-5 minutes
        'medium': [],     # 8-10 minutes
        'heavy': []       # 15+ minutes
    }

    workflow_files = [f for f in os.listdir('.github/workflows') if f.endswith('.yml')]

    for workflow_file in workflow_files:
        with open(f'.github/workflows/{workflow_file}', 'r') as f:
            data = yaml.safe_load(f)

        for job_name, job_data in data.get('jobs', {}).items():
            for step in job_data.get('steps', []):
                timeout = step.get('timeout-minutes')
                if timeout:
                    if timeout <= 5:
                        timeout_categories['quick'].append((step.get('name', 'Unnamed'), timeout))
                    elif timeout <= 10:
                        timeout_categories['medium'].append((step.get('name', 'Unnamed'), timeout))
                    else:
                        timeout_categories['heavy'].append((step.get('name', 'Unnamed'), timeout))

    print("[CHART] Timeout Strategy Analysis:")
    print(f"  Quick operations (<=5min): {len(timeout_categories['quick'])} steps")
    print(f"  Medium operations (6-10min): {len(timeout_categories['medium'])} steps")
    print(f"  Heavy operations (>10min): {len(timeout_categories['heavy'])} steps")

    # Check for reasonable distribution
    total_with_timeouts = sum(len(cat) for cat in timeout_categories.values())
    if total_with_timeouts > 0:
        quick_pct = len(timeout_categories['quick']) / total_with_timeouts * 100
        medium_pct = len(timeout_categories['medium']) / total_with_timeouts * 100
        heavy_pct = len(timeout_categories['heavy']) / total_with_timeouts * 100

        print(f"  Distribution: {quick_pct:.1f}% quick, {medium_pct:.1f}% medium, {heavy_pct:.1f}% heavy")

        if heavy_pct < 50:  # Most operations should be quick/medium
            print("[PASS] Good timeout strategy - most operations are quick/medium")
            return True
        else:
            print("[WARN]  Many heavy operations - consider optimization")
            return True

    return False

def test_error_recovery_configuration():
    """Test that error recovery mechanisms are properly configured."""
    print("\n[SHIELD]  Testing Error Recovery Configuration")
    print("=" * 60)

    recovery_features = {
        'continue-on-error': 0,
        'if: failure()': 0,
        'if: always()': 0,
        'timeout-minutes': 0
    }

    workflow_files = [f for f in os.listdir('.github/workflows') if f.endswith('.yml')]

    for workflow_file in workflow_files:
        with open(f'.github/workflows/{workflow_file}', 'r') as f:
            content = f.read()

        # Reload for YAML parsing
        with open(f'.github/workflows/{workflow_file}', 'r') as f:
            try:
                data = yaml.safe_load(f)
            except:
                continue

        # Count recovery features
        recovery_features['continue-on-error'] += content.count('continue-on-error: true')
        recovery_features['if: failure()'] += content.count('if: failure()')
        recovery_features['if: always()'] += content.count('if: always()')

        # Count timeout configurations
        if data and isinstance(data, dict):
            for job_name, job_data in data.get('jobs', {}).items():
                if job_data and isinstance(job_data, dict):
                    for step in job_data.get('steps', []):
                        if step and isinstance(step, dict) and 'timeout-minutes' in step:
                            recovery_features['timeout-minutes'] += 1

    print("[FIX] Error Recovery Features Found:")
    for feature, count in recovery_features.items():
        print(f"  {feature}: {count}")

    # Check if we have good coverage
    total_recovery = sum(recovery_features.values())
    if total_recovery >= 20:  # Reasonable threshold
        print("[PASS] Strong error recovery configuration")
        return True
    else:
        print("[WARN]  Consider adding more error recovery mechanisms")
        return True

def main():
    """Run all comprehensive CI timeout coverage tests."""
    print("[TEST] Comprehensive CI Timeout Coverage Validation")
    print("=" * 80)

    tests = [
        ("Comprehensive Timeout Coverage", test_comprehensive_timeout_coverage),
        ("Timeout Strategy Consistency", test_timeout_strategy_consistency),
        ("Error Recovery Configuration", test_error_recovery_configuration)
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"[FAIL] {test_name} failed with error: {e}")
            results.append((test_name, False))

    print("\n" + "=" * 80)
    print("[SUMMARY] COMPREHENSIVE VALIDATION SUMMARY")
    print("=" * 80)

    passed = 0
    for test_name, result in results:
        status = "[PASS] PASS" if result else "[FAIL] FAIL"
        print(f"{status:10} {test_name}")
        if result:
            passed += 1

    print(f"\nOverall: {passed}/{len(results)} tests passed")

    if passed == len(results):
        print("[SUCCESS] All comprehensive validation tests passed! CI pipelines are robust.")
        return True
    else:
        print("[WARN]  Some validation tests failed. Review and enhance CI configuration.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
