# Copilot Review Guide for CTMM-System

This guide helps ensure that your pull requests can be properly reviewed by GitHub Copilot.

## Why Copilot Couldn't Review Files

The most common reasons Copilot cannot review files in a PR:

### 1. No File Changes
- **Issue**: PR shows "0 additions, 0 deletions, 0 changed files"
- **Solution**: Ensure your branch contains actual commits with file changes
- **Check**: Run `git diff main...your-branch` to verify changes exist

### 2. Invalid File Types or Formats
- **Issue**: Files contain binary data, corrupted content, or unsupported formats
- **Solution**: Only commit text-based files (`.tex`, `.py`, `.md`, `.yml`, etc.)
- **Avoid**: Temporary files, editor artifacts, or system files

### 3. Workflow or CI Failures
- **Issue**: GitHub Actions workflow syntax errors prevent proper CI execution
- **Solution**: Validate YAML syntax in `.github/workflows/` files
- **Test**: Check workflow runs in GitHub Actions tab

## Best Practices for Reviewable PRs

### ✅ Do This
```bash
# 1. Make actual changes to files
echo "% Updated LaTeX module" >> modules/my-module.tex

# 2. Commit your changes
git add modules/my-module.tex
git commit -m "Add therapeutic content to my-module"

# 3. Push to your branch
git push origin feature/my-changes

# 4. Verify changes exist
git diff main...feature/my-changes --stat
```

### ❌ Avoid This
```bash
# Don't create empty commits
git commit --allow-empty -m "Empty commit"

# Don't commit temporary/system files
git add modules/Untitled*
git add modules/*.tmp
git add .DS_Store

# Don't commit without actual file changes
git commit -m "Fixed issue" # (but no files were actually changed)
```

## File Structure Guidelines

### Repository Structure
```
├── modules/           # Only .tex files with actual content
├── style/            # Only .sty LaTeX style files  
├── .github/          # Workflow and documentation files
└── docs/             # Additional documentation
```

### Prohibited Files in modules/
- `Untitled*` (editor temp files)
- `*.tmp`, `*.temp` (temporary files)
- `*.md` files (should be in docs/ or root)
- Empty or test files
- Files with special characters in names

## Troubleshooting Checklist

Before creating a PR, verify:

- [ ] **Files exist**: `git status` shows modified/new files
- [ ] **Changes are committed**: `git log --oneline -5` shows your commits
- [ ] **Diff is not empty**: `git diff main...HEAD --stat` shows file changes
- [ ] **Workflow is valid**: `.github/workflows/*.yml` files are syntactically correct
- [ ] **Build system works**: `python3 ctmm_build.py` completes successfully
- [ ] **No prohibited files**: Check against `.gitignore` patterns

## Testing Your Changes

### Local Testing
```bash
# Test the build system
python3 ctmm_build.py

# Check for syntax errors in workflows
yamllint .github/workflows/

# Verify LaTeX structure (if pdflatex available)
make check
```

### Pre-PR Verification
```bash
# Ensure your branch has changes compared to main
git diff main...HEAD --name-only

# Expected output: list of changed files
# If empty, Copilot cannot review
```

## Common Solutions

### Problem: "0 changed files" in PR
```bash
# Check if you're on the right branch
git branch

# Check if changes were committed
git log --oneline main..HEAD

# If no commits exist, make your changes and commit them
git add .
git commit -m "Descriptive commit message"
git push
```

### Problem: Workflow failures
```bash
# Check workflow syntax
cat .github/workflows/latex-build.yml

# Look for common YAML issues:
# - Incorrect indentation  
# - Extra dashes (- uses: vs uses:)
# - Missing quotes around special characters
```

### Problem: Binary or corrupted files
```bash
# Check file types
file modules/*

# Remove problematic files
git rm modules/problematic-file
git commit -m "Remove problematic file"
```

## Support

If you're still having issues with Copilot reviews:

1. **Check the PR diff**: Does it show actual file changes?
2. **Verify workflow status**: Are GitHub Actions passing?
3. **Review file types**: Are you committing only text-based files?
4. **Test locally**: Does `python3 ctmm_build.py` work?

For more help, refer to the main [Copilot Instructions](copilot-instructions.md) or create an issue with:
- Link to your PR
- Output of `git diff main...your-branch --stat`
- Any error messages from workflows