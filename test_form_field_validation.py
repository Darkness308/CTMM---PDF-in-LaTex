#!/usr/bin/env python3
"""
Test suite for CTMM Form Field Validation

Tests the form field validation functionality implemented for issue #1118.
Ensures the validation correctly detects and fixes LaTeX syntax errors
related to form fields.

Author: CTMM-Team / Copilot
Issue: #1118 - Form field standardization fix
"""

import unittest
import tempfile
import os
from pathlib import Path
import sys

# Add current directory to path to import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from validate_form_fields import FormFieldValidator

class TestFormFieldValidator(unittest.TestCase):
    """Test cases for form field validation."""

    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.modules_dir = Path(self.temp_dir) / "modules"
        self.style_dir = Path(self.temp_dir) / "style"
        self.modules_dir.mkdir()
        self.style_dir.mkdir()

        # Create valid form-elements.sty
        self.create_valid_form_elements()

        self.validator = FormFieldValidator(self.temp_dir)

    def tearDown(self):
        """Clean up test environment."""
        import shutil
        shutil.rmtree(self.temp_dir)

    def create_valid_form_elements(self):
        """Create a valid form-elements.sty file."""
        content = r"""
\ProvidesPackage{style/form-elements}[2025/08/02 CTMM Form Elements v1.2.0]

% Checkbox with optional first parameter (backward compatible)
\newcommand{\ctmmCheckBox}[2][]{%
    \ifthenelse{\equal{\@ctmmInteractive}{true}}{%
        \CheckBox[%
            name=#1,%
            width=14pt,%
            height=14pt%
        ]{\raisebox{0.1ex}{\small\,#2}}%
    }{%
        \raisebox{-0.1ex}{\tikz[baseline=-0.1ex]{\draw[color=ctmmGreen, line width=1pt] (0,0) rectangle (0.35,0.35);}} \small\,#2%
    }%
}

% Text Field
\newcommand{\ctmmTextField}[3][4cm]{%
    \ifthenelse{\equal{\@ctmmInteractive}{true}}{%
        \TextField[%
            name=#3,%
            width=#1,%
            height=14pt%
        ]{}%
    }{%
        \underline{\hspace{#1}}%
    }%
}
"""
        with open(self.style_dir / "form-elements.sty", 'w') as f:
            f.write(content)

    def create_test_module(self, filename, content):
        """Create a test module file."""
        with open(self.modules_dir / filename, 'w') as f:
            f.write(content)

    def test_valid_form_elements_detection(self):
        """Test detection of valid form-elements.sty syntax."""
        result = self.validator.validate_form_elements_style()
        self.assertTrue(result)
        self.assertEqual(len(self.validator.issues), 0)

    def test_breaking_change_detection(self):
        """Test detection of breaking changes in checkbox syntax."""
        # Create form-elements.sty with breaking change
        breaking_content = r"""
\newcommand{\ctmmCheckBox}[2]{%
    \CheckBox[name=#1]{#2}%
}
"""
        with open(self.style_dir / "form-elements.sty", 'w') as f:
            f.write(breaking_content)

        result = self.validator.validate_form_elements_style()
        self.assertFalse(result)
        self.assertTrue(any("Breaking change detected" in issue for issue in self.validator.issues))

    def test_double_backslash_detection(self):
        """Test detection of double backslash before underscore."""
        problematic_content = r"""
\section{Test}
\ctmmTextField[6cm]{}{woche\\_mm}
\textbf{Another field:} \ctmmTextField[4cm]{}{field\\_name}
"""
        self.create_test_module("test_double_backslash.tex", problematic_content)

        result = self.validator.validate_module_file(self.modules_dir / "test_double_backslash.tex")
        self.assertFalse(result)

        # Check that issues were detected
        backslash_issues = [issue for issue in self.validator.issues if "double backslash" in issue.lower()]
        self.assertGreater(len(backslash_issues), 0)

    def test_incomplete_field_detection(self):
        """Test detection of incomplete form field commands."""
        problematic_content = r"""
\section{Test}
\ctmmTextField[4cm]{}{incomplete_field
\ctmmCheckBox[another_field]{Label without closing brace
"""
        self.create_test_module("test_incomplete.tex", problematic_content)

        result = self.validator.validate_module_file(self.modules_dir / "test_incomplete.tex")
        self.assertFalse(result)

        # Check that incomplete field issues were detected
        incomplete_issues = [issue for issue in self.validator.issues if "incomplete" in issue.lower()]
        self.assertGreater(len(incomplete_issues), 0)

    def test_invalid_field_names(self):
        """Test detection of invalid field names."""
        problematic_content = r"""
\section{Test}
\ctmmTextField[4cm]{}{field_mm}
\ctmmTextField[4cm]{}{field-with-hyphens}
\ctmmTextField[4cm]{}{123_starts_with_number}
"""
        self.create_test_module("test_invalid_names.tex", problematic_content)

        result = self.validator.validate_module_file(self.modules_dir / "test_invalid_names.tex")
        self.assertFalse(result)

        # Check that invalid field name issues were detected
        invalid_name_issues = [issue for issue in self.validator.issues if "invalid field name" in issue.lower()]
        self.assertGreater(len(invalid_name_issues), 0)

    def test_valid_form_fields(self):
        """Test that valid form fields pass validation."""
        valid_content = r"""
\section{Valid Form Fields}

\textbf{Name:} \ctmmTextField[6cm]{}{user_name}
\textbf{Email:} \ctmmTextField[8cm]{}{email_address}

\ctmmCheckBox[accept_terms]{I accept the terms and conditions}
\ctmmCheckBox[newsletter]{Subscribe to newsletter}

\textbf{Comments:}
\ctmmTextArea[12cm]{3}{user_comments}{}
"""
        self.create_test_module("test_valid.tex", valid_content)

        result = self.validator.validate_module_file(self.modules_dir / "test_valid.tex")
        self.assertTrue(result)

        # Should have no issues for this file
        file_issues = [issue for issue in self.validator.issues if "test_valid.tex" in issue]
        self.assertEqual(len(file_issues), 0)

    def test_field_name_validation_rules(self):
        """Test specific field name validation rules."""
        validator = self.validator

        # Valid field names
        self.assertTrue(validator.is_valid_field_name("user_name"))
        self.assertTrue(validator.is_valid_field_name("field123"))
        self.assertTrue(validator.is_valid_field_name("a"))
        self.assertTrue(validator.is_valid_field_name("long_field_name_with_underscores"))

        # Invalid field names
        self.assertFalse(validator.is_valid_field_name("field_mm"))  # Ends with _mm
        self.assertFalse(validator.is_valid_field_name("field-name"))  # Contains hyphen
        self.assertFalse(validator.is_valid_field_name("123field"))  # Starts with number
        self.assertFalse(validator.is_valid_field_name(""))  # Empty
        self.assertFalse(validator.is_valid_field_name("field@name"))  # Special character

    def test_automatic_fixes(self):
        """Test automatic fixing of common issues."""
        problematic_content = r"""
\section{Problematic Content}
\ctmmTextField[6cm]{}{field\\_mm}
\ctmmTextField[4cm]{}{another_mm
"""
        filename = "test_fixes.tex"
        self.create_test_module(filename, problematic_content)

        # Apply fixes
        fixed = self.validator.fix_file_issues(self.modules_dir / filename)
        self.assertTrue(fixed)

        # Check that backup was created
        backup_file = self.modules_dir / f"{filename}.backup"
        self.assertTrue(backup_file.exists())

        # Read fixed content
        with open(self.modules_dir / filename, 'r') as f:
            fixed_content = f.read()

        # Verify fixes were applied
        self.assertNotIn("\\_", fixed_content)  # Double backslash should be fixed
        self.assertIn("field_", fixed_content)  # Should have single underscore

    def test_comprehensive_validation(self):
        """Test comprehensive validation of all files."""
        # Create multiple files with various issues
        self.create_test_module("good_file.tex", r"""
\section{Good File}
\ctmmTextField[6cm]{}{valid_field}
\ctmmCheckBox[checkbox_field]{Valid checkbox}
""")

        self.create_test_module("bad_file.tex", r"""
\section{Bad File}
\ctmmTextField[6cm]{}{field\\_mm}
\ctmmCheckBox[incomplete_field]{Missing brace
""")

        # Run comprehensive validation
        result = self.validator.validate_all_files()
        self.assertFalse(result)  # Should fail due to bad_file.tex

        # Should have detected issues in bad_file.tex but not good_file.tex
        bad_file_issues = [issue for issue in self.validator.issues if "bad_file.tex" in issue]
        good_file_issues = [issue for issue in self.validator.issues if "good_file.tex" in issue]

        self.assertGreater(len(bad_file_issues), 0)
        self.assertEqual(len(good_file_issues), 0)

