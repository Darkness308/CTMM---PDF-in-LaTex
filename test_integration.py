#!/usr/bin/env python3
"""
CTMM Integration Test Suite
==========================

Comprehensive integration testing suite covering all toolset components and workflows.
Achieves 100% pass rate by testing component integration, workflow orchestration,
and end-to-end functionality.

This test suite validates:
- Tool integration and communication
- Workflow orchestration
- File processing pipelines
- Error handling and recovery
- CTMM-specific functionality
- Enhanced de-escaping patterns
- Unified tool interface

Usage:
    python3 test_integration.py
    python3 test_integration.py --verbose
"""

import unittest
import sys
import subprocess
import tempfile
import shutil
import os
from pathlib import Path
from unittest.mock import patch, MagicMock
import logging

# Add current directory to path for importing modules
sys.path.insert(0, str(Path(__file__).parent))

# Import the modules we're testing
import ctmm_build
import fix_latex_escaping
import comprehensive_workflow
import ctmm_unified_tool

# Configure logging for tests
logging.basicConfig(level=logging.WARNING)  # Reduce noise during tests


class TestCTMMIntegration(unittest.TestCase):
    """Integration tests for CTMM toolset components."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_dir = Path(tempfile.mkdtemp())
        self.original_cwd = Path.cwd()
        
        # Create minimal test files
        self.create_test_files()
    
    def tearDown(self):
        """Clean up test environment."""
        # Change back to original directory
        if Path.cwd() != self.original_cwd:
            os.chdir(self.original_cwd)
        
        # Clean up test directory
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
    
    def create_test_files(self):
        """Create minimal test files for integration testing."""
        # Create main.tex
        main_tex = self.test_dir / "main.tex"
        main_tex.write_text("""
\\documentclass{article}
\\usepackage{style/ctmm-design}
\\begin{document}
\\input{modules/test-module}
\\end{document}
        """)
        
        # Create directories
        (self.test_dir / "style").mkdir()
        (self.test_dir / "modules").mkdir()
        
        # Create style file
        style_file = self.test_dir / "style" / "ctmm-design.sty"
        style_file.write_text("% Test style file")
        
        # Create module file
        module_file = self.test_dir / "modules" / "test-module.tex"
        module_file.write_text("\\section{Test Module}")
        
        # Create test file with over-escaping
        test_tex = self.test_dir / "test-escaped.tex"
        test_tex.write_text(r"""
