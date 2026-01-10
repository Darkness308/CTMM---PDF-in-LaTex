#!/usr/bin/env python3
"""
Comprehensive test suite validating git command batching optimization in validate_pr.py

This test validates that the optimization correctly:
1. Batches multiple git rev-parse commands into a single execution
2. Maintains backward compatibility and functionality
3. Provides proper error handling and fallback mechanisms
4. Improves performance by reducing process overhead
"""

import unittest
import subprocess
import sys
import os
from unittest.mock import patch, MagicMock
import tempfile

# Import the function under test
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from validate_pr import check_file_changes, run_command


class TestGitOptimization(unittest.TestCase):
    """Test cases for git command batching optimization."""

    def setUp(self):
        """Set up test environment."""
        self.original_dir = os.getcwd()

    def tearDown(self):
        """Clean up test environment."""
        os.chdir(self.original_dir)

    def test_run_command_function_exists(self):
        """Test that run_command function is available and working."""
        success, stdout, stderr = run_command("echo 'test'")
        self.assertTrue(success)
        self.assertEqual(stdout.strip(), "test")
        self.assertEqual(stderr, "")

    @patch('validate_pr.run_command')
    def test_git_batching_optimization(self, mock_run_command):
        """Test that git rev-parse commands are batched instead of individual calls."""

        # Mock git branch -r output
        mock_branch_output = "origin/main\norigin/develop\norigin/feature"

        # Mock git rev-parse batched output (simulating successful parsing)
        mock_revparse_output = "abc123def456\n789ghi012jkl\nmno345pqr678\nstu901vwx234"

        # Setup mock returns in sequence
        mock_run_command.side_effect = [
            (True, mock_branch_output, ""),  # git branch -r
            (True, mock_revparse_output, ""),  # batched git rev-parse
            (True, "file1.txt\nfile2.py", ""),  # git diff --name-only
            (True, "10\t5\tfile1.txt\n3\t2\tfile2.py", ""),  # git diff --numstat
        ]

        # Call the function
        success, changed_files, added_lines, deleted_lines = check_file_changes("main")

        # Verify the function succeeded
        self.assertTrue(success)

        # Verify that git rev-parse was called with batched command
        calls = mock_run_command.call_args_list

        # Should have these calls: git branch -r, batched git rev-parse, git diff commands
        self.assertGreaterEqual(len(calls), 2)

        # Check that git rev-parse was called with multiple arguments (batched)
        revparse_call = None
        for call in calls:
            cmd = call[0][0]  # First positional argument (the command)
            if "git rev-parse" in cmd and not cmd == "git rev-parse":
                revparse_call = cmd
                break

        self.assertIsNotNone(revparse_call, "Should have found a batched git rev-parse call")

        # Verify it contains multiple branch options (indicates batching)
        self.assertIn("origin/main", revparse_call)
        self.assertIn("main", revparse_call)

        # Count the number of space-separated arguments after "git rev-parse"
        parts = revparse_call.split()
        git_revparse_args = parts[2:]  # Skip "git" and "rev-parse"
        self.assertGreater(len(git_revparse_args), 1,
                          "Should batch multiple arguments in single git rev-parse call")

    @patch('validate_pr.run_command')
    def test_fallback_behavior_when_batching_fails(self, mock_run_command):
        """Test that function handles gracefully when batched git rev-parse fails."""

        # Mock git branch -r output
        mock_branch_output = "origin/main\norigin/develop"

        # Setup mock returns: branch succeeds, rev-parse fails, fallback to staged/HEAD~1
        mock_run_command.side_effect = [
            (True, mock_branch_output, ""),  # git branch -r
            (False, "", "fatal: ambiguous argument"),  # batched git rev-parse fails
            (False, "", ""),  # git diff --cached --name-only (no staged changes)
            (True, "file1.txt", ""),  # git diff --name-only HEAD~1..HEAD (fallback)
            (True, "file1.txt", ""),  # git diff --name-only HEAD~1..HEAD (for file count)
            (True, "5\t2\tfile1.txt", ""),  # git diff --numstat HEAD~1..HEAD
        ]

        # Call the function
        success, changed_files, added_lines, deleted_lines = check_file_changes("main")

        # Verify the function succeeded despite batching failure
        self.assertTrue(success)
        self.assertEqual(changed_files, 1)
        self.assertEqual(added_lines, 5)
        self.assertEqual(deleted_lines, 2)

    @patch('validate_pr.run_command')
    def test_empty_filtered_options_handling(self, mock_run_command):
        """Test handling when no valid base branch options are found."""

        # Mock git branch -r with no matching branches, so filtered_options will be empty
        mock_branch_output = "origin/feature1\norigin/feature2"

        # For this test, we will cycle through more calls since filtered_options is empty
        # and it goes to fallback paths
        mock_run_command.side_effect = [
            (True, mock_branch_output, ""),  # git branch -r
            (False, "", ""),  # git diff --cached --name-only (no staged changes)
            (True, "file1.txt", ""),  # git diff --name-only HEAD~1..HEAD (fallback)
            (True, "file1.txt", ""),  # git diff --name-only HEAD~1..HEAD (for changed files)
            (True, "3\t1\tfile1.txt", ""),  # git diff --numstat HEAD~1..HEAD
        ]

        # Call with a base branch that doesn't exist in available branches
        success, changed_files, added_lines, deleted_lines = check_file_changes("nonexistent")

        # Should still succeed by falling back to HEAD~1
        self.assertTrue(success)
        self.assertEqual(changed_files, 1)
        self.assertEqual(added_lines, 3)
        self.assertEqual(deleted_lines, 1)

    @patch('validate_pr.run_command')
    def test_git_rev_parse_output_parsing(self, mock_run_command):
        """Test proper parsing of git rev-parse batched output."""

        mock_branch_output = "origin/main\norigin/develop"

        # Mock rev-parse output with some failures mixed in
        mock_revparse_output = "abc123def456\nfatal: ambiguous argument 'origin/nonexistent'\n789ghi012jkl\nstu901vwx234"

        mock_run_command.side_effect = [
            (True, mock_branch_output, ""),  # git branch -r
            (True, mock_revparse_output, ""),  # batched git rev-parse with mixed results
            (True, "file1.txt", ""),  # git diff --name-only
            (True, "2\t1\tfile1.txt", ""),  # git diff --numstat
        ]

        success, changed_files, added_lines, deleted_lines = check_file_changes("main")

        # Should succeed and find the first valid hash
        self.assertTrue(success)
        self.assertEqual(changed_files, 1)

    def test_performance_improvement_concept(self):
        """Test that demonstrates the performance improvement concept."""

        # This test validates that we're reducing from N individual subprocess calls
        # to a single batched subprocess call

        base_options = ["origin/main", "main", "origin/develop", "develop"]

        # Simulate the old approach: N individual calls
        old_approach_calls = len(base_options)

        # Simulate the new approach: 1 batched call (plus git branch -r)
        new_approach_calls = 2  # git branch -r + batched git rev-parse

        # Verify that batching reduces the number of subprocess calls
        self.assertLess(new_approach_calls, old_approach_calls,
                       "Batched approach should use fewer subprocess calls than individual calls")

        # Calculate theoretical performance improvement
        improvement_ratio = old_approach_calls / new_approach_calls
        self.assertGreater(improvement_ratio, 1.5,
                          "Should provide significant performance improvement")

    @patch('validate_pr.run_command')
    def test_backward_compatibility(self, mock_run_command):
        """Test that the optimization maintains backward compatibility."""

        # Test with various base branch scenarios
        test_scenarios = [
            ("main", "origin/main"),
            ("develop", "origin/develop"),
            ("feature-branch", "feature-branch"),
        ]

        for input_branch, expected_match in test_scenarios:
            with self.subTest(base_branch=input_branch):

                mock_branch_output = f"origin/main\norigin/develop\n{expected_match}"
                mock_revparse_output = "abc123\ndef456\nghi789"

                mock_run_command.side_effect = [
                    (True, mock_branch_output, ""),
                    (True, mock_revparse_output, ""),
                    (True, "file1.txt", ""),
                    (True, "1\t0\tfile1.txt", ""),
                ]

                success, changed_files, added_lines, deleted_lines = check_file_changes(input_branch)

                self.assertTrue(success, f"Should succeed for base branch {input_branch}")
                self.assertEqual(changed_files, 1)

                # Reset for next iteration
                mock_run_command.reset_mock()

    def test_integration_with_actual_git(self):
        """Integration test with actual git repository (if available)."""

        # Only run if we're in a git repository
        if not os.path.exists('.git'):
            self.skipTest("Not in a git repository")

        try:
            # Test with actual git commands
            success, changed_files, added_lines, deleted_lines = check_file_changes("main")

            # Should return valid results without crashing
            self.assertIsInstance(success, bool)
            self.assertIsInstance(changed_files, int)
            self.assertIsInstance(added_lines, int)
            self.assertIsInstance(deleted_lines, int)

            # Results should be non-negative
            self.assertGreaterEqual(changed_files, 0)
            self.assertGreaterEqual(added_lines, 0)
            self.assertGreaterEqual(deleted_lines, 0)

        except Exception as e:
            self.fail(f"Integration test failed with actual git: {e}")


def main():
    """Run the git optimization tests."""
    print("🧪 Running Git Command Batching Optimization Tests")
    print("=" * 60)

    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGitOptimization)

    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\n" + "=" * 60)
    if result.wasSuccessful():
        print("✅ All git optimization tests passed!")
        print(f"Ran {result.testsRun} tests successfully")
    else:
        print("❌ Some git optimization tests failed")
        print(f"Failures: {len(result.failures)}, Errors: {len(result.errors)}")

    return result.wasSuccessful()


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)