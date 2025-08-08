# CTMM LaTeX System - GitHub Copilot Instructions

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

## System Overview
CTMM (Catch-Track-Map-Match) is a modular LaTeX framework for creating interactive therapy workbooks. The system generates a 27-page PDF with 134 interactive form elements (74 text fields, 60 checkboxes) for therapeutic documentation and patient worksheets.

## Working Effectively

### Bootstrap and Build the Repository
Install LaTeX dependencies first (CRITICAL for FontAwesome5 support):
- `sudo apt-get update && sudo apt-get install -y texlive-full`
  - NEVER CANCEL: Installation takes 15-20 minutes. Set timeout to 30+ minutes.
- `pip install chardet`

Validate the build system:
- `python3 ctmm_build.py` - runs in ~2 seconds, validates all modules and creates missing file templates
- `make check` - NEVER CANCEL: runs build system check, takes ~2 seconds
- `make build` - NEVER CANCEL: compiles PDF, takes ~3 seconds total (2 passes)
- `make clean` - removes build artifacts, runs in <1 second

### Full Build Process (NEVER CANCEL - Set 5+ minute timeouts)
Complete build sequence:
- `make deps` - install Python dependencies (~1 second)
- `make check` - validate system and dependencies (~2 seconds) 
- `make build` - full PDF compilation (~3 seconds for two pdflatex passes)

The build is FAST (under 5 seconds total) but always use generous timeouts in case of font generation.

### Common Build Commands and Timing
- `python3 ctmm_build.py` - Basic system check: ~2 seconds
- `pdflatex -interaction=nonstopmode main.tex` - Single pass: ~2.5 seconds
- `make test` - Quick validation: ~2 seconds  
- `make analyze` - Detailed module testing: ~11 seconds (may fail on encoding issues, non-critical)
- `make clean` - Cleanup: <1 second

NEVER CANCEL: Always wait for completion. Font generation during first builds may extend timing.

## Validation Scenarios

ALWAYS manually validate changes by:

1. **Build Validation**:
   - Run `make check && make build` 
   - Verify `main.pdf` is generated (should be ~435KB, 27 pages)
   - Check with `pdfinfo main.pdf` for proper metadata

2. **Interactive Form Testing**:
   - Open `main.pdf` in a PDF viewer that supports forms (Adobe Reader, Foxit, etc.)
   - Navigate to "Demo: Interaktive PDF-Formulare" section (around page 25)
   - Test text fields: Name, E-Mail, Telefon fields should be clickable and editable
   - Test checkboxes: Hobby checkboxes (Lesen, Musik, Sport, Kochen, Reisen, Gaming) should be toggleable
   - Test text areas: Multi-line description and goal fields should allow paragraph input
   - Verify forms retain input when saved and reopened

3. **Module Content Validation**:
   - Confirm all 14 therapy modules are included
   - Check for proper navigation between sections
   - Verify colored boxes (ctmmBlueBox, ctmmGreenBox, etc.) render correctly
   - Ensure FontAwesome icons display properly (not as missing character boxes)

4. **CRITICAL Error Patterns**:
   - If you see "Emergency stop" and "cannot \\read from terminal": FontAwesome5 package missing
   - If build fails on missing files: Run `python3 ctmm_build.py` to auto-generate templates
   - If PDF is corrupted: Run second pdflatex pass for proper references

## Dependencies and Installation

### Required LaTeX Packages (via texlive-full)
- `fontawesome5` - CRITICAL: Icons will break without this
- `tcolorbox` - For colored therapy module boxes  
- `hyperref` - Interactive PDF forms
- `tikz` - Graphics and diagrams
- `xcolor` - Color definitions
- `geometry` - Page layout

### Python Dependencies
- `chardet` - Character encoding detection for module files

### Installation Commands (EXACT sequence)
```bash
# Install LaTeX (NEVER CANCEL - 15-20 minutes)
sudo apt-get update
sudo apt-get install -y texlive-full

# Install Python dependencies
pip install chardet

# Verify installation
kpsewhich fontawesome5.sty  # Should return path
pdflatex --version         # Should show pdfTeX version
```

## Repository Structure

### Core Files
- `main.tex` - Main document (DO NOT modify package loading order)
- `Makefile` - Build automation with all validated commands
- `ctmm_build.py` - Simplified build system and validation
- `build_system.py` - Detailed module analysis (may have encoding issues)

### Style Files (style/)
- `ctmm-design.sty` - Color scheme and box definitions
- `form-elements.sty` - Interactive form components (text fields, checkboxes)  
- `ctmm-diagrams.sty` - TikZ diagrams and graphics

### Content Modules (modules/) - 14 therapy modules
- `depression.tex` - Depression management module
- `triggermanagement.tex` - Trigger identification and management
- `bindungsleitfaden.tex` - Attachment dynamics guide
- `demo-interactive.tex` - Interactive form demonstration
- `arbeitsblatt-*.tex` - Various therapy worksheets
- Additional specialized modules for therapy protocols

### Source Materials
- `therapie-material/` - Original Word documents (reference only)
- `build/` - Contains pre-built PDF version

## Critical Development Notes

### LaTeX Package Loading Rules
- NEVER add `\usepackage` commands inside modules or after `\begin{document}`
- ALL packages must be loaded in main.tex preamble
- FontAwesome5 commands (`\faEdit`, `\faArrowRight`, etc.) only work with full TeXLive

### Form Element Usage
Always use these macros for interactive elements:
- `\ctmmTextField[width]{default}{fieldname}` - Text input fields
- `\ctmmCheckBox[fieldname]{label}` - Checkboxes  
- `\ctmmTextArea[width]{lines}{fieldname}{default}` - Multi-line text areas

### Module Development
When creating new modules:
1. Add `\input{modules/new-module}` to main.tex
2. Run `python3 ctmm_build.py` - auto-creates template with TODO file
3. Complete content in generated template
4. Test with `make check && make build`
5. Remove `TODO_new-module.md` when complete

### Troubleshooting Common Issues
- **Build fails on missing FontAwesome**: Install texlive-full package
- **"Undefined control sequence"**: Check if custom commands are defined in style files
- **Form fields not working**: Verify hyperref package loaded and PDF viewer supports forms
- **Character encoding errors**: Check file encoding with `file modulename.tex`

## CI/CD Integration
- `.github/workflows/latex-build.yml` - Automated builds on push/PR
- Upload artifacts: `main.pdf` and build logs on failure
- Uses same commands: `python3 ctmm_build.py && pdflatex main.tex`

## Manual Validation Checklist
Before committing changes:
- [ ] `make clean && make check && make build` succeeds
- [ ] `main.pdf` generated (27 pages, ~435KB)
- [ ] Interactive forms functional in PDF viewer
- [ ] No missing FontAwesome icons (appear as missing chars if broken)
- [ ] All colored boxes render properly
- [ ] No LaTeX errors in build log

REMEMBER: This system builds FAST (~3 seconds) but creates complex interactive therapy documents. Always validate form functionality manually after changes.