#!/usr/bin/env python3
"""
Test to verify that no merge conflict markers exist in GitHub workflow files.
This test ensures that YAML files are valid and free of unresolved merge conflicts.
"""

import os
import re
import unittest


class TestMergeConflictMarkers(unittest.TestCase):
    """Test suite to detect merge conflict markers in workflow files."""

    WORKFLOW_DIR = ".github/workflows"

    # Common merge conflict marker patterns
    CONFLICT_PATTERNS = [
        r'^<{7}\s',      # <<<<<<< HEAD or <<<<<<< branch-name
        r'^={7}\s*$',    # =======
        r'^>{7}\s',      # >>>>>>> branch-name
        r'^\s*pr-\d+\s*$',  # Branch name like "pr-653" on its own line
    ]

    def setUp(self):
        """Set up test fixtures."""
        self.workflow_files = []
        if os.path.exists(self.WORKFLOW_DIR):
            for filename in os.listdir(self.WORKFLOW_DIR):
                if filename.endswith(('.yml', '.yaml')):
                    filepath = os.path.join(self.WORKFLOW_DIR, filename)
                    self.workflow_files.append(filepath)

    def test_workflow_files_exist(self):
        """Test that workflow files are found."""
        self.assertGreater(len(self.workflow_files), 0,
                          "No workflow files found in .github/workflows")

    def test_no_merge_conflict_markers(self):
        """Test that no merge conflict markers exist in workflow files."""
        conflicts_found = {}

        for filepath in self.workflow_files:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            file_conflicts = []
            for line_num, line in enumerate(lines, start=1):
                for pattern in self.CONFLICT_PATTERNS:
                    if re.match(pattern, line):
                        file_conflicts.append({
                            'line_num': line_num,
                            'content': line.rstrip(),
                            'pattern': pattern
                        })

            if file_conflicts:
                conflicts_found[filepath] = file_conflicts

        # Build error message if conflicts found
        if conflicts_found:
            error_msg = "\n\nMerge conflict markers found in workflow files:\n"
            error_msg += "=" * 60 + "\n"

            for filepath, conflicts in conflicts_found.items():
                error_msg += f"\nFile: {filepath}\n"
                error_msg += "-" * 60 + "\n"
                for conflict in conflicts:
                    error_msg += f"  Line {conflict['line_num']}: {conflict['content']}\n"
                    error_msg += f"  Pattern: {conflict['pattern']}\n"

            error_msg += "\n" + "=" * 60 + "\n"
            error_msg += "Please resolve these merge conflicts before committing.\n"

            self.fail(error_msg)

    def test_latex_build_yml_specific_fix(self):
        """Test the specific fix for latex-build.yml lines 116-119."""
        target_file = os.path.join(self.WORKFLOW_DIR, "latex-build.yml")

        if not os.path.exists(target_file):
            self.skipTest(f"{target_file} not found")

        with open(target_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Check that the specific problematic merge conflict marker is not present
        # (as a standalone line, not within echo statements)
        for line_num, line in enumerate(lines, start=1):
            stripped = line.strip()
            # Match exact merge conflict markers (not in echo statements)
            if re.match(r'^={7}\s*$', stripped):
                self.fail(f"Found merge conflict separator on line {line_num}: {line}")
            if stripped == 'pr-653':
                self.fail(f"Found branch marker 'pr-653' on line {line_num}: {line}")

        # Check that ghostscript appears only once in extra_system_packages
        # (not duplicated)
        content = ''.join(lines)
        in_extra_packages = False
        ghostscript_count = 0

        for line in lines:
            if 'extra_system_packages:' in line:
                in_extra_packages = True
            elif in_extra_packages:
                if line.strip() == 'ghostscript':
                    ghostscript_count += 1
                elif line.strip().startswith('- name:'):
                    # Reached next step
                    break

        self.assertEqual(ghostscript_count, 1,
                        f"Expected ghostscript to appear once, found {ghostscript_count} times")

    def test_yaml_syntax_valid(self):
        """Test that all workflow YAML files have valid syntax."""
        try:
            import yaml
        except ImportError:
            self.skipTest("PyYAML not installed, skipping YAML validation")

        for filepath in self.workflow_files:
            with self.subTest(file=filepath):
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        yaml.safe_load(f)
                except yaml.YAMLError as e:
                    self.fail(f"Invalid YAML syntax in {filepath}: {e}")


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
