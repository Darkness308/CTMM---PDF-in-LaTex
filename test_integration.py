#!/usr/bin/env python3
"""
CTMM Integration Test Suite

Comprehensive testing of the unified CTMM toolset including:
- Build system functionality
- De-escaping capabilities
- Validation accuracy
- Complete workflow integration

This test ensures all components work together seamlessly.
"""

import unittest
import tempfile
import shutil
from pathlib import Path
import subprocess
import sys
import os

# Add current directory to path to import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ctmm_unified_tool import CTMMUnifiedTool
from fix_latex_escaping import LaTeXDeEscaper


class TestCTMMIntegration(unittest.TestCase):
    """Test suite for CTMM unified tool integration."""

    def setUp(self):
        """Set up test environment."""
        self.test_dir = Path(tempfile.mkdtemp())
        self.original_dir = Path.cwd()

        # Copy necessary files to test directory
        for file in ['main.tex', 'ctmm_build.py', 'fix_latex_escaping.py', 'ctmm_unified_tool.py']:
            if Path(file).exists():
                shutil.copy2(file, self.test_dir)

        # Copy style and modules directories
        for dir_name in ['style', 'modules']:
            if Path(dir_name).exists():
                shutil.copytree(dir_name, self.test_dir / dir_name)

        os.chdir(self.test_dir)
        self.tool = CTMMUnifiedTool()

    def tearDown(self):
        """Clean up test environment."""
        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir)

    def test_unified_tool_initialization(self):
        """Test that the unified tool initializes correctly."""
        self.assertIsInstance(self.tool, CTMMUnifiedTool)
        self.assertEqual(self.tool.main_tex, "main.tex")
        self.assertIsInstance(self.tool.de_escaper, LaTeXDeEscaper)

    def test_build_system_integration(self):
        """Test build system functionality through unified tool."""
        success = self.tool.run_build_system(create_templates=False)

        # Should succeed if main.tex exists and references are valid
        if Path("main.tex").exists():
            self.assertTrue(success)
            self.assertTrue(self.tool.stats['build_success'])

    def test_de_escaping_integration(self):
        """Test de-escaping functionality through unified tool."""
        # Create test directory with over-escaped content
        test_converted = self.test_dir / 'test_converted'
        test_converted.mkdir()

        # Create sample over-escaped file
        over_escaped_content = r"""
\textbackslash{}hypertarget\textbackslash{}{test-section\textbackslash{}}\textbackslash{}{\textbackslash{}%
\textbackslash{}section\textbackslash{}{\textbackslash{}texorpdfstring\textbackslash{}{Test Section\textbackslash{}}\textbackslash{}{Test Section\textbackslash{}}\textbackslash{}}\textbackslash{}label\textbackslash{}{test-section\textbackslash{}}\textbackslash{}}

\textbackslash{}textbf\textbackslash{}{This is bold text\textbackslash{}}
"""

        test_file = test_converted / 'test.tex'
        test_file.write_text(over_escaped_content, encoding='utf-8')

        # Run de-escaping
        stats = self.tool.run_de_escaping(str(test_converted))

        # Verify results
        self.assertGreater(stats['files_processed'], 0)
        self.assertGreater(stats['total_replacements'], 0)

        # Check that content was actually fixed
        fixed_content = test_file.read_text(encoding='utf-8')
        self.assertNotIn(r'\textbackslash{}', fixed_content)
        self.assertIn(r'\hypertarget{test-section}', fixed_content)
        self.assertIn(r'\section{\texorpdfstring{Test Section}{Test Section}}', fixed_content)

    def test_validation_accuracy(self):
        """Test that validation correctly identifies issues."""
        issues = self.tool.validate_project(check_converted=False)

        # With proper setup, should have minimal issues
        self.assertIsInstance(issues, list)

        # If main.tex exists, basic validation should pass
        if Path("main.tex").exists():
            basic_issues = [issue for issue in issues if "main.tex" in issue]
            self.assertEqual(len(basic_issues), 0)

    def test_complete_workflow(self):
        """Test complete workflow integration."""
        # Create test converted directory
        test_converted = self.test_dir / 'test_workflow_converted'
        test_converted.mkdir()

        # Create sample file
        sample_content = r"""
\textbackslash{}section\textbackslash{}{Test Workflow\textbackslash{}}
\textbackslash{}textbf\textbackslash{}{Testing complete workflow integration\textbackslash{}}
"""

        (test_converted / 'workflow_test.tex').write_text(sample_content, encoding='utf-8')

        # Run complete workflow
        success = self.tool.run_complete_workflow(str(test_converted))

        # Workflow should complete successfully
        self.assertTrue(success)

        # Verify statistics were updated
        self.assertIn('build_success', self.tool.stats)
        self.assertIn('files_de_escaped', self.tool.stats)
        self.assertIn('validation_issues', self.tool.stats)

    def test_command_line_interface(self):
        """Test command line interface functionality."""
        # Test help command
        result = subprocess.run([
            sys.executable, 'ctmm_unified_tool.py', '--help'
        ], capture_output=True, text=True)

        self.assertEqual(result.returncode, 0)
        self.assertIn('CTMM Unified Tool', result.stdout)

        # Test validate command
        if Path("main.tex").exists():
            result = subprocess.run([
                sys.executable, 'ctmm_unified_tool.py', 'validate'
            ], capture_output=True, text=True)

            # Should complete (may return 0 or 1 depending on validation results)
            self.assertIn(result.returncode, [0, 1])

    def test_error_handling(self):
        """Test error handling in various scenarios."""
        # Test with non-existent directory
        stats = self.tool.run_de_escaping("non_existent_dir")
        self.assertEqual(stats, {})

        # Test validation with missing main.tex
        original_main = Path("main.tex")
        if original_main.exists():
            temp_main = Path("main.tex.temp")
            original_main.rename(temp_main)

            try:
                issues = self.tool.validate_project()
                self.assertGreater(len(issues), 0)
                self.assertTrue(any("main.tex" in issue for issue in issues))
            finally:
                temp_main.rename(original_main)


