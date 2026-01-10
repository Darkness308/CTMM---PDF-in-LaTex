#!/usr/bin/env python3
"""
Test script for Issue #1145 - Enhanced VS Code Build Tasks Implementation
Validates that the comprehensive module generation system is working correctly.
"""

import json
import os
import subprocess
import sys

def test_vscode_tasks():
    """Test that VS Code tasks are properly configured."""
    print("🔧 Testing VS Code tasks configuration...")

    # Load tasks.json
    tasks_file = ".vscode/tasks.json"
    if not os.path.exists(tasks_file):
        print(f"❌ {tasks_file} not found")
        return False

    with open(tasks_file, 'r') as f:
        tasks_config = json.load(f)

    # Expected CTMM tasks
    expected_tasks = [
        "CTMM: Build Complete System",
        "CTMM: Build Single Module",
        "CTMM: Generate Module",
        "CTMM: Clean Build Directory",
        "CTMM: Create Build Directory",
        "CTMM: Clean and Build"
    ]

    found_tasks = [task['label'] for task in tasks_config['tasks']]

    print(f"✅ Found {len(tasks_config['tasks'])} total tasks")

    # Check for required tasks
    missing_tasks = [task for task in expected_tasks if task not in found_tasks]
    if missing_tasks:
        print(f"❌ Missing tasks: {missing_tasks}")
        return False

    print("✅ All required CTMM tasks are present")

    # Check for cross-platform support
    cross_platform_tasks = []
    for task in tasks_config['tasks']:
        if any(platform in task for platform in ['windows', 'linux', 'osx']):
            cross_platform_tasks.append(task['label'])

    if cross_platform_tasks:
        print(f"✅ Cross-platform support found in {len(cross_platform_tasks)} tasks")
    else:
        print("⚠️  No cross-platform support detected")

    return True

def test_module_generator():
    """Test that the module generator is working."""
    print("\n🧩 Testing module generator...")

    # Test JavaScript module generator
    result = subprocess.run(
        ['node', 'module-generator.js', 'arbeitsblatt', 'Test Validation'],
        capture_output=True, text=True, cwd='.'
    )

    if result.returncode != 0:
        print(f"❌ Module generator failed: {result.stderr}")
        return False

    print("✅ JavaScript module generator works")

    # Clean up test file
    test_file = "modules/arbeitsblatt-test-validation.tex"
    if os.path.exists(test_file):
        os.remove(test_file)
        print("✅ Test file cleaned up")

    # Test shell script
    if os.path.exists("create-module.sh") and os.access("create-module.sh", os.X_OK):
        print("✅ Interactive shell script is executable")
    else:
        print("⚠️  create-module.sh may not be executable")

    return True

def test_build_system():
    """Test that the CTMM build system is working."""
    print("\n🔨 Testing CTMM build system...")

    result = subprocess.run(['python3', 'ctmm_build.py'], capture_output=True, text=True)

    if "PASS" in result.stdout and result.returncode == 0:
        print("✅ CTMM build system validation passed")
        return True
    else:
        print(f"❌ CTMM build system failed: {result.stderr}")
        return False

def test_documentation():
    """Test that all required documentation exists."""
    print("\n📖 Testing documentation...")

    required_docs = [
        "MODULE-GENERATOR-README.md",
        "BUILD-TASKS-EVALUATION.md",
        "GITHUB-PERMISSIONS.md"
    ]

    all_exist = True
    for doc in required_docs:
        if os.path.exists(doc):
            print(f"✅ {doc} exists")
        else:
            print(f"❌ {doc} missing")
            all_exist = False

    return all_exist

def test_example_modules():
    """Test that example modules from the issue description exist."""
    print("\n📄 Testing example modules...")

    example_modules = [
        "modules/tool-5-4-3-2-1-grounding.tex",
        "modules/notfall-panikattacken.tex",
        "modules/arbeitsblatt-taeglicher-stimmungscheck.tex"
    ]

    all_exist = True
    for module in example_modules:
        if os.path.exists(module):
            print(f"✅ {module} exists")
        else:
            print(f"❌ {module} missing")
            all_exist = False

    return all_exist

def main():
    """Run all tests for Issue #1145 implementation."""
    print("🧪 Testing Issue #1145 Implementation")
    print("=" * 50)

    tests = [
        ("VS Code Tasks", test_vscode_tasks),
        ("Module Generator", test_module_generator),
        ("Build System", test_build_system),
        ("Documentation", test_documentation),
        ("Example Modules", test_example_modules)
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"⚠️  {test_name} test had issues")
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")

    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! Issue #1145 implementation is complete.")
        return 0
    else:
        print("⚠️  Some tests failed. Please review the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
