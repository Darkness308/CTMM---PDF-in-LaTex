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
│   ├── form-elements.sty      # Interactive form components
│   └── ctmm-diagrams.sty      # Custom diagrams and visual elements
├── modules/                    # Individual therapy modules (.tex)
│   ├── arbeitsblatt-*.tex     # Worksheets (Arbeitsblätter)
│   ├── trigger*.tex           # Trigger management modules
│   ├── depression.tex         # Depression-related content
│   ├── bindungsleitfaden.tex  # Relationship binding guide
│   ├── notfallkarten.tex      # Emergency intervention cards
│   ├── safewords.tex          # Safe word systems
│   └── ...                    # Other therapeutic modules
├── converted/                  # Converted documents (for de-escaping fixes)
├── therapie-material/          # Additional therapy resources and templates
├── ctmm_build.py              # Automated build system (primary)
├── build_system.py            # Detailed module analysis and testing
├── ctmm_unified_tool.py       # Unified tool interface
├── latex_validator.py         # LaTeX syntax and escaping validation
├── fix_latex_escaping.py      # Over-escaping repair utilities
├── validate_*.py              # Various validation scripts
├── test_*.py                  # Comprehensive test suites
├── Makefile                   # Build commands and shortcuts
└── .github/workflows/         # CI/CD for PDF generation and validation
```

## LaTeX Architecture & Conventions

### 🔧 Build System Usage

**Primary Build Command:**
```bash
python3 ctmm_build.py
```

**What the build system does:**
1. **LaTeX Validation**: Checks for over-escaping issues and syntax problems
2. **Reference Scanning**: Scans `main.tex` for all `\usepackage{style/...}` and `\input{modules/...}` references
3. **Template Generation**: Auto-generates missing template files with proper structure
4. **Incremental Testing**: Tests basic build (without modules) and full build separately
5. **Documentation**: Creates TODO files for new templates with completion guidelines
6. **Error Recovery**: Gracefully handles missing LaTeX installation for CI environments

**Build System Requirements:**
- **Python 3.x** (required) - Core build system functionality
- **LaTeX Distribution** (optional) - For PDF compilation (TeX Live, MiKTeX)
  - If LaTeX is not available, the system validates structure without compilation
  - GitHub Actions workflow includes full LaTeX environment setup
- **Required Python packages**: `chardet` for encoding detection

**Validation Capabilities:**
- **Over-escaping Detection**: Identifies and can fix excessive `\textbackslash{}` usage
- **Syntax Validation**: Checks LaTeX file structure and command usage
- **Module Dependencies**: Ensures all referenced files exist or creates templates
- **Form Element Validation**: Verifies proper use of CTMM form components

**Note**: Build tests will show FAIL if pdflatex is not installed, but dependency checking and file generation still work correctly.

**Alternative Commands:**
```bash
make check          # Run build system check
make build          # Build PDF with pdflatex
make analyze        # Detailed module testing
make unit-test      # Run Python unit tests
python3 build_system.py --verbose  # Granular analysis
```

**Unit Testing:**
The build system includes comprehensive unit tests for core functions:
```bash
python3 test_ctmm_build.py -v
```
Tests cover filename-to-title conversion (23 test cases), German therapy terminology, and build system integration (56 total tests).

### 📄 LaTeX Best Practices

#### Package Loading Rules
- **CRITICAL**: All `\usepackage{...}` commands MUST be in the preamble of `main.tex`
- **NEVER** load packages in modules or after `\begin{document}`
- Error: `Can be used only in preamble` → Move package to preamble

#### Custom Macros & Commands
- Define custom macros centrally in preamble or style files
- **Form Elements Convention**: Use CTMM form elements only:
  ```latex
  \ctmmCheckBox[field_name]{Label}     % Interactive checkbox
  \ctmmTextField[width]{label}{name}   % Text input field
  \ctmmTextArea[width]{lines}{label}{name}  % Multi-line text area
  \ctmmRadioButton{group}{value}{label}     % Radio button
  ```
- **NEVER** use `\Box`, `\blacksquare`, or basic LaTeX form elements directly

#### Module Development
- Modules should contain ONLY content, not package definitions
- Use existing macros and commands defined in preamble/style files
- Keep modules focused on single therapeutic concepts

### 🎨 CTMM Design System

**Color Scheme:**
- `ctmmBlue` (#003087) - Primary blue for headers and structure
- `ctmmOrange` (#FF6200) - Accent orange for highlights
- `ctmmGreen` (#4CAF50) - Green for positive elements and form borders
- `ctmmPurple` (#7B1FA2) - Purple for special sections
- `ctmmRed` (#D32F2F) - Red for warnings or important notes
- `ctmmGray` (#757575) - Gray for secondary text
- `ctmmYellow` (#FFC107) - Yellow for emphasis

**Custom Elements:**
- `\begin{ctmmBlueBox}{Title}` - Styled info boxes in CTMM blue
- `\begin{ctmmGreenBox}{Title}` - Green boxes for positive content
- `\ctmmCheckBox[field_name]{Label}` - Interactive checkboxes
- `\ctmmTextField[width]{label}{name}` - Text input fields
- `\ctmmTextArea[width]{lines}{label}{name}` - Multi-line text areas
- Navigation system with `\faCompass` icons
- Interactive PDF features with hyperref integration
- Form elements automatically adapt for print vs. digital use

## Development Workflow

### Adding New Modules

1. **Reference in main.tex:**
   ```latex
   \input{modules/my-new-module}
   ```

2. **Run build system** (auto-generates templates):
   ```bash
   python3 ctmm_build.py
   ```

3. **Auto-generated files:**
   - `modules/my-new-module.tex` - Template with basic structure
   - `modules/TODO_my-new-module.md` - Task list for completion

4. **Complete the module** and remove TODO file when finished

### Troubleshooting Common Issues

**Build Errors:**
- `Undefined control sequence` → Check if macro is defined in preamble
- `Command already defined` → Remove duplicate macro definitions
- Missing file errors → Run `ctmm_build.py` to auto-generate templates
- `Can be used only in preamble` → Move `\usepackage` to main.tex preamble
- `Package hyperref Error` → Ensure hyperref is loaded last in package list
- LaTeX compilation fails → Check for special characters in German text, use proper UTF-8 encoding

**Module Guidelines:**
- Use semantic section structure: `\section{Title}`, `\subsection{}`
- Include therapeutic instructions in German
- Add form elements for interactive use
- Test individual modules by temporarily commenting others

## Content Guidelines

### 🧠 Therapeutic Content

**Sensitive Material**: This repository contains mental health resources. When contributing:

- **Respect privacy**: No personal information in examples
- **Clinical accuracy**: Ensure therapeutic techniques are evidence-based
- **Cultural sensitivity**: Content is designed for German-speaking therapy contexts
- **Professional tone**: Maintain therapeutic, non-judgmental language

**Content Types:**
- **Arbeitsblätter** (Worksheets): Interactive forms for self-reflection
- **Trigger Management**: Coping strategies and identification tools
- **Psychoeducation**: Information about mental health conditions
- **Relationship Tools**: Communication and binding pattern resources

### 🇩🇪 German Language Context

- Use formal therapeutic German (Sie-Form for clients)
- Medical/psychological terminology should be accurate
- Include pronunciation guides for technical terms when helpful
- Maintain consistency in therapeutic vocabulary

## Technical Requirements

### LaTeX Dependencies
- **Required packages**: TikZ, hyperref, xcolor, fontawesome5, tcolorbox, tabularx, amssymb, geometry, pifont, ifthen, calc, forloop
- **Font encoding**: T1 with UTF-8 input
- **Language**: ngerman babel
- **PDF features**: Interactive forms, bookmarks, metadata

### Development Environment
- **Local**: LaTeX distribution (TeX Live, MiKTeX) with required packages
- **GitHub Codespace**: Pre-configured environment available
- **VS Code Integration**:
  - `.vscode/tasks.json` provides "CTMM: Kompilieren" build task
  - Recommended extension: GitHub Copilot Chat
  - LaTeX Workshop extension for syntax highlighting and PDF preview
- **CI/CD**: Automated PDF building via GitHub Actions

## Contributing Best Practices

### Code Reviews
- Test builds before submitting PR
- Verify PDF output renders correctly
- Check for LaTeX compilation warnings
- Ensure German text is properly encoded
- Validate therapeutic content accuracy

### Documentation Updates
- Update README.md for new features or conventions
- Document new macros or style changes
- Include usage examples for complex components
- Maintain this Copilot instructions file

### Git Workflow
- Use descriptive commit messages in English
- Reference issue numbers when applicable
- Keep commits focused on single changes
- Test thoroughly before pushing

---

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

**Build Commands:**
- `python3 ctmm_build.py` - Main build system
- `make check` - Quick dependency check
- `make build` - Generate PDF
- `make clean` - Remove artifacts

### Key Files to Know
- `main.tex` - Document entry point and ALL package definitions
- `ctmm_build.py` - Primary build system and validation
- `style/*.sty` - Design and component definitions
- `modules/*.tex` - Individual therapy content
- `Makefile` - Common build commands and shortcuts
- `.github/workflows/` - CI/CD pipelines with proper timeouts

**Common Macros:**
- `\ctmmCheckBox[name]{label}` - Interactive form checkboxes
- `\ctmmTextField[width]{label}{name}` - Text input fields
- `\begin{ctmmBlueBox}{title}` - Styled info boxes
- `\textcolor{ctmmBlue}{text}` - CTMM colors

Remember: This is specialized therapeutic content requiring both LaTeX expertise and sensitivity to mental health contexts.
