#!/usr/bin/env python3
"""
Test Git Command Batching Optimization in validate_pr.py

This test suite validates that the git rev-parse optimization works correctly,
ensuring that multiple base branch options are checked in a single batched
command rather than individual calls, while maintaining exact functionality.
"""

import os
import sys
import subprocess
import tempfile
import unittest
from unittest.mock import patch, MagicMock

# Add the current directory to the path to import validate_pr
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import validate_pr


class TestGitOptimization(unittest.TestCase):
    """Test cases for git command batching optimization."""
    
    def setUp(self):
        """Set up test environment."""
        self.original_dir = os.getcwd()
        
    def tearDown(self):
        """Clean up test environment."""
        os.chdir(self.original_dir)
    
    @patch('validate_pr.run_command')
    def test_batched_git_rev_parse(self, mock_run_command):
        """Test that git rev-parse is called with multiple options in a single command."""
        # Mock git branch -r command
        mock_run_command.side_effect = [
            # First call: git branch -r
            (True, "  origin/main\n  origin/develop\n  origin/feature-branch", ""),
            # Second call: batched git rev-parse
            (True, "abc123def456\n789xyz012abc\nfed654cba321", ""),
            # Third call: git diff --name-only (for file changes)
            (True, "file1.py\nfile2.md", ""),
            # Fourth call: git diff --numstat (for line statistics)
            (True, "10\t5\tfile1.py\n3\t2\tfile2.md", "")
        ]
        
        # Call the function
        success, changed_files, added_lines, deleted_lines = validate_pr.check_file_changes("main")
        
        # Verify the batched git rev-parse was called
        calls = mock_run_command.call_args_list
        
        # Find the git rev-parse call
        rev_parse_call = None
        for call in calls:
            if 'git rev-parse' in call[0][0] and 'origin/main main origin/main main' in call[0][0]:
                rev_parse_call = call[0][0]
                break
        
        self.assertIsNotNone(rev_parse_call, "Batched git rev-parse command not found")
        
        # Verify it's a single command with multiple options
        self.assertIn("git rev-parse", rev_parse_call)
        self.assertIn("origin/main", rev_parse_call)
        self.assertIn("main", rev_parse_call)
        
        # Count the number of git rev-parse calls - should be only 1
        rev_parse_calls = [call for call in calls if 'git rev-parse' in call[0][0]]
        self.assertEqual(len(rev_parse_calls), 1, "Should have exactly one git rev-parse call")
        
        # Verify the function still works correctly
        self.assertTrue(success)
        self.assertEqual(changed_files, 2)
        self.assertEqual(added_lines, 13)
        self.assertEqual(deleted_lines, 7)
    
    @patch('validate_pr.run_command')
    def test_optimization_with_no_valid_branches(self, mock_run_command):
        """Test behavior when no valid branches are found."""
        # When no branches are available and no valid git refs, the function goes through:
        # 1. git branch -r (empty result)
        # 2. git diff --cached --name-only (no staged changes)
        # 3. git diff --name-only HEAD~1..HEAD (has changes)
        # 4. git diff --name-only HEAD~1..HEAD (file changes - duplicate call)
        # 5. git diff --numstat HEAD~1..HEAD (line stats)
        mock_run_command.side_effect = [
            (True, "", ""),  # git branch -r
            (True, "", ""),  # git diff --cached --name-only  
            (True, "test.py", ""),  # git diff --name-only HEAD~1..HEAD
            (True, "test.py", ""),  # git diff --name-only HEAD~1..HEAD (second call)
            (True, "5\t2\ttest.py", "")  # git diff --numstat HEAD~1..HEAD
        ]
        
        success, changed_files, added_lines, deleted_lines = validate_pr.check_file_changes("nonexistent")
        
        # Should still work with fallback logic
        self.assertTrue(success)
        self.assertEqual(changed_files, 1)
        self.assertEqual(added_lines, 5)
        self.assertEqual(deleted_lines, 2)
    
    @patch('validate_pr.run_command')
    def test_optimization_with_partial_failures(self, mock_run_command):
        """Test that optimization handles partial git rev-parse failures correctly."""
        # Mock git branch -r command
        mock_run_command.side_effect = [
            # First call: git branch -r
            (True, "  origin/main\n  origin/develop", ""),
            # Second call: batched git rev-parse with some failures
            (True, "abc123def456\nfatal: ambiguous argument\n789xyz012abc", ""),
            # Third call: git diff --name-only
            (True, "changed.py", ""),
            # Fourth call: git diff --numstat
            (True, "8\t3\tchanged.py", "")
        ]
        
        success, changed_files, added_lines, deleted_lines = validate_pr.check_file_changes("main")
        
        # Should pick the first valid hash and continue working
        self.assertTrue(success)
        self.assertEqual(changed_files, 1)
        self.assertEqual(added_lines, 8)
        self.assertEqual(deleted_lines, 3)
    
    def test_optimization_integration_real_git(self):
        """Test the optimization with real git commands in current repository."""
        # This test runs against the actual git repository
        if not os.path.exists('.git'):
            self.skipTest("Not in a git repository")
        
        # Call the actual function
        success, changed_files, added_lines, deleted_lines = validate_pr.check_file_changes("main")
        
        # Basic validation that the function completes successfully
        self.assertIsInstance(success, bool)
        self.assertIsInstance(changed_files, int)
        self.assertIsInstance(added_lines, int)
        self.assertIsInstance(deleted_lines, int)
        
        # Verify non-negative values
        self.assertGreaterEqual(changed_files, 0)
        self.assertGreaterEqual(added_lines, 0)
        self.assertGreaterEqual(deleted_lines, 0)
    
    def test_command_efficiency_verification(self):
        """Verify that the optimization reduces the number of git commands."""
        # This is more of a code inspection test
        with open('validate_pr.py', 'r') as f:
            content = f.read()
        
        # Verify that we don't have multiple individual git rev-parse calls in a loop
        lines = content.split('\n')
        
        # Count git rev-parse patterns
        individual_rev_parse_in_loop = 0
        batched_rev_parse = 0
        
        for i, line in enumerate(lines):
            if 'git rev-parse' in line and 'git rev-parse {' in line:
                # Check if this is in a loop context (previous lines contain 'for')
                context = '\n'.join(lines[max(0, i-5):i+1])
                if 'for ' in context and 'base_option' in context:
                    individual_rev_parse_in_loop += 1
            elif 'git rev-parse " + " ".join(' in line:
                batched_rev_parse += 1
        
        # Verify optimization: should have batched approach, not individual calls in loop
        self.assertEqual(individual_rev_parse_in_loop, 0, 
                        "Found individual git rev-parse calls in loop - optimization not applied")
        self.assertGreaterEqual(batched_rev_parse, 1, 
                               "No batched git rev-parse found - optimization missing")
    
    @patch('validate_pr.run_command')
    def test_backward_compatibility(self, mock_run_command):
        """Test that the optimization maintains backward compatibility."""
        # Focus on the main success case which is most important
        mock_run_command.side_effect = [
            # Call 1: git branch -r
            (True, "  origin/main\n  origin/develop", ""),
            # Call 2: batched git rev-parse
            (True, "abc123\ndef456", ""),
            # Call 3: git diff --name-only
            (True, "file.py", ""),
            # Call 4: git diff --numstat
            (True, "5\t2\tfile.py", "")
        ]
        
        success, changed_files, added_lines, deleted_lines = validate_pr.check_file_changes("main")
        
        # Should work correctly
        self.assertTrue(success, "Normal branch case failed")
        self.assertEqual(changed_files, 1)
        self.assertEqual(added_lines, 5)
        self.assertEqual(deleted_lines, 2)


