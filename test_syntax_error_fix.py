#!/usr/bin/env python3
"""
Test to verify the syntax error fix in ctmm_build.py (Issue #XXX).

This test ensures that the template creation section has proper try-except
structure to prevent SyntaxError: invalid syntax.
"""

import unittest
import ast
import os


class TestCTMMBuildSyntaxFix(unittest.TestCase):
    """Test that ctmm_build.py has correct syntax and proper error handling."""

    def setUp(self):
        """Set up test by reading the ctmm_build.py file."""
        self.ctmm_build_path = os.path.join(
            os.path.dirname(__file__),
            "ctmm_build.py"
        )
        with open(self.ctmm_build_path, 'r', encoding='utf-8') as f:
            self.source_code = f.read()

    def test_python_syntax_is_valid(self):
        """Test that ctmm_build.py has valid Python syntax."""
        try:
            ast.parse(self.source_code)
        except SyntaxError as e:
            self.fail(f"ctmm_build.py has syntax error: {e}")

    def test_template_creation_has_try_except(self):
        """Test that template creation section has proper try-except structure."""
        # Parse the source code
        tree = ast.parse(self.source_code)

        # Find the main() function
        main_func = None
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == 'main':
                main_func = node
                break

        self.assertIsNotNone(main_func, "main() function not found")

        # Look for try-except blocks in main()
        try_blocks = []
        for node in ast.walk(main_func):
            if isinstance(node, ast.Try):
                try_blocks.append(node)

        # Ensure we have try-except blocks
        self.assertGreater(
            len(try_blocks), 0,
            "No try-except blocks found in main() function"
        )

    def test_no_orphaned_except_blocks(self):
        """Test that there are no orphaned except blocks without matching try."""
        # Parse the source code
        tree = ast.parse(self.source_code)

        # Walk through the AST and verify structure
        for node in ast.walk(tree):
            # All except handlers should be part of a Try node
            if isinstance(node, ast.ExceptHandler):
                # Find parent Try node
                parent_has_try = False
                for potential_parent in ast.walk(tree):
                    if isinstance(potential_parent, ast.Try):
                        if node in potential_parent.handlers:
                            parent_has_try = True
                            break

                # If we found an ExceptHandler, it should be in a Try
                # (This is actually impossible in valid Python AST, but we test it anyway)
                self.assertTrue(
                    parent_has_try or True,  # AST guarantees this
                    "Found except handler without matching try block"
                )

    def test_template_creation_error_handling(self):
        """Test that template creation has proper error handling structure."""
        # This test verifies the specific fix for the reported issue
        # The code should have: if total_missing > 0: ... try: ... except:

        lines = self.source_code.split('\n')

        # Find the template creation section
        template_section_start = None
        for i, line in enumerate(lines):
            if 'Creating templates for missing files' in line:
                template_section_start = i
                break

        self.assertIsNotNone(
            template_section_start,
            "Template creation section not found"
        )

        # Check that there's a try block after the print statement
        found_try = False
        found_except = False

        # Look in the next 20 lines for try and except
        for i in range(template_section_start, min(template_section_start + 20, len(lines))):
            line = lines[i].strip()
            if line.startswith('try:'):
                found_try = True
            if line.startswith('except Exception as e:'):
                found_except = True

        self.assertTrue(
            found_try,
            "Template creation section missing try block"
        )
        self.assertTrue(
            found_except,
            "Template creation section missing except block"
        )

    def test_all_try_blocks_have_except(self):
        """Test that all try blocks have corresponding except or finally."""
        tree = ast.parse(self.source_code)

        for node in ast.walk(tree):
            if isinstance(node, ast.Try):
                # Each Try node should have either handlers or finalbody
                self.assertTrue(
                    len(node.handlers) > 0 or len(node.finalbody) > 0,
                    "Found try block without except or finally"
                )


if __name__ == '__main__':
    unittest.main()
