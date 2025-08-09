# CTMM Build System Guide

**Comprehensive Quick-Start Documentation for the CTMM LaTeX Project**

## Overview

The CTMM Build System provides automated build management with sophisticated error detection, template generation, and incremental testing capabilities. This guide will get you up and running quickly with the enhanced build workflow.

## Quick Start

### 1. Setup Development Environment
```bash
# Clone the repository
git clone https://github.com/Darkness308/CTMM---PDF-in-LaTex.git
cd CTMM---PDF-in-LaTex

# Set up development environment (installs dependencies, runs initial check)
make dev-setup
```

### 2. Basic Build Commands
```bash
# Build the main PDF
make build

# Run comprehensive analysis
make analyze

# Quick system check
make check
```

### 3. View Results
```bash
# View the build report
make report

# Check generated PDF
ls -la *.pdf
```

## Build System Components

### Core Tools

| Tool | Purpose | Usage |
|------|---------|--------|
| `build_manager.py` | **Primary build system** - Comprehensive analysis and management | `python3 build_manager.py` |
| `ctmm_build.py` | Simplified build checker - Legacy support | `python3 ctmm_build.py` |
| `build_system.py` | Detailed module analysis - Legacy support | `python3 build_system.py --verbose` |
| `Makefile` | Convenient command interface | `make help` |

### Key Features

- **🔍 Automatic Discovery**: Scans `main.tex` for all `\usepackage{style/...}` and `\input{modules/...}` references
- **📝 Template Generation**: Creates well-structured templates for missing files with TODO guidance
- **🧪 Incremental Testing**: Tests modules individually to isolate build errors
- **📊 Comprehensive Reporting**: Generates detailed `build_report.md` with actionable insights
- **⚡ CI/CD Ready**: Dedicated `main_final.tex` target for automated builds

## Available Commands

### Build Commands
```bash
make build        # Build main.tex (development target)
make build-ci     # Build main_final.tex (CI/CD target)
```

### Analysis Commands
```bash
make check        # Quick dependency check and analysis
make analyze      # Comprehensive build analysis with verbose output
make test         # Quick test without full build
make report       # View latest build report
```

### Maintenance Commands
```bash
make clean        # Remove build artifacts (*.aux, *.log, *.pdf, etc.)
make clean-all    # Remove ALL generated files including templates (⚠️ use with caution)
make deps         # Install Python dependencies
make dev-setup    # Complete development environment setup
```

## Workflow Examples

### Adding a New Module

1. **Add reference to main.tex**:
   ```latex
   \input{modules/my-new-module}
   ```

2. **Run build system**:
   ```bash
   make check
   # or
   python3 build_manager.py
   ```

3. **Templates automatically created**:
   - `modules/my-new-module.tex` - Module template with proper structure
   - `modules/TODO_my-new-module.md` - Task list and guidelines

4. **Complete the module**:
   - Edit `modules/my-new-module.tex` with your content
   - Follow the guidelines in the TODO file
   - Remove the TODO file when complete

5. **Test your changes**:
   ```bash
   make analyze      # Test with incremental module testing
   make build        # Build final PDF
   ```

### Troubleshooting Build Issues

1. **Run comprehensive analysis**:
   ```bash
   make analyze
   ```

2. **Check the build report**:
   ```bash
   make report
   ```

3. **Review error logs**:
   - `build_manager.log` - Main build system log
   - `module_error_*.log` - Specific module error details
   - `basic_build_error.log` - Fundamental build issues
   - `full_build_error.log` - Complete build error details

4. **Common solutions**:
   ```bash
   # Fix missing LaTeX installation
   sudo apt-get install texlive-latex-extra texlive-fonts-recommended

   # Clean and retry
   make clean
   make build

   # Reset templates (if needed)
   make clean-all
   make dev-setup
   ```

### CI/CD Integration

The build system is designed for seamless CI/CD integration:

