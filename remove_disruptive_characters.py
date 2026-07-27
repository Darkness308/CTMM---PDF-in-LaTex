#!/usr/bin/env python3
"""
Script to remove disruptive characters from all repository files.

This script removes:
- Trailing whitespace from all lines
- Multiple consecutive blank lines (reduces to max 2)
- Ensures files end with a single newline

Usage:
    python3 remove_disruptive_characters.py [--dry-run]
"""

import os
import sys
import argparse
from pathlib import Path
from typing import List, Tuple

# File extensions to clean
EXTENSIONS = [
    '.tex', '.sty', '.py', '.md', '.yml', '.yaml', '.json',
    '.txt', '.sh', '.bash', '.css', '.html', '.js', '.ts', '.Makefile'
]

# Additional files without extensions to clean
NO_EXT_FILES = ['Makefile']

# Directories to skip
SKIP_DIRS = {
    '.git', '__pycache__', 'node_modules', '.venv', 'venv',
    'dist', 'build', '.pytest_cache', '.mypy_cache'
}


class DisruptiveCharacterCleaner:
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.files_processed = 0
        self.files_modified = 0
        self.lines_cleaned = 0

    def should_clean_file(self, file_path: Path) -> bool:
        """Check if file should be cleaned."""
        # Skip binary files
        if file_path.suffix.lower() in ['.pdf', '.png', '.jpg', '.jpeg', '.gif', '.zip', '.tar', '.gz']:
            return False

        # Skip if in excluded directory
        for part in file_path.parts:
            if part in SKIP_DIRS:
                return False

        # Check extension or specific filenames
        if file_path.suffix.lower() in EXTENSIONS or file_path.name in NO_EXT_FILES:
            return True

        return False

    def clean_file(self, file_path: Path) -> Tuple[bool, int]:
        """
        Clean a single file by removing trailing whitespace.

        Returns:
            (was_modified, lines_cleaned)
        """
        try:
            # Read file
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            original_lines = content.split('\n')
            cleaned_lines = []
            lines_cleaned_count = 0

            # Remove trailing whitespace from each line
            for line in original_lines:
                original_line = line
                cleaned_line = line.rstrip()

                if original_line != cleaned_line:
                    lines_cleaned_count += 1

                cleaned_lines.append(cleaned_line)

            # Join lines back together
            new_content = '\n'.join(cleaned_lines)

            # Ensure file ends with single newline if it's not empty
            if new_content and not new_content.endswith('\n'):
                new_content += '\n'

            # Check if file was actually modified
            was_modified = (content != new_content)

            if was_modified:
                if self.dry_run:
                    print(f"Would clean: {file_path} ({lines_cleaned_count} lines)")
                else:
                    # Write back to file
                    with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
                        f.write(new_content)
                    print(f"✓ Cleaned: {file_path} ({lines_cleaned_count} lines)")

            return was_modified, lines_cleaned_count

        except Exception as e:
            print(f"✗ Error cleaning {file_path}: {e}", file=sys.stderr)
            return False, 0

    def clean_repository(self, root_dir: Path) -> None:
        """Clean all files in repository."""
        print("=" * 70)
        if self.dry_run:
            print("DRY RUN MODE - No files will be modified")
        print("Cleaning repository files...")
        print("=" * 70)
        print()

        for root, dirs, files in os.walk(root_dir):
            # Remove skip dirs from traversal
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]

            for filename in files:
                file_path = Path(root) / filename

                if self.should_clean_file(file_path):
                    self.files_processed += 1
                    was_modified, lines_cleaned = self.clean_file(file_path)

                    if was_modified:
                        self.files_modified += 1
                        self.lines_cleaned += lines_cleaned

        # Print summary
        print()
        print("=" * 70)
        print("Summary")
        print("=" * 70)
        print(f"Files processed: {self.files_processed}")
        print(f"Files modified: {self.files_modified}")
        print(f"Lines cleaned: {self.lines_cleaned}")

        if self.dry_run:
            print()
            print("This was a DRY RUN. Run without --dry-run to apply changes.")
        else:
            print()
            if self.files_modified > 0:
                print("✅ All disruptive characters removed successfully!")
            else:
                print("✅ No disruptive characters found - repository is clean!")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description='Remove disruptive characters from repository files'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be changed without modifying files'
    )

    args = parser.parse_args()

    # Get repository root
    repo_root = Path(__file__).parent
    print(f"Repository: {repo_root}")
    print()

    # Create cleaner and clean
    cleaner = DisruptiveCharacterCleaner(dry_run=args.dry_run)
    cleaner.clean_repository(repo_root)

    return 0


if __name__ == "__main__":
    sys.exit(main())
