# Merge Conflict Quick Reference Guide

This guide provides instructions for identifying and resolving merge conflicts in the CTMM repository.

## Quick Detection

### Find files with conflicts:
```bash
# Search for conflict markers
grep -r "<<<<<<< HEAD" . --include="*.tex" --include="*.md" --include="*.py" --include="*.sty"

# Count files with conflicts
grep -l "<<<<<<< HEAD" . -r --include="*.tex" --include="*.md" --include="*.py" --include="*.sty" | wc -l

# List files with conflict counts
for file in $(grep -l "<<<<<<< HEAD" . -r --include="*.tex" --include="*.md" --include="*.py" --include="*.sty"); do 
  echo "$file: $(grep -c "<<<<<<< HEAD" "$file") conflicts"
done
```

## Understanding Conflict Markers

Merge conflicts are marked with three types of markers:

```
<<<<<<< HEAD
Content from current branch (HEAD)
=======
Content from incoming branch
>>>>>>> branch-name
```

## Resolution Strategies

### 1. Keep HEAD version (current branch)
Remove markers and incoming content:
```
Content from current branch (HEAD)
```

### 2. Keep incoming version
Remove markers and HEAD content:
```
Content from incoming branch
```

### 3. Merge both versions
Keep relevant parts from both:
```
Content from current branch (HEAD)

Content from incoming branch
```

## File-Specific Guidelines

### Documentation Files (.md)
- **Strategy**: Usually prefer HEAD (newer documentation)
- **Reason**: Documentation tends to evolve, keep latest
- **Exception**: If incoming has significant new sections, merge both

### LaTeX Files (.tex)
- **Strategy**: Prefer HEAD, but merge complete sections
- **Reason**: Therapeutic content should be comprehensive
- **Check**: Ensure no duplicate sections after merge

### Python Files (.py)
- **Strategy**: Prefer HEAD (newer implementation)
- **Reason**: Code logic usually improves over time
- **Important**: Verify imports and function signatures match

### Style Files (.sty)
- **Strategy**: Prefer HEAD (newer styles)
- **Reason**: Design system should be consistent
- **Check**: Ensure macro names don't conflict

## Automated Resolution

For bulk conflict resolution, use the pattern from this resolution:

```python
def resolve_conflict_smart(head_content, merge_content, file_path):
    """Intelligently resolve conflict based on content."""
    
    # Case 1: Empty content
    if not head_content.strip():
        return merge_content
    if not merge_content.strip():
        return head_content
    
    # Case 2: Identical
    if head_content.strip() == merge_content.strip():
        return head_content
    
    # Case 3: Subset detection
    if head_content.strip() in merge_content:
        return merge_content
    if merge_content.strip() in head_content:
        return head_content
    
    # Case 4: File type specific
    if file_path.endswith('.md'):
        return head_content  # Prefer newer docs
    
    if file_path.endswith('.tex'):
        # Check if both have complete sections
        if '\\section' in head_content and '\\section' in merge_content:
            return head_content + '\n\n' + merge_content
        return head_content
    
    # Default: prefer HEAD
    return head_content
```

## Validation After Resolution

### 1. Check for remaining conflicts
```bash
grep -r "<<<<<<< HEAD" . --include="*.tex" --include="*.md" --include="*.py" --include="*.sty"
# Should return nothing
```

### 2. Test build system
```bash
python3 ctmm_build.py
# Should pass all checks
```

### 3. Verify file integrity
```bash
# Check LaTeX files
for f in modules/*.tex; do 
  python3 -c "open('$f').read()" && echo "✓ $f" || echo "✗ $f"
done
```

### 4. Run git status
```bash
git status
# Should show modified files, no untracked artifacts
```

## Common Pitfalls

### ❌ Don't:
1. **Delete conflict markers without reading**: Always understand what's being merged
2. **Keep both versions blindly**: Can cause duplicate content or logic errors
3. **Ignore context**: Look at surrounding code to make informed decisions
4. **Skip validation**: Always test after resolving

### ✅ Do:
1. **Read both versions carefully**: Understand the intent of each change
2. **Test incrementally**: Resolve a few files, test, continue
3. **Preserve working code**: When in doubt, keep the version that works
4. **Document decisions**: Note why you chose one version over another

## Prevention

To avoid merge conflicts:

1. **Pull frequently**: Keep your branch up to date
2. **Small commits**: Easier to merge than large changes
3. **Communicate**: Coordinate when working on same files
4. **Branch strategy**: Use feature branches, merge to main regularly

## Emergency Recovery

If resolution goes wrong:

```bash
# Discard all changes and start over
git reset --hard HEAD

# Or restore specific file
git checkout HEAD -- path/to/file.tex
```

## Reference

- See `MERGE_CONFLICT_RESOLUTION_COMPLETE.md` for detailed resolution example
- Git documentation: https://git-scm.com/docs/git-merge#_how_conflicts_are_presented
- CTMM build system: Run `python3 ctmm_build.py --help`

---

**Last Updated**: 2026-01-10  
**Validated Against**: CTMM LaTeX Therapeutic Materials System v1.0
