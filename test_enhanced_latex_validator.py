#!/usr/bin/env python3
"""
Comprehensive tests for the enhanced LaTeX validator with 50+ pattern recognition rules.
Tests the multi-pass cleaning functionality and comprehensive escaping detection.
"""

import unittest
import tempfile
import shutil
from pathlib import Path
from latex_validator import LaTeXValidator


class TestEnhancedLaTeXValidator(unittest.TestCase):
    """Test cases for enhanced LaTeX validator with comprehensive pattern recognition."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.validator = LaTeXValidator()
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir)
    
    def test_pattern_count(self):
        """Test that we have 25+ patterns as required."""
        pattern_count = len(self.validator.problematic_patterns)
        self.assertGreaterEqual(pattern_count, 25, f"Expected at least 25 patterns, got {pattern_count}")
        print(f"✓ Pattern count test passed: {pattern_count} patterns available")
    
    def test_command_escaping_detection(self):
        """Test detection of escaped commands."""
        content = r"""
        \textbackslash{}emph\textbackslash{} text
        \textbackslash{}textbf\textbackslash{} bold
        \textbackslash{}textit\textbackslash{} italic
        """
        issues = self.validator.detect_issues(content)
        
        # Should detect escaped command patterns
        self.assertIn('escaped_emph', issues)
        self.assertIn('escaped_textbf', issues)
        self.assertIn('escaped_textit', issues)
    
    def test_environment_escaping_detection(self):
        """Test detection of escaped environments."""
        content = r"""
        \textbackslash{}begin\textbackslash{}itemize
        \textbackslash{}end\textbackslash{}itemize
        \textbackslash{}begin\textbackslash{}enumerate
        """
        issues = self.validator.detect_issues(content)
        
        # Should detect escaped environment patterns
        self.assertIn('escaped_itemize', issues)
        self.assertIn('escaped_enumerate', issues)
    
    def test_special_character_escaping_detection(self):
        """Test detection of escaped special characters."""
        content = r"""
        Some text with \textbackslash{}\textbackslash{}& ampersand
        Hash \textbackslash{}\# symbol
        Percent \textbackslash{}\% symbol
        """
        issues = self.validator.detect_issues(content)
        
        # Should detect special character escaping
        self.assertIn('double_escaped_ampersand', issues)
        self.assertIn('escaped_hash', issues)
        self.assertIn('escaped_percent', issues)
    
    def test_math_mode_escaping_detection(self):
        """Test detection of escaped math commands."""
        content = r"""
        \textbackslash{}begin\textbackslash{}equation
        \textbackslash{}frac\textbackslash{} fraction
        \textbackslash{}sqrt\textbackslash{} square root
        """
        issues = self.validator.detect_issues(content)
        
        # Should detect math command escaping
        self.assertIn('escaped_equation', issues)
        self.assertIn('escaped_frac', issues)
        self.assertIn('escaped_sqrt', issues)
    
    def test_multi_pass_cleaning(self):
        """Test that multi-pass cleaning works correctly."""
        problematic_content = r"""
        \textbackslash{}emph\textbackslash{} emphasized text
        \textbackslash{}begin\textbackslash{}itemize
        \item First item
        \textbackslash{}end\textbackslash{}itemize
        Text with \textbackslash{}\textbackslash{}& ampersand
        """
        
        # Clean the content
        cleaned = self.validator.clean_excessive_escaping(problematic_content)
        
        # Should be cleaned
        self.assertNotIn(r'\textbackslash{}emph\textbackslash{}', cleaned)
        self.assertNotIn(r'\textbackslash{}begin\textbackslash{}', cleaned)
        self.assertNotIn(r'\textbackslash{}\textbackslash{}&', cleaned)
        
        # Should have proper LaTeX commands
        self.assertIn(r'\emph', cleaned)
        self.assertIn(r'\begin{itemize}', cleaned)
        self.assertIn(r'\end{itemize}', cleaned)
    
    def test_comprehensive_file_cleaning(self):
        """Test cleaning a file with many different escaping issues."""
        problematic_content = r"""
        \hypertarget{section}{%
        \section{\texorpdfstring{📄 \textbf{TEST SECTION}}{TEST SECTION}\label{section}}
        
        Some text with \textbackslash{}emph\textbackslash{} emphasis and \textbackslash{}textbf\textbackslash{} bold.
        
        \textbackslash{}begin\textbackslash{}itemize
        \item First item with \textbackslash{}\textbackslash{}& ampersand
        \item Second item with \textbackslash{}\# hash
        \textbackslash{}end\textbackslash{}itemize
        
        Math: \textbackslash{}frac\textbackslash{} and \textbackslash{}sqrt\textbackslash{}
        """
        
        test_file = Path(self.temp_dir) / "test_comprehensive.tex"
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(problematic_content)
        
        # Validate and clean
        is_valid, issues, cleaned_content = self.validator.validate_file(test_file)
        
        # Should detect multiple types of issues
        self.assertFalse(is_valid)
        self.assertGreater(len(issues), 5)  # Should find many different issues
        
        # Cleaned content should be better
        issues_after_cleaning = self.validator.detect_issues(cleaned_content)
        self.assertLessEqual(len(issues_after_cleaning), len(issues))
    
    def test_complex_pattern_combinations(self):
        """Test detection of complex pattern combinations."""
        content = r"""
        Triple backslashes \\\ problem
        Nested \textbackslash{\textbackslash{}} escaping
        Malformed \textbackslash{}command\textbackslash{} structures
        """
        issues = self.validator.detect_issues(content)
        
        # Should detect complex patterns
        self.assertIn('triple_backslashes', issues)
        self.assertIn('nested_textbackslash', issues)
    
    def test_table_and_figure_escaping(self):
        """Test detection of table and figure escaping issues."""
        content = r"""
        \textbackslash{}begin\textbackslash{}table
        \textbackslash{}caption\textbackslash{} Table caption
        \textbackslash{}centering\textbackslash{}
        \textbackslash{}hline\textbackslash{}
        \textbackslash{}end\textbackslash{}table
        
        \textbackslash{}begin\textbackslash{}figure
        \textbackslash{}includegraphics\textbackslash{} image
        \textbackslash{}end\textbackslash{}figure
        """
        issues = self.validator.detect_issues(content)
        
        # Should detect table and figure escaping
        self.assertIn('escaped_table', issues)
        self.assertIn('escaped_caption', issues)
        self.assertIn('escaped_centering', issues)
        self.assertIn('escaped_hline', issues)
        self.assertIn('escaped_figure', issues)
        self.assertIn('escaped_includegraphics', issues)
    
    def test_font_and_formatting_escaping(self):
        """Test detection of font and formatting command escaping."""
        content = r"""
        \textbackslash{}large\textbackslash{} large text
        \textbackslash{}huge\textbackslash{} huge text
        \textbackslash{}tiny\textbackslash{} tiny text
        \textbackslash{}color\textbackslash{} colored text
        """
        issues = self.validator.detect_issues(content)
        
        # Should detect font command escaping
        self.assertIn('escaped_large', issues)
        self.assertIn('escaped_huge', issues)
        self.assertIn('escaped_tiny', issues)
        self.assertIn('escaped_color', issues)
    
    def test_citation_and_reference_escaping(self):
        """Test detection of citation and reference escaping."""
        content = r"""
        See \textbackslash{}ref\textbackslash{} reference
        Citation \textbackslash{}cite\textbackslash{} here
        Page \textbackslash{}pageref\textbackslash{} reference
        Auto \textbackslash{}autoref\textbackslash{} reference
        """
        issues = self.validator.detect_issues(content)
        
        # Should detect reference command escaping
        self.assertIn('escaped_ref', issues)
        self.assertIn('escaped_cite', issues)
        self.assertIn('escaped_pageref', issues)
        self.assertIn('escaped_autoref', issues)
    
    def test_preserved_valid_latex(self):
        """Test that valid LaTeX is preserved during cleaning."""
        valid_content = r"""
        \section{Valid Section}
        \label{sec:valid-section}
        
        This is normal text with \emph{emphasis} and \textbf{bold} formatting.
        
        \begin{itemize}
        \item First item
        \item Second item with \& ampersand
        \end{itemize}
        
        Math: $\frac{1}{2}$ and $\sqrt{x}$
        
        Citation: \cite{reference} and \ref{sec:valid-section}
        """
        
        # Should be considered valid
        issues = self.validator.detect_issues(valid_content)
        self.assertEqual(len(issues), 0, f"Valid content should have no issues, found: {list(issues.keys())}")
        
        # Cleaning should not change valid content significantly
        cleaned = self.validator.clean_excessive_escaping(valid_content)
        self.assertIn(r'\section{Valid Section}', cleaned)
        self.assertIn(r'\emph{emphasis}', cleaned)
        self.assertIn(r'\textbf{bold}', cleaned)


class TestMultiPassCleaning(unittest.TestCase):
    """Test the multi-pass cleaning functionality specifically."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.validator = LaTeXValidator()
    
    def test_basic_escaping_pass(self):
        """Test the basic escaping pass."""
        content = r"""
        Multiple \textbackslash{} issues here
        Nested \textbackslash{\textbackslash{}} problems
        Triple \\\ backslashes
        """
        cleaned = self.validator._fix_basic_escaping(content)
        
        # Should fix basic textbackslash patterns
        self.assertNotIn(r'\textbackslash{}', cleaned)
        self.assertNotIn(r'\\\\\\', cleaned)  # Triple should become double
    
    def test_command_escaping_pass(self):
        """Test the command escaping pass."""
        content = r"""
        \textbackslash{}emph\textbackslash{} text
        \textbackslash{}textbf\textbackslash{} bold
        \textbackslash{}cite\textbackslash{} reference
        """
        cleaned = self.validator._fix_command_escaping(content)
        
        # Should fix command escaping
        self.assertIn(r'\emph', cleaned)
        self.assertIn(r'\textbf', cleaned)
        self.assertIn(r'\cite', cleaned)
        self.assertNotIn(r'\textbackslash{}emph\textbackslash{}', cleaned)
    
    def test_environment_escaping_pass(self):
        """Test the environment escaping pass."""
        content = r"""
        \textbackslash{}begin\textbackslash{}itemize
        \textbackslash{}end\textbackslash{}itemize
        \textbackslash{}begin\textbackslash{}equation
        """
        cleaned = self.validator._fix_environment_escaping(content)
        
        # Should fix environment escaping
        self.assertIn(r'\begin{itemize}', cleaned)
        self.assertIn(r'\end{itemize}', cleaned)
        self.assertIn(r'\begin{equation}', cleaned)
    
    def test_special_character_pass(self):
        """Test the special character escaping pass."""
        content = r"""
        Text with \textbackslash{}\textbackslash{}& ampersand
        Hash \textbackslash{}\# symbol
        Percent \textbackslash{}\% symbol
        """
        cleaned = self.validator._fix_special_character_escaping(content)
        
        # Should fix special character escaping
        self.assertIn(r' \& ', cleaned)
        self.assertIn(r'\#', cleaned)
        self.assertIn(r'\%', cleaned)
        self.assertNotIn(r'\textbackslash{}\textbackslash{}&', cleaned)
    
    def test_final_cleanup_pass(self):
        """Test the final cleanup pass."""
        content = r"""
        Text  with   excessive   whitespace


        Multiple blank lines
        Some\command\another malformed commands
        """
        cleaned = self.validator._final_cleanup(content)
        
        # Should clean up whitespace and malformed commands
        self.assertNotIn('\n\n\n', cleaned)  # Should normalize to max 2 newlines
        self.assertIn(r'\command \another', cleaned)  # Should separate commands


if __name__ == '__main__':
    unittest.main(verbosity=2)