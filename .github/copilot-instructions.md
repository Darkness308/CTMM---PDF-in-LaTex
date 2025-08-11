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
├── therapie-material/          # Additional Word documents (.docx)
│   ├── Tool *.docx            # Original therapeutic tools
│   ├── *Matrix*.docx          # Matching matrices and logic
│   └── *Arbeitsblätter*.docx  # Worksheet templates
├── ctmm_build.py              # Automated build system (primary)
├── build_system.py            # Detailed module analysis
├── test_ctmm_build.py         # Unit tests for build system
├── validate_latex_syntax.py   # LaTeX syntax validation
├── Makefile                   # Build commands
└── .github/workflows/         # CI/CD for PDF generation
    ├── latex-build.yml        # Main PDF build workflow
    └── latex-validation.yml   # Syntax validation workflow
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
make test           # Quick test + unit tests
make test-unit      # Run only unit tests
make clean          # Remove build artifacts
make deps           # Install Python dependencies
python3 build_system.py --verbose  # Granular analysis
python3 validate_latex_syntax.py   # LaTeX syntax validation
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

### Testing and Validation

**Build System Tests:**
```bash
python3 test_ctmm_build.py     # Unit tests for build functions
make test                       # Combined build + unit tests
python3 validate_latex_syntax.py  # LaTeX syntax validation
```

**Manual Testing:**
- Test individual modules by temporarily commenting others in `main.tex`
- Verify PDF output for formatting and interactive elements
- Check German text encoding and therapeutic accuracy

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
- **Reference Materials**: Original Word documents in `therapie-material/` containing source content and templates

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
  - Uses `dante-ev/latex-action@v2.1.0` for LaTeX compilation
  - Includes syntax validation with `validate_latex_syntax.py`
  - Uploads PDF artifacts and build logs on failure
  - Runs on push/PR to main branch

## Contributing Best Practices

### Code Reviews
- Test builds before submitting PR
- Run unit tests: `python3 test_ctmm_build.py`
- Verify PDF output renders correctly
- Check for LaTeX compilation warnings
- Ensure German text is properly encoded
- Validate therapeutic content accuracy
- Run syntax validation: `python3 validate_latex_syntax.py`

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
- `make test` - Run build system + unit tests  
- `make clean` - Remove artifacts
- `make deps` - Install Python dependencies

**Key Files:**
- `main.tex` - Document entry point and preamble
- `style/*.sty` - Design and component definitions
- `modules/*.tex` - Individual therapy content
- `therapie-material/*.docx` - Source reference materials

**Common Macros:**
- `\checkbox` / `\checkedbox` - Form checkboxes
- `\begin{ctmmBlueBox}{title}` - Styled info boxes
- `\textcolor{ctmmBlue}{text}` - CTMM colors

Remember: This is specialized therapeutic content requiring both LaTeX expertise and sensitivity to mental health contexts.