#!/usr/bin/env python3
"""
CTMM Package Name Sanitization Test Suite
Comprehensive tests for the security sanitization system that prevents invalid LaTeX command generation.

This test suite validates all edge cases and ensures the sanitization system correctly handles:
- Package names with hyphens and underscores
- Names starting with numbers
- Empty or invalid names
- Complex combinations of special characters
- LaTeX command validation requirements
"""

import unittest
import sys
from pathlib import Path

# Add the current directory to the path so we can import build_manager
sys.path.insert(0, str(Path(__file__).parent))

from build_manager import PackageNameSanitizer, CTMMEnhancedBuildManager


class TestPackageNameSanitization(unittest.TestCase):
    """Test cases for package name sanitization functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.sanitizer = PackageNameSanitizer()
    
    def test_basic_hyphen_sanitization(self):
        """Test basic hyphen to camelCase conversion."""
        test_cases = [
            ('ctmm-design', 'ctmmDesign'),
            ('form-elements', 'formElements'),
            ('my-package', 'myPackage'),
            ('single', 'single'),
            ('multi-word-package', 'multiWordPackage'),
        ]
        
        for input_name, expected in test_cases:
            with self.subTest(input_name=input_name):
                result = self.sanitizer.sanitize_package_name(input_name)
                self.assertEqual(result, expected, 
                               f"Failed to sanitize '{input_name}' to '{expected}', got '{result}'")
    
    def test_basic_underscore_sanitization(self):
        """Test basic underscore to camelCase conversion."""
        test_cases = [
            ('ctmm_diagrams', 'ctmmDiagrams'),
            ('form_elements', 'formElements'),
            ('my_package', 'myPackage'),
            ('multi_word_package', 'multiWordPackage'),
        ]
        
        for input_name, expected in test_cases:
            with self.subTest(input_name=input_name):
                result = self.sanitizer.sanitize_package_name(input_name)
                self.assertEqual(result, expected, 
                               f"Failed to sanitize '{input_name}' to '{expected}', got '{result}'")
    
    def test_mixed_separators(self):
        """Test packages with both hyphens and underscores."""
        test_cases = [
            ('ctmm-design_v2', 'ctmmDesignV2'),
            ('form_elements-beta', 'formElementsBeta'),
            ('my-pkg_test-suite', 'myPkgTestSuite'),
            ('complex_name-with-many_parts', 'complexNameWithManyParts'),
        ]
        
        for input_name, expected in test_cases:
            with self.subTest(input_name=input_name):
                result = self.sanitizer.sanitize_package_name(input_name)
                self.assertEqual(result, expected, 
                               f"Failed to sanitize '{input_name}' to '{expected}', got '{result}'")
    
    def test_numbers_in_names(self):
        """Test package names containing numbers."""
        test_cases = [
            ('package-v2', 'packageV2'),
            ('test123', 'test123'),
            ('v1-package-v2', 'v1PackageV2'),
            ('123-package', 'pkg123Package'),  # Starts with letter requirement
        ]
        
        for input_name, expected in test_cases:
            with self.subTest(input_name=input_name):
                result = self.sanitizer.sanitize_package_name(input_name)
                self.assertEqual(result, expected, 
                               f"Failed to sanitize '{input_name}' to '{expected}', got '{result}'")
    
    def test_edge_cases(self):
        """Test edge cases and problematic inputs."""
        test_cases = [
            ('', 'defaultPkg'),  # Empty string
            ('a', 'a'),  # Single character
            ('---', 'defaultPkg'),  # Only separators
            ('a-', 'a'),  # Trailing separator
            ('-a', 'a'),  # Leading separator
            ('a--b', 'aB'),  # Multiple consecutive separators
            ('a__b', 'aB'),  # Multiple underscores
        ]
        
        for input_name, expected in test_cases:
            with self.subTest(input_name=input_name):
                result = self.sanitizer.sanitize_package_name(input_name)
                self.assertEqual(result, expected, 
                               f"Failed to sanitize '{input_name}' to '{expected}', got '{result}'")
    
    def test_special_characters_removal(self):
        """Test removal of special characters that aren't valid in LaTeX commands."""
        test_cases = [
            ('package@name', 'packagename'),
            ('test!package', 'testpackage'),
            ('my$package', 'mypackage'),
            ('test%name', 'testname'),
            ('pkg^name', 'pkgname'),
            ('test&name', 'testname'),
        ]
        
        for input_name, expected in test_cases:
            with self.subTest(input_name=input_name):
                result = self.sanitizer.sanitize_package_name(input_name)
                self.assertEqual(result, expected, 
                               f"Failed to sanitize '{input_name}' to '{expected}', got '{result}'")
    
    def test_starts_with_number_handling(self):
        """Test that names starting with numbers are handled correctly."""
        test_cases = [
            ('123test', 'pkg123test'),
            ('1-package', 'pkg1Package'),
            ('2_test', 'pkg2Test'),
            ('999-name', 'pkg999Name'),
        ]
        
        for input_name, expected in test_cases:
            with self.subTest(input_name=input_name):
                result = self.sanitizer.sanitize_package_name(input_name)
                self.assertEqual(result, expected, 
                               f"Failed to sanitize '{input_name}' to '{expected}', got '{result}'")
                # Ensure result starts with a letter
                self.assertTrue(result[0].isalpha(), 
                              f"Result '{result}' should start with a letter")


