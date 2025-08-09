#!/usr/bin/env python3
"""
Unit tests for the LaTeX escaping fix functionality.
Tests the fix for the over-escaping issue identified in PR #3.
"""

import unittest
import tempfile
import os
from pathlib import Path
import sys

# Add scripts directory to path to import our modules
script_dir = Path(__file__).parent / 'scripts'
sys.path.insert(0, str(script_dir))

from scripts.fix_latex_escaping import clean_latex_escaping, fix_existing_latex_file


class TestLatexEscapingFix(unittest.TestCase):
    """Test cases for LaTeX escaping fix functionality."""
    
    def test_basic_textbackslash_replacement(self):
        """Test basic \textbackslash{} replacement."""
        input_text = r"\textbackslash{}section"
        expected = r"\section"
        result = clean_latex_escaping(input_text)
        self.assertEqual(result, expected)
    
    def test_complex_command_fix(self):
        """Test fixing complex over-escaped LaTeX commands."""
        input_text = r"\textbackslash{}hypertarget\textbackslash{}{tool-23\textbackslash{}}\textbackslash{}{\textbackslash{}%"
        expected = r"\hypertarget{tool-23}{%"  # Our fix correctly converts {\% to {% 
        result = clean_latex_escaping(input_text)
        self.assertEqual(result, expected)
    
    def test_multiple_commands_fix(self):
        """Test fixing multiple over-escaped commands in one text."""
        input_text = r"""
        \textbackslash{}section\textbackslash{}{Title\textbackslash{}}
        \textbackslash{}begin\textbackslash{}{itemize\textbackslash{}}
        \textbackslash{}item Some text
        \textbackslash{}end\textbackslash{}{itemize\textbackslash{}}
        """
        
        result = clean_latex_escaping(input_text)
        
        # Check that all the problematic patterns are fixed
        self.assertNotIn(r'\textbackslash{}', result)
        self.assertIn(r'\section{Title}', result)
        self.assertIn(r'\begin{itemize}', result)
        self.assertIn(r'\end{itemize}', result)
    
    def test_tool_23_example_fix(self):
        """Test fixing the actual Tool 23 example from the PR comments."""
        input_text = r"""\textbackslash{}hypertarget\textbackslash{}{tool-23-trigger-management\textbackslash{}}\textbackslash{}{\textbackslash{}%
\textbackslash{}section\textbackslash{}{\textbackslash{}texorpdfstring\textbackslash{}{📄 \textbackslash{}textbf\textbackslash{}{TOOL 23: TRIGGER-MANAGEMENT\textbackslash{}}\textbackslash{}}\textbackslash{}{📄 TOOL 23: TRIGGER-MANAGEMENT\textbackslash{}}\textbackslash{}}\textbackslash{}label\textbackslash{}{tool-23-trigger-management\textbackslash{}}\textbackslash{}}

🧩 \textbackslash{}emph\textbackslash{}{\textbackslash{}textbf\textbackslash{}{Modul zur Selbsthilfe \textbackslash{}\textbackslash{}& Co-Regulation -- Klartextversion für beide Partner\textbackslash{}}\textbackslash{}}"""
        
        result = clean_latex_escaping(input_text)
        
        # Verify the result contains proper LaTeX commands
        self.assertIn(r'\hypertarget{tool-23-trigger-management}{%', result)
        self.assertIn(r'\section{\texorpdfstring{📄 \textbf{TOOL 23: TRIGGER-MANAGEMENT}}{📄 TOOL 23: TRIGGER-MANAGEMENT}}\label{tool-23-trigger-management}}', result)
        self.assertIn(r'\emph{\textbf{Modul zur Selbsthilfe \\& Co-Regulation -- Klartextversion für beide Partner}}', result)
        
        # Verify no over-escaping remains
        self.assertNotIn(r'\textbackslash{}', result)
    
    def test_safe_words_example_fix(self):
        """Test fixing the Tool 22 Safe Words example from the PR comments."""
        input_text = r"""\textbackslash{}hypertarget\textbackslash{}{tool-22-safe-words-signalsysteme-ctmm-modul\textbackslash{}}\textbackslash{}{\textbackslash{}%
\textbackslash{}section\textbackslash{}{\textbackslash{}texorpdfstring\textbackslash{}{\textbackslash{}textbf\textbackslash{}{🛑 TOOL 22 -- SAFE-WORDS \textbackslash{}\textbackslash{}& SIGNALSYSTEME (CTMM-MODUL)\textbackslash{}}\textbackslash{}}\textbackslash{}{🛑 TOOL 22 -- SAFE-WORDS \textbackslash{}\textbackslash{}& SIGNALSYSTEME (CTMM-MODUL)\textbackslash{}}\textbackslash{}}\textbackslash{}label\textbackslash{}{tool-22-safe-words-signalsysteme-ctmm-modul\textbackslash{}}\textbackslash{}}

\textbackslash{}begin\textbackslash{}{quote\textbackslash{}}
🧠 \textbackslash{}textbf\textbackslash{}{\textbackslash{}ul\textbackslash{}{Worum geht's hier -- für Freunde?\textbackslash{}}\textbackslash{}}\textbackslash{}\textbackslash{}
Safe-Words sind vereinbarte Codes oder Zeichen, die sofort signalisieren:
\textbackslash{}end\textbackslash{}{quote\textbackslash{}}"""
        
        result = clean_latex_escaping(input_text)
        
        # Check for proper LaTeX formatting
        self.assertIn(r'\hypertarget{tool-22-safe-words-signalsysteme-ctmm-modul}{%', result)
        self.assertIn(r'\begin{quote}', result)
        self.assertIn(r'\end{quote}', result)
        self.assertIn(r"\textbf{\ul{Worum geht's hier -- für Freunde?}}", result)  # Regular apostrophe
        
        # Verify no over-escaping remains
        self.assertNotIn(r'\textbackslash{}', result)
    
    def test_readme_example_fix(self):
        """Test fixing the README example from the PR comments."""
        input_text = r"""\textbackslash{}hypertarget\textbackslash{}{ctmm-system\textbackslash{}}\textbackslash{}{\textbackslash{}%
\textbackslash{}section\textbackslash{}{CTMM-System\textbackslash{}}\textbackslash{}label\textbackslash{}{ctmm-system\textbackslash{}}\textbackslash{}}

Ein modulares LaTeX-Framework für Catch-Track-Map-Match Therapiematerialien.

\textbackslash{}hypertarget\textbackslash{}{uxfcberblick\textbackslash{}}\textbackslash{}{\textbackslash{}%
\textbackslash{}subsection\textbackslash{}{Überblick\textbackslash{}}\textbackslash{}label\textbackslash{}{uxfcberblick\textbackslash{}}\textbackslash{}}"""
        
        result = clean_latex_escaping(input_text)
        
        # Check for proper LaTeX formatting
        self.assertIn(r'\hypertarget{ctmm-system}{%', result)
        self.assertIn(r'\section{CTMM-System}\label{ctmm-system}}', result)
        self.assertIn(r'\subsection{Überblick}\label{uxfcberblick}}', result)
        
        # Verify no over-escaping remains
        self.assertNotIn(r'\textbackslash{}', result)
    
    def test_clean_text_unchanged(self):
        """Test that properly formatted LaTeX is not changed."""
        input_text = r"""
        \section{Proper Section}
        \begin{itemize}
        \item First item
        \item Second item
        \end{itemize}
        \textbf{Bold text} and \emph{emphasized text}.
        """
        
        result = clean_latex_escaping(input_text)
        self.assertEqual(result, input_text)
    
    def test_file_fix_functionality(self):
        """Test the file fixing functionality."""
        # Create a temporary file with over-escaped content
        with tempfile.NamedTemporaryFile(mode='w', suffix='.tex', delete=False) as f:
            test_content = r"\textbackslash{}section\textbackslash{}{Test Section\textbackslash{}}"
            f.write(test_content)
            temp_file_path = f.name
        
        try:
            # Fix the file
            result = fix_existing_latex_file(temp_file_path)
            self.assertTrue(result)
            
            # Read the fixed content
            with open(temp_file_path, 'r') as f:
                fixed_content = f.read()
            
            # Verify the fix
            self.assertEqual(fixed_content, r"\section{Test Section}")
            self.assertNotIn(r'\textbackslash{}', fixed_content)
            
            # Verify backup was created
            backup_path = temp_file_path + '.backup'
            self.assertTrue(os.path.exists(backup_path))
            
            # Clean up backup
            os.unlink(backup_path)
            
        finally:
            # Clean up
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)