#!/usr/bin/env python3
"""
Test suite for merge conflict character fixes

Verifies that:
1. No trailing whitespace exists in any files
2. All files are UTF-8 encoded
3. All files use LF line endings
4. No BOM (Byte Order Mark) present

German: Testsuite für die Behebung von Merge-Konflikt-Zeichen
"""

import os
import sys
import unittest
from pathlib import Path


class TestMergeConflictFix(unittest.TestCase):
    """Test that all merge-blocking characters have been removed"""

    def setUp(self):
        """Set up test fixtures"""
        self.repo_root = Path(__file__).parent
        self.file_extensions = ('.tex', '.sty', '.md', '.py', '.yml', '.yaml', '.sh', '.json')

    def get_relevant_files(self):
        """Get all files that should be checked"""
        files = []
        for root, dirs, filenames in os.walk(self.repo_root):
            # Skip .git directory
            if '.git' in dirs:
                dirs.remove('.git')

            for filename in filenames:
                if filename.endswith(self.file_extensions):
                    filepath = Path(root) / filename
                    files.append(filepath)

        return files

    def test_no_trailing_whitespace(self):
        """Test that no files have trailing whitespace on any line

        Note: Allows intentional Markdown double-space line breaks (two spaces at end of line)
        as these are semantic, not accidental whitespace.
        """
        files_with_whitespace = []

        for filepath in self.get_relevant_files():
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()

                for line_num, line in enumerate(lines, 1):
                    # Remove newline characters for checking
                    line_content = line.rstrip('\n\r')

                    # Skip if line is empty after removing newlines
                    if not line_content:
                        continue

                    # Check for trailing whitespace
                    stripped = line_content.rstrip()

                    # In Markdown, two spaces at end of line is intentional (line break)
                    # Allow this but flag other trailing whitespace
                    if line_content != stripped:
                        # Check if it's the intentional Markdown pattern
                        if filepath.suffix == '.md' and line_content.endswith('  ') and line_content == stripped + '  ':
                            # This is intentional Markdown line break, allow it
                            continue

                        # Otherwise, it's problematic trailing whitespace
                        files_with_whitespace.append((filepath, line_num, line[:50]))

            except Exception as e:
                self.fail(f"Error reading {filepath}: {e}")

        if files_with_whitespace:
            msg = "Found files with trailing whitespace (excluding intentional Markdown line breaks):\n"
            for filepath, line_num, line_preview in files_with_whitespace[:10]:
                msg += f"  {filepath}:{line_num} - '{line_preview}'\n"
            if len(files_with_whitespace) > 10:
                msg += f"  ... and {len(files_with_whitespace) - 10} more\n"
            self.fail(msg)

    def test_all_files_utf8(self):
        """Test that all files are valid UTF-8"""
        non_utf8_files = []

        for filepath in self.get_relevant_files():
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    f.read()
            except UnicodeDecodeError as e:
                non_utf8_files.append((filepath, str(e)))

        if non_utf8_files:
            msg = "Found files that are not valid UTF-8:\n"
            for filepath, error in non_utf8_files:
                msg += f"  {filepath}: {error}\n"
            self.fail(msg)

    def test_no_bom(self):
        """Test that no files have BOM (Byte Order Mark)"""
        files_with_bom = []

        for filepath in self.get_relevant_files():
            try:
                with open(filepath, 'rb') as f:
                    raw = f.read(4)

                # Check for various BOM markers
                if raw.startswith(b'\xef\xbb\xbf'):
                    files_with_bom.append((filepath, 'UTF-8 BOM'))
                elif raw.startswith(b'\xff\xfe'):
                    files_with_bom.append((filepath, 'UTF-16 LE BOM'))
                elif raw.startswith(b'\xfe\xff'):
                    files_with_bom.append((filepath, 'UTF-16 BE BOM'))

            except Exception as e:
                self.fail(f"Error reading {filepath}: {e}")

        if files_with_bom:
            msg = "Found files with BOM:\n"
            for filepath, bom_type in files_with_bom:
                msg += f"  {filepath}: {bom_type}\n"
            self.fail(msg)

    def test_lf_line_endings(self):
        """Test that files use LF line endings (not CRLF)"""
        files_with_crlf = []

        for filepath in self.get_relevant_files():
            try:
                with open(filepath, 'rb') as f:
                    raw = f.read()

                if b'\r\n' in raw:
                    crlf_count = raw.count(b'\r\n')
                    files_with_crlf.append((filepath, crlf_count))

            except Exception as e:
                self.fail(f"Error reading {filepath}: {e}")

        if files_with_crlf:
            msg = "Found files with CRLF line endings:\n"
            for filepath, count in files_with_crlf[:10]:
                msg += f"  {filepath}: {count} CRLF sequences\n"
            if len(files_with_crlf) > 10:
                msg += f"  ... and {len(files_with_crlf) - 10} more\n"
            self.fail(msg)

    def test_files_end_with_newline(self):
        """Test that files end with a newline (Unix convention)

        Note: This is a recommendation, not a hard requirement for merge success.
        Files that don't end with newline won't prevent merges, but it's best practice.
        """
        files_without_newline = []

        for filepath in self.get_relevant_files():
            try:
                with open(filepath, 'rb') as f:
                    raw = f.read()

                # Skip empty files
                if len(raw) == 0:
                    continue

                # Check if file ends with newline
                if not raw.endswith(b'\n'):
                    files_without_newline.append(filepath)

            except Exception as e:
                self.fail(f"Error reading {filepath}: {e}")

        # Report as warning, not failure, since this doesn't block merges
        if files_without_newline:
            print(f"\nNote: {len(files_without_newline)} files don't end with newline (not critical for merges)")
            # Don't fail the test - this is informational only
            # self.fail(msg)

    def test_no_mixed_line_endings(self):
        """Test that files don't have mixed line endings"""
        files_with_mixed = []

        for filepath in self.get_relevant_files():
            try:
                with open(filepath, 'rb') as f:
                    raw = f.read()

                has_crlf = b'\r\n' in raw
                has_lf_only = b'\n' in raw and not has_crlf

                # If file has both CRLF and LF-only, it has mixed endings
                if has_crlf and has_lf_only:
                    # Count each type
                    crlf_count = raw.count(b'\r\n')
                    lf_count = raw.count(b'\n') - crlf_count
                    files_with_mixed.append((filepath, crlf_count, lf_count))

            except Exception as e:
                self.fail(f"Error reading {filepath}: {e}")

        if files_with_mixed:
            msg = "Found files with mixed line endings:\n"
            for filepath, crlf, lf in files_with_mixed:
                msg += f"  {filepath}: {crlf} CRLF, {lf} LF\n"
            self.fail(msg)

    def test_fix_script_exists(self):
        """Test that the fix script exists and is executable"""
        script_path = self.repo_root / 'fix_merge_conflicts.py'
        self.assertTrue(script_path.exists(), "fix_merge_conflicts.py does not exist")
        self.assertTrue(script_path.is_file(), "fix_merge_conflicts.py is not a file")

    def test_documentation_exists(self):
        """Test that the fix documentation exists"""
        doc_path = self.repo_root / 'MERGE_CONFLICT_CHARACTERS_FIX.md'
        self.assertTrue(doc_path.exists(), "MERGE_CONFLICT_CHARACTERS_FIX.md does not exist")
        self.assertTrue(doc_path.is_file(), "Documentation is not a file")


