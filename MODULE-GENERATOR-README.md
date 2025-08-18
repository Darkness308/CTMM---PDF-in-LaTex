# CTMM Module Generator - Comprehensive Documentation

## Overview

The CTMM Module Generator is a comprehensive system for creating standardized therapeutic materials for the CTMM (Catch-Track-Map-Match) therapeutic approach. It generates LaTeX-based modules specifically designed for German-speaking neurodiverse couples therapy.

## System Components

### 1. Core Generator (`module-generator.js`)
JavaScript-based template engine that creates three types of therapeutic modules:

- **Arbeitsblatt (Worksheets)**: Interactive forms for structured self-reflection
- **Tool (Therapeutic Tools)**: Immediate intervention techniques  
- **Notfallkarte (Emergency Cards)**: Crisis intervention protocols

### 2. Interactive Shell Script (`create-module.sh`)
User-friendly interface providing:
- Cross-platform compatibility (Linux, macOS, Windows with WSL)
- Interactive module creation workflow
- Quick command-line module generation
- Build system validation
- Module listing and management

### 3. Generated Module Examples
Demonstration modules showcasing the generator's capabilities:
- `tool-5-4-3-2-1-grounding.tex` - Grounding techniques for anxiety
- `notfall-panikattacken.tex` - Panic attack emergency protocols
- `arbeitsblatt-taeglicher-stimmungscheck.tex` - Daily mood tracking worksheet

## Installation and Setup

### Prerequisites
- **Node.js** (v12 or higher) - for module generation
- **Python 3** - for CTMM build system integration
- **LaTeX distribution** (optional) - for PDF compilation
- **Bash shell** - for interactive script (available on Linux/macOS/WSL)

### Quick Start
```bash
# Clone and navigate to CTMM repository
cd CTMM---PDF-in-LaTex

# Make script executable
chmod +x create-module.sh

# Start interactive module creation
./create-module.sh
```

## Usage Guide

### Interactive Mode (Recommended)
```bash
./create-module.sh
```
Follow the prompts to:
1. Select module type (arbeitsblatt/tool/notfallkarte)
2. Enter module title and description
3. Specify filename
4. Automatically generate and integrate module

### Quick Command Line Mode
```bash
# Create a therapeutic tool
./create-module.sh --quick tool "Atemtechnik" "atemtechnik.tex"

# Create an emergency card
./create-module.sh --quick notfallkarte "Dissoziation" "notfall-dissoziation.tex"

# Create a worksheet
./create-module.sh --quick arbeitsblatt "Kommunikation" "arbeitsblatt-kommunikation.tex"
```

### Direct JavaScript Usage
```bash
# Interactive mode
node module-generator.js

# Command line mode  
node module-generator.js <type> <title> <filename> [description]
```

## Module Templates

### Arbeitsblatt (Worksheet) Structure
Generated worksheets include:
- **Therapeutic Instructions**: Guidance for therapy professionals
- **CTMM Methodology Integration**: Catch-Track-Map-Match structure
- **Interactive Forms**: Text fields, checkboxes, text areas
- **Couple Reflection Sections**: Joint processing activities
- **Therapeutic Notes Area**: Professional observation space
- **Navigation Links**: Connections to related modules

### Tool (Therapeutic Tool) Structure
Generated tools feature:
- **Immediate Application**: Step-by-step crisis intervention
- **CTMM Integration**: Four-phase therapeutic approach
- **Quick Reference Cards**: Printable emergency guides
- **Partner Support Instructions**: Guidance for non-affected partner
- **Customization Options**: Personalization for individual needs
- **Cross-references**: Links to related therapeutic resources

### Notfallkarte (Emergency Card) Structure  
Generated emergency cards provide:
- **Crisis Protocols**: Immediate safety and intervention steps
- **Escalation Management**: Structured response phases
- **Contact Information**: Emergency numbers and resources
- **Grounding Techniques**: Rapid stabilization methods
- **Prevention Planning**: Long-term crisis prevention strategies
- **Documentation Areas**: Incident tracking and analysis

## CTMM Design System Integration

