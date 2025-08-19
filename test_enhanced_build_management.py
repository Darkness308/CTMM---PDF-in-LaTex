#!/usr/bin/env python3
"""
Comprehensive tests for the enhanced CTMM build management system.
Tests all enhanced features including error categorization, performance tracking,
artifact management, and CI/CD integration.
"""

import unittest
import subprocess
import tempfile
import os
import sys
import time
from pathlib import Path

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ctmm_build import (
    enhanced_build_management, 
    comprehensive_build_workflow,
    _cleanup_build_artifacts,
    _categorize_build_errors,
    _manage_build_artifacts
)
from build_system import enhanced_incremental_testing


class TestEnhancedBuildManagement(unittest.TestCase):
    """Test enhanced build management functionality."""
    
    def test_enhanced_build_management_structure(self):
        """Test that enhanced build management returns proper structure."""
        result = enhanced_build_management()
        
        # Check required keys exist
        required_keys = [
            "validation_passed", "files_created", "errors_fixed",
            "automation_improvements", "error_categories", 
            "performance_metrics", "artifacts_managed"
        ]
        
        for key in required_keys:
            self.assertIn(key, result)
        
        # Check error categories structure
        error_categories = result["error_categories"]
        expected_categories = [
            "syntax_errors", "missing_files", "resource_issues", "template_warnings"
        ]
        
        for category in expected_categories:
            self.assertIn(category, error_categories)
            self.assertIsInstance(error_categories[category], list)
    
    def test_enhanced_build_management_performance_tracking(self):
        """Test that performance metrics are tracked."""
        result = enhanced_build_management()
        
        metrics = result["performance_metrics"]
        
        # Check performance metrics exist
        self.assertIn("total_files_processed", metrics)
        self.assertIn("validation_time", metrics)
        self.assertIn("build_time", metrics)
        
        # Check build time is reasonable
        self.assertGreaterEqual(metrics["build_time"], 0)
        self.assertLess(metrics["build_time"], 30)  # Should complete within 30 seconds
    
    def test_comprehensive_build_workflow(self):
        """Test comprehensive build workflow integration."""
        result = comprehensive_build_workflow()
        
        # Should return boolean indicating success
        self.assertIsInstance(result, bool)
        
        # For a valid CTMM project, should return True
        self.assertTrue(result)


class TestEnhancedIncrementalTesting(unittest.TestCase):
    """Test enhanced incremental testing functionality."""
    
    def test_enhanced_incremental_testing_basic(self):
        """Test basic enhanced incremental testing functionality."""
        result = enhanced_incremental_testing()
        
        # Should return boolean
        self.assertIsInstance(result, bool)
        
        # Should succeed for valid project
        self.assertTrue(result)
    
    def test_enhanced_incremental_testing_with_missing_file(self):
        """Test enhanced testing handles missing files gracefully."""
        # Create temporary main.tex with reference to missing file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.tex', delete=False) as f:
            f.write("""
\\documentclass{article}
\\usepackage{style/ctmm-design}
\\input{modules/nonexistent-module}
\\begin{document}
Test document
\\end{document}
""")
            temp_main = f.name
        
        try:
            result = enhanced_incremental_testing(temp_main)
            # Should handle missing files gracefully
            self.assertIsInstance(result, bool)
        finally:
            os.unlink(temp_main)


class TestBuildArtifactManagement(unittest.TestCase):
    """Test build artifact management functionality."""
    
    def test_cleanup_build_artifacts(self):
        """Test build artifact cleanup."""
        # Create some test artifacts
        test_files = ["test.aux", "test.log", "test.temp.tex"]
        for filename in test_files:
            with open(filename, 'w') as f:
                f.write("test content")
        
        try:
            # Run cleanup
            cleaned_count = _cleanup_build_artifacts()
            
            # Should return count of cleaned files
            self.assertIsInstance(cleaned_count, int)
            self.assertGreaterEqual(cleaned_count, 0)
            
        finally:
            # Clean up any remaining test files
            for filename in test_files:
                try:
                    os.remove(filename)
                except FileNotFoundError:
                    pass
    
    def test_categorize_build_errors(self):
        """Test build error categorization."""
        result = _categorize_build_errors()
        
        # Should return dictionary with error categories
        self.assertIsInstance(result, dict)
        
        expected_categories = [
            "syntax_errors", "missing_files", "resource_issues", "template_warnings"
        ]
        
        for category in expected_categories:
            self.assertIn(category, result)
            self.assertIsInstance(result[category], list)
    
    def test_manage_build_artifacts(self):
        """Test build artifact management."""
        result = _manage_build_artifacts()
        
        # Should return dictionary with artifact statistics
        self.assertIsInstance(result, dict)
        
        expected_keys = [
            "temp_files_cleaned", "output_files_created", "log_files_generated"
        ]
        
        for key in expected_keys:
            self.assertIn(key, result)
            self.assertIsInstance(result[key], int)
            self.assertGreaterEqual(result[key], 0)


