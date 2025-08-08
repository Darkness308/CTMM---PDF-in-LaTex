# GitHub Copilot Instructions for CTMM-System

**Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.**

## Project Overview

This repository contains a **LaTeX-based therapeutic materials system** called **CTMM** (Catch-Track-Map-Match) designed for creating professional therapy documents, particularly for neurodiverse couples dealing with mental health challenges including:

- Depression and mood disorders
- Trigger management 
- Borderline Personality Disorder (BPD)
- ADHD, Autism Spectrum Disorder (ASD)
- Complex PTSD (CPTSD)
- Relationship dynamics and binding patterns

**Language**: Primary content is in German (Deutsch)

## Repository Structure

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
│   └── ...                    # Other therapeutic modules (14 total)
├── therapie-material/          # Additional therapy resources
├── ctmm_build.py              # Automated build system (primary - ~2 seconds)
├── build_system.py            # Detailed module analysis (~10 seconds)
├── Makefile                   # Build commands (validated)
└── .github/workflows/         # CI/CD for PDF generation
```

## Working Effectively

### **CRITICAL**: Dependencies Setup

**Install LaTeX distribution first:**
```bash
sudo apt-get update
sudo apt-get install -y texlive-latex-base texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended texlive-lang-german texlive-fonts-extra
```
**Timing**: LaTeX installation takes 8-12 minutes. NEVER CANCEL - set timeout to 15+ minutes.

**Install Python dependencies:**
```bash
pip install chardet
```

### Build Commands (All Validated)

**Primary Build System - Run this first:**
```bash
python3 ctmm_build.py
```
**Timing**: ~2 seconds. Tests all dependencies and generates missing templates.

**LaTeX PDF Generation:**
```bash
make build
```
**Timing**: ~4 seconds total (2 pdflatex passes). Creates 27-page PDF (~435KB).

**Build System Validation:**
```bash
make check
```
**Timing**: ~2 seconds. Runs ctmm_build.py and validates dependencies.

**Quick Test:**
```bash
make test
```
**Timing**: ~2 seconds. Tests build system without generating PDF.

**Detailed Module Analysis:**
```bash
python3 build_system.py --verbose
```
**Timing**: ~10 seconds. Tests modules incrementally. May fail on encoding issues in safewords.tex module but still provides useful diagnostics.

**Alternative via Make:**
```bash
make analyze
```
**Note**: Currently fails due to UTF-8 encoding issue in safewords.tex module, but analysis command works when run directly.

**Clean Build Artifacts:**
```bash
make clean
```
**Timing**: <1 second. Removes *.aux, *.log, *.out, *.toc, *.pdf files.

**Install Dependencies:**
```bash
make deps
```
**Timing**: ~2 seconds. Installs chardet Python package.

### Manual Validation Scenarios

**Always test these workflows after making changes:**

1. **Basic Build Validation:**
   ```bash
   python3 ctmm_build.py && ls -la main.pdf
   ```
   Verify PDF is generated (~434KB, 27 pages).

2. **New Module Creation:**
   - Add `\input{modules/my-new-module}` to main.tex
   - Run `python3 ctmm_build.py`
   - Verify template created: `modules/my-new-module.tex`
   - Verify TODO created: `modules/TODO_my-new-module.md`
   - Build should succeed and include new template content

3. **Full Build Test:**
   ```bash
   make clean && make build && pdfinfo main.pdf
   ```
   Verify clean build produces valid PDF with correct page count.

## LaTeX Architecture & Conventions

### 🔧 Build System Usage

**Primary Build Command:**
```bash
python3 ctmm_build.py
```
**Timing**: ~2 seconds. ALWAYS run this first to validate dependencies.

**What the build system does:**
1. Scans `main.tex` for all `\usepackage{style/...}` and `\input{modules/...}` references
2. Auto-generates missing template files with proper structure
3. Tests basic build (without modules) and full build
4. Creates TODO files for new templates with completion guidelines

**Alternative Commands:**
```bash
make check          # Run build system check (~2 seconds)
make build          # Build PDF with pdflatex (~4 seconds, NEVER CANCEL)
make analyze        # Detailed module testing (~10 seconds, may fail on encoding)
python3 build_system.py --verbose  # Granular analysis (~10 seconds)
```

**CRITICAL BUILD TIMINGS:**
- `python3 ctmm_build.py`: ~2 seconds
- `make build`: ~4 seconds (2 LaTeX passes)
- `make analyze`: ~10 seconds
- LaTeX dependency installation: 8-12 minutes (NEVER CANCEL)

### 📄 LaTeX Best Practices

#### Package Loading Rules
- **CRITICAL**: All `\usepackage{...}` commands MUST be in the preamble of `main.tex`
- **NEVER** load packages in modules or after `\begin{document}`
- Error: `Can be used only in preamble` → Move package to preamble

#### Custom Macros & Commands
- Define custom macros centrally in preamble or style files
- **Checkbox Convention**: Use predefined macros only:
  ```latex
  \checkbox        % Empty checkbox: □
  \checkedbox      % Filled checkbox: ■
  ```
- **NEVER** use `\Box` or `\blacksquare` directly (causes undefined control sequence errors)

#### Module Development
- Modules should contain ONLY content, not package definitions
- Use existing macros and commands defined in preamble/style files
- Keep modules focused on single therapeutic concepts

### 🎨 CTMM Design System

**Color Scheme:**
- `ctmmBlue` - Primary blue for headers and structure
- `ctmmOrange` - Accent orange for highlights  
- `ctmmGreen` - Green for positive elements
- `ctmmPurple` - Purple for special sections

**Custom Elements:**
- `\begin{ctmmBlueBox}{Title}` - Styled info boxes
- Form elements from `form-elements.sty`
- Navigation system with `\faCompass` icons
- Interactive PDF features with hyperref

## Development Workflow

### Adding New Modules

1. **Reference in main.tex:**
   ```latex
   \input{modules/my-new-module}
   ```

2. **Run build system:**
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
- **Required packages**: TikZ, hyperref, xcolor, fontawesome5, tcolorbox, tabularx, amssymb
- **Font encoding**: T1 with UTF-8 input
- **Language**: ngerman babel
- **PDF features**: Interactive forms, bookmarks, metadata

### Development Environment
- **Local Setup**: 
  1. Install LaTeX distribution (TeX Live recommended): 8-12 minutes installation time
  2. Required packages: texlive-latex-base, texlive-latex-recommended, texlive-latex-extra, texlive-fonts-recommended, texlive-lang-german, texlive-fonts-extra
  3. Install Python dependencies: `pip install chardet`
- **GitHub Codespace**: Universal devcontainer pre-configured but requires LaTeX installation
- **CI/CD**: GitHub Actions builds PDF automatically (contains syntax error on line 30 that needs fixing)

## Contributing Best Practices

### Code Reviews
- **ALWAYS** test builds before submitting PR:
  ```bash
  python3 ctmm_build.py  # Validate dependencies (~2 seconds)
  make build             # Generate PDF (~4 seconds, NEVER CANCEL)
  ```
- Verify PDF output renders correctly (should be ~434KB, 27 pages)
- Check for LaTeX compilation warnings in build logs
- Ensure German text is properly encoded (UTF-8)
- Validate therapeutic content accuracy

### Build Validation Checklist
Run these commands in order before any PR:
```bash
# 1. Validate dependencies and templates
python3 ctmm_build.py