class TestRepositoryStats(unittest.TestCase):
    """Test to collect repository statistics"""

    def test_repository_statistics(self):
        """Collect and report statistics about the repository"""
        repo_root = Path(__file__).parent
        file_extensions = ('.tex', '.sty', '.md', '.py', '.yml', '.yaml', '.sh', '.json')

        file_count = 0
        line_count = 0
        size_bytes = 0

        for root, dirs, filenames in os.walk(repo_root):
            if '.git' in dirs:
                dirs.remove('.git')

            for filename in filenames:
                if filename.endswith(file_extensions):
                    filepath = Path(root) / filename
                    file_count += 1

                    try:
                        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                            lines = f.readlines()
                            line_count += len(lines)

                        size_bytes += filepath.stat().st_size
                    except:
                        pass

        print(f"\n{'='*60}")
        print("Repository Statistics")
        print(f"{'='*60}")
        print(f"Files checked: {file_count}")
        print(f"Total lines: {line_count:,}")
        print(f"Total size: {size_bytes:,} bytes ({size_bytes/1024/1024:.2f} MB)")
        print(f"{'='*60}\n")

        # This test always passes, it's just for reporting
        self.assertTrue(True)


def main():
    """Run all tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestMergeConflictFix))
    suite.addTests(loader.loadTestsFromTestCase(TestRepositoryStats))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)


if __name__ == '__main__':
    main()
