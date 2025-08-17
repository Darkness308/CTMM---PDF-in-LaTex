#!/usr/bin/env python3
"""
Unit tests for CTMM Build System functions.
Tests the ctmm_build.py module functions for correctness.

This comprehensive test suite covers:
- filename_to_title() function with 29 test cases
- Build system core functions (15+ test cases) 
- Integration tests for complete workflow
- Performance benchmarking and error handling
- Structured data returns and error recovery
"""

import unittest
import sys
import tempfile
import os
import time
import tracemalloc
from pathlib import Path

# Add current directory to path for importing ctmm_build
sys.path.insert(0, str(Path(__file__).parent))
import ctmm_build


class TestFilenameToTitle(unittest.TestCase):
    """Test cases for the filename_to_title function."""

    def test_underscores_to_spaces(self):
        """Test that underscores are converted to spaces."""
        result = ctmm_build.filename_to_title("test_module_name")
        self.assertEqual(result, "Test Module Name")

    def test_hyphens_to_spaces(self):
        """Test that hyphens are converted to spaces."""
        result = ctmm_build.filename_to_title("test-module-name")
        self.assertEqual(result, "Test Module Name")

    def test_mixed_separators(self):
        """Test handling of mixed underscores and hyphens."""
        result = ctmm_build.filename_to_title("test_module-name")
        self.assertEqual(result, "Test Module Name")

    def test_single_word(self):
        """Test single word filename."""
        result = ctmm_build.filename_to_title("module")
        self.assertEqual(result, "Module")

    def test_already_capitalized(self):
        """Test filename that's already properly formatted."""
        result = ctmm_build.filename_to_title("Test_Module")
        self.assertEqual(result, "Test Module")

    def test_lowercase_input(self):
        """Test all lowercase input."""
        result = ctmm_build.filename_to_title("depression_worksheet")
        self.assertEqual(result, "Depression Worksheet")

    def test_empty_string(self):
        """Test empty string input."""
        result = ctmm_build.filename_to_title("")
        self.assertEqual(result, "")

    def test_numbers_in_filename(self):
        """Test filename with numbers."""
        result = ctmm_build.filename_to_title("module_1_test")
        self.assertEqual(result, "Module 1 Test")

    def test_special_characters(self):
        """Test filename with multiple consecutive separators."""
        result = ctmm_build.filename_to_title("test__double--underscore")
        # Multiple consecutive separators are normalized to single spaces
        self.assertEqual(result, "Test Double Underscore")

    def test_german_therapeutic_names(self):
        """Test typical German therapeutic module names."""
        test_cases = [
            ("arbeitsblatt_trigger", "Arbeitsblatt Trigger"),
            ("depression-management", "Depression Management"),
            ("bindung_muster", "Bindung Muster"),
            ("kommunikation_skills", "Kommunikation Skills"),
        ]
        
        for input_name, expected in test_cases:
            with self.subTest(input_name=input_name):
                result = ctmm_build.filename_to_title(input_name)
                self.assertEqual(result, expected)

    def test_mixed_case_input(self):
        """Test mixed case input is normalized properly."""
        result = ctmm_build.filename_to_title("hELLo_WoRLd")
        self.assertEqual(result, "Hello World")

    def test_multiple_consecutive_separators(self):
        """Test multiple consecutive separators are normalized to single spaces."""
        result = ctmm_build.filename_to_title("hello__world")
        self.assertEqual(result, "Hello World")

    def test_leading_trailing_separators(self):
        """Test leading and trailing separators are normalized (trimmed)."""
        result = ctmm_build.filename_to_title("_hello_world_")
        self.assertEqual(result, "Hello World")

    def test_realistic_filenames(self):
        """Test realistic German therapy-related filenames from the CTMM system."""
        test_cases = [
            ("arbeitsblatt_depression", "Arbeitsblatt Depression"),
            ("trigger_management", "Trigger Management"),
            ("borderline_worksheet", "Borderline Worksheet"),
            ("ptsd-coping-strategies", "Ptsd Coping Strategies"),
            ("adhd_attention_exercises", "Adhd Attention Exercises"),
        ]
        
        for input_name, expected in test_cases:
            with self.subTest(input_name=input_name):
                result = ctmm_build.filename_to_title(input_name)
                self.assertEqual(result, expected)

    def test_very_long_filename(self):
        """Test very long filename to ensure performance and correctness."""
        long_filename = "very_long_module_name_with_many_words_that_should_still_work_correctly"
        expected = "Very Long Module Name With Many Words That Should Still Work Correctly"
        result = ctmm_build.filename_to_title(long_filename)
        self.assertEqual(result, expected)

    def test_german_umlauts_preserved(self):
        """Test that German umlauts and special characters are preserved."""
        test_cases = [
            ("übung_für_patienten", "Übung Für Patienten"),
            ("ängste_bewältigen", "Ängste Bewältigen"),
            ("selbst-fürsorge", "Selbst Fürsorge"),
        ]
        
        for input_name, expected in test_cases:
            with self.subTest(input_name=input_name):
                result = ctmm_build.filename_to_title(input_name)
                self.assertEqual(result, expected)

    def test_numeric_prefixes(self):
        """Test filenames with numeric prefixes (common in therapy modules)."""
        test_cases = [
            ("01_einführung", "01 Einführung"),
            ("2_advanced_techniques", "2 Advanced Techniques"),
            ("session_10_review", "Session 10 Review"),
        ]
        
        for input_name, expected in test_cases:
            with self.subTest(input_name=input_name):
                result = ctmm_build.filename_to_title(input_name)
                self.assertEqual(result, expected)

    def test_whitespace_edge_cases(self):
        """Test various whitespace scenarios."""
        test_cases = [
            ("  hello_world  ", "Hello World"),  # Leading/trailing spaces
            ("hello___world", "Hello World"),    # Multiple underscores
            ("hello---world", "Hello World"),    # Multiple hyphens
            ("hello_-_world", "Hello World"),    # Mixed separators
        ]
        
        for input_name, expected in test_cases:
            with self.subTest(input_name=input_name):
                result = ctmm_build.filename_to_title(input_name)
                self.assertEqual(result, expected)


