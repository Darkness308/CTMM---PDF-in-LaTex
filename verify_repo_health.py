#!/usr/bin/env python3
"""
Repository Health Check for CTMM Project

This script verifies that the repository is in a good state for code reviews
and automated analysis tools like GitHub Copilot.

Usage:
    python3 verify_repo_health.py
"""

import os
import sys
from pathlib import Path
import subprocess
import yaml


def check_yaml_files():
    """Check all YAML files for syntax validity."""
    print("🔍 Checking YAML files...")
    yaml_files = list(Path('.').rglob('*.yml')) + list(Path('.').rglob('*.yaml'))
    
    for yaml_file in yaml_files:
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                yaml.safe_load(f)
            print(f"  ✓ {yaml_file}")
        except yaml.YAMLError as e:
            print(f"  ✗ {yaml_file}: {e}")
            return False
        except Exception as e:
            print(f"  ⚠ {yaml_file}: {e}")
    
    return True


def check_python_files():
    """Check Python files for syntax validity."""
    print("\n🐍 Checking Python files...")
    python_files = list(Path('.').rglob('*.py'))
    
    for py_file in python_files:
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                compile(f.read(), py_file, 'exec')
            print(f"  ✓ {py_file}")
        except SyntaxError as e:
            print(f"  ✗ {py_file}: Syntax error - {e}")
            return False
        except Exception as e:
            print(f"  ⚠ {py_file}: {e}")
    
    return True


def check_file_names():
    """Check for problematic file names that might confuse automated tools."""
    print("\n📁 Checking file names...")
    problematic_patterns = ['#', '..']
    tracked_files = subprocess.run(['git', 'ls-files'], capture_output=True, text=True).stdout.strip().split('\n')
    
    # Focus on code and configuration files, skip binary/source materials
    code_extensions = {'.py', '.tex', '.sty', '.yml', '.yaml', '.md', '.txt', '.json'}
    
    issues = []
    for file_path in tracked_files:
        if not file_path:  # Skip empty lines
            continue
        
        # Skip therapie-material directory (source documents) and binary files
        if file_path.startswith('therapie-material/') or Path(file_path).suffix not in code_extensions:
            continue
        
        file_name = Path(file_path).name
        for pattern in problematic_patterns:
            if pattern in file_name:
                issues.append(f"  ⚠ {file_path}: Contains '{pattern}'")
        
        # Check for files starting with problematic characters
        if file_name.startswith(('#', '.')) and not file_name.startswith(('.git', '.vscode', '.dev')):
            issues.append(f"  ⚠ {file_path}: Starts with problematic character")
    
    if issues:
        print("Found potential file name issues in code files:")
        for issue in issues:
            print(issue)
        return False
    else:
        print("  ✓ All code file names look good")
        return True


def check_empty_files():
    """Check for empty files that might cause issues."""
    print("\n📄 Checking for empty files...")
    tracked_files = subprocess.run(['git', 'ls-files'], capture_output=True, text=True).stdout.strip().split('\n')
    
    empty_files = []
    for file_path in tracked_files:
        if not file_path:  # Skip empty lines
            continue
        
        try:
            if Path(file_path).stat().st_size == 0:
                empty_files.append(file_path)
        except FileNotFoundError:
            pass
    
    if empty_files:
        print("Found empty files:")
        for empty_file in empty_files:
            print(f"  ⚠ {empty_file}")
        return False
    else:
        print("  ✓ No empty files found")
        return True


def main():
    """Run all health checks."""
    print("🔍 CTMM Repository Health Check")
    print("=" * 40)
    
    checks = [
        ("YAML syntax", check_yaml_files),
        ("Python syntax", check_python_files), 
        ("File names", check_file_names),
        ("Empty files", check_empty_files),
    ]
    
    results = []
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"\n❌ Error in {check_name}: {e}")
            results.append((check_name, False))
    
    print("\n" + "=" * 40)
    print("📊 SUMMARY")
    print("=" * 40)
    
    all_passed = True
    for check_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{check_name}: {status}")
        if not passed:
            all_passed = False
    
    if all_passed:
        print("\n🎉 Repository is ready for code reviews!")
        return 0
    else:
        print("\n⚠ Some issues found. Consider fixing them to improve reviewability.")
        return 1


if __name__ == "__main__":
    sys.exit(main())