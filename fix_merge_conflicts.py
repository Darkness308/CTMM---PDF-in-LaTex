#!/usr/bin/env python3
"""
Fix Merge-Blocking Characters in Repository Files

This script identifies and fixes characters that could prevent merges:
- Ensures all files are UTF-8 encoded
- Removes trailing whitespace
- Normalizes line endings to LF
- Removes BOM (Byte Order Mark) if present

German: Behebt alle störenden Zeichen in Dateien, die einen Merge verhindern.
"""

import os
import sys
import chardet
from pathlib import Path

class MergeConflictFixer:
    def __init__(self, dry_run=False):
        self.dry_run = dry_run
        self.stats = {
            'files_scanned': 0,
            'files_fixed': 0,
            'encoding_fixes': 0,
            'whitespace_fixes': 0,
            'bom_fixes': 0,
            'line_ending_fixes': 0,
        }
        self.issues_found = []

    def should_process(self, filepath):
        """Check if file should be processed"""
        # Skip .git directory
        if '.git' in Path(filepath).parts:
            return False

        # Process specific file types
        extensions = ('.tex', '.sty', '.md', '.py', '.yml', '.yaml', '.sh', '.json')
        return filepath.endswith(extensions)

    def detect_issues(self, filepath):
        """Detect encoding and whitespace issues in a file"""
        issues = []

        try:
            with open(filepath, 'rb') as f:
                raw = f.read()

            # Check for BOM
            has_bom = False
            if raw.startswith(b'\xef\xbb\xbf'):
                issues.append('UTF-8 BOM')
                has_bom = True
            elif raw.startswith(b'\xff\xfe') or raw.startswith(b'\xfe\xff'):
                issues.append('UTF-16 BOM')
                has_bom = True

            # Check encoding
            result = chardet.detect(raw)
            encoding = result.get('encoding', 'unknown')

            # chardet can be overly sensitive, so check if it's actually valid UTF-8
            try:
                raw.decode('utf-8')
                actual_encoding = 'utf-8'
            except UnicodeDecodeError:
                actual_encoding = encoding

            if actual_encoding and actual_encoding.lower() not in ['utf-8', 'ascii']:
                issues.append(f'Non-UTF-8 encoding: {actual_encoding}')

            # Check for trailing whitespace and line endings
            try:
                text = raw.decode('utf-8', errors='ignore')
                lines = text.split('\n')

                trailing_ws_count = 0
                for line in lines:
                    if line and line != line.rstrip():
                        trailing_ws_count += 1

                if trailing_ws_count > 5:
                    issues.append(f'Trailing whitespace ({trailing_ws_count} lines)')

                # Check for CRLF
                if '\r\n' in text:
                    issues.append('CRLF line endings')

            except Exception as e:
                issues.append(f'Could not analyze content: {e}')

            return issues

        except Exception as e:
            return [f'Error reading file: {e}']

    def fix_file(self, filepath):
        """Fix encoding and whitespace issues in a file"""
        try:
            # Read file
            with open(filepath, 'rb') as f:
                raw = f.read()

            fixed = False

            # Remove BOM if present
            if raw.startswith(b'\xef\xbb\xbf'):
                raw = raw[3:]
                self.stats['bom_fixes'] += 1
                fixed = True
            elif raw.startswith(b'\xff\xfe') or raw.startswith(b'\xfe\xff'):
                raw = raw[2:]
                self.stats['bom_fixes'] += 1
                fixed = True

            # Try to decode and re-encode as UTF-8
            try:
                text = raw.decode('utf-8')
            except UnicodeDecodeError:
                # Try with chardet
                result = chardet.detect(raw)
                encoding = result.get('encoding', 'latin-1')
                try:
                    text = raw.decode(encoding)
                    self.stats['encoding_fixes'] += 1
                    fixed = True
                except Exception:
                    text = raw.decode('latin-1', errors='ignore')
                    self.stats['encoding_fixes'] += 1
                    fixed = True

            # Fix line endings (CRLF -> LF)
            if '\r\n' in text:
                text = text.replace('\r\n', '\n')
                self.stats['line_ending_fixes'] += 1
                fixed = True

            # Remove trailing whitespace
            lines = text.split('\n')
            new_lines = []
            whitespace_fixed = False

            for line in lines:
                original = line
                line = line.rstrip()
                if line != original:
                    whitespace_fixed = True
                new_lines.append(line)

            if whitespace_fixed:
                self.stats['whitespace_fixes'] += 1
                fixed = True

            new_text = '\n'.join(new_lines)

            # Ensure file ends with newline if it had content
            if new_text and not new_text.endswith('\n'):
                new_text += '\n'

            if fixed:
                if not self.dry_run:
                    # Write back as UTF-8
                    with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
                        f.write(new_text)

                self.stats['files_fixed'] += 1
                return True

            return False

        except Exception as e:
            print(f"Error fixing {filepath}: {e}")
            return False

    def process_directory(self, directory='.'):
        """Process all files in directory"""
        print("Scanning repository for merge-blocking characters...")
        print(f"Mode: {'DRY RUN' if self.dry_run else 'FIXING FILES'}\n")

        # First pass: identify issues
        for root, dirs, files in os.walk(directory):
            # Remove .git from dirs to skip it
            if '.git' in dirs:
                dirs.remove('.git')

            for file in files:
                filepath = os.path.join(root, file)

                if not self.should_process(filepath):
                    continue

                self.stats['files_scanned'] += 1
                issues = self.detect_issues(filepath)

                if issues:
                    self.issues_found.append((filepath, issues))

        # Report findings
        print(f"Scanned {self.stats['files_scanned']} files")
        print(f"Found {len(self.issues_found)} files with issues\n")

        if not self.issues_found:
            print("[PASS] No merge-blocking characters found!")
            return

        # Show sample of issues
        print("Sample of files with issues (first 20):")
        for filepath, issues in self.issues_found[:20]:
            print(f"\n{filepath}:")
            for issue in issues:
                print(f"  - {issue}")

        if len(self.issues_found) > 20:
            print(f"\n... and {len(self.issues_found) - 20} more files")

        # Second pass: fix issues
        if not self.dry_run:
            print(f"\n{'='*60}")
            print("Fixing files...")
            print(f"{'='*60}\n")

            for filepath, _ in self.issues_found:
                if self.fix_file(filepath):
                    print(f"[OK] Fixed: {filepath}")

        # Final report
        print(f"\n{'='*60}")
        print("SUMMARY")
        print(f"{'='*60}")
        print(f"Files scanned:  {self.stats['files_scanned']}")
        print(f"Files with issues:  {len(self.issues_found)}")

        if not self.dry_run:
            print(f"Files fixed:  {self.stats['files_fixed']}")
            print(f"Encoding fixes:  {self.stats['encoding_fixes']}")
            print(f"Whitespace fixes:  {self.stats['whitespace_fixes']}")
            print(f"BOM removals:  {self.stats['bom_fixes']}")
            print(f"Line ending fixes:  {self.stats['line_ending_fixes']}")
        else:
            print("\nRun without --dry-run to apply fixes")

        print(f"{'='*60}\n")

        if not self.dry_run and self.stats['files_fixed'] > 0:
            print("[PASS] All merge-blocking characters have been fixed!")
            print("  Files are now UTF-8 encoded with LF line endings.")
            print("  Trailing whitespace has been removed.")


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Fix merge-blocking characters in repository files'
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

    fixer = MergeConflictFixer(dry_run=args.dry_run)
    fixer.process_directory(args.directory)

    # Exit with error code if issues found (for CI)
    if fixer.issues_found and args.dry_run:
        sys.exit(1)


if __name__ == '__main__':
    main()
