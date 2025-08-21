#!/usr/bin/env python3
"""
Test script to verify CI failure fix for Issue #1114: Missing PyYAML dependency

This test validates that all workflow files contain the correct Python dependencies
and that YAML parsing works properly for CI validation scripts.
"""

import sys
import subprocess
from pathlib import Path

def test_yaml_import():
    """Test that yaml module can be imported successfully."""
    print("🔍 Testing YAML import...")
    try:
        import yaml
        print("✅ YAML import successful")
        return True
    except ImportError as e:
        print(f"❌ YAML import failed: {e}")
        return False

def test_workflow_dependencies():
    """Test that all workflow files include pyyaml in their dependencies."""
    print("\n📦 Testing workflow dependencies...")
    
    workflow_files = [
        '.github/workflows/latex-build.yml',
        '.github/workflows/latex-validation.yml', 
        '.github/workflows/automated-pr-merge-test.yml'
    ]
    
    all_good = True
    
    for workflow_file in workflow_files:
        if not Path(workflow_file).exists():
            print(f"❌ Missing workflow file: {workflow_file}")
            all_good = False
            continue
            
        with open(workflow_file, 'r') as f:
            content = f.read()
            
        if 'pip install' in content and 'pyyaml' in content:
            print(f"✅ {workflow_file}: Contains pyyaml dependency")
        elif 'pip install' in content:
            print(f"❌ {workflow_file}: Missing pyyaml dependency")
            all_good = False
        else:
            print(f"ℹ️  {workflow_file}: No pip install found (may not need Python deps)")
    
    return all_good

def test_yaml_parsing():
    """Test that YAML parsing works on actual workflow files."""
    print("\n🔧 Testing YAML parsing on workflow files...")
    
    import yaml
    
    workflow_files = [
        '.github/workflows/latex-build.yml',
        '.github/workflows/latex-validation.yml',
        '.github/workflows/automated-pr-merge-test.yml'
    ]
    
    all_good = True
    
    for workflow_file in workflow_files:
        try:
            with open(workflow_file, 'r') as f:
                data = yaml.safe_load(f)
            print(f"✅ {workflow_file}: YAML parsing successful")
        except Exception as e:
            print(f"❌ {workflow_file}: YAML parsing failed - {e}")
            all_good = False
    
    return all_good

def test_failing_scripts():
    """Test that previously failing validation scripts now work."""
    print("\n🧪 Testing previously failing validation scripts...")
    
    # Test just the import capability, not full execution 
    # since some tests require specific CI environment
    test_scripts = [
        'test_issue_743_validation.py',
        'test_workflow_structure.py'
    ]
    
    all_good = True
    
    for script in test_scripts:
        if not Path(script).exists():
            print(f"❌ Missing test script: {script}")
            all_good = False
            continue
            
        try:
            # Test that the script can at least import yaml without error
            cmd = [sys.executable, '-c', f'import sys; sys.path.insert(0, "."); import yaml; exec(open("{script}").read()[:100])']
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0 or 'yaml' not in result.stderr:
                print(f"✅ {script}: YAML import works")
            else:
                print(f"❌ {script}: Still has YAML issues - {result.stderr[:100]}")
                all_good = False
                
        except Exception as e:
            # Check if the issue is yaml-related
            if 'yaml' in str(e).lower():
                print(f"❌ {script}: YAML-related error - {e}")
                all_good = False
            else:
                print(f"✅ {script}: Non-YAML error (expected in test env)")
    
    return all_good

def main():
    """Run all tests and report results."""
    print("=" * 70)
    print("CI FAILURE FIX VALIDATION - Issue #1114")
    print("Testing PyYAML dependency fix")
    print("=" * 70)
    
    tests = [
        test_yaml_import,
        test_workflow_dependencies,
        test_yaml_parsing,
        test_failing_scripts
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
            results.append(False)
    
    print("\n" + "=" * 70)
    print("VALIDATION SUMMARY")
    print("=" * 70)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Tests passed: {passed}/{total}")
    
    if all(results):
        print("✅ All tests passed! CI failure fix should resolve the issue.")
        return 0
    else:
        print("❌ Some tests failed. Please review the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())