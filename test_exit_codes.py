#!/usr/bin/env python3
"""
Test to verify that main() functions return proper exit codes
instead of calling sys.exit() directly.

This addresses issue #304 about proper exit code handling.
"""

import sys
import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path

# Add the current directory to the path to import modules
sys.path.insert(0, str(Path(__file__).parent))

import ctmm_build
import build_system
import test_ctmm_build


class TestExitCodeHandling(unittest.TestCase):
    """Test that main() functions return exit codes instead of calling sys.exit()."""

    def test_ctmm_build_main_returns_exit_code(self):
        """Test that ctmm_build.main() returns an integer exit code."""
        # Mock subprocess.run to avoid needing pdflatex
        with patch('ctmm_build.subprocess.run') as mock_run:
            # Simulate successful pdflatex run
            mock_run.return_value = MagicMock(returncode=0)
            
            result = ctmm_build.main()
            
            # Should return an integer (exit code), not call sys.exit
            self.assertIsInstance(result, int)
            self.assertIn(result, [0, 1])  # Valid exit codes

    def test_build_system_main_returns_exit_code(self):
        """Test that build_system.main() returns an integer exit code."""
        # Mock sys.argv to provide arguments
        test_args = ['build_system.py', '--main-tex', 'main.tex']
        
        with patch('sys.argv', test_args):
            # Mock subprocess.run to avoid needing pdflatex
            with patch('build_system.subprocess.run') as mock_run:
                # Simulate successful pdflatex run
                mock_run.return_value = MagicMock(returncode=0)
                
                result = build_system.main()
                
                # Should return an integer (exit code), not call sys.exit
                self.assertIsInstance(result, int)
                self.assertIn(result, [0, 1])  # Valid exit codes

    def test_test_ctmm_build_main_returns_exit_code(self):
        """Test that test_ctmm_build.main() returns an integer exit code."""
        result = test_ctmm_build.main()
        
        # Should return an integer (exit code), not call sys.exit
        self.assertIsInstance(result, int)
        self.assertIn(result, [0, 1])  # Valid exit codes

    def test_main_functions_dont_call_sys_exit_directly(self):
        """Test that main() functions don't call sys.exit() directly."""
        
        # Test ctmm_build.main()
        with patch('ctmm_build.subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            with patch('sys.exit') as mock_exit:
                result = ctmm_build.main()
                # sys.exit should not be called inside main()
                mock_exit.assert_not_called()
                self.assertIsInstance(result, int)

        # Test build_system.main()  
        test_args = ['build_system.py', '--main-tex', 'main.tex']
        with patch('sys.argv', test_args):
            with patch('build_system.subprocess.run') as mock_run:
                mock_run.return_value = MagicMock(returncode=0)
                with patch('sys.exit') as mock_exit:
                    result = build_system.main()
                    # sys.exit should not be called inside main()
                    mock_exit.assert_not_called() 
                    self.assertIsInstance(result, int)

        # Test test_ctmm_build.main()
        with patch('sys.exit') as mock_exit:
            result = test_ctmm_build.main()
            # sys.exit should not be called inside main()
            mock_exit.assert_not_called()
            self.assertIsInstance(result, int)


def main():
    """Run the exit code tests and return exit code."""
    # Create a test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestExitCodeHandling)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return success status
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())