# 2. Clean build test  
make clean

# 3. Generate PDF
make build

# 4. Verify PDF output
ls -la main.pdf  # Should be ~434KB
pdfinfo main.pdf # Should show 27 pages

# 5. Quick build system test
make test
```

**Expected Timing**: Total validation takes ~10 seconds

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

**Build Commands (All Validated):**
- `python3 ctmm_build.py` - Main build system (~2 seconds)
- `make check` - Quick dependency check (~2 seconds)
- `make build` - Generate PDF (~4 seconds, NEVER CANCEL)
- `make clean` - Remove artifacts (<1 second)
- `make test` - Quick validation (~2 seconds)
- `make deps` - Install Python dependencies (~2 seconds)

**CRITICAL Timings:**
- LaTeX installation: 8-12 minutes (NEVER CANCEL, set 15+ minute timeout)
- Full build validation: ~10 seconds total
- PDF output: ~434KB, 27 pages

**Setup Commands:**
```bash
# Install LaTeX (8-12 minutes, NEVER CANCEL)
sudo apt-get update
sudo apt-get install -y texlive-latex-base texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended texlive-lang-german texlive-fonts-extra

# Install Python dependencies
pip install chardet

# Validate setup
python3 ctmm_build.py
make build
```

**Key Files:**
- `main.tex` - Document entry point and preamble
- `style/*.sty` - Design and component definitions
- `modules/*.tex` - Individual therapy content

**Common Macros:**
- `\checkbox` / `\checkedbox` - Form checkboxes
- `\begin{ctmmBlueBox}{title}` - Styled info boxes
- `\textcolor{ctmmBlue}{text}` - CTMM colors

**Known Issues:**
- `make analyze` fails due to UTF-8 encoding issue in safewords.tex
- GitHub Actions workflow has syntax error on line 30 (extra dash)
- Build system handles encoding gracefully but detailed analysis may fail

Remember: This is specialized therapeutic content requiring both LaTeX expertise and sensitivity to mental health contexts.