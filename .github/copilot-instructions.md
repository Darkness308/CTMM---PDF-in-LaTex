# GitHub Copilot Instructions for CTMM LaTeX Therapeutic Materials System

**DIRECTIVE: Always follow these instructions first. Only search for additional context if the information here is incomplete or found to be in error.**

## Project Overview

This repository contains a **LaTeX-based therapeutic materials system** called **CTMM** (Catch-Track-Map-Match) designed for creating professional therapy documents, particularly for neurodiverse couples dealing with mental health challenges including:

- Depression and mood disorders
- Trigger management 
- Borderline Personality Disorder (BPD)
- ADHD, Autism Spectrum Disorder (ASD)
- Complex PTSD (CPTSD)
- Relationship dynamics and binding patterns

**Language**: Primary content is in German (Deutsch)

## Essential Setup & Dependencies

### Required Dependencies - Install First
```bash
# Python dependencies (always required)
pip install chardet pyyaml

# LaTeX dependencies (required for PDF generation)
# Ubuntu/Debian:
sudo apt-get update
sudo apt-get install -y texlive-lang-german texlive-fonts-extra texlive-latex-extra texlive-latex-base texlive-fonts-recommended

# OR complete installation (recommended):
sudo apt-get install -y texlive-full
```

**Installation Timing**: LaTeX package installation takes approximately **4-5 minutes**. NEVER CANCEL - set timeout to 10+ minutes.

### Quick Start Commands
```bash
# 1. Primary build system check (ALWAYS run first)
python3 ctmm_build.py
# Takes ~1.9 seconds with LaTeX, ~0.055 seconds without
# NEVER CANCEL - set timeout to 5 minutes

# 2. Run comprehensive unit tests
make unit-test
# Takes ~0.2 seconds, 77 total tests
# Timeout: 2 minutes

# 3. Validate PR content (before creating PRs)
make validate-pr
# Takes ~0.1 seconds
# Timeout: 2 minutes

# 4. Build PDF (when LaTeX is working)
make build
# Currently fails due to form element syntax errors
# When working: ~1-2 seconds compilation
# Timeout: 5 minutes
```

## Core Build System - ctmm_build.py

The primary build system performs comprehensive validation and testing:

### What it does:
1. **LaTeX Validation** - Checks for over-escaping issues and syntax problems
2. **Reference Scanning** - Scans `main.tex` for all `\usepackage{style/...}` and `\input{modules/...}` references
3. **File Existence Check** - Ensures all referenced files exist
4. **Template Generation** - Auto-generates missing template files with proper structure
5. **Incremental Testing** - Tests basic build (without modules) and full build separately
6. **Comprehensive Reporting** - Creates detailed build reports and TODO files

### Build System Commands:
```bash
# Primary command - ALWAYS run this first
python3 ctmm_build.py
# Expected time: 1.9 seconds with LaTeX installed
# NEVER CANCEL - timeout: 5 minutes

# Enhanced build management
python3 ctmm_build.py --enhanced
make enhanced-build

# Detailed analysis with verbose output
python3 build_system.py --verbose
```

**CRITICAL**: The build system works even without LaTeX installed - it validates structure and generates templates.

## Testing & Validation

### Unit Tests - Run Frequently
```bash
# Comprehensive unit tests (77 tests total)
make unit-test
# OR:
python3 test_ctmm_build.py  # 56 build system tests
python3 test_latex_validator.py  # 21 validator tests

# Expected time: 0.2 seconds
# NEVER CANCEL - timeout: 3 minutes
```

**Test Coverage**:
- `filename_to_title()` function (29 test cases)
- Build system core functions (27+ test cases)  
- LaTeX validator functions (21 test cases)

### LaTeX Validation & Escaping Issues
```bash
# Validate LaTeX files for escaping problems
make validate
python3 latex_validator.py modules/

# Fix escaping issues (creates backups)
make validate-fix
python3 latex_validator.py modules/ --fix
```

### PR Validation - CRITICAL for Copilot Review
```bash
# ALWAYS run before creating PRs
make validate-pr
python3 validate_pr.py

# Expected time: 0.1 seconds
# NEVER CANCEL - timeout: 2 minutes
```

**PR Requirements for Copilot Review**:
- At least 1 file with meaningful changes
- Substantive content changes (not just whitespace)  
- Successful CTMM build system validation
- Use provided PR template

## LaTeX Architecture & Build Process

### Repository Structure
```
├── main.tex                    # Main LaTeX document (entry point)
├── style/                      # LaTeX style files (.sty)
│   ├── ctmm-design.sty        # CTMM color scheme and design elements
│   ├── ctmm-form-elements.sty # Interactive form components  
│   └── ctmm-navigation.sty    # Navigation system
├── modules/                    # Individual therapy modules (.tex)
│   ├── arbeitsblatt-*.tex     # Worksheets (Arbeitsblätter)
│   ├── trigger*.tex           # Trigger management modules
│   ├── depression.tex         # Depression-related content
│   └── ...                    # Other therapeutic modules
```

