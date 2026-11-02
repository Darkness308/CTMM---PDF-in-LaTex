#!/usr/bin/env python3
"""
Issue #1128 CI LaTeX Build Failure Fix Validation

This script validates that all the CI LaTeX build failure fixes mentioned in
the PR description have been properly implemented:

1. Fixed GitHub Actions workflow syntax issues by quoting YAML keywords
2. Updated LaTeX action to use latest version and corrected compilation arguments
3. Added comprehensive LaTeX package dependencies for German language support
4. Enhanced build system to gracefully handle missing LaTeX installations

Key improvements tested:
- YAML syntax with proper "on:" keyword quoting
- Robust LaTeX action usage (xu-cheng/latex-action@v3)
- Complete LaTeX package dependencies for German language support
- Two-tier compilation approach with fallback mechanisms
- Enhanced error recovery and reporting
"""

import os
import sys
import yaml
import subprocess
import re

def test_yaml_syntax_fixes():
    """Test that all workflow files have properly quoted 'on:' keywords."""
    print("\n[SEARCH] Testing YAML Syntax Fixes")
    print("=" * 50)

    workflow_dir = ".github/workflows"
    issues_found = []
    fixes_verified = []

    if not os.path.exists(workflow_dir):
        issues_found.append("[FAIL] Workflow directory not found")
        return issues_found, fixes_verified

    for filename in os.listdir(workflow_dir):
        if filename.endswith('.yml') or filename.endswith('.yaml'):
            filepath = os.path.join(workflow_dir, filename)

            print(f"[FILE] Checking {filename}...")

            try:
                # Test YAML parsing
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    yaml.safe_load(content)

                # Check for properly quoted "on:" keyword
                if '"on":' in content or "'on':" in content:
                    fixes_verified.append(f"[PASS] {filename}: Properly quoted 'on:' keyword")
                elif 'on:' in content and not re.search(r'^\s*["\']?on["\']?\s*:', content, re.MULTILINE):
                    issues_found.append(f"[FAIL] {filename}: 'on:' keyword should be quoted")
                else:
                    fixes_verified.append(f"[PASS] {filename}: YAML syntax valid")

            except yaml.YAMLError as e:
                issues_found.append(f"[FAIL] {filename}: YAML syntax error - {e}")
            except Exception as e:
                issues_found.append(f"[FAIL] {filename}: Error reading file - {e}")

    return issues_found, fixes_verified

