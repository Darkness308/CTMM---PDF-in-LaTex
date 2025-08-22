#!/usr/bin/env python3
"""
Test Issue #1141 Fix: CI Validation Failure - LaTeX Action Version Update

This test validates that the LaTeX action version issue that caused the CI failure
in the LaTeX Validation workflow has been properly resolved.

Issue: "Unable to resolve action `dante-ev/latex-action@v2`, unable to find version `v2`"
Solution: Update to xu-cheng/latex-action@v3 (proven stable version)
"""

import os
import sys
import yaml
import re

def test_latex_action_version_fix():
    """Test that workflows use the correct LaTeX action version."""
    print("\n🔧 Testing LaTeX Action Version Fix")
    print("=" * 60)
    
    workflow_files = [
        '.github/workflows/latex-validation.yml',
        '.github/workflows/latex-build.yml'
    ]
    
    version_fix_success = True
    
    for workflow_file in workflow_files:
        print(f"\n📄 Checking {workflow_file}...")
        
        if not os.path.exists(workflow_file):
            print(f"❌ Workflow file not found: {workflow_file}")
            version_fix_success = False
            continue
            
        try:
            with open(workflow_file, 'r') as f:
                content = f.read()
                
            # Check that no dante-ev LaTeX actions remain
            dante_ev_pattern = r'dante-ev/latex-action@'
            if re.search(dante_ev_pattern, content):
                print(f"❌ Found old dante-ev/latex-action in {workflow_file}")
                version_fix_success = False
            else:
                print(f"✅ No old dante-ev/latex-action found")
                
            # Check that xu-cheng/latex-action@v3 is used
            xu_cheng_pattern = r'xu-cheng/latex-action@v3'
            if re.search(xu_cheng_pattern, content):
                print(f"✅ Found xu-cheng/latex-action@v3")
            else:
                print(f"❌ xu-cheng/latex-action@v3 not found in {workflow_file}")
                version_fix_success = False
                
        except Exception as e:
            print(f"❌ Error analyzing {workflow_file}: {e}")
            version_fix_success = False
    
    return version_fix_success

def test_workflow_yaml_syntax():
    """Test that workflow YAML files have valid syntax after fixes."""
    print("\n📋 Testing Workflow YAML Syntax")
    print("=" * 60)
    
    workflow_files = [
        '.github/workflows/latex-validation.yml',
        '.github/workflows/latex-build.yml'
    ]
    
    syntax_valid = True
    
    for workflow_file in workflow_files:
        print(f"\n📄 Validating YAML syntax in {workflow_file}...")
        
        if not os.path.exists(workflow_file):
            print(f"❌ Workflow file not found: {workflow_file}")
            syntax_valid = False
            continue
            
        try:
            with open(workflow_file, 'r') as f:
                yaml.safe_load(f)
            print(f"✅ YAML syntax valid in {workflow_file}")
        except yaml.YAMLError as e:
            print(f"❌ YAML syntax error in {workflow_file}: {e}")
            syntax_valid = False
        except Exception as e:
            print(f"❌ Error reading {workflow_file}: {e}")
            syntax_valid = False
    
    return syntax_valid

def test_no_merge_conflict_markers():
    """Test that no git merge conflict markers remain in workflow files."""
    print("\n🔍 Testing for Merge Conflict Markers")
    print("=" * 60)
    
    workflow_files = [
        '.github/workflows/latex-validation.yml',
        '.github/workflows/latex-build.yml'
    ]
    
    no_conflicts = True
    
    for workflow_file in workflow_files:
        print(f"\n📄 Checking {workflow_file} for merge conflict markers...")
        
        if not os.path.exists(workflow_file):
            print(f"❌ Workflow file not found: {workflow_file}")
            no_conflicts = False
            continue
            
        try:
            with open(workflow_file, 'r') as f:
                content = f.read()
                
            # Check for git merge conflict markers (with spaces)
            conflict_patterns = [
                r'<<<<<<< ',
                r'>>>>>>> ',
                r'^=======$'  # Match only lines that are exactly =======
            ]
            
            conflicts_found = []
            lines = content.splitlines()
            for line_num, line in enumerate(lines, 1):
                for pattern in conflict_patterns:
                    if re.match(pattern, line.strip()):
                        conflicts_found.append(f"Line {line_num}: {line.strip()}")
                    
            # Check for branch names that might indicate merge conflicts
            branch_patterns = [
                r'^copilot/fix-\d+$',
                r'^main$'
            ]
            
            for line_num, line in enumerate(content.splitlines(), 1):
                line = line.strip()
                for pattern in branch_patterns:
                    if re.match(pattern, line):
                        conflicts_found.append(f"Line {line_num}: {line}")
                        
            if conflicts_found:
                print(f"❌ Merge conflict markers found in {workflow_file}:")
                for conflict in conflicts_found:
                    print(f"   {conflict}")
                no_conflicts = False
            else:
                print(f"✅ No merge conflict markers found")
                
        except Exception as e:
            print(f"❌ Error analyzing {workflow_file}: {e}")
            no_conflicts = False
    
    return no_conflicts