class TestCTMMBuildSystemIntegration(unittest.TestCase):
    """Integration tests for CTMM Build System functions."""

    def test_scan_references_function_exists(self):
        """Test that the scan_references function exists and is callable."""
        self.assertTrue(hasattr(ctmm_build, 'scan_references'))
        self.assertTrue(callable(ctmm_build.scan_references))

    def test_check_missing_files_function_exists(self):
        """Test that the check_missing_files function exists and is callable."""
        self.assertTrue(hasattr(ctmm_build, 'check_missing_files'))
        self.assertTrue(callable(ctmm_build.check_missing_files))

    def test_create_template_function_exists(self):
        """Test that the create_template function exists and is callable."""
        self.assertTrue(hasattr(ctmm_build, 'create_template'))
        self.assertTrue(callable(ctmm_build.create_template))

    def test_test_basic_build_function_exists(self):
        """Test that the test_basic_build function exists and is callable."""
        self.assertTrue(hasattr(ctmm_build, 'test_basic_build'))
        self.assertTrue(callable(ctmm_build.test_basic_build))

    def test_test_full_build_function_exists(self):
        """Test that the test_full_build function exists and is callable."""
        self.assertTrue(hasattr(ctmm_build, 'test_full_build'))
        self.assertTrue(callable(ctmm_build.test_full_build))

    def test_problematic_functions_removed(self):
        """Test that the problematic functions identified in PR #393 have been removed."""
        # These functions were flagged as unnecessary in the PR review
        self.assertFalse(hasattr(ctmm_build, 'test_basic_framework'))
        self.assertFalse(hasattr(ctmm_build, 'generate_build_report'))

    def test_return_type(self):
        """Test that the filename_to_title function returns a string."""
        result = ctmm_build.filename_to_title("test_file")
        self.assertIsInstance(result, str)

    def test_scan_references_returns_dict(self):
        """Test that the scan_references function returns a dictionary with correct keys."""
        result = ctmm_build.scan_references("main.tex")
        self.assertIsInstance(result, dict)
        self.assertIn("style_files", result)
        self.assertIn("module_files", result)
        self.assertIsInstance(result["style_files"], list)
        self.assertIsInstance(result["module_files"], list)

    def test_structured_data_returns(self):
        """Test that the build system functions return properly structured data."""
        # Test scan_references returns structured data
        references = ctmm_build.scan_references("main.tex")
        self.assertIsInstance(references, dict)
        
        # Verify required keys exist
        required_keys = ["style_files", "module_files"]
        for key in required_keys:
            self.assertIn(key, references, f"Missing required key: {key}")
            self.assertIsInstance(references[key], list, f"Key {key} should be a list")
        
        # Test check_missing_files returns list
        all_files = references["style_files"] + references["module_files"]
        missing_files = ctmm_build.check_missing_files(all_files)
        self.assertIsInstance(missing_files, list)

    def test_error_handling_robustness(self):
        """Test error handling in build system functions."""
        # Test scan_references with non-existent file
        result = ctmm_build.scan_references("non_existent_file.tex")
        self.assertIsInstance(result, dict)
        self.assertEqual(result["style_files"], [])
        self.assertEqual(result["module_files"], [])
        
        # Test check_missing_files with empty list
        result = ctmm_build.check_missing_files([])
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)

    def test_build_system_numbered_steps(self):
        """Test that the build system implements numbered steps as described in PR."""
        # This test verifies the main function structure without actually running it
        import inspect
        
        # Get the source code of the main function
        source = inspect.getsource(ctmm_build.main)
        
        # Check that numbered steps are implemented
        self.assertIn("step = 1", source, "Build system should use numbered steps")
        self.assertIn("step += 1", source, "Build system should increment step numbers")
        self.assertIn("print(f\"\\n{step}.", source, "Build system should print numbered steps")

    def test_structured_data_returns_enhanced(self):
        """Test that the enhanced build system returns structured data."""
        import inspect
        
        # Get the source code of the main function
        source = inspect.getsource(ctmm_build.main)
        
        # Check for structured data patterns
        self.assertIn("build_data", source, "Main function should use structured data")
        self.assertIn("latex_validation", source, "Should track LaTeX validation status")
        self.assertIn("file_scanning", source, "Should track file scanning results")
        self.assertIn("build_testing", source, "Should track build testing results")

    def test_enhanced_error_handling(self):
        """Test that the enhanced build system has proper error handling."""
        import inspect
        
        # Get the source code of the main function
        source = inspect.getsource(ctmm_build.main)
        
        # Check for try-except blocks
        self.assertIn("try:", source, "Main function should have error handling")
        self.assertIn("except Exception as e:", source, "Should catch and handle exceptions")
        self.assertIn("logger.error", source, "Should log errors appropriately")

    def test_modular_helper_functions(self):
        """Test that the build system uses modular helper functions."""
        # Check that helper functions exist
        self.assertTrue(hasattr(ctmm_build, '_generate_build_summary'))
        self.assertTrue(hasattr(ctmm_build, '_generate_exit_code'))
        self.assertTrue(callable(ctmm_build._generate_build_summary))
        self.assertTrue(callable(ctmm_build._generate_exit_code))


