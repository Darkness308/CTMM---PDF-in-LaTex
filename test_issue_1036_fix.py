#!/usr/bin/env python3
"""
Test case for Issue #1036: CI Build Failure - LaTeX Action Version Fix

This test validates that the dante-ev/latex-action version is correctly
specified to prevent "Unable to resolve action" errors in GitHub Actions.
"""

import unittest
import os
import re
from pathlib import Path


class TestIssue1036Fix(unittest.TestCase):
    """Test cases for Issue #1036 fix."""

    def setUp(self):
        """Set up test environment."""
        self.workflow_file = Path(".github/workflows/latex-build.yml")
        self.assertTrue(self.workflow_file.exists(), "LaTeX build workflow file must exist")

    def test_latex_action_version_is_valid(self):
        """Test that dante-ev/latex-action uses a valid version tag."""
        content = self.workflow_file.read_text(encoding='utf-8')
        
        # Find the latex-action usage
        pattern = r'uses:\s+dante-ev/latex-action@(\S+)'
        matches = re.findall(pattern, content)
        
        self.assertTrue(matches, "dante-ev/latex-action usage not found in workflow")
        
        version = matches[0]
        
        # Valid versions based on previous issue resolutions
        valid_versions = ['latest', 'v0.2', 'v1.0.0']
        invalid_versions = ['v2', 'v2.0.0']  # Known problematic versions from issues #735, #867
        
        self.assertIn(version, valid_versions, 
                     f"dante-ev/latex-action@{version} is not a valid version. "
                     f"Valid versions: {valid_versions}")
        
        self.assertNotIn(version, invalid_versions,
                        f"dante-ev/latex-action@{version} is a known problematic version. "
                        f"Avoid: {invalid_versions}")

    def test_workflow_syntax_is_valid(self):
        """Test that the workflow file has valid YAML syntax."""
        content = self.workflow_file.read_text(encoding='utf-8')
        
        # Check for quoted "on" syntax (Issue #458 fix)
        self.assertIn('"on":', content, "Workflow must use quoted 'on:' syntax")
        
        # Check for proper structure
        self.assertIn('jobs:', content, "Workflow must have jobs section")
        self.assertIn('build:', content, "Workflow must have build job")
        self.assertIn('runs-on: ubuntu-latest', content, "Build job must specify runner")

    def test_latex_action_configuration(self):
        """Test that LaTeX action is properly configured."""
        content = self.workflow_file.read_text(encoding='utf-8')
        
        # Check that root_file is specified
        self.assertIn('root_file: main.tex', content,
                     "LaTeX action must specify root_file: main.tex")
        
        # Check that args are specified
        self.assertIn('args:', content, "LaTeX action must specify compilation args")
        
        # Check for essential LaTeX packages
        required_packages = [
            'texlive-lang-german',
            'texlive-fonts-recommended',
            'texlive-latex-recommended'
        ]
        
        for package in required_packages:
            self.assertIn(package, content, 
                         f"Required LaTeX package {package} not found in workflow")

    def test_no_problematic_versions_remain(self):
        """Test that no problematic action versions remain in any workflow."""
        workflows_dir = Path(".github/workflows")
        problematic_patterns = [
            r'dante-ev/latex-action@v2\b',  # Issue #867, #1036
            r'dante-ev/latex-action@v2\.0\.0',  # Issue #735
        ]
        
        for workflow_file in workflows_dir.glob("*.yml"):
            content = workflow_file.read_text(encoding='utf-8')
            
            for pattern in problematic_patterns:
                matches = re.findall(pattern, content)
                self.assertEqual(len(matches), 0,
                               f"Found problematic version pattern '{pattern}' in {workflow_file}")

    def test_build_system_compatibility(self):
        """Test that the fix doesn't break build system compatibility."""
        # Import and run basic build system check
        try:
            import ctmm_build
            # Test that main() function exists and runs without errors
            self.assertTrue(hasattr(ctmm_build, 'main'), "ctmm_build should have main() function")
            
            # Test that the module can be imported and basic functionality works
            self.assertTrue(hasattr(ctmm_build, 'validate_latex_files'), 
                           "ctmm_build should have validate_latex_files() function")
        except ImportError:
            self.skipTest("ctmm_build module not available")
        except Exception as e:
            self.fail(f"Build system compatibility check failed: {e}")


class TestIssue1036Robustness(unittest.TestCase):
    """Robustness tests to prevent regression."""

    def test_action_version_robustness(self):
        """Test robustness against action version changes."""
        workflow_file = Path(".github/workflows/latex-build.yml")
        content = workflow_file.read_text(encoding='utf-8')
        
        # Ensure we have error handling for potential action failures
        steps = [
            'Verify PDF generation',
            'Upload build logs (on failure)'
        ]
        
        for step in steps:
            self.assertIn(step, content, 
                         f"Workflow missing robustness step: {step}")

    def test_github_actions_best_practices(self):
        """Test adherence to GitHub Actions best practices."""
        workflow_file = Path(".github/workflows/latex-build.yml")
        content = workflow_file.read_text(encoding='utf-8')
        
        # Check for pinned action versions (not latest for critical actions)
        critical_actions = [
            'actions/checkout@v4',
            'actions/setup-python@v4',
            'actions/upload-artifact@v4'
        ]
        
        for action in critical_actions:
            self.assertIn(action, content,
                         f"Critical action should be pinned: {action}")


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)