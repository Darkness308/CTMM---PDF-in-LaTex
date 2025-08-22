#!/usr/bin/env python3
"""
Issue #1157 Fix Validation: Comprehensive CI Fix Validation
==========================================================

This script validates the fixes implemented for Issue #1157, which addresses
CI build failures by standardizing LaTeX action usage, fixing hyperref package
validation logic, and updating validation expectations to match the enhanced
CI pipeline structure.

Key improvements tested:
1. Standardized use of xu-cheng/latex-action@v3 in both workflows
2. Enhanced hyperref validation logic in latex-validation.yml
3. Improved AWK regex patterns to eliminate warnings
4. Updated validation script expectations
"""

import os
import sys
import yaml
import re
import subprocess
from pathlib import Path


def test_latex_action_standardization():
    """Test that both workflows use xu-cheng/latex-action@v3 consistently."""
    print("\n🔧 Testing LaTeX Action Standardization")
    print("=" * 60)
    
    workflow_files = [
        '.github/workflows/latex-build.yml',
        '.github/workflows/latex-validation.yml'
    ]
    
    standardization_success = True
    
    for workflow_file in workflow_files:
        print(f"\n📄 Checking {workflow_file}...")
        
        if not os.path.exists(workflow_file):
            print(f"❌ Workflow file not found: {workflow_file}")
            standardization_success = False
            continue
            
        try:
            with open(workflow_file, 'r') as f:
                content = f.read()
                
            # Check for xu-cheng/latex-action@v3
            xu_cheng_pattern = r'xu-cheng/latex-action@v3'
            if re.search(xu_cheng_pattern, content):
                print(f"✅ Found xu-cheng/latex-action@v3 in {workflow_file}")
            else:
                print(f"❌ xu-cheng/latex-action@v3 not found in {workflow_file}")
                standardization_success = False
                
            # Check that no old actions remain
            old_patterns = [
                r'dante-ev/latex-action',
                r'latex-action@v2',
                r'latex-action@latest'
            ]
            
            for pattern in old_patterns:
                if re.search(pattern, content):
                    print(f"❌ Found deprecated action pattern '{pattern}' in {workflow_file}")
                    standardization_success = False
                    
        except Exception as e:
            print(f"❌ Error analyzing {workflow_file}: {e}")
            standardization_success = False
    
    if standardization_success:
        print("\n✅ LaTeX action standardization validated successfully")
    
    return standardization_success