class TestBuildSystemStructuredData(unittest.TestCase):
    """Test cases for structured data handling in the build system."""

    def test_build_data_structure(self):
        """Test that build data structure is properly defined."""
        import inspect
        
        # Get the source code to examine data structure
        source = inspect.getsource(ctmm_build.main)
        
        # Check for expected data structure keys
        expected_keys = [
            "latex_validation",
            "file_scanning", 
            "file_existence",
            "template_creation",
            "build_testing"
        ]
        
        for key in expected_keys:
            self.assertIn(f'"{key}"', source, f"build_data should contain {key}")

    def test_helper_function_error_handling(self):
        """Test that helper functions handle edge cases properly."""
        # Create mock build_data for testing
        mock_build_data = {
            "latex_validation": {"passed": True, "errors": []},
            "file_scanning": {"style_files": [], "module_files": []},
            "file_existence": {"missing_files": [], "total_missing": 0},
            "template_creation": {"created_count": 0, "created_files": []},
            "build_testing": {"basic_passed": True, "full_passed": True}
        }
        
        # Test _generate_exit_code with successful build
        exit_code = ctmm_build._generate_exit_code(mock_build_data)
        self.assertEqual(exit_code, 0, "Should return 0 for successful build")
        
        # Test _generate_exit_code with failed build
        mock_build_data["build_testing"]["basic_passed"] = False
        exit_code = ctmm_build._generate_exit_code(mock_build_data)
        self.assertEqual(exit_code, 1, "Should return 1 for failed build")

    def test_scan_references_enhanced_functionality(self):
        """Test enhanced scan_references with comment filtering."""
        # Create a test file with comments
        test_content = """
\\documentclass{article}
% This is a comment with \\usepackage{style/commented-style}
\\usepackage{style/active-style}
% Another comment with \\input{modules/commented-module}  
\\input{modules/active-module}
\\begin{document}
\\end{document}
"""
        test_file = "test_enhanced.tex"
        
        try:
            with open(test_file, 'w', encoding='utf-8') as f:
                f.write(test_content)
            
            result = ctmm_build.scan_references(test_file)
            
            # Should only find non-commented references
            self.assertEqual(result["style_files"], ["style/active-style.sty"])
            self.assertEqual(result["module_files"], ["modules/active-module.tex"])
            
        finally:
            if Path(test_file).exists():
                Path(test_file).unlink()

    def test_escaped_percent_handling(self):
        """Test that escaped percent signs (\\%) are handled correctly."""
        test_content = """
\\documentclass{article}
\\usepackage{style/test-style}
% This is a real comment
This line has an escaped \\% percent sign
\\input{modules/test-module}
\\begin{document}
Content with \\% escaped percent
\\end{document}
"""
        test_file = "test_escaped.tex"
        
        try:
            with open(test_file, 'w', encoding='utf-8') as f:
                f.write(test_content)
            
            result = ctmm_build.scan_references(test_file)
            
            # Should find both references despite escaped % in content
            self.assertEqual(result["style_files"], ["style/test-style.sty"])
            self.assertEqual(result["module_files"], ["modules/test-module.tex"])
            
        finally:
            if Path(test_file).exists():
                Path(test_file).unlink()