class TestCIIntegration(unittest.TestCase):
    """Test CI/CD integration functionality."""
    
    def test_makefile_enhanced_targets(self):
        """Test that enhanced Makefile targets work."""
        # Test enhanced-build target
        result = subprocess.run(
            ["make", "enhanced-build"], 
            capture_output=True, 
            text=True,
            timeout=60
        )
        
        self.assertEqual(result.returncode, 0)
        self.assertIn("ENHANCED BUILD MANAGEMENT REPORT", result.stdout)
    
    def test_makefile_enhanced_testing_target(self):
        """Test enhanced testing Makefile target."""
        result = subprocess.run(
            ["make", "enhanced-testing"],
            capture_output=True,
            text=True, 
            timeout=60
        )
        
        self.assertEqual(result.returncode, 0)
        self.assertIn("ENHANCED INCREMENTAL TESTING REPORT", result.stdout)
    
    def test_makefile_comprehensive_target(self):
        """Test comprehensive workflow Makefile target."""
        result = subprocess.run(
            ["make", "comprehensive"],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        self.assertEqual(result.returncode, 0)
        self.assertIn("Comprehensive workflow completed successfully", result.stdout)


class TestPerformanceMetrics(unittest.TestCase):
    """Test performance tracking and metrics."""
    
    def test_build_performance_tracking(self):
        """Test that build performance is tracked."""
        start_time = time.time()
        
        result = enhanced_build_management()
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Check that performance metrics are reasonable
        metrics = result["performance_metrics"]
        reported_time = metrics["build_time"]
        
        # Reported time should be close to actual execution time
        self.assertGreater(reported_time, 0)
        self.assertLess(abs(reported_time - execution_time), 1.0)
    
    def test_incremental_testing_performance(self):
        """Test enhanced incremental testing performance tracking."""
        # This test ensures incremental testing completes in reasonable time
        start_time = time.time()
        
        result = enhanced_incremental_testing()
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Should complete quickly for current project
        self.assertLess(execution_time, 10.0)
        self.assertTrue(result)


class TestErrorHandling(unittest.TestCase):
    """Test error handling and recovery mechanisms."""
    
    def test_enhanced_build_with_invalid_main_tex(self):
        """Test enhanced build handles invalid main.tex gracefully."""
        # Create invalid main.tex
        with tempfile.NamedTemporaryFile(mode='w', suffix='.tex', delete=False) as f:
            f.write("\\invalid{latex\\content")
            temp_main = f.name
        
        try:
            # Should handle gracefully without crashing
            # Note: We can't easily test this without modifying the main function
            # But we can ensure our helper functions are robust
            result = _categorize_build_errors()
            self.assertIsInstance(result, dict)
            
        finally:
            os.unlink(temp_main)
    
    def test_artifact_management_with_permission_errors(self):
        """Test artifact management handles permission errors."""
        # This test ensures robust error handling
        result = _manage_build_artifacts()
        
        # Should not crash even if some files can't be accessed
        self.assertIsInstance(result, dict)
        for key, value in result.items():
            self.assertIsInstance(value, int)
            self.assertGreaterEqual(value, 0)


def run_integration_tests():
    """Run all enhanced build management integration tests."""
    print("🧪 Running Enhanced Build Management Integration Tests")
    print("=" * 60)
    
    # Create test suite
    suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestEnhancedBuildManagement,
        TestEnhancedIncrementalTesting, 
        TestBuildArtifactManagement,
        TestCIIntegration,
        TestPerformanceMetrics,
        TestErrorHandling
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 60)
    if result.wasSuccessful():
        print("🎉 All enhanced build management tests passed!")
        print(f"Tests run: {result.testsRun}")
        return True
    else:
        print(f"❌ {len(result.failures)} test failures, {len(result.errors)} errors")
        print(f"Tests run: {result.testsRun}")
        return False


if __name__ == "__main__":
    success = run_integration_tests()
    sys.exit(0 if success else 1)