#!/usr/bin/env python3
"""
Comprehensive Disruptive Character Removal Script

This script removes all disruptive characters that could cause merge conflicts:
- Emojis (all Unicode emojis)
- Special Unicode symbols that can be misinterpreted
- While preserving intentional examples in documentation

The script creates backups and provides detailed reporting.
"""

import os
import re
import shutil
from pathlib import Path
from typing import List, Dict, Tuple

# Emoji patterns - comprehensive coverage
EMOJI_PATTERNS = [
    r'[\U0001F300-\U0001F9FF]',  # Main emoji block
    r'[\U00002600-\U000027BF]',  # Dingbats and misc symbols
    r'[\U0001F600-\U0001F64F]',  # Emoticons
    r'[\U0001F680-\U0001F6FF]',  # Transport and map
    r'[\U00002700-\U000027BF]',  # Dingbats
    r'[\U0001F900-\U0001F9FF]',  # Supplemental symbols
    r'[\U0001FA00-\U0001FA6F]',  # Extended symbols
    r'[\U00002300-\U000023FF]',  # Misc technical
    r'[\U0001F1E0-\U0001F1FF]',  # Flags
]

# Compile combined pattern
EMOJI_REGEX = re.compile('|'.join(EMOJI_PATTERNS))

# Common emoji replacements for maintaining meaning
EMOJI_REPLACEMENTS = {
    # Check marks and crosses
    '✅': '[PASS]',
    '✓': '[OK]',
    '❌': '[FAIL]',
    '✗': '[ERROR]',
    '⚠️': '[WARN]',
    '⚠': '[WARN]',

    # Symbols
    '🔍': '[SEARCH]',
    '📋': '[TEST]',
    '📄': '[FILE]',
    '📊': '[SUMMARY]',
    '🔧': '[FIX]',
    '🔄': '[SYNC]',
    '🎉': '[SUCCESS]',
    '🎯': '[TARGET]',
    '💥': '[ERROR]',
    '🧪': '[TEST]',
    '🚀': '[DEPLOY]',
    '📦': '[PACKAGE]',
    '🔑': '[KEY]',
    '🛠️': '[TOOLS]',
    '🛠': '[TOOLS]',
    '📝': '[NOTE]',
    '📌': '[PIN]',
    '💡': '[IDEA]',
    '🎨': '[DESIGN]',
    '🐛': '[BUG]',
    '🔒': '[SECURE]',
    '🔓': '[UNLOCK]',
    '⭐': '[STAR]',
    '✨': '[NEW]',
    '🏷️': '[TAG]',
    '🏷': '[TAG]',
    '📱': '[MOBILE]',
    '💻': '[CODE]',
    '🖥️': '[DESKTOP]',
    '🖥': '[DESKTOP]',
    '⚡': '[FAST]',
    '🔥': '[HOT]',
    '❤️': '[LOVE]',
    '❤': '[LOVE]',
    '💚': '[LIKE]',
    '👍': '[THUMBSUP]',
    '👎': '[THUMBSDOWN]',
    '👀': '[EYES]',
    '🎓': '[EDUCATION]',
    '📚': '[DOCS]',
    '🌐': '[WEB]',
    '🔗': '[LINK]',

    # Bullets and markers
    '•': '*',
    '◦': '-',
    '▪': '*',
    '▫': '-',
    '►': '>',
    '▶': '>',
    '▸': '>',
    '▹': '>',
    '→': '->',
    '←': '<-',
    '↑': '^',
    '↓': 'v',
    '↔': '<->',
    '⇒': '=>',
    '⇐': '<=',
    '⇔': '<=>',
}

# Files to skip (documentation about problematic characters)
SKIP_FILES = {
    'PROBLEMATIC_CHARACTERS_REFERENCE.md',
    'MERGE_CONFLICT_CHARACTER_ANALYSIS.md',
    'DISRUPTIVE_CHARACTERS_REMOVAL_COMPLETE.md',
    'remove_all_disruptive_chars.py',
}

# Directories to skip
SKIP_DIRS = {
    '.git', '.github', 'build', 'converted', '__pycache__', 'node_modules',
    '.vscode', '.devcontainer', 'therapie-material'
}


