# CTMM LaTeX-System - Paket-Dependencies

## Erforderliche LaTeX-Pakete mit Versionen

### Basis-System
- **texlive-latex-base** >= 2023
- **texlive-latex-recommended** >= 2023
- **texlive-fonts-recommended** >= 2023

### Kritische Pakete (mit Versionen)
```tex
# CTMM LaTeX Dependencies & Package Management

## Core LaTeX Distribution
- **Required:** TexLive 2023 or later
- **Minimal:** TexLive 2022 (with manual package updates)

## Essential Packages with Versions

### Document Structure & Formatting
```latex
\RequirePackage{geometry}     % v5.9 - Page layout
\RequirePackage{fancyhdr}     % v4.0.1 - Headers and footers
\RequirePackage{titlesec}     % v2.14 - Section formatting
\RequirePackage{tocloft}      % v2.3i - Table of contents
\RequirePackage{multicol}     % v1.9a - Multiple columns
\RequirePackage{enumitem}     % v3.9 - List formatting
```

### Colors & Graphics
```latex
\RequirePackage{xcolor}       % v2.14 - Color support
\RequirePackage{tikz}         % v3.1.10 - Graphics and diagrams
\RequirePackage{tcolorbox}    % v5.1.1 - Colored boxes
\RequirePackage{graphicx}     % v1.2d - Graphics inclusion
\RequirePackage{adjustbox}    % v1.3a - Box adjustments
```

### Interactive Forms & PDF Features
```latex
\RequirePackage{hyperref}     % v7.00v - PDF links and forms
\RequirePackage{insdljs}      % v1.3 - JavaScript in PDF
\RequirePackage{eforms}       % v2.9h - Enhanced PDF forms
\RequirePackage{acrotex}      % v1.0 - Advanced AcroForms
```

### Typography & Text Processing
```latex
\RequirePackage{fontenc}      % T1 encoding
\RequirePackage{inputenc}     % UTF-8 input
\RequirePackage{babel}        % German language support
\RequirePackage{microtype}    % v3.0a - Microtypography
\RequirePackage{setspace}     % v6.7a - Line spacing
```

## Installation Commands

### Ubuntu/Debian (GitHub Actions)
```bash
sudo apt-get update
sudo apt-get install -y texlive-full texlive-fonts-extra
sudo apt-get install -y chktex lacheck  # Linting tools
```

### Manual Package Installation (if needed)
```bash
tlmgr update --self
tlmgr install collection-latexextra
tlmgr install collection-fontsrecommended
tlmgr install insdljs eforms acrotex
```

## CI/CD Configuration

### GitHub Actions Workflow Requirements
```yaml
- name: Install LaTeX dependencies
  run: |
    sudo apt-get update
    sudo apt-get install -y texlive-full texlive-fonts-extra
    sudo apt-get install -y chktex lacheck

- name: LaTeX Syntax Check
  run: find . -name "*.tex" -exec chktex -q {} \;

- name: Compile with 3-pass build
  uses: dante-ev/latex-action@v0.2.0
  with:
    root_file: main.tex
    args: "-synctex=1 -interaction=nonstopmode -file-line-error"
```

### Build Validation Steps
1. **Syntax Validation:** `chktex` for LaTeX warnings
2. **Link Validation:** Check for undefined references in `.log`
3. **PDF Verification:** Confirm output file creation and basic info
4. **Form Validation:** Test AcroForms functionality (manual)

## Package Conflicts & Solutions

### Known Issues
- **hyperref vs. tikz:** Load hyperref AFTER tikz
- **xcolor conflicts:** Define colors after package loading
- **eforms dependency:** Requires specific hyperref configuration

### Resolution Strategy
```latex
% Correct loading order:
\RequirePackage{tikz}
\RequirePackage{xcolor}
\RequirePackage[unicode]{hyperref}  % Load AFTER graphics
\RequirePackage{eforms}             % Load AFTER hyperref
```

## Version Compatibility Matrix

| Package | Min Version | Tested Version | Notes |
|---------|-------------|----------------|-------|
| hyperref | v7.00 | v7.00v | PDF forms support |
| tikz | v3.1.0 | v3.1.10 | Diagrams stable |
| tcolorbox | v5.0.0 | v5.1.1 | Box layouts |
| eforms | v2.9 | v2.9h | Interactive forms |
| xcolor | v2.13 | v2.14 | Color definitions |

## Troubleshooting Guide

### Common Compilation Errors
1. **"Package eforms not found"**
   ```bash
   tlmgr install eforms
   ```

2. **"Undefined control sequence 	extcolor"**
   - Check: `\RequirePackage{xcolor}` is loaded
   - Verify: No typos like `extcolor`

3. **"PDF forms not interactive"**
   - Ensure: `eforms` package is loaded
   - Check: PDF viewer supports AcroForms

### Build Environment Setup
```bash
# Local development
sudo apt-get install texlive-full
code --install-extension james-yu.latex-workshop

# Validation tools
sudo apt-get install chktex lacheck
```

## Performance Optimization

### Build Speed Improvements
- Use `pdflatex` instead of `latex + dvipdf`
- Enable `--synctex=1` only in development
- Limit TikZ complexity for faster compilation

### Resource Management
- Build directory separation: `--output-directory=build`
- Automatic cleanup: Remove `.aux`, `.log`, `.toc` files
- Artifact retention: 30 days for PDFs, 7 days for logs

## Security Considerations

### PDF Form Security
- **JavaScript validation:** Client-side only, not server validation
- **Data export:** Forms can export to FDF/XFDF format
- **Viewer compatibility:** Adobe Reader required for full functionality

### Package Trust
- Use official CTAN packages only
- Verify package signatures when possible
- Review package documentation for security notes
```

### Zusätzliche Pakete
```bash
# Ubuntu/Debian Installation:
sudo apt-get update
sudo apt-get install texlive-full
sudo apt-get install texlive-fonts-extra
sudo apt-get install texlive-latex-extra

# Manuelle Paket-Installation (falls nötig):
tlmgr install fontawesome5
tlmgr install tcolorbox
tlmgr install pgf          # für TikZ
tlmgr install geometry
tlmgr install hyperref
tlmgr install xcolor
```

## Build-Dependencies
```json
{
  "latexmk": ">=4.77",
  "pdflatex": ">=3.141592653",
  "bibtex": ">=0.99d"
}
```

## Kompatibilität
- **Mindest-LaTeX:** TeXLive 2022
- **Empfohlen:** TeXLive 2023 oder neuer
- **Getestet mit:** TeXLive 2023/Debian

## Fehlerbehebung
```bash
# Bei fehlenden Paketen:
sudo apt-get install texlive-fonts-extra texlive-latex-extra

# Bei veralteten Versionen:
sudo apt-get upgrade texlive-base

# Manuelle Updates:
sudo tlmgr update --self
sudo tlmgr update --all
```
