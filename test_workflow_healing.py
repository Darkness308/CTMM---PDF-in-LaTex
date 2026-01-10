#!/usr/bin/env python3
"""
Test Suite for Workflow Healing System
Comprehensive tests for all components of the automated workflow healing system.
"""

import os
import sys
import unittest
import tempfile
import shutil
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from healing_config import config, HealingConfig
from workflow_monitor import WorkflowMonitor, WorkflowRun, JobRun
from error_analyzer import ErrorAnalyzer, ErrorAnalysis, ErrorInstance
from fix_strategies import FixStrategies, FixResult
from pr_manager import PRManager, HealingPR
from workflow_healing_system import WorkflowHealingSystem, HealingSession

class TestHealingConfig(unittest.TestCase):
    """Test the healing configuration system."""

    def test_config_initialization(self):
        """Test that configuration initializes correctly."""
        test_config = HealingConfig()
        self.assertIsInstance(test_config.monitored_workflows, list)
        self.assertGreater(len(test_config.monitored_workflows), 0)
        self.assertIn('latex-build.yml', test_config.monitored_workflows)

    def test_workflow_monitoring(self):
        """Test workflow monitoring configuration."""
        self.assertTrue(config.is_monitored_workflow('latex-build.yml'))
        self.assertTrue(config.is_monitored_workflow('pr-validation.yml'))
        self.assertFalse(config.is_monitored_workflow('unknown-workflow.yml'))

    def test_error_categorization(self):
        """Test error pattern matching."""
        # Test LaTeX action version error
        error_text = "uses: dante-ev/latex-action@v1.0.0"
        category = config.get_error_category(error_text)
        self.assertEqual(category, 'latex_action_version')

        # Test package missing error
        error_text = "Package fontawesome5 not found"
        category = config.get_error_category(error_text)
        self.assertEqual(category, 'package_missing')

        # Test timeout error
        error_text = "The operation was canceled"
        category = config.get_error_category(error_text)
        self.assertEqual(category, 'timeout')

    def test_unsolvable_error_detection(self):
        """Test detection of unsolvable errors."""
        solvable_error = "Package fontawesome5 not found"
        self.assertFalse(config.is_unsolvable_error(solvable_error))

        unsolvable_error = "Permission denied"
        self.assertTrue(config.is_unsolvable_error(unsolvable_error))

    def test_config_validation(self):
        """Test configuration validation."""
        # Temporarily modify config to test validation
        original_token = config.github_token
        config.github_token = None

        issues = config.validate_config()
        self.assertIn("GITHUB_TOKEN environment variable not set", issues)

        # Restore original config
        config.github_token = original_token

class TestWorkflowMonitor(unittest.TestCase):
    """Test the workflow monitoring system."""

    def setUp(self):
        """Set up test fixtures."""
        self.monitor = WorkflowMonitor()

    @patch('requests.Session.get')
    def test_get_failed_workflows(self, mock_get):
        """Test fetching failed workflows."""
        # Mock GitHub API response
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            'workflow_runs': [
                {
                    'id': 12345,
                    'name': 'Build LaTeX PDF',
                    'path': '.github/workflows/latex-build.yml',
                    'status': 'completed',
                    'conclusion': 'failure',
                    'created_at': '2024-01-01T00:00:00Z',
                    'updated_at': '2024-01-01T00:30:00Z',
                    'head_sha': 'abc123',
                    'head_branch': 'main',
                    'html_url': 'https://github.com/test/repo/actions/runs/12345',
                    'jobs_url': 'https://api.github.com/repos/test/repo/actions/runs/12345/jobs',
                    'logs_url': 'https://api.github.com/repos/test/repo/actions/runs/12345/logs'
                }
            ]
        }
        mock_get.return_value = mock_response

        failed_workflows = self.monitor.get_failed_workflows()

        self.assertEqual(len(failed_workflows), 1)
        self.assertEqual(failed_workflows[0].id, 12345)
        self.assertEqual(failed_workflows[0].workflow_name, 'Build LaTeX PDF')
        self.assertEqual(failed_workflows[0].conclusion, 'failure')

    @patch('requests.Session.get')
    def test_get_workflow_jobs(self, mock_get):
        """Test fetching workflow jobs."""
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            'jobs': [
                {
                    'id': 67890,
                    'name': 'build',
                    'status': 'completed',
                    'conclusion': 'failure',
                    'started_at': '2024-01-01T00:00:00Z',
                    'completed_at': '2024-01-01T00:30:00Z',
                    'html_url': 'https://github.com/test/repo/actions/jobs/67890'
                }
            ]
        }
        mock_get.return_value = mock_response

        jobs = self.monitor.get_workflow_jobs(12345)

        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0].id, 67890)
        self.assertEqual(jobs[0].name, 'build')
        self.assertEqual(jobs[0].conclusion, 'failure')

