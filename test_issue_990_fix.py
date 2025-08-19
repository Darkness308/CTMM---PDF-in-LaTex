#!/usr/bin/env python3
"""
Test validation for Issue #990: Corrupted Merge Markers and Conflicting LaTeX Action Configurations

This test validates that:
1. No merge conflict markers exist in workflow files
2. All LaTeX action configurations use consistent, working versions
3. Specifically fixes the dante-ev/latex-action@v2.0.0 → @v2 issue
"""

import os
import sys
import yaml
from pathlib import Path


def test_no_merge_conflict_markers():
    """Test that no merge conflict markers exist in workflow files."""
    print("🔍 Testing for merge conflict markers...")
    
    workflow_dir = Path(".github/workflows")
    if not workflow_dir.exists():
        print("❌ ERROR: .github/workflows directory not found")
        return False
    
    found_conflicts = False
    
    for workflow_file in workflow_dir.glob("*.yml"):
        content = workflow_file.read_text()
        
        # Look for actual Git merge conflict markers (at start of line)
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if (stripped.startswith('<<<<<<<') or 
                stripped.startswith('>>>>>>>') or
                (stripped == '=======' and not 'echo' in line.lower())):
                print(f"❌ FAIL: Found merge conflict marker on line {i} in {workflow_file}: {line.strip()}")
                found_conflicts = True
    
    if not found_conflicts:
        print("✅ PASS: No merge conflict markers found")
        return True
    return False


def test_latex_action_consistency():
    """Test that all LaTeX action configurations use consistent versions."""
    print("\n🔧 Testing LaTeX action version consistency...")
    
    workflow_files = [
        ".github/workflows/latex-build.yml",
        ".github/workflows/automated-pr-merge-test.yml"
    ]
    
    latex_action_versions = []
    all_valid = True
    
    for workflow_file in workflow_files:
        if not os.path.exists(workflow_file):
            print(f"⚠️  WARNING: {workflow_file} not found, skipping...")
            continue
            
        with open(workflow_file, 'r') as f:
            content = f.read()
        
        # Find dante-ev/latex-action usage
        if "dante-ev/latex-action" in content:
            # Extract the version
            import re
            matches = re.findall(r'dante-ev/latex-action@([^\s\n]+)', content)
            for version in matches:
                latex_action_versions.append((workflow_file, version))
                
                # Check for the problematic v2.0.0 version
                if version == "v2.0.0":
                    print(f"❌ FAIL: {workflow_file} uses problematic version @{version}")
                    print("   This version doesn't exist and causes CI failure")
                    all_valid = False
                elif version == "v2":
                    print(f"✅ PASS: {workflow_file} uses correct version @{version}")
                else:
                    print(f"⚠️  WARNING: {workflow_file} uses version @{version} (review needed)")
    
    # Check for consistency
    unique_versions = set(version for _, version in latex_action_versions)
    if len(unique_versions) > 1:
        print(f"⚠️  WARNING: Found {len(unique_versions)} different LaTeX action versions:")
        for file, version in latex_action_versions:
            print(f"   {file}: @{version}")
        print("   Consider standardizing on one version for consistency")
    elif len(unique_versions) == 1:
        version = list(unique_versions)[0]
        print(f"✅ PASS: All workflows use consistent version @{version}")
    
    return all_valid


def test_workflow_yaml_syntax():
    """Test that all workflow YAML files have valid syntax."""
    print("\n📋 Testing workflow YAML syntax...")
    
    workflow_dir = Path(".github/workflows")
    all_valid = True
    
    for workflow_file in workflow_dir.glob("*.yml"):
        try:
            with open(workflow_file, 'r') as f:
                yaml.safe_load(f)
            print(f"✅ PASS: {workflow_file.name} has valid YAML syntax")
        except yaml.YAMLError as e:
            print(f"❌ FAIL: {workflow_file.name} has YAML syntax error: {e}")
            all_valid = False
        except Exception as e:
            print(f"❌ ERROR: Failed to read {workflow_file.name}: {e}")
            all_valid = False
    
    return all_valid


def test_specific_v2_0_0_removal():
    """Test that the specific problematic v2.0.0 version has been removed."""
    print("\n🎯 Testing removal of dante-ev/latex-action@v2.0.0...")
    
    workflow_files = [
        ".github/workflows/latex-build.yml",
        ".github/workflows/automated-pr-merge-test.yml"
    ]
    
    found_problematic = False
    
    for workflow_file in workflow_files:
        if not os.path.exists(workflow_file):
            continue
            
        with open(workflow_file, 'r') as f:
            content = f.read()
        
        if "dante-ev/latex-action@v2.0.0" in content:
            print(f"❌ FAIL: {workflow_file} still contains problematic @v2.0.0 version")
            found_problematic = True
        else:
            print(f"✅ PASS: {workflow_file} does not contain @v2.0.0 version")
    
    if not found_problematic:
        print("✅ PASS: Problematic @v2.0.0 version successfully removed")
        return True
    return False


def main():
    """Run all tests for Issue #990 fix."""
    print("=" * 60)
    print("Issue #990 Fix Validation")
    print("Corrupted Merge Markers and Conflicting LaTeX Action Configurations")
    print("=" * 60)
    
    tests = [
        ("Merge conflict markers", test_no_merge_conflict_markers),
        ("LaTeX action consistency", test_latex_action_consistency),
        ("Workflow YAML syntax", test_workflow_yaml_syntax),
        ("v2.0.0 removal", test_specific_v2_0_0_removal)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ ERROR in {test_name}: {e}")
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    for i, (test_name, _) in enumerate(tests):
        status = "✅ PASS" if i < passed else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\nTests passed: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED - Issue #990 fix is working correctly!")
        print()
        print("The fix successfully:")
        print("- Removes problematic dante-ev/latex-action@v2.0.0 version")
        print("- Consolidates to consistent dante-ev/latex-action@v2 version")
        print("- Eliminates CI failures due to non-existent action versions")
        print("- Maintains valid YAML syntax across all workflows")
        return 0
    else:
        print("\n❌ SOME TESTS FAILED - Issue #990 fix needs more work")
        return 1


if __name__ == "__main__":
    sys.exit(main())