def test_workflow_action_consistency():
    """Test that all workflow files use consistent action versions."""
    print("\n🔄 Testing Action Version Consistency")
    print("=" * 60)
    
    workflow_files = [
        '.github/workflows/latex-validation.yml',
        '.github/workflows/latex-build.yml',
        '.github/workflows/automated-pr-merge-test.yml'
    ]
    
    consistency_success = True
    latex_actions_found = {}
    
    for workflow_file in workflow_files:
        print(f"\n📄 Checking action versions in {workflow_file}...")
        
        if not os.path.exists(workflow_file):
            print(f"⚠️  Workflow file not found: {workflow_file} (optional)")
            continue
            
        try:
            with open(workflow_file, 'r') as f:
                content = f.read()
                
            # Find all LaTeX actions
            latex_action_pattern = r'uses:\s*([\w-]+/latex-action@[^\s]+)'
            matches = re.findall(latex_action_pattern, content)
            
            for match in matches:
                if match not in latex_actions_found:
                    latex_actions_found[match] = []
                latex_actions_found[match].append(workflow_file)
                
        except Exception as e:
            print(f"❌ Error analyzing {workflow_file}: {e}")
            consistency_success = False
    
    print(f"\n📊 LaTeX Action Version Summary:")
    for action, files in latex_actions_found.items():
        print(f"   {action} used in: {', '.join(files)}")
        
    # Check that all use xu-cheng/latex-action@v3
    expected_action = "xu-cheng/latex-action@v3"
    for action in latex_actions_found.keys():
        if action != expected_action:
            print(f"❌ Inconsistent action version: {action} (expected {expected_action})")
            consistency_success = False
    
    if consistency_success and expected_action in latex_actions_found:
        print(f"✅ All workflows use consistent action version: {expected_action}")
    
    return consistency_success

def main():
    """Run all validation tests for Issue #1141 fix."""
    print("🎯 Issue #1141 Fix Validation: CI LaTeX Action Version Update")
    print("=" * 80)
    print("Testing that the LaTeX action version issue causing CI failures has been resolved.")
    print("=" * 80)
    
    all_tests_passed = True
    
    # Run all tests
    tests = [
        ("LaTeX Action Version Fix", test_latex_action_version_fix),
        ("Workflow YAML Syntax", test_workflow_yaml_syntax),
        ("No Merge Conflict Markers", test_no_merge_conflict_markers),
        ("Action Version Consistency", test_workflow_action_consistency)
    ]
    
    test_results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            test_results.append((test_name, result))
            if not result:
                all_tests_passed = False
        except Exception as e:
            print(f"❌ Test {test_name} failed with exception: {e}")
            test_results.append((test_name, False))
            all_tests_passed = False
    
    # Print summary
    print("\n" + "=" * 80)
    print("📊 VALIDATION SUMMARY")
    print("=" * 80)
    
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\nTests passed: {sum(1 for _, result in test_results if result)}/{len(test_results)}")
    
    if all_tests_passed:
        print("\n🎉 ALL TESTS PASSED! Issue #1141 fix validated successfully.")
        print("\nKey improvements confirmed:")
        print("• LaTeX action version updated to xu-cheng/latex-action@v3 ✅")
        print("• All workflow YAML syntax is valid ✅")
        print("• No merge conflict markers remain ✅")
        print("• Consistent action versions across all workflows ✅")
        print("\n✅ CI validation workflow should now pass without the action resolution error.")
    else:
        print("\n❌ Some tests failed. Please review the issues above.")
        
    return all_tests_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)