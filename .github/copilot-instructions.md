# GitHub Copilot Instructions for CTMM-System

**ALWAYS follow these instructions first and only search for additional context if the information here is incomplete or found to be in error.**

This repository contains a **LaTeX-based therapeutic materials system** called **CTMM** (Catch-Track-Map-Match) designed for creating professional therapy documents, particularly for neurodiverse couples dealing with mental health challenges including:

- Depression and mood disorders
- Trigger management 
- Borderline Personality Disorder (BPD)
- ADHD, Autism Spectrum Disorder (ASD)
- Complex PTSD (CPTSD)
- Relationship dynamics and binding patterns

**Language**: Primary content is in German (Deutsch)

## Working Effectively

**CRITICAL TIMING NOTES:**
- **NEVER CANCEL builds or tests** - Most commands complete in under 5 seconds except LaTeX package installation
- Set timeouts to 10+ minutes for any build command to be safe
- PDF builds take ~5 seconds total (4.5 seconds measured)
- Python tests take under 1 second (0.06 seconds measured)

### Bootstrap the Development Environment

**Install LaTeX dependencies FIRST (takes ~4-6 minutes, NEVER CANCEL):**
```bash
sudo apt-get update
sudo apt-get install -y texlive-latex-base texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended texlive-fonts-extra texlive-lang-german
```
**Timeout requirement**: Set timeout to 10+ minutes for LaTeX installation.

**Install Python dependencies (takes <1 second):**
```bash
pip install chardet
```

### Core Build and Test Commands

**Primary build system check (takes <1 second):**
```bash
python3 ctmm_build.py
```

**Run unit tests (takes <1 second, 22 tests):**
```bash
python3 test_ctmm_build.py
```

**Build PDF output (takes ~5 seconds, NEVER CANCEL):**
```bash
make build
```
**Expected timing**: 5 seconds total, set timeout to 2+ minutes to be safe.

**Clean build artifacts (takes <1 second):**
```bash
make clean
```

**Run comprehensive workflow validation (takes <1 second):**
```bash
python3 comprehensive_workflow.py
```

**Quick test without building PDF (takes <2 seconds):**
```bash
make test
```

### Known Issues and Workarounds

**DO NOT USE these broken commands:**
- `make analyze` - FAILS due to malformed code in `build_system.py` (line 23: `copilot/fix-403`)
- `python3 build_system.py --verbose` - FAILS for same reason

**When these fail, use working alternatives:**
- Use `python3 ctmm_build.py` instead for build system checks
- Use `make test` for validation instead of analyze

### Validation After Changes

**ALWAYS run these commands after making any changes:**

1. **Basic validation (takes <1 second):**
   ```bash
   python3 ctmm_build.py
   ```

2. **Run unit tests (takes <1 second):**
   ```bash
   python3 test_ctmm_build.py
   ```

3. **Test PDF generation (takes ~5 seconds, NEVER CANCEL):**
   ```bash
   make clean && make build
   ```

4. **Verify PDF was created:**
   ```bash
   ls -la main.pdf
   ```
   Expected: ~27 pages, ~435KB file size

5. **Run comprehensive validation (takes <1 second):**
   ```bash
   python3 comprehensive_workflow.py
   ```

**SCENARIO VALIDATION**: After making changes, ALWAYS verify the complete workflow:
- Build system detects all files correctly
- Unit tests pass (22/22)
- PDF generates without errors
- File references in `main.tex` are valid

## LaTeX Development Rules

### 📄 LaTeX Best Practices

**CRITICAL RULES - Follow these exactly:**

- **Package Loading**: ALL `\usepackage{...}` commands MUST be in the preamble of `main.tex` ONLY
- **NEVER load packages in modules or after `\begin{document}`**
- **Error**: `Can be used only in preamble` → Move package to preamble immediately

**Custom Macros & Commands:**
- Define custom macros centrally in preamble or style files ONLY
- **Use CTMM form elements exclusively:**
  ```latex
  \ctmmCheckBox[field_name]{Label}     % Interactive checkbox
  \ctmmTextField[width]{label}{name}   % Text input field
  \ctmmTextArea[width]{lines}{label}{name}  % Multi-line text area
  \ctmmRadioButton{group}{value}{label}     % Radio button
  ```
- **NEVER use** `\Box`, `\blacksquare`, or basic LaTeX form elements directly

**Module Development Rules:**
- Modules contain ONLY content, never package definitions
- Use existing macros and commands defined in preamble/style files
- Keep modules focused on single therapeutic concepts
- Test individual modules by temporarily commenting others in `main.tex`

### Adding New Modules

**Follow this exact sequence:**

1. **Add reference in main.tex:**
   ```latex
   \input{modules/my-new-module}
   ```

2. **Run build system to auto-generate templates:**
   ```bash
   python3 ctmm_build.py
   ```

3. **Verify template creation:**
   - Check `modules/my-new-module.tex` exists with basic structure
   - Check `modules/TODO_my-new-module.md` exists with completion guidelines

4. **Complete the module content** and remove TODO file when finished

5. **Test your changes:**
   ```bash
   make clean && make build
   ```

### Troubleshooting Common Issues

**When you see these errors, do this:**

