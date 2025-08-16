#!/usr/bin/env python3
"""
PR Validation Script for CTMM Repository

This script helps validate that pull requests contain meaningful changes
that Copilot can review. It checks for common issues that prevent effective
code review.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def run_command(cmd, capture_output=True):
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=capture_output, text=True)
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return False, "", str(e)

def check_git_status():
    """Check if there are uncommitted changes."""
    success, stdout, stderr = run_command("git status --porcelain")
    if not success:
        print(f"❌ Error checking git status: {stderr}")
        return False
    
    if stdout.strip():
        print("⚠️  Uncommitted changes detected:")
        print(stdout)
        print("Consider committing these changes before creating a PR.")
        return False
    
    print("✅ No uncommitted changes")
    return True

def check_file_changes(base_branch="main"):
    """Check for file changes compared to base branch."""
    # First try to find a suitable base branch
    success, stdout, stderr = run_command("git branch -r")
    available_branches = stdout.split('\n') if success else []
    
    # Try different base branch options
    base_options = [f"origin/{base_branch}", base_branch, "origin/main", "main"]
    actual_base = None
    
    for base_option in base_options:
        if any(base_option in branch for branch in available_branches) or base_option == base_branch:
            success, _, _ = run_command(f"git rev-parse {base_option}")
            if success:
                actual_base = base_option
    # Batch git rev-parse for all base_options at once
    valid_bases = []
    # Only check base_options that are present in available_branches or match base_branch
    filtered_options = [opt for opt in base_options if any(opt in branch for branch in available_branches) or opt == base_branch]
    if filtered_options:
        # Run git rev-parse for all filtered options at once
        cmd = "git rev-parse " + " ".join(filtered_options)
        success, stdout, stderr = run_command(cmd)
        if success and stdout.strip():
            # git rev-parse outputs each hash on a new line, in the same order as the arguments
            hashes = stdout.split('\n')
            for h, base_opt in zip(hashes, filtered_options):
                if h.strip() and not h.startswith("fatal:"):
                    actual_base = base_opt
                    break
    
    if not actual_base:
        # If no base branch found, compare with HEAD~1 or show staged changes
        success, stdout, stderr = run_command("git diff --cached --name-only")
        if success and stdout.strip():
            print("📄 Checking staged changes...")
            actual_base = "--cached"
        else:
            success, stdout, stderr = run_command("git diff --name-only HEAD~1..HEAD")
            if success:
                actual_base = "HEAD~1"
            else:
                print("⚠️  Cannot determine base for comparison, checking working directory changes...")
                success, stdout, stderr = run_command("git diff --name-only")
                actual_base = ""
    
    # Get file changes
    if actual_base == "--cached":
        success, stdout, stderr = run_command("git diff --cached --name-only")
    elif actual_base == "":
        success, stdout, stderr = run_command("git diff --name-only")
    else:
        success, stdout, stderr = run_command(f"git diff --name-only {actual_base}..HEAD")
    
    if not success:
        print(f"❌ Error checking file changes: {stderr}")
        return False, 0, 0, 0
    
    changed_files = len(stdout.split('\n')) if stdout.strip() else 0
    
    # Get line statistics
    if actual_base == "--cached":
        success, stdout, stderr = run_command("git diff --cached --numstat")
    elif actual_base == "":
        success, stdout, stderr = run_command("git diff --numstat")
    else:
        success, stdout, stderr = run_command(f"git diff --numstat {actual_base}..HEAD")
    
    added_lines = 0
    deleted_lines = 0
    
    if success and stdout.strip():
        for line in stdout.split('\n'):
            if line.strip():
                parts = line.split('\t')
                if len(parts) >= 2:
                    try:
                        added_lines += int(parts[0]) if parts[0] != '-' else 0
                        deleted_lines += int(parts[1]) if parts[1] != '-' else 0
                    except ValueError:
                        continue
    
    return True, changed_files, added_lines, deleted_lines

def check_ctmm_build():
    """Run the CTMM build system to validate the project."""
    print("\n🔧 Running CTMM build system...")
    success, stdout, stderr = run_command("python3 ctmm_build.py")
    
    if not success:
        print(f"❌ CTMM build failed")
        if stderr:
            print(f"Error details: {stderr}")
        return False
    
    # Check the output for success indicators
    if stdout and ("PASS" in stdout or "✓" in stdout):
        print("✅ CTMM build system passed")
        return True
    else:
        print("⚠️  CTMM build completed but status unclear")
        return True  # Don't fail if we can't parse the output clearly

def validate_latex_files():
    """Check for common LaTeX issues in changed files."""
    success, stdout, stderr = run_command("git diff --name-only HEAD~1..HEAD")
    if not success:
        return True  # Skip if we can't get changed files
    
    latex_files = [f for f in stdout.split('\n') if f.endswith('.tex')]
    
    if not latex_files:
        return True
    
    print(f"\n📄 Checking {len(latex_files)} LaTeX file(s)...")
    
    issues_found = False
    for file_path in latex_files:
        if not os.path.exists(file_path):
            continue
            
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check for common LaTeX issues
        if '\\usepackage{' in content and 'modules/' in file_path:
            print(f"⚠️  {file_path}: Contains \\usepackage - should be in main.tex preamble")
            issues_found = True
            
        if '\\Box' in content or '\\blacksquare' in content:
            print(f"⚠️  {file_path}: Uses \\Box or \\blacksquare - use \\checkbox/\\checkedbox macros")
            issues_found = True
    
    if not issues_found:
        print("✅ No LaTeX issues detected")
    
    return not issues_found

def main():
    parser = argparse.ArgumentParser(description='Validate PR content for CTMM repository')
    parser.add_argument('--base-branch', default='main', help='Base branch to compare against')
    parser.add_argument('--skip-build', action='store_true', help='Skip CTMM build check')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    print("🔍 CTMM PR Validation")
    print("=" * 50)
    
    # Check if we're in a git repository
    if not os.path.exists('.git'):
        print("❌ Not in a git repository")
        sys.exit(1)
    
    all_checks_passed = True
    
    # Check git status
    if not check_git_status():
        all_checks_passed = False
    
    # Check for file changes
    success, changed_files, added_lines, deleted_lines = check_file_changes(args.base_branch)
    if not success:
        all_checks_passed = False
    else:
        print(f"\n📊 Changes compared to {args.base_branch}:")
        print(f"  - Files changed: {changed_files}")
        print(f"  - Lines added: {added_lines}")
        print(f"  - Lines deleted: {deleted_lines}")
        
        if changed_files == 0:
            print("❌ No file changes detected - Copilot cannot review empty PRs")
            print("   💡 To fix: Add meaningful changes to files (documentation, code, etc.)")
            print("   📚 See existing ISSUE_*_RESOLUTION.md files for examples")
            all_checks_passed = False
        elif added_lines == 0 and deleted_lines == 0:
            print("❌ No content changes detected - PR appears to be empty")
            print("   💡 To fix: Ensure your changes add or modify actual content")
            print("   ⚠️  Whitespace-only changes won't enable Copilot review")
            all_checks_passed = False
        else:
            print("✅ Meaningful changes detected - Copilot should be able to review")
    
    # Validate LaTeX files
    if not validate_latex_files():
        all_checks_passed = False
    
    # Run CTMM build system
    if not args.skip_build:
        if not check_ctmm_build():
            all_checks_passed = False
    
    print("\n" + "=" * 50)
    if all_checks_passed:
        print("🎉 All validation checks passed!")
        print("This PR should be reviewable by Copilot.")
        sys.exit(0)
    else:
        print("❌ Some validation checks failed")
        print("Please address the issues above before creating/updating the PR.")
        print()
        print("🔗 Helpful Resources:")
        print("   📖 Repository: See existing ISSUE_*_RESOLUTION.md for examples")
        print("   🛠️  Build system: Run 'python3 ctmm_build.py' to check LaTeX")
        print("   📝 Validation: Run 'python3 validate_pr.py --verbose' for details")
        sys.exit(1)

if __name__ == "__main__":
    main()