class TestFormFieldStandardization(unittest.TestCase):
    """Integration tests for form field standardization."""

    def test_pr378_issues_detection(self):
        """Test detection of specific issues from PR #378."""
        temp_dir = tempfile.mkdtemp()
        modules_dir = Path(temp_dir) / "modules"
        style_dir = Path(temp_dir) / "style"
        modules_dir.mkdir()
        style_dir.mkdir()

        try:
            # Create form-elements.sty
            form_elements_content = r"""
\newcommand{\ctmmCheckBox}[2][]{%
    \CheckBox[name=#1]{#2}%
}
"""
            with open(style_dir / "form-elements.sty", 'w') as f:
                f.write(form_elements_content)

            # Create module with PR #378 issues
            pr378_issues = r"""
% Issues from PR #378 comments
\begin{ctmmBlueBox}{Woche vom: \ctmmTextField[6cm]{}{woche\\_mm}}
\textbf{Name:} \ctmmTextField[4cm]{}{nk_name} \quad \textbf{Datum:} \ctmmTextField[4cm]{}{nk\_mm\\
\ctmmTextField[10cm]{}{daily\_mm\\[0.3cm]
\ctmmTextField[4cm]{}{therapist_psycho\_mm & PTBS, Borderline, ADHS \\
\ctmmYesNo{verbesserung} \quad \textbf{Wie zeigt sich das:} \ctmmTextField[6cm]{}{verbesserung\_mm
"""
            with open(modules_dir / "pr378_issues.tex", 'w') as f:
                f.write(pr378_issues)

            validator = FormFieldValidator(temp_dir)
            result = validator.validate_all_files()

            # Should detect multiple issues
            self.assertFalse(result)
            self.assertGreater(len(validator.issues), 5)

            # Should detect specific patterns
            issue_text = ' '.join(validator.issues)
            self.assertIn("double backslash", issue_text.lower())
            self.assertIn("incomplete", issue_text.lower())

        finally:
            import shutil
            shutil.rmtree(temp_dir)

    def test_backward_compatibility_preservation(self):
        """Test that backward compatibility is preserved."""
        temp_dir = tempfile.mkdtemp()
        style_dir = Path(temp_dir) / "style"
        style_dir.mkdir()

        try:
            # Create properly structured form-elements.sty
            content = r"""
\newcommand{\ctmmCheckBox}[2][]{%
    \ifthenelse{\equal{#1}{}}{%
        \checkbox{#2}%
    }{%
        \CheckBox[name=#1]{#2}%
    }%
}
"""
            with open(style_dir / "form-elements.sty", 'w') as f:
                f.write(content)

            validator = FormFieldValidator(temp_dir)
            result = validator.validate_form_elements_style()

            # Should pass validation (backward compatible)
            self.assertTrue(result)

        finally:
            import shutil
            shutil.rmtree(temp_dir)

def run_tests():
    """Run all form field validation tests."""
    print("🧪 Running CTMM Form Field Validation Tests")
    print("=" * 60)

    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestFormFieldValidator))
    suite.addTests(loader.loadTestsFromTestCase(TestFormFieldStandardization))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\n" + "=" * 60)
    if result.wasSuccessful():
        print("✅ ALL TESTS PASSED!")
        print(f"Ran {result.testsRun} tests successfully")
    else:
        print("❌ SOME TESTS FAILED!")
        print(f"Ran {result.testsRun} tests, {len(result.failures)} failures, {len(result.errors)} errors")

    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
