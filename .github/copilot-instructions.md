# GitHub Copilot Instructions for CTMM LaTeX System

Always follow these instructions first and only search for additional information if something in these instructions is incomplete or found to be in error.

## Project Overview

This is a **LaTeX-based therapeutic materials system** for creating interactive therapy documents in German. The repository generates a 27-page PDF workbook for mental health therapy including trigger management, depression support, and relationship tools.

## Bootstrap, Build, and Test the Repository

### Required Dependencies
Run these commands in order to set up your environment:

```bash
# Install LaTeX and German language support
sudo apt-get update
sudo apt-get install -y texlive-latex-base texlive-latex-extra texlive-fonts-recommended texlive-fonts-extra texlive-lang-german

# Install Python dependencies
pip install chardet

# Install PDF utilities (optional, for validation)
sudo apt-get install -y poppler-utils
```

**CRITICAL TIMING:** Dependency installation takes 5-10 minutes. NEVER CANCEL - set timeout to 15+ minutes.

### Primary Build Commands

**Essential workflow - run these commands in order:**

1. **Check build system and dependencies:**
   ```bash
   python3 ctmm_build.py
   ```
   - Takes ~1.7 seconds
   - Validates all files exist, auto-generates missing templates
   - Tests both basic and full builds
   - **ALWAYS run this first after any changes**

2. **Build the PDF:**
   ```bash
   make build
   ```
   - Takes ~2.2 seconds (two LaTeX passes for references)
   - Generates `main.pdf` with 27 pages (~435KB)
   - **NEVER CANCEL - LaTeX compilation can appear to hang but is working**

3. **Alternative build commands:**
   ```bash
   make check          # Same as python3 ctmm_build.py (~1.7 seconds)
   make clean          # Remove build artifacts (<0.1 seconds)
   pdflatex -interaction=nonstopmode main.tex  # Single pass (~1.1 seconds)
   ```

**CRITICAL:** All build times are under 3 seconds. If commands take longer than 30 seconds, something is wrong.

## Validation Requirements

### Manual Functionality Testing
After making any changes, **ALWAYS:**

1. **Run the complete build workflow:**
   ```bash
   make clean
   python3 ctmm_build.py
   make build
   ```

2. **Verify PDF output:**
   ```bash
   ls -la main.pdf                    # Should be ~435KB
   pdfinfo main.pdf | head -5         # Should show 27+ pages
   ```

3. **Test new module workflow if adding content:**
   ```bash
   # Add \input{modules/your-new-module} to main.tex
   python3 ctmm_build.py              # Auto-generates template
   make build                         # Verify it compiles
   ```

### Build System Features
- **Automatic template generation:** Missing files are created with proper LaTeX structure
- **Incremental validation:** Tests basic build first, then full build with all modules
- **TODO file creation:** Generates `TODO_*.md` files for new templates
- **Error isolation:** Identifies problematic modules automatically

## Repository Structure and Key Files

```
├── main.tex                    # ENTRY POINT - contains preamble and module imports
├── style/                      # LaTeX style packages (.sty files)
│   ├── ctmm-design.sty        # Colors and design elements
│   ├── form-elements.sty      # Interactive form components
│   └── ctmm-diagrams.sty      # Custom diagrams
├── modules/                    # Individual therapy content (.tex files)
│   ├── depression.tex         # Depression management content
│   ├── triggermanagement.tex  # Trigger coping strategies
│   └── arbeitsblatt-*.tex     # Interactive worksheets
├── ctmm_build.py              # PRIMARY BUILD SYSTEM - always use this
├── Makefile                   # Make commands for building
└── .github/workflows/         # CI/CD automation
```

## Working with the Codebase

### LaTeX Architecture Rules
**CRITICAL - Follow these rules exactly:**

1. **Package Loading:**
   - ALL `\usepackage{...}` commands MUST be in `main.tex` preamble
   - NEVER load packages in modules or after `\begin{document}`
   - Error "Can be used only in preamble" means package is in wrong location

2. **Checkbox Commands:**
   - Use ONLY `\checkbox` and `\checkedbox` macros
   - NEVER use `\Box` or `\blacksquare` directly (causes errors)

3. **Module Development:**
   - Modules contain ONLY content, not package definitions
   - Use existing macros defined in preamble/style files
   - Test modules by temporarily commenting others in main.tex

### Adding New Content

**Standard workflow for new modules:**

1. **Add reference to main.tex:**
   ```latex
   \input{modules/your-module-name}
   ```

2. **Run build system:**
   ```bash
   python3 ctmm_build.py
   ```
   - Creates `modules/your-module-name.tex` template
   - Creates `modules/TODO_your-module-name.md` task list

3. **Complete module content and test:**
   ```bash
   make build          # Verify compilation
   # Remove TODO file when complete
   ```

### Common Commands Reference

```bash
# Essential commands (use these regularly)
python3 ctmm_build.py           # Check dependencies and build system
make build                      # Build final PDF  
make clean                      # Clean up artifacts

# Alternative commands
make check                      # Same as ctmm_build.py
pdflatex -interaction=nonstopmode main.tex  # Direct LaTeX compilation

# Troubleshooting
python3 build_system.py --verbose    # Detailed analysis (may have encoding issues)
```

## Troubleshooting and Validation

### Common Issues and Solutions

1. **Build fails with "language 'nil'" error:**
   - Install German language support: `sudo apt-get install texlive-lang-german`

2. **"Undefined control sequence" errors:**
   - Check if macro is defined in main.tex preamble
   - Ensure you're using `\checkbox` not `\Box`

3. **Missing file errors:**
   - Run `python3 ctmm_build.py` to auto-generate templates

4. **"Can be used only in preamble" error:**
   - Move `\usepackage{...}` command to main.tex before `\begin{document}`

### Validation Checklist
Before completing any work:
- [ ] Run `python3 ctmm_build.py` - must show "✓ PASS" for both builds
- [ ] Run `make build` - must generate main.pdf successfully
- [ ] Verify PDF has expected content and page count
- [ ] Test new modules compile without errors
- [ ] Check that no TODO files remain for completed work

## GitHub Actions and CI

The repository uses automated PDF building via `.github/workflows/latex-build.yml`:
- Triggers on push/PR to main branch
- Installs dependencies, runs build system, generates PDF
- Uploads PDF and logs as artifacts
- **Note:** Current workflow has minor syntax issue on line 30 (extra dash)

## Content Guidelines

- **Language:** Primary content in German (formal therapeutic language)
- **Sensitive content:** Mental health therapy materials - maintain professional tone
- **File encoding:** UTF-8 for all files
- **LaTeX conventions:** Use semantic structure (`\section`, `\subsection`)

## Critical Reminders

- **NEVER CANCEL** build commands - they complete in under 3 seconds
- **ALWAYS** run `python3 ctmm_build.py` before building after changes  
- **VALIDATE** every change with complete build workflow
- **TEST** new content by building and verifying PDF output
- **USE** the build system rather than manual LaTeX commands for reliability

Remember: This system generates professional therapeutic materials requiring both LaTeX expertise and sensitivity to mental health contexts.