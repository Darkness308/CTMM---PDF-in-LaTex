#!/usr/bin/env python3
"""
CTMM Document Conversion Pipeline Validator
============================================

Advanced error analysis and code optimization for converted therapy documents.
Provides actionable recommendations for quality improvement.

This script validates the document conversion pipeline that successfully converts
therapy documents from Word/Markdown to LaTeX format.
"""

import os
import sys
import re
from pathlib import Path
from typing import List, Dict, Tuple

class CTMMConversionValidator:
    """Validates CTMM therapy document conversions with advanced error analysis."""

    def __init__(self):
        self.converted_dir = "converted"
        self.expected_files = [
            "README.tex",
            "Tool 22 Safewords Signalsysteme CTMM.tex",
            "Tool 23 Trigger Management.tex",
            "Matching Matrix Wochenlogik.tex",
            "Matching Matrix Trigger Reaktion Intervention CTMM.tex"
        ]

        self.quality_metrics = {
            "file_count": 0,
            "total_lines": 0,
            "therapeutic_terms": 0,
            "interactive_elements": 0,
            "navigation_links": 0,
            "ctmm_patterns": 0,
            "table_structures": 0,
            "quality_score": 0.0
        }

        self.issues_found = []
        self.recommendations = []

    def validate_conversion_pipeline(self) -> Dict[str, any]:
        """Main validation function for the document conversion pipeline."""

        print("[SEARCH] CTMM Document Conversion Pipeline Validation")
        print("=" * 60)
        print("Analyzing converted therapy documents for quality and compliance...")
        print()

        # Check file existence
        self._validate_file_existence()

        # Analyze document quality
        self._analyze_document_quality()

        # Check therapeutic content compliance
        self._validate_therapeutic_content()

        # Verify LaTeX structure
        self._validate_latex_structure()

        # Generate quality score
        self._calculate_quality_score()

        # Generate report
        return self._generate_validation_report()

    def _validate_file_existence(self):
        """Validate that all expected converted files exist."""
        print("[FOLDER] Checking file existence...")

        if not os.path.exists(self.converted_dir):
            self.issues_found.append(f"[FAIL] Converted directory '{self.converted_dir}' not found")
            return

        existing_files = os.listdir(self.converted_dir)
        self.quality_metrics["file_count"] = len(existing_files)

        for expected_file in self.expected_files:
            if expected_file in existing_files:
                print(f"  [PASS] {expected_file}")
            else:
                self.issues_found.append(f"[FAIL] Missing converted file: {expected_file}")

        missing_count = len(self.expected_files) - len([f for f in self.expected_files if f in existing_files])
        if missing_count == 0:
            print(f"  [PASS] All {len(self.expected_files)} expected files found")
        else:
            print(f"  [WARN]  {missing_count} files missing")

    def _analyze_document_quality(self):
        """Analyze quality metrics for converted documents."""
        print("\n[SUMMARY] Analyzing document quality...")

        for filename in self.expected_files:
            filepath = os.path.join(self.converted_dir, filename)
            if os.path.exists(filepath):
                self._analyze_single_document(filepath, filename)

    def _analyze_single_document(self, filepath: str, filename: str):
        """Analyze a single converted document for quality metrics."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            lines = content.split('\n')
            self.quality_metrics["total_lines"] += len(lines)

            # Count therapeutic terminology
            therapeutic_terms = [
                "trigger", "ctmm", "therapie", "regulation", "bindung",
                "eskalation", "intervention", "safe-word", "grounding",
                "dissoziation", "neurodiver", "bewältigung"
            ]

            term_count = sum(content.lower().count(term) for term in therapeutic_terms)
            self.quality_metrics["therapeutic_terms"] += term_count

            # Count interactive elements
            interactive_patterns = [
                r"\\rule\{.*?\}\{.*?\}",  # Form fields
                r"\\begin\{tabular\}",  # Tables
                r"\\textbf\{.*?\}",  # Emphasis
                r"\\hypertarget\{.*?\}"  # Hyperlinks
            ]

            for pattern in interactive_patterns:
                matches = re.findall(pattern, content)
                if "rule" in pattern:
                    self.quality_metrics["interactive_elements"] += len(matches)
                elif "tabular" in pattern:
                    self.quality_metrics["table_structures"] += len(matches)
                elif "hypertarget" in pattern:
                    self.quality_metrics["navigation_links"] += len(matches)

            # Count CTMM-specific patterns
            ctmm_patterns = [
                r"Catch-Track-Map-Match", r"CTMM-System", r"CTMM-Modul",
                r"[EMOJI].*?Worum geht.*?hier", r"Kapitelzuordnung.*?CTMM"
            ]

            for pattern in ctmm_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                self.quality_metrics["ctmm_patterns"] += len(matches)

            print(f"  [FILE] {filename}: {len(lines)} lines, {term_count} therapeutic terms")

        except Exception as e:
            self.issues_found.append(f"[FAIL] Error analyzing {filename}: {str(e)}")

    def _validate_therapeutic_content(self):
        """Validate therapeutic content compliance."""
        print("\n[EMOJI] Validating therapeutic content...")

        required_elements = {
            "Tool 23 Trigger Management.tex": [
                "Trigger Erkennungszeichen", "Bewältigungsstrategien",
                "Persönliche Trigger-Analyse", "Notfall-Trigger Protokoll"
            ],
            "Tool 22 Safewords Signalsysteme CTMM.tex": [
                "Safe-Words", "Signalsysteme", "Eskalationsprävention"
            ],
            "Matching Matrix Wochenlogik.tex": [
                "Wochenlogik", "Energielevel Matrix", "Kommunikationsmuster"
            ],
            "Matching Matrix Trigger Reaktion Intervention CTMM.tex": [
                "Trigger-Reaktions Matrix", "Interventions-Toolbox", "Eskalations"
            ]
        }

        for filename, elements in required_elements.items():
            filepath = os.path.join(self.converted_dir, filename)
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                missing_elements = []
                for element in elements:
                    if element.lower() not in content.lower():
                        missing_elements.append(element)

                if missing_elements:
                    self.issues_found.append(f"[WARN] {filename}: Missing therapeutic elements: {missing_elements}")
                else:
                    print(f"  [PASS] {filename}: All therapeutic elements present")

    def _validate_latex_structure(self):
        """Validate LaTeX document structure and formatting."""
        print("\n[NOTE] Validating LaTeX structure...")

        structure_checks = [
            (r"\\section\{", "Section headers"),
            (r"\\subsection\{", "Subsection headers"),
            (r"\\begin\{quote\}", "Quote environments"),
            (r"\\begin\{itemize\}", "Itemize lists"),
            (r"\\begin\{tabular\}", "Table structures"),
            (r"\\hypertarget\{", "Hyperlink targets")
        ]

        for filename in self.expected_files:
            filepath = os.path.join(self.converted_dir, filename)
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                structure_score = 0
                for pattern, name in structure_checks:
                    if re.search(pattern, content):
                        structure_score += 1

                if structure_score >= 4:  # At least 4 structural elements
                    print(f"  [PASS] {filename}: Good LaTeX structure ({structure_score}/6)")
                else:
                    self.issues_found.append(f"[WARN] {filename}: Limited LaTeX structure ({structure_score}/6)")

    def _calculate_quality_score(self):
        """Calculate overall quality score for the conversion pipeline."""
        base_score = 70.0  # Base score for file existence

        # Bonus points for quality metrics
        if self.quality_metrics["file_count"] >= 5:
            base_score += 10

        if self.quality_metrics["therapeutic_terms"] >= 50:
            base_score += 10

        if self.quality_metrics["interactive_elements"] >= 20:
            base_score += 5

        if self.quality_metrics["table_structures"] >= 5:
            base_score += 5

        # Deduct points for issues
        base_score -= len(self.issues_found) * 5

        self.quality_metrics["quality_score"] = max(0.0, min(100.0, base_score))

    def _generate_validation_report(self) -> Dict[str, any]:
        """Generate comprehensive validation report."""
        print("\n" + "=" * 60)
        print("[TEST] CONVERSION PIPELINE VALIDATION REPORT")
        print("=" * 60)

        # Summary metrics
        print(f"\n[SUMMARY] Quality Metrics:")
        print(f"  Files converted: {self.quality_metrics['file_count']}/5")
        print(f"  Total lines: {self.quality_metrics['total_lines']}")
        print(f"  Therapeutic terms: {self.quality_metrics['therapeutic_terms']}")
        print(f"  Interactive elements: {self.quality_metrics['interactive_elements']}")
        print(f"  Table structures: {self.quality_metrics['table_structures']}")
        print(f"  Navigation links: {self.quality_metrics['navigation_links']}")
        print(f"  CTMM patterns: {self.quality_metrics['ctmm_patterns']}")

        # Quality score
        score = self.quality_metrics["quality_score"]
        print(f"\n[TARGET] Overall Quality Score: {score:.1f}/100")

        if score >= 90:
            print("  [EMOJI] Excellent conversion quality!")
        elif score >= 80:
            print("  [PASS] Good conversion quality")
        elif score >= 70:
            print("  [WARN] Acceptable conversion quality")
        else:
            print("  [FAIL] Conversion quality needs improvement")

        # Issues and recommendations
        if self.issues_found:
            print(f"\n[WARN] Issues Found ({len(self.issues_found)}):")
            for issue in self.issues_found:
                print(f"  {issue}")

        # Generate recommendations
        self._generate_recommendations()

        if self.recommendations:
            print(f"\n[TIP] Recommendations ({len(self.recommendations)}):")
            for rec in self.recommendations:
                print(f"  {rec}")

        return {
            "quality_score": score,
            "metrics": self.quality_metrics,
            "issues": self.issues_found,
            "recommendations": self.recommendations
        }

    def _generate_recommendations(self):
        """Generate actionable recommendations for improvement."""
        if self.quality_metrics["interactive_elements"] < 15:
            self.recommendations.append("[FIX] Add more interactive form elements (\\rule{}{} fields)")

        if self.quality_metrics["table_structures"] < 3:
            self.recommendations.append("[SUMMARY] Include more structured tables for data collection")

        if self.quality_metrics["ctmm_patterns"] < 10:
            self.recommendations.append("[EMOJI] Enhance CTMM methodology references and patterns")

        if len(self.issues_found) > 0:
            self.recommendations.append("[EMOJI] Address structural and content issues identified")

        if self.quality_metrics["therapeutic_terms"] < 40:
            self.recommendations.append("[EMOJI] Increase therapeutic terminology density for professional use")

def main():
    """Main function to run the conversion pipeline validation."""

    # Change to repository directory
    os.chdir("/home/runner/work/CTMM---PDF-in-LaTex/CTMM---PDF-in-LaTex")

    validator = CTMMConversionValidator()
    report = validator.validate_conversion_pipeline()

    print(f"\n[LAUNCH] Validation complete!")
    print(f"Quality Score: {report['quality_score']:.1f}/100")

    # Exit with appropriate code
    if report['quality_score'] >= 80:
        print("[PASS] CONVERSION PIPELINE VALIDATION: PASS")
        sys.exit(0)
    else:
        print("[WARN] CONVERSION PIPELINE VALIDATION: IMPROVEMENTS NEEDED")
        sys.exit(1)

if __name__ == "__main__":
    main()
