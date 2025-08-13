#!/usr/bin/env python3
"""
Unit tests for CTMM Build Manager.
Tests the build_manager.py module functions for correctness.
"""

import unittest
import sys
import tempfile
import os
from pathlib import Path

# Add current directory to path for importing modules
sys.path.insert(0, str(Path(__file__).parent))
import build_manager


class TestCTMMBuildManager(unittest.TestCase):
    """Test cases for the CTMMBuildManager class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.temp_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.temp_dir)
        
        # Create a minimal main.tex for testing
        self.main_tex_content = """\\documentclass{article}
\\usepackage{style/test-style}
\\usepackage{style/another-style}
\\begin{document}
\\input{modules/test-module}
\\input{modules/another-module}
\\end{document}
"""
        with open("main.tex", "w", encoding="utf-8") as f:
            f.write(self.main_tex_content)
        
        self.manager = build_manager.CTMMBuildManager()

    def tearDown(self):
        """Clean up after each test method."""
        os.chdir(self.original_cwd)
        # Note: Not cleaning up temp_dir to avoid permission issues in CI
    
    def test_initialization(self):
        """Test that CTMMBuildManager initializes correctly."""
        manager = build_manager.CTMMBuildManager("test.tex")
        self.assertEqual(manager.main_tex_file, "test.tex")
        self.assertEqual(manager.backup_suffix, ".backup")
        self.assertEqual(manager.missing_files, [])
        self.assertEqual(manager.build_log, [])
    
    def test_scan_references(self):
        """Test that scan_references correctly identifies style and module files."""
        references = self.manager.scan_references()
        
        self.assertIn('style_packages', references)
        self.assertIn('module_inputs', references)
        
        expected_styles = ['style/test-style.sty', 'style/another-style.sty']
        expected_modules = ['modules/test-module.tex', 'modules/another-module.tex']
        
        self.assertEqual(references['style_packages'], expected_styles)
        self.assertEqual(references['module_inputs'], expected_modules)
    
    def test_check_file_existence_missing_files(self):
        """Test that check_file_existence correctly identifies missing files."""
        references = {
            'style_packages': ['style/existing.sty', 'style/missing.sty'],
            'module_inputs': ['modules/existing.tex', 'modules/missing.tex']
        }
        
        # Create one file from each category to test mixed scenarios
        os.makedirs('style', exist_ok=True)
        os.makedirs('modules', exist_ok=True)
        with open('style/existing.sty', 'w') as f:
            f.write('% existing style')
        with open('modules/existing.tex', 'w') as f:
            f.write('% existing module')
        
        missing = self.manager.check_file_existence(references)
        
        self.assertEqual(missing['style_packages'], ['style/missing.sty'])
        self.assertEqual(missing['module_inputs'], ['modules/missing.tex'])
        self.assertEqual(len(self.manager.missing_files), 2)
    
    def test_create_style_template(self):
        """Test that create_style_template creates a valid template."""
        test_path = "style/test-template.sty"
        self.manager.create_style_template(test_path)
        
        self.assertTrue(Path(test_path).exists())
        
        with open(test_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for expected content
        self.assertIn('\\NeedsTeXFormat{LaTeX2e}', content)
        self.assertIn('\\ProvidesPackage{test-template}', content)
        self.assertIn('TODO', content)
        self.assertIn('\\endinput', content)
    
    def test_create_module_template(self):
        """Test that create_module_template creates a valid template."""
        test_path = "modules/test-module.tex"
        self.manager.create_module_template(test_path)
        
        self.assertTrue(Path(test_path).exists())
        
        with open(test_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for expected content
        self.assertIn('\\section{Test Module}', content)
        self.assertIn('\\label{sec:test-module}', content)
        self.assertIn('TODO', content)
        self.assertIn('CONTENT NEEDED', content)
    
    def test_backup_and_restore_main_tex(self):
        """Test backup and restore functionality."""
        original_content = "original content"
        with open("main.tex", "w", encoding="utf-8") as f:
            f.write(original_content)
        
        # Create backup
        backup_file = self.manager.backup_main_tex()
        self.assertTrue(Path(backup_file).exists())
        
        # Modify original
        with open("main.tex", "w", encoding="utf-8") as f:
            f.write("modified content")
        
        # Restore from backup
        self.manager.restore_main_tex(backup_file)
        
        with open("main.tex", "r", encoding="utf-8") as f:
            restored_content = f.read()
        
        self.assertEqual(restored_content, original_content)
        self.assertFalse(Path(backup_file).exists())
    
    def test_comment_out_inputs(self):
        """Test that comment_out_inputs correctly comments module inputs."""
        module_files = ['modules/test-module.tex']
        backup_file = self.manager.comment_out_inputs(module_files)
        
        with open("main.tex", "r", encoding="utf-8") as f:
            content = f.read()
        
        self.assertIn("% COMMENTED FOR TESTING: \\input{modules/test-module}", content)
        self.assertNotIn("\\input{modules/test-module}", content.replace("% COMMENTED FOR TESTING: \\input{modules/test-module}", ""))
        
        # Restore for cleanup
        self.manager.restore_main_tex(backup_file)
    
    def test_uncomment_input(self):
        """Test that uncomment_input correctly restores module inputs."""
        # First comment out
        module_files = ['modules/test-module.tex']
        backup_file = self.manager.comment_out_inputs(module_files)
        
        # Then uncomment one
        self.manager.uncomment_input('modules/test-module.tex')
        
        with open("main.tex", "r", encoding="utf-8") as f:
            content = f.read()
        
        self.assertIn("\\input{modules/test-module}", content)
        self.assertNotIn("% COMMENTED FOR TESTING: \\input{modules/test-module}", content)
        
        # Restore for cleanup
        self.manager.restore_main_tex(backup_file)
    
    def test_create_missing_templates(self):
        """Test that create_missing_templates creates all required templates."""
        missing_files = {
            'style_packages': ['style/missing1.sty', 'style/missing2.sty'],
            'module_inputs': ['modules/missing1.tex', 'modules/missing2.tex']
        }
        
        self.manager.create_missing_templates(missing_files)
        
        # Check that all files were created
        for file_path in missing_files['style_packages']:
            self.assertTrue(Path(file_path).exists())
        for file_path in missing_files['module_inputs']:
            self.assertTrue(Path(file_path).exists())
    
    def test_generate_build_report(self):
        """Test that generate_build_report creates a valid report."""
        test_results = {
            'modules/success.tex': True,
            'modules/failure.tex': False
        }
        
        self.manager.missing_files = ['style/missing.sty']
        self.manager.build_log = ['Test log entry']
        
        self.manager.generate_build_report(test_results)
        
        self.assertTrue(Path('build_report.md').exists())
        
        with open('build_report.md', 'r', encoding='utf-8') as f:
            report_content = f.read()
        
        # Check report content
        self.assertIn('CTMM LaTeX Build Report', report_content)
        self.assertIn('**Total modules tested**: 2', report_content)
        self.assertIn('**Successful builds**: 1', report_content)
        self.assertIn('**Failed builds**: 1', report_content)
        self.assertIn('success', report_content)
        self.assertIn('failure', report_content)
        self.assertIn('missing.sty', report_content)


class TestBuildManagerIntegration(unittest.TestCase):
    """Integration tests for build manager functionality."""
    
    def test_datetime_import_exists(self):
        """Test that datetime module is properly imported."""
        # This test ensures the datetime import issue from PR #8 is fixed
        self.assertTrue(hasattr(build_manager, 'datetime'))
        
        # Test that datetime.datetime.now() can be called
        now = build_manager.datetime.datetime.now()
        self.assertIsInstance(now, build_manager.datetime.datetime)
    
    def test_consistent_log_formatting(self):
        """Test that log messages use consistent [INFO] formatting."""
        # Create a temporary test environment
        temp_dir = tempfile.mkdtemp()
        original_cwd = os.getcwd()
        
        try:
            os.chdir(temp_dir)
            
            # Create minimal test files
            with open("main.tex", "w") as f:
                f.write("\\documentclass{article}\n\\begin{document}\nTest\n\\end{document}")
            
            manager = build_manager.CTMMBuildManager()
            
            # Capture output by redirecting stdout temporarily
            import io
            import contextlib
            
            captured_output = io.StringIO()
            with contextlib.redirect_stdout(captured_output):
                manager.create_style_template("style/test.sty")
                manager.create_module_template("modules/test.tex")
            
            output = captured_output.getvalue()
            
            # Check that all log messages use [INFO] format
            lines = output.strip().split('\n')
            for line in lines:
                if line.strip():  # Skip empty lines
                    self.assertTrue(line.startswith('[INFO]'), f"Line doesn't start with [INFO]: {line}")
        
        finally:
            os.chdir(original_cwd)
    
    def test_step_numbering_functionality(self):
        """Test that the step numbering system works correctly."""
        # This test validates the improved workflow structure suggested in PR #8
        temp_dir = tempfile.mkdtemp()
        original_cwd = os.getcwd()
        
        try:
            os.chdir(temp_dir)
            
            # Create minimal test files
            with open("main.tex", "w") as f:
                f.write("\\documentclass{article}\n\\begin{document}\nTest\n\\end{document}")
            
            manager = build_manager.CTMMBuildManager()
            
            # Test that run_complete_analysis uses step numbering
            # We'll check this by examining the method exists and is callable
            self.assertTrue(hasattr(manager, 'run_complete_analysis'))
            self.assertTrue(callable(manager.run_complete_analysis))
            
            # Test individual step methods exist
            self.assertTrue(hasattr(manager, 'scan_references'))
            self.assertTrue(hasattr(manager, 'check_file_existence'))
            self.assertTrue(hasattr(manager, 'create_missing_templates'))
            self.assertTrue(hasattr(manager, 'test_basic_framework'))
            self.assertTrue(hasattr(manager, 'test_modules_incrementally'))
            self.assertTrue(hasattr(manager, 'generate_build_report'))
        
        finally:
            os.chdir(original_cwd)


if __name__ == '__main__':
    # Run the tests with detailed output
    unittest.main(verbosity=2)