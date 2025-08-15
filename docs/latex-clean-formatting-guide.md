# LaTeX Clean Formatting Guide for CTMM

## Overview

This guide demonstrates proper CTMM LaTeX formatting conventions versus over-escaped patterns that can result from conversion tools like Pandoc or other document converters.

## ✅ Proper CTMM LaTeX Formatting

### Sections and Structure
```latex
\section*{\textcolor{ctmmBlue}{\faIcon~Module Title}}
\label{sec:module-name}
\addcontentsline{toc}{section}{Module Title}

\subsection*{\textcolor{ctmmOrange}{Subsection Title}}
```

### CTMM Color Boxes
```latex
\begin{ctmmBlueBox}{Box Title}
Content goes here...
\end{ctmmBlueBox}

\begin{ctmmGreenBox}{Success Message}
Positive content and achievements
\end{ctmmGreenBox}

\begin{ctmmOrangeBox}{Warning or Process}
Process steps and important information
\end{ctmmOrangeBox}
```

### Form Elements
```latex
% Text fields
\ctmmTextField[6cm]{Default text}{field_name}

% Text areas
\ctmmTextArea[12cm]{3}{field_name}{Default text}

% Checkboxes
\ctmmCheckBox[field_name]{Label text}

% Radio buttons
\ctmmRadioButton{group_name}{value}{Label}
```

### Navigation and References
```latex
% Internal references
\ctmmRef{sec:target}{Link Text}

% Navigation hints
\textit{\textcolor{ctmmGreen}{\faChevronRight~Weiter zu} \ctmmRef{sec:next}{Next Module}}
```

### Table Formatting
```latex
\begin{tabularx}{\textwidth}{|X|c|c|X|}
\hline
\textbf{Category} & \textbf{Partner A} & \textbf{Partner B} & \textbf{Notes} \\
\hline
Content & \ctmmTextField[2cm]{}{field_a} & \ctmmTextField[2cm]{}{field_b} & \ctmmTextField[4cm]{}{notes} \\
\hline
\end{tabularx}
```

## ❌ Over-Escaped Patterns to Avoid

### Complex Section Headers
```latex
% AVOID - Over-escaped from conversion tools
\hypertarget{section-1}{%
\section{\texorpdfstring{\textbf{OVER-COMPLEX}}{OVER-COMPLEX}\label{section-1}}

% USE INSTEAD - Clean CTMM format
\section*{\textcolor{ctmmBlue}{\faIcon~Clean Title}}
\label{sec:clean-title}
```

### Excessive Backslash Escaping
```latex
% AVOID - Double escaped ampersands
Text with \textbackslash{}\textbackslash{}& double escaping

% USE INSTEAD - Proper ampersand handling
Text with proper \& ampersand usage
```

### Auto-Generated Labels
```latex
% AVOID - Generic auto-generated labels
\label{section-1}
\label{subsection-2-1}

% USE INSTEAD - Semantic labels
\label{sec:trigger-management}
\label{sec:matching-matrix}
```

### Excessive texorpdfstring Usage
```latex
% AVOID - Unnecessary PDF string conversion
\section{\texorpdfstring{Simple Title}{Simple Title}}

% USE INSTEAD - Direct title usage
\section*{\textcolor{ctmmBlue}{Simple Title}}
```

## Best Practices for CTMM Modules

### 1. Module Structure Template
```latex
% Module Header
\newpage
\section*{\textcolor{ctmmBlue}{\faIcon~Module Name}}
\label{sec:module-name}
\addcontentsline{toc}{section}{Module Name}

% Introduction Quote
\begin{quote}
\textit{\textcolor{ctmmBlue}{Inspirational quote about the module topic.}}\\
\textbf{\textcolor{ctmmBlue}{What is this module about?}}\\
Brief description of the module's purpose and therapeutic goals.
\end{quote}

% Content sections with subsections
\subsection*{\textcolor{ctmmOrange}{Section Title}}

\begin{ctmmBlueBox}{Interactive Work Area}
Form elements and interactive content
\end{ctmmBlueBox}

% Navigation footer
\vspace{1cm}
\begin{center}
\textit{\textcolor{ctmmGreen}{\faChevronRight~Weiter zu} \ctmmRef{sec:next}{Next Module}}
\end{center}
```

### 2. Color Usage Guidelines
- **ctmmBlue**: Headers, primary content, information boxes
- **ctmmGreen**: Success messages, positive reinforcement, navigation forward
- **ctmmOrange**: Process steps, warnings, active work areas
- **ctmmRed**: Emergency content, critical information
- **ctmmPurple**: Worksheets, reflection areas
- **ctmmYellow**: Highlights, tips, support information

### 3. Form Field Naming Convention
```latex
% Use descriptive, consistent naming
trigger_situation    % For trigger description fields
matrix_trigger_01     % For matrix input fields
weekly_reflection     % For weekly review areas
partner_a_goals      % For partner-specific content
```

### 4. Validation and Cleaning

Before committing LaTeX files, always:

1. **Run the LaTeX validator**:
   ```bash
   python3 latex_validator.py path/to/file.tex
   ```

2. **Use the build system**:
   ```bash
   python3 ctmm_build.py
   ```

3. **Check for escaping patterns**:
   - No `\textbackslash{}` sequences
   - No auto-generated labels like `section-1`
   - No excessive `\texorpdfstring` usage
   - No double-escaped ampersands `\\&`

### 5. Module Integration

When adding a new module:

1. **Add to main.tex**:
   ```latex
   \input{modules/module-name}
   ```

2. **Follow naming convention**: Use hyphens, not underscores or spaces
3. **Test build**: Ensure the module compiles without errors
4. **Check navigation**: Verify internal references work correctly

## Tools and Automation

The CTMM repository includes several tools to maintain clean formatting:

- **`latex_validator.py`**: Detects and fixes over-escaped patterns
- **`ctmm_build.py`**: Tests compilation and generates missing templates
- **GitHub Actions**: Automated validation on pull requests

## Common Issues and Solutions

### Issue: "Undefined control sequence" errors
**Solution**: Ensure all custom macros are defined in style files, not in modules

### Issue: Checkbox symbols not displaying
**Solution**: Use `\ctmmCheckBox` macro instead of raw `$\square$` symbols

### Issue: Interactive forms not working
**Solution**: Verify hyperref package is loaded and form field names are unique

### Issue: Color not displaying
**Solution**: Check that color names use proper CTMM color definitions

## Conclusion

Following these formatting guidelines ensures:
- Consistent visual appearance across all CTMM modules
- Proper functionality of interactive PDF forms
- Maintainable and readable LaTeX source code
- Compatibility with the CTMM build system

When in doubt, refer to existing modules like `triggermanagement.tex` or `interactive.tex` as examples of proper CTMM formatting.