- `Undefined control sequence` → Check if macro is defined in preamble, add if missing
- `Command already defined` → Remove duplicate macro definitions  
- Missing file errors → Run `python3 ctmm_build.py` to auto-generate templates
- `Can be used only in preamble` → Move `\usepackage` to main.tex preamble immediately
- `Package hyperref Error` → Ensure hyperref is loaded last in package list
- LaTeX compilation fails → Check for special characters in German text, use proper UTF-8 encoding

**Module Guidelines:**
- Use semantic section structure: `\section{Title}`, `\subsection{}`
- Include therapeutic instructions in German
- Add form elements for interactive use
- Use formal therapeutic German (Sie-Form for clients)

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
├── ctmm_build.py              # Automated build system (PRIMARY)
├── build_system.py            # Detailed module analysis (BROKEN - DO NOT USE)
├── Makefile                   # Build commands
└── .github/workflows/         # CI/CD for PDF generation
```

## CTMM Design System Elements

**Available Color Commands:**
- `\textcolor{ctmmBlue}{text}` - Primary blue (#003087)
- `\textcolor{ctmmOrange}{text}` - Accent orange (#FF6200)  
- `\textcolor{ctmmGreen}{text}` - Green (#4CAF50)
- `\textcolor{ctmmPurple}{text}` - Purple (#7B1FA2)
- `\textcolor{ctmmRed}{text}` - Red (#D32F2F)
- `\textcolor{ctmmGray}{text}` - Gray (#757575)
- `\textcolor{ctmmYellow}{text}` - Yellow (#FFC107)

**Available Box Elements:**
- `\begin{ctmmBlueBox}{Title}` - Styled info boxes in CTMM blue
- `\begin{ctmmGreenBox}{Title}` - Green boxes for positive content

**Navigation Icons:**
- Use `\faCompass` for navigation elements (requires fontawesome5 package)

## Sensitive Content Guidelines

**This repository contains mental health resources. When contributing:**

- **Respect privacy**: No personal information in examples
- **Clinical accuracy**: Ensure therapeutic techniques are evidence-based
- **Cultural sensitivity**: Content is designed for German-speaking therapy contexts
- **Professional tone**: Maintain therapeutic, non-judgmental language
- **Use formal therapeutic German (Sie-Form for clients)**
- **Medical/psychological terminology must be accurate**

**Content Types:**
- **Arbeitsblätter** (Worksheets): Interactive forms for self-reflection
- **Trigger Management**: Coping strategies and identification tools
- **Psychoeducation**: Information about mental health conditions
- **Relationship Tools**: Communication and binding pattern resources

## Technical Requirements

**Required LaTeX Packages:**
- texlive-latex-base, texlive-latex-recommended, texlive-latex-extra
- texlive-fonts-recommended, texlive-fonts-extra
- texlive-lang-german (for ngerman babel support)
- TikZ, hyperref, xcolor, fontawesome5, tcolorbox, tabularx, amssymb

**Font and Language Settings:**
- **Font encoding**: T1 with UTF-8 input
- **Language**: ngerman babel
- **PDF features**: Interactive forms, bookmarks, metadata

## Quick Reference for Common Tasks

**When building fails, run in this order:**
1. `python3 ctmm_build.py` - Check build system
2. `python3 test_ctmm_build.py` - Verify unit tests
3. `make clean` - Clear artifacts  
4. `make build` - Build PDF

**When adding new modules:**
1. Add `\input{modules/new-module}` to main.tex
2. Run `python3 ctmm_build.py` to generate templates
3. Edit generated files
4. Test with `make clean && make build`

**Key Files to Know:**
- `main.tex` - Document entry point and preamble (edit package imports here)
- `style/*.sty` - Design and component definitions
- `modules/*.tex` - Individual therapy content (no packages allowed)

**Quick Commands:**
- `python3 ctmm_build.py` - Primary build system check (<2 seconds)
- `make build` - Generate PDF (~5 seconds, NEVER CANCEL)
- `make test` - Run all validation (~2 seconds)
- `make clean` - Remove artifacts (<1 second)

## Common File Outputs

### Repository Root (ls -la)
```
.devcontainer/          # GitHub Codespace configuration
.github/               # GitHub Actions workflows
.vscode/               # VS Code tasks and settings
COMPREHENSIVE_TOOLSET.md # Comprehensive toolset documentation
LICENSE                # Project license
Makefile               # Build commands
README.md              # Main documentation (German)
README_DE_ESCAPING.md  # De-escaping tool documentation
build_system.py        # BROKEN - DO NOT USE
comprehensive_workflow.py # Workflow validation tool
conversion_workflow.py  # LaTeX conversion tools
ctmm_build.py          # PRIMARY build system
fix_latex_escaping.py  # LaTeX escaping fixes
main.tex               # Main LaTeX document
modules/               # Individual therapy modules
style/                 # LaTeX style files
test_ctmm_build.py     # Unit tests
validate_*.py          # Various validation tools
```

### Expected Build Output
**Successful build produces:**
- `main.pdf` - ~27 pages, ~435KB
- No error messages
- Unit tests: 22/22 passing
- Build system: ✓ PASS for both basic and full builds