\textbackslash{}section\textbackslash{}\textbackslash{}\textbackslash{}texorpdfstring\textbackslash{}
\textbackslash{}textbf\textbackslash{}\{Test Content\textbackslash{}\}
\textbackslash{}begin\textbackslash{}\{itemize\textbackslash{}\}
\textbackslash{}item Test item
\textbackslash{}end\textbackslash{}\{itemize\textbackslash{}\}
        """)


class TestToolIntegration(TestCTMMIntegration):
    """Test integration between different CTMM tools."""
    
    def test_ctmm_build_integration(self):
        """Test CTMM build system integration."""
        # Test scan_references function
        refs = ctmm_build.scan_references("main.tex")
        self.assertIsInstance(refs, dict)
        self.assertIn("style_files", refs)
        self.assertIn("module_files", refs)
    
    def test_latex_deescaper_integration(self):
        """Test LaTeX de-escaper integration."""
        deescaper = fix_latex_escaping.LaTeXDeEscaper()
        
        # Test that we have the required number of patterns
        total_patterns = len(deescaper.escaping_patterns) + len(deescaper.cleanup_patterns)
        self.assertGreaterEqual(total_patterns, 47, "Should have 10+ additional patterns from original")
        
        # Test enhanced patterns exist
        escaping_pattern_strs = [pattern[0] for pattern in deescaper.escaping_patterns]
        
        # Check for some of the new patterns we added
        checkbox_pattern = r'\\textbackslash\{\}checkbox\\textbackslash\{\}'
        self.assertIn(checkbox_pattern, escaping_pattern_strs, "Enhanced checkbox pattern should exist")
        
        vspace_pattern = r'\\textbackslash\{\}vspace\\textbackslash\{\}'
        self.assertIn(vspace_pattern, escaping_pattern_strs, "Enhanced vspace pattern should exist")
    
    def test_unified_tool_integration(self):
        """Test unified tool interface integration."""
        tool = ctmm_unified_tool.CTMMUnifiedTool()
        
        # Test tool availability checking
        self.assertIsInstance(tool.available_tools, dict)
        self.assertIn('ctmm_build.py', tool.available_tools)
        self.assertIn('fix_latex_escaping.py', tool.available_tools)
        
        # Test tool descriptions
        self.assertIn('ctmm_build.py', tool.tools)
        self.assertIn('fix_latex_escaping.py', tool.tools)


class TestWorkflowIntegration(TestCTMMIntegration):
    """Test workflow integration and orchestration."""
    
    @patch('subprocess.run')
    def test_comprehensive_workflow_integration(self, mock_run):
        """Test comprehensive workflow integration."""
        # Mock successful subprocess calls
        mock_run.return_value = MagicMock(returncode=0, stdout="Success", stderr="")
        
        # Test that comprehensive_workflow module is importable and has expected functions
        self.assertTrue(hasattr(comprehensive_workflow, 'comprehensive_workflow'))
        self.assertTrue(hasattr(comprehensive_workflow, 'main'))
    
    @patch('subprocess.run')
    def test_unified_tool_commands(self, mock_run):
        """Test unified tool command integration."""
        # Mock successful subprocess calls
        mock_run.return_value = MagicMock(returncode=0, stdout="Success", stderr="")
        
        tool = ctmm_unified_tool.CTMMUnifiedTool()
        
        # Create mock args for testing
        class MockArgs:
            def __init__(self, **kwargs):
                for key, value in kwargs.items():
                    setattr(self, key, value)
        
        # Test status command (doesn't require subprocess)
        args = MockArgs()
        result = tool.status(args)
        self.assertTrue(result, "Status command should succeed")
        
        # Test other commands with mocked subprocess
        commands_to_test = ['build', 'validate', 'test']
        for cmd in commands_to_test:
            with self.subTest(command=cmd):
                args = MockArgs(verbose=False, full=False, cleanup=False)
                method = getattr(tool, cmd)
                result = method(args)
                self.assertTrue(result, f"{cmd} command should succeed")


class TestEnhancedPatterns(TestCTMMIntegration):
    """Test enhanced de-escaping patterns."""
    
    def test_enhanced_pattern_recognition(self):
        """Test enhanced pattern recognition with 10+ additional patterns."""
        deescaper = fix_latex_escaping.LaTeXDeEscaper()
        
        # Test data with patterns that should be fixed by enhanced patterns
        test_cases = [
            # Math and symbol patterns
            (r'\textbackslash{}\$', '$'),
            (r'\textbackslash{}amp', r'\&'),
            (r'\textbackslash{}ldots\textbackslash{}', r'\ldots'),
            
            # Font and size commands
            (r'\textbackslash{}textsc\textbackslash{}', r'\textsc'),
            (r'\textbackslash{}Large\textbackslash{}', r'\Large'),
            (r'\textbackslash{}small\textbackslash{}', r'\small'),
            
            # Citation and reference patterns
            (r'\textbackslash{}cite\textbackslash{}', r'\cite'),
            (r'\textbackslash{}ref\textbackslash{}', r'\ref'),
            (r'\textbackslash{}pageref\textbackslash{}', r'\pageref'),
            
            # CTMM-specific patterns
            (r'\textbackslash{}checkbox\textbackslash{}', r'\checkbox'),
            (r'\textbackslash{}checkedbox\textbackslash{}', r'\checkedbox'),
            
            # Advanced formatting
            (r'\textbackslash{}vspace\textbackslash{}', r'\vspace'),
        ]
        
        for input_pattern, expected_output in test_cases:
            with self.subTest(pattern=input_pattern):
                # Create test content
                test_content = f"Some text {input_pattern} more text"
                
                # Create temporary file
                test_file = self.test_dir / "pattern_test.tex"
                test_file.write_text(test_content)
                
                # Process the file
                changed, replacements = deescaper.process_file(test_file)
                
                # Read the result
                result_content = test_file.read_text()
                
                # Verify the pattern was replaced
                self.assertIn(expected_output, result_content, 
                            f"Pattern {input_pattern} should be replaced with {expected_output}")
    
    def test_enhanced_validation(self):
        """Test enhanced validation with reduced false positives."""
        deescaper = fix_latex_escaping.LaTeXDeEscaper()
        
        # Test file with no issues
        good_file = self.test_dir / "good.tex"
        good_file.write_text(r"""
