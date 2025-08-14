# GitHub Copilot Review Guidelines for CTMM Project

## Overview

This guide ensures that pull requests in the CTMM repository are optimized for GitHub Copilot code review. Following these guidelines will help Copilot provide meaningful feedback on your changes.

## Core Requirements for Copilot-Reviewable PRs

### 1. **Must Contain Actual File Changes**
- PRs with 0 additions, 0 deletions, and 0 changed files cannot be reviewed by Copilot
- Ensure your PR includes meaningful code, documentation, or configuration changes
- Verify changes are properly staged and committed before creating the PR

### 2. **File Naming Conventions**
- **Use underscores instead of spaces**: `Tool_22_Safewords.tex` ✅ not `Tool 22 Safewords.tex` ❌
- **Avoid special characters**: Use only letters, numbers, underscores, hyphens, and dots
- **Be consistent**: Follow existing naming patterns in the repository

#### Examples:
```
✅ Good filenames:
- Tool_22_Safewords_Signalsysteme_CTMM.tex
- Code_Citations.md
- arbeitsblatt-trigger.tex
- depression-management.tex

❌ Problematic filenames:
- Tool 22 Safewords Signalsysteme CTMM.tex (spaces)
- # Code Citations.md (special character)
- file with%symbols.tex (special characters)
```

### 3. **File Type Guidelines**

#### ✅ Copilot-Friendly File Types:
- **LaTeX source**: `.tex`, `.sty` files
- **Python scripts**: `.py` files  
- **Documentation**: `.md` files
- **Configuration**: `.json`, `.yaml`, `.toml` files
- **Build scripts**: `Makefile`, shell scripts

#### ❌ Files That Block Copilot Review:
- **Binary files**: PDFs, Word documents, images
- **Generated files**: Compiled outputs, build artifacts
- **Large files**: Files over 1MB typically cause issues
- **Files with encoding problems**: Non-UTF-8 encoded files

### 4. **Repository Structure Best Practices**

#### Keep Source Files Separate from Generated Content:
```
✅ Recommended structure:
├── modules/           # LaTeX source modules
├── style/            # LaTeX style files  
├── .github/          # GitHub configuration
├── main.tex          # Main document source
└── README.md         # Documentation

❌ Avoid in main repository:
├── main.pdf          # Generated PDF (use .gitignore)
├── build/            # Build artifacts
└── *.docx           # Binary documents
```

## Pre-PR Checklist

Before creating a pull request, verify:

- [ ] **Files changed**: Run `git status` to confirm files are modified
- [ ] **No spaces in filenames**: Check `find . -name "* *"` returns no results
- [ ] **UTF-8 encoding**: Ensure all text files use UTF-8 encoding
- [ ] **No large files**: Check `find . -size +1M` for files over 1MB
- [ ] **Build system works**: Run `python3 ctmm_build.py` successfully
- [ ] **Tests pass**: Run `python3 test_ctmm_build.py` without errors

## Automated Validation

Use the compatibility checker before creating PRs:

```bash
# Run the automated compatibility check
python3 check_copilot_compatibility.py

# Fix any issues reported before creating the PR
```

## Common Issues and Solutions

### Issue: "Copilot wasn't able to review any files in this pull request"

**Causes:**
1. PR contains only binary files
2. All files have problematic names or encoding
3. PR has no actual file changes (empty commit)
4. Files are too large for review

**Solutions:**
1. Exclude binary files from git tracking (add to `.gitignore`)
2. Rename files to follow naming conventions
3. Ensure PR includes actual code/text changes
4. Split large files or exclude them from the PR

### Issue: Files with spaces or special characters

**Solution:**
```bash
# Rename files to use underscores
mv "Tool 22 Safewords.tex" "Tool_22_Safewords.tex"
mv "# Code Citations.md" "Code_Citations.md"
```

### Issue: Large binary files in repository

**Solution:**
```bash
# Remove from git tracking
git rm --cached large_file.pdf

# Add to .gitignore
echo "*.pdf" >> .gitignore
```

## CTMM-Specific Guidelines

### LaTeX Files
- Keep `.tex` files focused on content, not package declarations
- Use existing macros from style files
- Follow German therapeutic naming conventions
- Test compilation with `python3 ctmm_build.py`

### Python Scripts
- Follow PEP 8 style guidelines
- Include docstrings for functions and classes
- Add unit tests for new functionality
- Use type hints where appropriate

### Documentation
- Write in English for technical documentation
- Use German for therapeutic content descriptions
- Include usage examples
- Keep README files up to date

## Getting Help

If Copilot still cannot review your PR after following these guidelines:

1. **Check the compatibility script results**: `python3 check_copilot_compatibility.py`
2. **Review file sizes**: Large files may need to be excluded
3. **Verify encoding**: Ensure all files are UTF-8 encoded
4. **Ask for help**: Tag maintainers in the PR for assistance

## Validation Commands

```bash
# Quick compatibility check
python3 check_copilot_compatibility.py

# Full build system test  
python3 ctmm_build.py

# Run unit tests
python3 test_ctmm_build.py

# Check for files with spaces
find . -name "* *" -type f

# Check for large files
find . -size +1M -type f
```

Following these guidelines will ensure GitHub Copilot can effectively review your contributions to the CTMM project!