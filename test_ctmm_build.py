#!/usr/bin/env python3
"""
Unit tests for CTMM Build System functions.
Tests the ctmm_build.py module functions for correctness.
copilot/fix-407

Unit tests for CTMM Build System functions
Tests the filename_to_title() function with various input formats.

main
"""

import unittest
import sys
from pathlib import Path
copilot/fix-407


main
# Add current directory to path for importing ctmm_build
sys.path.insert(0, str(Path(__file__).parent))
import ctmm_build

from ctmm_build import filename_to_title


main

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
        """Test filename that is already properly formatted."""
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

    def test_very_long_filename(self):
        """Test very long filename to ensure performance and correctness."""
        long_filename = "very_long_module_name_with_many_words_that_should_still_work_correctly"
        expected = "Very Long Module Name With Many Words That Should Still Work Correctly"
        result = ctmm_build.filename_to_title(long_filename)
        self.assertEqual(result, expected)

    def test_german_umlauts_preserved(self):
        """Test that German umlauts and special characters are preserved."""
        test_cases = [
            ("übung_für_patienten", "Übung Für Patienten"),
            ("ängste_bewältigen", "Ängste Bewältigen"),
            ("selbst-fürsorge", "Selbst Fürsorge"),
        ]
        
        for input_name, expected in test_cases:
            with self.subTest(input_name=input_name):
                result = ctmm_build.filename_to_title(input_name)
                self.assertEqual(result, expected)

    def test_numeric_prefixes(self):
        """Test filenames with numeric prefixes (common in therapy modules)."""
        test_cases = [
            ("01_einführung", "01 Einführung"),
            ("2_advanced_techniques", "2 Advanced Techniques"),
            ("session_10_review", "Session 10 Review"),
        ]
        
        for input_name, expected in test_cases:
            with self.subTest(input_name=input_name):
                result = ctmm_build.filename_to_title(input_name)
                self.assertEqual(result, expected)

    def test_whitespace_edge_cases(self):
        """Test various whitespace scenarios."""
        test_cases = [
            ("  hello_world  ", "Hello World"),  # Leading/trailing spaces
            ("hello___world", "Hello World"),    # Multiple underscores
            ("hello---world", "Hello World"),    # Multiple hyphens
            ("hello_-_world", "Hello World"),    # Mixed separators
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

    def test_scan_references_returns_dict(self):
        """Test that scan_references function returns a dictionary with correct keys."""
        result = ctmm_build.scan_references("main.tex")
        self.assertIsInstance(result, dict)
        self.assertIn("style_files", result)
        self.assertIn("module_files", result)
        self.assertIsInstance(result["style_files"], list)
        self.assertIsInstance(result["module_files"], list)

    def test_structured_data_returns(self):
        """Test that build system functions return properly structured data."""
        # Test scan_references returns structured data
        references = ctmm_build.scan_references("main.tex")
        self.assertIsInstance(references, dict)
        
        # Verify required keys exist
        required_keys = ["style_files", "module_files"]
        for key in required_keys:
            self.assertIn(key, references, f"Missing required key: {key}")
            self.assertIsInstance(references[key], list, f"Key {key} should be a list")
        
        # Test check_missing_files returns list
        all_files = references["style_files"] + references["module_files"]
        missing_files = ctmm_build.check_missing_files(all_files)
        self.assertIsInstance(missing_files, list)

    def test_error_handling_robustness(self):
        """Test error handling in build system functions."""
        # Test scan_references with non-existent file
        result = ctmm_build.scan_references("non_existent_file.tex")
        self.assertIsInstance(result, dict)
        self.assertEqual(result["style_files"], [])
        self.assertEqual(result["module_files"], [])
        
        # Test check_missing_files with empty list
        result = ctmm_build.check_missing_files([])
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)

    def test_build_system_numbered_steps(self):
        """Test that the build system implements numbered steps as described in PR."""
        # This test verifies the main function structure without actually running it
        import inspect
        
        # Get the source code of the main function
        source = inspect.getsource(ctmm_build.main)
        
        # Check that numbered steps are implemented
        self.assertIn("step = 1", source, "Build system should use numbered steps")
        self.assertIn("step += 1", source, "Build system should increment step numbers")
        self.assertIn("print(f\"\\n{step}.", source, "Build system should print numbered steps")


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)