#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Remove ALL Conflicting Characters That Block Merges

This script removes ALL emoji and special Unicode characters from source files
that can cause merge conflicts. It uses a comprehensive approach.

German: Entfernt ALLE störenden Zeichen, die Merges blockieren.
"""

import os
import re
from pathlib import Path

class ComprehensiveCharacterRemover:
    def __init__(self, dry_run=False):
        self.dry_run = dry_run
        self.stats = {
            'files_scanned': 0,
            'files_modified': 0,
            'characters_replaced': 0,
        }
        self.files_with_changes = []
        # Valid German and European characters
        self.valid_chars = set('äöüÄÖÜßáàâéèêíìîóòôúùûÁÀÂÉÈÊÍÌÎÓÒÔÚÙÛ')

    def should_process(self, filepath):
        """Check if file should be processed"""
        if '.git' in Path(filepath).parts:
            return False

        skip_dirs = ['converted', 'merge_conflict_analysis', 'merge_conflict_resolution']
        for skip_dir in skip_dirs:
            if skip_dir in Path(filepath).parts:
                return False

        extensions = ('.py', '.tex', '.sty')
        return filepath.endswith(extensions)

    def replace_character(self, char):
        """Replace a single character with ASCII equivalent"""
        code = ord(char)

        # Keep ASCII and valid German characters
        if code <= 127:
            return char
        if char in self.valid_chars:
            return char

        # Common special characters
        replacements = {
            # Punctuation
            '\u2013': '--',  # en-dash
            '\u2014': '---',  # em-dash
            '\u2018': "'",  # left single quote
            '\u2019': "'",  # right single quote
            '\u201C': '"',  # left double quote
            '\u201D': '"',  # right double quote
            '\u2026': '...',  # ellipsis
            '\u2022': '*',  # bullet
            '\u2192': '->',  # right arrow
            '\u2713': '[OK]',  # checkmark
            '\u2717': '[X]',  # x mark
            '\u2705': '[PASS]',# heavy check mark
            '\u274C': '[FAIL]',# cross mark

            # Math
            '\u2264': '<=',  # less than or equal
            '\u2265': '>=',  # greater than or equal

            # Box drawing
            '\u250C': '+',  # box top-left
            '\u2500': '-',  # box horizontal
            '\u2514': '+',  # box bottom-left
            '\u251C': '+',  # box vertical-right
            '\u2502': '|',  # box vertical

            # Arrows
            '\u2795': '[+]',  # heavy plus
            '\u2796': '[-]',  # heavy minus
            '\u27A4': '->',  # right arrow

            # Currency and symbols
            '\u20AC': 'EUR',  # euro
            '\u2122': '(TM)',  # trademark

            # Variation selector
            '\uFE0F': '',  # remove
        }

        if char in replacements:
            return replacements[char]

        # For all other high Unicode (including ALL emojis)
        # Replace with a generic placeholder
        if code >= 0x1F000:  # Emoji range and above
            return '[EMOJI]'
        elif code >= 0x2000 and code <= 0x2FFF:  # Special symbols
            return '[SYM]'
        elif code >= 0x3000:  # CJK and other high ranges
            return '[CHAR]'

        # For anything else > 255, use generic replacement
        if code > 255:
            return '[?]'

        return char

    def clean_text(self, text):
        """Clean all problematic characters from text"""
        result = []
        replacements = 0

        for char in text:
            new_char = self.replace_character(char)
            if new_char != char:
                replacements += 1
            result.append(new_char)

        return ''.join(result), replacements

    def process_file(self, filepath):
        """Process a single file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                original_content = f.read()

            new_content, replacements = self.clean_text(original_content)

            if replacements > 0:
                self.files_with_changes.append((filepath, replacements))

                if not self.dry_run:
                    with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
                        f.write(new_content)

                self.stats['files_modified'] += 1
                self.stats['characters_replaced'] += replacements
                return True

            return False

        except Exception as e:
            print(f"Error processing {filepath}: {e}")
            return False

    def process_directory(self, directory='.'):
        """Process all files in directory"""
        print("Scanning repository for ALL conflicting characters...")
        print(f"Mode: {'DRY RUN' if self.dry_run else 'FIXING FILES'}\n")

        for root, dirs, files in os.walk(directory):
            if '.git' in dirs:
                dirs.remove('.git')

            for skip_dir in ['converted', 'merge_conflict_analysis', 'merge_conflict_resolution']:
                if skip_dir in dirs:
                    dirs.remove(skip_dir)

            for file in files:
                filepath = os.path.join(root, file)

                if not self.should_process(filepath):
                    continue

                self.stats['files_scanned'] += 1
                self.process_file(filepath)

        print(f"Scanned {self.stats['files_scanned']} source files")
        print(f"Found {len(self.files_with_changes)} files with conflicting characters\n")

        if not self.files_with_changes:
            print("[PASS] No conflicting characters found!")
            return

        print("Files with conflicting characters (showing first 50):")
        for filepath, count in self.files_with_changes[:50]:
            print(f"  {filepath}: {count} character(s)")

        if len(self.files_with_changes) > 50:
            print(f"\n... and {len(self.files_with_changes) - 50} more files")

        print(f"\n{'='*60}")
        print("SUMMARY")
        print(f"{'='*60}")
        print(f"Files scanned:  {self.stats['files_scanned']}")
        print(f"Files modified:  {self.stats['files_modified']}")
        print(f"Characters replaced:  {self.stats['characters_replaced']}")

        if self.dry_run:
            print("\nRun without --dry-run to apply changes")
        else:
            print("\n[PASS] All conflicting characters removed!")

        print(f"{'='*60}\n")


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Remove ALL conflicting characters that block merges'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Only report issues without fixing them'
    )
    parser.add_argument(
        'directory',
        nargs='?',
        default='.',
        help='Directory to process (default: current directory)'
    )

    args = parser.parse_args()

    remover = ComprehensiveCharacterRemover(dry_run=args.dry_run)
    remover.process_directory(args.directory)


if __name__ == '__main__':
    main()