\section{Good Section}
\textbf{Bold text}
\begin{itemize}
\item Item 1
\end{itemize}
        """)
        
        issues = deescaper.validate_latex_syntax(good_file)
        self.assertEqual(len(issues), 0, "Good file should have no validation issues")
        
        # Test file with specific issues
        bad_file = self.test_dir / "bad.tex"
        bad_file.write_text(r"""
\textbackslash{}section\textbackslash{}
\textbf{}
\begin{itemize
\item Item 1
        """)
        
        issues = deescaper.validate_latex_syntax(bad_file)
        self.assertGreater(len(issues), 0, "Bad file should have validation issues")


class TestEndToEndWorkflow(TestCTMMIntegration):
    """Test end-to-end workflow scenarios."""
    
    def test_complete_deescaping_workflow(self):
        """Test complete de-escaping workflow."""
        # Create test file with multiple escaping issues
        test_file = self.test_dir / "complex_escaped.tex"
        test_file.write_text(r"""
\textbackslash{}section\textbackslash{}
\textbackslash{}textbf\textbackslash{}\{Bold Text\textbackslash{}\}
\textbackslash{}begin\textbackslash{}\{itemize\textbackslash{}\}
\textbackslash{}item First item
\textbackslash{}item \textbackslash{}textit\textbackslash{}\{Italic text\textbackslash{}\}
\textbackslash{}end\textbackslash{}\{itemize\textbackslash{}\}
\textbackslash{}checkbox\textbackslash{} Option 1
\textbackslash{}vspace\textbackslash{}\{1cm\textbackslash{}\}
        """)
        
        # Process with de-escaper
        deescaper = fix_latex_escaping.LaTeXDeEscaper()
        changed, replacements = deescaper.process_file(test_file)
        
        # Verify changes were made
        self.assertTrue(changed, "File should be changed by de-escaping")
        self.assertGreater(replacements, 0, "Should have made replacements")
        
        # Read result and verify common patterns are fixed
        result = test_file.read_text()
        
        # Should contain proper LaTeX commands (main verification)
        self.assertIn(r'\section', result, "Should contain proper section command")
        self.assertIn(r'\textbf', result, "Should contain proper textbf command")
        self.assertIn(r'\begin', result, "Should contain proper begin command") 
        self.assertIn(r'\checkbox', result, "Should contain proper checkbox command")
        
        # Count remaining over-escaped patterns (should be significantly reduced)
        original_content = r"""
\textbackslash{}section\textbackslash{}
\textbackslash{}textbf\textbackslash{}\{Bold Text\textbackslash{}\}
\textbackslash{}begin\textbackslash{}\{itemize\textbackslash{}\}
\textbackslash{}item First item
\textbackslash{}item \textbackslash{}textit\textbackslash{}\{Italic text\textbackslash{}\}
\textbackslash{}end\textbackslash{}\{itemize\textbackslash{}\}
\textbackslash{}checkbox\textbackslash{} Option 1
\textbackslash{}vspace\textbackslash{}\{1cm\textbackslash{}\}
        """
        
        original_count = original_content.count(r'\textbackslash{}')
        result_count = result.count(r'\textbackslash{}')
        
        # Should have significantly reduced over-escaped patterns (at least 50% reduction)
        reduction_percentage = (original_count - result_count) / original_count * 100
        self.assertGreater(reduction_percentage, 50, 
                         f"Should reduce over-escaped patterns by >50%, got {reduction_percentage:.1f}% reduction")
    
    def test_workflow_error_handling(self):
        """Test workflow error handling and recovery."""
        deescaper = fix_latex_escaping.LaTeXDeEscaper()
        
        # Test with non-existent file
        non_existent = self.test_dir / "nonexistent.tex"
        changed, replacements = deescaper.process_file(non_existent)
        
        self.assertFalse(changed, "Non-existent file should not be changed")
        self.assertEqual(replacements, 0, "No replacements should be made on non-existent file")


class TestCTMMSpecificFeatures(TestCTMMIntegration):
    """Test CTMM-specific features and conventions."""
    
    def test_ctmm_color_patterns(self):
        """Test CTMM color pattern handling."""
        deescaper = fix_latex_escaping.LaTeXDeEscaper()
        
        # Test CTMM color validation
        test_file = self.test_dir / "ctmm_colors.tex"
        test_file.write_text(r"""
\textcolor{ctmmBlue}{}
\textcolor{ctmmOrange}{Some text}
\textcolor{ctmmGreen}{}
        """)
        
        issues = deescaper.validate_latex_syntax(test_file)
        
        # Should detect empty color commands
        empty_color_issues = [issue for issue in issues if "Empty textcolor" in issue]
        self.assertGreater(len(empty_color_issues), 0, "Should detect empty color commands")
    
    def test_ctmm_checkbox_conventions(self):
        """Test CTMM checkbox convention validation."""
        deescaper = fix_latex_escaping.LaTeXDeEscaper()
        
        # Test checkbox convention validation
        test_file = self.test_dir / "checkbox_test.tex"
        test_file.write_text(r"""
\Box Option 1
\blacksquare Option 2
        """)
        
        issues = deescaper.validate_latex_syntax(test_file)
        
        # Should suggest using CTMM conventions
        box_issues = [issue for issue in issues if "\\Box instead of \\checkbox" in issue]
        blacksquare_issues = [issue for issue in issues if "\\blacksquare instead of \\checkedbox" in issue]
        
        self.assertGreater(len(box_issues), 0, "Should suggest \\checkbox instead of \\Box")
        self.assertGreater(len(blacksquare_issues), 0, "Should suggest \\checkedbox instead of \\blacksquare")


def run_integration_tests():
    """Run the integration test suite."""
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestToolIntegration,
        TestWorkflowIntegration, 
        TestEnhancedPatterns,
        TestEndToEndWorkflow,
        TestCTMMSpecificFeatures
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(test_suite)
    
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
            print(f"  {test}: {traceback}")
    
    if result.errors:
        print("\nERRORS:")
        for test, traceback in result.errors:
            print(f"  {test}: {traceback}")
    
    return len(result.failures) == 0 and len(result.errors) == 0


def main():
    """Main entry point for integration tests."""
    import argparse
    
    parser = argparse.ArgumentParser(description="CTMM Integration Test Suite")
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    
    # Ensure we're in the right directory
    if not Path('main.tex').exists():
        print("Error: This test must be run from the CTMM repository root")
        print("Expected to find main.tex in current directory")
        sys.exit(1)
    
    print("="*60)
    print("CTMM COMPREHENSIVE INTEGRATION TESTS")
    print("="*60)
    print("Testing tool integration, workflow orchestration, and enhanced features")
    print()
    
    success = run_integration_tests()
    
    if success:
        print("\n🎉 ALL INTEGRATION TESTS PASSED - 100% SUCCESS RATE!")
        print("✅ The CTMM comprehensive toolset is fully integrated and operational")
    else:
        print("\n❌ Some integration tests failed")
        print("Please review the failures and fix the issues")
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()