class TestErrorAnalyzer(unittest.TestCase):
    """Test the error analysis system."""

    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = ErrorAnalyzer()

    def test_analyze_job_log(self):
        """Test analysis of a single job log."""
        log_content = """
        Starting LaTeX compilation...
        uses: dante-ev/latex-action@v1.0.0
        Package fontawesome5 not found
        LaTeX Error: File ctmm-design.sty not found
        The operation was canceled after 15 minutes
        """

        errors = self.analyzer._analyze_job_log('test-job', log_content)

        # Should find multiple error types
        categories = {error.category for error in errors}
        self.assertIn('latex_action_version', categories)
        self.assertIn('package_missing', categories)
        self.assertIn('syntax_error', categories)
        self.assertIn('timeout', categories)

    def test_analyze_logs(self):
        """Test complete log analysis."""
        job_logs = {
            'build': """
                uses: dante-ev/latex-action@v1.0.0
                Package fontawesome5 not found
                The operation was canceled
            """,
            'test': """
                pip install failed for package PyYAML
                Could not find a version that satisfies
            """
        }

        analysis = self.analyzer.analyze_logs(12345, 'test-workflow', job_logs)

        self.assertEqual(analysis.workflow_run_id, 12345)
        self.assertEqual(analysis.workflow_name, 'test-workflow')
        self.assertGreater(analysis.total_errors, 0)
        self.assertIn('latex_action_version', analysis.error_categories)
        self.assertIn('dependency_error', analysis.error_categories)

    def test_extract_specific_values(self):
        """Test extraction of specific values from errors."""
        # Create test analysis with known errors
        errors = [
            ErrorInstance(
                category='latex_action_version',
                pattern='dante-ev/latex-action@v1.0.0',
                matched_text='uses: dante-ev/latex-action@v1.0.0',
                line_number=1,
                context='test',
                severity='high',
                job_name='test'
            )
        ]

        class MockAnalysis:
            def __init__(self):
                self.errors = errors

        mock_analysis = MockAnalysis()
        values = self.analyzer.extract_specific_values(mock_analysis, 'latex_action_version')

        self.assertIn('v1.0.0', values)

class TestFixStrategies(unittest.TestCase):
    """Test the fix strategies system."""

    def setUp(self):
        """Set up test fixtures."""
        self.strategies = FixStrategies()
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)

        # Create test workflow directory
        os.makedirs('.github/workflows', exist_ok=True)

    def tearDown(self):
        """Clean up test fixtures."""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)

    def test_find_workflow_files(self):
        """Test finding workflow files."""
        # Create test workflow files
        test_files = [
            '.github/workflows/test1.yml',
            '.github/workflows/test2.yml'
        ]

        for file_path in test_files:
            Path(file_path).touch()

        found_files = self.strategies._find_workflow_files()

        self.assertEqual(len(found_files), 2)
        self.assertIn('.github/workflows/test1.yml', found_files)
        self.assertIn('.github/workflows/test2.yml', found_files)

    def test_fix_latex_action_version(self):
        """Test LaTeX action version fixing."""
        # Create test workflow file
        workflow_content = """
name: Test
on: push
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: dante-ev/latex-action@v1.0.0
        with:
          root_file: main.tex
"""
        workflow_file = '.github/workflows/test.yml'
        with open(workflow_file, 'w') as f:
            f.write(workflow_content)

        # Create mock analysis
        class MockAnalysis:
            def __init__(self):
                self.error_categories = {'latex_action_version'}
                self.errors = []

        mock_analysis = MockAnalysis()
        result = self.strategies._fix_latex_action_version(mock_analysis)

        self.assertTrue(result.success)
        self.assertIn(workflow_file, result.files_modified)

        # Check that file was actually modified
        with open(workflow_file, 'r') as f:
            content = f.read()
        self.assertIn('dante-ev/latex-action@v2.3.0', content)

class TestPRManager(unittest.TestCase):
    """Test the PR management system."""

    def setUp(self):
        """Set up test fixtures."""
        self.pr_manager = PRManager()

    @patch('requests.Session.get')
    def test_get_open_healing_prs(self, mock_get):
        """Test fetching open healing PRs."""
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = [
            {
                'number': 123,
                'title': '🔧 Automated Workflow Fix: Test fix',
                'head': {'ref': 'workflow-healing/test-branch'},
                'created_at': '2024-01-01T00:00:00Z'
            },
            {
                'number': 124,
                'title': 'Regular PR',
                'head': {'ref': 'feature/test'},
                'created_at': '2024-01-01T00:00:00Z'
            }
        ]
        mock_get.return_value = mock_response

        healing_prs = self.pr_manager._get_open_healing_prs()

        self.assertEqual(len(healing_prs), 1)
        self.assertEqual(healing_prs[0]['number'], 123)

    def test_generate_commit_message(self):
        """Test commit message generation."""
        fix_results = [
            FixResult(
                success=True,
                description="Updated LaTeX action versions to v2.3.0",
                files_modified=[],
                changes_made=[],
                validation_passed=True
            )
        ]

        message = self.pr_manager._generate_commit_message(fix_results)

        self.assertIn('[Automated Fix]', message)
        self.assertIn('LaTeX action', message)

