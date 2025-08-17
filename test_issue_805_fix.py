#!/usr/bin/env python3
"""
Test validation for Issue #805: CI Failure Resolution
Validates the fixes for CI pipeline robustness and resource leak issues.
"""

import unittest
import subprocess
import sys
from pathlib import Path
import yaml
import tempfile
import warnings
import os


class TestIssue805Fix(unittest.TestCase):
    """Test suite for Issue #805 CI failure resolution."""
    
    def setUp(self):
        """Set up test environment."""
        self.repo_root = Path(__file__).parent
        
    def test_latex_validator_resource_leak_fixed(self):
        """Test that resource leaks in latex_validator.py are fixed."""
        # Enable resource warnings to catch file handle leaks
        warnings.filterwarnings("error", category=ResourceWarning)
        
        try:
            # Import and use the LaTeX validator
            sys.path.insert(0, str(self.repo_root))
            from latex_validator import LaTeXValidator
            
            validator = LaTeXValidator()
            
            # Test directory validation (this triggered the resource leak)
            modules_dir = self.repo_root / "modules"
            if modules_dir.exists():
                results = validator.validate_directory(modules_dir, fix=False)
                self.assertIsInstance(results, dict)
                
            # If we get here without ResourceWarning exception, the fix worked
            print("✅ No resource leaks detected in LaTeX validator")
            
        except ResourceWarning as e:
            self.fail(f"Resource leak still present: {e}")
        finally:
            warnings.resetwarnings()
            
    def test_workflow_syntax_remains_valid(self):
        """Test that workflow YAML syntax is still valid after enhancements."""
        workflows_dir = self.repo_root / ".github" / "workflows"
        
        workflow_files = [
            "latex-build.yml",
            "latex-validation.yml", 
            "pr-validation.yml",
            "static.yml"
        ]
        
        for workflow_file in workflow_files:
            workflow_path = workflows_dir / workflow_file
            
            with self.subTest(workflow=workflow_file):
                self.assertTrue(workflow_path.exists(), 
                              f"Workflow file {workflow_file} not found")
                
                # Test YAML parsing
                with open(workflow_path, 'r', encoding='utf-8') as f:
                    try:
                        workflow_data = yaml.safe_load(f)
                        self.assertIsInstance(workflow_data, dict)
                        
                        # Check that 'on' key is properly handled
                        self.assertIn('on', workflow_data)
                        self.assertIsInstance(workflow_data['on'], dict)
                        
                        print(f"✅ {workflow_file}: Valid YAML syntax")
                        
                    except yaml.YAMLError as e:
                        self.fail(f"YAML parsing error in {workflow_file}: {e}")
                        
    def test_pr_validation_enhancements(self):
        """Test that PR validation workflow has enhanced error handling."""
        pr_validation_path = self.repo_root / ".github" / "workflows" / "pr-validation.yml"
        
        with open(pr_validation_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check for enhanced error handling features
        error_handling_features = [
            "# Get the base and head commits with error handling",
            "if [ -z \"$BASE_SHA\" ] || [ -z \"$HEAD_SHA\" ]; then",
            "2>/dev/null",  # Error redirection
            "echo \"⚠️ Warning:",  # Warning messages
            "📋 Debug information:",  # Debug output
        ]
        
        for feature in error_handling_features:
            with self.subTest(feature=feature):
                self.assertIn(feature, content, 
                            f"Enhanced error handling feature missing: {feature}")
                
        print("✅ PR validation workflow has enhanced error handling")
        
    def test_latex_build_enhancements(self):
        """Test that LaTeX build workflow has enhanced robustness."""
        latex_build_path = self.repo_root / ".github" / "workflows" / "latex-build.yml"
        
        with open(latex_build_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check for enhanced robustness features  
        robustness_features = [
            "echo \"📋 Checking critical files:\"",  # File checking
            "if [ ! -f \"main.tex\" ]; then",  # Critical file validation
            "echo \"🔍 Verifying PDF generation...\"",  # Enhanced PDF verification
            "PDF_SIZE=$(stat -c%s \"main.pdf\"",  # File size check
            "FILE_TYPE=$(file main.pdf)",  # File type validation
        ]
        
        for feature in robustness_features:
            with self.subTest(feature=feature):
                self.assertIn(feature, content,
                            f"Enhanced robustness feature missing: {feature}")
                
        print("✅ LaTeX build workflow has enhanced robustness")
        
    def test_build_system_still_functional(self):
        """Test that the CTMM build system still works after changes."""
        try:
            result = subprocess.run(
                [sys.executable, "ctmm_build.py"],
                cwd=self.repo_root,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            # Build system should exit with code 0
            self.assertEqual(result.returncode, 0, 
                           f"Build system failed: {result.stderr}")
            
            # Combine stdout and stderr for checking
            output = result.stdout + result.stderr
            
            # Check for expected output
            expected_outputs = [
                "CTMM Build System - Starting check",
                "LaTeX validation: ✓ PASS",
                "CTMM BUILD SYSTEM SUMMARY"
            ]
            
            for expected in expected_outputs:
                self.assertIn(expected, output,
                            f"Expected output missing: {expected}")
                            
            print("✅ CTMM build system remains functional")
            
        except subprocess.TimeoutExpired:
            self.fail("Build system timed out")
        except Exception as e:
            self.fail(f"Build system execution failed: {e}")
            
    def test_validation_scripts_functional(self):
        """Test that key validation scripts still work."""
        validation_scripts = [
            "validate_latex_syntax.py",
            "test_issue_743_validation.py", 
            "test_issue_761_fix.py"
        ]
        
        for script in validation_scripts:
            with self.subTest(script=script):
                script_path = self.repo_root / script
                self.assertTrue(script_path.exists(), f"Script {script} not found")
                
                try:
                    result = subprocess.run(
                        [sys.executable, script],
                        cwd=self.repo_root,
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                    
                    self.assertEqual(result.returncode, 0,
                                   f"Validation script {script} failed: {result.stderr}")
                    print(f"✅ {script}: Functional")
                    
                except subprocess.TimeoutExpired:
                    self.fail(f"Validation script {script} timed out")
                except Exception as e:
                    self.fail(f"Validation script {script} execution failed: {e}")


def main():
    """Run the Issue #805 fix validation tests."""
    print("=" * 70)
    print("ISSUE #805 VALIDATION: CI Failure Resolution")
    print("=" * 70)
    print("🔧 Testing fixes for:")
    print("  - Resource leaks in latex_validator.py")  
    print("  - Enhanced CI workflow error handling")
    print("  - Improved robustness and stability")
    print("=" * 70)
    
    # Run the tests
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestIssue805Fix)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "=" * 70)
    print("VALIDATION SUMMARY")
    print("=" * 70)
    
    if result.wasSuccessful():
        print("🎉 ALL TESTS PASSED! Issue #805 fixes validated.")
        print("\nThe CI pipeline should now be more robust with:")
        print("✓ Fixed resource leaks in LaTeX validator")
        print("✓ Enhanced error handling in workflows")
        print("✓ Improved debugging and diagnostic output")
        print("✓ Better validation of critical files and dependencies")
        print("✓ Graceful handling of edge cases")
        return 0
    else:
        print(f"❌ {len(result.failures)} test(s) failed, {len(result.errors)} error(s)")
        return 1


if __name__ == "__main__":
    sys.exit(main())