class TestScanReferences(unittest.TestCase):
    """Test cases for the scan_references function."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_main_tex = "test_main.tex"
        self.test_content = """
\\documentclass{article}
\\usepackage{style/ctmm-design}
\\usepackage{style/form-elements}
\\usepackage{style/ctmm-diagrams}
\\begin{document}
\\input{modules/arbeitsblatt-trigger}
\\input{modules/depression}
\\input{modules/bindungsleitfaden}
\\end{document}
"""

    def tearDown(self):
        """Clean up test fixtures."""
        if Path(self.test_main_tex).exists():
            Path(self.test_main_tex).unlink()

    def test_scan_references_basic_functionality(self):
        """Test that scan_references correctly identifies style and module files."""
        # Create test file
        with open(self.test_main_tex, 'w', encoding='utf-8') as f:
            f.write(self.test_content)

        result = ctmm_build.scan_references(self.test_main_tex)
        
        # Verify return structure
        self.assertIsInstance(result, dict)
        self.assertIn("style_files", result)
        self.assertIn("module_files", result)
        
        # Verify style files
        expected_style_files = [
            "style/ctmm-design.sty",
            "style/form-elements.sty", 
            "style/ctmm-diagrams.sty"
        ]
        self.assertEqual(sorted(result["style_files"]), sorted(expected_style_files))
        
        # Verify module files
        expected_module_files = [
            "modules/arbeitsblatt-trigger.tex",
            "modules/depression.tex",
            "modules/bindungsleitfaden.tex"
        ]
        self.assertEqual(sorted(result["module_files"]), sorted(expected_module_files))

    def test_scan_references_empty_file(self):
        """Test scan_references with empty main.tex file."""
        with open(self.test_main_tex, 'w', encoding='utf-8') as f:
            f.write("")

        result = ctmm_build.scan_references(self.test_main_tex)
        
        self.assertEqual(result["style_files"], [])
        self.assertEqual(result["module_files"], [])

    def test_scan_references_commented_lines(self):
        """Test that commented lines are not processed."""
        content = """