### Color Scheme
All generated modules use the standardized CTMM color palette:
- **ctmmBlue (#003087)**: Primary structural elements
- **ctmmOrange (#FF6200)**: Highlights and active elements
- **ctmmGreen (#4CAF50)**: Positive actions and confirmations
- **ctmmPurple (#7B1FA2)**: Special sections and advanced content
- **ctmmRed (#D32F2F)**: Warnings and emergency information
- **ctmmYellow (#FFC107)**: Attention and emphasis

### Interactive Elements
Standardized form components:
- `\ctmmCheckBox[name]{label}` - Checkbox inputs
- `\ctmmTextField[width]{label}{name}` - Single-line text fields
- `\ctmmTextArea[width]{lines}{label}{name}` - Multi-line text areas
- `\ctmmRadioButton{group}{value}{label}` - Radio button selections

### Layout Components
Consistent structural elements:
- `\begin{ctmmBlueBox}{title}` - Information containers
- `\begin{ctmmGreenBox}{title}` - Positive action sections
- `\begin{ctmmRedBox}{title}` - Emergency/warning sections
- Navigation with `\faCompass` icons and cross-references

## Integration with CTMM Build System

### Automatic Detection
The CTMM build system (`ctmm_build.py`) automatically:
- Scans `main.tex` for new module references
- Validates generated LaTeX syntax
- Creates build reports including new modules
- Integrates with existing validation pipeline

### Manual Integration Steps
1. **Generate Module**: Use module generator to create new `.tex` file
2. **Add Reference**: Include `\input{modules/filename}` in `main.tex`
3. **Validate Build**: Run `python3 ctmm_build.py` to verify integration
4. **Test Compilation**: Use `make build` for full PDF generation

### Build Validation
```bash
# Quick validation
python3 ctmm_build.py

# Comprehensive testing
./create-module.sh --validate

# Manual LaTeX compilation
make build
```

## Customization and Extension

### Template Modification
Module templates can be customized by editing `module-generator.js`:

1. **Content Sections**: Modify template strings for each module type
2. **Color Schemes**: Adjust CTMM_COLORS constants
3. **Form Elements**: Add new interactive components
4. **Language Localization**: Translate German text for other languages

### Adding New Module Types
To add new therapeutic module types:

1. **Define Template**: Create new generation function in `CTMMModuleGenerator` class
2. **Update Interface**: Add type to `moduleTypes` object
3. **Add Validation**: Include type checking in shell script
4. **Test Integration**: Verify with CTMM build system

### Therapeutic Content Guidelines
When customizing modules, maintain:
- **Professional Standards**: Evidence-based therapeutic approaches
- **Cultural Sensitivity**: Appropriate for German-speaking therapy contexts
- **Accessibility**: Clear language for neurodiverse individuals
- **Safety Focus**: Risk-aware content for mental health contexts

## Troubleshooting

### Common Issues

**Node.js Not Found**
```bash
# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs
```

**Permission Denied**
```bash
# Make script executable
chmod +x create-module.sh
```

**Module Not Appearing in Build**
1. Verify `\input{modules/filename}` in `main.tex`
2. Check file exists in `modules/` directory  
3. Run `python3 ctmm_build.py` for validation
4. Review build logs for errors

**LaTeX Compilation Errors**
1. Check generated LaTeX syntax
2. Verify CTMM style files are available
3. Ensure all required packages are installed
4. Review compilation logs for specific errors

### Build System Integration Issues

**Module Not Detected**
- Ensure filename follows convention: `*.tex`
- Verify placement in `modules/` directory
- Check `main.tex` includes correct `\input{}` statement

**Style Package Errors**
- Confirm all CTMM style packages are available in `style/`
- Verify `\usepackage{}` statements in `main.tex` preamble
- Check for conflicting package definitions

## Development and Contribution

### Code Structure
```
module-generator.js          # Core generation logic
create-module.sh            # Interactive shell interface
modules/                    # Generated module files
  ├── tool-*.tex           # Therapeutic tools
  ├── arbeitsblatt-*.tex   # Worksheets
  └── notfall-*.tex        # Emergency cards
```

### Testing New Features
1. **Unit Testing**: Test individual generator functions
2. **Integration Testing**: Verify CTMM build system compatibility
3. **Content Review**: Validate therapeutic content accuracy
4. **Cross-platform Testing**: Verify shell script compatibility

### Contributing Guidelines
- Follow existing code style and structure
- Maintain therapeutic content accuracy and sensitivity
- Test all changes with CTMM build system
- Update documentation for new features
- Consider accessibility and neurodiverse user needs

## Support and Resources

### Documentation
- `BUILD-TASKS-EVALUATION.md` - Build system optimization
- `GITHUB-PERMISSIONS.md` - CI/CD and automation setup
- `ISSUE_898_RESOLUTION.md` - Implementation details and rationale

### Community Resources
- CTMM methodology documentation
- German language therapy material standards
- LaTeX best practices for therapeutic documents
- Neurodiverse couples therapy research and guidelines

### Professional Support
This tool is designed for use by qualified therapy professionals. Always ensure:
- Proper therapeutic training before using generated materials
- Cultural and clinical appropriateness for specific contexts
- Ethical guidelines compliance for therapy documentation
- Regular supervision and quality assurance processes

---

**Version**: 1.0.0  
**Last Updated**: 2024  
**Compatibility**: CTMM Build System 2.x, Node.js 12+, LaTeX 2020+