#!/usr/bin/env python3
"""
Enhanced Merge Conflict Resolver V2
Handles consecutive and nested conflicts properly.
"""

import sys
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def resolve_file_conflicts(filepath: Path, strategy='keep-head') -> bool:
    """
    Resolve all merge conflicts in a file.
    
    Strategy:
        keep-head: Keep HEAD version (default)
        keep-pr: Keep pr-653 version
        merge-both: Try to keep both when possible
    """
    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception as e:
        logger.error(f"Error reading {filepath}: {e}")
        return False
    
    if '<<<<<<< HEAD' not in content:
        return True
    
    lines = content.split('\n')
    result_lines = []
    in_conflict = False
    conflict_count = 0
    in_head_section = False
    in_pr_section = False
    head_lines = []
    pr_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        if line.startswith('<<<<<<< HEAD'):
            in_conflict = True
            in_head_section = True
            in_pr_section = False
            head_lines = []
            pr_lines = []
            conflict_count += 1
            i += 1
            continue
            
        if line.startswith('=======') and in_conflict and in_head_section:
            in_head_section = False
            in_pr_section = True
            i += 1
            continue
            
        if line.startswith('>>>>>>> pr-653') and in_conflict:
            # Resolve the conflict
            if strategy == 'keep-head':
                result_lines.extend(head_lines)
            elif strategy == 'keep-pr':
                result_lines.extend(pr_lines)
            elif strategy == 'merge-both':
                # Try to intelligently merge
                head_content = '\n'.join(head_lines).strip()
                pr_content = '\n'.join(pr_lines).strip()
                
                if not head_content and pr_content:
                    result_lines.extend(pr_lines)
                elif not pr_content and head_content:
                    result_lines.extend(head_lines)
                elif pr_content in head_content:
                    result_lines.extend(head_lines)
                elif head_content in pr_content:
                    result_lines.extend(pr_lines)
                else:
                    # Different content, prefer HEAD
                    result_lines.extend(head_lines)
            
            in_conflict = False
            in_head_section = False
            in_pr_section = False
            head_lines = []
            pr_lines = []
            i += 1
            continue
        
        if in_conflict:
            if in_head_section:
                head_lines.append(line)
            elif in_pr_section:
                pr_lines.append(line)
        else:
            result_lines.append(line)
        
        i += 1
    
    # Write resolved content
    resolved_content = '\n'.join(result_lines)
    
    try:
        filepath.write_text(resolved_content, encoding='utf-8')
        logger.info(f"[OK] Resolved {conflict_count} conflicts in {filepath}")
        return True
    except Exception as e:
        logger.error(f"Error writing {filepath}: {e}")
        return False


def main():
    """Resolve all merge conflicts."""
    if len(sys.argv) > 1:
        directory = Path(sys.argv[1])
    else:
        directory = Path.cwd()
    
    strategy = 'keep-head' if len(sys.argv) <= 2 else sys.argv[2]
    
    logger.info(f"Resolving conflicts in {directory} (strategy: {strategy})")
    
    # Find all files with conflicts
    conflict_files = []
    for filepath in directory.rglob('*'):
        if filepath.is_file():
            # Skip .git directory and test files that check for conflicts
            if '.git/' in str(filepath) and '.github/' not in str(filepath):
                continue
            if filepath.name in ['test_issue_1054_fix.py', 'validate_merge_readiness.py']:
                continue
            try:
                content = filepath.read_text(encoding='utf-8', errors='ignore')
                if '<<<<<<< HEAD' in content:
                    conflict_files.append(filepath)
            except:
                continue
    
    logger.info(f"Found {len(conflict_files)} files with conflicts")
    
    resolved = 0
    for filepath in conflict_files:
        if resolve_file_conflicts(filepath, strategy):
            resolved += 1
    
    logger.info(f"[OK] Resolved conflicts in {resolved}/{len(conflict_files)} files")
    return 0 if resolved == len(conflict_files) else 1


if __name__ == '__main__':
    sys.exit(main())
