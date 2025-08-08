# CTMM LaTeX Framework - Copilot Instructions

## Repository Overview

This repository contains a German LaTeX framework for creating therapeutic materials using the **CTMM (Catch-Track-Map-Match) system**. It provides a modular architecture for developing interactive PDF therapy workbooks with forms, checkboxes, and specialized therapeutic content.

## Core Architecture

### Main Structure
- `main.tex` - Primary document that includes all modules and packages
- `modules/` - Individual therapy modules (14+ modules for different therapeutic areas)
- `style/` - Custom LaTeX packages for design, forms, and diagrams
- `build_system.py` & `ctmm_build.py` - Python build automation scripts
- `.github/workflows/` - CI/CD pipeline for automated builds

### Key Components
1. **Modular Therapy Content**: Depression monitoring, trigger management, binding dynamics, crisis cards
2. **Interactive Forms**: PDF form fields for therapeutic documentation using hyperref
3. **Custom Style System**: CTMM-specific design language with colors and layouts
4. **Automated Build System**: Python scripts for testing and template generation

## Development Guidelines

### LaTeX Best Practices for CTMM

#### Package Loading Rules
- **CRITICAL**: All `\usepackage{}` commands MUST be in the preamble of `main.tex` only
- Never load packages in modules or after `\begin{document}`
- Common error: `Can be used only in preamble` indicates package loaded in wrong location

#### Macro Definitions
- Define custom macros centrally in preamble or style files
- **Checkbox System**: Use `\checkbox` and `\checkedbox` macros only
- **Never use direct symbols**: Avoid `\Box`, `\blacksquare` directly in modules
- Example error: `Undefined control sequence` usually means missing macro definition

#### Module Development
```tex
% Correct module structure:
\section{Module Title}
\subsection{Content Section}

% Use predefined macros:
\checkbox Option 1 \\
\checkedbox Option 2 \\

% Use form elements:
\ctmmTextField[6cm]{Default text}{fieldname}
```

### Build System Usage

#### Primary Build Script
```bash
python3 ctmm_build.py
```
- Scans `main.tex` for all package and module references
- Creates templates for missing files automatically
- Tests builds incrementally to identify issues
- Generates TODO files for new templates

#### Advanced Analysis
```bash
python3 build_system.py --verbose
```
- Module-by-module testing
- Detailed error reporting
- Build operation logging

### Common Issues & Solutions

#### LaTeX Compilation Errors
1. **Package in wrong location**: Move to `main.tex` preamble
2. **Undefined control sequence**: Check macro definitions in style files
3. **Command already defined**: Remove duplicate definitions
4. **Missing files**: Run build system to auto-generate templates

#### Form Elements
- Use `\ctmmTextField`, `\ctmmCheckbox`, `\ctmmRadioButton` from `form-elements.sty`
- All form elements require unique field names
- Interactive features need hyperref package loaded

#### Module Integration
1. Add reference in `main.tex`: `\input{modules/new-module}`
2. Run build system to create template
3. Fill template following existing module patterns
4. Remove TODO file when complete

## File Naming Conventions

### Modules
- Use kebab-case: `arbeitsblatt-depression-monitoring.tex`
- Descriptive names in German for therapeutic content
- Include purpose: `bindungsleitfaden.tex`, `notfallkarten.tex`

### Style Files
- Use descriptive names: `ctmm-design.sty`, `form-elements.sty`
- Version comments in package headers
- Document required dependencies

## Therapeutic Context

### Target Conditions
- Depression & mood disorders
- Trigger management (trauma, PTSD)
- Attachment dynamics
- ADHD, ASD support materials
- Crisis intervention tools

### Content Guidelines
- German language for all therapeutic content
- Professional therapeutic terminology
- Interactive elements for patient engagement
- Clear structure for clinical use

## Testing & Quality Assurance

### Automated Testing
- GitHub Actions workflow builds PDF on every push
- Python build system validates all references
- Missing file detection and template generation

### Manual Testing
- Test form functionality in PDF viewers
- Validate therapeutic content accuracy
- Check accessibility of interactive elements

## Contribution Guidelines

### Adding New Modules
1. Plan content structure and required macros
2. Add input reference to `main.tex`
3. Run build system to generate template
4. Develop content following existing patterns
5. Test build and form functionality

### Updating Style System
- Document new macros in package headers
- Update this instruction file if adding new patterns
- Test compatibility with existing modules
- Consider backward compatibility

### Error Debugging
1. Check latest build system log: `build_system.log`
2. Use verbose mode for detailed analysis
3. Isolate problematic modules using incremental testing
4. Verify package loading order and locations

## Development Environment

### Recommended Setup
- LaTeX distribution with TikZ, hyperref, babel (German)
- Python 3.x with chardet package
- Git for version control
- PDF viewer supporting interactive forms

### GitHub Codespace
- Repository includes dev container configuration
- Pre-configured LaTeX environment
- All dependencies included

## Documentation Updates

When modifying the framework:
1. Update this instruction file for new patterns
2. Document breaking changes in README.md
3. Update package version numbers
4. Add examples for complex new features

Remember: This framework serves therapeutic professionals. Accuracy, reliability, and professional presentation are paramount.