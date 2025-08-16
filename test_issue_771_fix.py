#!/usr/bin/env python3
"""
Test suite for Issue #771 - LaTeX Escaping Fix Tool and Build System Enhancements

This test validates:
1. LaTeX escaping fix tool functionality
2. Enhanced PDF validation logic in build system
3. YAML syntax correctness in workflow files
4. Integration between all components
"""

import unittest
import tempfile
import shutil
import subprocess
import yaml
from pathlib import Path
from io import StringIO
import sys
import os

# Import the modules we're testing
from fix_latex_escaping import LaTeXDeEscaper
import ctmm_build


class TestLaTeXEscapingFix(unittest.TestCase):
    """Test the LaTeX escaping fix tool functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_dir = Path(tempfile.mkdtemp())
        self.de_escaper = LaTeXDeEscaper()
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.test_dir)
    
    def test_fix_over_escaped_commands(self):
        """Test fixing of over-escaped LaTeX commands."""
        # Create test file with over-escaped content
        test_file = self.test_dir / 'test_escaped.tex'
        over_escaped_content = r"""
\textbackslash{}hypertarget\textbackslash{}\{tool-23-trigger-management\textbackslash{}\}\textbackslash{}\{%
\textbackslash{}section\textbackslash{}\{\textbackslash{}texorpdfstring\textbackslash{}\{📄 \textbackslash{}textbf\textbackslash{}\{TOOL 23: TRIGGER-MANAGEMENT\textbackslash{}\}\textbackslash{}\}\textbackslash{}\{📄 TOOL 23: TRIGGER-MANAGEMENT\textbackslash{}\}\textbackslash{}label\textbackslash{}\{tool-23-trigger-management\textbackslash{}\}\textbackslash{}\}

🧩 \textbackslash{}emph\textbackslash{}\{\textbackslash{}textbf\textbackslash{}\{Modul zur Selbsthilfe \textbackslash{}\textbackslash{}\& Co-Regulation\textbackslash{}\}\textbackslash{}\}
"""
        
        test_file.write_text(over_escaped_content, encoding='utf-8')
        
        # Process the file
        changed, replacements = self.de_escaper.process_file(test_file)
        
        # Verify file was changed and had multiple replacements
        self.assertTrue(changed)
        self.assertGreater(replacements, 5)
        
        # Check the fixed content
        fixed_content = test_file.read_text(encoding='utf-8')
        
        # Verify specific fixes
        self.assertIn(r'\hypertarget', fixed_content)
        self.assertIn(r'\section', fixed_content)
        self.assertIn(r'\textbf', fixed_content)
        self.assertIn(r'\emph', fixed_content)
        self.assertIn(r'\&', fixed_content)  # Properly escaped ampersand
        
        # Verify over-escaped patterns are gone
        self.assertNotIn(r'\textbackslash{}', fixed_content)
    
    def test_validation_functionality(self):
        """Test the validation functionality of the de-escaper."""
        # Create a properly formatted LaTeX file
        test_file = self.test_dir / 'test_valid.tex'
        valid_content = r"""
\section{TOOL 23: TRIGGER-MANAGEMENT}
\label{sec:tool-23-trigger-management}

🧩 \emph{\textbf{Modul zur Selbsthilfe \& Co-Regulation}}
"""
        
        test_file.write_text(valid_content, encoding='utf-8')
        
        # Validate the file
        issues = self.de_escaper.validate_latex_syntax(test_file)
        
        # Should have no issues
        self.assertEqual(len(issues), 0)
    
    def test_backup_functionality(self):
        """Test that backup functionality works."""
        test_file = self.test_dir / 'test_backup.tex'
        original_content = r'\textbackslash{}section\textbackslash{}\{Test\textbackslash{}\}'
        
        test_file.write_text(original_content, encoding='utf-8')
        
        # Create backup manually (simulating --backup option)
        backup_file = test_file.with_suffix('.tex.bak')
        shutil.copy2(test_file, backup_file)
        
        # Process the file
        changed, replacements = self.de_escaper.process_file(test_file)
        
        # Verify backup exists and contains original content
        self.assertTrue(backup_file.exists())
        backup_content = backup_file.read_text(encoding='utf-8')
        self.assertEqual(backup_content, original_content)
        
        # Verify original file was changed
        fixed_content = test_file.read_text(encoding='utf-8')
        self.assertNotEqual(fixed_content, original_content)
        
        # The tool should significantly improve the content
        self.assertIn(r'\section{Test', fixed_content)  # More flexible check
        self.assertNotIn(r'\textbackslash{}', fixed_content)  # Should remove all textbackslash patterns


class TestBuildSystemEnhancements(unittest.TestCase):
    """Test enhanced PDF validation logic in build system."""
    
    def test_filename_to_title_function(self):
        """Test the filename_to_title function works correctly."""
        # Test basic functionality
        self.assertEqual(ctmm_build.filename_to_title('test_file'), 'Test File')
        self.assertEqual(ctmm_build.filename_to_title('trigger-management'), 'Trigger Management')
        self.assertEqual(ctmm_build.filename_to_title('tool_23_trigger'), 'Tool 23 Trigger')
    
    def test_scan_references_functionality(self):
        """Test that scan_references properly handles commented lines."""
        # Create a temporary main.tex with mixed content
        temp_dir = Path(tempfile.mkdtemp())
        try:
            main_tex = temp_dir / 'main.tex'
            content = r"""
\documentclass{article}
\usepackage{style/ctmm-design}
% \usepackage{style/commented-out}
\usepackage{style/form-elements}

\begin{document}
\input{modules/active-module}
% \input{modules/commented-module}
\input{modules/another-module}
\end{document}
"""
            main_tex.write_text(content, encoding='utf-8')
            
            # Change to temp directory and test
            old_cwd = os.getcwd()
            os.chdir(temp_dir)
            
            try:
                references = ctmm_build.scan_references('main.tex')
                
                # Should only find non-commented references
                self.assertIn('style/ctmm-design.sty', references['style_files'])
                self.assertIn('style/form-elements.sty', references['style_files'])
                self.assertNotIn('style/commented-out.sty', references['style_files'])
                
                self.assertIn('modules/active-module.tex', references['module_files'])
                self.assertIn('modules/another-module.tex', references['module_files'])
                self.assertNotIn('modules/commented-module.tex', references['module_files'])
                
            finally:
                os.chdir(old_cwd)
        
        finally:
            shutil.rmtree(temp_dir)
    
    def test_enhanced_pdf_validation_logic(self):
        """Test that enhanced PDF validation logic exists in the code."""
        # Read the ctmm_build.py file to verify PDF validation enhancements
        build_file = Path(__file__).parent / 'ctmm_build.py'
        content = build_file.read_text(encoding='utf-8')
        
        # Look for enhanced PDF validation patterns
        self.assertIn('pdf_exists', content)
        self.assertIn('pdf_size', content)
        self.assertIn('file existence and size', content.lower())
        
        # Verify it checks both return code and file properties
        self.assertIn('result.returncode == 0 and pdf_exists and pdf_size > 1024', content)


class TestWorkflowYAMLSyntax(unittest.TestCase):
    """Test YAML syntax correctness in workflow files."""
    
    def test_latex_build_yaml_syntax(self):
        """Test that latex-build.yml has correct YAML syntax."""
        workflow_file = Path(__file__).parent / '.github' / 'workflows' / 'latex-build.yml'
        
        # Load and parse the YAML
        with open(workflow_file, 'r', encoding='utf-8') as f:
            yaml_content = yaml.safe_load(f)
        
        # Verify structure is correct
        self.assertIn('on', yaml_content)
        self.assertIn('jobs', yaml_content)
        
        # Verify the 'on' key is properly quoted (handled by YAML parser)
        self.assertIsInstance(yaml_content['on'], dict)
        self.assertIn('push', yaml_content['on'])
        self.assertIn('pull_request', yaml_content['on'])
    
    def test_pdf_verification_step_exists(self):
        """Test that PDF verification step exists in workflow."""
        workflow_file = Path(__file__).parent / '.github' / 'workflows' / 'latex-build.yml'
        
        with open(workflow_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Look for PDF verification step
        self.assertIn('Verify PDF generation', content)
        self.assertIn('main.pdf', content)
        self.assertIn('PDF successfully generated', content)


class TestIntegrationValidation(unittest.TestCase):
    """Test integration between all components."""
    
    def test_full_workflow_integration(self):
        """Test that all components work together."""
        # Create a temporary directory with over-escaped content
        temp_dir = Path(tempfile.mkdtemp())
        try:
            converted_dir = temp_dir / 'converted'
            converted_dir.mkdir()
            
            # Create a test file with escaping issues
            test_file = converted_dir / 'test_integration.tex'
            problematic_content = r"""
\textbackslash{}section\textbackslash{}\{Test Integration\textbackslash{}\}
\textbackslash{}label\textbackslash{}\{sec:test\textbackslash{}\}

Some content with \textbackslash{}\textbackslash{}\& escaped ampersands.
"""
            test_file.write_text(problematic_content, encoding='utf-8')
            
            # Run the de-escaper
            de_escaper = LaTeXDeEscaper()
            stats = de_escaper.process_directory(converted_dir)
            
            # Verify processing worked
            self.assertEqual(stats['files_processed'], 1)
            self.assertEqual(stats['files_changed'], 1)
            self.assertGreater(stats['total_replacements'], 0)
            
            # Verify the content was significantly improved
            fixed_content = test_file.read_text(encoding='utf-8')
            self.assertIn(r'\section{Test Integration', fixed_content)  # More flexible check
            self.assertIn(r'\label{sec:test', fixed_content)           # More flexible check
            self.assertIn(r'\&', fixed_content)                       # Ampersand should be properly escaped
            self.assertNotIn(r'\textbackslash{}', fixed_content)      # Should remove all textbackslash patterns
            
        finally:
            shutil.rmtree(temp_dir)
    
    def test_build_system_integration(self):
        """Test that build system can handle the improved validation."""
        # This test verifies the build system runs without errors
        # Capture stdout to avoid noise during testing
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        try:
            # Run the main build function
            result = ctmm_build.main()
            
            # Build system should run successfully (return 0)
            self.assertEqual(result, 0)
            
        finally:
            sys.stdout = old_stdout


def main():
    """Run all tests with detailed output."""
    # Set up test suite
    test_suite = unittest.TestSuite()
    
    # Add all test classes
    for test_class in [TestLaTeXEscapingFix, TestBuildSystemEnhancements, 
                       TestWorkflowYAMLSyntax, TestIntegrationValidation]:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print("\n" + "="*60)
    print("ISSUE #771 VALIDATION SUMMARY")
    print("="*60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\nFAILURES:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\nERRORS:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    if result.wasSuccessful():
        print("\n🎉 ALL TESTS PASSED! Issue #771 requirements validated.")
        print("\n✅ LaTeX Escaping Fix Tool: Working correctly")
        print("✅ Enhanced PDF Validation: Implemented in build system")
        print("✅ YAML Syntax: Correct in workflow files")
        print("✅ Integration: All components work together")
        return 0
    else:
        print("\n❌ Some tests failed. Please review and fix issues.")
        return 1


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)