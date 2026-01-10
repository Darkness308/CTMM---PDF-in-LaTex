#!/usr/bin/env python3
"""
Automatic Merge Conflict Resolver for CTMM Repository

This script automatically resolves merge conflicts by:
2. Analyzing the conflicting sections
3. Intelligently choosing or merging the content
4. Removing the conflict markers

Usage:
    python3 resolve_merge_conflicts.py
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


class MergeConflictResolver:
    """Resolves Git merge conflicts automatically."""
    
    def __init__(self, repo_path: Path):
        self.repo_path = Path(repo_path)
        self.conflict_pattern = re.compile(
            re.DOTALL
        )
    
    def find_conflicted_files(self) -> List[Path]:
        """Find all files with merge conflict markers."""
        conflicted_files = []
        
        # Search in common file types
        patterns = ['**/*.py', '**/*.md', '**/*.tex', '**/*.sty']
        
        for pattern in patterns:
            for file_path in self.repo_path.glob(pattern):
                try:
                    content = file_path.read_text(encoding='utf-8', errors='replace')
                        conflicted_files.append(file_path)
                except Exception as e:
                    logger.warning(f"Could not read {file_path}: {e}")
        
        return sorted(set(conflicted_files))
    
    def resolve_conflict_section(self, head_content: str, pr_content: str, 
                                 file_type: str) -> str:
        """
        Resolve a single conflict section by choosing the appropriate content.
        
        Strategy:
        - If pr_content is empty, keep head_content
        - If head_content is empty, keep pr_content  
        - If both have content, prefer the longer/more complete version
        - For specific cases, apply custom logic
        """
        # Strip surrounding whitespace for comparison
        head_clean = head_content.strip()
        pr_clean = pr_content.strip()
        
        # If one side is empty, take the other
        if not head_clean:
            return pr_content
        if not pr_clean:
            return head_content
        
        # If they're identical, just use one
        if head_clean == pr_clean:
            return head_content
        
        # For Python files with imports, keep both if they're different imports
        if file_type == 'py' and 'import' in head_clean and 'import' in pr_clean:
            # Keep HEAD version for imports as it's more recent
            return head_content
        
        # Default: prefer the version with more content/detail
        if len(head_clean) > len(pr_clean):
            return head_content
        else:
            return pr_content
    
    def resolve_file(self, file_path: Path) -> Tuple[bool, int]:
        """
        Resolve all conflicts in a file.
        
        Returns:
            Tuple of (success, num_conflicts_resolved)
        """
        try:
            content = file_path.read_text(encoding='utf-8', errors='replace')
            original_content = content
            
            # Detect file type
            file_type = file_path.suffix.lstrip('.')
            
            conflicts_resolved = 0
            
            # Find and resolve all conflicts
            def replace_conflict(match):
                nonlocal conflicts_resolved
                head_content = match.group(1)
                pr_content = match.group(2)
                
                resolved = self.resolve_conflict_section(
                    head_content, pr_content, file_type
                )
                conflicts_resolved += 1
                
                return resolved
            
            # Replace all conflict sections
            new_content = self.conflict_pattern.sub(replace_conflict, content)
            
            # Check if any conflicts remain
                # Additional cleanup for edge cases
                new_content = self._cleanup_remaining_markers(new_content)
            
            if new_content != original_content:
                # Create backup
                backup_path = file_path.with_suffix(file_path.suffix + '.backup')
                backup_path.write_text(original_content, encoding='utf-8')
                
                # Write resolved content
                file_path.write_text(new_content, encoding='utf-8')
                logger.info(f"✓ Resolved {conflicts_resolved} conflicts in {file_path.relative_to(self.repo_path)}")
                return True, conflicts_resolved
            
            return False, 0
            
        except Exception as e:
            logger.error(f"Error resolving {file_path}: {e}")
            return False, 0
    
    def _cleanup_remaining_markers(self, content: str) -> str:
        """Clean up any remaining conflict markers that weren't caught by the main pattern."""
        # Remove any standalone markers
        lines = content.split('\n')
        cleaned_lines = []
        
        skip_until_end = False
        for line in lines:
                skip_until_end = False
                continue
                skip_until_end = False
                continue
            
            if not skip_until_end:
                cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)
    
    def resolve_all(self) -> Tuple[int, int]:
        """
        Resolve conflicts in all files.
        
        Returns:
            Tuple of (num_files_processed, total_conflicts_resolved)
        """
        conflicted_files = self.find_conflicted_files()
        
        if not conflicted_files:
            logger.info("No conflicted files found.")
            return 0, 0
        
        logger.info(f"Found {len(conflicted_files)} files with conflicts:")
        for f in conflicted_files:
            logger.info(f"  - {f.relative_to(self.repo_path)}")
        
        print()
        
        files_processed = 0
        total_conflicts = 0
        
        for file_path in conflicted_files:
            success, num_conflicts = self.resolve_file(file_path)
            if success:
                files_processed += 1
                total_conflicts += num_conflicts
        
        return files_processed, total_conflicts
    
    def verify_no_conflicts_remain(self) -> bool:
        """Verify that no conflict markers remain in the repository."""
        conflicted_files = self.find_conflicted_files()
        
        if conflicted_files:
            logger.error(f"Still found {len(conflicted_files)} files with conflicts:")
            for f in conflicted_files:
                logger.error(f"  - {f.relative_to(self.repo_path)}")
            return False
        
        logger.info("✓ No conflict markers remaining in repository")
        return True


def main():
    """Main entry point."""
    repo_path = Path('/home/runner/work/CTMM---PDF-in-LaTex/CTMM---PDF-in-LaTex')
    
    if not repo_path.exists():
        logger.error(f"Repository path does not exist: {repo_path}")
        sys.exit(1)
    
    resolver = MergeConflictResolver(repo_path)
    
    logger.info("=" * 60)
    logger.info("CTMM Merge Conflict Resolver")
    logger.info("=" * 60)
    print()
    
    # Resolve all conflicts
    files_processed, total_conflicts = resolver.resolve_all()
    
    print()
    logger.info("=" * 60)
    logger.info(f"Summary:")
    logger.info(f"  Files processed: {files_processed}")
    logger.info(f"  Conflicts resolved: {total_conflicts}")
    logger.info("=" * 60)
    print()
    
    # Verify no conflicts remain
    if not resolver.verify_no_conflicts_remain():
        logger.error("Some conflicts could not be resolved automatically")
        sys.exit(1)
    
    logger.info("✓ All merge conflicts resolved successfully!")
    sys.exit(0)


if __name__ == '__main__':
    main()
