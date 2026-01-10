#!/usr/bin/env python3
"""
Unit tests for LaTeX validator functionality.
"""

import unittest
import tempfile
import os
from pathlib import Path
from latex_validator import LaTeXValidator, sanitize_pkg_name


class TestLaTeXValidator(unittest.TestCase):
    """Test cases for LaTeX validator."""

    def setUp(self):
        """Set up test fixtures."""
        self.validator = LaTeXValidator()
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir)

    def test_detect_textbackslash_escaping(self):
        """Test detection of excessive textbackslash escaping."""
        content = r"""
        Some text with \textbackslash{} sequences that should be \textbackslash{} detected.
        Normal \\ backslashes should be fine.
        """
        issues = self.validator.detect_issues(content)
        self.assertIn('textbackslash_escape', issues)
        self.assertEqual(len(issues['textbackslash_escape']), 2)

    def test_detect_hypertarget_overuse(self):
        """Test detection of over-complex hypertarget usage."""
        content = r"""
        \hypertarget{tool-23-trigger-management}{%
        \section{\texorpdfstring{📄 \textbf{TOOL 23: TRIGGER-MANAGEMENT}}{📄 TOOL 23: TRIGGER-MANAGEMENT}\label{tool-23-trigger-management}}
        """
        issues = self.validator.detect_issues(content)
        self.assertIn('hypertarget_overuse', issues)

    def test_detect_texorpdfstring_overuse(self):
        """Test detection of excessive texorpdfstring usage."""
        content = r"""
        \subsection{\texorpdfstring{🎯 \textbf{\ul{ZIEL}}}{🎯 ZIEL}}
        """
        issues = self.validator.detect_issues(content)
        self.assertIn('texorpdfstring_overuse', issues)

    def test_clean_textbackslash_escaping(self):
        """Test cleaning of textbackslash escaping."""
        content = r"Text with \textbackslash{} should become normal \\ backslash."
        cleaned = self.validator.clean_excessive_escaping(content)
        self.assertNotIn(r'\textbackslash{}', cleaned)
        self.assertIn(r'\\', cleaned)

    def test_clean_complex_section_headers(self):
        """Test simplification of over-complex section headers."""
        content = r"""
        \hypertarget{tool-23-trigger-management}{%
        \section{\texorpdfstring{📄 \textbf{TOOL 23: TRIGGER-MANAGEMENT}}{📄 TOOL 23: TRIGGER-MANAGEMENT}\label{tool-23-trigger-management}}
        """
        cleaned = self.validator.clean_excessive_escaping(content)
        self.assertIn(r'\section{TOOL 23: TRIGGER-MANAGEMENT}', cleaned)
        self.assertIn(r'\label{sec:tool-23-trigger-management}', cleaned)
        self.assertNotIn(r'\hypertarget{', cleaned)

    def test_validate_clean_file(self):
        """Test validation of a properly formatted LaTeX file."""
        clean_content = r"""
        \section{Test Section}
        \label{sec:test}

        This is a properly formatted LaTeX file with no escaping issues.

        \subsection{Test Subsection}
        Some content here.
        """

        test_file = Path(self.temp_dir) / "clean_test.tex"
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(clean_content)

        is_valid, issues, _ = self.validator.validate_file(test_file)
        self.assertTrue(is_valid)
        self.assertEqual(len(issues), 0)

    def test_validate_problematic_file(self):
        """Test validation of a file with escaping issues."""
        problematic_content = r"""
        \hypertarget{tool-23-trigger-management}{%
        \section{\texorpdfstring{📄 \textbf{TOOL 23: TRIGGER-MANAGEMENT}}{📄 TOOL 23: TRIGGER-MANAGEMENT}\label{tool-23-trigger-management}}

        Text with \textbackslash{} escaping issues.
        """

        test_file = Path(self.temp_dir) / "problematic_test.tex"
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(problematic_content)

        is_valid, issues, _ = self.validator.validate_file(test_file)
        self.assertFalse(is_valid)
        self.assertGreater(len(issues), 0)

    def test_fix_escaping_issues(self):
        """Test automatic fixing of escaping issues."""
        problematic_content = r"""
        Text with multiple \textbackslash{} sequences that need \textbackslash{} fixing.
        """

        test_file = Path(self.temp_dir) / "fix_test.tex"
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(problematic_content)

        # First validation should find issues
        is_valid, issues, cleaned_content = self.validator.validate_file(test_file)
        self.assertFalse(is_valid)

        # Write cleaned content back
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)

        # Second validation should be cleaner (may still have some complex patterns)
        is_valid_after, issues_after, _ = self.validator.validate_file(test_file)
        self.assertLessEqual(len(issues_after), len(issues))

    def test_preserve_valid_latex(self):
        """Test that valid LaTeX commands are preserved."""
        valid_content = r"""
        \section{Valid Section}
        \textbf{Bold text} and \emph{emphasized text}.
        \begin{itemize}
        \item First item
        \item Second item with \& ampersand
        \end{itemize}
        """

        cleaned = self.validator.clean_excessive_escaping(valid_content)
        self.assertIn(r'\textbf{Bold text}', cleaned)
        self.assertIn(r'\emph{emphasized text}', cleaned)
        self.assertIn(r'\begin{itemize}', cleaned)

    def test_double_backslash_ampersand_fix(self):
        """Test fixing of double backslash before ampersand."""
        content = r"Text with \\& should become text with \& properly."
        cleaned = self.validator.clean_excessive_escaping(content)
        self.assertIn(r' \& ', cleaned)
        self.assertNotIn(r'\\&', cleaned)


