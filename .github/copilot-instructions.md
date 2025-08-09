# Copilot Instructions for CTMM-System

**ALWAYS reference these instructions first and fallback to search or additional context gathering only when you encounter unexpected information that does not match the information here.**

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
│   └── ...                    # Other therapeutic modules
├── therapie-material/          # Additional therapy resources
├── ctmm_build.py              # Automated build system (primary)
├── build_system.py            # Detailed module analysis
├── Makefile                   # Build commands
└── .github/workflows/         # CI/CD for PDF generation
```

## Working Effectively

### Bootstrap, Build, and Test the Repository

Run these commands to set up and validate the repository:

```bash
# Install LaTeX dependencies
sudo apt update
sudo apt install -y texlive-latex-base texlive-latex-extra texlive-fonts-recommended texlive-fonts-extra texlive-lang-german

# Install Python dependencies  
pip install chardet

# Validate build system - takes ~1.7 seconds
python3 ctmm_build.py

# Build PDF - takes ~2.2 seconds  
make build

# Full check and build - takes ~4 seconds
make all
```

### Build Commands and Timing

- **Primary build check**: `python3 ctmm_build.py` - 1.7 seconds
- **PDF generation**: `make build` - 2.2 seconds  
- **Complete workflow**: `make all` - 4 seconds
- **Clean artifacts**: `make clean` - immediate
- **Dependencies**: `make deps` - immediate if already installed

**All commands complete quickly (under 5 seconds). No special timeout requirements needed.**

### Validation

**ALWAYS run these validation steps after making changes:**

1. **Build system check**: `python3 ctmm_build.py` - must show "✓ PASS" for both basic and full builds
2. **PDF generation**: `make build` - must complete without errors and generate `main.pdf`
3. **File verification**: `ls -la main.pdf && file main.pdf` - must show valid PDF document
4. **Manual validation**: Open and inspect `main.pdf` to ensure content renders correctly

**Critical validation scenario**: After any module or style changes, ALWAYS run:
```bash
make clean && make all
```
Then verify the PDF contains the expected content and no compilation errors occurred.

## LaTeX Architecture & Conventions

### 🔧 Build System Usage

**Primary Build Command:**
```bash
python3 ctmm_build.py
```

**What the build system does:**
1. Scans `main.tex` for all `\usepackage{style/...}` and `\input{modules/...}` references
2. Auto-generates missing template files with proper structure
3. Tests basic build (without modules) and full build
4. Creates TODO files for new templates with completion guidelines

**Alternative Commands:**
```bash
make check          # Run build system check
make build          # Build PDF with pdflatex
make analyze        # Detailed module testing
python3 build_system.py --verbose  # Granular analysis
```

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
- **Local**: LaTeX distribution (TeX Live, MiKTeX) with required packages
- **GitHub Codespace**: Pre-configured environment available
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

## Common Tasks

Run these commands for frequent development activities:

### Environment Setup (First Time)
```bash
# Check if LaTeX is installed
which pdflatex || echo "LaTeX not installed"

# Install LaTeX on Ubuntu/Debian systems
sudo apt update && sudo apt install -y texlive-latex-base texlive-latex-extra texlive-fonts-recommended texlive-fonts-extra texlive-lang-german

# Install Python dependencies
pip install chardet

# Verify installation
python3 --version  # Should show Python 3.x
pdflatex --version  # Should show pdfTeX version
```

### Daily Development Workflow
```bash
# Start with clean state
make clean

# Check build system
python3 ctmm_build.py

# Build PDF  
make build

# Verify PDF was created
ls -la main.pdf && file main.pdf
```

### Adding New Modules
```bash
# 1. Add reference to main.tex manually:
# \input{modules/my-new-module}

# 2. Run build system to auto-generate template
python3 ctmm_build.py

# 3. Edit the generated file: modules/my-new-module.tex

# 4. Test build
make build

# 5. Remove TODO file when complete: modules/TODO_my-new-module.md
```

### Troubleshooting Build Issues
```bash
# Check detailed analysis (takes ~10 seconds)
make analyze

# Clean and rebuild
make clean && make all

# Check for encoding issues in modules
python3 build_system.py --verbose
```

## Repository Contents

Use these reference outputs instead of running commands to save time:

### Root Directory Listing
```
.devcontainer/
.git/
.github/
.gitignore
.vscode/
HYPERLINK-STATUS.md
LICENSE  
Makefile
README.md
build/
build_system.py*
ctmm_build.py*
main.pdf
main.tex
modules/
style/
therapie-material/
```

### Modules Directory
```
arbeitsblatt-checkin.tex
arbeitsblatt-depression-monitoring.tex  
arbeitsblatt-trigger.tex
bindungsleitfaden.tex
demo-interactive.tex
depression.tex
interactive.tex
navigation-system.tex
notfallkarten.tex
qrcode.tex
safewords.tex
selbstreflexion.tex
therapiekoordination.tex
triggermanagement.tex
```

### Style Directory  
```
ctmm-design.sty
ctmm-diagrams.sty
form-elements.sty
```

---

## Quick Reference

**Build Commands:**
- `python3 ctmm_build.py` - Main build system
- `make check` - Quick dependency check
- `make build` - Generate PDF
- `make clean` - Remove artifacts

**Key Files:**
- `main.tex` - Document entry point and preamble
- `style/*.sty` - Design and component definitions
- `modules/*.tex` - Individual therapy content

**Common Macros:**
- `\checkbox` / `\checkedbox` - Form checkboxes
- `\begin{ctmmBlueBox}{title}` - Styled info boxes
- `\textcolor{ctmmBlue}{text}` - CTMM colors

Remember: This is specialized therapeutic content requiring both LaTeX expertise and sensitivity to mental health contexts.