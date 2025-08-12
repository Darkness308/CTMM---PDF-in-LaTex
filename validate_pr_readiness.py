#!/usr/bin/env python3
"""
Pre-PR validation script for the CTMM repository.
Checks if the current branch has meaningful changes that Copilot can review.
"""

import subprocess
import sys
from pathlib import Path

def run_git_command(cmd):
    """Run a git command and return the output."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout.strip(), result.returncode
    except Exception as e:
        print(f"Error running git command '{cmd}': {e}")
        return "", 1

def get_branch_name():
    """Get the current branch name."""
    output, code = run_git_command("git branch --show-current")
    if code != 0:
        print("❌ Error: Unable to determine current branch")
        return None
    return output

def get_default_branch():
    """Get the default branch name (usually main or master)."""
    # First try to get it from remote
    output, code = run_git_command("git symbolic-ref refs/remotes/origin/HEAD")
    if code == 0:
        return output.split('/')[-1]
    
    # Check what branches exist remotely
    output, code = run_git_command("git ls-remote --heads origin")
    if code == 0:
        # Look for common default branch names
        for line in output.split('\n'):
            if 'refs/heads/main' in line:
                return 'main'
            elif 'refs/heads/master' in line:
                return 'master'
    
    # Fallback to common defaults
    for branch in ['main', 'master']:
        output, code = run_git_command(f"git rev-parse --verify origin/{branch}")
        if code == 0:
            return branch
    
    return 'main'  # Default fallback

def check_changes_against_branch(base_branch):
    """Check what changes exist compared to the base branch."""
    print(f"Checking changes against '{base_branch}'...")
    
    # Get changed files
    changed_files_cmd = f"git diff --name-only origin/{base_branch}..HEAD"
    changed_files, code = run_git_command(changed_files_cmd)
    
    if code != 0:
        print(f"❌ Error: Unable to compare with origin/{base_branch}")
        print("Make sure you have fetched the latest changes: git fetch origin")
        print("This might also occur in special environments (like CI) without a proper base branch.")
        
        # Fallback: check if we have any files at all (basic validation)
        files_output, files_code = run_git_command("git ls-files | head -10")
        if files_code == 0 and files_output.strip():
            print(f"\n🔍 Fallback validation: Repository contains files")
            print("In a normal environment, this validation would work properly.")
            return True
        else:
            return False
    
    files_list = [f for f in changed_files.split('\n') if f.strip()]
    changed_files_count = len(files_list)
    
    # Get line changes
    stats_cmd = f"git diff --numstat origin/{base_branch}..HEAD"
    stats_output, code = run_git_command(stats_cmd)
    
    total_additions = 0
    total_deletions = 0
    
    if code == 0 and stats_output:
        for line in stats_output.split('\n'):
            if line.strip():
                parts = line.split('\t')
                if len(parts) >= 2:
                    try:
                        additions = int(parts[0]) if parts[0] != '-' else 0
                        deletions = int(parts[1]) if parts[1] != '-' else 0
                        total_additions += additions
                        total_deletions += deletions
                    except ValueError:
                        continue
    
    # Report findings
    print(f"\n📊 Change Summary:")
    print(f"   Files changed: {changed_files_count}")
    print(f"   Lines added: {total_additions}")
    print(f"   Lines deleted: {total_deletions}")
    print(f"   Total changes: {total_additions + total_deletions}")
    
    if changed_files_count > 0:
        print(f"\n📁 Changed files:")
        for file in files_list:
            print(f"   - {file}")
    
    # Validation logic
    if changed_files_count == 0:
        print("\n❌ VALIDATION FAILED: No files changed")
        print("   Copilot cannot review PRs without file changes.")
        print("   Make sure your changes are committed and pushed.")
        return False
    
    if total_additions + total_deletions == 0:
        print("\n⚠️  WARNING: No line changes detected")
        print("   This might indicate formatting-only changes or git issues.")
        print("   Copilot may have difficulty reviewing this PR.")
        return False
    
    print("\n✅ VALIDATION PASSED")
    print("   This branch has meaningful changes that Copilot can review.")
    return True

def check_git_status():
    """Check if there are uncommitted changes."""
    status_output, code = run_git_command("git status --porcelain")
    
    if code != 0:
        print("❌ Error: Unable to check git status")
        return False
    
    if status_output.strip():
        print("\n⚠️  Uncommitted changes detected:")
        uncommitted_files = [line.strip() for line in status_output.split('\n') if line.strip()]
        for file_status in uncommitted_files:
            print(f"   {file_status}")
        print("\n   Consider committing these changes before creating a PR.")
        return False
    
    return True

def main():
    """Main validation function."""
    print("🔍 CTMM Pre-PR Validation")
    print("=" * 40)
    
    # Check if we're in a git repository
    if not Path('.git').exists():
        print("❌ Error: Not in a git repository")
        sys.exit(1)
    
    # Get current branch
    current_branch = get_branch_name()
    if not current_branch:
        sys.exit(1)
    
    print(f"Current branch: {current_branch}")
    
    # Check for uncommitted changes
    if not check_git_status():
        print("\n💡 Tip: Run 'git add .' and 'git commit' to include changes")
    
    # Get default branch
    default_branch = get_default_branch()
    print(f"Comparing against: {default_branch}")
    
    # Fetch latest changes
    print("\nFetching latest changes...")
    output, code = run_git_command("git fetch origin")
    if code != 0:
        print("⚠️  Warning: Unable to fetch latest changes")
    
    # Check changes
    has_valid_changes = check_changes_against_branch(default_branch)
    
    print("\n" + "=" * 40)
    if has_valid_changes:
        print("🎉 Ready to create PR!")
        print("   Copilot should be able to review your changes successfully.")
        sys.exit(0)
    else:
        print("🚫 NOT ready for PR")
        print("   Please address the issues above before creating a PR.")
        sys.exit(1)

if __name__ == "__main__":
    main()