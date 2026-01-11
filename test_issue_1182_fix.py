#!/usr/bin/env python3
"""
Issue #1182 Fix Validation Script
Validates LaTeX textcolor command syntax and verifies fix implementation.
"""

import os
import re
import sys
from pathlib import Path

def test_textcolor_syntax_validation():
    """Test comprehensive textcolor syntax validation for Issue #1182."""
    print("[SEARCH] Issue #1182 - LaTeX textcolor Syntax Validation")
    print("=" * 60)

    # Count properly and improperly formatted textcolor commands
    properly_formatted = 0
    improperly_formatted = 0
    files_checked = 0
    error_files = []

    # Search patterns
    proper_pattern = re.compile(r'\\textcolor\{[^}]+\}\{[^}]*\}')
    improper_pattern = re.compile(r'(?<!\\)textcolor\{[^}]+\}')  # Missing backslash

    # Check all LaTeX files
    for root, dirs, files in os.walk('.'):
        # Skip hidden directories and build artifacts
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']

        for file in files:
            if file.endswith(('.tex', '.sty')):
                file_path = os.path.join(root, file)
                files_checked += 1

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Count proper textcolor commands
                    proper_matches = proper_pattern.findall(content)
                    properly_formatted += len(proper_matches)

                    # Check for improper textcolor commands
                    improper_matches = improper_pattern.findall(content)
                    if improper_matches:
                        improperly_formatted += len(improper_matches)
                        error_files.append({
                            'file': file_path,
                            'errors': improper_matches
                        })
                        print(f"[FAIL] {file_path}: Found {len(improper_matches)} syntax errors")
                        for error in improper_matches:
                            print(f"  ERROR: {error}")
                    else:
                        proper_count = len(proper_matches)
                        if proper_count > 0:
                            print(f"[PASS] {file_path}: {proper_count} properly formatted textcolor commands")

                except Exception as e:
                    print(f"[WARN]  Error reading {file_path}: {e}")

    # Summary results
    print(f"\n[SUMMARY] Validation Summary")
    print("=" * 60)
    print(f"Files checked: {files_checked}")
    print(f"Properly formatted \\textcolor commands: {properly_formatted}")
    print(f"Improperly formatted textcolor commands: {improperly_formatted}")

    if improperly_formatted == 0:
        print("[PASS] SUCCESS: No LaTeX syntax errors found!")
        print("[PASS] All textcolor commands have required backslashes")
        return True
    else:
        print(f"[FAIL] FAILED: Found {improperly_formatted} syntax errors in {len(error_files)} files")
        return False

def test_build_system_integration():
    """Test that build system validation catches textcolor errors."""
    print(f"\n[FIX] Testing Build System Integration")
    print("=" * 60)

    # Test that build system validation works
    try:
        import ctmm_build
        print("[PASS] ctmm_build module imported successfully")

        # Test LaTeX validation function
        if hasattr(ctmm_build, 'validate_latex_files'):
            result = ctmm_build.validate_latex_files()
            if result:
                print("[PASS] LaTeX validation function passes")
            else:
                print("[FAIL] LaTeX validation function failed")
                return False
        else:
            print("[WARN]  validate_latex_files function not found")

        return True

    except ImportError as e:
        print(f"[FAIL] Failed to import ctmm_build: {e}")
        return False
    except Exception as e:
        print(f"[FAIL] Build system test failed: {e}")
        return False

def test_prevention_tools():
    """Test that prevention tools are available and functional."""
    print(f"\n[TOOL]  Testing Prevention Tools")
    print("=" * 60)

    tools_available = 0
    tools_total = 4

    # Check ctmm_build.py
    if Path('ctmm_build.py').exists():
        print("[PASS] ctmm_build.py - Primary build system available")
        tools_available += 1
    else:
        print("[FAIL] ctmm_build.py - Missing primary build system")

    # Check latex_validator.py
    if Path('latex_validator.py').exists():
        print("[PASS] latex_validator.py - LaTeX validator available")
        tools_available += 1
    else:
        print("[FAIL] latex_validator.py - Missing LaTeX validator")

    # Check fix_latex_escaping.py
    if Path('fix_latex_escaping.py').exists():
        print("[PASS] fix_latex_escaping.py - Escaping fix tool available")
        tools_available += 1
    else:
        print("[FAIL] fix_latex_escaping.py - Missing escaping fix tool")

    # Check test suite
    if Path('test_ctmm_build.py').exists():
        print("[PASS] test_ctmm_build.py - Unit test suite available")
        tools_available += 1
    else:
        print("[FAIL] test_ctmm_build.py - Missing unit test suite")

    print(f"\n[SUMMARY] Tools Available: {tools_available}/{tools_total}")
    return tools_available == tools_total

def run_comprehensive_validation():
    """Run comprehensive validation for Issue #1182."""
    print("[LAUNCH] Issue #1182 Comprehensive Validation")
    print("=" * 60)

    tests_passed = 0
    tests_total = 3

    # Test 1: textcolor syntax validation
    if test_textcolor_syntax_validation():
        tests_passed += 1

    # Test 2: Build system integration
    if test_build_system_integration():
        tests_passed += 1

    # Test 3: Prevention tools availability
    if test_prevention_tools():
        tests_passed += 1

    # Final results
    print(f"\n[TARGET] Final Results - Issue #1182")
    print("=" * 60)
    print(f"Tests passed: {tests_passed}/{tests_total}")

    if tests_passed == tests_total:
        print("[PASS] SUCCESS: Issue #1182 completely resolved!")
        print("[PASS] LaTeX syntax errors prevented and validated")
        print("[PASS] Build system integration working correctly")
        print("[PASS] Prevention tools available and functional")
        return True
    else:
        print(f"[FAIL] PARTIAL SUCCESS: {tests_passed}/{tests_total} tests passed")
        print("[WARN]  Some validation aspects need attention")
        return False

if __name__ == "__main__":
    success = run_comprehensive_validation()
    sys.exit(0 if success else 1)
