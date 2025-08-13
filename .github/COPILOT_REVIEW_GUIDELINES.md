# Copilot Review Guidelines for CTMM Project

## Overview
This document provides guidelines to ensure GitHub Copilot can effectively review pull requests in the CTMM LaTeX project.

## File Naming Conventions
- **Use underscores or hyphens instead of spaces** in filenames
- **Avoid special characters** that might cause parsing issues
- **Keep filenames descriptive but concise**

### ✅ Good Examples:
- `tool_23_trigger_management.tex`
- `matching-matrix-intervention.tex`
- `arbeitsblatt-depression.tex`

### ❌ Avoid:
- `Tool 23 Trigger Management.tex` (spaces)
- `file#with$special@chars.tex` (special characters)
- `very_very_very_long_filename_that_exceeds_reasonable_limits.tex`

## File Size Guidelines
- **Text files**: No practical limit for LaTeX, Python, Markdown files
- **Binary files**: Exclude large PDFs (>100KB) from git tracking
- **Generated files**: Use .gitignore to exclude build artifacts

## Content Guidelines
- **Encoding**: Use UTF-8 encoding for all text files
- **Line endings**: Use Unix line endings (LF) for consistency
- **German content**: Ensure proper UTF-8 encoding for umlauts and special characters

## Pull Request Best Practices
- **Include actual changes**: Ensure PRs contain file modifications
- **Focus changes**: Keep PRs focused on specific features or fixes
- **Test before submission**: Run `python3 ctmm_build.py` to verify builds
- **Clean working directory**: Remove temporary files before committing

## Troubleshooting Copilot Review Issues

### If Copilot cannot review files:
1. **Check file changes**: Ensure the PR actually modifies files
2. **Verify file names**: Rename files with spaces or special characters
3. **Check file sizes**: Large binary files may block reviews
4. **Validate encoding**: Ensure files use UTF-8 encoding
5. **Test locally**: Verify files can be opened and read properly

### Common Issues:
- **Empty PRs**: PRs with 0 additions/deletions have no files to review
- **Binary files**: Large PDFs, images may prevent review
- **Encoding issues**: Non-UTF-8 files may cause parsing problems
- **File path issues**: Spaces in paths can cause problems

## Repository Optimization
- Large binary files are excluded via `.gitignore`
- Build artifacts are automatically excluded
- Generated PDFs are not tracked in git to reduce repository size

For questions or issues with Copilot reviews, check these guidelines first or create an issue with the `copilot-review` label.