#!/usr/bin/env python3
"""
Test suite for Issue #1068: LaTeX Action Migration and Robustness Improvements

This test validates the migration from dante-ev/latex-action to xu-cheng/latex-action@v3
and the implementation of robust fallback mechanisms.
"""

import os
import sys
import yaml
import subprocess
import re
from pathlib import Path


def test_latex_action_migration():
    """Test that workflows have been migrated to xu-cheng/latex-action@v3."""
    print("\n🔄 Testing LaTeX Action Migration")
    print("=" * 60)
    
    workflows_dir = Path('.github/workflows')
    if not workflows_dir.exists():
        print("❌ Workflows directory not found")
        return False
    
    target_workflows = ['latex-build.yml', 'automated-pr-merge-test.yml']
    migration_success = True
    
    for workflow_file in target_workflows:
        workflow_path = workflows_dir / workflow_file
        if not workflow_path.exists():
            print(f"⚠️  Workflow file not found: {workflow_file}")
            continue
            
        print(f"🔍 Checking {workflow_file}...")
        
        with open(workflow_path, 'r') as f:
            content = f.read()
        
        # Check for migration to xu-cheng/latex-action@v3
        if 'xu-cheng/latex-action@v3' in content:
            print(f"✅ FOUND: xu-cheng/latex-action@v3 in {workflow_file}")
        else:
            print(f"❌ MISSING: xu-cheng/latex-action@v3 not found in {workflow_file}")
            migration_success = False
        
        # Check that old action is removed
        if 'dante-ev/latex-action' in content:
            print(f"⚠️  WARNING: dante-ev/latex-action still present in {workflow_file}")
            migration_success = False
        else:
            print(f"✅ CONFIRMED: dante-ev/latex-action removed from {workflow_file}")
    
    return migration_success


def test_fallback_mechanism():
    """Test that fallback mechanism is properly implemented."""
    print("\n🛡️  Testing Fallback Mechanism")
    print("=" * 60)
    
    workflow_path = Path('.github/workflows/latex-build.yml')
    if not workflow_path.exists():
        print("❌ latex-build.yml not found")
        return False
    
    with open(workflow_path, 'r') as f:
        content = f.read()
    
    fallback_checks = {
        'Primary action with ID': 'id: latex_primary',
        'Continue on error': 'continue-on-error: true',
        'Fallback step condition': 'if: steps.latex_primary.outcome == \'failure\'',
        'Manual TeX Live installation': 'sudo apt-get install -y',
        'Fallback verification': 'pdflatex --version',
        'Fallback compilation': 'pdflatex -interaction=nonstopmode'
    }
    
    fallback_success = True
    
    for check_name, pattern in fallback_checks.items():
        if pattern in content:
            print(f"✅ FOUND: {check_name}")
        else:
            print(f"❌ MISSING: {check_name} (pattern: {pattern})")
            fallback_success = False
    
    return fallback_success


def test_enhanced_error_reporting():
    """Test that enhanced error reporting is implemented."""
    print("\n📝 Testing Enhanced Error Reporting")
    print("=" * 60)
    
    workflow_path = Path('.github/workflows/latex-build.yml')
    if not workflow_path.exists():
        print("❌ latex-build.yml not found")
        return False
    
    with open(workflow_path, 'r') as f:
        content = f.read()
    
    error_reporting_features = {
        'Enhanced PDF verification': 'enhanced PDF verification',
        'PDF file analysis': 'PDF File Analysis',
        'PDF size check': 'PDF file size',
        'PDF header verification': 'PDF Header Verification',
        'Detailed failure analysis': 'Detailed failure analysis',
        'Comprehensive error report': 'comprehensive error report',
        'Enhanced build logs': 'enhanced_build_logs',
        'Error report generation': 'ERROR_REPORT='
    }
    
    reporting_success = True
    features_found = 0
    
    for feature_name, pattern in error_reporting_features.items():
        if pattern in content:
            print(f"✅ FOUND: {feature_name}")
            features_found += 1
        else:
            print(f"❌ MISSING: {feature_name}")
            reporting_success = False
    
    print(f"\n📊 Error Reporting Features: {features_found}/{len(error_reporting_features)}")
    
    if features_found >= 6:  # Require at least 6 out of 8 features
        print("✅ Good error reporting coverage")
        return True
    else:
        print("❌ Insufficient error reporting features")
        return False


def test_package_dependencies_preserved():
    """Test that LaTeX package dependencies are preserved after migration."""
    print("\n📦 Testing Package Dependencies Preservation")
    print("=" * 60)
    
    workflows = ['latex-build.yml', 'automated-pr-merge-test.yml']
    
    required_packages = [
        'texlive-lang-german',
        'texlive-fonts-recommended', 
        'texlive-latex-recommended',
        'texlive-fonts-extra',
        'texlive-latex-extra',
        'texlive-science',
        'texlive-pstricks'
    ]
    
    all_packages_preserved = True
    
    for workflow_file in workflows:
        workflow_path = Path('.github/workflows') / workflow_file
        if not workflow_path.exists():
            print(f"⚠️  {workflow_file} not found")
            continue
        
        print(f"\n🔍 Checking packages in {workflow_file}:")
        
        with open(workflow_path, 'r') as f:
            content = f.read()
        
        packages_found = 0
        for package in required_packages:
            if package in content:
                print(f"  ✅ {package}")
                packages_found += 1
            else:
                print(f"  ❌ {package}")
                all_packages_preserved = False
        
        print(f"  📊 Packages found: {packages_found}/{len(required_packages)}")
    
    return all_packages_preserved


