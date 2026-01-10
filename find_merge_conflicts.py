#!/usr/bin/env python3
"""
Script to find and report merge conflict markers in the repository.
Searches for:
- <<<<<<< (conflict start)
- ======= (conflict separator)
- >>>>>>> (conflict end)
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Tuple

# Patterns for merge conflict markers
CONFLICT_START = re.compile(r'^<{7}(\s|$)')
CONFLICT_SEP = re.compile(r'^={7}(\s|$)')
CONFLICT_END = re.compile(r'^>{7}(\s|$)')

# File extensions to check
EXTENSIONS = [
    '.tex', '.sty', '.py', '.md', '.yml', '.yaml', '.json',
    '.txt', '.sh', '.bash', '.css', '.html', '.js', '.ts'
]

# Directories to skip
SKIP_DIRS = {
    '.git', '__pycache__', 'node_modules', '.venv', 'venv',
    'dist', 'build', '.pytest_cache', '.mypy_cache'
}


def should_check_file(file_path: Path) -> bool:
    """Check if file should be scanned for conflict markers."""
    # Skip if in excluded directory
    for part in file_path.parts:
        if part in SKIP_DIRS:
            return False
    
    # Check extension
    if file_path.suffix.lower() in EXTENSIONS:
        return True
    
    # Also check files without extension
    if not file_path.suffix and file_path.is_file():
        return True
    
    return False


def find_conflicts_in_file(file_path: Path) -> List[Dict[str, any]]:
    """
    Find merge conflict markers in a file.
    Returns list of conflicts with line numbers and content.
    """
    conflicts = []
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        
        for i, line in enumerate(lines, 1):
            if CONFLICT_START.match(line):
                conflicts.append({
                    'file': str(file_path),
                    'line': i,
                    'type': 'start',
                    'content': line.rstrip()
                })
            elif CONFLICT_SEP.match(line):
                conflicts.append({
                    'file': str(file_path),
                    'line': i,
                    'type': 'separator',
                    'content': line.rstrip()
                })
            elif CONFLICT_END.match(line):
                conflicts.append({
                    'file': str(file_path),
                    'line': i,
                    'type': 'end',
                    'content': line.rstrip()
                })
    
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    
    return conflicts


def scan_repository(root_dir: Path) -> Dict[str, List[Dict]]:
    """
    Scan entire repository for merge conflict markers.
    Returns dictionary mapping file paths to lists of conflicts.
    """
    all_conflicts = {}
    
    for root, dirs, files in os.walk(root_dir):
        # Remove skip dirs from traversal
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        
        for filename in files:
            file_path = Path(root) / filename
            
            if should_check_file(file_path):
                conflicts = find_conflicts_in_file(file_path)
                if conflicts:
                    # Make path relative to root
                    rel_path = file_path.relative_to(root_dir)
                    all_conflicts[str(rel_path)] = conflicts
    
    return all_conflicts


def print_report(conflicts: Dict[str, List[Dict]]) -> None:
    """Print a detailed report of all conflicts found."""
    if not conflicts:
        print("✅ No merge conflict markers found in repository!")
        print("   Repository is clean and ready for merging.")
        return
    
    print(f"⚠️  Found merge conflict markers in {len(conflicts)} file(s):\n")
    
    for file_path, file_conflicts in sorted(conflicts.items()):
        print(f"📄 {file_path}")
        print(f"   {len(file_conflicts)} conflict marker(s) found:")
        
        for conflict in file_conflicts:
            marker_type = conflict['type']
            line_num = conflict['line']
            content = conflict['content'][:80]  # Truncate long lines
            
            symbol = {
                'start': '<<<',
                'separator': '===',
                'end': '>>>'
            }.get(marker_type, '???')
            
            print(f"   Line {line_num:4d} [{symbol}]: {content}")
        print()
    
    print(f"\n📊 Summary:")
    print(f"   Total files with conflicts: {len(conflicts)}")
    total_markers = sum(len(c) for c in conflicts.values())
    print(f"   Total conflict markers: {total_markers}")


def main():
    """Main function to run the conflict scanner."""
    print("=" * 70)
    print("CTMM Repository - Merge Conflict Marker Scanner")
    print("=" * 70)
    print()
    
    # Get repository root
    repo_root = Path(__file__).parent
    print(f"Scanning directory: {repo_root}")
    print()
    
    # Scan for conflicts
    conflicts = scan_repository(repo_root)
    
    # Print report
    print_report(conflicts)
    
    # Exit with appropriate code
    if conflicts:
        print("\n❌ Action required: Remove merge conflict markers before merging.")
        return 1
    else:
        print("\n✅ Repository is clean!")
        return 0


if __name__ == "__main__":
    exit(main())
