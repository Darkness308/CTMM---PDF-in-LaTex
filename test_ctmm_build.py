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

    def test_hyphen_separation(self):
        """Test converting hyphens to spaces and capitalizing."""
        self.assertEqual(ctmm_build.filename_to_title("hello-world"), "Hello World")
        self.assertEqual(ctmm_build.filename_to_title("my-test-file"), "My Test File")
        self.assertEqual(ctmm_build.filename_to_title("trigger-management"), "Trigger Management")

    def test_mixed_separators_comprehensive(self):
        """Test converting both underscores and hyphens to spaces."""
        self.assertEqual(ctmm_build.filename_to_title("hello_world-test"), "Hello World Test")
        self.assertEqual(ctmm_build.filename_to_title("my-test_file"), "My Test File")
        self.assertEqual(ctmm_build.filename_to_title("trigger_management-worksheet"), "Trigger Management Worksheet")

    def test_multiple_consecutive_separators(self):
        """Test multiple consecutive separators are normalized to single spaces."""
        self.assertEqual(ctmm_build.filename_to_title("hello__world"), "Hello World")
        self.assertEqual(ctmm_build.filename_to_title("test--file"), "Test File")
        self.assertEqual(ctmm_build.filename_to_title("my___test___file"), "My Test File")

    def test_leading_trailing_separators(self):
        """Test leading and trailing separators are handled properly."""
        # The function should handle these gracefully
        result1 = ctmm_build.filename_to_title("_hello_world_")
        result2 = ctmm_build.filename_to_title("-test-file-")
        # Results should not have leading/trailing spaces
        self.assertFalse(result1.startswith(' ') or result1.endswith(' '))
        self.assertFalse(result2.startswith(' ') or result2.endswith(' '))

    def test_realistic_ctmm_filenames(self):
        """Test realistic German therapy-related filenames from the CTMM system."""
        test_cases = [
            ("arbeitsblatt_depression", "Arbeitsblatt Depression"),
            ("trigger_management", "Trigger Management"),
            ("borderline_worksheet", "Borderline Worksheet"),
            ("ptsd-coping-strategies", "Ptsd Coping Strategies"),
            ("adhd_attention_exercises", "Adhd Attention Exercises"),
            ("bindungsmuster_analyse", "Bindungsmuster Analyse"),
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

    def test_check_missing_files_function_exists(self):
        """Test that check_missing_files function exists and is callable."""
        self.assertTrue(hasattr(ctmm_build, 'check_missing_files'))
        self.assertTrue(callable(ctmm_build.check_missing_files))

    def test_create_template_function_exists(self):
        """Test that create_template function exists and is callable."""
        self.assertTrue(hasattr(ctmm_build, 'create_template'))
        self.assertTrue(callable(ctmm_build.create_template))

    def test_filename_to_title_function_exists(self):
        """Test that filename_to_title function exists and is callable."""
        self.assertTrue(hasattr(ctmm_build, 'filename_to_title'))
        self.assertTrue(callable(ctmm_build.filename_to_title))

    def test_scan_references_basic_functionality(self):
        """Test basic functionality of scan_references."""
        # This should not crash and should return two lists
        style_files, module_files = ctmm_build.scan_references()
        self.assertIsInstance(style_files, list)
        self.assertIsInstance(module_files, list)

    def test_check_missing_files_basic_functionality(self):
        """Test basic functionality of check_missing_files."""
        # Test with empty list
        result = ctmm_build.check_missing_files([])
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)

        # Test with non-existent files
        result = ctmm_build.check_missing_files(['non_existent_file.txt'])
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)