class TestCommandGeneration(unittest.TestCase):
    """Test cases for safe LaTeX command generation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.sanitizer = PackageNameSanitizer()
    
    def test_basic_command_generation(self):
        """Test basic placeholder command generation."""
        test_cases = [
            ('ctmm-design', 'ctmmDesignPlaceholder'),
            ('form-elements', 'formElementsPlaceholder'),
            ('simple', 'simplePlaceholder'),
        ]
        
        for package_name, expected in test_cases:
            with self.subTest(package_name=package_name):
                result = self.sanitizer.generate_safe_command_name(package_name)
                self.assertEqual(result, expected, 
                               f"Failed to generate command for '{package_name}', expected '{expected}', got '{result}'")
    
    def test_custom_suffix_command_generation(self):
        """Test command generation with custom suffixes."""
        test_cases = [
            ('ctmm-design', 'Template', 'ctmmDesignTemplate'),
            ('form-elements', 'Helper', 'formElementsHelper'),
            ('test-pkg', 'Command', 'testPkgCommand'),
        ]
        
        for package_name, suffix, expected in test_cases:
            with self.subTest(package_name=package_name, suffix=suffix):
                result = self.sanitizer.generate_safe_command_name(package_name, suffix)
                self.assertEqual(result, expected, 
                               f"Failed to generate command for '{package_name}' with suffix '{suffix}', expected '{expected}', got '{result}'")
    
    def test_command_validation(self):
        """Test LaTeX command name validation."""
        valid_commands = [
            'ctmmDesign',
            'formElements',
            'simpleName',
            'testCommand123',
            'a',
            'Package',
        ]
        
        invalid_commands = [
            'ctmm-design',  # Contains hyphen
            'form_elements',  # Contains underscore
            'test@command',  # Contains special character
            '123command',  # Starts with number
            '',  # Empty
            'test command',  # Contains space
            'test!',  # Contains exclamation
        ]
        
        for command in valid_commands:
            with self.subTest(command=command, valid=True):
                result = self.sanitizer.validate_latex_command_name(command)
                self.assertTrue(result, f"Command '{command}' should be valid but was rejected")
        
        for command in invalid_commands:
            with self.subTest(command=command, valid=False):
                result = self.sanitizer.validate_latex_command_name(command)
                self.assertFalse(result, f"Command '{command}' should be invalid but was accepted")


class TestIntegrationScenarios(unittest.TestCase):
    """Integration test cases for real-world scenarios."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.sanitizer = PackageNameSanitizer()
    
    def test_ctmm_package_names(self):
        """Test the actual CTMM package names used in the project."""
        ctmm_packages = [
            ('ctmm-design', 'ctmmDesign'),
            ('form-elements', 'formElements'),
            ('ctmm-diagrams', 'ctmmDiagrams'),
        ]
        
        for package_name, expected_sanitized in ctmm_packages:
            with self.subTest(package_name=package_name):
                # Test sanitization
                sanitized = self.sanitizer.sanitize_package_name(package_name)
                self.assertEqual(sanitized, expected_sanitized)
                
                # Test command generation
                command = self.sanitizer.generate_safe_command_name(package_name)
                expected_command = expected_sanitized + 'Placeholder'
                self.assertEqual(command, expected_command)
                
                # Test validation
                self.assertTrue(self.sanitizer.validate_latex_command_name(command))
    
    def test_end_to_end_security_validation(self):
        """Test complete end-to-end security validation."""
        problematic_packages = [
            'ctmm-design',
            'form-elements',
            'ctmm_diagrams',
            'complex-package_name-v2',
            '123-numeric-start',
            'special@chars!',
        ]
        
        for package_name in problematic_packages:
            with self.subTest(package_name=package_name):
                # Sanitize the package name
                sanitized = self.sanitizer.sanitize_package_name(package_name)
                
                # Generate a command
                command = self.sanitizer.generate_safe_command_name(package_name)
                
                # Validate the command is safe
                is_valid = self.sanitizer.validate_latex_command_name(command)
                
                # All generated commands should be valid
                self.assertTrue(is_valid, 
                              f"Package '{package_name}' generated invalid command '{command}'")
                
                # Command should start with a letter
                self.assertTrue(command[0].isalpha(), 
                              f"Command '{command}' should start with a letter")
                
                # Command should contain only alphanumeric characters
                self.assertTrue(command.isalnum(), 
                              f"Command '{command}' should contain only alphanumeric characters")


