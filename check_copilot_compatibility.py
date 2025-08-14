#!/usr/bin/env python3
"""
GitHub Copilot Compatibility Checker for CTMM Project

This script validates repository structure and files for optimal GitHub Copilot review experience.
It checks for common issues that prevent Copilot from reviewing pull requests effectively.
"""

import os
import sys
import re
import subprocess
from pathlib import Path
from typing import List, Dict, Tuple, Set
import chardet
import argparse


class CopilotCompatibilityChecker:
    """Validates repository structure for GitHub Copilot compatibility."""
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path).resolve()
        self.issues: List[Dict] = []
        self.stats = {
            'total_files': 0,
            'problematic_files': 0,
            'large_files': 0,
            'encoding_issues': 0,
            'naming_issues': 0
        }
        
    def check_filename_conventions(self) -> List[Dict]:
        """Check for problematic filename conventions."""
        print("🔍 Checking filename conventions...")
        filename_issues = []
        
        # Patterns that cause issues for Copilot
        problematic_patterns = [
            (r'\s', 'contains spaces'),
            (r'[<>:"|?*]', 'contains special characters'),
            (r'^[#@$%]', 'starts with special character'),
            (r'\.{2,}', 'contains multiple consecutive dots'),
        ]
        
        for file_path in self.repo_path.rglob('*'):
            if file_path.is_file() and not self._is_git_ignored(file_path):
                filename = file_path.name
                relative_path = file_path.relative_to(self.repo_path)
                
                for pattern, description in problematic_patterns:
                    if re.search(pattern, filename):
                        issue = {
                            'type': 'filename',
                            'severity': 'warning',
                            'file': str(relative_path),
                            'issue': f'Filename {description}',
                            'suggestion': self._suggest_filename_fix(filename)
                        }
                        filename_issues.append(issue)
                        self.stats['naming_issues'] += 1
                        break
        
        return filename_issues
    
    def check_file_encoding(self) -> List[Dict]:
        """Check for encoding issues that prevent Copilot review."""
        print("🔍 Checking file encoding...")
        encoding_issues = []
        
        text_extensions = {'.tex', '.py', '.md', '.txt', '.sty', '.json', '.yaml', '.yml'}
        
        for file_path in self.repo_path.rglob('*'):
            if (file_path.is_file() and 
                file_path.suffix.lower() in text_extensions and
                not self._is_git_ignored(file_path)):
                
                try:
                    with open(file_path, 'rb') as f:
                        raw_data = f.read()
                    
                    if raw_data:
                        detected = chardet.detect(raw_data)
                        encoding = detected.get('encoding', '').lower()
                        confidence = detected.get('confidence', 0)
                        
                        # Flag non-UTF-8 files with high confidence (but ASCII is fine)
                        if (encoding and 
                            'utf-8' not in encoding and 
                            'ascii' not in encoding and 
                            confidence > 0.7):
                            relative_path = file_path.relative_to(self.repo_path)
                            issue = {
                                'type': 'encoding',
                                'severity': 'warning',
                                'file': str(relative_path),
                                'issue': f'Non-UTF-8 encoding detected: {encoding} (confidence: {confidence:.2f})',
                                'suggestion': 'Convert to UTF-8 encoding'
                            }
                            encoding_issues.append(issue)
                            self.stats['encoding_issues'] += 1
                            
                except Exception as e:
                    relative_path = file_path.relative_to(self.repo_path)
                    issue = {
                        'type': 'encoding',
                        'severity': 'error',
                        'file': str(relative_path),
                        'issue': f'Cannot read file: {e}',
                        'suggestion': 'Check file permissions and encoding'
                    }
                    encoding_issues.append(issue)
        
        return encoding_issues
    
    def check_large_files(self, size_limit_mb: float = 1.0) -> List[Dict]:
        """Check for large files that may block Copilot review."""
        print(f"🔍 Checking for large files (>{size_limit_mb}MB)...")
        large_file_issues = []
        size_limit_bytes = size_limit_mb * 1024 * 1024
        
        for file_path in self.repo_path.rglob('*'):
            if file_path.is_file() and not self._is_git_ignored(file_path):
                try:
                    file_size = file_path.stat().st_size
                    if file_size > size_limit_bytes:
                        relative_path = file_path.relative_to(self.repo_path)
                        size_mb = file_size / (1024 * 1024)
                        
                        issue = {
                            'type': 'large_file',
                            'severity': 'warning',
                            'file': str(relative_path),
                            'issue': f'Large file: {size_mb:.2f}MB',
                            'suggestion': 'Consider adding to .gitignore or using Git LFS'
                        }
                        large_file_issues.append(issue)
                        self.stats['large_files'] += 1
                        
                except Exception as e:
                    pass  # Skip files we can't stat
        
        return large_file_issues
    
    def check_binary_files(self) -> List[Dict]:
        """Check for binary files that should be excluded from review."""
        print("🔍 Checking for binary files...")
        binary_issues = []
        
        binary_extensions = {
            '.pdf', '.docx', '.doc', '.xlsx', '.xls', '.pptx', '.ppt',
            '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico',
            '.zip', '.tar', '.gz', '.exe', '.dll', '.so'
        }
        
        for file_path in self.repo_path.rglob('*'):
            if (file_path.is_file() and 
                file_path.suffix.lower() in binary_extensions and
                not self._is_git_ignored(file_path)):
                
                relative_path = file_path.relative_to(self.repo_path)
                issue = {
                    'type': 'binary_file',
                    'severity': 'warning',
                    'file': str(relative_path),
                    'issue': f'Binary file tracked in git: {file_path.suffix}',
                    'suggestion': f'Add *{file_path.suffix} to .gitignore'
                }
                binary_issues.append(issue)
        
        return binary_issues
    
    def check_repository_structure(self) -> List[Dict]:
        """Check overall repository structure for Copilot compatibility."""
        print("🔍 Checking repository structure...")
        structure_issues = []
        
        # Check for essential files
        essential_files = ['.gitignore', 'README.md']
        for essential_file in essential_files:
            if not (self.repo_path / essential_file).exists():
                issue = {
                    'type': 'structure',
                    'severity': 'warning',
                    'file': essential_file,
                    'issue': f'Missing essential file: {essential_file}',
                    'suggestion': f'Create {essential_file} for better repository structure'
                }
                structure_issues.append(issue)
        
        # Check for common problematic directories
        problematic_dirs = ['node_modules', '__pycache__', '.DS_Store', 'build', 'dist']
        for dir_name in problematic_dirs:
            for dir_path in self.repo_path.rglob(dir_name):
                if dir_path.is_dir() and not self._is_git_ignored(dir_path):
                    relative_path = dir_path.relative_to(self.repo_path)
                    issue = {
                        'type': 'structure',
                        'severity': 'warning',
                        'file': str(relative_path),
                        'issue': f'Directory should be excluded: {dir_name}',
                        'suggestion': f'Add {dir_name}/ to .gitignore'
                    }
                    structure_issues.append(issue)
        
        return structure_issues
    
    def _is_git_ignored(self, file_path: Path) -> bool:
        """Check if a file is ignored by git."""
        try:
            # Use git check-ignore to determine if file should be ignored
            relative_path = file_path.relative_to(self.repo_path)
            result = subprocess.run(
                ['git', 'check-ignore', str(relative_path)],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except:
            return False
    
    def _suggest_filename_fix(self, filename: str) -> str:
        """Suggest a fixed filename."""
        # Replace spaces with underscores
        fixed = re.sub(r'\s+', '_', filename)
        # Remove problematic characters
        fixed = re.sub(r'[<>:"|?*]', '', fixed)
        # Remove leading special characters
        fixed = re.sub(r'^[#@$%]+', '', fixed)
        # Replace multiple dots with single dot
        fixed = re.sub(r'\.{2,}', '.', fixed)
        return fixed
    
    def run_all_checks(self) -> Dict:
        """Run all compatibility checks."""
        print("🚀 Running GitHub Copilot compatibility checks...")
        print(f"📁 Repository: {self.repo_path}")
        print()
        
        all_issues = []
        
        # Run individual checks
        all_issues.extend(self.check_filename_conventions())
        all_issues.extend(self.check_file_encoding())
        all_issues.extend(self.check_large_files())
        all_issues.extend(self.check_binary_files())
        all_issues.extend(self.check_repository_structure())
        
        # Count total files
        for file_path in self.repo_path.rglob('*'):
            if file_path.is_file():
                self.stats['total_files'] += 1
        
        self.issues = all_issues
        self.stats['problematic_files'] = len(set(issue['file'] for issue in all_issues))
        
        return {
            'issues': all_issues,
            'stats': self.stats
        }
    
    def generate_report(self, verbose: bool = True) -> str:
        """Generate a comprehensive compatibility report."""
        if not self.issues:
            return "✅ No compatibility issues found! Repository is optimized for GitHub Copilot review."
        
        report = []
        report.append("=" * 60)
        report.append("GITHUB COPILOT COMPATIBILITY REPORT")
        report.append("=" * 60)
        
        # Summary statistics
        report.append(f"📊 SUMMARY:")
        report.append(f"   Total files scanned: {self.stats['total_files']}")
        report.append(f"   Files with issues: {self.stats['problematic_files']}")
        report.append(f"   Naming issues: {self.stats['naming_issues']}")
        report.append(f"   Encoding issues: {self.stats['encoding_issues']}")
        report.append(f"   Large files: {self.stats['large_files']}")
        report.append("")
        
        # Group issues by type
        issues_by_type = {}
        for issue in self.issues:
            issue_type = issue['type']
            if issue_type not in issues_by_type:
                issues_by_type[issue_type] = []
            issues_by_type[issue_type].append(issue)
        
        # Report each type
        for issue_type, issues in issues_by_type.items():
            report.append(f"🔍 {issue_type.upper().replace('_', ' ')} ISSUES ({len(issues)}):")
            report.append("-" * 40)
            
            for issue in issues:
                severity_icon = "⚠️" if issue['severity'] == 'warning' else "❌"
                report.append(f"{severity_icon} {issue['file']}")
                if verbose:
                    report.append(f"   Issue: {issue['issue']}")
                    report.append(f"   Fix: {issue['suggestion']}")
                report.append("")
        
        # Recommendations
        report.append("💡 RECOMMENDATIONS:")
        report.append("-" * 20)
        if self.stats['naming_issues'] > 0:
            report.append("• Rename files with spaces to use underscores")
        if self.stats['large_files'] > 0:
            report.append("• Add large files to .gitignore or use Git LFS")
        if self.stats['encoding_issues'] > 0:
            report.append("• Convert non-UTF-8 files to UTF-8 encoding")
        
        report.append("")
        report.append("📖 For detailed guidelines, see: .github/COPILOT_REVIEW_GUIDELINES.md")
        
        return "\n".join(report)


def main():
    """Main function with command-line interface."""
    parser = argparse.ArgumentParser(
        description="Check repository compatibility for GitHub Copilot reviews"
    )
    parser.add_argument(
        '--path', '-p',
        default='.',
        help='Path to repository (default: current directory)'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed issue information'
    )
    parser.add_argument(
        '--size-limit',
        type=float,
        default=1.0,
        help='File size limit in MB for large file detection (default: 1.0)'
    )
    parser.add_argument(
        '--format',
        choices=['text', 'json'],
        default='text',
        help='Output format (default: text)'
    )
    
    args = parser.parse_args()
    
    try:
        checker = CopilotCompatibilityChecker(args.path)
        results = checker.run_all_checks()
        
        if args.format == 'json':
            import json
            print(json.dumps(results, indent=2))
        else:
            print(checker.generate_report(verbose=args.verbose))
        
        # Exit with error code if issues found
        if results['issues']:
            sys.exit(1)
        else:
            print("\n✅ Repository is optimized for GitHub Copilot review!")
            sys.exit(0)
            
    except Exception as e:
        print(f"❌ Error running compatibility check: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()