#!/usr/bin/env python3
"""
CTMM Build System Test Coverage Analysis
Provides detailed coverage reporting for unit tests.
"""

import unittest
import sys
import time
import tracemalloc
from pathlib import Path

# Add current directory to path for importing test modules
sys.path.insert(0, str(Path(__file__).parent))

def run_with_coverage():
    """Run tests with coverage analysis if coverage.py is available."""
    try:
        import coverage
        cov = coverage.Coverage()
        cov.start()
        
        # Import and run tests
        import test_ctmm_build
        suite = unittest.TestLoader().loadTestsFromModule(test_ctmm_build)
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        cov.stop()
        cov.save()
        
        print("\n" + "="*60)
        print("COVERAGE REPORT")
        print("="*60)
        cov.report(show_missing=True)
        
        # Generate HTML report if possible
        try:
            cov.html_report(directory='htmlcov')
            print(f"\nHTML coverage report generated in 'htmlcov/' directory")
        except Exception as e:
            print(f"Note: HTML report could not be generated: {e}")
            
        return result
        
    except ImportError:
        print("Coverage.py not available, running tests without coverage analysis")
        return run_without_coverage()

def run_without_coverage():
    """Run tests without coverage analysis."""
    # Import and run tests
    import test_ctmm_build
    suite = unittest.TestLoader().loadTestsFromModule(test_ctmm_build)
    runner = unittest.TextTestRunner(verbosity=2)
    return runner.run(suite)

def analyze_test_performance():
    """Analyze test performance and memory usage."""
    print("\n" + "="*60)
    print("PERFORMANCE ANALYSIS")
    print("="*60)
    
    # Start memory tracking
    tracemalloc.start()
    start_time = time.time()
    
    # Run performance tests specifically
    import test_ctmm_build
    loader = unittest.TestLoader()
    
    # Load only performance tests
    performance_suite = unittest.TestSuite()
    
    # Get all test classes
    test_classes = [
        test_ctmm_build.TestPerformanceBenchmarks,
        test_ctmm_build.TestCodeCoverage
    ]
    
    for test_class in test_classes:
        try:
            tests = loader.loadTestsFromTestCase(test_class)
            performance_suite.addTests(tests)
        except AttributeError:
            print(f"Warning: {test_class.__name__} not found")
    
    # Run performance tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(performance_suite)
    
    # Get memory usage
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    total_time = time.time() - start_time
    
    print(f"\nPerformance Summary:")
    print(f"Total test time: {total_time:.3f}s")
    print(f"Peak memory usage: {peak / 1024 / 1024:.2f}MB")
    print(f"Current memory usage: {current / 1024 / 1024:.2f}MB")
    
    if result.wasSuccessful():
        print("✓ All performance tests passed")
    else:
        print(f"✗ {len(result.failures)} failures, {len(result.errors)} errors")
    
    return result

def generate_test_report():
    """Generate comprehensive test report."""
    print("CTMM Build System - Comprehensive Test Report")
    print("=" * 60)
    print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Run main test suite
    print("Running main test suite...")
    main_result = run_with_coverage()
    
    # Run performance analysis
    print("\nRunning performance analysis...")
    perf_result = analyze_test_performance()
    
    # Summary
    print("\n" + "="*60)
    print("OVERALL SUMMARY")
    print("="*60)
    
    total_tests = main_result.testsRun
    total_failures = len(main_result.failures) + len(main_result.errors)
    
    print(f"Total tests run: {total_tests}")
    print(f"Failures/Errors: {total_failures}")
    print(f"Success rate: {((total_tests - total_failures) / total_tests * 100):.1f}%")
    
    if main_result.wasSuccessful() and perf_result.wasSuccessful():
        print("✓ All tests passed successfully")
        return 0
    else:
        print("✗ Some tests failed")
        return 1

if __name__ == '__main__':
    sys.exit(generate_test_report())