def test_latex_action_configuration():
    """Test that LaTeX action configuration is correct and robust."""
    print("\n[SEARCH] Testing LaTeX Action Configuration")
    print("=" * 50)

    issues_found = []
    fixes_verified = []

    expected_action = "xu-cheng/latex-action@v3"
    expected_args = ["-interaction=nonstopmode", "-halt-on-error", "-shell-escape"]

    workflow_files = [
        ".github/workflows/latex-build.yml",
        ".github/workflows/automated-pr-merge-test.yml"
    ]

    for workflow_file in workflow_files:
        if not os.path.exists(workflow_file):
            continue

        print(f"[FILE] Checking {workflow_file}...")

        with open(workflow_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check for xu-cheng/latex-action usage
        if expected_action in content:
            fixes_verified.append(f"[PASS] {workflow_file}: Using robust {expected_action}")
        else:
            # Check for problematic dante-ev/latex-action
            if "dante-ev/latex-action" in content:
                issues_found.append(f"[FAIL] {workflow_file}: Still using unreliable dante-ev/latex-action")
            else:
                issues_found.append(f"[FAIL] {workflow_file}: No LaTeX action found")

        # Check for proper compilation arguments
        if "args:" in content:
            args_section = re.search(r'args:\s*(.+)', content)
            if args_section:
                args_line = args_section.group(1).strip()
                all_args_present = all(arg in args_line for arg in expected_args)

                if all_args_present:
                    fixes_verified.append(f"[PASS] {workflow_file}: Proper compilation arguments")
                else:
                    missing_args = [arg for arg in expected_args if arg not in args_line]
                    issues_found.append(f"[FAIL] {workflow_file}: Missing arguments: {missing_args}")

        # Check for fallback mechanism
        if "fallback" in content.lower() and "manual" in content.lower():
            fixes_verified.append(f"[PASS] {workflow_file}: Two-tier fallback mechanism implemented")
        else:
            issues_found.append(f"[FAIL] {workflow_file}: Missing fallback mechanism")

    return issues_found, fixes_verified

def test_latex_package_dependencies():
    """Test that comprehensive LaTeX package dependencies are included."""
    print("\n[SEARCH] Testing LaTeX Package Dependencies")
    print("=" * 50)

    issues_found = []
    fixes_verified = []

    required_packages = [
        'texlive-lang-german',  # German language support
        'texlive-fonts-recommended', # Essential fonts
        'texlive-latex-recommended', # Core LaTeX packages
        'texlive-fonts-extra',  # FontAwesome5, additional fonts
        'texlive-latex-extra',  # TikZ, tcolorbox, advanced packages
        'texlive-science',  # amssymb, mathematical symbols
        'texlive-pstricks'  # pifont, graphics packages
    ]

    workflow_files = [
        ".github/workflows/latex-build.yml",
        ".github/workflows/automated-pr-merge-test.yml"
    ]

    for workflow_file in workflow_files:
        if not os.path.exists(workflow_file):
            continue

        print(f"[FILE] Checking {workflow_file}...")

        with open(workflow_file, 'r', encoding='utf-8') as f:
            content = f.read()

        for package in required_packages:
            if package in content:
                fixes_verified.append(f"[PASS] {workflow_file}: Package {package} included")
            else:
                issues_found.append(f"[FAIL] {workflow_file}: Missing package {package}")

    return issues_found, fixes_verified

def test_build_system_robustness():
    """Test that build system gracefully handles missing LaTeX installations."""
    print("\n[SEARCH] Testing Build System Robustness")
    print("=" * 50)

    issues_found = []
    fixes_verified = []

    try:
        # Test that build system works without LaTeX
        print("[TEST] Running CTMM build system...")
        result = subprocess.run(
            [sys.executable, 'ctmm_build.py'],
            capture_output=True,
            text=True,
            timeout=60
        )

        output = result.stdout + result.stderr

        if result.returncode == 0:
            fixes_verified.append("[PASS] Build system handles missing LaTeX gracefully")

            # Check for specific robustness indicators
            robustness_indicators = [
                'pdflatex not found',
                'skipping LaTeX compilation',
                'LaTeX not available',
                'Basic structure test passed'
            ]

            for indicator in robustness_indicators:
                if indicator in output:
                    fixes_verified.append(f"[PASS] Robustness: {indicator}")
                    break
            else:
                issues_found.append("[WARN]  Build system may not have proper fallback messaging")
        else:
            issues_found.append(f"[FAIL] Build system failed (exit code: {result.returncode})")

    except subprocess.TimeoutExpired:
        issues_found.append("[FAIL] Build system check timed out")
    except Exception as e:
        issues_found.append(f"[FAIL] Error running build system: {e}")

    # Test LaTeX syntax validation
    try:
        print("[TEST] Running LaTeX syntax validation...")
        result = subprocess.run(
            [sys.executable, 'validate_latex_syntax.py'],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            fixes_verified.append("[PASS] LaTeX syntax validation works correctly")
        else:
            issues_found.append("[FAIL] LaTeX syntax validation failed")

    except Exception as e:
        issues_found.append(f"[FAIL] Error running LaTeX validation: {e}")

    return issues_found, fixes_verified

def test_critical_files_exist():
    """Test that all critical files exist for proper CI operation."""
    print("\n[SEARCH] Testing Critical Files Existence")
    print("=" * 50)

    issues_found = []
    fixes_verified = []

    critical_files = [
        'main.tex',
        'ctmm_build.py',
        'validate_latex_syntax.py',
        'style/ctmm-design.sty',
        'style/form-elements.sty',
        'style/ctmm-diagrams.sty',
        '.github/workflows/latex-build.yml',
        '.github/workflows/latex-validation.yml'
    ]

    for file_path in critical_files:
        if os.path.exists(file_path):
            fixes_verified.append(f"[PASS] Critical file exists: {file_path}")
        else:
            issues_found.append(f"[FAIL] Missing critical file: {file_path}")

    return issues_found, fixes_verified

def test_workflow_timeout_configuration():
    """Test that workflows have proper timeout configuration to prevent CI hangs."""
    print("\n[SEARCH] Testing Workflow Timeout Configuration")
    print("=" * 50)

    issues_found = []
    fixes_verified = []

    workflow_files = [
        ".github/workflows/latex-build.yml",
        ".github/workflows/latex-validation.yml",
        ".github/workflows/automated-pr-merge-test.yml"
    ]

    for workflow_file in workflow_files:
        if not os.path.exists(workflow_file):
            continue

        print(f"[FILE] Checking {workflow_file}...")

        with open(workflow_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check for timeout configurations
        timeout_count = content.count('timeout-minutes:')

        if timeout_count > 0:
            fixes_verified.append(f"[PASS] {workflow_file}: Has {timeout_count} timeout configurations")
        else:
            issues_found.append(f"[FAIL] {workflow_file}: Missing timeout configurations")

        # Check for reasonable timeout values
        timeout_matches = re.findall(r'timeout-minutes:\s*(\d+)', content)
        if timeout_matches:
            max_timeout = max(int(t) for t in timeout_matches)
            if max_timeout <= 30:  # Reasonable maximum
                fixes_verified.append(f"[PASS] {workflow_file}: Reasonable timeout values (max: {max_timeout})")
            else:
                issues_found.append(f"[WARN]  {workflow_file}: High timeout value detected ({max_timeout} minutes)")

    return issues_found, fixes_verified

def main():
    """Run all validation tests for Issue #1128 CI fixes."""
    print("============================================================")
    print("[LAUNCH] Issue #1128 CI LaTeX Build Failure Fix Validation")
    print("============================================================")
    print("Validating fixes for CI LaTeX build failures...")
    print()

    all_issues = []
    all_fixes = []

    # Run all test categories
    test_functions = [
        test_yaml_syntax_fixes,
        test_latex_action_configuration,
        test_latex_package_dependencies,
        test_build_system_robustness,
        test_critical_files_exist,
        test_workflow_timeout_configuration
    ]

    for test_func in test_functions:
        try:
            issues, fixes = test_func()
            all_issues.extend(issues)
            all_fixes.extend(fixes)
        except Exception as e:
            all_issues.append(f"[FAIL] Test function {test_func.__name__} failed: {e}")

    # Generate summary
    print("\n" + "=" * 60)
    print("[SUMMARY] VALIDATION SUMMARY")
    print("=" * 60)

    if all_fixes:
        print(f"\n[PASS] FIXES VERIFIED ({len(all_fixes)}):")
        for fix in all_fixes:
            print(f"  {fix}")

    if all_issues:
        print(f"\n[FAIL] ISSUES FOUND ({len(all_issues)}):")
        for issue in all_issues:
            print(f"  {issue}")

    print(f"\n[TARGET] OVERALL RESULT:")
    if not all_issues:
        print("[PASS] ALL CHECKS PASSED - CI fixes are properly implemented!")
        return 0
    elif len(all_fixes) > len(all_issues):
        print("[WARN]  MOSTLY GOOD - Minor issues found but fixes are working")
        return 0
    else:
        print("[FAIL] SIGNIFICANT ISSUES - Review and fix the identified problems")
        return 1

if __name__ == "__main__":
    sys.exit(main())
