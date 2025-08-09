# CTMM LaTeX Therapeutic Materials System

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

The CTMM (Catch-Track-Map-Match) system is a LaTeX-based framework for generating interactive German-language therapeutic materials focused on mental health challenges including depression, triggers, BPD, ADHD, autism, and CPTSD.

## Working Effectively

**CRITICAL**: ALL builds and tests can complete successfully in under 5 minutes. NEVER CANCEL any build or test command. Use the specified timeouts below.

### Bootstrap Environment and Dependencies
Run these commands to set up a working environment:

```bash
# Install LaTeX (takes ~10 minutes - NEVER CANCEL)
sudo apt-get update && sudo apt-get install -y texlive-full
```
**TIMEOUT: 15 minutes (900 seconds) - NEVER CANCEL even if it appears to hang**

```bash
# Install Python dependencies (instant)
pip install chardet
```
**TIMEOUT: 60 seconds**

### Build and Test Commands
Run these commands in order to validate the system:

```bash
# Run unit tests (takes <1 second - NEVER CANCEL) 
python3 test_ctmm_build.py
```
**TIMEOUT: 60 seconds**

```bash
# Check build system and dependencies (takes ~2 seconds - NEVER CANCEL)
python3 ctmm_build.py
```
**TIMEOUT: 120 seconds**

```bash
# Build PDF document (takes ~4 seconds total - NEVER CANCEL)
make build
```
**TIMEOUT: 300 seconds**

Alternative build commands:
```bash
make check          # Run build system check (~2 seconds)
make unit-test      # Run Python unit tests (<1 second)  
make all           # Run check + build (~4 seconds total)
make clean         # Remove build artifacts (instant)
make help          # Show available targets (instant)
```

**DO NOT USE:** `make analyze` - has encoding issues, use the basic commands above instead.

### Verify PDF Generation
After building, verify the PDF was generated successfully:

```bash
# Check PDF exists and get metadata
ls -la main.pdf
file main.pdf
pdfinfo main.pdf
```

Expected output: 27-page PDF with interactive forms, German content, and CTMM metadata.

## Validation Scenarios

**ALWAYS run these validation steps after making any changes:**

1. **Unit Test Validation:** Run `python3 test_ctmm_build.py` and verify all 14 tests pass.

2. **Build System Validation:** Run `python3 ctmm_build.py` and verify:
   - "All referenced files exist" message
   - "Basic build: ✓ PASS" 
   - "Full build: ✓ PASS"
   - "PDF generated successfully"

3. **PDF Generation Validation:** Run `make build` and verify:
   - No LaTeX errors in output
   - `main.pdf` file is created
   - PDF is 27 pages and ~435KB
   - `pdfinfo main.pdf` shows proper CTMM metadata

4. **New Module Testing:** When adding modules to `main.tex`:
   - Add `\input{modules/new-module-name}` to main.tex
   - Run `python3 ctmm_build.py` to auto-generate templates
   - Verify template files are created in `modules/` directory
   - Complete template content and remove TODO files

## Repository Structure and Key Files

### Core Build Files
- `main.tex` - Main LaTeX document (entry point, contains preamble)
- `ctmm_build.py` - Primary build system with template generation  
- `test_ctmm_build.py` - Unit tests for build system functions
- `Makefile` - Build automation with tested targets

### Content Organization  
- `style/` - LaTeX style packages (.sty files):
  - `ctmm-design.sty` - Color scheme and design elements
  - `form-elements.sty` - Interactive form components
  - `ctmm-diagrams.sty` - Custom diagrams and visual elements
- `modules/` - Individual therapy content modules (.tex files)
- `therapie-material/` - Additional therapy resources

### Configuration
- `.devcontainer/devcontainer.json` - GitHub Codespace configuration
- `.vscode/tasks.json` - VS Code build tasks for LaTeX
- `.github/workflows/latex-build.yml` - CI/CD for automated PDF generation

## LaTeX Development Rules

**CRITICAL RULES - violating these causes build failures:**

### Package Loading
- ALL `\usepackage{...}` commands MUST be in `main.tex` preamble only
- NEVER load packages in module files or after `\begin{document}`
- Error "Can be used only in preamble" means a package was loaded in wrong location

### Custom Macros
- Define macros only in preamble or style files, never in modules
- Use predefined checkbox macros only:
  ```latex
  \checkbox        % Empty checkbox: □
  \checkedbox      % Filled checkbox: ■  
  ```
- NEVER use `\Box` or `\blacksquare` directly (causes undefined control sequence errors)

### Module Development
- Modules contain ONLY content, no package loading or macro definitions
- Use existing macros from preamble/style files
- Structure modules with `\section{Title}` and `\subsection{}`
- Include German therapeutic instructions and form elements

## Common Build Issues and Solutions

**"Undefined control sequence"** → Check if macro is defined in preamble
**"Command already defined"** → Remove duplicate macro definitions  
**"Can be used only in preamble"** → Move `\usepackage` to main.tex preamble
**Missing file errors** → Run `python3 ctmm_build.py` to auto-generate templates
**Encoding errors** → Use UTF-8 encoding for all German text files

## Content Guidelines

This repository contains sensitive mental health materials in German. When contributing:

- Maintain therapeutic, professional language using formal German (Sie-Form)
- Ensure clinical accuracy for techniques and medical terminology
- Respect privacy - no personal information in examples
- Test all interactive form elements after changes
- Validate German text encoding (UTF-8)

## Quick Command Reference

**Frequently used commands with validated timings:**

```bash
# Complete setup and build (total ~15 minutes including LaTeX install)
sudo apt-get update && sudo apt-get install -y texlive-full  # 10 min
pip install chardet                                           # instant
python3 test_ctmm_build.py                                   # <1 sec
python3 ctmm_build.py                                        # 2 sec  
make build                                                   # 4 sec
```

**Repository navigation:**
```bash
ls -la                           # Show all files in root
ls -la style/                    # Show LaTeX style files
ls -la modules/                  # Show therapy content modules
find . -name "*.tex" | head -10  # Find LaTeX source files
```

**Git workflow:**
```bash
git status                       # Check working directory status
git --no-pager log --oneline -5  # Show recent commits
git --no-pager diff              # Show current changes
```

Remember: This is a specialized therapeutic LaTeX system requiring both technical LaTeX knowledge and sensitivity to German mental health contexts.