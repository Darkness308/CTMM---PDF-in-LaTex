# CTMM Build System Guide

This comprehensive guide covers the CTMM LaTeX project's automated build management system, designed to ensure reliable builds, automatic template generation, and sophisticated error detection.

## Quick Start

### Prerequisites

**Required:**
- Python 3.6+ with `chardet` package
- LaTeX distribution (TeX Live, MiKTeX, or equivalent)
- Git (for version control)

**Installation:**
```bash
# Install Python dependencies
make deps
# or
pip install chardet

# Install LaTeX (system-specific)
make install-latex  # Shows installation instructions
```

### Basic Usage

**Development Workflow:**
```bash
# Complete development workflow (recommended)
make dev

# Or step-by-step:
make check      # Quick system check
make analyze    # Comprehensive analysis
make build      # Build development PDF
```

**CI/Production Workflow:**
```bash
# Complete CI workflow
make ci

# Or step-by-step:
make deps       # Install dependencies
make analyze    # Comprehensive analysis
make build-ci   # Build production PDF
```

## Build System Architecture

The CTMM build system consists of several components:

### Core Components

1. **`build_manager.py`** - Main comprehensive build management system
2. **`ctmm_build.py`** - Simplified quick-check system
3. **`build_system.py`** - Legacy detailed analysis system
4. **`main.tex`** - Development build target
5. **`main_final.tex`** - CI/production build target

### Build Targets

| Target | Purpose | Output | When to Use |
|--------|---------|--------|-------------|
| `main.tex` | Development builds | `main.pdf` | Local development, testing |
| `main_final.tex` | CI/Production builds | `main_final.pdf` | Release, CI/CD pipelines |

## Build Manager Features

### Automatic File Detection

The build manager scans `main.tex` for:
- `\usepackage{style/...}` commands → Style packages
- `\input{modules/...}` commands → Content modules

**Example Detection:**
```latex
% Detected automatically:
\usepackage{style/ctmm-design}     → style/ctmm-design.sty
\input{modules/depression}         → modules/depression.tex
```

### Template Generation

When missing files are detected, the system creates:

**Style Package Template:**
```latex
\NeedsTeXFormat{LaTeX2e}
\ProvidesPackage{package-name}[date Package Description - Template]
% TODO: Add package content
```

**Module Template:**
```latex
\section{Module Name}
\label{sec:module-name}
% TODO: Add actual module content
```

### Incremental Testing

The system tests modules incrementally to isolate build errors:

1. Test basic build (without modules)
2. Add modules one by one
3. Identify exact failure points
4. Generate detailed error reports

### Comprehensive Reporting

Generates `build_report.md` with:
- File analysis results
- Missing file status
- Build test outcomes
- Specific troubleshooting guidance
- Actionable recommendations

## Command Reference

### Make Targets

| Command | Description | Use Case |
|---------|-------------|----------|
| `make analyze` | **Recommended**: Complete analysis | Regular development |
| `make build` | Build development version | Create `main.pdf` |
| `make build-ci` | Build CI/production version | Create `main_final.pdf` |
| `make check` | Quick system check | Fast validation |
| `make test` | Status-only test | CI health checks |
| `make clean` | Remove build artifacts | Before committing |
| `make clean-all` | Remove all generated files | Fresh start |
| `make dev` | Complete development workflow | Full local workflow |
| `make ci` | Complete CI workflow | Automated builds |

### Python Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `build_manager.py` | Main system | `python3 build_manager.py [--verbose]` |
| `ctmm_build.py` | Quick check | `python3 ctmm_build.py` |
| `build_system.py` | Legacy analysis | `python3 build_system.py --verbose` |

## Development Workflow

### Adding New Modules

1. **Reference in main.tex:**
   ```latex
   \input{modules/my-new-module}
   ```

2. **Run analysis:**
   ```bash
   make analyze
   ```

3. **Complete generated template:**
   - Edit `modules/my-new-module.tex`
   - Follow TODO comments
   - Remove `TODO_my-new-module.md` when done

4. **Test integration:**
   ```bash
   make build
   ```

### Adding New Style Packages

1. **Reference in main.tex preamble:**
   ```latex
   \usepackage{style/my-new-package}
   ```

