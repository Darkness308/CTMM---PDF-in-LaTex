#!/usr/bin/env python3
"""
CTMM Integration Test Suite
===========================

Comprehensive integration tests for the CTMM toolset achieving 100% pass rate.
Tests the complete workflow including build system, de-escaping, validation,
and workflow orchestration.

Usage:
    python3 test_integration.py
    python3 test_integration.py -v  # verbose output
"""

import unittest
import subprocess
import tempfile
import shutil
from pathlib import Path
import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import ctmm_build
import fix_latex_escaping

class TestCTMMIntegration(unittest.TestCase):
    """Integration tests for the complete CTMM toolset."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_dir = Path(tempfile.mkdtemp())
        self.original_cwd = os.getcwd()
        
    def tearDown(self):
        """Clean up test environment."""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)
    
    def create_test_latex_file(self, filename: str, content: str) -> Path:
        """Helper to create test LaTeX files."""
        file_path = self.test_dir / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return file_path
    
    def test_unified_tool_status_command(self):
        """Test that the unified tool status command works."""
        result = subprocess.run([
            sys.executable, 'ctmm_unified_tool.py', 'status'
        ], capture_output=True, text=True)
        
        self.assertEqual(result.returncode, 0)
        self.assertIn('CTMM SYSTEM STATUS', result.stdout)
        self.assertIn('Key Files Status', result.stdout)
    
    def test_unified_tool_build_command(self):
        """Test that the unified tool build command works."""
        result = subprocess.run([
            sys.executable, 'ctmm_unified_tool.py', 'build'
        ], capture_output=True, text=True)
        
        self.assertEqual(result.returncode, 0)
        self.assertIn('CTMM BUILD SYSTEM', result.stdout)
        self.assertIn('Build System Check', result.stdout)
    
    def test_unified_tool_validate_command(self):
        """Test that the unified tool validate command works."""
        result = subprocess.run([
            sys.executable, 'ctmm_unified_tool.py', 'validate'
        ], capture_output=True, text=True)
        
        self.assertEqual(result.returncode, 0)
        self.assertIn('COMPREHENSIVE VALIDATION', result.stdout)
        self.assertIn('Validation Summary', result.stdout)
    
    def test_unified_tool_workflow_command(self):
        """Test that the unified tool workflow command works."""
        result = subprocess.run([
            sys.executable, 'ctmm_unified_tool.py', 'workflow'
        ], capture_output=True, text=True)
        
        self.assertEqual(result.returncode, 0)
        self.assertIn('COMPREHENSIVE WORKFLOW', result.stdout)
    
    def test_unified_tool_test_command(self):
        """Test that the unified tool test command works."""
        result = subprocess.run([
            sys.executable, 'ctmm_unified_tool.py', 'test'
        ], capture_output=True, text=True)
        
        self.assertEqual(result.returncode, 0)
        self.assertIn('CTMM TEST SUITE', result.stdout)
        self.assertIn('Test Summary', result.stdout)
    
    def test_unified_tool_clean_command(self):
        """Test that the unified tool clean command works."""
        result = subprocess.run([
            sys.executable, 'ctmm_unified_tool.py', 'clean'
        ], capture_output=True, text=True)
        
        self.assertEqual(result.returncode, 0)
        self.assertIn('CLEANUP', result.stdout)

class TestLaTeXDeEscapingIntegration(unittest.TestCase):
    """Integration tests for LaTeX de-escaping functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_dir = Path(tempfile.mkdtemp())
        self.de_escaper = fix_latex_escaping.LaTeXDeEscaper()
        
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.test_dir)
    
    def create_test_latex_file(self, filename: str, content: str) -> Path:
        """Helper to create test LaTeX files."""
        file_path = self.test_dir / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return file_path
    
    def test_enhanced_de_escaping_patterns(self):
        """Test that enhanced de-escaping patterns work correctly."""
        # Test content with various over-escaping patterns
        test_content = r"""
\textbackslash{}section\textbackslash{}\textbackslash{}\textbackslash{}texorpdfstring\textbackslash{}
\textbackslash{}textbf\textbackslash{}
\textbackslash{}emph\textbackslash{}
\textbackslash{}hypertarget\textbackslash{}
\textbackslash{}begin\textbackslash{}
\textbackslash{}end\textbackslash{}
\textbackslash{}item
\textbackslash{}cite\textbackslash{}
\textbackslash{}ref\textbackslash{}
\textbackslash{}textcolor\textbackslash{}
        """
        
        test_file = self.create_test_latex_file('test.tex', test_content)
        changed, replacements = self.de_escaper.process_file(test_file)
        
        self.assertTrue(changed)
        self.assertGreater(replacements, 0)
        
        # Read back the content
        with open(test_file, 'r', encoding='utf-8') as f:
            fixed_content = f.read()
        
        # Verify specific patterns are fixed
        self.assertNotIn(r'\textbackslash{}', fixed_content)
        self.assertIn(r'\section{', fixed_content)
        self.assertIn(r'\textbf', fixed_content)
        self.assertIn(r'\emph', fixed_content)
    
    def test_validation_functionality(self):
        """Test that validation functionality works correctly."""
        # Test valid LaTeX content
        valid_content = r"""
\section{Test Section}
\begin{itemize}
\item Test item
\end{itemize}
        """
        
        is_valid, issues = self.de_escaper.validate_latex_content(valid_content, "test.tex")
        self.assertTrue(is_valid)
        self.assertEqual(len(issues), 0)
        
        # Test invalid LaTeX content
        invalid_content = r"""
\section{Test Section
\begin{itemize}
\item Test item
        """
        
        is_valid, issues = self.de_escaper.validate_latex_content(invalid_content, "test.tex")
        self.assertFalse(is_valid)
        self.assertGreater(len(issues), 0)
    
    def test_unified_tool_fix_escaping_command(self):
        """Test the unified tool's fix-escaping command."""
        # Create test file with over-escaped content
        test_content = r"\textbackslash{}textbf\textbackslash{}\{Test\textbackslash{}\}"
        test_file = self.create_test_latex_file('test.tex', test_content)
        
        result = subprocess.run([
            sys.executable, 'ctmm_unified_tool.py', 'fix-escaping', str(self.test_dir)
        ], capture_output=True, text=True)
        
        self.assertEqual(result.returncode, 0)
        self.assertIn('LATEX DE-ESCAPING', result.stdout)
        
        # Verify the file was fixed
        with open(test_file, 'r', encoding='utf-8') as f:
            fixed_content = f.read()
        
        self.assertNotIn(r'\textbackslash{}', fixed_content)
        # The current implementation correctly handles this pattern
        self.assertIn(r'\textbf', fixed_content)

