# CTMM Build System Quick Start Guide

This guide provides comprehensive instructions for using the CTMM LaTeX automated build management system.

## Quick Start

### 1. Prerequisites

**LaTeX Installation:**
```bash
# Ubuntu/Debian
sudo apt-get install texlive-latex-base texlive-latex-extra texlive-fonts-recommended texlive-lang-german

# macOS (with Homebrew)
brew install --cask mactex

# Windows
# Download and install MiKTeX from https://miktex.org/
```

**Python Dependencies:**
```bash
pip install chardet
```

### 2. Basic Usage

**Run comprehensive build analysis:**
```bash
python3 build_manager.py
# or
make check
```

**Build the PDF:**
```bash
make build        # Builds main.tex
make build-ci     # Builds main_final.tex for CI
```

**Clean up:**
```bash
make clean        # Remove build artifacts
make clean-all    # Remove all generated files
```

## Build System Features

### Automated File Management

The build system automatically:
- Scans `main.tex` for all `\usepackage{style/...}` and `\input{modules/...}` references
- Detects missing files and creates minimal templates
- Generates TODO files with completion guidelines
- Provides comprehensive error reporting

### Template Generation

**Style Package Templates:**
```latex
\NeedsTeXFormat{LaTeX2e}
\ProvidesPackage{package-name}[date Package Description - Template]
% TODO: Add package content
```

**Module Templates:**
```latex
\section{Module Name}
\label{sec:module-name}
% TODO: Add actual module content
```

### Incremental Testing

The system tests modules incrementally to isolate build errors:
1. Tests basic build without modules
2. Gradually enables modules one by one
3. Identifies exactly which modules cause build failures
4. Generates detailed error reports

## Available Commands

### Make Targets

| Command | Description |
|---------|-------------|
| `make all` | Run check and build (default) |
| `make check` | Run build manager analysis |
| `make build` | Build main PDF (main.tex) |
| `make build-ci` | Build CI PDF (main_final.tex) |
| `make analyze` | Run comprehensive analysis |
| `make test` | Quick build system test |
| `make clean` | Remove build artifacts |
| `make clean-all` | Remove all generated files |
| `make deps` | Install Python dependencies |
| `make help` | Show help information |

### Build Manager Options

```bash
# Basic usage
python3 build_manager.py

# Verbose output
python3 build_manager.py --verbose

# Test specific file
python3 build_manager.py --test-file main_final.tex

# Use different main file
python3 build_manager.py --main-tex custom.tex
```

## Understanding Output

### Build Status Indicators

- ✓ **SUCCESS**: Operation completed successfully
- ✗ **FAILED**: Operation failed, check logs
- ⚠️ **WARNING**: Potential issue detected

### Generated Files

- `build_report.md`: Comprehensive analysis report
- `build_manager.log`: Detailed operation log
- `TODO_*.md`: Task lists for new template files
- `build_error_*.log`: Specific error logs for failed modules

### Report Sections

1. **Summary**: Overview of files and build status
2. **File Analysis**: Status of all style and module files
3. **Missing Files**: Templates created for missing files
4. **Problematic Modules**: Modules causing build failures
5. **Recommendations**: Actionable next steps

## Troubleshooting

### Common Issues

**LaTeX Package Missing:**
```
Error: Unknown option 'ngerman'
Solution: sudo apt-get install texlive-lang-german
```

**pdflatex Not Found:**
```
Error: pdflatex not found in PATH
Solution: Install full LaTeX distribution
```

**Module Build Failure:**
```
Error: Build failed when adding module
Solution: Check build_error_*.log for specific issues
```

### Debug Process

1. **Check installation:**
   ```bash
   python3 build_manager.py --verbose
   ```

2. **Review error logs:**
   ```bash
   cat build_error_modulename.log
   ```

3. **Test individual modules:**
   ```bash
   # Temporarily comment out problematic modules in main.tex
   # Then run build_manager.py again
   ```

4. **Clean and retry:**
   ```bash
   make clean-all
   python3 build_manager.py
   ```

## Development Workflow

### Adding New Modules

1. **Add reference in main.tex:**
   ```latex
   \input{modules/my-new-module}
   ```

2. **Run build system:**
   ```bash
   python3 build_manager.py
   ```

3. **Complete generated template:**
   - Edit `modules/my-new-module.tex`
   - Follow guidelines in `modules/TODO_my-new-module.md`
   - Remove TODO file when complete

### Adding New Style Packages

1. **Add reference in main.tex:**
   ```latex
   \usepackage{style/my-style}
   ```

2. **Run build system:**
   ```bash
   python3 build_manager.py
   ```

3. **Complete generated template:**
   - Edit `style/my-style.sty`
   - Add proper `\ProvidesPackage` declaration
   - Follow guidelines in `style/TODO_my-style.md`

## CI/CD Integration

### GitHub Actions

The system includes GitHub Actions integration:

```yaml
- name: Run CTMM Build System Check
  run: python3 build_manager.py

- name: Set up LaTeX
  uses: dante-ev/latex-action@v2.0.0
  with:
    root_file: main_final.tex
```

### CI Build Target

Use `main_final.tex` for CI builds:
- Identical content to `main.tex`
- Optimized for automated builds
- Consistent, reproducible results

## Best Practices

### File Organization

- Keep modules focused on single concepts
- Use semantic naming (e.g., `arbeitsblatt-trigger.tex`)
- Place style definitions in dedicated `.sty` files
- Maintain clean separation between content and styling

### Development Process

1. Run `make check` before making changes
2. Add new files through main.tex references
3. Let build system generate templates
4. Complete templates incrementally
5. Test builds frequently with `make build`
6. Clean up with `make clean` when needed

### Error Handling

- Always check `build_report.md` for comprehensive analysis
- Review specific error logs for detailed diagnostics
- Use incremental testing to isolate issues
- Keep builds clean and reproducible

## Getting Help

- **Quick help**: `make help`
- **Verbose output**: `python3 build_manager.py --verbose`
- **Comprehensive report**: Check `build_report.md`
- **Error details**: Review `build_error_*.log` files

The build system provides extensive logging and error reporting to help diagnose and resolve issues quickly.