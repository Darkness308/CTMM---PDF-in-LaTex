# Copilot Instructions for CTMM-System

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
  \ctmmCheckBox[fieldname]{label}    % Interactive checkbox from form-elements.sty
  \ctmmTextField[width]{default}{name}  % Text input field
  \ctmmRadioButton{group}{value}{label} % Radio button
  ```
- **NEVER** use `\Box` or `\blacksquare` directly (causes undefined control sequence errors)
- **Color Usage**: Use predefined CTMM colors from `ctmm-design.sty`:
  ```latex
  \textcolor{ctmmBlue}{text}    % Primary blue
  \textcolor{ctmmOrange}{text}  % Accent orange  
  \textcolor{ctmmGreen}{text}   % Success/positive green
  \textcolor{ctmmPurple}{text}  % Special sections
  ```

#### Module Development
- Modules should contain ONLY content, not package definitions
- Use existing macros and commands defined in preamble/style files
- Keep modules focused on single therapeutic concepts

### 🎨 CTMM Design System

**Color Scheme:**
- `ctmmBlue` - Primary blue for headers and structure (`#003087`)
- `ctmmOrange` - Accent orange for highlights (`#FF6200`)
- `ctmmGreen` - Green for positive elements (`#4CAF50`)
- `ctmmPurple` - Purple for special sections (`#7B1FA2`)
- `ctmmRed` - Red for warnings/alerts (`#D32F2F`)
- `ctmmGray` - Gray for secondary text (`#757575`)
- `ctmmYellow` - Yellow for highlights (`#FFC107`)

**Custom Elements:**
- `\begin{ctmmBlueBox}{Title}` - Blue styled info boxes
- `\begin{ctmmGreenBox}{Title}` - Green styled info boxes  
- `\begin{ctmmOrangeBox}{Title}` - Orange styled info boxes
- `\ctmmTextField[width]{default}{name}` - Interactive text fields
- `\ctmmCheckBox[name]{label}` - Interactive checkboxes
- `\ctmmRadioButton{group}{value}{label}` - Radio buttons
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
- `Can be used only in preamble` → Move `\usepackage` to main.tex preamble
- `File not found` → Check file paths and ensure modules are referenced correctly

**Form Element Issues:**
- Interactive forms not working → Check hyperref package is loaded
- Checkbox styling issues → Use `\ctmmCheckBox` instead of raw LaTeX symbols
- Text field problems → Verify `\ctmmTextField` syntax: `[width]{default}{name}`

**Module Guidelines:**
- Use semantic section structure: `\section{Title}`, `\subsection{}`
- Include therapeutic instructions in German
- Add form elements for interactive use
- Test individual modules by temporarily commenting others
- **Never load packages in modules** - only in main.tex preamble

## Content Guidelines

### 🧠 Therapeutic Content

**Sensitive Material**: This repository contains mental health resources. When contributing:

- **Respect privacy**: No personal information in examples
- **Clinical accuracy**: Ensure therapeutic techniques are evidence-based
- **Cultural sensitivity**: Content is designed for German-speaking therapy contexts
- **Professional tone**: Maintain therapeutic, non-judgmental language

**Content Types:**
- **Arbeitsblätter** (Worksheets): Interactive forms for self-reflection
  - `arbeitsblatt-checkin.tex` - Daily check-in forms
  - `arbeitsblatt-trigger.tex` - Trigger identification and management
  - `arbeitsblatt-depression-monitoring.tex` - Depression tracking
- **Trigger Management**: Coping strategies and identification tools
  - `triggermanagement.tex` - Main trigger management content
  - `safewords.tex` - Safe word systems for couples
- **Psychoeducation**: Information about mental health conditions
  - `depression.tex` - Depression-related content and strategies
  - `bindungsleitfaden.tex` - Attachment and binding patterns
- **Relationship Tools**: Communication and binding pattern resources
  - `therapiekoordination.tex` - Therapy coordination between partners
  - `notfallkarten.tex` - Emergency/crisis cards
- **System Components**: Navigation and interactive elements
  - `navigation-system.tex` - Document navigation structure
  - `interactive.tex` - Interactive form demonstrations

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
- **TikZ Usage**: Custom diagrams in `ctmm-diagrams.sty`, form element styling
- **Form System**: Based on hyperref package for interactive PDF forms

### Development Environment
- **Local**: LaTeX distribution (TeX Live, MiKTeX) with required packages
  - Essential packages: `texlive-latex-base`, `texlive-latex-extra`, `texlive-latex-recommended`
  - Font packages: `texlive-fonts-extra` (includes FontAwesome5)
- **GitHub Codespace**: Pre-configured environment available
- **CI/CD**: Automated PDF building via GitHub Actions
- **Package Requirements**: 
  ```bash
  # Ubuntu/Debian
  sudo apt-get install texlive-latex-base texlive-latex-extra texlive-latex-recommended texlive-fonts-extra
  
  # Python dependencies
  pip install chardet
  ```

## Contributing Best Practices

### Code Reviews
- Test builds before submitting PR
- Verify PDF output renders correctly  
- Check for LaTeX compilation warnings
- Ensure German text is properly encoded
- Validate therapeutic content accuracy
- **Test form functionality**: Verify interactive elements work in PDF viewers
- **Module isolation**: Test individual modules by commenting others in main.tex
- **Build system validation**: Run `python3 ctmm_build.py` before committing

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
- `\ctmmCheckBox[name]{label}` - Interactive form checkboxes
- `\ctmmTextField[width]{default}{name}` - Interactive text fields
- `\begin{ctmmBlueBox}{title}` - Styled info boxes
- `\textcolor{ctmmBlue}{text}` - CTMM colors
- `\faCompass`, `\faCalendar`, `\faUsers` - FontAwesome icons

Remember: This is specialized therapeutic content requiring both LaTeX expertise and sensitivity to mental health contexts.