class TestBuildManagerIntegration(unittest.TestCase):
    """Test cases for build manager integration."""
    
    def test_package_mapping_creation(self):
        """Test that package mappings are created correctly."""
        # Create a temporary main.tex content for testing
        test_content = """
\\usepackage{style/ctmm-design}
\\usepackage{style/form-elements}
\\usepackage{style/ctmm-diagrams}
"""
        
        # This test would need a mock setup since we can't easily test file I/O
        # For now, just test the sanitizer directly
        expected_mappings = {
            'ctmm-design': 'ctmmDesign',
            'form-elements': 'formElements',
            'ctmm-diagrams': 'ctmmDiagrams',
        }
        
        sanitizer = PackageNameSanitizer()
        for original, expected in expected_mappings.items():
            result = sanitizer.sanitize_package_name(original)
            self.assertEqual(result, expected)


def run_comprehensive_tests():
    """Run all test suites and provide a comprehensive report."""
    print("CTMM Package Name Sanitization Test Suite")
    print("=========================================")
    print()
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestPackageNameSanitization))
    suite.addTests(loader.loadTestsFromTestCase(TestCommandGeneration))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegrationScenarios))
    suite.addTests(loader.loadTestsFromTestCase(TestBuildManagerIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print(f"\nFAILURES ({len(result.failures)}):")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback.split('AssertionError: ')[-1].split('\\n')[0]}")
    
    if result.errors:
        print(f"\nERRORS ({len(result.errors)}):")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback.split('\\n')[-2]}")
    
    if result.wasSuccessful():
        print("\n✅ ALL TESTS PASSED - Security sanitization system is working correctly!")
        return True
    else:
        print("\n❌ SOME TESTS FAILED - Review and fix issues before deployment!")
        return False


if __name__ == "__main__":
    success = run_comprehensive_tests()
    sys.exit(0 if success else 1)