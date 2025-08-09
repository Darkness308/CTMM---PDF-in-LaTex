#!/usr/bin/env python3
"""
Unit tests for the CTMM Document Converter

Tests conversion functionality and over-escape fixing.
"""

import unittest
import tempfile
import os
from pathlib import Path
import sys

# Add the current directory to the path so we can import the module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from document_converter import DocumentConverter


class TestDocumentConverter(unittest.TestCase):
    """Test cases for DocumentConverter class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.input_dir = Path(self.temp_dir) / "input"
        self.output_dir = Path(self.temp_dir) / "output" 
        self.input_dir.mkdir()
        self.output_dir.mkdir()
        
        self.converter = DocumentConverter(
            input_dir=str(self.input_dir),
            output_dir=str(self.output_dir)
        )
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_over_escape_patterns(self):
        """Test that over-escape patterns are correctly defined."""
        patterns = self.converter.over_escape_patterns
        
        # Check that key patterns are included
        pattern_dict = dict(patterns)
        self.assertIn(r'\\textbackslash\{\}', pattern_dict)
        self.assertEqual(pattern_dict[r'\\textbackslash\{\}'], r'\\')
        
        self.assertIn(r'\\section\\textbackslash\{\}', pattern_dict)
        self.assertEqual(pattern_dict[r'\\section\\textbackslash\{\}'], r'\\section')
    
    def test_fix_over_escaped_latex_simple(self):
        """Test fixing simple over-escaped LaTeX patterns."""
        # Create a test file with over-escaped content
        test_file = self.output_dir / "test.tex"
        over_escaped_content = r"\section\textbackslash{}{Test Title}"
        
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(over_escaped_content)
        
        # Fix the over-escaping
        result = self.converter.fix_over_escaped_latex(test_file)
        self.assertTrue(result)
        
        # Check the fixed content
        with open(test_file, 'r', encoding='utf-8') as f:
            fixed_content = f.read()
        
        self.assertIn(r'\section{Test Title}', fixed_content)
        self.assertNotIn(r'\textbackslash{}', fixed_content)
        
        # Check that backup was created
        backup_file = test_file.with_suffix('.tex.backup')
        self.assertTrue(backup_file.exists())
    
    def test_fix_over_escaped_latex_complex(self):
        """Test fixing complex over-escaped patterns from PR #226."""
        test_file = self.output_dir / "complex_test.tex"
        
        # Example from the original PR
        complex_content = (
            r"\textbackslash{}section\textbackslash{}{" +
            r"\textbackslash{}texorpdfstring\textbackslash{}{" +
            r"📄 \textbackslash{}textbf\textbackslash{}{TOOL 23: TRIGGER-MANAGEMENT\textbackslash{}}" +
            r"\textbackslash{}}\textbackslash{}{📄 TOOL 23: TRIGGER-MANAGEMENT\textbackslash{}}" +
            r"\textbackslash{}}\textbackslash{}label\textbackslash{}{tool-23-trigger-management\textbackslash{}}\textbackslash{}}"
        )
        
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(complex_content)
        
        result = self.converter.fix_over_escaped_latex(test_file)
        self.assertTrue(result)
        
        with open(test_file, 'r', encoding='utf-8') as f:
            fixed_content = f.read()
        
        # Should be much cleaner now
        self.assertIn(r'\section', fixed_content)
        self.assertIn(r'\texorpdfstring', fixed_content)
        self.assertIn(r'\textbf', fixed_content)
        self.assertIn(r'\label', fixed_content)
        # Should not contain the over-escaped patterns
        self.assertNotIn(r'\textbackslash{}', fixed_content)
    
    def test_fix_clean_latex_file(self):
        """Test that clean LaTeX files are not modified unnecessarily."""
        test_file = self.output_dir / "clean_test.tex"
        clean_content = r"\section{Clean Title}" + "\n" + r"\subsection{Clean Subtitle}"
        
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(clean_content)
        
        result = self.converter.fix_over_escaped_latex(test_file)
        self.assertFalse(result)  # Should return False if no changes were made
        
        with open(test_file, 'r', encoding='utf-8') as f:
            unchanged_content = f.read()
        
        self.assertEqual(clean_content, unchanged_content)
        
        # No backup should be created for clean files
        backup_file = test_file.with_suffix('.tex.backup')
        self.assertFalse(backup_file.exists())
    
    def test_post_process_latex(self):
        """Test LaTeX post-processing functionality."""
        test_file = self.output_dir / "postprocess_test.tex"
        
        # Simulate pandoc output with document class
        pandoc_content = """\\documentclass{article}
\\usepackage[ngerman]{babel}
\\begin{document}
\\section{Test Section}
Content here
\\end{document}"""
        
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(pandoc_content)
        
        self.converter.post_process_latex(test_file)
        
        with open(test_file, 'r', encoding='utf-8') as f:
            processed_content = f.read()
        
        # Should remove document class and document environment
        self.assertNotIn(r'\documentclass', processed_content)
        self.assertNotIn(r'\begin{document}', processed_content)
        self.assertNotIn(r'\end{document}', processed_content)
        
        # Should add CTMM header
        self.assertIn('CTMM Therapy Module:', processed_content)
        self.assertIn('document_converter.py', processed_content)
        
        # Should preserve the actual content
        self.assertIn(r'\section{Test Section}', processed_content)
        self.assertIn('Content here', processed_content)
    
    def test_ensure_output_dir(self):
        """Test output directory creation."""
        new_output_dir = Path(self.temp_dir) / "new_output"
        converter = DocumentConverter(
            input_dir=str(self.input_dir),
            output_dir=str(new_output_dir)
        )
        
        self.assertFalse(new_output_dir.exists())
        converter.ensure_output_dir()
        self.assertTrue(new_output_dir.exists())


class TestDocumentConverterIntegration(unittest.TestCase):
    """Integration tests for document converter functionality."""
    
    def test_converter_handles_empty_input_directory(self):
        """Test that converter handles empty input directories gracefully."""
        with tempfile.TemporaryDirectory() as temp_dir:
            input_dir = Path(temp_dir) / "empty_input"
            output_dir = Path(temp_dir) / "output"
            input_dir.mkdir()
            
            converter = DocumentConverter(str(input_dir), str(output_dir))
            result = converter.convert_all_docx()
            
            # Should return True even with no files to convert
            self.assertTrue(result)
    
    def test_converter_handles_nonexistent_input_directory(self):
        """Test that converter handles non-existent input directories."""
        with tempfile.TemporaryDirectory() as temp_dir:
            input_dir = Path(temp_dir) / "nonexistent"
            output_dir = Path(temp_dir) / "output"
            
            converter = DocumentConverter(str(input_dir), str(output_dir))
            result = converter.convert_all_docx()
            
            # Should return False for non-existent directory
            self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()