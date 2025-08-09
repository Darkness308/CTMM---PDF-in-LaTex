#!/usr/bin/env python3
"""
CTMM Advanced Error Analysis and Code Optimization System
Provides actionable recommendations for LaTeX code quality improvement.

This script:
1. Analyzes LaTeX code for potential issues and optimization opportunities
2. Provides detailed error reports with suggested fixes
3. Checks CTMM coding standards compliance
4. Offers code quality metrics and recommendations
5. Generates comprehensive optimization reports
"""

import os
import re
import subprocess
import sys
from pathlib import Path
from typing import List, Dict, Tuple, Set
import logging
import json
from dataclasses import dataclass
from enum import Enum

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('error_analysis.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class IssueLevel(Enum):
    CRITICAL = "critical"
    WARNING = "warning"
    INFO = "info"
    OPTIMIZATION = "optimization"

@dataclass
class CodeIssue:
    level: IssueLevel
    category: str
    description: str
    line_number: int
    suggestion: str
    code_snippet: str
    
class CTMMCodeAnalyzer:
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.issues: List[CodeIssue] = []
        self.metrics = {
            "total_files": 0,
            "total_lines": 0,
            "error_count": 0,
            "warning_count": 0,
            "optimization_opportunities": 0
        }
        
    def analyze_project(self) -> Dict:
        """Run comprehensive analysis on the entire CTMM project."""
        logger.info("Starting comprehensive CTMM project analysis...")
        
        # Find all LaTeX files
        tex_files = list(self.project_root.glob("**/*.tex"))
        sty_files = list(self.project_root.glob("**/*.sty"))
        
        all_files = tex_files + sty_files
        self.metrics["total_files"] = len(all_files)
        
        logger.info(f"Found {len(tex_files)} .tex files and {len(sty_files)} .sty files")
        
        # Analyze each file
        for file_path in all_files:
            self._analyze_file(file_path)
        
        # Generate comprehensive report
        report = self._generate_analysis_report()
        
        # Save detailed report
        self._save_analysis_results()
        
        return report
    
    def _analyze_file(self, file_path: Path):
        """Analyze a single LaTeX file for issues."""
        logger.debug(f"Analyzing {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
                lines = content.split('\n')
                
            self.metrics["total_lines"] += len(lines)
            
            # Run various analysis checks
            self._check_syntax_issues(file_path, lines)
            self._check_ctmm_standards(file_path, lines)
            self._check_performance_issues(file_path, lines)
            self._check_accessibility_issues(file_path, lines)
            self._check_best_practices(file_path, lines)
            
        except Exception as e:
            self._add_issue(
                IssueLevel.CRITICAL,
                "File Access",
                f"Could not read file: {e}",
                0,
                f"Check file permissions and encoding for {file_path}",
                ""
            )
    
    def _check_syntax_issues(self, file_path: Path, lines: List[str]):
        """Check for LaTeX syntax issues."""
        for i, line in enumerate(lines, 1):
            # Check for undefined control sequences
            if re.search(r'\\[a-zA-Z]+', line) and not self._is_known_command(line):
                potential_issues = re.findall(r'\\([a-zA-Z]+)', line)
                for command in potential_issues:
                    if command in ['Box', 'blacksquare', 'square']:
                        self._add_issue(
                            IssueLevel.CRITICAL,
                            "Undefined Command",
                            f"Use of undefined command \\{command}",
                            i,
                            f"Replace \\{command} with \\checkbox for CTMM compatibility",
                            line.strip()
                        )
            
            # Check for unmatched braces
            open_braces = line.count('{')
            close_braces = line.count('}')
            if open_braces != close_braces and not line.strip().startswith('%'):
                self._add_issue(
                    IssueLevel.WARNING,
                    "Syntax",
                    "Potentially unmatched braces",
                    i,
                    "Check that all { have matching } on the same logical line",
                    line.strip()
                )
            
            # Check for package loading in wrong place
            if '\\usepackage' in line and '\\begin{document}' in '\n'.join(lines[:i]):
                self._add_issue(
                    IssueLevel.CRITICAL,
                    "Package Loading",
                    "Package loaded after \\begin{document}",
                    i,
                    "Move \\usepackage commands to document preamble",
                    line.strip()
                )
    
    def _check_ctmm_standards(self, file_path: Path, lines: List[str]):
        """Check compliance with CTMM coding standards."""
        content = '\n'.join(lines)
        
        # Check for CTMM color usage
        if 'textcolor' in content:
            for i, line in enumerate(lines, 1):
                if '\\textcolor{' in line and not any(color in line for color in ['ctmmBlue', 'ctmmOrange', 'ctmmGreen', 'ctmmPurple']):
                    self._add_issue(
                        IssueLevel.OPTIMIZATION,
                        "CTMM Standards",
                        "Non-CTMM color used",
                        i,
                        "Consider using CTMM colors: ctmmBlue, ctmmOrange, ctmmGreen, ctmmPurple",
                        line.strip()
                    )
        
        # Check for proper checkbox usage
        for i, line in enumerate(lines, 1):
            if any(cmd in line for cmd in ['\\Box', '\\square', '\\blacksquare']):
                self._add_issue(
                    IssueLevel.WARNING,
                    "CTMM Standards",
                    "Non-standard checkbox command",
                    i,
                    "Use \\checkbox or \\checkedbox for CTMM compatibility",
                    line.strip()
                )
        
        # Check for German language support
        if file_path.suffix == '.tex' and 'ngerman' not in content and any(german_char in content for german_char in ['ä', 'ö', 'ü', 'ß']):
            self._add_issue(
                IssueLevel.WARNING,
                "Language Support",
                "German characters found but no ngerman package",
                1,
                "Ensure babel with ngerman option is loaded for proper German support",
                "Contains German characters"
            )
    
    def _check_performance_issues(self, file_path: Path, lines: List[str]):
        """Check for performance-related issues."""
        content = '\n'.join(lines)
        
        # Check for excessive package loading
        package_count = len(re.findall(r'\\usepackage', content))
        if package_count > 20:
            self._add_issue(
                IssueLevel.OPTIMIZATION,
                "Performance",
                f"High number of packages loaded ({package_count})",
                1,
                "Review if all packages are necessary for optimal compilation speed",
                f"{package_count} packages loaded"
            )
        
        # Check for large images without optimization
        for i, line in enumerate(lines, 1):
            if '\\includegraphics' in line and 'width=' not in line and 'height=' not in line:
                self._add_issue(
                    IssueLevel.OPTIMIZATION,
                    "Performance",
                    "Image included without size specification",
                    i,
                    "Specify width or height for better layout and performance",
                    line.strip()
                )
    
    def _check_accessibility_issues(self, file_path: Path, lines: List[str]):
        """Check for accessibility-related issues."""
        for i, line in enumerate(lines, 1):
            # Check for alt text in graphics
            if '\\includegraphics' in line and 'alt=' not in line:
                self._add_issue(
                    IssueLevel.INFO,
                    "Accessibility",
                    "Image without alt text",
                    i,
                    "Consider adding alt text for screen readers",
                    line.strip()
                )
            
            # Check for meaningful link text
            if '\\href{' in line:
                link_match = re.search(r'\\href\{[^}]+\}\{([^}]+)\}', line)
                if link_match and link_match.group(1).lower() in ['here', 'click here', 'link']:
                    self._add_issue(
                        IssueLevel.INFO,
                        "Accessibility",
                        "Non-descriptive link text",
                        i,
                        "Use descriptive link text instead of 'here' or 'click here'",
                        line.strip()
                    )
    
    def _check_best_practices(self, file_path: Path, lines: List[str]):
        """Check for LaTeX best practices."""
        for i, line in enumerate(lines, 1):
            # Check for hardcoded spacing
            if re.search(r'\\vspace\{[0-9]+cm\}', line):
                self._add_issue(
                    IssueLevel.OPTIMIZATION,
                    "Best Practices",
                    "Hardcoded vertical spacing",
                    i,
                    "Consider using semantic spacing commands or flexible spaces",
                    line.strip()
                )
            
            # Check for inline math in text mode
            if '$' in line and line.count('$') % 2 == 0:
                math_content = re.findall(r'\$([^$]+)\$', line)
                for math in math_content:
                    if len(math.split()) > 3:  # Long math expressions
                        self._add_issue(
                            IssueLevel.INFO,
                            "Best Practices",
                            "Long inline math expression",
                            i,
                            "Consider using display math for complex expressions",
                            line.strip()
                        )
            
            # Check for TODO comments
            if 'TODO' in line.upper():
                self._add_issue(
                    IssueLevel.INFO,
                    "Development",
                    "TODO comment found",
                    i,
                    "Review and complete TODO item",
                    line.strip()
                )
    
    def _is_known_command(self, line: str) -> bool:
        """Check if LaTeX commands in line are known/standard."""
        # This is a simplified check - in practice, you'd have a comprehensive list
        known_commands = {
            'section', 'subsection', 'subsubsection', 'textbf', 'textit', 'textcolor',
            'begin', 'end', 'item', 'checkbox', 'checkedbox', 'ctmmBlueBox',
            'usepackage', 'documentclass', 'input', 'include', 'label', 'ref',
            'href', 'url', 'includegraphics', 'caption', 'vspace', 'hspace',
            'newpage', 'clearpage', 'tableofcontents', 'maketitle'
        }
        
        commands_in_line = re.findall(r'\\([a-zA-Z]+)', line)
        return all(cmd in known_commands or len(cmd) <= 2 for cmd in commands_in_line)
    
    def _add_issue(self, level: IssueLevel, category: str, description: str, 
                   line_number: int, suggestion: str, code_snippet: str):
        """Add an issue to the analysis results."""
        issue = CodeIssue(level, category, description, line_number, suggestion, code_snippet)
        self.issues.append(issue)
        
        # Update metrics
        if level == IssueLevel.CRITICAL:
            self.metrics["error_count"] += 1
        elif level == IssueLevel.WARNING:
            self.metrics["warning_count"] += 1
        elif level == IssueLevel.OPTIMIZATION:
            self.metrics["optimization_opportunities"] += 1
    
    def _generate_analysis_report(self) -> Dict:
        """Generate comprehensive analysis report."""
        # Group issues by category and level
        issues_by_level = {}
        issues_by_category = {}
        
        for issue in self.issues:
            # By level
            if issue.level not in issues_by_level:
                issues_by_level[issue.level] = []
            issues_by_level[issue.level].append(issue)
            
            # By category
            if issue.category not in issues_by_category:
                issues_by_category[issue.category] = []
            issues_by_category[issue.category].append(issue)
        
        # Calculate quality score
        total_issues = len(self.issues)
        critical_issues = len(issues_by_level.get(IssueLevel.CRITICAL, []))
        warning_issues = len(issues_by_level.get(IssueLevel.WARNING, []))
        
        # Quality score: 100 - (critical * 10 + warnings * 5) / total_lines * 1000
        if self.metrics["total_lines"] > 0:
            quality_score = max(0, 100 - (critical_issues * 10 + warning_issues * 5) * 1000 / self.metrics["total_lines"])
        else:
            quality_score = 100
        
        report = {
            "summary": {
                "total_files": self.metrics["total_files"],
                "total_lines": self.metrics["total_lines"],
                "total_issues": total_issues,
                "critical_issues": critical_issues,
                "warning_issues": warning_issues,
                "optimization_opportunities": self.metrics["optimization_opportunities"],
                "quality_score": round(quality_score, 1)
            },
            "issues_by_level": {level.value: len(issues) for level, issues in issues_by_level.items()},
            "issues_by_category": {category: len(issues) for category, issues in issues_by_category.items()},
            "recommendations": self._generate_recommendations(issues_by_category)
        }
        
        return report
    
    def _generate_recommendations(self, issues_by_category: Dict) -> List[str]:
        """Generate actionable recommendations based on analysis."""
        recommendations = []
        
        if "CTMM Standards" in issues_by_category:
            recommendations.append(
                "Review CTMM coding standards: Use \\checkbox instead of \\Box, "
                "prefer CTMM colors (ctmmBlue, ctmmOrange, ctmmGreen, ctmmPurple)"
            )
        
        if "Undefined Command" in issues_by_category:
            recommendations.append(
                "Check package dependencies: Ensure all required packages are loaded in preamble"
            )
        
        if "Performance" in issues_by_category:
            recommendations.append(
                "Optimize for performance: Review package usage and image sizing"
            )
        
        if "Accessibility" in issues_by_category:
            recommendations.append(
                "Improve accessibility: Add alt text to images and use descriptive link text"
            )
        
        if "Development" in issues_by_category:
            recommendations.append(
                "Complete development tasks: Review and address TODO comments"
            )
        
        return recommendations
    
    def _save_analysis_results(self):
        """Save detailed analysis results to files."""
        # Save JSON report
        json_report = {
            "metrics": self.metrics,
            "issues": [
                {
                    "level": issue.level.value,
                    "category": issue.category,
                    "description": issue.description,
                    "line_number": issue.line_number,
                    "suggestion": issue.suggestion,
                    "code_snippet": issue.code_snippet
                }
                for issue in self.issues
            ]
        }
        
        with open('ctmm_analysis.json', 'w', encoding='utf-8') as f:
            json.dump(json_report, f, indent=2, ensure_ascii=False)
        
        # Save detailed markdown report
        self._save_markdown_report()
        
        logger.info("Analysis results saved to ctmm_analysis.json and ctmm_analysis_report.md")
    
    def _save_markdown_report(self):
        """Save a detailed markdown analysis report."""
        with open('ctmm_analysis_report.md', 'w', encoding='utf-8') as f:
            f.write("# CTMM Advanced Error Analysis Report\n\n")
            
            # Summary
            f.write("## Executive Summary\n")
            f.write(f"- **Files Analyzed:** {self.metrics['total_files']}\n")
            f.write(f"- **Total Lines:** {self.metrics['total_lines']}\n")
            f.write(f"- **Issues Found:** {len(self.issues)}\n")
            f.write(f"- **Critical Issues:** {self.metrics['error_count']}\n")
            f.write(f"- **Warnings:** {self.metrics['warning_count']}\n")
            f.write(f"- **Optimization Opportunities:** {self.metrics['optimization_opportunities']}\n\n")
            
            # Issues by category
            f.write("## Issues by Category\n")
            categories = {}
            for issue in self.issues:
                if issue.category not in categories:
                    categories[issue.category] = []
                categories[issue.category].append(issue)
            
            for category, issues in categories.items():
                f.write(f"\n### {category} ({len(issues)} issues)\n")
                for issue in issues[:10]:  # Limit to top 10 per category
                    f.write(f"- **{issue.level.value.upper()}:** {issue.description}\n")
                    f.write(f"  - *Suggestion:* {issue.suggestion}\n")
                    if issue.code_snippet:
                        f.write(f"  - *Code:* `{issue.code_snippet}`\n")
                if len(issues) > 10:
                    f.write(f"  - ... and {len(issues) - 10} more\n")
            
            # Recommendations
            f.write("\n## Actionable Recommendations\n")
            recommendations = self._generate_recommendations(categories)
            for i, rec in enumerate(recommendations, 1):
                f.write(f"{i}. {rec}\n")
            
            f.write("\n## Next Steps\n")
            f.write("1. Address critical issues first (compilation blockers)\n")
            f.write("2. Review CTMM standards compliance\n")
            f.write("3. Implement optimization suggestions\n")
            f.write("4. Test compilation after fixes\n")
            f.write("5. Re-run analysis to verify improvements\n")

def main():
    """Run the CTMM advanced error analysis system."""
    analyzer = CTMMCodeAnalyzer()
    
    logger.info("CTMM Advanced Error Analysis starting...")
    
    # Run comprehensive analysis
    report = analyzer.analyze_project()
    
    # Display summary
    print("\n" + "="*60)
    print("CTMM ADVANCED ERROR ANALYSIS SUMMARY")
    print("="*60)
    print(f"Files analyzed: {report['summary']['total_files']}")
    print(f"Total lines: {report['summary']['total_lines']}")
    print(f"Quality score: {report['summary']['quality_score']}/100")
    print(f"Issues found: {report['summary']['total_issues']}")
    print(f"  - Critical: {report['summary']['critical_issues']}")
    print(f"  - Warnings: {report['summary']['warning_issues']}")
    print(f"  - Optimizations: {report['summary']['optimization_opportunities']}")
    
    if report['summary']['critical_issues'] > 0:
        print("\n🚨 CRITICAL ISSUES DETECTED - Address immediately!")
        return 1
    elif report['summary']['warning_issues'] > 0:
        print("\n⚠️  Warnings found - Review recommended")
        return 0
    else:
        print("\n✅ No critical issues found - Code quality looks good!")
        return 0

if __name__ == "__main__":
    sys.exit(main())