class TestLaTeXDeEscaperEnhancements(unittest.TestCase):
    """Test enhancements to the LaTeX de-escaper."""

    def setUp(self):
        """Set up test environment."""
        self.de_escaper = LaTeXDeEscaper()
        self.test_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.test_dir)

    def test_improved_validation(self):
        """Test improved validation logic."""
        # Create test file with valid LaTeX line breaks
        test_file = self.test_dir / 'test_validation.tex'
        content_with_line_breaks = r"""
\section{Test Section}
This is a line with proper line break \\
And another line \\& with escaped ampersand.
"""

        test_file.write_text(content_with_line_breaks, encoding='utf-8')

        issues = self.de_escaper.validate_latex_syntax(test_file)

        # Should not flag valid LaTeX constructs as issues
        malformed_issues = [issue for issue in issues if "malformed" in issue.lower()]
        self.assertEqual(len(malformed_issues), 0)

    def test_enhanced_patterns(self):
        """Test that enhanced patterns work correctly."""
        test_file = self.test_dir / 'test_patterns.tex'
        test_content = r"""
\textbackslash{}def\textbackslash{}labelenumi\textbackslash{}{\textbackslash{}arabic\textbackslash{}{enumi\textbackslash{}}.\textbackslash{}}
\textbackslash{}enumerate\textbackslash{}
\textbackslash{}\&
"""

        test_file.write_text(test_content, encoding='utf-8')

        # Process the file
        changed, replacements = self.de_escaper.process_file(test_file)

        # Verify file was changed and patterns were fixed
        self.assertTrue(changed)
        self.assertGreater(replacements, 0)

        # Check the fixed content
        fixed_content = test_file.read_text(encoding='utf-8')

        # Check that new patterns are fixed
        self.assertIn(r'\def', fixed_content)
        self.assertIn(r'\deflabelenumi', fixed_content)
        self.assertIn(r'enumerate', fixed_content)
        self.assertIn(r'\&', fixed_content)


def run_integration_tests():
    """Run the complete integration test suite."""
    print("="*60)
    print("CTMM INTEGRATION TEST SUITE")
    print("="*60)

    # Create test loader
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestCTMMIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestLaTeXDeEscaperEnhancements))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(suite)

    # Print summary
    print("\n" + "="*60)
    print("INTEGRATION TEST SUMMARY")
    print("="*60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")

    if result.failures:
        print("\nFAILURES:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")

    if result.errors:
        print("\nERRORS:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")

    success = len(result.failures) == 0 and len(result.errors) == 0
    print(f"\nOverall result: {'✓ PASS' if success else '✗ FAIL'}")

    return success


if __name__ == '__main__':
    success = run_integration_tests()
    sys.exit(0 if success else 1)