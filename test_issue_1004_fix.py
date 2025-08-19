#!/usr/bin/env python3
"""
Test script to validate the fix for Issue #1004.
Tests the sanitization of package names in LaTeX command generation.

Issue #1004: Copilot review comment about package name sanitization 
preventing invalid LaTeX command names when using string formatting.
"""

import unittest
import tempfile
import os
import re
from pathlib import Path

# Import the sanitization functions
from build_system import sanitize_latex_identifier as build_system_sanitize
from ctmm_build import sanitize_latex_identifier as ctmm_build_sanitize, create_template


class TestIssue1004Fix(unittest.TestCase):
    """Test cases specifically for Issue #1004 fix."""
    
    def test_copilot_review_issue_resolved(self):
        """
        Test that the specific Copilot review issue is resolved.
        
        Original concern: String formatting that could create invalid LaTeX 
        command names if package_name contains special characters.
        """
        # Test cases that would have caused issues before the fix
        problematic_names = [
            "test-package",      # Common hyphenated names
            "my_style",          # Underscores 
            "123invalid",        # Starting with number
            "special@chars!",    # Special characters
            "form-elements",     # Real CTMM package name
            "ctmm-design",       # Real CTMM package name
            "package.name",      # Dots
            "complex-name_with@special&chars!",  # Multiple issues
        ]
        
        for package_name in problematic_names:
            with self.subTest(package_name=package_name):
                # Test both sanitization functions
                sanitized1 = build_system_sanitize(package_name)
                sanitized2 = ctmm_build_sanitize(package_name)
                
                # Both should produce the same result
                self.assertEqual(sanitized1, sanitized2, 
                    f"Inconsistent sanitization for '{package_name}'")
                
                # Result should be safe for LaTeX commands
                self.assertTrue(re.match(r'^[a-zA-Z][a-zA-Z0-9]*$', sanitized1),
                    f"Sanitized name '{sanitized1}' is not safe for LaTeX")
    
    def test_template_generation_safety(self):
        """
        Test that template generation produces valid LaTeX code
        even with problematic package names.
        """
        problematic_files = [
            "test-package.sty",
            "my_style.sty", 
            "form-elements.sty",
            "test-module.tex",
            "my_module.tex",
        ]
        
        with tempfile.TemporaryDirectory() as temp_dir:
            for filename in problematic_files:
                with self.subTest(filename=filename):
                    file_path = os.path.join(temp_dir, filename)
                    create_template(file_path)
                    
                    self.assertTrue(os.path.exists(file_path))
                    
                    with open(file_path, 'r') as f:
                        content = f.read()
                    
                    if filename.endswith('.sty'):
                        # Check that \ProvidesPackage uses safe name
                        provides_match = re.search(r'\\ProvidesPackage\{([^}]+)\}', content)
                        self.assertIsNotNone(provides_match, 
                            f"No \\ProvidesPackage found in {filename}")
                        
                        package_name = provides_match.group(1)
                        self.assertTrue(re.match(r'^[a-zA-Z][a-zA-Z0-9]*$', package_name),
                            f"Package name '{package_name}' in {filename} is not LaTeX-safe")
                    
                    elif filename.endswith('.tex'):
                        # Check that \label uses safe name
                        label_match = re.search(r'\\label\{sec:([^}]+)\}', content)
                        self.assertIsNotNone(label_match, 
                            f"No \\label found in {filename}")
                        
                        label_name = label_match.group(1)
                        self.assertTrue(re.match(r'^[a-zA-Z][a-zA-Z0-9]*$', label_name),
                            f"Label name '{label_name}' in {filename} is not LaTeX-safe")
    
    def test_specific_copilot_concern(self):
        """
        Test the specific pattern mentioned in the Copilot review.
        
        Original problematic pattern (conceptual):
        \\newcommand{{\\{package_name}Placeholder}}{{\\textcolor{{red}}{{[{package_name.upper()} TEMPLATE - NEEDS CONTENT]}}}}
        """
        # Simulate the kind of string formatting that was concerning
        test_package_names = [
            "test-package",      # Would create \test-packagePlaceholder (invalid)
            "my_style",          # Would create \my_stylePlaceholder (invalid)
            "123invalid",        # Would create \123invalidPlaceholder (invalid)
        ]
        
        for package_name in test_package_names:
            with self.subTest(package_name=package_name):
                # This would have been the problematic approach:
                # unsafe_command = f"\\newcommand{{\\{package_name}Placeholder}}"
                
                # Our safe approach:
                safe_name = sanitize_latex_identifier(package_name)
                safe_command = f"\\newcommand{{\\{safe_name}Placeholder}}"
                
                # Verify the safe command would be valid LaTeX
                # Extract the command name
                command_match = re.search(r'\\newcommand\{\\([^}]+)\}', safe_command)
                self.assertIsNotNone(command_match)
                
                command_name = command_match.group(1)
                self.assertTrue(re.match(r'^[a-zA-Z][a-zA-Z0-9]*$', command_name),
                    f"Command name '{command_name}' would not be valid LaTeX")
    
    def test_backwards_compatibility(self):
        """Test that the fix doesn't break existing valid names."""
        valid_names = [
            "valid",
            "validPackage", 
            "package123",
            "myStyle",
        ]
        
        for name in valid_names:
            with self.subTest(name=name):
                sanitized = sanitize_latex_identifier(name)
                # Valid names should remain unchanged
                self.assertEqual(sanitized, name,
                    f"Valid name '{name}' was unnecessarily changed to '{sanitized}'")


def sanitize_latex_identifier(name):
    """Use the same function as the build systems for testing."""
    return build_system_sanitize(name)


if __name__ == '__main__':
    print("Testing Issue #1004 fix: Package name sanitization")
    print("=" * 60)
    print("Validating that package names with special characters")
    print("are properly sanitized for safe LaTeX command generation.")
    print("=" * 60)
    
    # Run the tests
    unittest.main(verbosity=2)