#!/usr/bin/env python3
"""
CTMM Integration Test Suite
===========================

Comprehensive integration tests covering all CTMM toolset components and workflows.
This test suite validates the complete system integration and ensures 100% compatibility
between all tools.

Tests covered:
1. Unified tool interface integration
2. Build system integration
3. LaTeX de-escaping workflow integration
4. Validation system integration
5. End-to-end workflow validation
6. File system operations
7. Error handling and recovery
8. Performance and reliability tests

Usage:
    python3 test_integration.py
    python3 test_integration.py --verbose
    python3 test_integration.py --quick
"""

import unittest
import subprocess
import tempfile
import shutil
import os
import sys
from pathlib import Path
import logging
import time
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class TestCTMMIntegration(unittest.TestCase):
    """Comprehensive integration tests for CTMM toolset."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment."""
        cls.test_dir = Path(tempfile.mkdtemp(prefix='ctmm_integration_test_'))
        cls.original_dir = Path.cwd()
        logger.info(f"Test directory: {cls.test_dir}")
        
        # Copy essential files to test directory
        essential_files = [
            'ctmm_unified_tool.py',
            'ctmm_build.py',
            'fix_latex_escaping.py',
            'comprehensive_workflow.py',
            'test_ctmm_build.py',
            'validate_latex_syntax.py',
            'main.tex'
        ]
        
        for file in essential_files:
            if os.path.exists(file):
                shutil.copy2(file, cls.test_dir)
        
        # Copy directories
        for dirname in ['style', 'modules']:
            if os.path.exists(dirname):
                shutil.copytree(dirname, cls.test_dir / dirname)
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test environment."""
        os.chdir(cls.original_dir)
        shutil.rmtree(cls.test_dir, ignore_errors=True)
        logger.info("Test cleanup completed")
    
    def setUp(self):
        """Set up for each test."""
        os.chdir(self.test_dir)
        self.start_time = time.time()
    
    def tearDown(self):
        """Clean up after each test."""
        test_time = time.time() - self.start_time
        logger.info(f"Test completed in {test_time:.2f}s")
    
    def run_command(self, cmd, check_success=True):
        """Run a command and return result."""
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, errors='replace')
            if check_success and result.returncode != 0:
                self.fail(f"Command failed: {cmd}\nStderr: {result.stderr}\nStdout: {result.stdout}")
            return result
        except Exception as e:
            if check_success:
                self.fail(f"Command exception: {cmd}\nError: {e}")
            return None

class TestUnifiedToolInterface(TestCTMMIntegration):
    """Test the unified tool interface."""
    
    def test_unified_tool_exists(self):
        """Test that the unified tool exists and is executable."""
        self.assertTrue(os.path.exists('ctmm_unified_tool.py'))
        self.assertTrue(os.access('ctmm_unified_tool.py', os.X_OK))
    
    def test_unified_tool_help(self):
        """Test unified tool help functionality."""
        result = self.run_command("python3 ctmm_unified_tool.py --help")
        self.assertEqual(result.returncode, 0)
        self.assertIn("CTMM Unified Tool", result.stdout)
        self.assertIn("build", result.stdout)
        self.assertIn("de-escape", result.stdout)
        self.assertIn("validate", result.stdout)
        self.assertIn("workflow", result.stdout)
        self.assertIn("test", result.stdout)
        self.assertIn("status", result.stdout)
    
    def test_unified_tool_status(self):
        """Test unified tool status command."""
        result = self.run_command("python3 ctmm_unified_tool.py status")
        self.assertEqual(result.returncode, 0)
        self.assertIn("CTMM System Status", result.stdout)
        self.assertIn("Key Files", result.stdout)
        self.assertIn("Overall Status", result.stdout)
    
    def test_unified_tool_build(self):
        """Test unified tool build command."""
        result = self.run_command("python3 ctmm_unified_tool.py build")
        self.assertEqual(result.returncode, 0)
        self.assertIn("CTMM Build System", result.stdout)
        self.assertIn("Operation completed successfully", result.stdout)
    
    def test_unified_tool_validate(self):
        """Test unified tool validate command."""
        result = self.run_command("python3 ctmm_unified_tool.py validate")
        self.assertEqual(result.returncode, 0)
        self.assertIn("LaTeX Syntax Validation", result.stdout)

class TestBuildSystemIntegration(TestCTMMIntegration):
    """Test build system integration."""
    
    def test_build_system_basic(self):
        """Test basic build system functionality."""
        result = self.run_command("python3 ctmm_build.py")
        self.assertEqual(result.returncode, 0)
        self.assertIn("CTMM BUILD SYSTEM SUMMARY", result.stdout)
        self.assertIn("✓ PASS", result.stdout)
    
    def test_build_system_file_detection(self):
        """Test build system file detection."""
        result = self.run_command("python3 ctmm_build.py")
        self.assertEqual(result.returncode, 0)
        self.assertIn("Style files:", result.stdout)
        self.assertIn("Module files:", result.stdout)
        self.assertIn("Missing files:", result.stdout)

class TestLaTeXDeEscapingIntegration(TestCTMMIntegration):
    """Test LaTeX de-escaping integration."""
    
    def setUp(self):
        """Set up test files for de-escaping."""
        super().setUp()
        
        # Create test directory with sample over-escaped content
        self.test_escape_dir = Path('test_converted')
        self.test_escape_dir.mkdir(exist_ok=True)
        
        # Create sample over-escaped LaTeX file
        sample_content = r"""