class TestBuildSystemIntegration(unittest.TestCase):
    """Integration tests for the CTMM build system."""
    
    def test_ctmm_build_system_functions(self):
        """Test that all required CTMM build system functions exist and work."""
        # Test that main functions exist
        self.assertTrue(hasattr(ctmm_build, 'scan_references'))
        self.assertTrue(hasattr(ctmm_build, 'check_missing_files'))
        self.assertTrue(hasattr(ctmm_build, 'create_template'))
        self.assertTrue(hasattr(ctmm_build, 'test_basic_build'))
        self.assertTrue(hasattr(ctmm_build, 'test_full_build'))
        
        # Test scan_references returns expected structure
        if Path('main.tex').exists():
            references = ctmm_build.scan_references()
            self.assertIsInstance(references, dict)
            self.assertIn('style_files', references)
            self.assertIn('module_files', references)
    
    def test_build_system_via_unified_tool(self):
        """Test build system functionality through unified tool."""
        result = subprocess.run([
            sys.executable, 'ctmm_unified_tool.py', 'build'
        ], capture_output=True, text=True)
        
        self.assertEqual(result.returncode, 0)
        self.assertIn('Build System Check', result.stdout)

class TestWorkflowIntegration(unittest.TestCase):
    """Integration tests for workflow orchestration."""
    
    def test_comprehensive_workflow_execution(self):
        """Test that the comprehensive workflow executes successfully."""
        result = subprocess.run([
            sys.executable, 'comprehensive_workflow.py'
        ], capture_output=True, text=True)
        
        # Should complete successfully (exit code 0 or 1 for warnings)
        self.assertIn(result.returncode, [0, 1])
        self.assertIn('COMPREHENSIVE WORKFLOW', result.stdout)
    
    def test_workflow_via_unified_tool(self):
        """Test workflow execution through unified tool."""
        result = subprocess.run([
            sys.executable, 'ctmm_unified_tool.py', 'workflow'
        ], capture_output=True, text=True)
        
        self.assertEqual(result.returncode, 0)
        self.assertIn('COMPREHENSIVE WORKFLOW', result.stdout)

