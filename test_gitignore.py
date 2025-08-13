#!/usr/bin/env python3
"""
Test to verify that binary files are properly excluded from git tracking.
This addresses the Copilot review issue where binary files prevent proper code review.
"""

import unittest
import subprocess
import os
from pathlib import Path

class TestGitIgnoreConfiguration(unittest.TestCase):
    """Test that binary files are properly ignored by git."""

    def test_no_pdf_files_tracked(self):
        """Test that no PDF files are tracked by git."""
        result = subprocess.run(
            ['git', 'ls-files'], 
            capture_output=True, 
            text=True, 
            check=True
        )
        tracked_files = result.stdout.strip().split('\n')
        pdf_files = [f for f in tracked_files if f.endswith('.pdf')]
        self.assertEqual(len(pdf_files), 0, 
                        f"Found PDF files tracked by git: {pdf_files}")

    def test_no_docx_files_tracked(self):
        """Test that no DOCX files are tracked by git."""
        result = subprocess.run(
            ['git', 'ls-files'], 
            capture_output=True, 
            text=True, 
            check=True
        )
        tracked_files = result.stdout.strip().split('\n')
        docx_files = [f for f in tracked_files if f.endswith('.docx')]
        self.assertEqual(len(docx_files), 0, 
                        f"Found DOCX files tracked by git: {docx_files}")

    def test_gitignore_includes_binary_patterns(self):
        """Test that .gitignore includes patterns for binary files."""
        gitignore_path = Path('.gitignore')
        self.assertTrue(gitignore_path.exists(), ".gitignore file must exist")
        
        with open(gitignore_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for essential binary file patterns
        self.assertIn('*.pdf', content, ".gitignore must include *.pdf pattern")
        self.assertIn('*.docx', content, ".gitignore must include *.docx pattern")

    def test_pdf_files_are_ignored(self):
        """Test that PDF files are properly ignored by git."""
        # Check if main.pdf exists and is ignored
        if Path('main.pdf').exists():
            result = subprocess.run(
                ['git', 'check-ignore', 'main.pdf'], 
                capture_output=True, 
                check=False
            )
            self.assertEqual(result.returncode, 0, 
                           "main.pdf should be ignored by git")

    def test_all_text_files_have_proper_encoding(self):
        """Test that all tracked text files have proper UTF-8 encoding."""
        result = subprocess.run(
            ['git', 'ls-files'], 
            capture_output=True, 
            text=True, 
            check=True
        )
        tracked_files = result.stdout.strip().split('\n')
        
        # Filter for text files we expect to be UTF-8
        text_extensions = ['.tex', '.py', '.md', '.txt']
        text_files = [f for f in tracked_files 
                     if any(f.endswith(ext) for ext in text_extensions)]
        
        encoding_issues = []
        for file_path in text_files:
            if Path(file_path).exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        f.read()
                except UnicodeDecodeError:
                    encoding_issues.append(file_path)
        
        self.assertEqual(len(encoding_issues), 0, 
                        f"Files with encoding issues: {encoding_issues}")

if __name__ == '__main__':
    # Change to repository directory if needed
    repo_root = Path(__file__).parent
    os.chdir(repo_root)
    
    unittest.main(verbosity=2)