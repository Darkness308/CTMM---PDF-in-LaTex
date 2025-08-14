#!/usr/bin/env python3
"""
Validation script for GitHub Copilot file review fix - Issue #538

This script validates that all problematic files that could interfere with
GitHub Copilot's ability to review pull request files have been resolved.

The issues identified and fixed:
1. Removed `modules/Untitled-1` - file without proper extension
2. Renamed `modules/# Code Citations.md` to remove special character
3. Renamed files with spaces in converted/ directory to use underscores
"""

import os
import sys
import subprocess
from pathlib import Path


def validate_no_problematic_filenames():
    """Validate that no files have problematic names that could confuse GitHub systems."""
    
    print("=" * 80)
    print("GITHUB COPILOT FIX VALIDATION - ISSUE #538")
    print("=" * 80)
    print("Validating that all problematic filenames have been resolved.\n")
    
    # Get all tracked files
    result = subprocess.run(['git', 'ls-files'], capture_output=True, text=True)
    if result.returncode != 0:
        print("❌ Error: Could not get git tracked files")
        return False
    
    tracked_files = result.stdout.strip().split('\n')
    print(f"📁 Total tracked files: {len(tracked_files)}\n")
    
    # Check for various problematic patterns
    issues = []
    
    # 1. Files without extensions (excluding known good files)
    known_good_no_ext = {'LICENSE', 'Makefile', '.gitignore'}
    
    for file_path in tracked_files:
        filename = os.path.basename(file_path)
        
        # Check for files without extensions
        if '.' not in filename and filename not in known_good_no_ext:
            issues.append(f"File without extension: {file_path}")
        
        # Check for special characters at start
        if filename.startswith('#') or filename.startswith('@') or filename.startswith('$'):
            issues.append(f"File starts with special character: {file_path}")
        
        # Check for spaces in filenames
        if ' ' in filename:
            issues.append(f"File contains spaces: {file_path}")
        
        # Check for other problematic characters
        problematic_chars = ['|', '<', '>', ':', '"', '?', '*']
        for char in problematic_chars:
            if char in filename:
                issues.append(f"File contains problematic character '{char}': {file_path}")
    
    # Report results
    print("🔍 PROBLEMATIC FILENAME CHECK")
    print("-" * 50)
    
    if issues:
        print("❌ Found problematic filenames:")
        for issue in issues:
            print(f"   {issue}")
        return False
    else:
        print("✅ No problematic filenames found")
    
    return True


def validate_no_binary_files():
    """Validate that no binary files are tracked in git."""
    
    print("\n🔍 BINARY FILE CHECK")
    print("-" * 50)
    
    # Get all tracked files and check their types
    result = subprocess.run(['git', 'ls-files'], capture_output=True, text=True)
    if result.returncode != 0:
        print("❌ Error: Could not get git tracked files")
        return False
    
    tracked_files = result.stdout.strip().split('\n')
    binary_files = []
    
    for file_path in tracked_files:
        if os.path.exists(file_path):
            # Use file command to check if it's binary
            file_result = subprocess.run(['file', file_path], capture_output=True, text=True)
            if file_result.returncode == 0:
                file_output = file_result.stdout.lower()
                # Only consider it binary if:
                # 1. It's explicitly marked as binary data, OR
                # 2. It's a known binary file type, AND
                # 3. It's NOT identified as text
                if 'text' not in file_output:
                    if ('binary' in file_output or 
                        any(binary_type in file_output for binary_type in 
                            ['pdf', 'image', 'audio', 'video', 'archive', 'zip', 'executable', 'data'])):
                        binary_files.append(file_path)
    
    if binary_files:
        print("❌ Found binary files:")
        for binary_file in binary_files:
            print(f"   {binary_file}")
        return False
    else:
        print("✅ No binary files found in git tracking")
    
    return True


