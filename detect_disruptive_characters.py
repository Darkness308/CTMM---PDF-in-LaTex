#!/usr/bin/env python3
"""
Character Encoding and Disruptive Character Detection for LaTeX Files

This script scans LaTeX files for potentially problematic characters that could
cause build failures, including:
- Non-ASCII characters that might not be properly escaped
- Invalid UTF-8 sequences
- Hidden control characters
- Byte Order Marks (BOM)
- Windows line endings (CRLF)
- Other special characters that could disrupt LaTeX compilation
"""

import os
import sys
import chardet
from pathlib import Path
from typing import List, Dict, Tuple, Set


class CharacterValidator:
    """Validates character encoding and detects disruptive characters in files."""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.issues_found = []
        self.files_scanned = 0
        self.files_with_issues = 0
        
    def detect_encoding(self, file_path: Path) -> Dict[str, any]:
        """Detect the encoding of a file."""
        try:
            with open(file_path, 'rb') as f:
                raw_data = f.read()
                result = chardet.detect(raw_data)
                return {
                    'encoding': result['encoding'],
                    'confidence': result['confidence'],
                    'has_bom': raw_data.startswith(b'\xef\xbb\xbf'),  # UTF-8 BOM
                    'raw_data': raw_data
                }
        except Exception as e:
            return {
                'encoding': 'ERROR',
                'confidence': 0.0,
                'has_bom': False,
                'error': str(e)
            }
    
    def check_line_endings(self, raw_data: bytes) -> Dict[str, any]:
        """Check for line ending types."""
        crlf_count = raw_data.count(b'\r\n')
        lf_count = raw_data.count(b'\n') - crlf_count  # Subtract CRLF's LF
        cr_count = raw_data.count(b'\r') - crlf_count   # Subtract CRLF's CR
        
        return {
            'crlf': crlf_count,
            'lf': lf_count,
            'cr': cr_count,
            'mixed': (crlf_count > 0 and lf_count > 0) or (cr_count > 0)
        }
    
    def find_control_characters(self, content: str, file_path: Path) -> List[Dict]:
        """Find hidden control characters in the content."""
        issues = []
        
        for line_num, line in enumerate(content.splitlines(), 1):
            for char_pos, char in enumerate(line, 1):
                # Check for control characters (excluding common whitespace)
                if ord(char) < 32 and char not in '\n\r\t':
                    issues.append({
                        'type': 'control_character',
                        'line': line_num,
                        'column': char_pos,
                        'char': repr(char),
                        'ord': ord(char),
                        'context': line[max(0, char_pos-10):char_pos+10]
                    })
        
        return issues
    
    def find_problematic_non_ascii(self, content: str, file_path: Path) -> List[Dict]:
        """Find potentially problematic non-ASCII characters."""
        issues = []
        
        # Characters that should typically be escaped in LaTeX
        problematic_chars = {
            '§': r'\S',
            '°': r'\degree',
            '±': r'\pm',
            '×': r'\times',
            '÷': r'\div',
            '€': r'\euro',
            '£': r'\pounds',
            '¥': r'\yen',
            '©': r'\copyright',
            '®': r'\textregistered',
            '™': r'\texttrademark',
            '…': r'\ldots',
            '–': r'--',
            '—': r'---',
            ''': r'`',
            ''': r"'",
            '"': r'``',
            '"': r"''",
        }
        
        for line_num, line in enumerate(content.splitlines(), 1):
            for char_pos, char in enumerate(line, 1):
                if ord(char) > 127:  # Non-ASCII
                    # Check if it's a problematic character
                    if char in problematic_chars:
                        # Check if it's already escaped (basic check)
                        context_start = max(0, char_pos - 10)
                        context = line[context_start:char_pos+10]
                        
                        # Skip if preceded by backslash (likely already escaped)
                        if char_pos > 0 and line[char_pos-2] == '\\':
                            continue
                        
                        issues.append({
                            'type': 'unescaped_special_char',
                            'line': line_num,
                            'column': char_pos,
                            'char': char,
                            'ord': ord(char),
                            'suggested_escape': problematic_chars[char],
                            'context': context
                        })
        
        return issues
    
    def validate_utf8(self, raw_data: bytes) -> Tuple[bool, List[Dict]]:
        """Validate UTF-8 encoding and find invalid sequences."""
        issues = []
        
        try:
            # Try to decode as UTF-8
            raw_data.decode('utf-8')
            return True, issues
        except UnicodeDecodeError as e:
            issues.append({
                'type': 'invalid_utf8',
                'position': e.start,
                'reason': str(e.reason),
                'object': repr(e.object[max(0, e.start-10):e.end+10])
            })
            return False, issues
    
    def scan_file(self, file_path: Path) -> Dict:
        """Scan a single file for all types of issues."""
        self.files_scanned += 1
        result = {
            'file': str(file_path),
            'issues': [],
            'warnings': [],
            'info': {}
        }
        
        # Detect encoding
        encoding_info = self.detect_encoding(file_path)
        result['info']['encoding'] = encoding_info['encoding']
        result['info']['confidence'] = encoding_info['confidence']
        
        if 'error' in encoding_info:
            result['issues'].append({
                'type': 'file_read_error',
                'message': encoding_info['error']
            })
            self.files_with_issues += 1
            return result
        
        raw_data = encoding_info['raw_data']
        
        # Check for BOM
        if encoding_info['has_bom']:
            result['issues'].append({
                'type': 'bom_detected',
                'message': 'UTF-8 BOM detected at start of file'
            })
        
        # Check line endings
        line_endings = self.check_line_endings(raw_data)
        result['info']['line_endings'] = line_endings
        
        if line_endings['mixed']:
            result['warnings'].append({
                'type': 'mixed_line_endings',
                'message': f"Mixed line endings detected (CRLF: {line_endings['crlf']}, LF: {line_endings['lf']}, CR: {line_endings['cr']})"
            })
        elif line_endings['crlf'] > 0:
            result['warnings'].append({
                'type': 'windows_line_endings',
                'message': f"Windows line endings (CRLF) detected: {line_endings['crlf']} occurrences"
            })
        
        # Validate UTF-8
        is_valid_utf8, utf8_issues = self.validate_utf8(raw_data)
        if not is_valid_utf8:
            result['issues'].extend(utf8_issues)
        
        # Try to read file content for further analysis
        try:
            with open(file_path, 'r', encoding=encoding_info['encoding'] or 'utf-8', errors='replace') as f:
                content = f.read()
            
            # Find control characters
            control_chars = self.find_control_characters(content, file_path)
            if control_chars:
                result['issues'].extend(control_chars)
            
            # Find problematic non-ASCII characters
            non_ascii_issues = self.find_problematic_non_ascii(content, file_path)
            if non_ascii_issues:
                result['warnings'].extend(non_ascii_issues)
            
        except Exception as e:
            result['issues'].append({
                'type': 'content_analysis_error',
                'message': f"Error analyzing content: {str(e)}"
            })
        
        # Mark file if it has issues
        if result['issues'] or result['warnings']:
            self.files_with_issues += 1
        
        return result
    
    def scan_directory(self, directory: Path, extensions: List[str] = ['.tex']) -> List[Dict]:
        """Scan all files in a directory with specified extensions."""
        results = []
        
        for ext in extensions:
            for file_path in directory.rglob(f'*{ext}'):
                if self.verbose:
                    print(f"Scanning: {file_path}")
                result = self.scan_file(file_path)
                results.append(result)
        
        return results
    
    def print_summary(self, results: List[Dict]):
        """Print a summary of the scan results."""
        print("\n" + "=" * 80)
        print("CHARACTER VALIDATION SUMMARY")
        print("=" * 80)
        print(f"\nFiles scanned: {self.files_scanned}")
        print(f"Files with issues/warnings: {self.files_with_issues}")
        
        # Count issue types
        issue_counts = {}
        warning_counts = {}
        
        for result in results:
            for issue in result.get('issues', []):
                issue_type = issue.get('type', 'unknown')
                issue_counts[issue_type] = issue_counts.get(issue_type, 0) + 1
            
            for warning in result.get('warnings', []):
                warning_type = warning.get('type', 'unknown')
                warning_counts[warning_type] = warning_counts.get(warning_type, 0) + 1
        
        if issue_counts:
            print("\n❌ CRITICAL ISSUES:")
            for issue_type, count in sorted(issue_counts.items()):
                print(f"  - {issue_type}: {count}")
        
        if warning_counts:
            print("\n⚠️  WARNINGS:")
            for warning_type, count in sorted(warning_counts.items()):
                print(f"  - {warning_type}: {count}")
        
        if not issue_counts and not warning_counts:
            print("\n✅ No issues or warnings found!")
        
        print("\n" + "=" * 80)
    
    def print_detailed_report(self, results: List[Dict]):
        """Print a detailed report of all findings."""
        print("\n" + "=" * 80)
        print("DETAILED FINDINGS")
        print("=" * 80)
        
        for result in results:
            if not result.get('issues') and not result.get('warnings'):
                continue
            
            print(f"\n📄 File: {result['file']}")
            print(f"   Encoding: {result['info'].get('encoding', 'unknown')} "
                  f"(confidence: {result['info'].get('confidence', 0):.2%})")
            
            # Print issues
            if result.get('issues'):
                print("\n   ❌ CRITICAL ISSUES:")
                for issue in result['issues']:
                    self._print_issue_details(issue)
            
            # Print warnings
            if result.get('warnings'):
                print("\n   ⚠️  WARNINGS:")
                for warning in result['warnings']:
                    self._print_issue_details(warning)
        
        print("\n" + "=" * 80)
    
    def _print_issue_details(self, issue: Dict):
        """Print details of a single issue or warning."""
        issue_type = issue.get('type', 'unknown')
        
        if issue_type == 'control_character':
            print(f"      Line {issue['line']}, Col {issue['column']}: "
                  f"Control character {issue['char']} (ord={issue['ord']})")
            print(f"      Context: {repr(issue.get('context', ''))}")
        
        elif issue_type == 'unescaped_special_char':
            print(f"      Line {issue['line']}, Col {issue['column']}: "
                  f"Unescaped '{issue['char']}' (ord={issue['ord']})")
            print(f"      Suggested LaTeX escape: {issue.get('suggested_escape', 'N/A')}")
            print(f"      Context: {issue.get('context', '')}")
        
        elif 'message' in issue:
            print(f"      {issue['message']}")
        
        else:
            print(f"      {issue_type}: {issue}")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Detect disruptive characters in LaTeX files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                          # Scan all .tex files in current directory
  %(prog)s --dir modules            # Scan modules directory
  %(prog)s --verbose                # Show detailed scanning progress
  %(prog)s --no-detailed-report     # Show only summary
        """
    )
    parser.add_argument('--dir', type=str, default='.',
                        help='Directory to scan (default: current directory)')
    parser.add_argument('--extensions', type=str, default='.tex',
                        help='Comma-separated file extensions to scan (default: .tex)')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Show verbose output during scanning')
    parser.add_argument('--no-detailed-report', action='store_true',
                        help='Skip detailed report, show only summary')
    
    args = parser.parse_args()
    
    # Parse extensions
    extensions = [ext.strip() if ext.startswith('.') else f'.{ext.strip()}'
                  for ext in args.extensions.split(',')]
    
    # Create validator
    validator = CharacterValidator(verbose=args.verbose)
    
    # Scan directory
    directory = Path(args.dir)
    if not directory.exists():
        print(f"Error: Directory '{directory}' does not exist", file=sys.stderr)
        return 1
    
    print(f"Scanning directory: {directory.absolute()}")
    print(f"File extensions: {', '.join(extensions)}")
    
    results = validator.scan_directory(directory, extensions)
    
    # Print reports
    if not args.no_detailed_report:
        validator.print_detailed_report(results)
    
    validator.print_summary(results)
    
    # Return exit code based on critical issues
    critical_issues = sum(len(r.get('issues', [])) for r in results)
    return 1 if critical_issues > 0 else 0


if __name__ == '__main__':
    sys.exit(main())
