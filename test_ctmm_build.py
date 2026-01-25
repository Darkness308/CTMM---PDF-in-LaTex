#!/usr/bin/env python3
"""
Unit tests for CTMM Build System functions
Tests the filename_to_title() function with various input formats.
"""

import unittest
import sys
from pathlib import Path

# Add the current directory to the path to import ctmm_build
sys.path.insert(0, str(Path(__file__).parent))

from ctmm_build import filename_to_title


class TestFilenameToTitle(unittest.TestCase):
    """Test cases for the filename_to_title function."""

    def test_underscore_separation(self):
        """Test converting underscores to spaces and capitalizing."""
        self.assertEqual(filename_to_title("hello_world"), "Hello World")
        self.assertEqual(filename_to_title("my_test_file"), "My Test File")
        self.assertEqual(filename_to_title("arbeitsblatt_depression"), "Arbeitsblatt Depression")

    def test_hyphen_separation(self):
        """Test converting hyphens to spaces and capitalizing."""
        self.assertEqual(filename_to_title("hello-world"), "Hello World")
        self.assertEqual(filename_to_title("my-test-file"), "My Test File")
        self.assertEqual(filename_to_title("trigger-management"), "Trigger Management")

    def test_mixed_separators(self):
        """Test converting both underscores and hyphens to spaces."""
        self.assertEqual(filename_to_title("hello_world-test"), "Hello World Test")
        self.assertEqual(filename_to_title("my-test_file"), "My Test File")
        self.assertEqual(filename_to_title("trigger_management-worksheet"), "Trigger Management Worksheet")

    def test_single_word(self):
        """Test single words are properly capitalized."""
        self.assertEqual(filename_to_title("hello"), "Hello")
        self.assertEqual(filename_to_title("test"), "Test")
        self.assertEqual(filename_to_title("depression"), "Depression")

    def test_already_capitalized(self):
        """Test that already capitalized words remain properly formatted."""
        self.assertEqual(filename_to_title("Hello_World"), "Hello World")
        self.assertEqual(filename_to_title("My-Test"), "My Test")
        self.assertEqual(filename_to_title("UPPER_CASE"), "Upper Case")

    def test_mixed_case_input(self):
        """Test mixed case input is normalized properly."""
        self.assertEqual(filename_to_title("hELLo_WoRLd"), "Hello World")
        self.assertEqual(filename_to_title("mY-tEsT"), "My Test")
        self.assertEqual(filename_to_title("TrIgGeR_mAnAgEmEnT"), "Trigger Management")

    def test_empty_string(self):
        """Test empty string returns empty string."""
        self.assertEqual(filename_to_title(""), "")

    def test_multiple_consecutive_separators(self):
        """Test multiple consecutive separators are normalized to single spaces."""
        self.assertEqual(filename_to_title("hello__world"), "Hello World")
        self.assertEqual(filename_to_title("test--file"), "Test File")
        self.assertEqual(filename_to_title("my___test___file"), "My Test File")

    def test_leading_trailing_separators(self):
        """Test leading and trailing separators are normalized (trimmed)."""
        self.assertEqual(filename_to_title("_hello_world_"), "Hello World")
        self.assertEqual(filename_to_title("-test-file-"), "Test File")
        self.assertEqual(filename_to_title("_test-file_"), "Test File")

    def test_numbers_in_filename(self):
        """Test filenames containing numbers."""
        self.assertEqual(filename_to_title("test_file_1"), "Test File 1")
        self.assertEqual(filename_to_title("module-02-depression"), "Module 02 Depression")
        self.assertEqual(filename_to_title("arbeitsblatt_001_trigger"), "Arbeitsblatt 001 Trigger")

    def test_special_characters(self):
        """Test filenames with other characters (not underscores or hyphens)."""
        # Only underscores and hyphens should be replaced, other chars preserved
        # Only the first character of each word (split by space) gets capitalized
        self.assertEqual(filename_to_title("test.file"), "Test.file")
        self.assertEqual(filename_to_title("my_test@file"), "My Test@file")
        self.assertEqual(filename_to_title("hello_world(1)"), "Hello World(1)")

    def test_german_therapy_filenames(self):
        """Test realistic German therapy-related filenames from the CTMM system."""
        self.assertEqual(filename_to_title("arbeitsblatt_depression"), "Arbeitsblatt Depression")
        self.assertEqual(filename_to_title("trigger_management"), "Trigger Management")
        self.assertEqual(filename_to_title("borderline_worksheet"), "Borderline Worksheet")
        self.assertEqual(filename_to_title("ptsd-coping-strategies"), "Ptsd Coping Strategies")
        self.assertEqual(filename_to_title("adhd_attention_exercises"), "Adhd Attention Exercises")


class TestIntegration(unittest.TestCase):
    """Integration tests to ensure the function works in context."""

    def test_function_exists_and_callable(self):
        """Test that the filename_to_title function exists and is callable."""
        self.assertTrue(callable(filename_to_title))

    def test_return_type(self):
        """Test that the function returns a string."""
        result = filename_to_title("test_file")
        self.assertIsInstance(result, str)


def run_tests():
    """Run all tests and return success status."""
    # Create a test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestFilenameToTitle))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Return success status
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)