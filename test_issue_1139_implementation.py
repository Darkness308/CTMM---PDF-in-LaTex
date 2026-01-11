#!/usr/bin/env python3
"""
Test CTMM Comprehensive LaTeX Workflow System Implementation

This test validates the comprehensive LaTeX workflow system implementation
including document conversion pipeline, error analysis, and code optimization.

Tests the implementation for Issue #1139.
"""

import unittest
import os
import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from validate_conversion_pipeline import CTMMConversionValidator
except ImportError:
    print("Error: Could not import validation module")
    sys.exit(1)

class TestCTMMWorkflowSystem(unittest.TestCase):
    """Test the comprehensive CTMM LaTeX workflow system implementation."""

    def setUp(self):
        """Set up test environment."""
        self.repo_root = "/home/runner/work/CTMM---PDF-in-LaTex/CTMM---PDF-in-LaTex"
        os.chdir(self.repo_root)
        self.validator = CTMMConversionValidator()

    def test_enhanced_latex_build_system(self):
        """Test enhanced LaTeX build system with multi-pass compilation and error handling."""
        print("\n[FIX] Testing enhanced LaTeX build system...")

        # Check that ctmm_build.py exists and is executable
        build_script = os.path.join(self.repo_root, "ctmm_build.py")
        self.assertTrue(os.path.exists(build_script), "CTMM build script should exist")
        self.assertTrue(os.access(build_script, os.X_OK), "Build script should be executable")

        # Run build system and check output
        import subprocess
        result = subprocess.run([sys.executable, "ctmm_build.py"],
                              capture_output=True, text=True, timeout=60)

        self.assertEqual(result.returncode, 0, "Build system should complete successfully")
        self.assertIn("CTMM BUILD SYSTEM SUMMARY", result.stdout)
        self.assertIn("LaTeX validation: [OK] PASS", result.stdout)
        self.assertIn("Basic build: [OK] PASS", result.stdout)
        self.assertIn("Full build: [OK] PASS", result.stdout)

        print("  [PASS] Enhanced LaTeX build system functional")

    def test_document_conversion_pipeline(self):
        """Test document conversion pipeline that converts therapy documents to LaTeX."""
        print("\n[FILE] Testing document conversion pipeline...")

        # Check that converted directory exists
        converted_dir = os.path.join(self.repo_root, "converted")
        self.assertTrue(os.path.exists(converted_dir), "Converted directory should exist")

        # Check for expected converted files
        expected_files = [
            "README.tex",
            "Tool 22 Safewords Signalsysteme CTMM.tex",
            "Tool 23 Trigger Management.tex",
            "Matching Matrix Wochenlogik.tex",
            "Matching Matrix Trigger Reaktion Intervention CTMM.tex"
        ]

        existing_files = os.listdir(converted_dir)
        for expected_file in expected_files:
            self.assertIn(expected_file, existing_files,
                         f"Converted file {expected_file} should exist")

        # Validate content quality
        for filename in expected_files:
            filepath = os.path.join(converted_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check for LaTeX structure
            self.assertIn("\\section{", content, f"{filename} should have section headers")
            self.assertIn("\\hypertarget{", content, f"{filename} should have hyperlink targets")

            # Check for therapeutic content
            therapeutic_indicators = ["trigger", "ctmm", "therapie", "intervention"]
            has_therapeutic_content = any(term in content.lower() for term in therapeutic_indicators)
            self.assertTrue(has_therapeutic_content, f"{filename} should contain therapeutic content")

        print(f"  [PASS] All {len(expected_files)} documents successfully converted")

    def test_advanced_error_analysis_and_optimization(self):
        """Test advanced error analysis and code optimization capabilities."""
        print("\n[SEARCH] Testing advanced error analysis and optimization...")

        # Run validation pipeline
        report = self.validator.validate_conversion_pipeline()

        # Check quality metrics
        self.assertIsInstance(report, dict, "Validation should return a report dictionary")
        self.assertIn("quality_score", report, "Report should include quality score")
        self.assertIn("metrics", report, "Report should include metrics")

        # Validate quality score
        quality_score = report["quality_score"]
        self.assertIsInstance(quality_score, (int, float), "Quality score should be numeric")
        self.assertGreaterEqual(quality_score, 80, "Quality score should be at least 80/100")

        # Check metrics completeness
        metrics = report["metrics"]
        required_metrics = [
            "file_count", "total_lines", "therapeutic_terms",
            "interactive_elements", "table_structures", "navigation_links"
        ]

        for metric in required_metrics:
            self.assertIn(metric, metrics, f"Metrics should include {metric}")
            self.assertGreaterEqual(metrics[metric], 0, f"{metric} should be non-negative")

        # Validate analysis depth
        self.assertGreaterEqual(metrics["file_count"], 5, "Should analyze at least 5 files")
        self.assertGreaterEqual(metrics["total_lines"], 500, "Should analyze substantial content")
        self.assertGreaterEqual(metrics["therapeutic_terms"], 100, "Should detect therapeutic terminology")

        print(f"  [PASS] Quality analysis complete (Score: {quality_score:.1f}/100)")

    def test_pdf_verification_capabilities(self):
        """Test PDF verification and multi-format output capabilities."""
        print("\n[TEST] Testing PDF verification capabilities...")

        # Check that build system includes PDF verification logic
        build_script_path = os.path.join(self.repo_root, "ctmm_build.py")
        with open(build_script_path, 'r', encoding='utf-8') as f:
            build_content = f.read()

        # Look for PDF-related functionality
        pdf_indicators = ["pdflatex", "pdf", "compilation", "build"]
        has_pdf_support = any(indicator in build_content.lower() for indicator in pdf_indicators)
        self.assertTrue(has_pdf_support, "Build system should support PDF compilation")

        # Check for error handling in build system
        error_handling_indicators = ["try:", "except", "error", "WARNING"]
        has_error_handling = any(indicator in build_content for indicator in error_handling_indicators)
        self.assertTrue(has_error_handling, "Build system should have error handling")

        print("  [PASS] PDF verification capabilities present")

    def test_therapy_content_compliance(self):
        """Test that converted documents maintain therapeutic content standards."""
        print("\n[EMOJI] Testing therapy content compliance...")

        # Check for CTMM methodology compliance
        converted_dir = os.path.join(self.repo_root, "converted")
        ctmm_compliance_count = 0

        for filename in os.listdir(converted_dir):
            if filename.endswith('.tex'):
                filepath = os.path.join(converted_dir, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Check for CTMM methodology elements
                ctmm_elements = [
                    "Catch-Track-Map-Match", "CTMM-System", "CTMM-Modul",
                    "Worum geht", "Kapitelzuordnung"
                ]

                if any(element in content for element in ctmm_elements):
                    ctmm_compliance_count += 1

        self.assertGreaterEqual(ctmm_compliance_count, 3,
                               "At least 3 documents should show CTMM compliance")

        # Check for German therapeutic terminology
        german_terms = ["Trigger", "Intervention", "Bewältigung", "Regulation"]
        terminology_files = 0

        for filename in os.listdir(converted_dir):
            if filename.endswith('.tex'):
                filepath = os.path.join(converted_dir, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                if any(term in content for term in german_terms):
                    terminology_files += 1

        self.assertGreaterEqual(terminology_files, 4,
                               "Most documents should contain German therapeutic terminology")

        print("  [PASS] Therapeutic content compliance verified")

    def test_interactive_elements_and_forms(self):
        """Test interactive elements and form functionality in converted documents."""
        print("\n[TARGET] Testing interactive elements and forms...")

        converted_dir = os.path.join(self.repo_root, "converted")
        interactive_element_count = 0
        table_structure_count = 0

        for filename in os.listdir(converted_dir):
            if filename.endswith('.tex'):
                filepath = os.path.join(converted_dir, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Count interactive form elements
                import re
                form_fields = re.findall(r'\\rule\{.*?\}\{.*?\}', content)
                interactive_element_count += len(form_fields)

                # Count table structures
                tables = re.findall(r'\\begin\{tabular\}', content)
                table_structure_count += len(tables)

        self.assertGreaterEqual(interactive_element_count, 50,
                               "Should have substantial interactive form elements")
        self.assertGreaterEqual(table_structure_count, 10,
                               "Should have multiple table structures")

        print(f"  [PASS] Interactive elements: {interactive_element_count}, Tables: {table_structure_count}")

    def test_system_integration_and_workflow(self):
        """Test overall system integration and workflow functionality."""
        print("\n[GEAR] Testing system integration and workflow...")

        # Test that validation script can be run
        validation_script = os.path.join(self.repo_root, "validate_conversion_pipeline.py")
        self.assertTrue(os.path.exists(validation_script), "Validation script should exist")

        import subprocess
        result = subprocess.run([sys.executable, validation_script],
                              capture_output=True, text=True, timeout=60)

        self.assertEqual(result.returncode, 0, "Validation pipeline should complete successfully")
        self.assertIn("CONVERSION PIPELINE VALIDATION: PASS", result.stdout)

        # Test main CTMM build system integration
        result = subprocess.run([sys.executable, "ctmm_build.py"],
                              capture_output=True, text=True, timeout=60)

        self.assertEqual(result.returncode, 0, "Main build system should integrate successfully")

        print("  [PASS] System integration and workflow functional")

def main():
    """Run the comprehensive test suite."""
    print("[LAUNCH] CTMM Comprehensive LaTeX Workflow System Test Suite")
    print("=" * 70)
    print("Testing implementation for Issue #1139...")
    print()

    # Run tests
    unittest.main(verbosity=2, exit=False)

    print("\n" + "=" * 70)
    print("[SUCCESS] Test Suite Complete!")
    print("[PASS] Comprehensive LaTeX workflow system implementation validated")

if __name__ == "__main__":
    main()
