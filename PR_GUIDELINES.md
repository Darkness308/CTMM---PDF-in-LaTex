# Pull Request Guidelines for CTMM

## Overview

This document provides guidelines for creating pull requests that can be properly reviewed by GitHub Copilot and maintain the quality of the CTMM therapeutic materials system.

## The "Empty PR" Problem

GitHub Copilot cannot review pull requests that have no file changes. This can happen when:

- Changes are not properly committed to git
- Changes are not pushed to the remote branch  
- Only whitespace or invisible changes are made
- Git configuration issues prevent proper change tracking

## Pre-PR Validation

Before creating a pull request, **always run our validation tools**:

### Quick Validation
```bash
make validate-pr
```

### Full Pre-commit Check
```bash
make pre-commit
```

### Manual Validation
```bash
python3 validate_pr_readiness.py
```

## Creating a Valid Pull Request

### 1. Make Meaningful Changes
Ensure your changes include actual content modifications:
- ✅ Adding new therapeutic content
- ✅ Fixing LaTeX syntax errors
- ✅ Updating build system functionality
- ✅ Improving documentation
- ❌ Only changing whitespace
- ❌ Empty commits without content

### 2. Proper Git Workflow
```bash
# 1. Make your changes
vim modules/new-therapy-module.tex

# 2. Check status
git status

# 3. Add changes
git add .

# 4. Commit with descriptive message
git commit -m "Add new anxiety management module"

# 5. Validate before pushing
make validate-pr

# 6. Push to remote
git push origin your-branch-name

# 7. Create PR on GitHub
```

### 3. Commit Message Guidelines
Use clear, descriptive commit messages:
- ✅ "Add ADHD coping strategies worksheet"
- ✅ "Fix LaTeX compilation error in trigger management"
- ✅ "Update build system to handle German characters"
- ❌ "Fix"
- ❌ "Update"
- ❌ "WIP"

## Troubleshooting Empty PRs

If Copilot reports "wasn't able to review any files":

### Check 1: Verify Changes Exist
```bash
git diff origin/main..HEAD --name-only
```
Should show modified files. If empty, you have no changes.

### Check 2: Check Commit History
```bash
git log --oneline origin/main..HEAD
```
Should show your commits. If empty, commits weren't made.

### Check 3: Verify Push Status
```bash
git status
```
Should show "Your branch is up to date" or "ahead by X commits".

### Check 4: Run Validation
```bash
make validate-pr
```
Will identify specific issues with your PR.

## Common Fixes

### Problem: "No files changed"
**Solution:** Ensure changes are committed and pushed
```bash
git add .
git commit -m "Describe your changes"
git push origin your-branch
```

### Problem: "No line changes detected"
**Solution:** Verify files have actual content changes
```bash
git diff HEAD~1 --stat  # Check what changed in last commit
```

### Problem: "Unable to compare with origin/main"
**Solution:** Fetch latest changes
```bash
git fetch origin
make validate-pr
```

## Best Practices

### For LaTeX Content
- Test compilation with `make check` before committing
- Ensure German characters are properly encoded
- Follow CTMM style guidelines from `style/` directory

### For Python Scripts
- Run unit tests: `make test-unit`
- Follow existing code style
- Add tests for new functionality

### For Documentation
- Update relevant README sections
- Include usage examples for new features
- Keep therapeutic content culturally appropriate

## Repository Structure

### Always Reviewable Files
- `modules/*.tex` - Therapeutic content modules
- `style/*.sty` - LaTeX style definitions
- `*.py` - Build system scripts
- `*.md` - Documentation
- `.github/workflows/*.yml` - CI/CD configuration

### Usually Not Reviewable
- `*.pdf` - Generated outputs (ignored by .gitignore)
- `*.aux`, `*.log` - LaTeX artifacts (ignored by .gitignore)
- `__pycache__/` - Python cache (ignored by .gitignore)

## Automated Validation

The repository includes automated validation:

### GitHub Actions
- **PR Validation** - Automatically checks new PRs for meaningful changes
- **LaTeX Build** - Ensures changes don't break PDF generation
- **Syntax Validation** - Checks LaTeX and Python syntax

### Local Tools
- `validate_pr_readiness.py` - Pre-PR validation script
- `test_ctmm_build.py` - Unit tests for build system
- `ctmm_build.py` - Main build system with validation

## Getting Help

If you're still having issues with PR validation:

1. **Check GitHub Actions** - Look at failed workflow runs for specific errors
2. **Run local validation** - Use `make validate-pr` for immediate feedback
3. **Review change history** - Use `git log --stat` to see what changed
4. **Create an issue** - Describe the problem and include validation output

## Examples

### ✅ Good PR Example
```
Files changed: 3
- modules/anxiety-worksheet.tex (new file)
- style/ctmm-design.sty (updated colors)
- README.md (added usage example)

Lines: +127 -3
Result: Copilot can review successfully
```

### ❌ Bad PR Example
```
Files changed: 0
Lines: +0 -0
Result: Copilot cannot review - no changes detected
```

---

**Remember:** The goal is creating meaningful changes that improve the CTMM therapeutic materials system while ensuring they can be properly reviewed and validated.