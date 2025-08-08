# CONTRIBUTING.md

## Contributing to CTMM LaTeX System

Thank you for your interest in contributing to the CTMM (Catch-Track-Map-Match) therapy materials system!

## Quick Start for Developers

### Prerequisites
- LaTeX distribution (TeX Live, MiKTeX, or similar)
- Python 3.x for build tools
- Basic understanding of LaTeX and modular document structure

### Development Workflow

1. **Clone and setup**:
   ```bash
   git clone https://github.com/Darkness308/CTMM---PDF-in-LaTex.git
   cd CTMM---PDF-in-LaTex
   ```

2. **Test current build**:
   ```bash
   python3 ctmm_build.py
   ```

3. **Make changes** following the guidelines in `.github/copilot-instructions.md`

4. **Test your changes**:
   ```bash
   python3 ctmm_build.py  # Quick test
   python3 build_system.py --verbose  # Detailed analysis
   ```

### File Organization Rules

| File Type | Location | Purpose | Rules |
|-----------|----------|---------|-------|
| **Main Document** | `main.tex` | Entry point, preamble | All `\usepackage{}` commands go here |
| **Style Files** | `style/*.sty` | Reusable formatting | Define macros, colors, layouts |
| **Modules** | `modules/*.tex` | Individual therapy content | Use predefined macros only |
| **Build Tools** | `*.py` | Automation and testing | Keep Python 3 compatible |

### Adding New Therapy Modules

1. **Add reference in main.tex**:
   ```tex
   \input{modules/your-new-module}
   ```

2. **Run build system** to generate template:
   ```bash
   python3 ctmm_build.py
   ```
   This creates:
   - `modules/your-new-module.tex` (basic template)
   - `modules/TODO_your-new-module.md` (completion checklist)

3. **Follow the module template**:
   ```tex
   \section{Your Module Title}
   
   \begin{ctmmBlueBox}{Purpose}
   Brief description of what this module covers.
   \end{ctmmBlueBox}
   
   % Use only predefined macros:
   % \checkbox, \checkedbox, \textfield{}, etc.
   ```

4. **Remove TODO file** when module is complete

### Style and Design Guidelines

#### Colors
Use the predefined CTMM color scheme:
- `ctmmBlue` - Primary headings, navigation
- `ctmmGreen` - Success, positive actions  
- `ctmmOrange` - Warnings, attention items
- `ctmmPurple` - Special emphasis, highlights

#### Interactive Elements
```tex
% Checkboxes
\checkbox \text{Unchecked option}
\checkedbox \text{Checked option}

% Text input fields
\textfield{3cm}  % 3cm wide underlined space
\largertextfield{5cm}{2cm}  % 5cm x 2cm text area

% Rating scales
\ratingScale{5}  % 1-5 numbered scale
```

#### Content Boxes
```tex
\begin{ctmmBlueBox}{Title}
Important information or instructions
\end{ctmmBlueBox}

\begin{ctmmGreenBox}{Success Tip}
Positive reinforcement or success strategies
\end{ctmmGreenBox}
```

### Common Mistakes to Avoid

❌ **Don't do this**:
```tex
% In modules - WRONG
\usepackage{tikz}  % Packages only in main.tex preamble
\newcommand{\mybox}{...}  % Macro definitions only in style files
\Box  % Use \checkbox macro instead
```

✅ **Do this instead**:
```tex
% In modules - CORRECT
\checkbox  % Use predefined macros
\textcolor{ctmmBlue}{...}  % Use predefined colors
\section{...}  % Standard LaTeX structure
```

### Testing Your Changes

#### Local Testing
```bash
# Quick build validation
python3 ctmm_build.py

# Comprehensive testing
python3 build_system.py --verbose

# Check specific module
python3 build_system.py --module your-module-name
```

#### PDF Verification
1. Compile `main.tex` to PDF
2. Open PDF in a reader
3. Test interactive elements (checkboxes, text fields)
4. Verify hyperlinks work correctly

### Code Review Guidelines

When submitting PRs:

1. **Include testing evidence**: Screenshots of PDF output if relevant
2. **Follow modular principles**: Don't break the module system
3. **Test build system**: Ensure `ctmm_build.py` passes
4. **Document new features**: Update this guide if adding new macros/colors
5. **Consider therapy context**: Ensure content is clinically appropriate

### Therapeutic Content Standards

This system serves real therapeutic needs:

- **Clinical accuracy**: Verify therapy techniques are evidence-based
- **Inclusive language**: Use person-first, non-stigmatizing terms
- **Accessibility**: Content should be readable at 8th-grade level
- **Cultural sensitivity**: Avoid assumptions about family/relationship structures
- **Trauma-informed**: Avoid potentially triggering language or scenarios

### Getting Help

- **Build issues**: Check the logs from `python3 build_system.py --verbose`
- **LaTeX errors**: Review the guidelines in `.github/copilot-instructions.md`
- **Content questions**: Open an issue for discussion
- **Technical problems**: Include your Python/LaTeX versions and error messages

### Maintainer Notes

For repository maintainers:

- Keep `.github/copilot-instructions.md` updated with new patterns
- Document new macros and their usage
- Test major changes across all modules
- Maintain backward compatibility when possible
- Consider impact on existing therapy workflows

---

Thank you for contributing to accessible, evidence-based therapy resources! 🧠💙