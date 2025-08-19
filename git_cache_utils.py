#!/usr/bin/env python3
"""
Git Cache Utilities for CTMM Repository

This module provides caching utilities to optimize Git command execution
and avoid redundant Git operations during script execution.
"""

import subprocess
import hashlib
from functools import lru_cache
from typing import Tuple, List, Optional

class GitCache:
    """Simple caching mechanism for Git operations to improve performance."""
    
    def __init__(self):
        self._cache = {}
    
    def _cache_key(self, cmd: str) -> str:
        """Generate a cache key for a Git command."""
        return hashlib.md5(cmd.encode()).hexdigest()
    
    def run_cached_git_command(self, cmd: str, capture_output: bool = True) -> Tuple[bool, str, str]:
        """Run a Git command with caching to avoid redundant operations."""
        cache_key = self._cache_key(cmd)
        
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        try:
            result = subprocess.run(cmd, shell=True, capture_output=capture_output, text=True)
            success = result.returncode == 0
            output = (success, result.stdout.strip(), result.stderr.strip())
            
            # Cache the result for future use
            self._cache[cache_key] = output
            return output
        except Exception as e:
            output = (False, "", str(e))
            self._cache[cache_key] = output
            return output
    
    def clear_cache(self):
        """Clear the Git command cache."""
        self._cache.clear()

# Global cache instance
_git_cache = GitCache()

def run_command_cached(cmd: str, capture_output: bool = True) -> Tuple[bool, str, str]:
    """Run a command with caching - drop-in replacement for the original run_command."""
    return _git_cache.run_cached_git_command(cmd, capture_output)

@lru_cache(maxsize=32)
def get_available_branches() -> List[str]:
    """Get available remote branches (cached)."""
    success, stdout, stderr = run_command_cached("git branch -r")
    return stdout.split('\n') if success else []

@lru_cache(maxsize=16)
def check_base_branches_exist(base_options: Tuple[str]) -> List[str]:
    """Check which base branches exist (cached)."""
    # Convert tuple back to list for processing
    base_list = list(base_options)
    
    if not base_list:
        return []
    
    # Use batched git rev-parse for efficiency
    cmd = f"git rev-parse {' '.join(base_list)} 2>/dev/null"
    success, stdout, stderr = run_command_cached(cmd)
    
    valid_bases = []
    if success and stdout.strip():
        hashes = stdout.split('\n')
        for i, h in enumerate(hashes):
            if i < len(base_list) and h.strip() and len(h.strip()) >= 7 and not h.startswith("fatal:"):
                valid_bases.append(base_list[i])
    
    return valid_bases

def find_valid_base_branch(base_branch: str = "main") -> Optional[str]:
    """Find a valid base branch for comparison (cached)."""
    base_options = [f"origin/{base_branch}", base_branch, "origin/main", "main"]
    available_branches = get_available_branches()
    
    # Filter options that might be available
    filtered_options = [opt for opt in base_options 
                       if any(opt in branch for branch in available_branches) or opt == base_branch]
    
    if not filtered_options:
        return None
    
    # Check which ones actually exist (this call is cached)
    valid_bases = check_base_branches_exist(tuple(filtered_options))
    
    return valid_bases[0] if valid_bases else None

def get_file_changes_cached(base_ref: str = None) -> Tuple[bool, int, int, int]:
    """Get file changes with caching for better performance."""
    if base_ref is None:
        base_ref = find_valid_base_branch()
    
    if base_ref is None:
        # Fallback to checking working directory changes
        files_cmd = "git diff --name-only"
        stats_cmd = "git diff --numstat"
    elif base_ref == "--cached":
        files_cmd = "git diff --cached --name-only"
        stats_cmd = "git diff --cached --numstat"
    elif base_ref == "HEAD~1":
        files_cmd = "git diff --name-only HEAD~1..HEAD"
        stats_cmd = "git diff --numstat HEAD~1..HEAD"
    else:
        files_cmd = f"git diff --name-only {base_ref}..HEAD"
        stats_cmd = f"git diff --numstat {base_ref}..HEAD"
    
    # Combine both commands into a single operation where possible
    if base_ref is None:
        # For working directory changes, we can combine name-only and numstat
        combined_cmd = "git diff --numstat"
    elif base_ref == "--cached":
        combined_cmd = "git diff --cached --numstat"
    elif base_ref == "HEAD~1":
        combined_cmd = "git diff --numstat HEAD~1..HEAD"
    else:
        combined_cmd = f"git diff --numstat {base_ref}..HEAD"
    
    # Use the combined command for both file count and statistics
    success, stdout, stderr = run_command_cached(combined_cmd)
    
    if not success:
        return False, 0, 0, 0
    
    changed_files = 0
    added_lines = 0
    deleted_lines = 0
    
    if stdout.strip():
        lines = stdout.strip().split('\n')
        changed_files = len(lines)
        
        for line in lines:
            if line.strip():
                parts = line.split('\t')
                if len(parts) >= 2:
                    try:
                        added_lines += int(parts[0]) if parts[0] != '-' else 0
                        deleted_lines += int(parts[1]) if parts[1] != '-' else 0
                    except ValueError:
                        continue
    
    return True, changed_files, added_lines, deleted_lines

def clear_git_cache():
    """Clear the Git command cache."""
    _git_cache.clear_cache()
    # Clear LRU caches too
    get_available_branches.cache_clear()
    check_base_branches_exist.cache_clear()