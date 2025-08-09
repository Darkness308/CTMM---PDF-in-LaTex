#!/usr/bin/env python3
"""
Test suite for the over-escaping fix tool.
"""

import unittest
import tempfile
import os
from pathlib import Path
import sys

# Add the current directory to Python path to import the fix tool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fix_over_escaping import fix_over_escaping


class TestOverEscapingFix(unittest.TestCase):
    """Test cases for over-escaping fix functionality."""

    def test_fix_double_escaped_ampersands(self):
        """Test fixing double-escaped ampersands."""
        input_text = r"Safe-Words \\& Signalsysteme"
        expected = r"Safe-Words \& Signalsysteme"
        result, changes = fix_over_escaping(input_text)
        self.assertEqual(result, expected)
        self.assertIn("double-escaped ampersands", " ".join(changes))

    def test_fix_hypertarget_commands(self):
        """Test removing hypertarget wrapper commands."""
        input_text = r"""\hypertarget{tool-22}{%
\section{Test Section}
}\label{tool-22}"""
        expected = r"\section{Test Section}"
        result, changes = fix_over_escaping(input_text)
        self.assertEqual(result.strip(), expected)
        self.assertIn("hypertarget", " ".join(changes))

    def test_fix_texorpdfstring_commands(self):
        """Test removing texorpdfstring wrapper commands."""
        input_text = r"\section{\texorpdfstring{\textbf{Title}}{Title}}"
        expected = r"\section{\textbf{Title}}"
        result, changes = fix_over_escaping(input_text)
        self.assertEqual(result, expected)
        self.assertIn("texorpdfstring", " ".join(changes))

    def test_fix_quote_wrapping_in_lists(self):
        """Test removing unnecessary quote wrapping in list items."""
        input_text = r"""\item
  \begin{quote}
  \textbf{Test item}
  \end{quote}"""
        expected = r"\item \textbf{Test item}"
        result, changes = fix_over_escaping(input_text)
        self.assertEqual(result.strip(), expected)
        self.assertIn("quote wrapping", " ".join(changes))

    def test_fix_ul_commands(self):
        """Test replacing ul commands with underline."""
        input_text = r"\ul{underlined text}"
        expected = r"\underline{underlined text}"
        result, changes = fix_over_escaping(input_text)
        self.assertEqual(result, expected)
        self.assertIn("ul{}", " ".join(changes))

    def test_no_changes_needed(self):
        """Test that properly formatted content is not changed."""
        input_text = r"\section*{\textcolor{ctmmRed}{\faStop~Safe-Words \& Signalsysteme}}"
        result, changes = fix_over_escaping(input_text)
        self.assertEqual(result, input_text)
        self.assertEqual(len(changes), 0)

    def test_complex_over_escaped_content(self):
        """Test fixing the complex example from the issue."""
        input_text = r"""\hypertarget{tool-22-safe-words}{%
\section{\texorpdfstring{\textbf{🛑 TOOL 22 -- SAFE-WORDS \\& SIGNALSYSTEME}}{TOOL 22}}
}\label{tool-22}

\begin{itemize}
\item
  \begin{quote}
  \textbf{„Ich kann nicht mehr``}
  \end{quote}
\end{itemize}

\ul{underlined text}"""

        result, changes = fix_over_escaping(input_text)
        
        # Should fix multiple issues
        self.assertGreater(len(changes), 3)
        self.assertIn("hypertarget", " ".join(changes))
        self.assertIn("texorpdfstring", " ".join(changes))
        self.assertIn("quote wrapping", " ".join(changes))
        self.assertIn("ul{}", " ".join(changes))
        
        # Result should not contain problematic patterns
        self.assertNotIn(r"\\&", result)
        self.assertNotIn("hypertarget", result)
        self.assertNotIn("texorpdfstring", result)
        self.assertNotIn(r"\ul{", result)

    def test_file_processing(self):
        """Test processing a temporary file."""
        from fix_over_escaping import process_file
        
        # Create a temporary file with over-escaped content
        with tempfile.NamedTemporaryFile(mode='w', suffix='.tex', delete=False) as f:
            f.write(r"Test \\& content with \ul{problems}")
            temp_path = Path(f.name)
        
        try:
            # Process the file
            result = process_file(temp_path, dry_run=False)
            self.assertTrue(result)  # Should return True indicating changes were made
            
            # Read the corrected content
            with open(temp_path, 'r') as f:
                corrected_content = f.read()
            
            self.assertIn(r"\&", corrected_content)
            self.assertIn(r"\underline{", corrected_content)
            self.assertNotIn(r"\\&", corrected_content)
            self.assertNotIn(r"\ul{", corrected_content)
            
        finally:
            # Clean up
            temp_path.unlink()


if __name__ == '__main__':
    unittest.main()