```yaml
# In GitHub Actions workflow
- name: Set up Python
  uses: actions/setup-python@v4
  with:
    python-version: '3.x'

- name: Install dependencies
  run: pip install chardet

- name: Run CTMM Build Manager
  run: python3 build_manager.py

- name: Build PDF
  uses: dante-ev/latex-action@v2.0.0
  with:
    root_file: main_final.tex
```

## Build System Architecture

### File Discovery Process

1. **Scan main.tex** for package and module references
2. **Check file existence** and identify missing files
3. **Create templates** for missing files with proper structure
4. **Test incrementally** to isolate problematic modules

### Template Generation

**Style Package Template** (`.sty` files):
```latex
\NeedsTeXFormat{LaTeX2e}
\ProvidesPackage{package-name}[date Package Description - Template]
% TODO: Add package content
```

**Module Template** (`.tex` files):
```latex
\section{Module Name}
\label{sec:module-name}
% TODO: Add actual module content
```

### Testing Strategy

1. **Basic Build Test**: Temporarily comments out all modules to test fundamental structure
2. **Incremental Module Testing**: Adds modules one by one to identify specific issues
3. **Full Build Test**: Tests complete document with all modules

## Best Practices

### Development Workflow

1. **Always run `make check`** before starting development
2. **Use `make analyze`** for detailed debugging
3. **Check `build_report.md`** for actionable insights
4. **Clean up TODO files** when templates are complete
5. **Test incrementally** as you add content

### LaTeX Best Practices

- **Package Loading**: All `\usepackage{...}` commands must be in main.tex preamble
- **Custom Macros**: Define centrally in preamble or style files, not in modules
- **Checkbox Convention**: Use `\checkbox` and `\checkedbox` macros only
- **Module Structure**: Keep modules focused on content, not package definitions

### Error Prevention

- **Never load packages in modules** (use preamble only)
- **Avoid direct symbol usage** (use defined macros)
- **Test builds frequently** during development
- **Use consistent naming conventions** for files and labels

## Advanced Features

### Verbose Analysis
```bash
python3 build_manager.py --verbose
# Shows detailed debug information
```

### Custom Main File
```bash
python3 build_manager.py --main-tex my_document.tex
# Analyze different main file
```

### Integration with IDEs

Most LaTeX IDEs can be configured to use the build system:

**VS Code** (with LaTeX Workshop):
```json
{
    "latex-workshop.latex.recipes": [
        {
            "name": "CTMM Build",
            "tools": ["ctmm-check", "pdflatex", "pdflatex"]
        }
    ],
    "latex-workshop.latex.tools": [
        {
            "name": "ctmm-check",
            "command": "python3",
            "args": ["build_manager.py"]
        }
    ]
}
```

## Support and Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| `pdflatex not found` | Install LaTeX: `sudo apt-get install texlive-latex-extra` |
| `Undefined control sequence` | Check macro definitions in preamble |
| `Can be used only in preamble` | Move package loading to main.tex preamble |
| Build timeout | Large documents may need more time, check for infinite loops |

### Getting Help

1. **Check build report**: `make report`
2. **Review logs**: Check `*.log` files for detailed error information
3. **Clean and retry**: `make clean && make build`
4. **Use legacy tools**: `python3 ctmm_build.py` for simpler analysis

### Performance Tips

- Use `make test` for quick checks
- Run `make clean` regularly to remove artifacts
- Use incremental testing for large projects
- Monitor `build_manager.log` for performance insights

## Migration from Legacy System

If you're migrating from the older build system:

1. **Backup your work**: `git commit -am "backup before migration"`
2. **Run new system**: `make dev-setup`
3. **Compare results**: Check `build_report.md` vs. old output
4. **Update workflows**: Replace `ctmm_build.py` calls with `build_manager.py`

The new system is backward compatible and provides enhanced capabilities while maintaining the same core functionality.

---

**Need more help?** Check the project README.md or open an issue on GitHub.