class TestWorkflowHealingSystem(unittest.TestCase):
    """Test the main workflow healing system."""

    def setUp(self):
        """Set up test fixtures."""
        self.healing_system = WorkflowHealingSystem(debug=True)

    @patch('workflow_healing_system.WorkflowMonitor')
    @patch('workflow_healing_system.ErrorAnalyzer')
    @patch('workflow_healing_system.FixStrategies')
    @patch('workflow_healing_system.PRManager')
    def test_system_initialization(self, mock_pr, mock_fix, mock_analyzer, mock_monitor):
        """Test system initialization."""
        system = WorkflowHealingSystem()

        self.assertIsNotNone(system.monitor)
        self.assertIsNotNone(system.analyzer)
        self.assertIsNotNone(system.fix_strategies)
        self.assertIsNotNone(system.pr_manager)

    def test_get_system_status(self):
        """Test system status reporting."""
        status = self.healing_system.get_system_status()

        self.assertIn('system_version', status)
        self.assertIn('config_valid', status)
        self.assertIn('monitored_workflows', status)
        self.assertIsInstance(status['monitored_workflows'], list)

class TestIntegration(unittest.TestCase):
    """Integration tests for the complete healing system."""

    def setUp(self):
        """Set up integration test fixtures."""
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)

        # Create test repository structure
        os.makedirs('.github/workflows', exist_ok=True)

        # Initialize git repository
        os.system('git init > /dev/null 2>&1')
        os.system('git config user.email "test@example.com"')
        os.system('git config user.name "Test User"')

    def tearDown(self):
        """Clean up integration test fixtures."""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)

    def test_dry_run_workflow(self):
        """Test a complete dry run workflow."""
        # Create test workflow file with known issues
        workflow_content = """
name: Test Workflow
on: push
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: dante-ev/latex-action@v1.0.0
        with:
          root_file: main.tex
"""
        with open('.github/workflows/test.yml', 'w') as f:
            f.write(workflow_content)

        # Mock the workflow monitor to return our test workflow
        mock_workflow = WorkflowRun(
            id=12345,
            workflow_name='Test Workflow',
            status='completed',
            conclusion='failure',
            created_at='2024-01-01T00:00:00Z',
            updated_at='2024-01-01T00:30:00Z',
            head_sha='abc123',
            head_branch='main',
            html_url='https://github.com/test/repo/actions/runs/12345',
            jobs_url='https://api.github.com/repos/test/repo/actions/runs/12345/jobs',
            logs_url='https://api.github.com/repos/test/repo/actions/runs/12345/logs'
        )

        # Mock logs with known errors
        mock_logs = {
            'build': 'uses: dante-ev/latex-action@v1.0.0\nPackage fontawesome5 not found'
        }

        healing_system = WorkflowHealingSystem()

        # Mock the components to return test data
        with patch.object(healing_system.monitor, 'get_failed_workflows', return_value=[mock_workflow]):
            with patch.object(healing_system.monitor, 'get_workflow_run_logs', return_value=mock_logs):
                # This would be a full integration test
                # For now, just verify the system can be created and configured
                status = healing_system.get_system_status()
                self.assertIsNotNone(status)

def run_comprehensive_tests():
    """Run comprehensive test suite with detailed output."""
    print("🧪 Running Comprehensive Workflow Healing System Tests")
    print("=" * 60)

    # Create test suite
    test_classes = [
        TestHealingConfig,
        TestWorkflowMonitor,
        TestErrorAnalyzer,
        TestFixStrategies,
        TestPRManager,
        TestWorkflowHealingSystem,
        TestIntegration
    ]

    total_tests = 0
    passed_tests = 0
    failed_tests = []

    for test_class in test_classes:
        print(f"\n📋 Testing {test_class.__name__}")
        print("-" * 40)

        suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
        runner = unittest.TextTestRunner(verbosity=1, stream=open(os.devnull, 'w'))
        result = runner.run(suite)

        class_total = result.testsRun
        class_passed = class_total - len(result.failures) - len(result.errors)

        total_tests += class_total
        passed_tests += class_passed

        print(f"   Tests run: {class_total}")
        print(f"   Passed: {class_passed}")

        if result.failures:
            print(f"   Failures: {len(result.failures)}")
            for test, traceback in result.failures:
                failed_tests.append(f"{test_class.__name__}.{test._testMethodName}: FAILURE")

        if result.errors:
            print(f"   Errors: {len(result.errors)}")
            for test, traceback in result.errors:
                failed_tests.append(f"{test_class.__name__}.{test._testMethodName}: ERROR")

        status = "✅ PASSED" if class_passed == class_total else "❌ FAILED"
        print(f"   Status: {status}")

    # Summary
    print(f"\n{'=' * 60}")
    print(f"📊 TEST SUMMARY")
    print(f"{'=' * 60}")
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {total_tests - passed_tests}")
    print(f"Success Rate: {(passed_tests / total_tests * 100):.1f}%")

    if failed_tests:
        print(f"\n❌ Failed Tests:")
        for test in failed_tests:
            print(f"   - {test}")

    overall_status = "✅ ALL TESTS PASSED" if passed_tests == total_tests else "❌ SOME TESTS FAILED"
    print(f"\n{overall_status}")

    return passed_tests == total_tests

if __name__ == "__main__":
    success = run_comprehensive_tests()
    sys.exit(0 if success else 1)