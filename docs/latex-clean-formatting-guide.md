# CTMM LaTeX Clean Formatting Guide

## Overview

This guide provides best practices for maintaining clean, professional LaTeX formatting in the CTMM system, focusing on avoiding over-escaped patterns often introduced by conversion tools.

## Clean CTMM LaTeX Patterns vs Over-Escaped Patterns

### ✅ Proper CTMM Formatting

#### Color Usage
```latex
% GOOD: Clean CTMM color usage
\textcolor{ctmmBlue}{Text content}
\textcolor{ctmmOrange}{Highlight text}
\textcolor{ctmmPurple}{\faPuzzlePiece~Section Title}
```

#### Form Elements
```latex
% GOOD: Clean CTMM form elements
\ctmmTextArea[12cm]{3}{field_name}
\ctmmCheckBox{field_name}{Label text}
\ctmmTextField[6cm]{}{field_name}
```

#### Section Headers
```latex
% GOOD: Clean section formatting
\section*{\textcolor{ctmmPurple}{\faPuzzlePiece~Matching-Matrix}}
\subsection*{\textcolor{ctmmBlue}{Interactive Section}}
```

#### Boxes and Containers
```latex
% GOOD: Clean tcolorbox usage
\begin{tcolorbox}[colback=ctmmGreen!5!white,colframe=ctmmGreen,title=Usage Notes]
Content here
\end{tcolorbox}

\begin{ctmmBlueBox}{Box Title}
Content here
\end{ctmmBlueBox}
```

### ❌ Over-Escaped Patterns to Avoid

#### Excessive Backslash Escaping
```latex
% BAD: Over-escaped from conversion tools
\textbackslash{}textcolor\{ctmmBlue\}\{Text\}
\textbackslash{}begin\{itemize\}

% GOOD: Clean LaTeX commands
\textcolor{ctmmBlue}{Text}
\begin{itemize}
```

#### Unicode and Special Characters
```latex
% BAD: Escaped unicode
\textbackslash{}faCompass\textasciitilde{}
\textbackslash{}u\{1F9E9\}

% GOOD: Direct FontAwesome and unicode
\faCompass~
🧩
```

#### Table Formatting
```latex
% BAD: Over-escaped table separators
\textbackslash{}\textbackslash{}
\textbackslash{}hline

% GOOD: Clean table syntax
\\
\hline
```

## CTMM Design System Compliance

### Required Color Scheme
- `ctmmBlue` - Primary structural elements
- `ctmmOrange` - Accent and highlights  
- `ctmmGreen` - Positive elements and forms
- `ctmmPurple` - Special sections and tools
- `ctmmRed` - Warnings and critical items
- `ctmmGray` - Secondary text
- `ctmmYellow` - Emphasis elements

### Interactive Form Standards
All interactive elements must use CTMM form macros:
- Use `\ctmmTextArea[width]{lines}{name}` for multi-line input
- Use `\ctmmTextField[width]{label}{name}` for single-line input
- Use `\ctmmCheckBox{name}{label}` for checkboxes
- Use `\ctmmRadioButton{group}{value}{label}` for radio buttons

### Typography Guidelines
- Section headers should use CTMM colors with FontAwesome icons
- Use proper German typography conventions
- Maintain consistent spacing and structure
- Follow semantic markup principles

## Validation Tools

### Build System Validation
The CTMM build system (`ctmm_build.py`) automatically checks for:
- Over-escaping patterns
- Proper form element usage
- Color scheme compliance
- LaTeX syntax validation

### Manual Validation Checklist
- [ ] No `\textbackslash{}` patterns in source
- [ ] Proper CTMM color usage throughout
- [ ] Interactive forms use CTMM macros only
- [ ] FontAwesome icons display correctly
- [ ] German text renders properly
- [ ] Table formatting is clean and readable

## Common Conversion Issues

### Pandoc Conversion
When converting from other formats, watch for:
- Excessive backslash escaping
- Unicode character corruption
- Broken table structures
- Missing color formatting

### Microsoft Word to LaTeX
Common issues include:
- Lost formatting in complex tables
- Incorrect list structures
- Missing interactive elements
- Broken special characters

## Best Practices

1. **Always validate with build system** after making changes
2. **Use CTMM templates** for new modules
3. **Test interactive elements** in PDF output
4. **Review for therapeutic accuracy** and sensitivity
5. **Maintain German language conventions** throughout
6. **Follow existing module patterns** for consistency

## Integration with CTMM System

This formatting guide ensures that all modules integrate properly with:
- Main document structure in `main.tex`
- CTMM style files in `style/` directory
- Build system validation in `ctmm_build.py`
- Interactive PDF generation workflow
- Therapeutic content standards

## Troubleshooting

### Common Build Errors
- **Over-escaping detected**: Run `python3 fix_latex_escaping.py`
- **Form element errors**: Check macro usage against CTMM standards
- **Color issues**: Verify `style/ctmm-design.sty` is loaded
- **Font problems**: Ensure FontAwesome5 package is available

### Validation Commands
```bash
# Check current formatting
python3 ctmm_build.py

# Fix escaping issues
python3 fix_latex_escaping.py

# Validate specific file
python3 latex_validator.py modules/filename.tex
```

---

This guide ensures professional, therapeutic-grade LaTeX documents that maintain the CTMM system's design integrity and interactive functionality.