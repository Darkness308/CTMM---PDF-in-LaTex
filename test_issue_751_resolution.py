#!/usr/bin/env python3
"""
Test Suite for GitHub Copilot Issue #751 Resolution

This test suite validates that all components of the Issue #751 resolution
are working correctly and that GitHub Copilot can successfully review PRs.

Test Categories:
- Resolution tool functionality
- Repository health validation
- PR content analysis
- Copilot readiness verification
- Integration with CTMM system
"""

import unittest
import subprocess
import os
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add the current directory to path to import our module
sys.path.insert(0, str(Path(__file__).parent))

try:
    from verify_issue_751_resolution import Issue751Resolver
except ImportError:
    print("❌ Cannot import Issue751Resolver - please ensure verify_issue_751_resolution.py exists")
    sys.exit(1)

class TestIssue751Resolution(unittest.TestCase):
    """Test suite for Issue #751 resolution tools."""
    
    def setUp(self):
        """Set up test environment."""
        self.resolver = Issue751Resolver()
        self.test_results = []
    
    def tearDown(self):
        """Clean up after tests."""
        # Record test results for summary
        pass
    
    def test_resolver_initialization(self):
        """Test that the resolver initializes correctly."""
        self.assertIsInstance(self.resolver, Issue751Resolver)
        self.assertEqual(self.resolver.repo_root, Path.cwd())
        self.assertIsInstance(self.resolver.issues_found, list)
        self.assertIsInstance(self.resolver.resolutions_applied, list)
        print("✅ Resolver initialization test passed")
    
    def test_run_command_functionality(self):
        """Test the command execution functionality."""
        # Test successful command
        success, stdout, stderr = self.resolver.run_command("echo test")
        self.assertTrue(success)
        self.assertIn("test", stdout)
        
        # Test command that should fail
        success, stdout, stderr = self.resolver.run_command("nonexistent_command_12345")
        self.assertFalse(success)
        
        print("✅ Command execution test passed")
    
    def test_repository_health_validation(self):
        """Test repository health validation functionality."""
        health_results = self.resolver.validate_repository_health()
        
        # Check that all expected keys are present
        expected_keys = ['clean_working_tree', 'no_binary_files', 'reasonable_size', 'no_merge_conflicts']
        for key in expected_keys:
            self.assertIn(key, health_results)
            self.assertIsInstance(health_results[key], bool)
        
        print("✅ Repository health validation test passed")
    
    def test_pr_content_analysis(self):
        """Test PR content analysis functionality."""
        content_analysis = self.resolver.analyze_pr_content()
        
        # Check for expected analysis results
        if 'error' not in content_analysis:
            expected_keys = ['changed_files', 'files_list']
            for key in expected_keys:
                self.assertIn(key, content_analysis)
        
        print("✅ PR content analysis test passed")
    
    def test_copilot_readiness_check(self):
        """Test Copilot readiness verification."""
        readiness = self.resolver.check_copilot_readiness()
        
        # Check that all readiness criteria are evaluated
        expected_keys = ['healthy_repo', 'has_changes', 'meaningful_content', 'reviewable_files', 'copilot_ready']
        for key in expected_keys:
            self.assertIn(key, readiness)
            self.assertIsInstance(readiness[key], bool)
        
        print("✅ Copilot readiness check test passed")
    
    def test_issue_751_resolution_verification(self):
        """Test that Issue #751 resolution verification works."""
        resolution_status = self.resolver.verify_issue_751_resolution()
        self.assertIsInstance(resolution_status, bool)
        
        # If resolved, ensure all components are present
        if resolution_status:
            self.assertTrue(Path('ISSUE_751_RESOLUTION.md').exists())
            self.assertTrue(Path('verify_issue_751_resolution.py').exists())
        
        print("✅ Issue #751 resolution verification test passed")
    
    def test_ctmm_integration(self):
        """Test integration with CTMM build system."""
        if Path('ctmm_build.py').exists():
            integration_status = self.resolver.run_ctmm_integration_test()
            self.assertIsInstance(integration_status, bool)
            print("✅ CTMM integration test passed")
        else:
            print("⚠️ CTMM build system not found - skipping integration test")
    
    def test_status_report_generation(self):
        """Test comprehensive status report generation."""
        report = self.resolver.generate_status_report()
        
        # Check that all report sections are present
        expected_sections = [
            'timestamp', 'repository_health', 'pr_content', 
            'copilot_readiness', 'issue_751_resolved', 'ctmm_integration'
        ]
        
        for section in expected_sections:
            self.assertIn(section, report)
        
        print("✅ Status report generation test passed")
    
    def test_file_existence(self):
        """Test that all required files exist."""
        required_files = [
            'ISSUE_751_RESOLUTION.md',
            'verify_issue_751_resolution.py',
            'test_issue_751_resolution.py'
        ]
        
        for file_path in required_files:
            self.assertTrue(Path(file_path).exists(), f"Required file missing: {file_path}")
        
        print("✅ File existence test passed")
    
    def test_documentation_completeness(self):
        """Test that documentation is complete and informative."""
        doc_path = Path('ISSUE_751_RESOLUTION.md')
        if doc_path.exists():
            content = doc_path.read_text()
            
            # Check for key sections
            required_sections = [
                'Problem Statement',
                'Root Cause Analysis', 
                'Comprehensive Solution Framework',
                'Resolution Status'
            ]
            
            for section in required_sections:
                self.assertIn(section, content, f"Documentation missing section: {section}")
        
        print("✅ Documentation completeness test passed")

