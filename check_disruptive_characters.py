#!/usr/bin/env python3
"""
Script to find disruptive characters that could block merges:
- Merge conflict markers (<<<<<<, =======, >>>>>>>)
- BOM (Byte Order Mark) characters
- Null bytes
- Unusual control characters
- Mixed line endings
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Tuple, Any
import codecs

# File extensions to check
EXTENSIONS = [
    '.tex', '.sty', '.py', '.md', '.yml', '.yaml', '.json',
    '.txt', '.sh', '.bash', '.css', '.html', '.js', '.ts'
]

# Directories to skip
SKIP_DIRS = {
    '.git', '__pycache__', 'node_modules', '.venv', 'venv',
    'dist', 'build', '.pytest_cache', '.mypy_cache', 'main.pdf'
}


class DisruptiveCharacterFinder:
    def __init__(self):
        # Regex patterns for merge conflict markers
        self.conflict_start = re.compile(r'^<{7}(\s|$)')
        self.conflict_sep = re.compile(r'^={7}(\s|$)')
        self.conflict_end = re.compile(r'^>{7}(\s|$)')
    
    def should_check_file(self, file_path: Path) -> bool:
        """Check if file should be scanned."""
        # Skip binary files
        if file_path.name.endswith(('.pdf', '.png', '.jpg', '.jpeg', '.gif', '.zip', '.tar', '.gz')):
            return False
        
        # Skip if in excluded directory
        for part in file_path.parts:
            if part in SKIP_DIRS:
                return False
        
        # Check extension or no extension
        if file_path.suffix.lower() in EXTENSIONS or not file_path.suffix:
            return True
        
        return False
    
    def check_file(self, file_path: Path) -> Dict[str, Any]:
        """Check a file for various disruptive characters."""
        issues = []
        
        try:
            # Read file as binary first
            with open(file_path, 'rb') as f:
                content_bytes = f.read()
            
            # Check for BOM
            if content_bytes.startswith(codecs.BOM_UTF8):
                issues.append({
                    'type': 'BOM',
                    'description': 'UTF-8 BOM detected at start of file',
                    'severity': 'low'
                })
            
            if content_bytes.startswith(codecs.BOM_UTF16_LE) or content_bytes.startswith(codecs.BOM_UTF16_BE):
                issues.append({
                    'type': 'BOM',
                    'description': 'UTF-16 BOM detected',
                    'severity': 'medium'
                })
            
            # Check for null bytes
            if b'\x00' in content_bytes:
                issues.append({
                    'type': 'null_byte',
                    'description': 'Null bytes found (file may be binary)',
                    'severity': 'high'
                })
                # Don't continue checking if null bytes found (likely binary)
                return issues
            
            # Decode and check text content
            try:
                content = content_bytes.decode('utf-8')
            except UnicodeDecodeError:
                try:
                    content = content_bytes.decode('latin-1')
                    issues.append({
                        'type': 'encoding',
                        'description': 'File is not UTF-8 encoded',
                        'severity': 'low'
                    })
                except UnicodeDecodeError:
                    issues.append({
                        'type': 'encoding',
                        'description': 'Unable to decode file',
                        'severity': 'high'
                    })
                    return issues
            
            lines = content.split('\n')
            
            # Check for merge conflict markers (exactly 7 characters or 7 followed by space/text)
            for i, line in enumerate(lines, 1):
                if self.conflict_start.match(line):
                    issues.append({
                        'type': 'conflict_marker',
                        'line': i,
                        'description': f'Merge conflict start marker at line {i}',
                        'severity': 'critical',
                        'content': line[:50]
                    })
                elif self.conflict_sep.match(line):
                    issues.append({
                        'type': 'conflict_marker',
                        'line': i,
                        'description': f'Merge conflict separator at line {i}',
                        'severity': 'critical',
                        'content': line[:50]
                    })
                elif self.conflict_end.match(line):
                    issues.append({
                        'type': 'conflict_marker',
                        'line': i,
                        'description': f'Merge conflict end marker at line {i}',
                        'severity': 'critical',
                        'content': line[:50]
                    })
            
            # Check for mixed line endings
            has_crlf = '\r\n' in content
            has_lf = '\n' in content.replace('\r\n', '')
            if has_crlf and has_lf:
                issues.append({
                    'type': 'mixed_line_endings',
                    'description': 'Mixed line endings (CRLF and LF)',
                    'severity': 'low'
                })
            
            # Check for unusual control characters (except tab, newline, carriage return)
            control_chars = []
            for i, char in enumerate(content):
                if ord(char) < 32 and char not in ['\t', '\n', '\r']:
                    control_chars.append((i, ord(char)))
            
            if control_chars:
                issues.append({
                    'type': 'control_characters',
                    'description': f'{len(control_chars)} unusual control characters found',
                    'severity': 'medium',
                    'details': control_chars[:5]  # Show first 5
                })
            
            # Check for zero-width characters
            zero_width_chars = ['\u200b', '\u200c', '\u200d', '\ufeff']
            for i, char in enumerate(content):
                if char in zero_width_chars:
                    issues.append({
                        'type': 'zero_width',
                        'char_pos': i,
                        'description': f'Zero-width character found at position {i}',
                        'severity': 'low'
                    })
                    break  # Just report first one
        
        except Exception as e:
            issues.append({
                'type': 'error',
                'description': f'Error checking file: {str(e)}',
                'severity': 'high'
            })
        
        return issues
    
    def scan_repository(self, root_dir: Path) -> Dict[str, List[Dict]]:
        """Scan entire repository for disruptive characters."""
        all_issues = {}
        
        for root, dirs, files in os.walk(root_dir):
            # Remove skip dirs from traversal
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            
            for filename in files:
                file_path = Path(root) / filename
                
                if self.should_check_file(file_path):
                    issues = self.check_file(file_path)
                    if issues:
                        rel_path = file_path.relative_to(root_dir)
                        all_issues[str(rel_path)] = issues
        
        return all_issues
    
    def print_report(self, issues: Dict[str, List[Dict]]) -> None:
        """Print a detailed report of all issues found."""
        if not issues:
            print("✅ No disruptive characters found in repository!")
            print("   Repository is clean and ready for merging.")
            return
        
        # Count by severity
        severity_counts = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
        
        print(f"⚠️  Found issues in {len(issues)} file(s):\n")
        
        for file_path, file_issues in sorted(issues.items()):
            # Only show critical and high severity issues by default
            critical_issues = [i for i in file_issues if i.get('severity') in ['critical', 'high']]
            
            if critical_issues:
                print(f"📄 {file_path}")
                print(f"   {len(critical_issues)} critical/high severity issue(s):")
                
                for issue in critical_issues:
                    severity = issue.get('severity', 'unknown')
                    severity_counts[severity] = severity_counts.get(severity, 0) + 1
                    
                    symbol = {
                        'critical': '🔴',
                        'high': '🟠',
                        'medium': '🟡',
                        'low': '🟢'
                    }.get(severity, '⚪')
                    
                    desc = issue['description']
                    if 'line' in issue:
                        print(f"   {symbol} Line {issue['line']}: {desc}")
                        if 'content' in issue:
                            print(f"      Content: {issue['content']}")
                    else:
                        print(f"   {symbol} {desc}")
                print()
        
        # Summary
        print(f"\n📊 Summary:")
        print(f"   Files with issues: {len(issues)}")
        if severity_counts['critical'] > 0:
            print(f"   🔴 Critical issues: {severity_counts['critical']}")
        if severity_counts['high'] > 0:
            print(f"   🟠 High severity: {severity_counts['high']}")
        if severity_counts['medium'] > 0:
            print(f"   🟡 Medium severity: {severity_counts['medium']}")
        if severity_counts['low'] > 0:
            print(f"   🟢 Low severity: {severity_counts['low']}")


def main():
    """Main function to run the disruptive character checker."""
    print("=" * 70)
    print("CTMM Repository - Disruptive Character Scanner")
    print("=" * 70)
    print("Checking for:")
    print("  - Merge conflict markers")
    print("  - BOM (Byte Order Mark) characters")
    print("  - Null bytes")
    print("  - Unusual control characters")
    print("  - Mixed line endings")
    print("  - Zero-width characters")
    print()
    
    # Get repository root
    repo_root = Path(__file__).parent
    print(f"Scanning directory: {repo_root}")
    print()
    
    # Create scanner and scan
    scanner = DisruptiveCharacterFinder()
    issues = scanner.scan_repository(repo_root)
    
    # Print report
    scanner.print_report(issues)
    
    # Exit with appropriate code
    if any(i.get('severity') in ['critical', 'high'] for issues_list in issues.values() for i in issues_list):
        print("\n❌ Action required: Fix critical/high severity issues before merging.")
        return 1
    elif issues:
        print("\n⚠️  Some minor issues found, but they shouldn't block merging.")
        return 0
    else:
        print("\n✅ Repository is clean!")
        return 0


if __name__ == "__main__":
    exit(main())