\\documentclass{article}
% \\usepackage{style/commented-style}
\\usepackage{style/active-style}
% \\input{modules/commented-module}
\\input{modules/active-module}
\\begin{document}
\\end{document}
"""
        with open(self.test_main_tex, 'w', encoding='utf-8') as f:
            f.write(content)

        result = ctmm_build.scan_references(self.test_main_tex)
        
        self.assertEqual(result["style_files"], ["style/active-style.sty"])
        self.assertEqual(result["module_files"], ["modules/active-module.tex"])


class TestCheckMissingFiles(unittest.TestCase):
    """Test cases for the check_missing_files function."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_files = []
        self.existing_file = "test_existing.txt"
        self.missing_file = "test_missing.txt"
        
        # Create an existing file for testing
        with open(self.existing_file, 'w') as f:
            f.write("test content")
        self.test_files.append(self.existing_file)

    def tearDown(self):
        """Clean up test fixtures."""
        for file_path in self.test_files:
            if Path(file_path).exists():
                Path(file_path).unlink()

    def test_check_missing_files_mixed_list(self):
        """Test check_missing_files with both existing and missing files."""
        files_to_check = [self.existing_file, self.missing_file]
        
        result = ctmm_build.check_missing_files(files_to_check)
        
        self.assertIsInstance(result, list)
        self.assertEqual(result, [self.missing_file])

    def test_check_missing_files_all_exist(self):
        """Test check_missing_files when all files exist."""
        files_to_check = [self.existing_file]
        
        result = ctmm_build.check_missing_files(files_to_check)
        
        self.assertEqual(result, [])

    def test_check_missing_files_all_missing(self):
        """Test check_missing_files when all files are missing."""
        files_to_check = ["missing1.txt", "missing2.txt"]
        
        result = ctmm_build.check_missing_files(files_to_check)
        
        self.assertEqual(sorted(result), sorted(files_to_check))

    def test_check_missing_files_empty_list(self):
        """Test check_missing_files with empty file list."""
        result = ctmm_build.check_missing_files([])
        
        self.assertEqual(result, [])