class TestLaTeXValidatorIntegration(unittest.TestCase):
    """Integration tests for LaTeX validator with build system."""

    def test_validator_import(self):
        """Test that validator can be imported by build system."""
        try:
            from latex_validator import LaTeXValidator
            validator = LaTeXValidator()
            self.assertIsInstance(validator, LaTeXValidator)
        except ImportError:
            self.fail("LaTeX validator should be importable")

    def test_problematic_patterns_defined(self):
        """Test that all problematic patterns are defined."""
        validator = LaTeXValidator()
        expected_patterns = [
            'textbackslash_escape',
            'hypertarget_overuse',
            'texorpdfstring_overuse',
            'excessive_backslashes',
            'auto_generated_labels'
        ]

        for pattern in expected_patterns:
            self.assertIn(pattern, validator.problematic_patterns)


class TestSanitizePkgName(unittest.TestCase):
    """Test cases for the sanitize_pkg_name function."""

    def test_problem_statement_cases(self):
        """Test the specific cases mentioned in the problem statement."""
        test_cases = [
            ('123-package', 'pkg123Package'),
            ('1-package', 'pkg1Package'),
            ('2_test', 'pkg2Test'),
            ('999-name', 'pkg999Name'),
        ]

        for input_name, expected in test_cases:
            with self.subTest(input_name=input_name):
                result = sanitize_pkg_name(input_name)
                self.assertEqual(result, expected,
                               f"Expected '{expected}' but got '{result}' for input '{input_name}'")

    def test_basic_functionality(self):
        """Test basic package name sanitization."""
        test_cases = [
            ('test', 'pkgTest'),
            ('my-package', 'pkgMyPackage'),
            ('my_package', 'pkgMyPackage'),
            ('test-name', 'pkgTestName'),
            ('test_name', 'pkgTestName'),
        ]

        for input_name, expected in test_cases:
            with self.subTest(input_name=input_name):
                result = sanitize_pkg_name(input_name)
                self.assertEqual(result, expected)

    def test_mixed_separators(self):
        """Test names with mixed hyphens and underscores."""
        test_cases = [
            ('test-name_package', 'pkgTestNamePackage'),
            ('my_test-package', 'pkgMyTestPackage'),
            ('complex-test_name-package', 'pkgComplexTestNamePackage'),
        ]

        for input_name, expected in test_cases:
            with self.subTest(input_name=input_name):
                result = sanitize_pkg_name(input_name)
                self.assertEqual(result, expected)

    def test_numbers_in_middle(self):
        """Test names with numbers in the middle."""
        test_cases = [
            ('test-2-package', 'pkgTest2Package'),
            ('name_123_test', 'pkgName123Test'),
            ('v1-test-v2', 'pkgV1TestV2'),
            ('package-42-name', 'pkgPackage42Name'),
        ]

        for input_name, expected in test_cases:
            with self.subTest(input_name=input_name):
                result = sanitize_pkg_name(input_name)
                self.assertEqual(result, expected)

    def test_numbers_only(self):
        """Test names that are only numbers."""
        test_cases = [
            ('123', 'pkg123'),
            ('42', 'pkg42'),
            ('999', 'pkg999'),
        ]

        for input_name, expected in test_cases:
            with self.subTest(input_name=input_name):
                result = sanitize_pkg_name(input_name)
                self.assertEqual(result, expected)

    def test_consecutive_separators(self):
        """Test names with consecutive separators."""
        test_cases = [
            ('test--package', 'pkgTestPackage'),
            ('test__package', 'pkgTestPackage'),
            ('test-_package', 'pkgTestPackage'),
            ('test_-package', 'pkgTestPackage'),
        ]

        for input_name, expected in test_cases:
            with self.subTest(input_name=input_name):
                result = sanitize_pkg_name(input_name)
                self.assertEqual(result, expected)

    def test_edge_cases(self):
        """Test edge cases."""
        test_cases = [
            ('', 'pkg'),  # Empty string
            ('-', 'pkg'),  # Only separator
            ('_', 'pkg'),  # Only separator
            ('--', 'pkg'),  # Multiple separators
            ('123-', 'pkg123'),  # Trailing separator
            ('-123', 'pkg123'),  # Leading separator
        ]

        for input_name, expected in test_cases:
            with self.subTest(input_name=input_name):
                result = sanitize_pkg_name(input_name)
                self.assertEqual(result, expected)

    def test_case_preservation(self):
        """Test that the function properly handles case."""
        test_cases = [
            ('Test-Package', 'pkgTestPackage'),
            ('TEST-PACKAGE', 'pkgTestPackage'),
            ('test-PACKAGE', 'pkgTestPackage'),
            ('MyGreat_Package', 'pkgMygreatPackage'),
        ]

        for input_name, expected in test_cases:
            with self.subTest(input_name=input_name):
                result = sanitize_pkg_name(input_name)
                self.assertEqual(result, expected)

    def test_complex_realistic_names(self):
        """Test complex, realistic package names."""
        test_cases = [
            ('latex-utils-v2', 'pkgLatexUtilsV2'),
            ('math-symbols_1-0', 'pkgMathSymbols10'),
            ('document-style_2024', 'pkgDocumentStyle2024'),
            ('ctmm-design-1_2_3', 'pkgCtmmDesign123'),
        ]

        for input_name, expected in test_cases:
            with self.subTest(input_name=input_name):
                result = sanitize_pkg_name(input_name)
                self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()