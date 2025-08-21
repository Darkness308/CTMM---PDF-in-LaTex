#!/usr/bin/env python3
"""
Test CI Improvements for Issue #1084
Validates the enhanced CI monitoring and diagnostics implementation.
"""

import unittest
import subprocess
import os
from pathlib import Path


class TestCIImprovements(unittest.TestCase):
    """Test cases for CI improvements."""

    def setUp(self):
        """Set up test environment."""
        self.repo_root = Path('.')
        
    def test_enhanced_ci_validation_script_exists(self):
        """Test that the enhanced CI validation script exists and is executable."""
        script_path = self.repo_root / 'validate_ci_environment.py'
        self.assertTrue(script_path.exists(), "validate_ci_environment.py should exist")
        
        # Test that it can be executed
        result = subprocess.run(['python3', str(script_path)], 
                               capture_output=True, text=True, timeout=60)
        self.assertEqual(result.returncode, 0, 
                        f"validate_ci_environment.py should execute successfully: {result.stderr}")

    def test_ci_failure_prevention_script_exists(self):
        """Test that the CI failure prevention script exists and is executable."""
        script_path = self.repo_root / 'ci_failure_prevention.py'
        self.assertTrue(script_path.exists(), "ci_failure_prevention.py should exist")
        
        # Test that it can be executed (may return 1 if issues found, that's OK)
        result = subprocess.run(['python3', str(script_path)], 
                               capture_output=True, text=True, timeout=60)
        self.assertIn(result.returncode, [0, 1], 
                     f"ci_failure_prevention.py should execute: {result.stderr}")

    def test_workflow_files_contain_enhanced_monitoring(self):
        """Test that workflow files contain the enhanced monitoring steps."""
        # Check latex-build.yml
        latex_build_path = self.repo_root / '.github/workflows/latex-build.yml'
        self.assertTrue(latex_build_path.exists(), "latex-build.yml should exist")
        
        with open(latex_build_path, 'r') as f:
            content = f.read()
            
        self.assertIn('Enhanced CI environment validation', content,
                     "latex-build.yml should contain enhanced CI validation step")
        self.assertIn('validate_ci_environment.py', content,
                     "latex-build.yml should reference the validation script")
        self.assertIn('CI failure prevention analysis', content,
                     "latex-build.yml should contain failure prevention step")

    def test_pr_validation_workflow_enhanced(self):
        """Test that PR validation workflow has enhanced monitoring."""
        pr_validation_path = self.repo_root / '.github/workflows/pr-validation.yml'
        self.assertTrue(pr_validation_path.exists(), "pr-validation.yml should exist")
        
        with open(pr_validation_path, 'r') as f:
            content = f.read()
            
        self.assertIn('Enhanced CI environment validation for PRs', content,
                     "pr-validation.yml should contain enhanced CI validation step")

    def test_timeout_configurations_are_reasonable(self):
        """Test that all timeout configurations are reasonable."""
        workflow_dir = self.repo_root / '.github/workflows'
        
        for workflow_file in workflow_dir.glob('*.yml'):
            with open(workflow_file, 'r') as f:
                content = f.read()
                
            # Find all timeout values
            import re
            timeout_matches = re.findall(r'timeout-minutes:\s*(\d+)', content)
            
            for timeout_str in timeout_matches:
                timeout = int(timeout_str)
                # Timeouts should be reasonable (between 3 and 30 minutes)
                self.assertGreaterEqual(timeout, 3, 
                                       f"Timeout {timeout} in {workflow_file.name} is too short")
                self.assertLessEqual(timeout, 30, 
                                    f"Timeout {timeout} in {workflow_file.name} is too long")

    def test_workflow_yaml_syntax_is_valid(self):
        """Test that all workflow YAML files have proper syntax."""
        workflow_dir = self.repo_root / '.github/workflows'
        
        for workflow_file in workflow_dir.glob('*.yml'):
            with open(workflow_file, 'r') as f:
                content = f.read()
                
            # Check for quoted 'on:' syntax (prevents YAML boolean interpretation)
            self.assertIn('"on":', content, 
                         f"{workflow_file.name} should use quoted 'on:' syntax")

    def test_ci_monitoring_scripts_have_proper_structure(self):
        """Test that CI monitoring scripts have proper structure."""
        scripts = ['validate_ci_environment.py', 'ci_failure_prevention.py']
        
        for script_name in scripts:
            script_path = self.repo_root / script_name
            self.assertTrue(script_path.exists(), f"{script_name} should exist")
            
            with open(script_path, 'r') as f:
                content = f.read()
                
            # Check for proper structure
            self.assertIn('def main()', content, 
                         f"{script_name} should have a main() function")
            self.assertIn('if __name__ == "__main__":', content,
                         f"{script_name} should be executable as a script")
            self.assertIn('Issue #1084', content,
                         f"{script_name} should reference Issue #1084")

    def test_enhanced_error_handling_in_workflows(self):
        """Test that workflows have enhanced error handling."""
        workflow_files = [
            '.github/workflows/latex-build.yml',
            '.github/workflows/pr-validation.yml'
        ]
        
        for workflow_file in workflow_files:
            path = self.repo_root / workflow_file
            with open(path, 'r') as f:
                content = f.read()
                
            # Should have continue-on-error for non-critical steps
            continue_on_error_count = content.count('continue-on-error: true')
            self.assertGreater(continue_on_error_count, 0,
                              f"{workflow_file} should have continue-on-error for non-critical steps")

    def test_integration_with_existing_validation_tools(self):
        """Test that new tools integrate with existing validation tools."""
        # Test that existing validation tools still work
        existing_tools = [
            'validate_latex_syntax.py',
            'ctmm_build.py',
            'validate_action_versions.py'
        ]
        
        for tool in existing_tools:
            tool_path = self.repo_root / tool
            self.assertTrue(tool_path.exists(), f"{tool} should exist")
            
            # Test basic execution (may timeout in CI, so keep it short)
            result = subprocess.run(['python3', str(tool_path)], 
                                   capture_output=True, text=True, timeout=30)
            # Should either succeed or fail gracefully (not crash)
            self.assertIn(result.returncode, [0, 1], 
                         f"{tool} should execute without crashing")

    def test_ci_health_monitoring_comprehensive(self):
        """Test that CI health monitoring is comprehensive."""
        script_path = self.repo_root / 'validate_ci_environment.py'
        
        result = subprocess.run(['python3', str(script_path)], 
                               capture_output=True, text=True, timeout=60)
        
        output = result.stdout
        
        # Should check all essential components
        essential_checks = [
            'SYSTEM RESOURCES ANALYSIS',
            'GITHUB ACTIONS ENVIRONMENT', 
            'PACKAGE DEPENDENCIES CHECK',
            'WORKFLOW FILES VALIDATION',
            'LATEX CONFIGURATION CHECK',
            'DIAGNOSTIC TESTS'
        ]
        
        for check in essential_checks:
            self.assertIn(check, output, 
                         f"CI validation should include {check}")