### LaTeX Best Practices - CRITICAL Rules
- **Package Loading**: ALL `\usepackage{...}` commands MUST be in `main.tex` preamble ONLY
- **NEVER** load packages in modules or after `\begin{document}`
- **Form Elements**: Use ONLY CTMM form elements:
  ```latex
  \ctmmCheckBox[field_name]{Label}     # Interactive checkbox
  \ctmmTextField[width]{label}{name}   # Text input field
  \ctmmTextArea[width]{lines}{label}{name}  # Multi-line text area
  ```
- **NEVER** use `\Box`, `\blacksquare`, or basic LaTeX form elements directly

### Current LaTeX Compilation Issue
**Known Problem**: LaTeX compilation currently fails due to malformed `\ctmmTextField` commands with incorrectly escaped underscores.

**Error Pattern**:
```
! Missing } inserted.
l.21 ...tmmTextField[4cm]{}{therapist_psycho\_mm &
```

**Do NOT attempt to fix this during normal development** - focus on build system validation and module development.

## GitHub Actions & CI/CD

### Workflows with Timing
1. **`latex-build.yml`** - Main PDF build workflow
   - LaTeX package installation: 15 minutes timeout
   - Build validation steps: 5-10 minutes timeout each
   - Total workflow: ~20-30 minutes when working

2. **`latex-validation.yml`** - Syntax and structure validation
   - Faster validation-only workflow
   - 10-15 minutes total

**CRITICAL TIMEOUTS**:
- LaTeX package installation: NEVER CANCEL - takes 4-5 minutes, set 15+ minute timeout
- Build system validation: NEVER CANCEL - set 10+ minute timeout
- Unit tests: NEVER CANCEL - set 5+ minute timeout

### CI Failure Prevention
The repository has comprehensive CI failure prevention:
```bash
# Test CI robustness (for CI pipeline issues)
python3 test_issue_1044_ci_robustness.py
python3 test_comprehensive_ci_timeout_coverage.py
```

## Development Workflow

### Adding New Modules
1. **Reference in main.tex**:
   ```latex
   \input{modules/my-new-module}
   ```

2. **Run build system** (auto-generates templates):
   ```bash
   python3 ctmm_build.py
   ```

3. **Files created automatically**:
   - `modules/my-new-module.tex` - Template with basic structure
   - `modules/TODO_my-new-module.md` - Task list for completion

4. **Complete module content** and remove TODO file when finished

### Development Best Practices
- Always run `python3 ctmm_build.py` after making changes
- Use `make validate` to check for LaTeX escaping issues
- Run `make unit-test` frequently during development
- Use `make validate-pr` before creating pull requests

## Validation Scenarios - Test These After Changes

### 1. Build System Validation
```bash
# Primary validation - ALWAYS works
python3 ctmm_build.py
# Expected: All checks pass, files exist or templates created
```

### 2. Unit Test Validation  
```bash
# Comprehensive test suite
make unit-test
# Expected: All 77 tests pass
```

### 3. LaTeX Structure Validation
```bash
# Validate LaTeX syntax and escaping
make validate
# Expected: No escaping issues found
```

### 4. Form Element Testing (Manual)
When LaTeX compilation is working:
- Test interactive PDF forms in generated PDF
- Verify checkboxes, text fields, and text areas function
- Check form field naming and accessibility

### 5. Module Integration Testing
```bash
# Test individual modules by temporarily commenting others in main.tex
# Uncomment one module at a time to isolate issues
```

## Troubleshooting Common Issues

### Build Errors
- `Undefined control sequence` → Check if macro is defined in `main.tex` preamble
- `Can be used only in preamble` → Move `\usepackage` to `main.tex` preamble  
- Missing file errors → Run `python3 ctmm_build.py` to auto-generate templates
- Form element errors → Check `\ctmmTextField` syntax and escaping

### LaTeX Package Issues
```bash
# FontAwesome missing
sudo apt-get install texlive-fonts-extra

# German language support missing  
sudo apt-get install texlive-lang-german

# Complete package installation
sudo apt-get install texlive-full
```

### CI/CD Issues
- Check GitHub Actions logs for timeout issues
- Verify all timeouts are set to appropriate values (10+ minutes)
- Use comprehensive validation scripts to identify pipeline problems

## Quick Reference

### Most Important Commands
```bash
# 1. ALWAYS start here - primary build validation
python3 ctmm_build.py                    # 1.9s, timeout: 5min

# 2. Test changes thoroughly  
make unit-test                          # 0.2s, timeout: 3min

# 3. Validate before PR
make validate-pr                        # 0.1s, timeout: 2min

# 4. Fix LaTeX issues
make validate                           # Check escaping
make validate-fix                       # Fix with backups
```

### Key Files to Know
- `main.tex` - Document entry point and ALL package definitions
- `ctmm_build.py` - Primary build system and validation
- `Makefile` - Common build commands and shortcuts
- `.github/workflows/` - CI/CD pipelines with proper timeouts

### Timing Expectations - NEVER CANCEL
- **Build system check**: 1.9 seconds  
- **Unit tests**: 0.2 seconds
- **LaTeX package installation**: 4-5 minutes
- **PR validation**: 0.1 seconds
- **LaTeX compilation**: 1-2 seconds (when working)

**Remember**: This is specialized therapeutic content requiring both LaTeX expertise and sensitivity to mental health contexts. Always test thoroughly and validate changes comprehensively before committing.