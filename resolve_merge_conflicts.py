#!/usr/bin/env python3
"""
Script to automatically resolve merge conflicts by removing conflict markers
and keeping the HEAD version (from copilot/fix-314 branch).

This script:
1. Finds all files with merge conflict markers
2. Removes the markers and keeps the HEAD version
3. Stages the resolved files
"""

import os
import sys
import re
import subprocess
from pathlib import Path
from typing import List, Tuple

def find_conflict_files() -> List[str]:
    """Find all files with merge conflicts using git status."""
    
    result = subprocess.run(
        ['git', 'diff', '--name-only', '--diff-filter=U'],
        capture_output=True,
        text=True,
        check=True
    )
    
    files = result.stdout.strip().split('\n')
    return [f for f in files if f]

def resolve_conflicts_in_file(file_path: str) -> Tuple[bool, str]:
    """
    Resolve merge conflicts in a file by keeping HEAD version.
    
    Returns:
        Tuple of (success, message)
    """
    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    except Exception as e:
        return False, f"Failed to read file: {e}"
    
    # Check if file has conflict markers using regex for better detection
    # This pattern matches any conflict start marker regardless of branch name
    conflict_pattern = r'^<{7}\s'
    if not re.search(conflict_pattern, content, re.MULTILINE):
        return True, "No conflicts found"
    
    # Pattern to match conflict blocks
    # <<<<<<< HEAD (or any branch name)
    # ... content from HEAD ...
    # =======
    # ... content from incoming branch ...
    # >>>>>>> branch-name
    
    lines = content.split('\n')
    resolved_lines = []
    in_conflict = False
    in_head_section = False
    conflict_count = 0
    
    for i, line in enumerate(lines):
        if line.startswith('<<<<<<< '):
            # Start of conflict - we want to keep what follows
            in_conflict = True
            in_head_section = True
            conflict_count += 1
            continue
        elif line.startswith('=======') and in_conflict:
            # End of HEAD section, start of main section (which we discard)
            in_head_section = False
            continue
        elif line.startswith('>>>>>>> ') and in_conflict:
            # End of conflict
            in_conflict = False
            in_head_section = False
            continue
        elif in_conflict and in_head_section:
            # This is content from HEAD - keep it
            resolved_lines.append(line)
        elif not in_conflict:
            # Not in a conflict block - keep the line
            resolved_lines.append(line)
        # else: in conflict but not in HEAD section - discard (it's from main)
    
    # Write resolved content
    try:
        resolved_content = '\n'.join(resolved_lines)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(resolved_content)
        return True, f"Resolved {conflict_count} conflict(s)"
    except Exception as e:
        return False, f"Failed to write file: {e}"

def main():
    """Main function to resolve all merge conflicts."""
    print("=" * 70)
    print("Merge Conflict Resolution - Keeping HEAD (copilot/fix-314) version")
    print("=" * 70)
    print()
    
    # Find all files with conflicts
    print("🔍 Finding files with merge conflicts...")
    conflict_files = find_conflict_files()
    
    if not conflict_files:
        print("✅ No files with merge conflicts found!")
        return 0
    
    print(f"Found {len(conflict_files)} file(s) with conflicts:\n")
    for f in conflict_files:
        print(f"  - {f}")
    print()
    
    # Resolve each file
    resolved_count = 0
    failed_count = 0
    
    for file_path in conflict_files:
        print(f"📄 Resolving: {file_path}")
        success, message = resolve_conflicts_in_file(file_path)
        
        if success:
            print(f"   ✅ {message}")
            resolved_count += 1
            
            # Stage the resolved file
            try:
                subprocess.run(['git', 'add', file_path], check=True)
                print(f"   📌 Staged for commit")
            except Exception as e:
                print(f"   ⚠️  Warning: Could not stage file: {e}")
        else:
            print(f"   ❌ {message}")
            failed_count += 1
        print()
    
    # Summary
    print("=" * 70)
    print("📊 Summary:")
    print(f"   Successfully resolved: {resolved_count}/{len(conflict_files)}")
    if failed_count > 0:
        print(f"   Failed: {failed_count}/{len(conflict_files)}")
    print("=" * 70)
    print()
    
    if failed_count == 0:
        print("✅ All conflicts resolved successfully!")
        print("   Run 'git status' to review changes")
        print("   Run 'git commit' to complete the merge")
        return 0
    else:
        print("⚠️  Some files could not be resolved automatically")
        return 1

if __name__ == "__main__":
    sys.exit(main())