def test_hyperref_validation_logic():
    """Test the enhanced hyperref validation logic in latex-validation.yml."""
    print("\n🔍 Testing Hyperref Validation Logic")
    print("=" * 60)
    
    workflow_file = '.github/workflows/latex-validation.yml'
    
    if not os.path.exists(workflow_file):
        print(f"❌ Validation workflow not found: {workflow_file}")
        return False
        
    try:
        with open(workflow_file, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error reading {workflow_file}: {e}")
        return False
    
    hyperref_validation_success = True
    
    # Check for enhanced hyperref validation step
    if 'Check hyperref is last core package' in content:
        print("✅ Hyperref validation step found")
    else:
        print("❌ Hyperref validation step not found")
        hyperref_validation_success = False
    
    # Check for robust arithmetic expansion
    if 'next_line=$((hyperref_line + 1))' in content:
        print("✅ Robust arithmetic expansion found")
    else:
        print("❌ Robust arithmetic expansion not found")
        hyperref_validation_success = False
    
    # Check for debug output
    debug_patterns = [
        'echo "Debug: hyperref at line $hyperref_line"',
        'echo "Debug: bookmark at line $bookmark_line"',
        'echo "Debug: checking from line $next_line onward"'
    ]
    
    debug_found = 0
    for pattern in debug_patterns:
        if pattern in content:
            debug_found += 1
    
    if debug_found >= 2:
        print(f"✅ Debug output found ({debug_found}/{len(debug_patterns)} patterns)")
    else:
        print(f"❌ Insufficient debug output ({debug_found}/{len(debug_patterns)} patterns)")
        hyperref_validation_success = False
    
    # Check bookmark package handling
    if 'grep -v \'bookmark\'' in content:
        print("✅ Bookmark package exception handling found")
    else:
        print("❌ Bookmark package exception handling not found")
        hyperref_validation_success = False
    
    return hyperref_validation_success


def test_awk_regex_improvements():
    """Test that AWK regex patterns are properly escaped."""
    print("\n📝 Testing AWK Regex Improvements")
    print("=" * 60)
    
    workflow_file = '.github/workflows/latex-validation.yml'
    
    if not os.path.exists(workflow_file):
        print(f"❌ Validation workflow not found: {workflow_file}")
        return False
        
    try:
        with open(workflow_file, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error reading {workflow_file}: {e}")
        return False
    
    awk_improvements_success = True
    
    # Check for properly escaped AWK patterns - in YAML, LaTeX backslashes become quadruple backslashes
    # Look for the pattern that indicates proper escaping in the YAML file
    if '/\\\\\\\\begin\\\\{document\\\\}/' in content and '/\\\\\\\\usepackage/' in content:
        print("✅ Properly escaped AWK regex pattern found (quadruple backslashes in YAML)")
    elif '/\\\\begin\\\\{document\\\\}/' in content and '/\\\\usepackage/' in content:
        print("✅ Properly escaped AWK regex pattern found (double backslashes in YAML)")
    else:
        print("❌ Properly escaped AWK regex pattern not found")
        awk_improvements_success = False
        
        # Check for problematic old pattern with minimal escaping
        if 'awk \'/\\begin{document}/' in content:
            print("⚠️  Old problematic AWK pattern with minimal escaping still present")
    
    return awk_improvements_success


def test_validation_script_updates():
    """Test that validation scripts have been updated to match new structure."""
    print("\n📋 Testing Validation Script Updates")
    print("=" * 60)
    
    validation_script = 'test_issue_743_validation.py'
    
    if not os.path.exists(validation_script):
        print(f"❌ Validation script not found: {validation_script}")
        return False
        
    try:
        with open(validation_script, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error reading {validation_script}: {e}")
        return False
    
    script_updates_success = True
    
    # Check for xu-cheng/latex-action validation
    if 'xu-cheng/latex-action' in content:
        print("✅ Validation script checks for xu-cheng/latex-action")
    else:
        print("❌ Validation script does not check for xu-cheng/latex-action")
        script_updates_success = False
    
    # Check for proper step validation
    expected_steps = [
        'Set up LaTeX',
        'Enhanced pre-build validation',
        'Check system resources before LaTeX compilation'
    ]
    
    found_steps = 0
    for step in expected_steps:
        if step in content:
            found_steps += 1
    
    if found_steps >= 2:
        print(f"✅ Updated step validation found ({found_steps}/{len(expected_steps)})")
    else:
        print(f"❌ Insufficient step validation updates ({found_steps}/{len(expected_steps)})")
        script_updates_success = False
    
    return script_updates_success


def test_workflow_syntax_validity():
    """Test that all workflow files have valid YAML syntax."""
    print("\n📄 Testing Workflow YAML Syntax Validity")
    print("=" * 60)
    
    workflow_files = [
        '.github/workflows/latex-build.yml',
        '.github/workflows/latex-validation.yml'
    ]
    
    syntax_validity_success = True
    
    for workflow_file in workflow_files:
        print(f"\n🔍 Validating {workflow_file}...")
        
        if not os.path.exists(workflow_file):
            print(f"❌ Workflow file not found: {workflow_file}")
            syntax_validity_success = False
            continue
            
        try:
            with open(workflow_file, 'r') as f:
                yaml.safe_load(f)
            print(f"✅ Valid YAML syntax in {workflow_file}")
        except yaml.YAMLError as e:
            print(f"❌ YAML syntax error in {workflow_file}: {e}")
            syntax_validity_success = False
        except Exception as e:
            print(f"❌ Error validating {workflow_file}: {e}")
            syntax_validity_success = False
    
    return syntax_validity_success


def test_ci_pipeline_consistency():
    """Test overall CI pipeline consistency between workflows."""
    print("\n🔄 Testing CI Pipeline Consistency")
    print("=" * 60)
    
    try:
        # Check latex-build.yml
        with open('.github/workflows/latex-build.yml', 'r') as f:
            build_workflow = yaml.safe_load(f)
            
        # Check latex-validation.yml  
        with open('.github/workflows/latex-validation.yml', 'r') as f:
            validation_workflow = yaml.safe_load(f)
    except Exception as e:
        print(f"❌ Error loading workflows: {e}")
        return False
    
    consistency_success = True
    
    # Check that both workflows use the same LaTeX action version
    build_latex_action = None
    validation_latex_action = None
    
    # Extract LaTeX action from build workflow
    for step in build_workflow.get('jobs', {}).get('build', {}).get('steps', []):
        if 'xu-cheng/latex-action' in str(step.get('uses', '')):
            build_latex_action = step.get('uses')
            break
    
    # Extract LaTeX action from validation workflow
    for step in validation_workflow.get('jobs', {}).get('validate', {}).get('steps', []):
        if 'xu-cheng/latex-action' in str(step.get('uses', '')):
            validation_latex_action = step.get('uses')
            break
    
    if build_latex_action and validation_latex_action:
        if build_latex_action == validation_latex_action:
            print(f"✅ Consistent LaTeX action: {build_latex_action}")
        else:
            print(f"❌ Inconsistent LaTeX actions: {build_latex_action} vs {validation_latex_action}")
            consistency_success = False
    else:
        print("⚠️  Could not find LaTeX actions in both workflows")
        consistency_success = False
    
    # Check for similar package configurations
    build_packages = None
    validation_packages = None
    
    for step in build_workflow.get('jobs', {}).get('build', {}).get('steps', []):
        if 'xu-cheng/latex-action' in str(step.get('uses', '')):
            build_packages = step.get('with', {}).get('extra_system_packages', '')
            break
    
    for step in validation_workflow.get('jobs', {}).get('validate', {}).get('steps', []):
        if 'xu-cheng/latex-action' in str(step.get('uses', '')):
            validation_packages = step.get('with', {}).get('extra_system_packages', '')
            break
    
    if build_packages and validation_packages:
        # Convert to sets for comparison
        build_pkg_set = set(line.strip() for line in build_packages.strip().split('\n') if line.strip())
        validation_pkg_set = set(line.strip() for line in validation_packages.strip().split('\n') if line.strip())
        
        if build_pkg_set == validation_pkg_set:
            print("✅ Consistent package configurations")
        else:
            print("⚠️  Different package configurations (this may be acceptable)")
            print(f"   Build packages: {len(build_pkg_set)} packages")
            print(f"   Validation packages: {len(validation_pkg_set)} packages")
    
    return consistency_success


def run_issue_1157_validation():
    """Run all Issue #1157 fix validation tests."""
    print("=" * 70)
    print("ISSUE #1157 FIX VALIDATION")
    print("CI LaTeX Action Standardization and Workflow Fixes")
    print("=" * 70)
    
    validation_tests = [
        ("LaTeX Action Standardization", test_latex_action_standardization),
        ("Hyperref Validation Logic", test_hyperref_validation_logic),
        ("AWK Regex Improvements", test_awk_regex_improvements),
        ("Validation Script Updates", test_validation_script_updates),
        ("Workflow YAML Syntax Validity", test_workflow_syntax_validity),
        ("CI Pipeline Consistency", test_ci_pipeline_consistency),
    ]
    
    results = []
    
    for test_name, test_func in validation_tests:
        print(f"\n{'='*15} {test_name.upper()} {'='*15}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ ERROR: Test '{test_name}' failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary report
    print("\n" + "=" * 70)
    print("FIX VALIDATION SUMMARY REPORT")
    print("=" * 70)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ISSUE #1157 FIX VALIDATION PASSED!")
        print("\nThe following improvements have been verified:")
        print("  ✓ Standardized xu-cheng/latex-action@v3 usage across workflows")
        print("  ✓ Enhanced hyperref package validation logic with debug output")
        print("  ✓ Improved AWK regex patterns to eliminate warnings")
        print("  ✓ Updated validation scripts to match new workflow structure")
        print("  ✓ Valid YAML syntax in all workflow files")
        print("  ✓ Consistent CI pipeline configuration")
        print("\nCI pipeline is now more robust and standardized.")
        return True
    else:
        print(f"\n❌ {total - passed} validation test(s) failed")
        print("Please address the issues above to complete Issue #1157 requirements.")
        return False


def main():
    """Main entry point for Issue #1157 fix validation."""
    # Ensure we're in the right directory
    if not Path('main.tex').exists():
        print("❌ ERROR: This script must be run from the CTMM repository root")
        print("Expected to find main.tex in current directory")
        sys.exit(1)
    
    success = run_issue_1157_validation()
    
    print("\n" + "=" * 70)
    if success:
        print("ISSUE #1157 FIX VALIDATION: SUCCESS ✅")
        print("All CI standardization and workflow fixes have been validated.")
    else:
        print("ISSUE #1157 FIX VALIDATION: NEEDS ATTENTION ❌")
        print("Please resolve the validation issues before proceeding.")
    print("=" * 70)
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()