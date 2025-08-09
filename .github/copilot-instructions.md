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
- **Checkbox Convention**: Use CTMM form elements instead of direct symbols:
  ```latex
  \ctmmCheckbox{label}     % Interactive checkbox from form-elements.sty
  $\square$                % Basic empty checkbox (avoid if possible)
  ```
- **NEVER** use `\Box` or `\blacksquare` directly (causes undefined control sequence errors)
- **Form Elements**: Use `\ctmmCheckbox{}`, `\ctmmRadioButton{}{}{}`, `\ctmmTextfield{}{}` from `form-elements.sty`

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
- `Unknown option 'ngerman'` → Install `texlive-lang-german` package
- `Can be used only in preamble` → Move `\usepackage{}` commands to preamble in `main.tex`

**Common Installation Issues:**
- **Missing pdflatex**: Install `texlive-latex-base` 
- **Missing German support**: Install `texlive-lang-german`
- **Missing fonts**: Install `texlive-fonts-recommended` and `texlive-fonts-extra`
- **Missing packages**: Install `texlive-latex-extra` for additional LaTeX packages

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
- **Required packages**: TikZ, hyperref, xcolor, fontawesome5, tcolorbox, tabularx, amssymb, pifont
- **Font encoding**: T1 with UTF-8 input
- **Language**: ngerman babel (requires `texlive-lang-german` package)
- **PDF features**: Interactive forms, bookmarks, metadata

**Installation Commands:**
```bash
# Ubuntu/Debian systems
sudo apt install texlive-latex-base texlive-latex-extra texlive-fonts-recommended texlive-fonts-extra texlive-lang-german

# For Python dependencies
pip install chardet
```

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
- **Validate YAML**: Check GitHub workflow files with `yamllint` before committing
- **Test locally**: Run `make check` and `python3 ctmm_build.py` before pushing

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
- `\ctmmCheckbox{label}` - Interactive checkbox from form-elements.sty
- `\ctmmRadioButton{group}{value}{label}` - Radio button
- `\ctmmTextfield{name}{width}` - Text input field
- `\begin{ctmmBlueBox}{title}` - Styled info boxes
- `\textcolor{ctmmBlue}{text}` - CTMM colors

**CTMM Colors:**
- `ctmmBlue` - Primary blue (#003087)
- `ctmmGreen` - Success green (#4CAF50)
- `ctmmOrange` - Accent orange (#FF6200)
- `ctmmRed` - Alert red (#D32F2F)
- `ctmmPurple` - Special purple (#7B1FA2)

Remember: This is specialized therapeutic content requiring both LaTeX expertise and sensitivity to mental health contexts.