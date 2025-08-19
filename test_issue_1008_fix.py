#!/usr/bin/env python3
"""
Test script to validate Issue #1008 fix
Verifies GitHub Actions workflow consolidation and merge conflict resolution
"""

import yaml
import os
import sys
from pathlib import Path


def test_consistent_latex_action_versions():
    """Test that all workflows use consistent dante-ev/latex-action versions"""
    print("🔍 Testing LaTeX Action Version Consistency")
    print("=" * 60)
    
    workflow_files = [
        '.github/workflows/latex-build.yml',
        '.github/workflows/automated-pr-merge-test.yml'
    ]
    
    found_versions = {}
    all_valid = True
    
    for workflow_path in workflow_files:
        if not os.path.exists(workflow_path):
            print(f"⚠️  Warning: {workflow_path} not found")
            continue
            
        try:
            with open(workflow_path, 'r') as f:
                workflow = yaml.safe_load(f)
        except Exception as e:
            print(f"❌ ERROR: Failed to parse {workflow_path}: {e}")
            all_valid = False
            continue
        
        # Find dante-ev/latex-action usage
        latex_actions = find_latex_actions_in_workflow(workflow)
        
        if latex_actions:
            for action_usage in latex_actions:
                print(f"📄 {workflow_path}: {action_usage}")
                found_versions[workflow_path] = action_usage
                
                # Check for problematic versions
                if "@v2.0.0" in action_usage:
                    print(f"❌ FAIL: {workflow_path} still uses problematic version @v2.0.0")
                    print("   This version doesn't exist and will cause CI failure")
                    all_valid = False
                elif "@v2" in action_usage and action_usage.endswith("@v2"):
                    print(f"✅ PASS: {workflow_path} uses correct version @v2")
                else:
                    print(f"⚠️  WARNING: {workflow_path} uses unexpected version: {action_usage}")
    
    # Check consistency
    unique_versions = set(found_versions.values())
    if len(unique_versions) > 1:
        print(f"\n❌ INCONSISTENCY: Found {len(unique_versions)} different versions:")
        for file, version in found_versions.items():
            print(f"   {file}: {version}")
        all_valid = False
    elif len(unique_versions) == 1:
        version = list(unique_versions)[0]
        print(f"\n✅ CONSISTENCY: All workflows use {version}")
    
    return all_valid


def find_latex_actions_in_workflow(workflow_data):
    """Recursively find dante-ev/latex-action usage in workflow data"""
    actions = []
    
    def search_dict(obj):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key == 'uses' and isinstance(value, str) and 'dante-ev/latex-action' in value:
                    actions.append(value)
                else:
                    search_dict(value)
        elif isinstance(obj, list):
            for item in obj:
                search_dict(item)
    
    search_dict(workflow_data)
    return actions


def test_no_merge_conflict_markers():
    """Test that there are no merge conflict markers in workflow files"""
    print("\n🔍 Testing for Merge Conflict Markers")
    print("=" * 60)
    
    workflow_dir = Path('.github/workflows')
    
    all_clean = True
    
    for workflow_file in workflow_dir.glob('*.yml'):
        try:
            with open(workflow_file, 'r') as f:
                content = f.read()
                
            conflicts_found = False
            for line_num, line in enumerate(content.splitlines(), 1):
                stripped = line.strip()
                
                # Look for actual merge conflict markers at start of line or standalone
                if (stripped.startswith('<<<<<<<') or 
                    stripped.startswith('>>>>>>>') or
                    (stripped == '=======' or stripped.startswith('======= '))):
                    
                    # Exclude echo statements and comments
                    if 'echo' not in line and '#' not in line:
                        print(f"❌ CONFLICT MARKER: {workflow_file}:{line_num} - {stripped}")
                        conflicts_found = True
                        all_clean = False
            
            if not conflicts_found:
                print(f"✅ CLEAN: {workflow_file} - No merge conflict markers")
        except Exception as e:
            print(f"❌ ERROR: Failed to read {workflow_file}: {e}")
            all_clean = False
    
    return all_clean


def test_workflow_syntax():
    """Test that all workflow files have valid YAML syntax"""
    print("\n⚙️  Testing Workflow YAML Syntax")
    print("=" * 60)
    
    workflow_dir = Path('.github/workflows')
    all_valid = True
    
    for workflow_file in workflow_dir.glob('*.yml'):
        try:
            with open(workflow_file, 'r') as f:
                yaml.safe_load(f)
            print(f"✅ VALID: {workflow_file} - YAML syntax OK")
        except yaml.YAMLError as e:
            print(f"❌ INVALID: {workflow_file} - YAML syntax error: {e}")
            all_valid = False
        except Exception as e:
            print(f"❌ ERROR: {workflow_file} - {e}")
            all_valid = False
    
    return all_valid


def main():
    """Run all tests for Issue #1008 fix"""
    print("🧪 GitHub Actions Workflow Consolidation - Issue #1008 Fix Validation")
    print("=" * 80)
    
    tests = [
        ("LaTeX Action Version Consistency", test_consistent_latex_action_versions),
        ("Merge Conflict Markers", test_no_merge_conflict_markers),
        ("Workflow YAML Syntax", test_workflow_syntax),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running: {test_name}")
        try:
            if test_func():
                print(f"✅ PASSED: {test_name}")
                passed += 1
            else:
                print(f"❌ FAILED: {test_name}")
        except Exception as e:
            print(f"❌ ERROR in {test_name}: {e}")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! GitHub Actions workflow issues have been resolved.")
        return True
    else:
        print("⚠️  Some tests failed. Please review the issues above.")
        return False


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)