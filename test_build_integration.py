#!/usr/bin/env python3
"""
Test the sanitize_pkg_name integration with the build system.
"""

import unittest
import tempfile
import os
import shutil
from pathlib import Path
import sys

# Add the project root to the path
sys.path.insert(0, '/home/runner/work/CTMM---PDF-in-LaTex/CTMM---PDF-in-LaTex')

from ctmm_build import create_template, sanitize_pkg_name


class TestBuildSystemIntegration(unittest.TestCase):
    """Test cases for build system integration with sanitize_pkg_name."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir)

    def test_sanitize_pkg_name_import(self):
        """Test that sanitize_pkg_name can be imported from build system."""
        # This should work without raising an ImportError
        result = sanitize_pkg_name('test-package')
        self.assertEqual(result, 'pkgTestPackage')

    def test_style_template_with_hyphens(self):
        """Test style template creation with hyphenated names."""
        test_file = self.temp_dir / 'ctmm-design.sty'
        create_template(str(test_file))
        
        content = test_file.read_text()
        
        # Check that the package name is sanitized
        self.assertIn(r'\ProvidesPackage{pkgCtmmDesign}', content)
        # But original filename is preserved in comments
        self.assertIn('ctmm-design.sty - CTMM Style Package', content)

    def test_style_template_with_numbers(self):
        """Test style template creation with numbers in names."""
        test_file = self.temp_dir / 'test-123-package.sty'
        create_template(str(test_file))
        
        content = test_file.read_text()
        
        # Check that the package name is sanitized correctly
        self.assertIn(r'\ProvidesPackage{pkgTest123Package}', content)
        # Original filename is preserved in comments
        self.assertIn('test-123-package.sty - CTMM Style Package', content)

    def test_style_template_with_underscores(self):
        """Test style template creation with underscores in names."""
        test_file = self.temp_dir / 'form_elements.sty'
        create_template(str(test_file))
        
        content = test_file.read_text()
        
        # Check that the package name is sanitized correctly
        self.assertIn(r'\ProvidesPackage{pkgFormElements}', content)
        # Original filename is preserved in comments
        self.assertIn('form_elements.sty - CTMM Style Package', content)

    def test_style_template_complex_names(self):
        """Test style template creation with complex names."""
        test_cases = [
            ('ctmm-design-1_2', 'pkgCtmmDesign12'),
            ('math-symbols_v2-0', 'pkgMathSymbolsV20'),
            ('123-test-package', 'pkg123TestPackage'),
        ]
        
        for filename_stem, expected_pkg_name in test_cases:
            with self.subTest(filename=filename_stem):
                test_file = self.temp_dir / f'{filename_stem}.sty'
                create_template(str(test_file))
                
                content = test_file.read_text()
                
                # Check that the package name is sanitized correctly
                self.assertIn(f'\\ProvidesPackage{{{expected_pkg_name}}}', content)
                # Original filename is preserved in comments
                self.assertIn(f'{filename_stem}.sty - CTMM Style Package', content)

    def test_module_template_not_affected(self):
        """Test that module templates are not affected by package name changes."""
        test_file = self.temp_dir / 'test-module.tex'
        create_template(str(test_file))
        
        content = test_file.read_text()
        
        # Module templates should not have ProvidesPackage commands
        self.assertNotIn(r'\ProvidesPackage', content)
        # Should have section with original name conversion
        self.assertIn(r'\section{TODO: Test Module}', content)


if __name__ == '__main__':
    unittest.main()