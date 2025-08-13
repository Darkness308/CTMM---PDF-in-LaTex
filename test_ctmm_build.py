#!/usr/bin/env python3
"""
Unit tests for CTMM Build System functions.
Tests the ctmm_build.py module functions for correctness.
"""

import unittest
import sys
from pathlib import Path

# Add current directory to path for importing ctmm_build
sys.path.insert(0, str(Path(__file__).parent))
import ctmm_build


class TestFilenameToTitle(unittest.TestCase):
    """Test cases for the filename_to_title function."""

    def test_underscores_to_spaces(self):
        """Test that underscores are converted to spaces."""
        result = ctmm_build.filename_to_title("test_module_name")
        self.assertEqual(result, "Test Module Name")

    def test_hyphens_to_spaces(self):
        """Test that hyphens are converted to spaces."""
        result = ctmm_build.filename_to_title("test-module-name")
        self.assertEqual(result, "Test Module Name")

    def test_mixed_separators(self):
        """Test handling of mixed underscores and hyphens."""
        result = ctmm_build.filename_to_title("test_module-name")
        self.assertEqual(result, "Test Module Name")

    def test_single_word(self):
        """Test single word filename."""
        result = ctmm_build.filename_to_title("module")
        self.assertEqual(result, "Module")

    def test_already_capitalized(self):
        """Test filename that's already properly formatted."""
        result = ctmm_build.filename_to_title("Test_Module")
        self.assertEqual(result, "Test Module")

    def test_lowercase_input(self):
        """Test all lowercase input."""
        result = ctmm_build.filename_to_title("depression_worksheet")
        self.assertEqual(result, "Depression Worksheet")

    def test_empty_string(self):
        """Test empty string input."""
        result = ctmm_build.filename_to_title("")
        self.assertEqual(result, "")

    def test_numbers_in_filename(self):
        """Test filename with numbers."""
        result = ctmm_build.filename_to_title("module_1_test")
        self.assertEqual(result, "Module 1 Test")

    def test_special_characters(self):
        """Test filename with multiple consecutive separators."""
        result = ctmm_build.filename_to_title("test__double--underscore")
        # Multiple consecutive separators are normalized to single spaces
        self.assertEqual(result, "Test Double Underscore")

    def test_german_therapeutic_names(self):
        """Test typical German therapeutic module names."""
        test_cases = [
            ("arbeitsblatt_trigger", "Arbeitsblatt Trigger"),
            ("depression-management", "Depression Management"),
            ("bindung_muster", "Bindung Muster"),
            ("kommunikation_skills", "Kommunikation Skills"),
        ]
        
        for input_name, expected in test_cases:
            with self.subTest(input_name=input_name):
                result = ctmm_build.filename_to_title(input_name)
                self.assertEqual(result, expected)

    def test_mixed_case_input(self):
        """Test mixed case input is normalized properly."""
        result = ctmm_build.filename_to_title("hELLo_WoRLd")
        self.assertEqual(result, "Hello World")

    def test_multiple_consecutive_separators(self):
        """Test multiple consecutive separators are normalized to single spaces."""
        result = ctmm_build.filename_to_title("hello__world")
        self.assertEqual(result, "Hello World")

    def test_leading_trailing_separators(self):
        """Test leading and trailing separators are normalized (trimmed)."""
        result = ctmm_build.filename_to_title("_hello_world_")
        self.assertEqual(result, "Hello World")

    def test_realistic_filenames(self):
        """Test realistic German therapy-related filenames from the CTMM system."""
        test_cases = [
            ("arbeitsblatt_depression", "Arbeitsblatt Depression"),
            ("trigger_management", "Trigger Management"),
            ("borderline_worksheet", "Borderline Worksheet"),
            ("ptsd-coping-strategies", "Ptsd Coping Strategies"),
            ("adhd_attention_exercises", "Adhd Attention Exercises"),
        ]
        
        for input_name, expected in test_cases:
            with self.subTest(input_name=input_name):
                result = ctmm_build.filename_to_title(input_name)
                self.assertEqual(result, expected)


class TestCTMMBuildSystemIntegration(unittest.TestCase):
    """Integration tests for CTMM Build System functions."""

    def test_scan_references_function_exists(self):
        """Test that scan_references function exists and is callable."""
        self.assertTrue(hasattr(ctmm_build, 'scan_references'))
        self.assertTrue(callable(ctmm_build.scan_references))

    def test_scan_references_return_type(self):
        """Test that scan_references returns a dictionary with correct keys."""
        result = ctmm_build.scan_references()
        self.assertIsInstance(result, dict)
        self.assertIn('style_files', result)
        self.assertIn('module_files', result)
        self.assertIsInstance(result['style_files'], list)
        self.assertIsInstance(result['module_files'], list)

    def test_check_missing_files_function_exists(self):
        """Test that check_missing_files function exists and is callable."""
        self.assertTrue(hasattr(ctmm_build, 'check_missing_files'))
        self.assertTrue(callable(ctmm_build.check_missing_files))

    def test_check_missing_files_return_type(self):
        """Test that check_missing_files returns a dictionary with correct keys."""
        # Test with a mix of existing and non-existing files
        test_files = ["test_ctmm_build.py", "nonexistent_file.txt", "ctmm_build.py"]
        result = ctmm_build.check_missing_files(test_files)
        self.assertIsInstance(result, dict)
        self.assertIn('missing', result)
        self.assertIn('existing', result)
        self.assertIsInstance(result['missing'], list)
        self.assertIsInstance(result['existing'], list)
        # Verify the actual categorization
        self.assertIn("nonexistent_file.txt", result['missing'])
        self.assertIn("test_ctmm_build.py", result['existing'])
        self.assertIn("ctmm_build.py", result['existing'])

    def test_validate_latex_structure_function_exists(self):
        """Test that validate_latex_structure function exists and is callable."""
        self.assertTrue(hasattr(ctmm_build, 'validate_latex_structure'))
        self.assertTrue(callable(ctmm_build.validate_latex_structure))

    def test_validate_latex_structure_return_type(self):
        """Test that validate_latex_structure returns a dictionary with correct keys."""
        result = ctmm_build.validate_latex_structure()
        self.assertIsInstance(result, dict)
        self.assertIn('valid', result)
        self.assertIn('errors', result)
        self.assertIn('warnings', result)
        self.assertIsInstance(result['valid'], bool)
        self.assertIsInstance(result['errors'], list)
        self.assertIsInstance(result['warnings'], list)

    def test_create_template_function_exists(self):
        """Test that create_template function exists and is callable."""
        self.assertTrue(hasattr(ctmm_build, 'create_template'))
        self.assertTrue(callable(ctmm_build.create_template))

    def test_test_basic_build_function_exists(self):
        """Test that test_basic_build function exists and is callable."""
        self.assertTrue(hasattr(ctmm_build, 'test_basic_build'))
        self.assertTrue(callable(ctmm_build.test_basic_build))

    def test_test_full_build_function_exists(self):
        """Test that test_full_build function exists and is callable."""
        self.assertTrue(hasattr(ctmm_build, 'test_full_build'))
        self.assertTrue(callable(ctmm_build.test_full_build))

    def test_problematic_functions_removed(self):
        """Test that the problematic functions identified in PR #393 have been removed."""
        # These functions were flagged as unnecessary in the PR review
        self.assertFalse(hasattr(ctmm_build, 'test_basic_framework'))
        self.assertFalse(hasattr(ctmm_build, 'generate_build_report'))

    def test_return_type(self):
        """Test that the filename_to_title function returns a string."""
        result = ctmm_build.filename_to_title("test_file")
        self.assertIsInstance(result, str)


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)