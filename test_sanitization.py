#!/usr/bin/env python3
"""
Test script for LaTeX identifier sanitization functionality.
Tests the fix for issue #1004 regarding package name sanitization.
"""

import unittest
import tempfile
import os
from pathlib import Path

# Import the functions we're testing
from build_system import sanitize_latex_identifier as build_system_sanitize
from ctmm_build import sanitize_latex_identifier as ctmm_build_sanitize


class TestLatexSanitization(unittest.TestCase):
    """Test cases for LaTeX identifier sanitization."""
    
    def test_sanitize_function_consistency(self):
        """Test that both build systems use the same sanitization logic."""
        test_cases = [
            "test-package",
            "my_style", 
            "123invalid",
            "special@chars!",
            "",
            "valid",
            "complex-name_with@special&chars!",
        ]
        
        for test_case in test_cases:
            with self.subTest(test_case=test_case):
                result1 = build_system_sanitize(test_case)
                result2 = ctmm_build_sanitize(test_case)
                self.assertEqual(result1, result2, 
                    f"Sanitization results differ for '{test_case}': {result1} != {result2}")
    
    def test_sanitize_basic_cases(self):
        """Test basic sanitization cases."""
        # Test normal case
        self.assertEqual(sanitize_latex_identifier("valid"), "valid")
        
        # Test with hyphens (common in package names)
        self.assertEqual(sanitize_latex_identifier("test-package"), "testpackage")
        
        # Test with underscores
        self.assertEqual(sanitize_latex_identifier("my_style"), "mystyle")
        
        # Test starting with number
        result = sanitize_latex_identifier("123invalid")
        self.assertTrue(result.startswith("pkg"))
        self.assertIn("123invalid", result)
        
        # Test empty string
        result = sanitize_latex_identifier("")
        self.assertEqual(result, "defaultpackage")
        
        # Test special characters
        self.assertEqual(sanitize_latex_identifier("special@chars!"), "specialchars")
    
    def test_sanitize_latex_requirements(self):
        """Test that sanitized names meet LaTeX requirements."""
        test_cases = [
            "test-package",
            "my_style", 
            "123invalid",
            "special@chars!",
            "",
            "valid",
            "complex-name_with@special&chars!",
            "form-elements",
            "ctmm-design",
        ]
        
        for test_case in test_cases:
            with self.subTest(test_case=test_case):
                result = sanitize_latex_identifier(test_case)
                
                # Must not be empty
                self.assertTrue(result, f"Result is empty for '{test_case}'")
                
                # Must start with a letter
                self.assertTrue(result[0].isalpha(), 
                    f"Result '{result}' for '{test_case}' doesn't start with letter")
                
                # Must contain only alphanumeric characters
                self.assertTrue(result.isalnum(), 
                    f"Result '{result}' for '{test_case}' contains non-alphanumeric characters")
    
    def test_template_generation_with_problematic_names(self):
        """Test template generation with problematic package/module names."""
        from ctmm_build import create_template
        
        # Test with a problematic filename
        with tempfile.TemporaryDirectory() as temp_dir:
            # Test style file with hyphens
            style_path = os.path.join(temp_dir, "test-style.sty")
            create_template(style_path)
            
            self.assertTrue(os.path.exists(style_path))
            
            # Read the generated content
            with open(style_path, 'r') as f:
                content = f.read()
            
            # Check that \ProvidesPackage uses sanitized name
            self.assertIn("\\ProvidesPackage{teststyle}", content)
            self.assertNotIn("\\ProvidesPackage{test-style}", content)
            
            # Test module file with underscores
            module_path = os.path.join(temp_dir, "test_module.tex")
            create_template(module_path)
            
            self.assertTrue(os.path.exists(module_path))
            
            # Read the generated content
            with open(module_path, 'r') as f:
                content = f.read()
            
            # Check that \label uses sanitized name
            self.assertIn("\\label{sec:testmodule}", content)
            self.assertNotIn("\\label{sec:test_module}", content)


def sanitize_latex_identifier(name):
    """Use the same function as the build systems for testing."""
    return build_system_sanitize(name)


if __name__ == '__main__':
    print("Testing LaTeX identifier sanitization...")
    
    # Run the tests
    unittest.main(verbosity=2)