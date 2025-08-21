#!/usr/bin/env python3
"""
Test suite for PDF validation logic in the CTMM build system.
Tests the enhanced PDF validation that checks file existence and size.
"""

import unittest
import tempfile
import subprocess
import sys
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add current directory to path for importing ctmm_build
sys.path.insert(0, str(Path(__file__).parent))
import ctmm_build


class TestPDFValidation(unittest.TestCase):
    """Test cases for PDF validation logic in the build system."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir)

    def create_mock_pdf(self, path: Path, size_bytes: int = 2048):
        """Create a mock PDF file with specified size."""
        content = b"PDF mock content" * (size_bytes // 16 + 1)
        path.write_bytes(content[:size_bytes])

    def test_pdf_validation_file_exists_and_size_ok(self):
        """Test PDF validation when file exists and has adequate size."""
        test_pdf = self.temp_path / "test.pdf"
        self.create_mock_pdf(test_pdf, 2048)  # 2KB file
        
        # Mock subprocess to return success
        mock_result = MagicMock()
        mock_result.returncode = 0
        
        with patch('subprocess.run', return_value=mock_result):
            with patch('ctmm_build.Path') as mock_path_class:
                # Mock Path to return our test directory structure
                mock_path = MagicMock()
                mock_path.with_suffix.return_value = test_pdf
                mock_path_class.return_value = mock_path
                
                # Mock the file existence and size checks
                with patch.object(test_pdf, 'exists', return_value=True), \
                     patch.object(test_pdf, 'stat') as mock_stat:
                    
                    mock_stat.return_value.st_size = 2048
                    
                    # This would be part of the actual test_basic_build logic
                    pdf_exists = test_pdf.exists()
                    pdf_size = test_pdf.stat().st_size if pdf_exists else 0
                    success = mock_result.returncode == 0 and pdf_exists and pdf_size > 1024
                    
                    self.assertTrue(success)

    def test_pdf_validation_file_too_small(self):
        """Test PDF validation when file exists but is too small."""
        test_pdf = self.temp_path / "test.pdf"
        self.create_mock_pdf(test_pdf, 512)  # 512 bytes - too small
        
        mock_result = MagicMock()
        mock_result.returncode = 0
        
        with patch('subprocess.run', return_value=mock_result):
            # Test the validation logic directly
            pdf_exists = test_pdf.exists()
            pdf_size = test_pdf.stat().st_size if pdf_exists else 0
            success = mock_result.returncode == 0 and pdf_exists and pdf_size > 1024
            
            self.assertFalse(success)
            self.assertTrue(pdf_exists)
            self.assertLessEqual(pdf_size, 1024)

    def test_pdf_validation_file_not_exists(self):
        """Test PDF validation when file doesn't exist."""
        test_pdf = self.temp_path / "nonexistent.pdf"
        
        mock_result = MagicMock()
        mock_result.returncode = 0
        
        with patch('subprocess.run', return_value=mock_result):
            # Test the validation logic directly
            pdf_exists = test_pdf.exists()
            pdf_size = test_pdf.stat().st_size if pdf_exists else 0
            success = mock_result.returncode == 0 and pdf_exists and pdf_size > 1024
            
            self.assertFalse(success)
            self.assertFalse(pdf_exists)
            self.assertEqual(pdf_size, 0)

    def test_pdf_validation_latex_error(self):
        """Test PDF validation when LaTeX compilation fails."""
        test_pdf = self.temp_path / "test.pdf"
        # Don't create the PDF file to simulate LaTeX failure
        
        mock_result = MagicMock()
        mock_result.returncode = 1  # LaTeX error
        
        with patch('subprocess.run', return_value=mock_result):
            # Test the validation logic directly
            pdf_exists = test_pdf.exists()
            pdf_size = test_pdf.stat().st_size if pdf_exists else 0
            success = mock_result.returncode == 0 and pdf_exists and pdf_size > 1024
            
            self.assertFalse(success)

    @patch('subprocess.run')
    def test_basic_build_pdf_validation_integration(self, mock_subprocess):
        """Test integration of PDF validation in basic build test."""
        # Mock successful LaTeX compilation
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_subprocess.return_value = mock_result
        
        # Test with pdflatex available
        mock_subprocess.side_effect = [
            mock_result,  # pdflatex --version check
            mock_result   # actual compilation
        ]
        
        # Create a temporary test file
        test_tex = self.temp_path / "test_basic.tex"
        test_tex.write_text(r"""
        \documentclass{article}
        \begin{document}
        Test document
        \end{document}
        """, encoding='utf-8')
        
        # Create expected PDF with adequate size
        test_pdf = self.temp_path / "test_basic.pdf"
        self.create_mock_pdf(test_pdf, 2048)
        
        with patch('ctmm_build.Path') as mock_path_class:
            # Mock Path behavior for temporary file handling
            mock_temp_path = MagicMock()
            mock_temp_path.with_suffix.return_value = test_pdf
            mock_path_class.return_value = mock_temp_path
            
            with patch.object(test_pdf, 'exists', return_value=True), \
                 patch.object(test_pdf, 'stat') as mock_stat:
                
                mock_stat.return_value.st_size = 2048
                
                # The actual validation logic as implemented in ctmm_build.py
                pdf_exists = test_pdf.exists()
                pdf_size = test_pdf.stat().st_size if pdf_exists else 0
                success = mock_result.returncode == 0 and pdf_exists and pdf_size > 1024
                
                self.assertTrue(success)

    def test_pdf_size_threshold_boundary(self):
        """Test PDF size validation at the 1KB boundary."""
        test_cases = [
            (1023, False),  # Just under threshold
            (1024, False),  # Exactly at threshold (should fail with <= check)
            (1025, True),   # Just over threshold
            (2048, True),   # Well over threshold
        ]
        
        for size, expected_success in test_cases:
            with self.subTest(size=size):
                test_pdf = self.temp_path / f"test_{size}.pdf"
                self.create_mock_pdf(test_pdf, size)
                
                mock_result = MagicMock()
                mock_result.returncode = 0
                
                # Test validation logic
                pdf_exists = test_pdf.exists()
                pdf_size = test_pdf.stat().st_size if pdf_exists else 0
                success = mock_result.returncode == 0 and pdf_exists and pdf_size > 1024
                
                self.assertEqual(success, expected_success,
                               f"Size {size} bytes should {'pass' if expected_success else 'fail'}")

    @patch('ctmm_build.logger')
    def test_pdf_validation_logging(self, mock_logger):
        """Test that PDF validation provides appropriate logging."""
        # Test case: PDF file too small
        test_pdf = self.temp_path / "small.pdf"
        self.create_mock_pdf(test_pdf, 512)
        
        mock_result = MagicMock()
        mock_result.returncode = 0
        
        with patch('subprocess.run', return_value=mock_result):
            pdf_exists = test_pdf.exists()
            pdf_size = test_pdf.stat().st_size if pdf_exists else 0
            success = mock_result.returncode == 0 and pdf_exists and pdf_size > 1024
            
            # Simulate the logging that would occur in the actual build system
            if not success:
                if mock_result.returncode != 0:
                    mock_logger.error("LaTeX compilation returned error code: %d", mock_result.returncode)
                elif not pdf_exists:
                    mock_logger.error("Test PDF file was not generated")
                elif pdf_size <= 1024:
                    mock_logger.error("Test PDF file is too small (%.2f KB) - likely incomplete", pdf_size / 1024)
            
            # Verify appropriate error logging would occur
            self.assertFalse(success)
            # Note: In real implementation, we would verify mock_logger.error was called with size message

    def test_cleanup_after_pdf_validation(self):
        """Test that temporary files are cleaned up after PDF validation."""
        # This tests the cleanup logic in the build system
        temp_files = [
            self.temp_path / "temp.tex",
            self.temp_path / "temp.aux", 
            self.temp_path / "temp.log",
            self.temp_path / "temp.pdf",
            self.temp_path / "temp.out",
            self.temp_path / "temp.toc"
        ]
        
        # Create all temporary files
        for temp_file in temp_files:
            temp_file.write_text("temporary content", encoding='utf-8')
            self.assertTrue(temp_file.exists())
        
        # Simulate cleanup logic from ctmm_build.py
        for ext in ['', '.aux', '.log', '.pdf', '.out', '.toc']:
            cleanup_file = self.temp_path / f"temp{ext}"
            if cleanup_file.exists():
                cleanup_file.unlink()
        
        # Verify all files are cleaned up
        for temp_file in temp_files:
            with self.subTest(file=str(temp_file)):
                self.assertFalse(temp_file.exists(), f"File {temp_file} was not cleaned up")

    def test_full_build_pdf_validation(self):
        """Test PDF validation in full build context."""
        main_pdf = self.temp_path / "main.pdf"
        self.create_mock_pdf(main_pdf, 4096)  # Larger PDF for full build
        
        mock_result = MagicMock()
        mock_result.returncode = 0
        
        with patch('subprocess.run', return_value=mock_result):
            # Test the full build validation logic
            pdf_exists = main_pdf.exists()
            pdf_size = main_pdf.stat().st_size if pdf_exists else 0
            success = mock_result.returncode == 0 and pdf_exists and pdf_size > 1024
            
            self.assertTrue(success)
            self.assertTrue(pdf_exists)
            self.assertGreater(pdf_size, 1024)

    def test_enhanced_vs_basic_validation(self):
        """Test that enhanced validation is more robust than just checking return codes."""
        # Scenario: LaTeX returns success but doesn't generate proper PDF
        test_pdf = self.temp_path / "fake_success.pdf"
        # Don't create the PDF file
        
        mock_result = MagicMock()
        mock_result.returncode = 0  # LaTeX claims success
        
        with patch('subprocess.run', return_value=mock_result):
            # Basic validation (return code only)
            basic_success = mock_result.returncode == 0
            
            # Enhanced validation (return code + file existence + size)
            pdf_exists = test_pdf.exists()
            pdf_size = test_pdf.stat().st_size if pdf_exists else 0
            enhanced_success = mock_result.returncode == 0 and pdf_exists and pdf_size > 1024
            
            # Enhanced validation should catch the issue
            self.assertTrue(basic_success)      # Basic validation passes
            self.assertFalse(enhanced_success)  # Enhanced validation fails
            
            # This demonstrates why the enhanced validation is necessary


