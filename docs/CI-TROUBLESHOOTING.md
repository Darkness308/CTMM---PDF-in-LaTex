# CI Troubleshooting Guide

This document provides solutions for common CI/CD issues in the CTMM LaTeX repository.

## Issue: Git Checkout Failures Due to Uncommitted Files

**Problem:** CI workflows fail with errors like:
```
error: Your local changes to the following files would be overwritten by checkout:
    converted/file1.tex
    converted/file2.tex
    ...
Please commit your changes or stash them before you switch branches.
```

### Root Cause
This occurs when:
1. Scripts or tools generate files during CI runs
2. Generated files are not properly ignored by git
3. Subsequent git operations (checkout, merge, etc.) conflict with uncommitted changes

### Solutions Applied

#### 1. Updated `.gitignore`
Added proper exclusions for generated directories:
```gitignore
## Conversion and processing directories:
converted/
converted_files/
processed/
```

#### 2. Enhanced CI Workflow
Modified `.github/workflows/latex-build.yml` to include:
- Clean checkout with `clean: true`
- Workspace cleanup before operations
- Removal of potentially conflicting directories

#### 3. Cleanup Script
Created `scripts/cleanup-workspace.sh` for manual workspace management:
```bash
# Standard cleanup
./scripts/cleanup-workspace.sh

# Deep clean (removes all git-ignored files)
./scripts/cleanup-workspace.sh --deep
```

### Prevention Best Practices

#### For Developers
1. **Before committing:** Run the cleanup script to ensure no temporary files are included
2. **After pulling:** Clean workspace if experiencing git conflicts
3. **When adding new tools:** Ensure generated files are properly ignored

#### For CI/CD
1. **Always use clean checkout** in workflows
2. **Clean workspace** before critical git operations
3. **Upload only intentional artifacts** (not temporary files)

#### For Scripts and Tools
1. **Generate files in ignored directories** (e.g., `converted/`, `build/`, `tmp/`)
2. **Clean up after processing** when possible
3. **Document which files are generated** in comments or README

### Example Workflow Configuration
```yaml
steps:
  - name: Checkout repository
    uses: actions/checkout@v4
    with:
      clean: true

  - name: Clean workspace
    run: |
      rm -rf converted/ converted_files/ processed/ || true
      git clean -fdx || true

  # ... rest of workflow
```

### Related Issues
- Issue #241: Fixed LaTeX over-escaping in converted files
- Issue #249: CI insights reporting this checkout failure
- PR #242: Successful resolution of the original problem

### Historical Context
The original issue occurred during an attempt to fix LaTeX over-escaping problems. The fixing process generated many `.tex` files in a `converted/` directory, which weren't properly handled by git, leading to checkout conflicts. The core problem was successfully resolved in PR #242, but this CI robustness improvement prevents similar issues in the future.