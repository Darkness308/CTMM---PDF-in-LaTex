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
├── test_ctmm_build.py         # Unit tests for build system
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
make unit-test      # Run Python unit tests for build system
python3 build_system.py --verbose  # Granular analysis
python3 test_ctmm_build.py         # Direct unit test execution
```

### 🧪 Testing Framework

**Unit Tests:**
The repository includes comprehensive unit tests for the build system:

```bash
# Run all unit tests
make unit-test
# or directly:
python3 test_ctmm_build.py
```

**Test Coverage:**
- `filename_to_title()` function with various input formats
- File path handling and validation
- Template generation logic
- Error handling in build processes

**Continuous Integration:**
GitHub Actions workflow (`.github/workflows/latex-build.yml`) provides:
- Automated build verification on push/PR
- Python dependency installation
- Build system validation
- PDF artifact generation
- Build log collection on failures

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

### Build System Features

**Robust Error Handling:**
- Graceful handling of missing LaTeX installations
- Automatic template generation for missing files
- Comprehensive logging with detailed error messages
- Build status reporting with clear success/failure indicators

**Template Generation:**
- Creates structured module templates with proper LaTeX formatting
- Generates TODO files with completion guidelines
- Maintains consistent therapeutic content structure
- Preserves German language and formatting conventions

### Troubleshooting Common Issues

**Build Errors:**
- `Undefined control sequence` → Check if macro is defined in preamble
- `Command already defined` → Remove duplicate macro definitions
- Missing file errors → Run `ctmm_build.py` to auto-generate templates
- `[Errno 2] No such file or directory: 'pdflatex'` → LaTeX not installed

**Environment Issues:**
- **Local Development**: Install TeX Live or MiKTeX with required packages
- **GitHub Codespaces**: Pre-configured environment should work out of the box
- **CI/CD**: Check GitHub Actions logs for LaTeX installation issues

**Build System Debugging:**
- Run with verbose mode: `python3 build_system.py --verbose`
- Check individual module builds by commenting others in `main.tex`
- Review generated TODO files for completion guidance
- Check `build_system.log` for detailed error information

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

**GitHub Actions Workflow:**
- Triggers on push to main branch and pull requests
- Installs Python dependencies (`chardet`)
- Runs CTMM build system validation
- Compiles LaTeX to PDF using `dante-ev/latex-action`
- Uploads PDF and logs as artifacts
- Provides build failure diagnostics

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

**Build Commands:**
- `python3 ctmm_build.py` - Main build system with error handling
- `make check` - Quick dependency check
- `make build` - Generate PDF with LaTeX
- `make unit-test` - Run Python unit tests
- `make clean` - Remove artifacts
- `make analyze` - Detailed module analysis with logging

**Key Files:**
- `main.tex` - Document entry point and preamble
- `style/*.sty` - Design and component definitions
- `modules/*.tex` - Individual therapy content

**Common Macros:**
- `\checkbox` / `\checkedbox` - Form checkboxes
- `\begin{ctmmBlueBox}{title}` - Styled info boxes
- `\textcolor{ctmmBlue}{text}` - CTMM colors

Remember: This is specialized therapeutic content requiring both LaTeX expertise and sensitivity to mental health contexts.

## Known Issues & Environment Notes

### LaTeX Installation Requirements
- **Local Development**: Requires full LaTeX distribution (TeX Live recommended)
- **GitHub Codespaces**: Pre-configured with LaTeX packages
- **Build System**: Gracefully handles missing LaTeX installation with informative error messages
- **CI/CD**: Uses `dante-ev/latex-action` for reliable LaTeX compilation in GitHub Actions

### Build System Status
- ✅ File detection and template generation working perfectly
- ✅ Unit tests pass (14/14 tests successful)
- ✅ Module structure validation functional
- ✅ Error handling robust and informative
- ⚠️ PDF compilation requires LaTeX environment (expected limitation)

### Development Environment Setup
For full functionality, ensure:
1. LaTeX distribution installed (`pdflatex` command available)
2. Python 3.x with `chardet` package
3. All required LaTeX packages: TikZ, hyperref, xcolor, fontawesome5, tcolorbox, tabularx, amssymb