def validate_file_extensions():
    """Validate that all files have appropriate extensions for their content."""
    
    print("\n🔍 FILE EXTENSION CHECK")
    print("-" * 50)
    
    result = subprocess.run(['git', 'ls-files'], capture_output=True, text=True)
    if result.returncode != 0:
        print("❌ Error: Could not get git tracked files")
        return False
    
    tracked_files = result.stdout.strip().split('\n')
    
    # Count file types
    extensions = {}
    for file_path in tracked_files:
        if '.' in os.path.basename(file_path):
            ext = file_path.split('.')[-1].lower()
            extensions[ext] = extensions.get(ext, 0) + 1
        else:
            # Special files without extensions
            filename = os.path.basename(file_path)
            extensions[f"no-ext ({filename})"] = extensions.get(f"no-ext ({filename})", 0) + 1
    
    print("📊 File type distribution:")
    for ext, count in sorted(extensions.items(), key=lambda x: x[1], reverse=True):
        print(f"   .{ext}: {count} files")
    
    # Check for appropriate file types
    expected_types = {'tex', 'py', 'md', 'yml', 'yaml', 'json', 'sty', 'gitignore'}
    unexpected_types = set(ext.split(' ')[0] for ext in extensions.keys()) - expected_types - {'no-ext'}
    
    if unexpected_types:
        print(f"\n⚠️  Unexpected file types: {unexpected_types}")
        print("   (This may be normal depending on project needs)")
    else:
        print("\n✅ All file types are appropriate for a LaTeX project")
    
    return True


def validate_build_system():
    """Validate that the build system still works after changes."""
    
    print("\n🔍 BUILD SYSTEM CHECK")
    print("-" * 50)
    
    # Run the CTMM build system
    result = subprocess.run(['python3', 'ctmm_build.py'], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Build system runs successfully")
        # Check for specific success indicators
        if "Basic build: ✓ PASS" in result.stdout and "Full build: ✓ PASS" in result.stdout:
            print("✅ Both basic and full builds pass")
            return True
        else:
            print("⚠️  Build system ran but some tests may have failed")
            print("Build output:", result.stdout[-500:])  # Last 500 chars
            return False
    else:
        print("❌ Build system failed")
        print("Error output:", result.stderr)
        return False


def main():
    """Run all validation checks."""
    
    # Ensure we're in the repository root
    if not Path('.git').exists():
        print("Error: This script must be run from the repository root directory")
        print("Expected to find .git directory")
        sys.exit(1)
    
    print("🚀 Starting GitHub Copilot fix validation...\n")
    
    # Run all checks
    checks = [
        ("Problematic Filenames", validate_no_problematic_filenames),
        ("Binary Files", validate_no_binary_files),
        ("File Extensions", validate_file_extensions),
        ("Build System", validate_build_system),
    ]
    
    results = []
    for check_name, check_func in checks:
        try:
            success = check_func()
            results.append((check_name, success))
        except Exception as e:
            print(f"❌ Error in {check_name} check: {e}")
            results.append((check_name, False))
    
    # Summary
    print("\n" + "=" * 80)
    print("VALIDATION SUMMARY")
    print("=" * 80)
    
    all_passed = True
    for check_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {check_name}")
        if not success:
            all_passed = False
    
    if all_passed:
        print("\n🎉 ALL CHECKS PASSED")
        print("GitHub Copilot should now be able to review files in pull requests!")
        print("\nThe following issues have been resolved:")
        print("• Removed file without extension (modules/Untitled-1)")
        print("• Fixed filename with special character (# Code Citations.md)")
        print("• Renamed files with spaces to use underscores")
        print("• Verified no binary files are tracked")
        print("• Confirmed build system still works")
    else:
        print("\n⚠️  SOME CHECKS FAILED")
        print("Additional fixes may be needed for GitHub Copilot to work properly.")
    
    print("\n📋 STATUS: ISSUE #538", "RESOLVED" if all_passed else "NEEDS ATTENTION")
    print("=" * 80)
    
    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)