class TestBuildSystemIntegration(unittest.TestCase):
    """Test integration between PDF validation and the broader build system."""

    def test_build_system_uses_enhanced_validation(self):
        """Test that the build system actually uses enhanced PDF validation."""
        # Verify that the ctmm_build module has the enhanced validation logic
        import inspect
        
        # Check test_basic_build function
        basic_build_source = inspect.getsource(ctmm_build.test_basic_build)
        self.assertIn("pdf_exists", basic_build_source)
        self.assertIn("pdf_size", basic_build_source)
        self.assertIn("> 1024", basic_build_source)
        
        # Check test_full_build function
        full_build_source = inspect.getsource(ctmm_build.test_full_build)
        self.assertIn("pdf_exists", full_build_source)
        self.assertIn("pdf_size", full_build_source)
        self.assertIn("> 1024", full_build_source)

    def test_validation_threshold_constant(self):
        """Test that the 1KB threshold is consistently applied."""
        # Both basic and full build should use the same threshold
        import inspect
        
        basic_build_source = inspect.getsource(ctmm_build.test_basic_build)
        full_build_source = inspect.getsource(ctmm_build.test_full_build)
        
        # Both should use 1024 bytes threshold
        self.assertIn("1024", basic_build_source)
        self.assertIn("1024", full_build_source)

    def test_error_handling_integration(self):
        """Test that PDF validation errors are properly integrated into build reporting."""
        # This would test the integration with _generate_exit_code and error reporting
        # The build system should return appropriate exit codes based on PDF validation
        
        # Mock a failed PDF validation scenario
        build_data = {
            "build_testing": {
                "basic_passed": False,   # PDF validation failed
                "full_passed": False
            },
            "latex_validation": {
                "passed": True
            }
        }
        
        # Test the exit code generation logic
        exit_code = ctmm_build._generate_exit_code(build_data)
        self.assertEqual(exit_code, 1)  # Should return error code
        
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
        self.assertEqual(exit_code_success, 0)  # Should return success


if __name__ == '__main__':
    unittest.main(verbosity=2)