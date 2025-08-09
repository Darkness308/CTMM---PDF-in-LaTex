# CTMM Build Management System - Quick Start Guide

This guide provides comprehensive instructions for using the CTMM automated build management system.

## Table of Contents
- [Quick Start](#quick-start)
- [Build System Overview](#build-system-overview)
- [Commands Reference](#commands-reference)
- [Workflow Guide](#workflow-guide)
- [Troubleshooting](#troubleshooting)
- [Advanced Usage](#advanced-usage)

## Quick Start

### Prerequisites
- Python 3.x
- LaTeX distribution (TeX Live, MiKTeX, or MacTeX)
- Required LaTeX packages (installed automatically by most distributions)

### Installation Check
```bash
# Check if dependencies are available
python3 --version
pdflatex --version

# Install Python dependencies
pip install chardet
```

### Basic Usage
```bash
# 1. Run comprehensive analysis
make analyze
# or
python3 build_manager.py

# 2. Build the PDF
make build

# 3. Clean up artifacts
make clean
```

## Build System Overview

The CTMM Build Management System provides automated error detection, template generation, and comprehensive build analysis for the LaTeX-based therapeutic materials.

### Key Features
- **Automated File Detection**: Scans `main.tex` for all dependencies
- **Template Generation**: Creates structured templates for missing files
- **Incremental Testing**: Isolates problematic modules for easy debugging
- **Comprehensive Reporting**: Generates detailed `build_report.md`
- **CI/CD Integration**: Dedicated `main_final.tex` for automated builds

### System Architecture
```
CTMM Build System
├── build_manager.py     # Main comprehensive build manager
├── ctmm_build.py       # Legacy simple build system
├── build_system.py     # Legacy detailed analysis
├── main.tex            # Primary document
├── main_final.tex      # CI build target
└── Makefile           # Build commands
```

## Commands Reference

### Primary Commands

#### `make analyze` (Recommended)
Runs comprehensive build analysis including:
- File dependency scanning
- Missing file detection and template creation
- Incremental module testing
- Error isolation and reporting
- Build report generation

```bash
make analyze
```

#### `make build`
Builds the standard PDF from `main.tex`:
```bash
make build
```

#### `make build-ci`
Builds the CI version from `main_final.tex`:
```bash
make build-ci
```

### Utility Commands

#### `make test`
Quick test without generating PDFs:
```bash
make test
```

#### `make clean`
Remove build artifacts:
```bash
make clean
```

#### `make clean-all`
Remove all generated files (⚠️ includes templates):
```bash
make clean-all
```

#### `make help`
Show comprehensive help:
```bash
make help
```

### Direct Python Usage

#### Comprehensive Analysis
```bash
python3 build_manager.py
```

#### With Verbose Output
```bash
python3 build_manager.py --verbose
```

#### Custom Main File
```bash
python3 build_manager.py --main-tex custom.tex
```

## Workflow Guide

### Standard Development Workflow

1. **Initial Setup**
   ```bash
   # Clone repository and navigate to project
   cd CTMM---PDF-in-LaTex
   
   # Run comprehensive analysis
   make analyze
   ```

2. **Review Analysis Results**
   - Check `build_report.md` for comprehensive status
   - Review any `TODO_*.md` files for missing content
   - Address any problematic modules identified

3. **Complete Templates** (if any were created)
   - Edit generated template files in `style/` or `modules/`
   - Follow guidelines in corresponding `TODO_*.md` files
   - Remove TODO files when content is complete

4. **Build and Test**
   ```bash
   # Build the PDF
   make build
   
   # Test specific scenarios
   make test
   ```

5. **Clean Up**
   ```bash
   # Remove temporary files
   make clean
   ```

### Adding New Content

#### Adding a New Module
1. Add reference in `main.tex`:
   ```latex
   \input{modules/new-module-name}
   ```

2. Run analysis to create template:
   ```bash
   make analyze
   ```

3. Complete the template:
   - Edit `modules/new-module-name.tex`
   - Follow guidelines in `modules/TODO_new-module-name.md`
   - Remove TODO file when complete

#### Adding a New Style Package
1. Add reference in `main.tex`:
   ```latex
   \usepackage{style/new-style-name}
   ```

2. Run analysis and complete template as above

### CI/CD Integration

The system includes dedicated CI/CD support:

- **`main_final.tex`**: Optimized for automated builds
- **Enhanced GitHub Actions**: Automatic build verification
- **Artifact Collection**: Build reports and error logs
- **Error Reporting**: Detailed failure analysis

## Troubleshooting

### Common Issues

#### LaTeX Not Found
```
Error: pdflatex not found
```
**Solution:**
```bash
# Ubuntu/Debian
sudo apt install texlive-latex-base texlive-latex-extra texlive-fonts-recommended texlive-fonts-extra

# MacOS
brew install mactex

# Windows
# Install MiKTeX or TeX Live from official websites
```

#### Missing LaTeX Packages
```
Error: File 'package.sty' not found
```
**Solution:**
```bash
# Ubuntu/Debian - install comprehensive packages
sudo apt install texlive-latex-extra texlive-fonts-extra texlive-lang-german

# MacOS/Windows - usually included in full distributions
```

#### Python Dependencies Missing
```
Error: No module named 'chardet'
```
**Solution:**
```bash
pip install chardet
```

#### Build Failures
1. Run `make analyze` to identify problematic modules
2. Check `build_report.md` for detailed analysis
3. Review `build_error_*.log` files for specific errors
4. Fix issues and re-run analysis

### Debugging Workflow

1. **Run Comprehensive Analysis**
   ```bash
   make analyze
   ```

2. **Check Build Report**
   ```bash
   cat build_report.md
   ```

3. **Review Error Logs**
   ```bash
   ls build_error_*.log
   cat build_error_module-name.log
   ```

4. **Test Individual Components**
   ```bash
   # Test without problematic modules
   make test
   ```

## Advanced Usage

### Custom Configuration

#### Using Different Main Files
```bash
python3 build_manager.py --main-tex alternative.tex
```

#### Verbose Logging
```bash
python3 build_manager.py --verbose
```

### Integration with IDEs

#### VS Code Integration
Add to `.vscode/tasks.json`:
```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "CTMM Analyze",
            "type": "shell",
            "command": "make analyze",
            "group": "build",
            "presentation": {
                "echo": true,
                "reveal": "always",
                "focus": false,
                "panel": "shared"
            }
        }
    ]
}
```

### Automation Scripts

#### Pre-commit Hook
Create `.git/hooks/pre-commit`:
```bash
#!/bin/bash
make analyze
exit $?
```

#### Continuous Development
```bash
# Watch for changes and auto-rebuild
while inotifywait -e modify *.tex modules/*.tex style/*.sty; do
    make analyze && make build
done
```

## File Structure Reference

### Generated Files
- `build_report.md` - Comprehensive analysis report
- `build_system.log` - Detailed system logs
- `build_error_*.log` - Module-specific error logs
- `TODO_*.md` - Template completion guidelines

### Template Structure

#### Style Package Template
```latex
\NeedsTeXFormat{LaTeX2e}
\ProvidesPackage{package-name}[date description]
% TODO: Add content
```

#### Module Template
```latex
\section{Module Title}
\label{sec:module-name}
% TODO: Add content
```

## Support and Resources

- **Build Reports**: Always check `build_report.md` first
- **Error Logs**: Review specific `build_error_*.log` files
- **Documentation**: This guide and inline code comments
- **Templates**: Follow guidelines in `TODO_*.md` files

For additional help, run `make help` for command reference.

---

*CTMM Build Management System - Automated LaTeX Build Pipeline for Therapeutic Materials*