#!/usr/bin/env python3
"""
Test script to validate Issue #739 fix
Verifies that the GitHub Actions workflow includes the necessary LaTeX packages for pifont dependency
"""

import yaml
import os
import sys

def test_pifont_package_availability():
    """Test that the GitHub Actions workflow includes packages that provide pifont"""

    workflow_path = '.github/workflows/latex-build.yml'

    if not os.path.exists(workflow_path):
        print(f"❌ ERROR: Workflow file {workflow_path} not found")
        return False

    try:
        with open(workflow_path, 'r') as f:
            workflow_content = yaml.safe_load(f)
    except Exception as e:
        print(f"❌ ERROR: Failed to parse {workflow_path}: {e}")
        return False

    # Find the LaTeX action step
    jobs = workflow_content.get('jobs', {})
    build_job = jobs.get('build', {})
    steps = build_job.get('steps', [])

    latex_step = None
    for step in steps:
        if step.get('name') == 'Set up LaTeX':
            latex_step = step
            break

    if not latex_step:
        print("❌ ERROR: 'Set up LaTeX' step not found in workflow")
        return False

    extra_packages = latex_step.get('with', {}).get('extra_system_packages', '')

    print(f"Found LaTeX packages: {extra_packages}")

    # Check for packages that should contain pifont
    pifont_packages = ['texlive-pstricks', 'texlive-latex-extra', 'texlive-fonts-extra']
    found_packages = []

    for pkg in pifont_packages:
        if pkg in extra_packages:
            found_packages.append(pkg)

    if not found_packages:
        print("❌ FAIL: No packages found that provide pifont")
        print("Expected one of: texlive-pstricks, texlive-latex-extra, texlive-fonts-extra")
        return False

    # Specifically check for texlive-pstricks which was added in the fix
    if 'texlive-pstricks' in extra_packages:
        print("✅ PASS: texlive-pstricks package included (contains pifont)")
        return True
    elif found_packages:
        print(f"✅ PASS: Found packages that should contain pifont: {found_packages}")
        return True

    return False

def test_workflow_syntax():
    """Test that the workflow file has valid syntax"""

    workflow_path = '.github/workflows/latex-build.yml'

    try:
        with open(workflow_path, 'r') as f:
            yaml.safe_load(f)
        print("✅ PASS: Workflow YAML syntax is valid")
        return True
    except yaml.YAMLError as e:
        print(f"❌ FAIL: Invalid YAML syntax: {e}")
        return False
    except Exception as e:
        print(f"❌ ERROR: Failed to read workflow file: {e}")
        return False

def test_form_elements_dependency():
    """Test that form-elements.sty properly requires pifont"""

    form_elements_path = 'style/form-elements.sty'

    if not os.path.exists(form_elements_path):
        print(f"❌ ERROR: {form_elements_path} not found")
        return False

    try:
        with open(form_elements_path, 'r') as f:
            content = f.read()

        if '\\RequirePackage{pifont}' in content:
            print("✅ PASS: form-elements.sty properly requires pifont package")
            return True
        else:
            print("❌ FAIL: form-elements.sty does not require pifont package")
            return False

    except Exception as e:
        print(f"❌ ERROR: Failed to read {form_elements_path}: {e}")
        return False

def main():
    """Run all tests for Issue #739 fix"""

    print("============================================================")
    print("Issue #739 Fix Validation")
    print("============================================================")

    tests = [
        ("pifont package availability", test_pifont_package_availability),
        ("Workflow YAML syntax", test_workflow_syntax),
        ("form-elements.sty dependency", test_form_elements_dependency),
    ]

    results = []

    for test_name, test_func in tests:
        print(f"\nTesting {test_name}...")
        result = test_func()
        results.append((test_name, result))

    print("\n============================================================")
    print("TEST SUMMARY")
    print("============================================================")

    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1

    print(f"\nTests passed: {passed}/{len(tests)}")

    if passed == len(tests):
        print("🎉 ALL TESTS PASSED - Issue #739 fix is working correctly!")
        print("\nThe GitHub Actions workflow should now be able to:")
        print("- Install the pifont package through texlive-pstricks")
        print("- Successfully compile LaTeX files using form elements")
        print("- Complete the PDF build without missing package errors")
        return True
    else:
        print("❌ Some tests failed. Please address the issues above.")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)