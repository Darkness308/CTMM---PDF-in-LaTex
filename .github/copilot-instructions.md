# GitHub Copilot Instructions for CTMM-System

## ⚠️ ALWAYS FOLLOW THESE INSTRUCTIONS FIRST
**DIRECTIVE**: Always reference these instructions FIRST before using search, bash commands, or other exploration. Only fallback to additional context gathering when the information here is incomplete or found to be in error.

## Project Overview

This repository contains a **LaTeX-based therapeutic materials system** called **CTMM** (Catch-Track-Map-Match) designed for creating professional therapy documents for neurodiverse couples dealing with mental health challenges.

**Primary Language**: German (Deutsch) - All therapeutic content uses formal therapeutic German (Sie-Form)

### Repository Structure
```
├── main.tex                    # Main LaTeX document (entry point)
├── style/                      # LaTeX style files (.sty)  
│   ├── ctmm-design.sty        # CTMM colors and design
│   ├── form-elements.sty      # Interactive form components
│   └── ctmm-diagrams.sty      # Custom diagrams
├── modules/                    # Individual therapy modules (.tex)
│   ├── arbeitsblatt-*.tex     # Worksheets (Arbeitsblätter)
│   ├── trigger*.tex           # Trigger management
│   ├── depression.tex         # Depression content
│   └── [14 other modules]     # Total: 15 modules
├── ctmm_build.py              # Primary build system
├── build_system.py            # Detailed analysis (HAS ISSUES)
├── comprehensive_workflow.py   # Integrated validation
├── Makefile                   # Make commands
└── .github/workflows/         # CI/CD pipelines
```

## 🚀 Working Effectively - Bootstrap and Build

### Step 1: Install Dependencies
```bash
# Install LaTeX packages (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install -y texlive-latex-base texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended texlive-fonts-extra texlive-lang-german texlive-science

# Install Python dependencies  
pip install chardet
```

### Step 2: Primary Build System Commands

**ALWAYS use these validated commands:**

```bash
# 1. PRIMARY BUILD COMMAND - Use this first
python3 ctmm_build.py
# ⏱️ Takes: 1.8 seconds
# ✅ Status: WORKS PERFECTLY  
# 📋 Does: Scans files, creates templates, tests builds, generates 27-page PDF

# 2. Make wrapper for build system
make check
# ⏱️ Takes: 1.7 seconds  
# ✅ Status: WORKS PERFECTLY
# 📋 Same as ctmm_build.py but via Makefile

# 3. Generate PDF only
make build  
# ⏱️ Takes: 2.2 seconds
# ✅ Status: WORKS PERFECTLY
# 📋 Generates main.pdf (434KB, 27 pages, valid PDF)
# 🔁 Runs pdflatex twice for references

# 4. Run unit tests
python3 test_ctmm_build.py -v
# ⏱️ Takes: 0.2 seconds
# ✅ Status: WORKS PERFECTLY  
# 📋 Runs 22/22 tests, all pass

# 5. Make wrapper for unit tests
make unit-test
# ⏱️ Takes: 0.06 seconds
# ✅ Status: WORKS PERFECTLY

# 6. Comprehensive validation workflow
python3 comprehensive_workflow.py
# ⏱️ Takes: 11.6 seconds
# ⚠️ Status: MOSTLY WORKS (some sub-components fail)
# 📋 Runs full validation suite, 6/6 steps complete

# 7. Make wrapper for comprehensive 
make comprehensive
# ⏱️ Takes: 11.6 seconds  
# ⚠️ Status: MOSTLY WORKS (same as above)
```

### Step 3: Utility Commands
```bash
# Clean build artifacts
make clean        # < 1 second, WORKS
make help         # < 1 second, WORKS  
make deps         # < 1 second, WORKS
```

### ❌ COMMANDS THAT FAIL (Do NOT use)
```bash
# BROKEN: Detailed module analysis  
make analyze
python3 build_system.py --verbose
# ❌ FAILS after 9.7 seconds with UTF-8 encoding error
# 🐛 Error: "'utf-8' codec can't decode byte 0xe4 in position 14858"
# 📂 Issue: Some modules (safewords.tex) have encoding problems
```

## 🎯 Validation Scenarios

### ALWAYS Test Complete User Workflow After Changes

**Scenario 1: New Module Creation**
```bash
# 1. Add module reference to main.tex
echo '\input{modules/my-test-module}' >> main.tex

# 2. Run build system to auto-generate template  
python3 ctmm_build.py
# ✅ Creates: modules/my-test-module.tex (with TODO template)
# ✅ Creates: modules/TODO_my-test-module.md (with task list)

# 3. Verify PDF still builds
make build
# ✅ Should complete in ~2.2 seconds
# ✅ PDF should be generated successfully

# 4. Clean up test
git checkout main.tex
rm modules/my-test-module.tex modules/TODO_my-test-module.md
```

**Scenario 2: Full Build Verification**  
```bash
# 1. Clean start
make clean

# 2. Run full workflow
python3 ctmm_build.py && make build

# 3. Verify output
file main.pdf
# ✅ Should show: "main.pdf: PDF document, version 1.5"
# ✅ Size should be ~434KB with 27 pages
```

## 🔧 LaTeX Architecture Rules