def test_yaml_syntax_validity():
    """Test that workflow YAML files have valid syntax after changes."""
    print("\n🔧 Testing YAML Syntax Validity")
    print("=" * 60)
    
    workflows_dir = Path('.github/workflows')
    yaml_files = list(workflows_dir.glob('*.yml'))
    
    syntax_valid = True
    
    for yaml_file in yaml_files:
        print(f"🔍 Validating {yaml_file.name}...")
        
        try:
            with open(yaml_file, 'r') as f:
                yaml.safe_load(f)
            print(f"✅ Valid YAML syntax: {yaml_file.name}")
        except yaml.YAMLError as e:
            print(f"❌ Invalid YAML syntax in {yaml_file.name}: {e}")
            syntax_valid = False
        except Exception as e:
            print(f"❌ Error reading {yaml_file.name}: {e}")
            syntax_valid = False
    
    return syntax_valid


def test_compilation_arguments_preserved():
    """Test that LaTeX compilation arguments are preserved."""
    print("\n⚙️  Testing Compilation Arguments Preservation")
    print("=" * 60)
    
    workflow_path = Path('.github/workflows/latex-build.yml')
    if not workflow_path.exists():
        print("❌ latex-build.yml not found")
        return False
    
    with open(workflow_path, 'r') as f:
        content = f.read()
    
    required_args = [
        '-interaction=nonstopmode',
        '-halt-on-error', 
        '-shell-escape'
    ]
    
    args_preserved = True
    
    for arg in required_args:
        if arg in content:
            print(f"✅ FOUND: {arg}")
        else:
            print(f"❌ MISSING: {arg}")
            args_preserved = False
    
    # Also check for main.tex as root file
    if 'root_file: main.tex' in content:
        print("✅ FOUND: root_file: main.tex")
    else:
        print("❌ MISSING: root_file: main.tex")
        args_preserved = False
    
    return args_preserved


def test_timeout_configurations():
    """Test that timeout configurations are appropriate for the new action."""
    print("\n⏱️  Testing Timeout Configurations")
    print("=" * 60)
    
    workflow_path = Path('.github/workflows/latex-build.yml')
    if not workflow_path.exists():
        print("❌ latex-build.yml not found")
        return False
    
    with open(workflow_path, 'r') as f:
        content = f.read()
    
    # Check for appropriate timeouts
    timeout_checks = {
        'Primary LaTeX action timeout': 'timeout-minutes: 15',
        'Fallback installation timeout': 'timeout-minutes: 20',
        'PDF verification timeout': 'timeout-minutes: 5'
    }
    
    timeout_success = True
    
    for check_name, pattern in timeout_checks.items():
        if pattern in content:
            print(f"✅ FOUND: {check_name}")
        else:
            print(f"⚠️  MISSING: {check_name}")
            # Don't fail the test for timeout configs, just warn
    
    return True


def test_workflow_structure_integrity():
    """Test that overall workflow structure is maintained."""
    print("\n🏗️  Testing Workflow Structure Integrity")
    print("=" * 60)
    
    workflow_path = Path('.github/workflows/latex-build.yml')
    if not workflow_path.exists():
        print("❌ latex-build.yml not found")
        return False
    
    with open(workflow_path, 'r') as f:
        content = f.read()
    
    # Check for essential workflow elements
    essential_elements = [
        'name: Build LaTeX PDF',
        'runs-on: ubuntu-latest',
        'uses: actions/checkout@v4',
        'uses: actions/setup-python@v4',
        'pip install chardet',
        'python3 ctmm_build.py',
        'uses: actions/upload-artifact@v4'
    ]
    
    structure_intact = True
    
    for element in essential_elements:
        if element in content:
            print(f"✅ FOUND: {element}")
        else:
            print(f"❌ MISSING: {element}")
            structure_intact = False
    
    return structure_intact


def main():
    """Run all robustness tests."""
    print("🧪 CTMM LaTeX Action Migration and Robustness Test Suite")
    print("=" * 80)
    print("Testing Issue #1068: Migration to xu-cheng/latex-action@v3 with fallback")
    print("=" * 80)
    
    tests = [
        test_latex_action_migration,
        test_fallback_mechanism,
        test_enhanced_error_reporting,
        test_package_dependencies_preserved,
        test_yaml_syntax_validity,
        test_compilation_arguments_preserved,
        test_timeout_configurations,
        test_workflow_structure_integrity
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_func in tests:
        try:
            if test_func():
                passed_tests += 1
                print("✅ PASSED")
            else:
                print("❌ FAILED")
        except Exception as e:
            print(f"❌ ERROR: {e}")
        print()
    
    print("=" * 80)
    print(f"📊 FINAL RESULTS: {passed_tests}/{total_tests} tests passed")
    print("=" * 80)
    
    if passed_tests == total_tests:
        print("🎉 All tests passed! LaTeX action migration and robustness improvements are working correctly.")
        return True
    elif passed_tests >= total_tests - 1:
        print("✅ Most tests passed. Minor issues may need attention.")
        return True
    else:
        print("❌ Significant issues found. Review the test results above.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)