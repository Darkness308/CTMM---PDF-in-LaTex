#!/usr/bin/env python3
"""
Error Analyzer - Log Analysis and Error Categorization
Analyzes workflow logs to identify and categorize errors for automated fixing.
"""

import re
import logging
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass
from datetime import datetime

from healing_config import config

@dataclass
class ErrorInstance:
    """Represents a single error found in logs."""
    category: str
    pattern: str
    matched_text: str
    line_number: int
    context: str
    severity: str
    job_name: str

@dataclass
class ErrorAnalysis:
    """Complete analysis of errors found in workflow logs."""
    workflow_run_id: int
    workflow_name: str
    total_errors: int
    error_categories: Set[str]
    errors: List[ErrorInstance]
    is_solvable: bool
    recommended_fixes: List[str]
    analysis_timestamp: str

class ErrorAnalyzer:
    """Analyzes workflow logs to identify and categorize errors."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

        # Extended error patterns with more context
        self.detailed_patterns = {
            'latex_action_version': {
                'patterns': [
                    r'uses:\s*dante-ev/latex-action@(v[\d\.]+)',
                    r'Invalid version.*dante-ev/latex-action@([\w\.]+)',
                    r'The version.*?(v[\d\.]+).*?does not exist',
                    r'Action.*dante-ev/latex-action.*version.*?([\w\.]+).*not found'
                ],
                'severity': 'high',
                'description': 'LaTeX action version issues'
            },
            'package_missing': {
                'patterns': [
                    r'Package\s+([^\s]+)\s+not found',
                    r'File\s+([^\.]+\.sty)\s+not found',
                    r'LaTeX Error:\s+File\s+([^\s]+)\s+not found',
                    r'Unable to locate package\s+([^\s]+)',
                    r'texlive-([^\s]+).*not available'
                ],
                'severity': 'medium',
                'description': 'Missing LaTeX packages or files'
            },
            'syntax_error': {
                'patterns': [
                    r'LaTeX Error:\s+(.+)',
                    r'Undefined control sequence\s+(.+)',
                    r'Missing\s+([{}$])+',
                    r'Runaway argument.*?(.+)',
                    r'! (.+?) Error',
                    r'! (.+?) undefined'
                ],
                'severity': 'high',
                'description': 'LaTeX syntax and compilation errors'
            },
            'timeout': {
                'patterns': [
                    r'The operation was canceled',
                    r'timeout.*?(\d+)\s*(minutes?|seconds?)',
                    r'exceeded.*?time limit.*?(\d+)',
                    r'step.*?timed out.*?(\d+)',
                    r'Job was canceled.*timeout'
                ],
                'severity': 'medium',
                'description': 'Workflow or step timeouts'
            },
            'resource_limit': {
                'patterns': [
                    r'No space left on device',
                    r'out of memory',
                    r'resource temporarily unavailable',
                    r'Disk quota exceeded',
                    r'Cannot allocate memory'
                ],
                'severity': 'high',
                'description': 'System resource limitations'
            },
            'dependency_error': {
                'patterns': [
                    r'pip.*?failed.*?package\s+([^\s]+)',
                    r'Unable to install\s+([^\s]+)',
                    r'Could not find a version.*?([^\s]+)',
                    r'No matching distribution found.*?([^\s]+)',
                    r'ERROR: Could not install packages.*?([^\s]+)'
                ],
                'severity': 'medium',
                'description': 'Python package dependency issues'
            },
            'github_api_error': {
                'patterns': [
                    r'API rate limit exceeded',
                    r'Authentication failed',
                    r'Repository not found',
                    r'Permission denied.*GitHub',
                    r'Bad credentials'
                ],
                'severity': 'high',
                'description': 'GitHub API authentication or access issues'
            },
            'font_error': {
                'patterns': [
                    r'fontawesome.*not found',
                    r'Font.*?([^\s]+).*?not found',
                    r'Missing font.*?([^\s]+)',
                    r'Package fontawesome5.*Error'
                ],
                'severity': 'medium',
                'description': 'Font package or FontAwesome issues'
            },
            'workflow_syntax': {
                'patterns': [
                    r'Invalid workflow file',
                    r'YAML.*?error.*?line\s+(\d+)',
                    r'workflow.*?syntax.*?error',
                    r'Invalid.*?workflow.*?configuration'
                ],
                'severity': 'high',
                'description': 'GitHub Actions workflow syntax errors'
            }
        }

    def analyze_logs(self, workflow_run_id: int, workflow_name: str, job_logs: Dict[str, str]) -> ErrorAnalysis:
        """Analyze logs from all jobs in a workflow run."""
        all_errors = []
        error_categories = set()

        for job_name, log_content in job_logs.items():
            job_errors = self._analyze_job_log(job_name, log_content)
            all_errors.extend(job_errors)
            error_categories.update(error.category for error in job_errors)

        # Determine if errors are solvable
        is_solvable = self._assess_solvability(all_errors, job_logs)

        # Generate recommended fixes
        recommended_fixes = self._generate_fix_recommendations(error_categories, all_errors)

        analysis = ErrorAnalysis(
            workflow_run_id=workflow_run_id,
            workflow_name=workflow_name,
            total_errors=len(all_errors),
            error_categories=error_categories,
            errors=all_errors,
            is_solvable=is_solvable,
            recommended_fixes=recommended_fixes,
            analysis_timestamp=datetime.utcnow().isoformat()
        )

        self.logger.info(f"Analyzed {len(all_errors)} errors in {len(job_logs)} jobs")
        self.logger.info(f"Error categories: {', '.join(error_categories)}")

        return analysis

    def _analyze_job_log(self, job_name: str, log_content: str) -> List[ErrorInstance]:
        """Analyze a single job's log content for errors."""
        errors = []
        lines = log_content.split('\n')

        for line_num, line in enumerate(lines, 1):
            for category, pattern_info in self.detailed_patterns.items():
                for pattern in pattern_info['patterns']:
                    match = re.search(pattern, line, re.IGNORECASE)
                    if match:
                        # Get context around the error
                        context_start = max(0, line_num - 3)
                        context_end = min(len(lines), line_num + 2)
                        context = '\n'.join(lines[context_start:context_end])

                        error = ErrorInstance(
                            category=category,
                            pattern=pattern,
                            matched_text=match.group(0),
                            line_number=line_num,
                            context=context,
                            severity=pattern_info['severity'],
                            job_name=job_name
                        )
                        errors.append(error)
                        break  # Only match first pattern per line

        return errors

    def _assess_solvability(self, errors: List[ErrorInstance], job_logs: Dict[str, str]) -> bool:
        """Assess whether the found errors can be automatically solved."""
        # Check for unsolvable error patterns
        all_log_text = ' '.join(job_logs.values())
        if config.is_unsolvable_error(all_log_text):
            return False

        # Check for error categories that have known fix strategies
        solvable_categories = set(config.fix_strategies.keys())
        found_categories = {error.category for error in errors}

        # If all error categories have fix strategies, it's potentially solvable
        unsolvable_categories = found_categories - solvable_categories

        if unsolvable_categories:
            self.logger.warning(f"Found unsolvable error categories: {unsolvable_categories}")
            return False

        # Additional heuristics
        high_severity_errors = [e for e in errors if e.severity == 'high']
        if len(high_severity_errors) > 5:
            self.logger.warning("Too many high-severity errors - may not be solvable")
            return False

        return True

    def _generate_fix_recommendations(self, error_categories: Set[str], errors: List[ErrorInstance]) -> List[str]:
        """Generate specific fix recommendations based on found errors."""
        recommendations = []

        for category in error_categories:
            category_errors = [e for e in errors if e.category == category]

            if category == 'latex_action_version':
                versions_found = set()
                for error in category_errors:
                    match = re.search(r'v?(\d+\.\d+\.\d+)', error.matched_text)
                    if match:
                        versions_found.add(match.group(1))

                if versions_found:
                    recommendations.append(
                        f"Update LaTeX action versions from {', '.join(versions_found)} "
                        f"to {config.fix_strategies['latex_action_version']['fallback_version']}"
                    )
                else:
                    recommendations.append("Fix LaTeX action version specification")

            elif category == 'package_missing':
                missing_packages = set()
                for error in category_errors:
                    match = re.search(r'Package\s+([^\s]+)', error.matched_text)
                    if match:
                        missing_packages.add(match.group(1))

                if missing_packages:
                    recommendations.append(f"Install missing LaTeX packages: {', '.join(missing_packages)}")
                else:
                    recommendations.append("Install missing LaTeX packages")

            elif category == 'syntax_error':
                recommendations.append("Fix LaTeX syntax errors (requires manual review)")

            elif category == 'timeout':
                timeout_values = []
                for error in category_errors:
                    match = re.search(r'(\d+)\s*(minutes?|seconds?)', error.matched_text)
                    if match:
                        timeout_values.append(f"{match.group(1)} {match.group(2)}")

                if timeout_values:
                    recommendations.append(f"Increase timeout values (current: {', '.join(timeout_values)})")
                else:
                    recommendations.append("Increase workflow step timeouts")

            elif category == 'dependency_error':
                recommendations.append("Update Python package dependencies and versions")

            elif category == 'font_error':
                recommendations.append("Install FontAwesome packages and fix font dependencies")

            elif category == 'workflow_syntax':
                recommendations.append("Fix GitHub Actions workflow YAML syntax")

            else:
                recommendations.append(f"Address {category} errors (strategy available)")

        return recommendations

    def get_error_summary(self, analysis: ErrorAnalysis) -> str:
        """Generate a human-readable summary of the error analysis."""
        summary = []
        summary.append(f"Workflow: {analysis.workflow_name} (Run ID: {analysis.workflow_run_id})")
        summary.append(f"Total Errors: {analysis.total_errors}")
        summary.append(f"Error Categories: {', '.join(analysis.error_categories)}")
        summary.append(f"Solvable: {'Yes' if analysis.is_solvable else 'No'}")

        if analysis.recommended_fixes:
            summary.append("\nRecommended Fixes:")
            for i, fix in enumerate(analysis.recommended_fixes, 1):
                summary.append(f"  {i}. {fix}")

        if analysis.errors:
            summary.append(f"\nTop {min(5, len(analysis.errors))} Errors:")
            for i, error in enumerate(analysis.errors[:5], 1):
                summary.append(f"  {i}. [{error.category}] {error.matched_text}")

        return '\n'.join(summary)

    def extract_specific_values(self, analysis: ErrorAnalysis, category: str) -> List[str]:
        """Extract specific values for a given error category."""
        values = []
        category_errors = [e for e in analysis.errors if e.category == category]

        if category == 'latex_action_version':
            for error in category_errors:
                match = re.search(r'dante-ev/latex-action@(v?[\d\.]+)', error.matched_text)
                if match:
                    values.append(match.group(1))

        elif category == 'package_missing':
            for error in category_errors:
                match = re.search(r'Package\s+([^\s]+)', error.matched_text)
                if match:
                    values.append(match.group(1))
                match = re.search(r'File\s+([^\.]+\.sty)', error.matched_text)
                if match:
                    values.append(match.group(1).replace('.sty', ''))

        elif category == 'timeout':
            for error in category_errors:
                match = re.search(r'(\d+)\s*(minutes?|seconds?)', error.matched_text)
                if match:
                    values.append(f"{match.group(1)}{match.group(2)[0]}")  # "30m" or "300s"

        return list(set(values))  # Remove duplicates

