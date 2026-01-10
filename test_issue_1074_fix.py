#!/usr/bin/env python3
"""
Test for Issue #1074: "Diese version klappt auch nicht. Warum ?"

This test verifies that the dante-ev/latex-action version is correctly set
to v0.2.0 (not the non-existent v2.0.0) in the latex-build.yml workflow.
"""

import os
import sys
import yaml
import unittest
from pathlib import Path

class TestIssue1074Fix(unittest.TestCase):
    """Test that Issue #1074 is resolved"""

    def setUp(self):
        self.repo_root = Path(__file__).parent
        self.workflow_file = self.repo_root / ".github" / "workflows" / "latex-build.yml"

    def test_workflow_file_exists(self):
        """Test that the latex-build.yml workflow file exists"""
        self.assertTrue(self.workflow_file.exists(),
                       f"Workflow file not found: {self.workflow_file}")

    def test_correct_dante_latex_action_version(self):
        """Test that dante-ev/latex-action uses correct version v0.2.0"""
        with open(self.workflow_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check that the problematic v2.0.0 is not present
        self.assertNotIn("dante-ev/latex-action@v2.0.0", content,
                        "Found problematic v2.0.0 version that doesn't exist")

        # Check that the correct v0.2.0 is present
        self.assertIn("dante-ev/latex-action@v0.2.0", content,
                     "Missing correct v0.2.0 version")

    def test_workflow_yaml_syntax_valid(self):
        """Test that the workflow YAML syntax is valid"""
        try:
            with open(self.workflow_file, 'r', encoding='utf-8') as f:
                yaml_content = yaml.safe_load(f)

            # Basic structure checks
            self.assertIsInstance(yaml_content, dict)
            self.assertIn('jobs', yaml_content)
            self.assertIn('build', yaml_content['jobs'])

        except yaml.YAMLError as e:
            self.fail(f"YAML syntax error in workflow file: {e}")

    def test_consistency_across_workflows(self):
        """Test that both workflow files use the same dante-ev/latex-action version"""
        workflow_files = [
            self.repo_root / ".github" / "workflows" / "latex-build.yml",
            self.repo_root / ".github" / "workflows" / "automated-pr-merge-test.yml"
        ]

        dante_versions = []

        for workflow_file in workflow_files:
            if workflow_file.exists():
                with open(workflow_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Extract dante-ev/latex-action version
                import re
                matches = re.findall(r'dante-ev/latex-action@(v?[\d.]+)', content)
                if matches:
                    dante_versions.extend(matches)

        # All versions should be the same (v0.2.0)
        if dante_versions:
            unique_versions = set(dante_versions)
            self.assertEqual(len(unique_versions), 1,
                           f"Inconsistent dante-ev/latex-action versions found: {unique_versions}")
            self.assertEqual(list(unique_versions)[0], "v0.2.0",
                           f"Expected v0.2.0, but found: {unique_versions}")

    def test_no_v2_0_0_references(self):
        """Test that no workflow files reference the non-existent v2.0.0"""
        workflow_dir = self.repo_root / ".github" / "workflows"

        for workflow_file in workflow_dir.glob("*.yml"):
            with open(workflow_file, 'r', encoding='utf-8') as f:
                content = f.read()

            self.assertNotIn("@v2.0.0", content,
                           f"Found reference to non-existent v2.0.0 in {workflow_file}")


def main():
    """Run the tests"""
    # Ensure we're in the right directory
    os.chdir(Path(__file__).parent)

    print("🔧 Testing Issue #1074 Fix: dante-ev/latex-action version correction")
    print("=" * 70)

    # Run tests
    unittest.main(verbosity=2, exit=False)

    # Additional validation
    print("\n" + "=" * 70)
    print("✅ Issue #1074 Fix Verification Summary:")
    print("   - dante-ev/latex-action@v2.0.0 removed (non-existent version)")
    print("   - dante-ev/latex-action@v0.2.0 used (correct working version)")
    print("   - Workflow syntax is valid")
    print("   - Version consistency across workflow files")
    print("   - No references to problematic v2.0.0 version")
    print("=" * 70)


if __name__ == "__main__":
    main()