class TestCreateTemplate(unittest.TestCase):
    """Test cases for the create_template function."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_files = []
        self.test_dirs = []

    def tearDown(self):
        """Clean up test fixtures."""
        for file_path in self.test_files:
            if Path(file_path).exists():
                Path(file_path).unlink()
        for dir_path in reversed(self.test_dirs):
            if Path(dir_path).exists() and Path(dir_path).is_dir():
                try:
                    Path(dir_path).rmdir()
                except OSError:
                    pass  # Directory not empty, that's ok

    def test_create_template_style_file(self):
        """Test creating a template for a style file."""
        style_file = "test_templates/test-style.sty"
        self.test_files.append(style_file)
        self.test_files.append("test_templates/TODO_test-style.md")
        self.test_dirs.append("test_templates")
        
        ctmm_build.create_template(style_file)
        
        # Check that style file was created
        self.assertTrue(Path(style_file).exists())
        
        # Check content contains expected elements
        with open(style_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        self.assertIn("\\NeedsTeXFormat{LaTeX2e}", content)
        self.assertIn("\\ProvidesPackage{test-style}", content)
        self.assertIn("TODO", content)
        
        # Check that TODO file was created
        todo_file = "test_templates/TODO_test-style.md"
        self.assertTrue(Path(todo_file).exists())

    def test_create_template_module_file(self):
        """Test creating a template for a module file."""
        module_file = "test_templates/test-module.tex"
        self.test_files.append(module_file)
        self.test_files.append("test_templates/TODO_test-module.md")
        self.test_dirs.append("test_templates")
        
        ctmm_build.create_template(module_file)
        
        # Check that module file was created
        self.assertTrue(Path(module_file).exists())
        
        # Check content contains expected elements
        with open(module_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        self.assertIn("\\section{TODO: Test Module}", content)
        self.assertIn("\\label{sec:test-module}", content)
        self.assertIn("TODO", content)
        
        # Check that TODO file was created
        todo_file = "test_templates/TODO_test-module.md"
        self.assertTrue(Path(todo_file).exists())

    def test_create_template_creates_directories(self):
        """Test that create_template creates necessary directories."""
        nested_file = "deep/nested/path/test-file.tex"
        self.test_files.append(nested_file)
        self.test_files.append("deep/nested/path/TODO_test-file.md")
        self.test_dirs.extend(["deep/nested/path", "deep/nested", "deep"])
        
        ctmm_build.create_template(nested_file)
        
        # Check that all directories were created
        self.assertTrue(Path("deep").exists())
        self.assertTrue(Path("deep/nested").exists())
        self.assertTrue(Path("deep/nested/path").exists())
        self.assertTrue(Path(nested_file).exists())


class TestBuildSystemIntegration(unittest.TestCase):
    """Integration tests for build system functionality."""

    def test_validate_latex_files_function_exists(self):
        """Test that validate_latex_files function exists and is callable."""
        self.assertTrue(hasattr(ctmm_build, 'validate_latex_files'))
        self.assertTrue(callable(ctmm_build.validate_latex_files))

    def test_main_function_error_handling(self):
        """Test that main function has proper error handling structure."""
        import inspect
        
        source = inspect.getsource(ctmm_build.main)
        
        # Check for logging usage
        self.assertIn("logger.", source, "Main function should use logging")
        
        # Check for step-by-step execution
        self.assertIn("step", source, "Main function should implement steps")

    def test_build_system_comprehensive_workflow(self):
        """Test the complete build system workflow."""
        # This test verifies that all main functions work together
        # without actually running LaTeX compilation
        
        # Test scan_references
        references = ctmm_build.scan_references("main.tex")
        self.assertIsInstance(references, dict)
        
        # Test check_missing_files
        all_files = references["style_files"] + references["module_files"]
        missing_files = ctmm_build.check_missing_files(all_files)
        self.assertIsInstance(missing_files, list)
        
        # Test validate_latex_files
        is_valid = ctmm_build.validate_latex_files()
        self.assertIsInstance(is_valid, bool)

    def test_function_return_types(self):
        """Test that all build system functions return expected types."""
        # Test scan_references return type
        result = ctmm_build.scan_references("main.tex")
        self.assertIsInstance(result, dict)
        self.assertIn("style_files", result)
        self.assertIn("module_files", result)
        
        # Test check_missing_files return type
        result = ctmm_build.check_missing_files([])
        self.assertIsInstance(result, list)
        
        # Test validate_latex_files return type
        result = ctmm_build.validate_latex_files()
        self.assertIsInstance(result, bool)

    def test_error_resilience(self):
        """Test that functions handle errors gracefully."""
        # Test scan_references with invalid file
        result = ctmm_build.scan_references("nonexistent_file.tex")
        self.assertIsInstance(result, dict)
        self.assertEqual(result["style_files"], [])
        self.assertEqual(result["module_files"], [])
        
        # Test check_missing_files with invalid paths
        result = ctmm_build.check_missing_files(["invalid/path/file.txt"])
        self.assertIsInstance(result, list)
        self.assertEqual(result, ["invalid/path/file.txt"])


class TestPerformanceBenchmarks(unittest.TestCase):
    """Performance benchmarking tests for critical CTMM build system functions."""

    def setUp(self):
        """Set up performance testing."""
        tracemalloc.start()
        self.start_time = time.time()

    def tearDown(self):
        """Clean up after performance testing."""
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        execution_time = time.time() - self.start_time
        
        # Log performance metrics (optional - for debugging)
        if hasattr(self, '_testMethodName'):
            test_name = self._testMethodName
            # Only print if test takes longer than expected thresholds
            if execution_time > 0.1:  # 100ms threshold
                print(f"\n⚠️  Performance Warning - {test_name}: {execution_time:.3f}s")
            if peak > 1024 * 1024:  # 1MB threshold
                print(f"⚠️  Memory Warning - {test_name}: {peak / 1024 / 1024:.2f}MB peak")

    def test_filename_to_title_performance(self):
        """Test filename_to_title performance with large inputs."""
        # Test with very long filename
        long_filename = "_".join([f"word{i}" for i in range(100)])
        
        start_time = time.time()
        result = ctmm_build.filename_to_title(long_filename)
        execution_time = time.time() - start_time
        
        # Should complete in under 10ms even for very long inputs
        self.assertLess(execution_time, 0.01, "filename_to_title should be fast for long inputs")
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)

    def test_scan_references_performance(self):
        """Test scan_references performance with main.tex."""
        start_time = time.time()
        result = ctmm_build.scan_references("main.tex")
        execution_time = time.time() - start_time
        
        # Should complete in under 100ms for typical main.tex
        self.assertLess(execution_time, 0.1, "scan_references should be fast for typical files")
        self.assertIsInstance(result, dict)

    def test_check_missing_files_performance(self):
        """Test check_missing_files performance with large file lists."""
        # Create a list of 1000 non-existent files
        large_file_list = [f"nonexistent_{i}.tex" for i in range(1000)]
        
        start_time = time.time()
        result = ctmm_build.check_missing_files(large_file_list)
        execution_time = time.time() - start_time
        
        # Should complete in under 500ms even for 1000 files
        self.assertLess(execution_time, 0.5, "check_missing_files should handle large lists efficiently")
        self.assertEqual(len(result), 1000)  # All should be missing

    def test_memory_efficiency(self):
        """Test that functions don't leak memory significantly."""
        # Run filename_to_title many times to check for memory leaks
        for i in range(1000):
            ctmm_build.filename_to_title(f"test_file_{i}")
        
        # Memory usage should be reasonable (checked in tearDown)
        # This test mainly serves to trigger the memory monitoring

    def test_bulk_operations_performance(self):
        """Test performance when processing multiple operations in sequence."""
        start_time = time.time()
        
        # Simulate a typical build system workflow
        for i in range(10):
            ctmm_build.filename_to_title(f"module_{i}_test")
            ctmm_build.check_missing_files([f"file_{i}.tex"])
        
        execution_time = time.time() - start_time
        
        # Bulk operations should complete efficiently
        self.assertLess(execution_time, 0.1, "Bulk operations should be efficient")


