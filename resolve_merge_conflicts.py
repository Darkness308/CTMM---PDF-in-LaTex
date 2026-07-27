#!/usr/bin/env python3
"""
<<<<<<< HEAD
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
    # This pattern matches conflict start marker: exactly 7 '<' chars followed by space or EOL
    conflict_pattern = r'^<{7}(\s|$)'
    if not re.search(conflict_pattern, content, re.MULTILINE):
        return True, "No conflicts found"

    # Pattern to match conflict blocks
    # <<<<<<< HEAD (or any branch name) - exactly 7 '<' chars
    # ... content from HEAD ...
    # ======= - exactly 7 '=' chars
    # ... content from incoming branch ...
    # >>>>>>> branch-name - exactly 7 '>' chars

    lines = content.split('\n')
    resolved_lines = []
    in_conflict = False
    in_head_section = False
    conflict_count = 0

    # Compile regex patterns for conflict markers (exactly 7 chars)
    conflict_start_re = re.compile(r'^<{7}(\s|$)')
    conflict_sep_re = re.compile(r'^={7}(\s|$)')
    conflict_end_re = re.compile(r'^>{7}(\s|$)')

    for i, line in enumerate(lines):
        if conflict_start_re.match(line):
            # Start of conflict - we want to keep what follows
            in_conflict = True
            in_head_section = True
            conflict_count += 1
            continue
        elif conflict_sep_re.match(line) and in_conflict:
            # End of HEAD section, start of incoming section (which we discard)
            in_head_section = False
            continue
        elif conflict_end_re.match(line) and in_conflict:
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
=======
Automatic Merge Conflict Resolver
Resolves Git merge conflicts by intelligently choosing the appropriate version.
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


class MergeConflictResolver:
    """Resolves Git merge conflicts in files."""

    def __init__(self):
        self.conflict_pattern = re.compile(
            r'<<<<<<< HEAD\n(.*?)\n=======\n(.*?)\n>>>>>>> pr-653',
            re.DOTALL
        )

    def resolve_conflict(self, head_content: str, pr_content: str, context: str = "") -> str:
        """
        Resolve a single conflict by choosing the appropriate version.

        Strategy:
        1. If pr_content is empty/whitespace, keep head_content
        2. If head_content is empty/whitespace, keep pr_content
        3. If both have content, try to merge intelligently
        4. Default: keep head_content (current branch)
        """
        head_stripped = head_content.strip()
        pr_stripped = pr_content.strip()

        # If one side is empty, use the other
        if not head_stripped and pr_stripped:
            logger.debug("Keeping pr-653 content (HEAD is empty)")
            return pr_content
        elif not pr_stripped and head_stripped:
            logger.debug("Keeping HEAD content (pr-653 is empty)")
            return head_content
        elif not head_stripped and not pr_stripped:
            logger.debug("Both sides empty, removing conflict marker")
            return ""

        # Check if contents are identical (just whitespace differences)
        if head_stripped == pr_stripped:
            logger.debug("Contents identical, keeping HEAD version")
            return head_content

        # Check if one is a subset/superset of the other
        if pr_stripped in head_stripped:
            logger.debug("HEAD contains pr-653 content, keeping HEAD")
            return head_content
        elif head_stripped in pr_stripped:
            logger.debug("pr-653 contains HEAD content, keeping pr-653")
            return pr_content

        # For different content, keep HEAD (current branch)
        logger.debug("Content differs, keeping HEAD version")
        return head_content

    def resolve_file(self, filepath: Path) -> Tuple[bool, int]:
        """
        Resolve all conflicts in a file.

        Returns:
            Tuple of (success, conflicts_resolved)
        """
        try:
            content = filepath.read_text(encoding='utf-8')
        except Exception as e:
            logger.error(f"Error reading {filepath}: {e}")
            return False, 0

        # Check if file has conflicts
        if '<<<<<<< HEAD' not in content:
            logger.info(f"No conflicts in {filepath}")
            return True, 0

        original_content = content
        conflicts_found = len(re.findall(r'<<<<<<< HEAD', content))

        # Resolve all conflicts
        def replace_conflict(match):
            head_content = match.group(1)
            pr_content = match.group(2)
            return self.resolve_conflict(head_content, pr_content)

        resolved_content = self.conflict_pattern.sub(replace_conflict, content)

        # Verify all conflicts were resolved
        remaining_conflicts = len(re.findall(r'<<<<<<< HEAD', resolved_content))
        if remaining_conflicts > 0:
            logger.warning(f"Could not resolve all conflicts in {filepath}: {remaining_conflicts} remaining")
            return False, conflicts_found - remaining_conflicts

        # Write resolved content
        try:
            filepath.write_text(resolved_content, encoding='utf-8')
            logger.info(f"[OK] Resolved {conflicts_found} conflicts in {filepath}")
            return True, conflicts_found
        except Exception as e:
            logger.error(f"Error writing {filepath}: {e}")
            return False, 0

    def resolve_all(self, directory: Path = None) -> Tuple[int, int]:
        """
        Resolve conflicts in all files in the directory.

        Returns:
            Tuple of (files_resolved, total_conflicts_resolved)
        """
        if directory is None:
            directory = Path.cwd()

        files_resolved = 0
        conflicts_resolved = 0

        # Find all files with conflicts
        conflict_files = []
        for filepath in directory.rglob('*'):
            if filepath.is_file() and not any(part.startswith('.') for part in filepath.parts[:-1]):
                # Skip hidden directories but not .github
                if '.git' in str(filepath) and '.github' not in str(filepath):
                    continue
                try:
                    content = filepath.read_text(encoding='utf-8', errors='ignore')
                    if '<<<<<<< HEAD' in content:
                        conflict_files.append(filepath)
                except:
                    continue

        logger.info(f"Found {len(conflict_files)} files with conflicts")

        for filepath in conflict_files:
            success, num_conflicts = self.resolve_file(filepath)
            if success:
                files_resolved += 1
                conflicts_resolved += num_conflicts

        return files_resolved, conflicts_resolved


def main():
    """Main entry point."""
    resolver = MergeConflictResolver()

    # Get directory from command line or use current directory
    if len(sys.argv) > 1:
        directory = Path(sys.argv[1])
    else:
        directory = Path.cwd()

    logger.info(f"Resolving merge conflicts in {directory}")
    files_resolved, conflicts_resolved = resolver.resolve_all(directory)

    logger.info("")
    logger.info("=" * 60)
    logger.info(f"Summary:")
    logger.info(f"  Files resolved: {files_resolved}")
    logger.info(f"  Conflicts resolved: {conflicts_resolved}")
    logger.info("=" * 60)

    return 0 if files_resolved > 0 else 1


if __name__ == '__main__':
>>>>>>> origin/main
    sys.exit(main())
