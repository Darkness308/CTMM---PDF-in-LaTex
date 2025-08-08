# Copilot Instructions for CTMM-System

## Repository Overview

This is a German LaTeX framework for creating therapeutic materials using the **CTMM (Catch-Track-Map-Match)** system. The repository generates interactive PDF documents for therapeutic use, particularly for depression, trigger management, attachment dynamics, and other therapeutic interventions.

## Key Technologies & Architecture

### LaTeX-Based Modular System
- **Main Document**: `main.tex` - Entry point that includes all modules
- **Style Package**: Custom LaTeX packages in `style/` directory
  - `ctmm-design.sty` - Visual design and colors
  - `form-elements.sty` - Interactive form elements (checkboxes, text fields)
  - `ctmm-diagrams.sty` - Therapeutic diagrams and visual elements
- **Modules**: Individual therapy components in `modules/` directory
- **Build System**: Python-based automation (`ctmm_build.py`, `build_system.py`)

### Build & Testing Infrastructure
- **Makefile**: Standard build commands (`make build`, `make check`, `make clean`)
- **GitHub Actions**: Automated LaTeX compilation and PDF generation
- **Python Build System**: Automatic dependency checking and template creation

## Development Guidelines

### LaTeX Best Practices for CTMM

#### Package Management
```latex
% ✅ CORRECT: Load packages ONLY in main.tex preamble
\usepackage{style/ctmm-design}
\usepackage{style/form-elements}

% ❌ INCORRECT: Never load packages in modules
% This will cause "Can be used only in preamble" errors
```

#### Form Elements & Macros
```latex
% ✅ CORRECT: Use predefined macros for consistency
\checkbox      % Empty checkbox
\checkedbox    % Filled checkbox
\textfield{width}{label}  % Interactive text field

% ❌ INCORRECT: Never use direct symbols
% \Box or \blacksquare will cause "Undefined control sequence" errors
```

#### Module Structure
```latex
% ✅ CORRECT module structure
\section{Module Title}
\subsection{Subsection}

Content using predefined macros and commands only.
% No \usepackage commands
% No \newcommand definitions
% Only content and predefined elements
```

### File Organization

#### Adding New Modules
1. **Reference in main.tex**: Add `\input{modules/new-module-name}`
2. **Run build system**: `python3 ctmm_build.py` creates template automatically
3. **Complete template**: Fill in content, remove TODO file when done
4. **Test build**: Use `make check` to verify compilation

#### Style Development
- Modify existing `.sty` files in `style/` directory
- Test changes with `make build`
- Document new macros in README.md

### Common Issues & Solutions

#### Build Errors
- **"Can be used only in preamble"**: Package loaded in wrong location → Move to main.tex preamble
- **"Undefined control sequence"**: Macro not defined → Check if macro exists in style files
- **"Command already defined"**: Duplicate macro definition → Remove duplicate, keep central definition

#### Development Workflow
```bash
# 1. Check current state
make check

# 2. Add new module reference to main.tex
# 3. Auto-generate template
python3 ctmm_build.py

# 4. Develop content in generated template
# 5. Test build
make build

# 6. Clean up when done
make clean
```

## Therapeutic Context

### Content Guidelines
- **Language**: German (primary language for all content)
- **Target Audience**: Mental health professionals and patients
- **Therapeutic Approaches**: 
  - Depression and mood monitoring
  - Trigger management (PTSD, trauma)
  - Attachment dynamics
  - Crisis intervention materials
  - Interactive therapeutic exercises

### Module Types
- **Arbeitsblätter** (Worksheets): Interactive forms for patient work
- **Monitoring**: Progress tracking and assessment tools
- **Leitfäden** (Guidelines): Professional guidance documents
- **Interaktive Elemente**: QR codes, hyperlinks, fillable forms

## Code Quality & Standards

### LaTeX Code Style
- Use semantic commands over direct formatting
- Maintain consistent indentation (2 spaces)
- Comment complex TikZ diagrams
- Use German comments for therapeutic content

### Python Build System
- Follow existing logging patterns in `ctmm_build.py`
- Use type hints for new functions
- Maintain compatibility with existing workflow

### Git Workflow
- Use descriptive German commit messages for content changes
- Use English for technical/build system changes
- Test builds before committing with `make check`

## Testing & Validation

### Pre-commit Checks
```bash
# Always run before committing
make check          # Verify build system
make build         # Test PDF generation
make clean         # Remove artifacts
```

### Module Testing
```bash
# Detailed module analysis
python3 build_system.py --verbose
```

### CI/CD Integration
- GitHub Actions automatically builds PDF on push
- Artifacts available as GitHub Actions downloads
- Build logs help identify issues

## Dependencies

### Required Software
- **LaTeX Distribution**: TeX Live or MiKTeX with packages:
  - TikZ (diagrams)
  - hyperref (interactive elements)
  - tcolorbox (styled containers)
  - fontawesome5 (icons)
  - xcolor (colors)
- **Python 3**: For build system (chardet package)

### Installation
```bash
# Install Python dependencies
make deps

# LaTeX packages via system package manager
# Ubuntu/Debian: apt install texlive-full
# macOS: brew install mactex
```

## Troubleshooting Guide

### Common LaTeX Errors
1. **Missing file errors**: Run `python3 ctmm_build.py` to auto-generate templates
2. **Package conflicts**: Check package loading order in main.tex
3. **Encoding issues**: Ensure UTF-8 encoding for German characters
4. **Form elements not working**: Verify PDF viewer supports interactive forms

### Build System Issues
- Check `build_system.log` for detailed error information
- Use `--verbose` flag for extended debugging
- Verify file permissions for Python scripts

### PDF Generation Problems
- Ensure all referenced files exist
- Check for circular dependencies between modules
- Verify image files are in correct format (PNG, JPG, PDF)

## Contributing

### Adding New Therapeutic Modules
1. Identify therapeutic goal and target audience
2. Design module structure with appropriate LaTeX elements
3. Use existing form elements and design patterns
4. Test with real therapeutic scenarios when possible
5. Document new patterns in this file

### Extending Build System
- Maintain backward compatibility
- Add logging for new features
- Update Makefile targets as needed
- Test with various module combinations

### Documentation
- Update README.md for user-facing changes
- Update this file for developer guidelines
- Use German for therapeutic content documentation
- Use English for technical documentation

## Resources

### LaTeX References
- [TikZ Documentation](https://tikz.dev/) - For diagrams and visual elements
- [hyperref Manual](https://ctan.org/pkg/hyperref) - For interactive forms
- [tcolorbox Documentation](https://ctan.org/pkg/tcolorbox) - For styled containers

### Therapeutic Material Guidelines
- Follow evidence-based therapeutic principles
- Ensure accessibility and usability for diverse populations
- Consider cultural sensitivity in German-speaking contexts
- Validate content with mental health professionals when possible