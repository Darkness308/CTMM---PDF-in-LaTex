# CTMM Build Manager - Quick Start Guide

## Overview
The CTMM Build Manager is an automated tool that ensures your LaTeX project builds reliably by:
- Detecting missing files automatically
- Creating minimal templates for missing files
- Testing modules incrementally to isolate errors
- Generating comprehensive build reports

## Quick Usage

### 1. Run Complete Analysis
```bash
python3 build_manager.py
# or
make analyze
```

### 2. Standard Build
```bash
make build        # Builds main.tex
make build-ci     # Builds main_final.tex for CI
```

### 3. Clean Up
```bash
make clean        # Remove build artifacts
make clean-all    # Remove all generated files
```

## What the Build Manager Does

1. **Scans References**: Finds all `\usepackage{style/...}` and `\input{modules/...}` commands
2. **Checks Existence**: Verifies that all referenced files exist
3. **Creates Templates**: For missing files, creates minimal templates with:
   - Proper structure (`\ProvidesPackage` for .sty, `\section` for .tex)
   - TODO comments indicating what needs to be added
   - Placeholder content to prevent build errors
4. **Tests Incrementally**: 
   - First tests the basic framework (all modules commented out)
   - Then tests each module individually
   - Identifies exactly which module causes build failures
5. **Generates Report**: Creates `build_report.md` with detailed results

## Template Structure

### Style Package Template (.sty)
```latex
\NeedsTeXFormat{LaTeX2e}
\ProvidesPackage{package-name}[date Package Description - Template]

% TODO: Add package content
% TODO: Define commands and environments
```

### Module Template (.tex)
```latex
\section{Module Name}
\label{sec:module-name}

% TODO: Add actual module content here
\begin{center}
\textcolor{red}{\textbf{[MODULE NAME - CONTENT NEEDED]}}
\end{center}

% TODO: Replace with actual content
```

## Troubleshooting

### Common Issues
- **LaTeX not found**: Install texlive packages
- **Encoding errors**: Script handles UTF-8 with error replacement
- **Build timeouts**: Increase timeout in script if needed

### Manual Recovery
If something goes wrong, the build manager creates backups:
```bash
# Restore from backup if needed
cp main.tex.backup main.tex
```

## Integration with CI/CD

The system works seamlessly with GitHub Actions:
- `main_final.tex` is the CI build target
- All templates are version-controlled
- Build reports help identify issues quickly

## Best Practices

1. **Run analysis before major changes**
2. **Check build_report.md for detailed results**
3. **Complete TODO items in generated templates**
4. **Test incrementally when adding new modules**
5. **Keep templates under version control**

This tool ensures your LaTeX build never breaks due to missing files and helps maintain a clean, modular project structure.