#!/usr/bin/env python3
"""
Unit tests for filename_to_title function in ctmm_build.py

Tests verify the function correctly converts various filename formats 
(with underscores, hyphens, mixed cases) to proper titles.
"""

import sys
import unittest
from pathlib import Path

# Add the current directory to path to import ctmm_build
sys.path.insert(0, str(Path(__file__).parent))

from ctmm_build import filename_to_title


class TestFilenameToTitle(unittest.TestCase):
    """Test cases for filename_to_title function."""

    def test_underscore_conversion(self):
        """Test conversion of underscores to spaces."""
        test_cases = [
            ("simple_file", "Simple File"),
            ("multiple_words_here", "Multiple Words Here"),
            ("single_word_test", "Single Word Test"),
            ("_leading_underscore", "Leading Underscore"),
            ("trailing_underscore_", "Trailing Underscore"),
            ("multiple___underscores", "Multiple Underscores"),
        ]
        
        for input_filename, expected_output in test_cases:
            with self.subTest(filename=input_filename):
                result = filename_to_title(input_filename)
                self.assertEqual(result, expected_output)

    def test_hyphen_conversion(self):
        """Test conversion of hyphens to spaces."""
        test_cases = [
            ("hyphen-separated", "Hyphen Separated"),
            ("multiple-word-file", "Multiple Word File"),
            ("hyphen-separated-words", "Hyphen Separated Words"),
            ("-leading-hyphen", "Leading Hyphen"),
            ("trailing-hyphen-", "Trailing Hyphen"),
            ("multiple---hyphens", "Multiple Hyphens"),
        ]
        
        for input_filename, expected_output in test_cases:
            with self.subTest(filename=input_filename):
                result = filename_to_title(input_filename)
                self.assertEqual(result, expected_output)

    def test_mixed_separators(self):
        """Test conversion of mixed underscores and hyphens."""
        test_cases = [
            ("mixed-file_name", "Mixed File Name"),
            ("complex-file_name_test", "Complex File Name Test"),
            ("under_score-and-hyphen_mix", "Under Score And Hyphen Mix"),
            ("_mixed-_start_-end_", "Mixed Start End"),
        ]
        
        for input_filename, expected_output in test_cases:
            with self.subTest(filename=input_filename):
                result = filename_to_title(input_filename)
                self.assertEqual(result, expected_output)

    def test_case_handling(self):
        """Test proper capitalization of words."""
        test_cases = [
            ("lowercase", "Lowercase"),
            ("UPPERCASE", "Uppercase"),
            ("MixedCase", "Mixedcase"),
            ("camelCase", "Camelcase"),
            ("mixedCase-with_underscores", "Mixedcase With Underscores"),
            ("UPPERCASE_FILE", "Uppercase File"),
            ("lowercase_file_name", "Lowercase File Name"),
        ]
        
        for input_filename, expected_output in test_cases:
            with self.subTest(filename=input_filename):
                result = filename_to_title(input_filename)
                self.assertEqual(result, expected_output)

    def test_single_words(self):
        """Test single word conversion."""
        test_cases = [
            ("single", "Single"),
            ("word", "Word"),
            ("test", "Test"),
            ("a", "A"),
            ("", ""),
        ]
        
        for input_filename, expected_output in test_cases:
            with self.subTest(filename=input_filename):
                result = filename_to_title(input_filename)
                self.assertEqual(result, expected_output)

    def test_edge_cases(self):
        """Test edge cases and special scenarios."""
        test_cases = [
            ("", ""),  # Empty string
            ("   ", ""),  # Spaces only (gets stripped)
            ("a_b_c_d", "A B C D"),  # Single letters
            ("123_numeric_456", "123 Numeric 456"),  # Numbers
            ("special.chars", "Special.chars"),  # Other chars preserved
            ("file.with.dots", "File.with.dots"),  # Dots preserved
            ("unicode_üöä", "Unicode Üöä"),  # Unicode characters
        ]
        
        for input_filename, expected_output in test_cases:
            with self.subTest(filename=input_filename):
                result = filename_to_title(input_filename)
                self.assertEqual(result, expected_output)

    def test_real_world_examples(self):
        """Test with realistic module filenames from CTMM system."""
        test_cases = [
            ("arbeitsblatt_depression", "Arbeitsblatt Depression"),
            ("trigger_management_module", "Trigger Management Module"),
            ("emotional-regulation_worksheet", "Emotional Regulation Worksheet"),
            ("ctmm-couples_therapy", "Ctmm Couples Therapy"),
            ("adhd_autism_support", "Adhd Autism Support"),
            ("borderline_personality_disorder", "Borderline Personality Disorder"),
            ("complex-ptsd_resources", "Complex Ptsd Resources"),
        ]
        
        for input_filename, expected_output in test_cases:
            with self.subTest(filename=input_filename):
                result = filename_to_title(input_filename)
                self.assertEqual(result, expected_output)


def run_tests():
    """Run all tests and return success status."""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestFilenameToTitle)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == "__main__":
    print("Running tests for filename_to_title function...")
    print("=" * 60)
    
    success = run_tests()
    
    print("\n" + "=" * 60)
    if success:
        print("✓ All tests passed successfully!")
        sys.exit(0)
    else:
        print("✗ Some tests failed!")
        sys.exit(1)