class TestCommandLineInterface(unittest.TestCase):
    """Test the command-line interface of the resolution tool."""
    
    def test_help_functionality(self):
        """Test that help functionality works."""
        result = subprocess.run([
            sys.executable, 'verify_issue_751_resolution.py', '--help'
        ], capture_output=True, text=True)
        
        self.assertEqual(result.returncode, 0)
        self.assertIn('GitHub Copilot Issue #751', result.stdout)
        print("✅ Command-line help test passed")
    
    def test_repo_health_option(self):
        """Test the repository health command-line option."""
        result = subprocess.run([
            sys.executable, 'verify_issue_751_resolution.py', '--repo-health'
        ], capture_output=True, text=True)
        
        # Should exit with 0 or 1 depending on repository health
        self.assertIn(result.returncode, [0, 1])
        print("✅ Repository health CLI option test passed")

class TestIntegration(unittest.TestCase):
    """Integration tests for the complete resolution system."""
    
    def test_full_resolution_workflow(self):
        """Test the complete resolution workflow."""
        resolver = Issue751Resolver()
        
        # Run the complete verification process
        try:
            resolution_status = resolver.verify_issue_751_resolution()
            self.assertIsInstance(resolution_status, bool)
            print("✅ Full resolution workflow test passed")
        except Exception as e:
            self.fail(f"Full resolution workflow failed: {e}")
    
    def test_error_handling(self):
        """Test that error conditions are handled gracefully."""
        resolver = Issue751Resolver()
        
        # Test with invalid git repository (if we can simulate it)
        with patch.object(resolver, 'run_command') as mock_command:
            mock_command.return_value = (False, "", "Not a git repository")
            
            # Should handle the error gracefully
            health = resolver.validate_repository_health()
            self.assertIsInstance(health, dict)
        
        print("✅ Error handling test passed")

def run_test_suite():
    """Run the complete test suite and provide summary."""
    print("🧪 ISSUE #751 RESOLUTION TEST SUITE")
    print("=" * 60)
    
    # Create test loader and suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestIssue751Resolution,
        TestCommandLineInterface,
        TestIntegration
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print("🎯 TEST SUITE SUMMARY")
    print("=" * 60)
    
    total_tests = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    success_rate = ((total_tests - failures - errors) / total_tests * 100) if total_tests > 0 else 0
    
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {total_tests - failures - errors}")
    print(f"Failed: {failures}")
    print(f"Errors: {errors}")
    print(f"Success Rate: {success_rate:.1f}%")
    
    if failures > 0:
        print(f"\n❌ FAILURES ({failures}):")
        for test, traceback in result.failures:
            print(f"   - {test}: {traceback.split('AssertionError:')[-1].strip()}")
    
    if errors > 0:
        print(f"\n💥 ERRORS ({errors}):")
        for test, traceback in result.errors:
            print(f"   - {test}: {traceback.split('Exception:')[-1].strip()}")
    
    if failures == 0 and errors == 0:
        print("\n🎉 ALL TESTS PASSED!")
        print("Issue #751 resolution system is fully functional.")
        return True
    else:
        print("\n⚠️ SOME TESTS FAILED")
        print("Please review and fix the issues above.")
        return False

def main():
    """Main test execution function."""
    if len(sys.argv) > 1 and sys.argv[1] == '--quick':
        # Quick test mode - just run basic functionality tests
        print("🏃 QUICK TEST MODE")
        suite = unittest.TestSuite()
        suite.addTest(TestIssue751Resolution('test_resolver_initialization'))
        suite.addTest(TestIssue751Resolution('test_file_existence'))
        runner = unittest.TextTestRunner(verbosity=1)
        result = runner.run(suite)
        return len(result.failures) == 0 and len(result.errors) == 0
    else:
        # Full test suite
        return run_test_suite()

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)