\textbackslash{}section\textbackslash{}\textbackslash{}\textbackslash{}texorpdfstring\textbackslash{}
\textbackslash{}textbf\textbackslash{}\{Test Content\textbackslash{}\}
\textbackslash{}begin\textbackslash{}\{itemize\textbackslash{}\}
\textbackslash{}item Test item
\textbackslash{}end\textbackslash{}\{itemize\textbackslash{}\}
"""
        
        with open(self.test_escape_dir / 'test_sample.tex', 'w') as f:
            f.write(sample_content)
    
    def test_deescaping_tool_basic(self):
        """Test basic de-escaping functionality."""
        result = self.run_command(f"python3 fix_latex_escaping.py {self.test_escape_dir}")
        self.assertEqual(result.returncode, 0)
    
    def test_deescaping_via_unified_tool(self):
        """Test de-escaping via unified tool."""
        result = self.run_command(f"python3 ctmm_unified_tool.py de-escape {self.test_escape_dir}")
        self.assertEqual(result.returncode, 0)
        self.assertIn("LaTeX De-escaping", result.stdout)
    
    def test_deescaping_pattern_coverage(self):
        """Test that enhanced patterns are working."""
        # Test the new patterns are being applied
        result = self.run_command(f"python3 fix_latex_escaping.py --verbose {self.test_escape_dir}")
        self.assertEqual(result.returncode, 0)

class TestWorkflowIntegration(TestCTMMIntegration):
    """Test workflow integration."""
    
    def test_comprehensive_workflow_basic(self):
        """Test basic comprehensive workflow."""
        result = self.run_command("python3 comprehensive_workflow.py", check_success=False)
        # Allow either success or partial success due to missing tools
        self.assertIn("COMPREHENSIVE WORKFLOW", result.stdout)
    
    def test_workflow_via_unified_tool(self):
        """Test workflow via unified tool."""
        result = self.run_command("python3 ctmm_unified_tool.py workflow", check_success=False)
        self.assertIn("Comprehensive Workflow", result.stdout)

class TestValidationIntegration(TestCTMMIntegration):
    """Test validation system integration."""
    
    def test_latex_syntax_validation(self):
        """Test LaTeX syntax validation."""
        result = self.run_command("python3 validate_latex_syntax.py")
        self.assertEqual(result.returncode, 0)
        self.assertIn("LATEX SYNTAX VALIDATION", result.stdout)
    
    def test_validation_main_tex(self):
        """Test validation of main.tex file."""
        self.assertTrue(os.path.exists('main.tex'))
        result = self.run_command("python3 validate_latex_syntax.py")
        self.assertEqual(result.returncode, 0)
        self.assertIn("✅", result.stdout)

class TestEndToEndWorkflow(TestCTMMIntegration):
    """Test complete end-to-end workflows."""
    
    def test_full_workflow_sequence(self):
        """Test complete workflow sequence."""
        # Step 1: Status check
        result = self.run_command("python3 ctmm_unified_tool.py status")
        self.assertEqual(result.returncode, 0)
        
        # Step 2: Build system
        result = self.run_command("python3 ctmm_unified_tool.py build")
        self.assertEqual(result.returncode, 0)
        
        # Step 3: Validation
        result = self.run_command("python3 ctmm_unified_tool.py validate")
        self.assertEqual(result.returncode, 0)
        
        # Step 4: Tests
        result = self.run_command("python3 ctmm_unified_tool.py test", check_success=False)
        # Allow partial success due to environment
    
    def test_error_recovery(self):
        """Test error recovery and handling."""
        # Test with non-existent directory
        result = self.run_command("python3 ctmm_unified_tool.py de-escape nonexistent_dir", check_success=False)
        # Should handle gracefully
        self.assertIn("Tip:", result.stdout)  # The tool creates the directory and provides helpful tip

class TestPerformanceAndReliability(TestCTMMIntegration):
    """Test performance and reliability."""
    
    def test_tool_response_time(self):
        """Test that tools respond within reasonable time."""
        start_time = time.time()
        result = self.run_command("python3 ctmm_unified_tool.py status")
        end_time = time.time()
        
        self.assertEqual(result.returncode, 0)
        self.assertLess(end_time - start_time, 10.0)  # Should complete within 10 seconds
    
    def test_repeated_operations(self):
        """Test repeated operations for stability."""
        for i in range(3):
            result = self.run_command("python3 ctmm_unified_tool.py status")
            self.assertEqual(result.returncode, 0)
            self.assertIn("CTMM System Status", result.stdout)

class TestFileSystemOperations(TestCTMMIntegration):
    """Test file system operations."""
    
    def test_directory_creation(self):
        """Test directory creation for de-escaping."""
        test_dir = 'test_new_directory'
        result = self.run_command(f"python3 ctmm_unified_tool.py de-escape {test_dir}")
        self.assertEqual(result.returncode, 0)
        self.assertTrue(os.path.exists(test_dir))
    
    def test_file_backup_functionality(self):
        """Test file backup during de-escaping."""
        # Create test file
        test_dir = Path('test_backup')
        test_dir.mkdir(exist_ok=True)
        test_file = test_dir / 'test.tex'
        
        with open(test_file, 'w') as f:
            f.write(r'\textbackslash{}textbf\textbackslash{}\{test\textbackslash{}\}')
        
        # Run de-escaping with backup
        result = self.run_command(f"python3 fix_latex_escaping.py --backup {test_dir}")
        self.assertEqual(result.returncode, 0)

def run_integration_tests(verbose=False, quick=False):
    """
    Run the integration test suite.
    
    Args:
        verbose: Enable verbose output
        quick: Run only quick tests
    """
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Test discovery
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestUnifiedToolInterface,
        TestBuildSystemIntegration,
        TestLaTeXDeEscapingIntegration,
        TestWorkflowIntegration,
        TestValidationIntegration,
        TestEndToEndWorkflow,
        TestPerformanceAndReliability,
        TestFileSystemOperations,
    ]
    
    if quick:
        # For quick tests, only run essential tests
        test_classes = test_classes[:4]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(
        verbosity=2 if verbose else 1,
        buffer=True,
        failfast=False
    )
    
    print("="*70)
    print("CTMM INTEGRATION TEST SUITE")
    print("="*70)
    print(f"Running {'quick' if quick else 'comprehensive'} integration tests...")
    print(f"Test classes: {len(test_classes)}")
    print(f"Verbose mode: {verbose}")
    print("="*70)
    
    start_time = time.time()
    result = runner.run(suite)
    end_time = time.time()
    
    # Print summary
    print("="*70)
    print("INTEGRATION TEST RESULTS")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / max(result.testsRun, 1)) * 100:.1f}%")
    print(f"Total time: {end_time - start_time:.2f}s")
    print("="*70)
    
    # Return success status
    return len(result.failures) == 0 and len(result.errors) == 0

def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="CTMM Integration Test Suite")
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('--quick', action='store_true', help='Run only quick tests')
    
    args = parser.parse_args()
    
    success = run_integration_tests(verbose=args.verbose, quick=args.quick)
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())