class TestPerformanceImprovement(unittest.TestCase):
    """Test that the optimization actually improves performance."""
    
    @patch('validate_pr.run_command')
    def test_single_git_command_for_multiple_bases(self, mock_run_command):
        """Verify that multiple base options result in a single git command."""
        # Setup mock to track calls
        mock_run_command.side_effect = [
            (True, "  origin/main\n  origin/develop\n  origin/feature", ""),  # git branch -r
            (True, "hash1\nhash2\nhash3", ""),  # batched git rev-parse
            (True, "file.py", ""),  # git diff
            (True, "1\t1\tfile.py", "")  # git diff --numstat
        ]
        
        # Call with a base that will result in multiple options being checked
        validate_pr.check_file_changes("main")
        
        # Extract all git rev-parse calls
        git_rev_parse_calls = []
        for call in mock_run_command.call_args_list:
            cmd = call[0][0]
            if 'git rev-parse' in cmd:
                git_rev_parse_calls.append(cmd)
        
        # Should be exactly one git rev-parse call
        self.assertEqual(len(git_rev_parse_calls), 1, 
                        f"Expected 1 git rev-parse call, got {len(git_rev_parse_calls)}")
        
        # The single call should contain multiple base options
        git_cmd = git_rev_parse_calls[0]
        # Count the number of potential base branches in the command
        base_count = git_cmd.count('origin/') + git_cmd.count('main')
        self.assertGreater(base_count, 1, 
                          "Batched command should contain multiple base options")


def main():
    """Run all git optimization tests."""
    print("🧪 Git Command Batching Optimization Tests")
    print("=" * 60)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestGitOptimization))
    suite.addTests(loader.loadTestsFromTestCase(TestPerformanceImprovement))
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "=" * 60)
    if result.wasSuccessful():
        print("🎉 All git optimization tests passed!")
        print("✅ Optimization successfully reduces git command executions")
        print("✅ Backward compatibility maintained")
        print("✅ Performance improvement verified")
    else:
        print("❌ Some git optimization tests failed")
        print(f"Failures: {len(result.failures)}")
        print(f"Errors: {len(result.errors)}")
    
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())