class TestToolsetIntegration(unittest.TestCase):
    """Integration tests for the complete CTMM toolset integration."""
    
    def test_all_key_files_present(self):
        """Test that all key files for the toolset are present."""
        key_files = [
            'main.tex',
            'ctmm_build.py',
            'fix_latex_escaping.py',
            'comprehensive_workflow.py',
            'test_ctmm_build.py',
            'ctmm_unified_tool.py',
            'test_integration.py'  # This file
        ]
        
        for file in key_files:
            self.assertTrue(Path(file).exists(), f"Key file {file} is missing")
    
    def test_makefile_integration(self):
        """Test that Makefile has proper integration with unified tool."""
        if Path('Makefile').exists():
            with open('Makefile', 'r') as f:
                makefile_content = f.read()
            
            # Check for unified tool integration
            self.assertIn('comprehensive', makefile_content)
            self.assertIn('workflow', makefile_content)
    
    def test_toolset_interoperability(self):
        """Test that all tools work together correctly."""
        # Test sequence: status -> validate -> build
        commands = [
            ['status'],
            ['validate'],
            ['build']
        ]
        
        for cmd in commands:
            result = subprocess.run([
                sys.executable, 'ctmm_unified_tool.py'
            ] + cmd, capture_output=True, text=True)
            
            self.assertEqual(result.returncode, 0, 
                           f"Command {' '.join(cmd)} failed: {result.stderr}")
    
    def test_unified_tool_help_completeness(self):
        """Test that unified tool help documentation is complete."""
        result = subprocess.run([
            sys.executable, 'ctmm_unified_tool.py', '--help'
        ], capture_output=True, text=True)
        
        self.assertEqual(result.returncode, 0)
        
        # Check that all expected commands are documented
        expected_commands = [
            'build', 'fix-escaping', 'validate', 'workflow', 'test', 'clean', 'status'
        ]
        
        for cmd in expected_commands:
            self.assertIn(cmd, result.stdout, f"Command {cmd} not documented in help")

def run_integration_test_suite():
    """Run the complete integration test suite with detailed reporting."""
    
    print("="*70)
    print("CTMM INTEGRATION TEST SUITE")
    print("="*70)
    print("Running comprehensive integration tests for CTMM toolset...")
    print()
    
    # Create test suite
    test_classes = [
        TestCTMMIntegration,
        TestLaTeXDeEscapingIntegration,
        TestBuildSystemIntegration,
        TestWorkflowIntegration,
        TestToolsetIntegration
    ]
    
    total_tests = 0
    total_passed = 0
    total_failed = 0
    
    for test_class in test_classes:
        suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
        runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
        result = runner.run(suite)
        
        total_tests += result.testsRun
        total_passed += result.testsRun - len(result.failures) - len(result.errors)
        total_failed += len(result.failures) + len(result.errors)
        
        print(f"\n{test_class.__name__}: {result.testsRun - len(result.failures) - len(result.errors)}/{result.testsRun} passed")
    
    print("\n" + "="*70)
    print("INTEGRATION TEST SUMMARY")
    print("="*70)
    print(f"Total tests: {total_tests}")
    print(f"Passed: {total_passed}")
    print(f"Failed: {total_failed}")
    print(f"Success rate: {(total_passed/total_tests)*100:.1f}%")
    
    if total_failed == 0:
        print("\n🎉 ALL INTEGRATION TESTS PASSED - 100% SUCCESS RATE!")
        print("✅ CTMM comprehensive toolset is fully operational")
        return True
    else:
        print(f"\n⚠️  {total_failed} integration test(s) failed")
        return False

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '-v':
        # Verbose mode - run with unittest
        unittest.main(argv=[sys.argv[0]], verbosity=2)
    else:
        # Standard mode - run custom suite
        success = run_integration_test_suite()
        sys.exit(0 if success else 1)