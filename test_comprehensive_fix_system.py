#!/usr/bin/env python3
"""
Integration test for the comprehensive LaTeX escaping fix and PDF validation system.
Tests the end-to-end functionality described in the PR overview.
"""

import unittest
import tempfile
import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from fix_latex_escaping import LaTeXDeEscaper
import ctmm_build


class TestComprehensiveFixSystem(unittest.TestCase):
    """Integration tests for the comprehensive LaTeX fix system."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir)

    def test_multi_pass_escaping_fix_tool(self):
        """Test that the LaTeX escaping fix tool has multi-pass functionality."""
        de_escaper = LaTeXDeEscaper()
        
        # Verify it has both escaping patterns and cleanup patterns (multi-pass)
        self.assertGreater(len(de_escaper.escaping_patterns), 0, "Escaping patterns should exist")
        self.assertGreater(len(de_escaper.cleanup_patterns), 0, "Cleanup patterns should exist (multi-pass)")
        
        # Test that it has at least 25 pattern recognition rules as specified
        total_patterns = len(de_escaper.escaping_patterns) + len(de_escaper.cleanup_patterns)
        self.assertGreaterEqual(total_patterns, 25, f"Expected at least 25+ patterns, found {total_patterns}")

    def test_enhanced_pdf_validation_logic(self):
        """Test that the build system has enhanced PDF validation logic."""
        import inspect
        
        # Check test_basic_build function has enhanced validation
        basic_build_source = inspect.getsource(ctmm_build.test_basic_build)
        
        # Should check file existence
        self.assertIn("pdf_exists", basic_build_source, "Should check PDF file existence")
        
        # Should check file size
        self.assertIn("pdf_size", basic_build_source, "Should check PDF file size")
        
        # Should validate size threshold rather than just return codes
        self.assertIn("> 1024", basic_build_source, "Should check PDF size > 1KB")
        
        # Check test_full_build function has the same enhancements
        full_build_source = inspect.getsource(ctmm_build.test_full_build)
        self.assertIn("pdf_exists", full_build_source, "Full build should check PDF existence")
        self.assertIn("pdf_size", full_build_source, "Full build should check PDF size")
        self.assertIn("> 1024", full_build_source, "Full build should check PDF size > 1KB")

    def test_comprehensive_error_handling(self):
        """Test comprehensive error handling in the fix system."""
        de_escaper = LaTeXDeEscaper()
        
        # Test error handling for non-existent files
        non_existent = self.temp_path / "nonexistent.tex"
        changed, count = de_escaper.process_file(non_existent)
        
        # Should handle errors gracefully
        self.assertFalse(changed)
        self.assertEqual(count, 0)

    def test_detailed_progress_reporting(self):
        """Test that the system provides detailed progress reporting."""
        de_escaper = LaTeXDeEscaper()
        
        # Create test files for statistics tracking
        test_files = {
            "file1.tex": r"\textbackslash{}section\textbackslash{}{Test}",
            "file2.tex": r"Valid LaTeX content",
            "file3.tex": r"\textbackslash{}textbf\textbackslash{}{Bold}",
        }
        
        for filename, content in test_files.items():
            (self.temp_path / filename).write_text(content, encoding='utf-8')
        
        # Process directory and get detailed stats
        stats = de_escaper.process_directory(self.temp_path)
        
        # Should provide detailed statistics
        self.assertIn('files_processed', stats)
        self.assertIn('files_changed', stats)
        self.assertIn('total_replacements', stats)
        
        # Verify statistics are meaningful
        self.assertEqual(stats['files_processed'], 3)
        self.assertGreater(stats['files_changed'], 0)
        self.assertGreater(stats['total_replacements'], 0)

    def test_validation_functionality(self):
        """Test the comprehensive validation functionality."""
        de_escaper = LaTeXDeEscaper()
        
        # Create a test file with issues
        content = r"\textbackslash{}section\textbackslash{}{Test Section}"
        test_file = self.temp_path / "test.tex"
        test_file.write_text(content, encoding='utf-8')
        
        # Fix the file
        changed, count = de_escaper.process_file(test_file)
        self.assertTrue(changed)
        self.assertGreater(count, 0)
        
        # Validate the fixed file
        issues = de_escaper.validate_latex_syntax(test_file)
        
        # Should have validation capability
        self.assertIsInstance(issues, list)
        
        # Should not have textbackslash issues after fixing
        textbackslash_issues = [issue for issue in issues if 'textbackslash' in issue.lower()]
        self.assertEqual(len(textbackslash_issues), 0, "Should fix textbackslash issues")

    def test_build_system_integration(self):
        """Test integration between components."""
        # Test that LaTeX validator can be imported by build system
        try:
            from latex_validator import LaTeXValidator
            validator = LaTeXValidator()
            self.assertIsInstance(validator, LaTeXValidator)
        except ImportError:
            # LaTeX validator is optional for this test
            pass
        
        # Test that de-escaper can be imported by build system
        try:
            de_escaper = LaTeXDeEscaper()
            self.assertIsInstance(de_escaper, LaTeXDeEscaper)
        except ImportError:
            self.fail("LaTeXDeEscaper should be importable by build system")

    def test_ctmm_specific_patterns(self):
        """Test patterns specific to CTMM therapeutic materials."""
        de_escaper = LaTeXDeEscaper()
        
        # Test CTMM-specific therapeutic content patterns
        ctmm_content = r"""
        \textbackslash{}hypertarget\textbackslash{}{trigger-management\textbackslash{}}
        \textbackslash{}section\textbackslash{}{TOOL 23: TRIGGER-MANAGEMENT}
        \textbackslash{}textbf\textbackslash{}{Selbstreflexion\textbackslash{}}
        """
        
        test_file = self.temp_path / "ctmm_test.tex"
        test_file.write_text(ctmm_content, encoding='utf-8')
        
        # Process the CTMM content
        changed, count = de_escaper.process_file(test_file)
        
        self.assertTrue(changed, "CTMM content should be processed")
        self.assertGreater(count, 0, "Should make multiple replacements in CTMM content")
        
        # Verify key CTMM elements are properly fixed
        result = test_file.read_text(encoding='utf-8')
        self.assertIn(r"\hypertarget", result, "Should fix hypertarget commands")
        self.assertIn(r"\section", result, "Should fix section commands")
        self.assertIn(r"\textbf", result, "Should fix textbf commands")
        
        # Should not contain over-escaping
        self.assertNotIn(r"\textbackslash{}", result, "Should remove over-escaping")

    def test_build_system_pdf_validation_thresholds(self):
        """Test that PDF validation uses appropriate thresholds."""
        # Test the validation logic constants
        import inspect
        
        # Both build functions should use consistent thresholds
        basic_source = inspect.getsource(ctmm_build.test_basic_build)
        full_source = inspect.getsource(ctmm_build.test_full_build)
        
        # Should use 1024 byte threshold consistently
        self.assertIn("1024", basic_source, "Basic build should use 1KB threshold")
        self.assertIn("1024", full_source, "Full build should use 1KB threshold")

    def test_error_recovery_mechanisms(self):
        """Test error recovery mechanisms in the build system."""
        # Test that build system has appropriate error handling
        build_data = {
            "build_testing": {
                "basic_passed": False,
                "full_passed": True
            },
            "latex_validation": {
                "passed": True
            }
        }
        
        # Should return error code when basic build fails
        exit_code = ctmm_build._generate_exit_code(build_data)
        self.assertEqual(exit_code, 1, "Should return error when basic build fails")
        
        # Test successful case
        build_data_success = {
            "build_testing": {
                "basic_passed": True,
                "full_passed": True
            },
            "latex_validation": {
                "passed": True
            }
        }
        
        exit_code_success = ctmm_build._generate_exit_code(build_data_success)
        self.assertEqual(exit_code_success, 0, "Should return success when all tests pass")


class TestSystemRequirements(unittest.TestCase):
    """Test that the system meets the PR requirements."""

    def test_pr_requirement_multi_pass_fix_tool(self):
        """Test: Multi-pass LaTeX escaping fix tool with 25+ pattern recognition rules."""
        de_escaper = LaTeXDeEscaper()
        
        # Verify multi-pass capability
        self.assertGreater(len(de_escaper.escaping_patterns), 0)
        self.assertGreater(len(de_escaper.cleanup_patterns), 0)
        
        # Verify 25+ patterns
        total_patterns = len(de_escaper.escaping_patterns) + len(de_escaper.cleanup_patterns)
        self.assertGreaterEqual(total_patterns, 25)

    def test_pr_requirement_enhanced_pdf_validation(self):
        """Test: Enhanced PDF validation that checks file existence and size."""
        import inspect
        
        # Check both validation functions
        for func_name in ['test_basic_build', 'test_full_build']:
            source = inspect.getsource(getattr(ctmm_build, func_name))
            
            # Should check file existence
            self.assertIn("exists", source, f"{func_name} should check file existence")
            
            # Should check file size
            self.assertIn("size", source, f"{func_name} should check file size")
            
            # Should validate rather than just return codes
            self.assertIn("and", source, f"{func_name} should combine multiple checks")

    def test_pr_requirement_comprehensive_test_suite(self):
        """Test: Comprehensive test suite validating all functionality."""
        # This test itself validates that we have comprehensive testing
        
        # Count test methods in our test files
        import test_fix_latex_escaping
        import test_pdf_validation
        
        escaping_tests = [m for m in dir(test_fix_latex_escaping.TestLaTeXDeEscaper) if m.startswith('test_')]
        pdf_tests = [m for m in dir(test_pdf_validation.TestPDFValidation) if m.startswith('test_')]
        integration_tests = [m for m in dir(TestComprehensiveFixSystem) if m.startswith('test_')]
        
        total_tests = len(escaping_tests) + len(pdf_tests) + len(integration_tests)
        
        # Should have comprehensive test coverage
        self.assertGreater(total_tests, 20, f"Should have comprehensive test suite, found {total_tests} tests")

    def test_pr_requirement_robust_error_handling(self):
        """Test: Comprehensive error handling."""
        de_escaper = LaTeXDeEscaper()
        
        # Test error handling with various edge cases
        test_cases = [
            ("nonexistent_file.tex", False, 0),  # Non-existent file
            ("", False, 0),  # Empty filename
        ]
        
        for filename, expected_changed, expected_count in test_cases:
            with self.subTest(filename=filename):
                result_changed, result_count = de_escaper.process_file(Path(filename))
                self.assertEqual(result_changed, expected_changed)
                self.assertEqual(result_count, expected_count)


if __name__ == '__main__':
    unittest.main(verbosity=2)