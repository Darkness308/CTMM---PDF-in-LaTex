# CI/CD Troubleshooting Guide for CTMM LaTeX System

## Overview

This guide provides comprehensive information for troubleshooting CI/CD build failures in the CTMM LaTeX therapy materials system. The system includes enhanced error detection, analysis tools, and systematic debugging approaches.

## Quick Start for CI Issues

### 1. Run Comprehensive Analysis
```bash
# Local testing
make ci-analysis

# Or directly
python3 ci_build_analyzer.py
```

### 2. Check Build System Status
```bash
# Basic build system check
make check

# Detailed module analysis
make analyze

# Run all tests
make test
```

### 3. Review CI Artifacts
- Download `ci_analysis_report.json` from GitHub Actions artifacts
- Check `build_*_latest.log` files for detailed error information
- Review workflow logs for error patterns

## Common CI Build Issues

### 1. LaTeX Package Missing Errors

**Symptoms:**
```
! LaTeX Error: File `package.sty' not found
Package foo Error: Unknown option 'bar'
```

**Solution:**
1. Check if the package is listed in the workflow `extra_system_packages`
2. Verify package name mapping (e.g., `collection-fontsrecommended` → `texlive-fonts-recommended`)
3. Add missing packages to the appropriate workflow file

**Required Packages for CTMM:**
```yaml
extra_system_packages: |
  texlive-lang-german
  texlive-fonts-recommended
  texlive-latex-recommended
  texlive-fonts-extra
  texlive-latex-extra
  texlive-science
```

### 2. File Not Found Errors

**Symptoms:**
```
! LaTeX Error: File `modules/module-name.tex' not found
! I can't find file `style/package.sty'
```

**Solution:**
1. Run `python3 ctmm_build.py` to auto-generate missing templates
2. Check that `\input{}` and `\usepackage{}` paths are correct
3. Verify file names match exactly (case-sensitive)

### 3. LaTeX Syntax Errors

**Symptoms:**
```
! Undefined control sequence
! Missing $ inserted
! Extra }, or forgotten {
```

**Solution:**
1. Run `python3 validate_latex_syntax.py` for syntax checking
2. Use the CI build analyzer to get detailed error analysis
3. Check the specific line mentioned in the error

### 4. Over-escaped Document Issues

**Symptoms:**
```
\\textbackslash{}section\\textbackslash{}{Title}
```

**Solution:**
1. Use the de-escaping tool: `python3 fix_latex_escaping.py converted/`
2. Review the conversion workflow documentation
3. Configure document conversion tools properly

## Enhanced Error Analysis

### Build System Features

The enhanced build system provides:

1. **CI Environment Detection**: Automatically detects GitHub Actions, Jenkins, etc.
2. **LaTeX Availability Checking**: Gracefully handles missing LaTeX installations
3. **Comprehensive Error Analysis**: Parses LaTeX logs for meaningful error information
4. **Artifact Generation**: Saves detailed logs for debugging

### Error Analysis Tools

#### `ctmm_build.py` - Enhanced Build System
- Detects CI environment automatically
- Provides detailed error analysis
- Saves build artifacts for debugging
- Handles missing LaTeX gracefully

#### `ci_build_analyzer.py` - Comprehensive CI Analysis
- Python dependency verification
- LaTeX package availability checking
- Build system testing
- File integrity verification
- JSON report generation

#### `validate_latex_syntax.py` - Syntax Validation
- Basic LaTeX syntax checking
- File existence verification
- Reference validation

## Debugging Workflow

### Step 1: Initial Analysis
```bash
# Run comprehensive analysis
python3 ci_build_analyzer.py

# Check the generated report
cat ci_analysis_report.json
```

### Step 2: Identify the Issue Type
- **Environment Issues**: LaTeX not available, packages missing
- **Syntax Issues**: LaTeX compilation errors
- **File Issues**: Missing modules or style files
- **Configuration Issues**: Workflow setup problems

### Step 3: Apply Specific Fixes

#### For Environment Issues:
1. Check the CI workflow configuration
2. Verify LaTeX package dependencies
3. Update `extra_system_packages` if needed

#### For Syntax Issues:
1. Run local validation: `python3 validate_latex_syntax.py`
2. Check specific error lines in the LaTeX log
3. Fix syntax errors in the problematic files

#### For File Issues:
1. Run `python3 ctmm_build.py` to generate missing templates
2. Verify file paths and names
3. Check `\input{}` and `\usepackage{}` statements

### Step 4: Verify the Fix
```bash
# Test locally
make test

# Full analysis
make ci-analysis

# Check specific build
make check
```

## CI Workflow Integration

### GitHub Actions Integration

The workflows automatically run:
1. LaTeX syntax validation
2. CTMM build system check
3. Comprehensive CI analysis
4. Artifact collection on failure

### Artifact Collection

On build failures, the following artifacts are collected:
- `ci_analysis_report.json` - Comprehensive analysis results
- `build_*_latest.log` - Build logs with error details
- `*.log` files - LaTeX compilation logs

### Environment Variables

The system automatically detects CI environments using:
- `GITHUB_ACTIONS`
- `CI`
- `CONTINUOUS_INTEGRATION`
- And other common CI indicators

## Best Practices

### 1. Local Testing First
Always test changes locally before pushing:
```bash
make check
make test
make ci-analysis
```

### 2. Incremental Changes
Make small, focused changes to avoid introducing multiple issues simultaneously.

### 3. Validate Syntax
Use the validation tools before committing:
```bash
python3 validate_latex_syntax.py
```

### 4. Monitor CI Artifacts
Always download and review CI analysis reports when builds fail.

### 5. Keep Documentation Updated
Update this guide when new CI issues are discovered and resolved.

## Getting Help

### Error Reporting
When reporting CI issues, include:
1. The complete error log
2. The `ci_analysis_report.json` file
3. The specific commit or PR that triggered the failure
4. Any recent changes to LaTeX files or workflows

### Useful Commands
```bash
# Complete diagnostic run
make ci-analysis

# Clean start
make clean && make check

# Generate missing files
python3 ctmm_build.py

# Fix over-escaped documents
python3 fix_latex_escaping.py --backup converted/
```

## Version History

- **v1.0** - Initial CI troubleshooting documentation
- **v1.1** - Added comprehensive CI build analyzer
- **v1.2** - Enhanced error detection and artifact collection
- **v1.3** - Integrated de-escaping tools and validation

---

This guide is part of the CTMM LaTeX therapy materials system and is regularly updated based on discovered CI issues and their solutions.