2. **Generate and complete template:**
   ```bash
   make analyze
   # Edit style/my-new-package.sty
   ```

3. **Test compilation:**
   ```bash
   make build
   ```

### Troubleshooting Builds

1. **Run comprehensive analysis:**
   ```bash
   make analyze
   ```

2. **Check build report:**
   ```bash
   cat build_report.md
   ```

3. **Review error logs:**
   ```bash
   ls build_error_*.log
   cat build_error_module-name.log
   ```

4. **Test incrementally:**
   - Comment out problematic modules in `main.tex`
   - Build successfully
   - Add modules back one by one

## CI/CD Integration

### GitHub Actions

The system integrates with GitHub Actions:

```yaml
- name: Run CTMM Build System Check
  run: python3 build_manager.py

- name: Build LaTeX PDF
  uses: dante-ev/latex-action@v2.0.0
  with:
    root_file: main_final.tex
```

### Build Artifacts

CI builds generate:
- `main_final.pdf` - Production PDF
- `build_report.md` - Analysis report
- Error logs (if any failures)

## File Structure

```
CTMM-System/
├── main.tex                    # Development build target
├── main_final.tex              # CI/production build target
├── build_manager.py            # Main build system
├── ctmm_build.py              # Quick check system
├── build_system.py            # Legacy analysis
├── Makefile                   # Build commands
├── BUILD_GUIDE.md             # This guide
├── style/                     # Style packages (.sty)
│   ├── ctmm-design.sty
│   ├── form-elements.sty
│   └── ctmm-diagrams.sty
├── modules/                   # Content modules (.tex)
│   ├── navigation-system.tex
│   ├── depression.tex
│   └── ...
└── build/                     # Build artifacts (generated)
    ├── build_report.md
    ├── build_manager.log
    └── build_error_*.log
```

## Error Handling

### Common Issues

**LaTeX Not Found:**
```
Error: pdflatex not found
Solution: Install LaTeX distribution (see make install-latex)
```

**Missing Packages:**
```
Error: Package 'example' not found
Solution: Add \usepackage{example} to main.tex preamble
```

**Undefined Commands:**
```
Error: Undefined control sequence \exampleCommand
Solution: Define command in style package or main.tex preamble
```

### Error Logs

The system generates detailed error logs:
- `build_manager.log` - General system log
- `build_error_module-name.log` - Module-specific errors
- Standard LaTeX `.log` files

## Advanced Usage

### Custom Build Targets

Create custom TeX files:
```bash
python3 build_manager.py --main-tex custom.tex
```

### Verbose Analysis

Enable detailed debugging:
```bash
python3 build_manager.py --verbose
make test-legacy  # Legacy verbose system
```

### Template Customization

Modify template generation in `build_manager.py`:
- `_generate_style_template()` - Style package templates
- `_generate_module_template()` - Module templates

## Best Practices

### Development

1. **Regular Analysis**: Run `make analyze` after file changes
2. **Incremental Testing**: Test new modules individually
3. **Clean Builds**: Use `make clean` before important builds
4. **Documentation**: Complete TODO files promptly

### CI/CD

1. **Use CI Target**: Always build `main_final.tex` in CI
2. **Artifact Collection**: Save build reports and error logs
3. **Dependency Caching**: Cache LaTeX and Python dependencies
4. **Timeout Handling**: Set appropriate build timeouts

### Project Maintenance

1. **Regular Updates**: Keep templates up to date
2. **Documentation Sync**: Update guides when adding features
3. **Error Monitoring**: Review error logs regularly
4. **Dependency Management**: Keep Python/LaTeX dependencies current

## Support and Troubleshooting

### Getting Help

1. **Build Report**: Check `build_report.md` for analysis
2. **Error Logs**: Review detailed error files
3. **Documentation**: Consult this guide and README.md
4. **Community**: Check project issues and discussions

### Reporting Issues

When reporting build system issues:

1. Include `build_report.md`
2. Attach relevant error logs
3. Specify LaTeX distribution and version
4. Include Python version and environment details
5. Provide minimal reproduction steps

---

**Version**: CTMM Build System v1.0  
**Last Updated**: 2024  
**Maintainers**: CTMM Team

For the latest updates and documentation, visit the project repository.