class CharacterRemover:
    """Removes disruptive characters from files."""

    def __init__(self, dry_run: bool = False, create_backups: bool = True):
        self.dry_run = dry_run
        self.create_backups = create_backups
        self.files_processed = 0
        self.files_modified = 0
        self.emojis_removed = 0
        self.changes_log = []

    def should_skip_file(self, filepath: Path) -> bool:
        """Determine if a file should be skipped."""
        if filepath.name in SKIP_FILES:
            return True

        # Skip files in skip directories
        for skip_dir in SKIP_DIRS:
            if skip_dir in filepath.parts:
                return True

        return False

    def replace_emoji(self, match) -> str:
        """Replace an emoji with its text equivalent."""
        emoji = match.group(0)

        # Check for direct replacement
        if emoji in EMOJI_REPLACEMENTS:
            return EMOJI_REPLACEMENTS[emoji]

        # Check for emoji with variation selector (U+FE0F)
        emoji_base = emoji.rstrip('\uFE0F')
        if emoji_base in EMOJI_REPLACEMENTS:
            return EMOJI_REPLACEMENTS[emoji_base]

        # Default: remove it
        return ''

    def clean_content(self, content: str, filepath: Path) -> Tuple[str, int]:
        """Clean disruptive characters from content."""
        original_content = content
        emojis_in_file = 0

        # Count emojis first
        emojis_in_file = len(EMOJI_REGEX.findall(content))

        # Replace emojis
        content = EMOJI_REGEX.sub(self.replace_emoji, content)

        # Clean up multiple spaces left by removals (but NOT at start of lines - preserve indentation)
        # Only clean up spaces in the middle of lines (preceded by non-whitespace)
        lines = content.split('\n')
        cleaned_lines = []
        for line in lines:
            # Only clean up multiple spaces that are not at the start of the line
            if line.lstrip():  # If line has non-whitespace content
                # Get leading whitespace
                leading = line[:len(line) - len(line.lstrip())]
                # Get rest of line
                rest = line[len(leading):]
                # Clean up multiple spaces in rest (not indentation)
                rest = re.sub(r' {3,}', '  ', rest)
                cleaned_lines.append(leading + rest)
            else:
                cleaned_lines.append(line)
        content = '\n'.join(cleaned_lines)

        # Clean up empty lines (more than 3 consecutive)
        content = re.sub(r'\n{4,}', '\n\n\n', content)

        return content, emojis_in_file

    def process_file(self, filepath: Path) -> bool:
        """Process a single file."""
        self.files_processed += 1

        if self.should_skip_file(filepath):
            return False

        try:
            # Read file
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                original_content = f.read()

            # Clean content
            cleaned_content, emojis_count = self.clean_content(original_content, filepath)

            # Check if modified
            if cleaned_content != original_content:
                self.files_modified += 1
                self.emojis_removed += emojis_count

                # Log changes
                self.changes_log.append({
                    'file': str(filepath),
                    'emojis_removed': emojis_count,
                    'size_before': len(original_content),
                    'size_after': len(cleaned_content)
                })

                if not self.dry_run:
                    # Create backup
                    if self.create_backups:
                        backup_path = filepath.with_suffix(filepath.suffix + '.backup')
                        shutil.copy2(filepath, backup_path)

                    # Write cleaned content
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(cleaned_content)

                return True

            return False

        except Exception as e:
            print(f"Error processing {filepath}: {e}")
            return False

    def process_directory(self, directory: Path, extensions: List[str]):
        """Process all files in directory with given extensions."""
        for root, dirs, files in os.walk(directory):
            # Remove skip directories from traversal
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]

            for file in files:
                # Check extension
                if not any(file.endswith(ext) for ext in extensions):
                    continue

                filepath = Path(root) / file
                self.process_file(filepath)

    def print_summary(self):
        """Print summary of changes."""
        print("\n" + "=" * 80)
        print("DISRUPTIVE CHARACTER REMOVAL SUMMARY")
        print("=" * 80)
        print(f"\nMode: {'DRY RUN' if self.dry_run else 'LIVE'}")
        print(f"Files processed: {self.files_processed}")
        print(f"Files modified: {self.files_modified}")
        print(f"Emojis removed: {self.emojis_removed}")

        if self.changes_log:
            print(f"\nTop 20 files with most changes:")
            sorted_changes = sorted(self.changes_log, key=lambda x: -x['emojis_removed'])
            for change in sorted_changes[:20]:
                print(f"  {change['file']}")
                print(f"    Emojis removed: {change['emojis_removed']}")
                print(f"    Size: {change['size_before']} -> {change['size_after']} bytes")

        print("\n" + "=" * 80)

        if self.dry_run:
            print("\nThis was a DRY RUN. No files were modified.")
            print("Run with --execute to apply changes.")
        else:
            print("\nChanges applied successfully!")
            if self.create_backups:
                print("Backups created with .backup extension.")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Remove all disruptive characters from repository files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --dry-run                    # Preview changes
  %(prog)s --execute                    # Apply changes
  %(prog)s --execute --no-backups       # Apply without backups
        """
    )
    parser.add_argument('--dry-run', action='store_true',
                        help='Preview changes without modifying files (default)')
    parser.add_argument('--execute', action='store_true',
                        help='Actually modify files')
    parser.add_argument('--no-backups', action='store_true',
                        help='Do not create backup files')
    parser.add_argument('--dir', type=str, default='.',
                        help='Directory to process (default: current)')
    parser.add_argument('--extensions', type=str, default='.py,.tex,.md,.yml,.yaml,.sty,.sh',
                        help='Comma-separated file extensions (default: .py,.tex,.md,.yml,.yaml,.sty,.sh)')

    args = parser.parse_args()

    # Parse extensions
    extensions = [ext.strip() if ext.startswith('.') else f'.{ext.strip()}'
                  for ext in args.extensions.split(',')]

    # Determine mode
    dry_run = not args.execute
    create_backups = not args.no_backups

    if dry_run:
        print("=" * 80)
        print("DRY RUN MODE - No files will be modified")
        print("=" * 80)

    # Create remover
    remover = CharacterRemover(dry_run=dry_run, create_backups=create_backups)

    # Process directory
    directory = Path(args.dir)
    if not directory.exists():
        print(f"Error: Directory '{directory}' does not exist")
        return 1

    print(f"\nProcessing directory: {directory.absolute()}")
    print(f"File extensions: {', '.join(extensions)}")
    print()

    remover.process_directory(directory, extensions)
    remover.print_summary()

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