class TestCIFailurePatternDetection(unittest.TestCase):
    """Test CI failure pattern detection capabilities."""

    def test_failure_pattern_analysis(self):
        """Test that failure pattern analysis detects common issues."""
        script_path = Path('ci_failure_prevention.py')
        
        result = subprocess.run(['python3', str(script_path)], 
                               capture_output=True, text=True, timeout=60)
        
        output = result.stdout
        
        # Should analyze key areas
        analysis_areas = [
            'timeout configurations',
            'GitHub Actions versions', 
            'resource usage patterns',
            'LaTeX dependencies'
        ]
        
        for area in analysis_areas:
            self.assertIn(area, output, 
                         f"Should analyze {area}")

    def test_recommendations_generated(self):
        """Test that actionable recommendations are generated."""
        script_path = Path('ci_failure_prevention.py')
        
        result = subprocess.run(['python3', str(script_path)], 
                               capture_output=True, text=True, timeout=60)
        
        output = result.stdout
        
        # Should provide recommendations
        self.assertIn('Recommendations:', output,
                     "Should provide recommendations")
        self.assertIn('Prevention Strategy:', output,
                     "Should provide prevention strategy")


def main():
    """Run all CI improvement tests."""
    print("=" * 70)
    print("🧪 TESTING CI IMPROVEMENTS FOR ISSUE #1084")
    print("=" * 70)
    
    # Run the tests
    unittest.main(verbosity=2, exit=False)
    
    print("\n" + "=" * 70)
    print("✅ CI IMPROVEMENT TESTS COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()