### CRITICAL: Package Loading Rules
- **ALL** `\usepackage{...}` commands MUST be in `main.tex` preamble
- **NEVER** load packages in modules or after `\begin{document}`
- Error `Can be used only in preamble` → Move package to main.tex

### Custom Macros (Use these, not raw LaTeX)
```latex
\ctmmCheckBox[field_name]{Label}     % Interactive checkbox  
\ctmmTextField[width]{label}{name}   % Text input field
\ctmmTextArea[width]{lines}{label}{name}  % Multi-line area
\begin{ctmmBlueBox}{Title}           % Styled info boxes
```

**NEVER use**: `\Box`, `\blacksquare`, or basic LaTeX form elements

### CTMM Color System
```latex
\textcolor{ctmmBlue}{text}      % #003087 - Primary  
\textcolor{ctmmOrange}{text}    % #FF6200 - Accent
\textcolor{ctmmGreen}{text}     % #4CAF50 - Positive
\textcolor{ctmmRed}{text}       % #D32F2F - Warnings
```

## 🐛 Known Issues and Workarounds

### Issue 1: UTF-8 Encoding in Some Modules
- **Symptom**: Build fails with "utf-8 codec can't decode byte 0xe4"
- **Files affected**: `modules/safewords.tex` and potentially others
- **Workaround**: Use basic build system (`python3 ctmm_build.py`) instead of detailed analysis
- **DO NOT** use `make analyze` or `python3 build_system.py --verbose`

### Issue 2: Workflow YAML Parsing  
- **Symptom**: YAML parsing errors in `.github/workflows/latex-build.yml`
- **Cause**: Merge conflict markers (`copilot/fix-288`) in workflow file
- **Impact**: CI builds may fail, but local builds work fine

### Issue 3: German Character Encoding
- **Symptom**: LaTeX compilation warnings about character encoding
- **Solution**: Always use UTF-8 encoding for German text
- **Check**: German umlauts (ä, ö, ü, ß) render correctly in PDF

## 🚦 Timeout and Performance Guidelines

### Build Time Expectations
- **Basic operations**: < 2 seconds (ctmm_build.py, make check, make build)
- **Unit tests**: < 1 second (22 tests run very fast)  
- **Comprehensive workflow**: ~12 seconds (includes multiple validation steps)
- **PDF generation**: ~2 seconds (27-page document with complex LaTeX)

### ⏰ NEVER CANCEL These Commands
- `make build` - May take up to 3 seconds for complex LaTeX compilation
- `python3 comprehensive_workflow.py` - May take up to 15 seconds for full validation
- Set timeout to **60 seconds minimum** for any build command to account for system variability

## 📋 Development Workflow

### Adding New Modules
1. **Reference in main.tex**: `\input{modules/module-name}`
2. **Run build system**: `python3 ctmm_build.py`  
3. **Edit generated template**: Complete `modules/module-name.tex`
4. **Remove TODO file**: Delete `modules/TODO_module-name.md` when done
5. **Test build**: `make build` to verify PDF generation

### Before Committing Changes
```bash
# ALWAYS run these validation steps:
python3 ctmm_build.py     # Verify build system
python3 test_ctmm_build.py  # Run unit tests  
make build                # Generate PDF
# Check that main.pdf is created and is valid
```

### Common LaTeX Error Fixes
- `Undefined control sequence` → Check macro definition in preamble
- `Command already defined` → Remove duplicate macro definitions
- Missing file errors → Run `python3 ctmm_build.py` to generate templates
- Encoding errors → Ensure German text uses UTF-8 encoding

## 🎯 Content Guidelines

### Therapeutic Content Standards
- **Privacy**: No personal information in examples
- **Language**: Formal therapeutic German (Sie-Form)  
- **Accuracy**: Evidence-based therapeutic techniques only
- **Tone**: Professional, non-judgmental therapeutic language

### Module Structure
```latex
\section{Module Title}
\label{sec:module-name}

% Content with therapeutic instructions in German
% Use CTMM form elements for interactivity
% Focus on single therapeutic concept per module
```

## 🔍 Quick Reference

### Most Used Commands (In Order of Frequency)
1. `python3 ctmm_build.py` - Primary build and validation
2. `make build` - Generate PDF output  
3. `python3 test_ctmm_build.py` - Unit testing
4. `make clean` - Clean artifacts
5. `python3 comprehensive_workflow.py` - Full validation

### Key Files to Know
- `main.tex` - Document entry point, ALL packages loaded here
- `style/ctmm-design.sty` - Color definitions and design system
- `style/form-elements.sty` - Interactive form components
- `modules/*.tex` - 15 therapy modules (content only, no packages)
- `ctmm_build.py` - Primary build system (most reliable)

### Project Status
- ✅ **Build system**: Fully operational  
- ✅ **PDF generation**: Working (27 pages, 434KB)
- ✅ **Unit tests**: 22/22 passing
- ✅ **Template generation**: Automatic module creation works
- ⚠️ **Module analysis**: Has UTF-8 encoding issues (avoid `make analyze`)
- ⚠️ **CI workflows**: YAML parsing issues (local builds work fine)

**Remember**: This is specialized therapeutic content requiring both LaTeX expertise and sensitivity to mental health contexts.