def main():
    """Test the error analyzer functionality."""
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    analyzer = ErrorAnalyzer()

    print("🔍 Testing Error Analyzer")
    print("=" * 50)

    # Test with sample log content
    sample_logs = {
        "Build LaTeX PDF": """
        Starting LaTeX compilation...
        uses: dante-ev/latex-action@v1.0.0
        Package fontawesome5 not found
        LaTeX Error: File ctmm-design.sty not found
        The operation was canceled after 15 minutes
        """,
        "Setup Environment": """
        Installing dependencies...
        pip install failed for package PyYAML
        Could not find a version that satisfies the requirement chardet==5.0.0
        """,
        "Validation": """
        Running validation...
        Undefined control sequence \\ctmmCheckBox
        Missing } in argument
        """
    }

    # Analyze the sample logs
    analysis = analyzer.analyze_logs(12345, "latex-build.yml", sample_logs)

    # Print results
    print(f"✅ Analysis completed:")
    print(f"   - Total errors: {analysis.total_errors}")
    print(f"   - Categories: {', '.join(analysis.error_categories)}")
    print(f"   - Solvable: {analysis.is_solvable}")

    print("\n📋 Error Summary:")
    print(analyzer.get_error_summary(analysis))

    print("\n🔧 Testing specific value extraction:")
    for category in analysis.error_categories:
        values = analyzer.extract_specific_values(analysis, category)
        if values:
            print(f"   - {category}: {', '.join(values)}")

    print("\n✅ Error analyzer test completed")

if __name__ == "__main__":
    main()
