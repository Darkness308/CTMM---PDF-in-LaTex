#!/usr/bin/env python3
"""
Test script to validate GitHub Actions workflow consolidation fix.
Ensures all dante-ev/latex-action entries use the same correct version.
"""

import yaml
import os
import sys
from pathlib import Path

def test_latex_action_version_consistency():
    """Test that all workflows using dante-ev/latex-action use the same correct version."""
    print("🔍 Testing LaTeX Action Version Consistency")
    print("=" * 60)
    
    workflow_dir = Path(".github/workflows")
    if not workflow_dir.exists():
        print("❌ Workflow directory not found")
        return False
    
    latex_action_entries = []
    
    # Scan all workflow files for dante-ev/latex-action usage
    for workflow_file in workflow_dir.glob("*.yml"):
        try:
            with open(workflow_file, 'r') as f:
                workflow = yaml.safe_load(f)
            
            # Recursively search for dante-ev/latex-action usage
            def find_latex_actions(obj, path=""):
                if isinstance(obj, dict):
                    for key, value in obj.items():
                        if key == 'uses' and isinstance(value, str) and 'dante-ev/latex-action' in value:
                            latex_action_entries.append({
                                'file': str(workflow_file),
                                'path': path,
                                'uses': value
                            })
                        find_latex_actions(value, f"{path}.{key}" if path else key)
                elif isinstance(obj, list):
                    for i, item in enumerate(obj):
                        find_latex_actions(item, f"{path}[{i}]")
            
            find_latex_actions(workflow)
            
        except Exception as e:
            print(f"❌ Error parsing {workflow_file}: {e}")
            return False
    
    if not latex_action_entries:
        print("ℹ️  No dante-ev/latex-action entries found")
        return True
    
    print(f"Found {len(latex_action_entries)} dante-ev/latex-action entries:")
    for entry in latex_action_entries:
        print(f"  📄 {entry['file']}: {entry['uses']}")
    
    # Check for consistency
    versions = set(entry['uses'] for entry in latex_action_entries)
    
    if len(versions) == 1:
        version = list(versions)[0]
        print(f"✅ All entries use consistent version: {version}")
        
        # Check if it's a valid version (not the problematic v2.0.0)
        if version == 'dante-ev/latex-action@v2.0.0':
            print("❌ Using problematic version v2.0.0 that doesn't exist")
            return False
        elif version == 'dante-ev/latex-action@v2':
            print("✅ Using correct version @v2")
            return True
        else:
            print(f"⚠️  Using version: {version}")
            print("   Consider using @v2 for consistency with issue resolutions")
            return True
    else:
        print("❌ Inconsistent versions found:")
        for version in versions:
            count = sum(1 for entry in latex_action_entries if entry['uses'] == version)
            print(f"   {version}: {count} files")
        return False

def test_no_problematic_versions():
    """Test that no workflow files use known problematic versions."""
    print("\n🚫 Testing for Problematic Versions")
    print("=" * 60)
    
    problematic_versions = [
        'dante-ev/latex-action@v2.0.0',  # Known non-existent version
    ]
    
    workflow_dir = Path(".github/workflows") 
    issues_found = []
    
    for workflow_file in workflow_dir.glob("*.yml"):
        with open(workflow_file, 'r') as f:
            content = f.read()
        
        for version in problematic_versions:
            if version in content:
                issues_found.append(f"{workflow_file}: {version}")
    
    if issues_found:
        print("❌ Found problematic versions:")
        for issue in issues_found:
            print(f"   {issue}")
        return False
    else:
        print("✅ No problematic versions found")
        return True

def test_workflow_yaml_syntax():
    """Test that all workflow files have valid YAML syntax."""
    print("\n📋 Testing Workflow YAML Syntax")
    print("=" * 60)
    
    workflow_dir = Path(".github/workflows")
    all_valid = True
    
    for workflow_file in workflow_dir.glob("*.yml"):
        try:
            with open(workflow_file, 'r') as f:
                yaml.safe_load(f)
            print(f"✅ {workflow_file.name}: Valid YAML")
        except yaml.YAMLError as e:
            print(f"❌ {workflow_file.name}: Invalid YAML - {e}")
            all_valid = False
        except Exception as e:
            print(f"❌ {workflow_file.name}: Error - {e}")
            all_valid = False
    
    return all_valid

def main():
    """Run all validation tests."""
    print("🧪 GitHub Actions Workflow Consolidation Fix Validation")
    print("=" * 60)
    print("Testing workflow file consistency and syntax")
    print()
    
    tests = [
        ("LaTeX Action Version Consistency", test_latex_action_version_consistency),
        ("No Problematic Versions", test_no_problematic_versions),
        ("Workflow YAML Syntax", test_workflow_yaml_syntax),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name}: Error - {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\nTests passed: {passed}/{len(results)}")
    
    if passed == len(results):
        print("🎉 ALL TESTS PASSED - Workflow consolidation fix is working correctly!")
        print("\nThe GitHub Actions workflows should now:")
        print("- Use consistent dante-ev/latex-action versions")
        print("- Avoid version resolution errors")
        print("- Successfully execute PDF build processes")
        return True
    else:
        print("💥 Some tests failed. Please review the configuration.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)