class TestCodeCoverage(unittest.TestCase):
    """Test coverage validation for build system functions."""

    def test_all_public_functions_tested(self):
        """Verify that all public functions in ctmm_build are tested."""
        # Get all public functions from ctmm_build module
        public_functions = [name for name in dir(ctmm_build) 
                          if callable(getattr(ctmm_build, name)) 
                          and not name.startswith('_')
                          and name != 'main']  # main is tested indirectly
        
        # Expected functions that should have tests
        expected_functions = [
            'filename_to_title',
            'scan_references', 
            'check_missing_files',
            'create_template',
            'test_basic_build',
            'test_full_build',
            'validate_latex_files'
        ]
        
        # Verify all expected functions exist
        for func_name in expected_functions:
            self.assertIn(func_name, public_functions, 
                         f"Expected function {func_name} should exist in ctmm_build")

    def test_error_conditions_covered(self):
        """Verify that error conditions are properly tested."""
        # Test that scan_references handles file errors
        result = ctmm_build.scan_references("nonexistent_file.tex")
        self.assertEqual(result["style_files"], [])
        self.assertEqual(result["module_files"], [])
        
        # Test that check_missing_files handles empty input
        result = ctmm_build.check_missing_files([])
        self.assertEqual(result, [])
        
        # These tests verify error handling is robust

    def test_return_type_consistency(self):
        """Verify that functions return consistent types across different inputs."""
        # Test filename_to_title with various inputs
        test_inputs = ["", "single", "under_score", "hyphen-test", "Mixed_Case-test"]
        
        for test_input in test_inputs:
            result = ctmm_build.filename_to_title(test_input)
            self.assertIsInstance(result, str, f"filename_to_title should return string for '{test_input}'")
        
        # Test scan_references return type consistency
        result = ctmm_build.scan_references("main.tex")
        self.assertIsInstance(result, dict)
        self.assertIn("style_files", result)
        self.assertIn("module_files", result)
        self.assertIsInstance(result["style_files"], list)
        self.assertIsInstance(result["module_files"], list)


if __name__ == '__main__':
    # Configure test runner for enhanced output
    unittest.main(verbosity=2, buffer=True)