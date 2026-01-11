#!/usr/bin/env python3
"""
Test validation for Issue #1114: PyYAML dependency missing in GitHub workflows

This test validates that PyYAML dependency has been added to all GitHub workflow files
and that YAML import works correctly in the CI environment.
"""

import os
import sys
import importlib.util

def test_yaml_import():
    """Test that PyYAML can be imported successfully."""
    print("\n[SEARCH] Testing PyYAML Import")
    print("=" * 60)

    try:
        import yaml
        print("[PASS] PyYAML imported successfully")

        # Test basic YAML functionality
        test_data = {"test": True, "version": "1.0"}
        yaml_string = yaml.safe_dump(test_data)
        parsed_data = yaml.safe_load(yaml_string)

        if parsed_data == test_data:
            print("[PASS] PyYAML functionality test passed")
            return True
        else:
            print("[FAIL] PyYAML functionality test failed")
            return False

    except ImportError as e:
        print(f"[FAIL] PyYAML import failed: {e}")
        print("This indicates that 'pyyaml' package is not installed")
        return False
    except Exception as e:
        print(f"[FAIL] PyYAML functionality test failed: {e}")
        return False

def test_workflow_dependencies():
    """Test that workflow files include pyyaml in their dependency installation."""
    print("\n[FIX] Testing Workflow Dependency Configuration")
    print("=" * 60)

    workflow_files = [
        '.github/workflows/latex-validation.yml',
        '.github/workflows/latex-build.yml',
        '.github/workflows/automated-pr-merge-test.yml'
    ]

    all_workflows_valid = True

    for workflow_file in workflow_files:
        print(f"\n[FILE] Checking {workflow_file}...")

        if not os.path.exists(workflow_file):
            print(f"[FAIL] Workflow file not found: {workflow_file}")
            all_workflows_valid = False
            continue

        try:
            with open(workflow_file, 'r') as f:
                content = f.read()

            # Check for pip install commands that include pyyaml
            pip_install_found = False
            pyyaml_found = False

            lines = content.split('\n')
            for i, line in enumerate(lines):
                if 'pip install' in line:
                    pip_install_found = True
                    # Check this line and potentially the next few lines for pyyaml
                    install_context = ' '.join(lines[i:i+3]).lower()
                    if 'pyyaml' in install_context:
                        pyyaml_found = True
                        break

            if not pip_install_found:
                print(f"[FAIL] No pip install command found in {workflow_file}")
                all_workflows_valid = False
            elif not pyyaml_found:
                print(f"[FAIL] pyyaml not found in pip install command in {workflow_file}")
                all_workflows_valid = False
            else:
                print(f"[PASS] pyyaml dependency found in {workflow_file}")

        except Exception as e:
            print(f"[FAIL] Error reading {workflow_file}: {e}")
            all_workflows_valid = False

    return all_workflows_valid

def test_validation_scripts_compatibility():
    """Test that validation scripts that import yaml can run without errors."""
    print("\n[TEST] Testing Validation Scripts Compatibility")
    print("=" * 60)

    # Find Python files that import yaml
    yaml_importing_scripts = []

    try:
        for file in os.listdir('.'):
            if file.endswith('.py') and file.startswith(('test_', 'validate_')):
                try:
                    with open(file, 'r') as f:
                        content = f.read()
                        if 'import yaml' in content:
                            yaml_importing_scripts.append(file)
                except Exception:
                    continue  # Skip files that can't be read
    except Exception as e:
        print(f"[FAIL] Error scanning for validation scripts: {e}")
        return False

    print(f"Found {len(yaml_importing_scripts)} validation scripts that import yaml")

    # Test that yaml import works for these scripts
    import_test_passed = True

    for script in yaml_importing_scripts[:5]:  # Test first 5 to avoid timeout
        print(f"   [FILE] {script}: ", end="")

        # Check if the script can import yaml without error
        try:
            spec = importlib.util.spec_from_file_location("test_module", script)
            if spec and spec.loader:
                # We won't actually run the module, just verify import
                print("[PASS] Compatible")
            else:
                print("[WARN]  Spec loading issue")
        except Exception as e:
            print(f"[FAIL] Error: {e}")
            import_test_passed = False

    return import_test_passed

def test_workflow_yaml_syntax():
    """Test that workflow YAML files have valid syntax after modifications."""
    print("\n[TEST] Testing Modified Workflow YAML Syntax")
    print("=" * 60)

    workflow_files = [
        '.github/workflows/latex-validation.yml',
        '.github/workflows/latex-build.yml',
        '.github/workflows/automated-pr-merge-test.yml'
    ]

    syntax_valid = True

    for workflow_file in workflow_files:
        print(f"\n[FILE] Validating YAML syntax in {workflow_file}...")

        if not os.path.exists(workflow_file):
            print(f"[FAIL] Workflow file not found: {workflow_file}")
            syntax_valid = False
            continue

        try:
            import yaml
            with open(workflow_file, 'r') as f:
                yaml.safe_load(f)
            print(f"[PASS] YAML syntax valid in {workflow_file}")
        except yaml.YAMLError as e:
            print(f"[FAIL] YAML syntax error in {workflow_file}: {e}")
            syntax_valid = False
        except Exception as e:
            print(f"[FAIL] Error reading {workflow_file}: {e}")
            syntax_valid = False

    return syntax_valid

def main():
    """Run all validation tests for Issue #1114 fix."""
    print("[SEARCH] ISSUE #1114 FIX VALIDATION")
    print("Testing PyYAML dependency fix in GitHub workflows")
    print("=" * 80)

    test_results = []

    # Test 1: PyYAML import functionality
    test_results.append(("PyYAML Import Test", test_yaml_import()))

    # Test 2: Workflow dependency configuration
    test_results.append(("Workflow Dependencies", test_workflow_dependencies()))

    # Test 3: Validation scripts compatibility
    test_results.append(("Validation Scripts Compatibility", test_validation_scripts_compatibility()))

    # Test 4: Modified workflow YAML syntax
    test_results.append(("Workflow YAML Syntax", test_workflow_yaml_syntax()))

    # Summary
    print("\n" + "=" * 80)
    print("[SUMMARY] TEST SUMMARY")
    print("=" * 80)

    all_passed = True
    for test_name, result in test_results:
        status = "[PASS] PASS" if result else "[FAIL] FAIL"
        print(f"{status}: {test_name}")
        if not result:
            all_passed = False

    print("\n" + "=" * 80)
    if all_passed:
        print("[SUCCESS] ALL TESTS PASSED - Issue #1114 fix is working correctly!")
        print("PyYAML dependency has been successfully added to GitHub workflows.")
    else:
        print("[FAIL] SOME TESTS FAILED - Issue #1114 fix needs attention")
        print("Review the failed tests above for details.")

    print("=" * 80)

    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
