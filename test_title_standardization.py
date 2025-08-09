#!/usr/bin/env python3
"""
Test for title generation standardization between build systems.
Validates that both build systems use the same filename_to_title function.
"""

import unittest
import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from build_system import filename_to_title as bs_title
from ctmm_build import filename_to_title as ctmm_title


class TestTitleStandardization(unittest.TestCase):
    """Test that both build systems use the same title generation function."""

    def test_same_function_instance(self):
        """Test that both systems import the same function instance."""
        self.assertIs(bs_title, ctmm_title, 
                     "build_system and ctmm_build should use the same filename_to_title function instance")

    def test_consistent_output(self):
        """Test that both systems produce identical output for test cases."""
        test_cases = [
            'hello_world',
            'test-file', 
            'arbeitsblatt_depression',
            'trigger_management-worksheet',
            'my_test-example_file',
            '_leading_underscore_',
            'UPPER_CASE',
            'module-02-depression'
        ]
        
        for case in test_cases:
            with self.subTest(case=case):
                bs_result = bs_title(case)
                ctmm_result = ctmm_title(case)
                self.assertEqual(bs_result, ctmm_result,
                               f"Both systems should produce identical results for '{case}'")

    def test_no_code_duplication(self):
        """Test that there's no duplicate function definition in build_system.py."""
        import build_system
        import inspect
        
        # Get all functions defined in build_system module
        bs_functions = [name for name, obj in inspect.getmembers(build_system)
                       if inspect.isfunction(obj) and obj.__module__ == 'build_system']
        
        self.assertNotIn('filename_to_title', bs_functions,
                        "filename_to_title should not be defined in build_system.py")

    def test_proper_import_source(self):
        """Test that build_system imports from ctmm_build."""
        import build_system
        import ctmm_build
        
        # Check that the function in build_system comes from ctmm_build module
        self.assertEqual(bs_title.__module__, 'ctmm_build',
                        "build_system should import filename_to_title from ctmm_build")


def run_tests():
    """Run standardization tests."""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestTitleStandardization)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)