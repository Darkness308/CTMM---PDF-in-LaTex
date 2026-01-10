#!/usr/bin/env python3
"""
Test for Issue #1153 Fix: CI Failure due to Missing Label References

This test validates that all \ctmmRef{} references have corresponding \label{} definitions,
which was the root cause of the CI failures in both "Build LaTeX PDF" and "LaTeX Validation" workflows.

Usage:
    python3 test_issue_1153_fix.py

Expected: All tests pass, confirming that the validation logic used in CI will work correctly.
"""

import subprocess
import os
import sys
import re

def test_ctmm_ref_label_consistency():
    """Test that all \ctmmRef references have corresponding labels."""
    print("\n🔍 Testing ctmmRef and label consistency (Issue #1153 Fix)")
    print("=" * 70)

    # Find all \ctmmRef references
    try:
        result = subprocess.run([
            'grep', '-o', r'\\ctmmRef{[^}]*}', *[f'modules/{f}' for f in os.listdir('modules') if f.endswith('.tex')]
        ], capture_output=True, text=True)

        if result.returncode != 0:
            print("✅ No ctmmRef references found (which is also valid)")
            return True

        refs_raw = result.stdout.strip().split('\n') if result.stdout.strip() else []

        # Extract just the reference names
        refs = []
        for ref_line in refs_raw:
            if ref_line:
                match = re.search(r'\\ctmmRef\{([^}]*)\}', ref_line)
                if match:
                    refs.append(match.group(1))

        refs = list(set(refs))  # Remove duplicates
        refs.sort()

        print(f"📋 Found {len(refs)} unique ctmmRef references:")
        for ref in refs:
            print(f"   • {ref}")

        # Check that each reference has a corresponding label
        missing_labels = []
        for ref in refs:
            # Check in all module files and main.tex
            files_to_check = [f'modules/{f}' for f in os.listdir('modules') if f.endswith('.tex')] + ['main.tex']
            label_found = False

            for file_path in files_to_check:
                if os.path.exists(file_path):
                    check_result = subprocess.run([
                        'grep', '-q', f'\\label{{{ref}}}', file_path
                    ])
                    if check_result.returncode == 0:
                        label_found = True
                        break

            if not label_found:
                missing_labels.append(ref)

        if missing_labels:
            print(f"\n❌ MISSING LABELS ({len(missing_labels)}):")
            for label in missing_labels:
                print(f"   • {label}")
            return False
        else:
            print(f"\n✅ ALL LABELS FOUND: All {len(refs)} ctmmRef references have corresponding labels")
            return True

    except Exception as e:
        print(f"❌ Error during test: {e}")
        return False

def test_ci_validation_logic():
    """Test the exact validation logic used in the CI workflow."""
    print("\n🔧 Testing CI workflow validation logic")
    print("=" * 70)

    try:
        # This is the exact command used in .github/workflows/latex-validation.yml
        validation_script = '''
        refs=$(grep -o '\\ctmmRef{[^}]*}' modules/*.tex | sed 's/.*{//;s/}//')
        for ref in $refs; do
            grep -q "\\label{$ref}" modules/*.tex main.tex || (echo "::error ::Label {$ref} fehlt!" && exit 1)
        done
        '''

        result = subprocess.run(['/bin/bash', '-c', validation_script],
                              capture_output=True, text=True, cwd='.')

        if result.returncode == 0:
            print("✅ CI validation logic passes - no missing labels")
            if result.stdout.strip():
                print(f"Output: {result.stdout.strip()}")
            return True
        else:
            print("❌ CI validation logic fails:")
            print(f"Exit code: {result.returncode}")
            if result.stdout:
                print(f"Stdout: {result.stdout}")
            if result.stderr:
                print(f"Stderr: {result.stderr}")
            return False

    except Exception as e:
        print(f"❌ Error during CI validation test: {e}")
        return False

def test_specific_fixed_labels():
    """Test the specific labels that were fixed in this issue."""
    print("\n🎯 Testing specific labels fixed in Issue #1153")
    print("=" * 70)

    labels_to_check = [
        ('sec:selbstreflexion', 'modules/selbstreflexion.tex'),
        ('sec:feedback', 'modules/selbstreflexion.tex'),
    ]

    all_passed = True

    for label, expected_file in labels_to_check:
        result = subprocess.run([
            'grep', '-q', f'\\label{{{label}}}', expected_file
        ])

        if result.returncode == 0:
            print(f"✅ Found label {label} in {expected_file}")
        else:
            print(f"❌ Missing label {label} in {expected_file}")
            all_passed = False

    return all_passed

def main():
    """Run all tests for Issue #1153 fix."""
    print("🧪 Issue #1153 Fix Validation Tests")
    print("=" * 70)
    print("Testing CI failure fix for missing label references")

    tests = [
        ("ctmmRef and label consistency", test_ctmm_ref_label_consistency),
        ("CI workflow validation logic", test_ci_validation_logic),
        ("Specific fixed labels", test_specific_fixed_labels),
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test '{test_name}' failed with exception: {e}")
            results.append((test_name, False))

    # Summary
    print(f"\n{'='*70}")
    print("TEST RESULTS SUMMARY")
    print(f"{'='*70}")

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")

    if passed == total:
        print(f"\n🎉 ALL TESTS PASSED! ({passed}/{total})")
        print("✅ Issue #1153 fix validated successfully")
        print("\nKey improvements confirmed:")
        print("• All ctmmRef references have corresponding labels ✅")
        print("• CI validation logic passes without errors ✅")
        print("• Specific missing labels (sec:selbstreflexion) are now present ✅")
        return 0
    else:
        print(f"\n❌ SOME TESTS FAILED ({passed}/{total} passed)")
        return 1

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    sys.exit(main())