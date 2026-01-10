#!/usr/bin/env python3
"""
Unit tests for detect_disruptive_characters.py

Tests the character validation functionality to ensure it correctly
detects and reports various character encoding issues.
"""

import unittest
import tempfile
import os
from pathlib import Path
from detect_disruptive_characters import CharacterValidator


class TestCharacterValidator(unittest.TestCase):
    """Test cases for CharacterValidator class."""

    def setUp(self):
        """Set up test fixtures."""
        self.validator = CharacterValidator(verbose=False)
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test fixtures."""
        # Clean up temp files
        for file in Path(self.temp_dir).rglob('*'):
            if file.is_file():
                file.unlink()
        Path(self.temp_dir).rmdir()

    def create_temp_file(self, filename: str, content: bytes) -> Path:
        """Create a temporary file with specified content."""
        filepath = Path(self.temp_dir) / filename
        with open(filepath, 'wb') as f:
            f.write(content)
        return filepath

    def test_clean_utf8_file(self):
        """Test that a clean UTF-8 file passes validation."""
        content = b"\\documentclass{article}\n\\begin{document}\nHello World\n\\end{document}"
        filepath = self.create_temp_file('test.tex', content)

        result = self.validator.scan_file(filepath)

        self.assertEqual(result['info']['encoding'], 'ascii')
        self.assertEqual(len(result['issues']), 0)
        self.assertEqual(len(result['warnings']), 0)

    def test_german_umlauts_utf8(self):
        """Test that German umlauts in UTF-8 are properly handled."""
        content = "\\documentclass{article}\n\\begin{document}\näöü ÄÖÜ ß\n\\end{document}".encode('utf-8')
        filepath = self.create_temp_file('test.tex', content)

        result = self.validator.scan_file(filepath)

        # Should be detected as UTF-8
        self.assertIn(result['info']['encoding'], ['utf-8', 'UTF-8-SIG'])
        # No critical issues, only potential warnings about special chars
        self.assertEqual(len(result['issues']), 0)

    def test_bom_detection(self):
        """Test that UTF-8 BOM is detected."""
        content = b'\xef\xbb\xbf\\documentclass{article}\n\\begin{document}\nTest\n\\end{document}'
        filepath = self.create_temp_file('test.tex', content)

        result = self.validator.scan_file(filepath)

        # Should detect BOM
        has_bom_issue = any(issue['type'] == 'bom_detected' for issue in result['issues'])
        self.assertTrue(has_bom_issue, "BOM should be detected as an issue")

    def test_crlf_line_endings(self):
        """Test that Windows (CRLF) line endings are detected."""
        content = b'\\documentclass{article}\r\n\\begin{document}\r\nTest\r\n\\end{document}\r\n'
        filepath = self.create_temp_file('test.tex', content)

        result = self.validator.scan_file(filepath)

        # Should detect CRLF
        has_crlf_warning = any(
            warning['type'] in ['windows_line_endings', 'mixed_line_endings']
            for warning in result['warnings']
        )
        self.assertTrue(has_crlf_warning, "CRLF line endings should be detected")

    def test_control_characters(self):
        """Test that control characters are detected."""
        # Create content with a control character (e.g., ASCII 0x01)
        content = b'\\documentclass{article}\n\\begin{document}\nTest\x01Content\n\\end{document}'
        filepath = self.create_temp_file('test.tex', content)

        result = self.validator.scan_file(filepath)

        # Should detect control character
        has_control_char = any(
            issue['type'] == 'control_character'
            for issue in result['issues']
        )
        self.assertTrue(has_control_char, "Control character should be detected")

    def test_mixed_line_endings(self):
        """Test that mixed line endings (CRLF and LF) are detected."""
        content = b'\\documentclass{article}\r\n\\begin{document}\nTest\r\n\\end{document}\n'
        filepath = self.create_temp_file('test.tex', content)

        result = self.validator.scan_file(filepath)

        # Should detect mixed line endings
        has_mixed_warning = any(
            warning['type'] == 'mixed_line_endings'
            for warning in result['warnings']
        )
        self.assertTrue(has_mixed_warning, "Mixed line endings should be detected")

    def test_invalid_utf8_sequence(self):
        """Test that invalid UTF-8 sequences are detected."""
        # Create content with invalid UTF-8 sequence
        content = b'\\documentclass{article}\n\\begin{document}\nTest\xff\xfe\n\\end{document}'
        filepath = self.create_temp_file('test.tex', content)

        result = self.validator.scan_file(filepath)

        # Should detect invalid UTF-8 or report different encoding
        # Either it detects as not UTF-8 or reports invalid sequence
        self.assertTrue(
            result['info']['encoding'] not in ['utf-8', 'UTF-8-SIG', 'ascii'] or
            any(issue['type'] == 'invalid_utf8' for issue in result['issues'])
        )

    def test_scan_directory(self):
        """Test scanning a directory with multiple files."""
        # Create multiple test files
        self.create_temp_file('test1.tex', b'\\documentclass{article}\n')
        self.create_temp_file('test2.tex', b'\\begin{document}\n')
        self.create_temp_file('test3.txt', b'Not a LaTeX file\n')  # Should not be scanned

        results = self.validator.scan_directory(Path(self.temp_dir), extensions=['.tex'])

        # Should scan only .tex files
        self.assertEqual(len(results), 2)
        self.assertEqual(self.validator.files_scanned, 2)

    def test_line_ending_counts(self):
        """Test that line ending counts are accurate."""
        content = b'Line1\r\nLine2\nLine3\r\nLine4\n'
        filepath = self.create_temp_file('test.tex', content)

        result = self.validator.scan_file(filepath)
        line_endings = result['info']['line_endings']

        # 2 CRLF, 2 LF-only
        self.assertEqual(line_endings['crlf'], 2)
        self.assertEqual(line_endings['lf'], 2)
        self.assertTrue(line_endings['mixed'])

    def test_special_character_detection(self):
        """Test detection of LaTeX special characters that might need escaping."""
        content = "\\documentclass{article}\n\\begin{document}\n§ © ® ™\n\\end{document}".encode('utf-8')
        filepath = self.create_temp_file('test.tex', content)

        result = self.validator.scan_file(filepath)

        # Should find unescaped special characters
        special_char_warnings = [
            w for w in result['warnings']
            if w['type'] == 'unescaped_special_char'
        ]
        self.assertGreater(len(special_char_warnings), 0)

    def test_encoding_confidence(self):
        """Test that encoding detection provides confidence scores."""
        content = "\\documentclass{article}\n\\begin{document}\nTest\n\\end{document}".encode('utf-8')
        filepath = self.create_temp_file('test.tex', content)

        result = self.validator.scan_file(filepath)

        # Should have confidence score
        self.assertIn('confidence', result['info'])
        self.assertIsInstance(result['info']['confidence'], float)
        self.assertGreaterEqual(result['info']['confidence'], 0.0)
        self.assertLessEqual(result['info']['confidence'], 1.0)


class TestCharacterValidatorIntegration(unittest.TestCase):
    """Integration tests for the character validator."""

    def test_real_repository_scan(self):
        """Test scanning the actual repository LaTeX files."""
        # This test runs on the real repository files
        validator = CharacterValidator(verbose=False)

        # Scan the modules directory
        repo_root = Path(__file__).parent
        modules_dir = repo_root / 'modules'

        if not modules_dir.exists():
            self.skipTest("modules directory not found")

        results = validator.scan_directory(modules_dir, extensions=['.tex'])

        # Should scan multiple files
        self.assertGreater(len(results), 0)
        self.assertGreater(validator.files_scanned, 0)

        # Check that no critical issues exist (only warnings allowed)
        for result in results:
            critical_issues = [
                issue for issue in result.get('issues', [])
                if issue['type'] not in ['bom_detected']  # BOM might be acceptable
            ]
            self.assertEqual(len(critical_issues), 0,
                           f"Critical issues found in {result['file']}: {critical_issues}")


if __name__ == '__main__':
    unittest.main()
