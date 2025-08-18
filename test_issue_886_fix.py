#!/usr/bin/env python3
"""
Test for Issue #886: CI Build Failure - Invalid LaTeX Action Version

This test validates that the GitHub Actions workflow uses a valid version tag
for the dante-ev/latex-action, preventing the CI failure caused by using @v2
which doesn't exist.
"""

import unittest
import os
import re
import yaml

class TestIssue886Fix(unittest.TestCase):
    """Test the fix for Issue #886 - CI build failure due to invalid action version."""
    
    def test_latex_action_version_exists(self):
        """Test that dante-ev/latex-action uses a valid, specific version tag."""
        workflow_file = '.github/workflows/latex-build.yml'
        self.assertTrue(os.path.exists(workflow_file), 
                       f"Workflow file {workflow_file} should exist")
        
        with open(workflow_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find dante-ev/latex-action usage
        latex_action_pattern = r'uses:\s+(dante-ev/latex-action)@([^\s\n]+)'
        matches = re.findall(latex_action_pattern, content)
        
        self.assertTrue(matches, "Should find dante-ev/latex-action usage in workflow")
        
        action, version = matches[0]
        
        # The version should NOT be just @v2 (which doesn't exist)
        self.assertNotEqual(version, 'v2', 
                           "dante-ev/latex-action@v2 doesn't exist and causes CI failure")
        
        # The version should be a semantic version like v2.0.0
        self.assertRegex(version, r'^v\d+\.\d+\.\d+$', 
                        f"Version should be semantic (e.g., v2.0.0), found: {version}")
        
        # Specifically, it should be v2.0.0 based on previous resolutions
        self.assertEqual(version, 'v2.0.0', 
                        "Based on ISSUE_702_RESOLUTION.md, should use v2.0.0")
    
    def test_workflow_yaml_syntax_valid(self):
        """Test that the workflow YAML file is valid and can be parsed."""
        workflow_file = '.github/workflows/latex-build.yml'
        
        with open(workflow_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        try:
            yaml.safe_load(content)
        except yaml.YAMLError as e:
            self.fail(f"Workflow YAML should be valid: {e}")
    
    def test_no_other_invalid_versions(self):
        """Test that no other actions use invalid major-only version tags."""
        workflow_file = '.github/workflows/latex-build.yml'
        
        with open(workflow_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all action usages
        uses_pattern = r'uses:\s+([^@\s]+)@([^\s\n]+)'
        matches = re.findall(uses_pattern, content)
        
        for action, version in matches:
            # Skip the specific dante-ev/latex-action since we test it separately
            if 'dante-ev/latex-action' in action:
                continue
                
            # Other actions should not use major-only versions like @v2, @v3, etc.
            # (unless they're well-known GitHub actions that support major version tags)
            if action.startswith('actions/'):
                # GitHub's own actions support major version tags like @v4
                continue
            else:
                # Third-party actions should use semantic versions
                self.assertRegex(version, r'^v\d+\.\d+', 
                               f"Third-party action {action} should use semantic version, found: {version}")

if __name__ == '__main__':
    print("=" * 70)
    print("Testing Issue #886 Fix: CI Build Failure - Invalid LaTeX Action Version")
    print("=" * 70)
    
    unittest.main(verbosity=2)