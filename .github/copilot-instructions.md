# Copilot Instructions for CTMM LaTeX System

## Project Overview

This is a **modular LaTeX framework** for creating **CTMM (Catch-Track-Map-Match) therapy materials**. The system generates interactive PDF workbooks for neurodiverse couples and individuals dealing with trauma, ADHD, autism, and borderline personality disorders.

### Key Concepts
- **CTMM**: Catch-Track-Map-Match methodology for trigger management
- **Modular Design**: Separate `.tex` files for each therapy module
- **Interactive Forms**: PDF forms with fillable fields and checkboxes
- **Automated Build System**: Python scripts handle missing files and build validation

## Repository Structure

```
├── main.tex                 # Main document (entry point)
├── ctmm_build.py           # Simplified build system
├── build_system.py         # Advanced build analysis tool
├── style/                  # LaTeX style packages
│   ├── ctmm-design.sty    # Colors, boxes, and visual design
│   ├── form-elements.sty  # Interactive form components
│   └── ctmm-diagrams.sty  # TikZ diagrams and charts
├── modules/                # Individual therapy modules
│   ├── depression.tex
│   ├── triggermanagement.tex
│   ├── bindungsleitfaden.tex
│   └── arbeitsblatt-*.tex  # Interactive worksheets
└── .github/workflows/      # CI/CD for PDF generation
```

## Development Guidelines

### 1. LaTeX Package Management Rules

**CRITICAL**: All `\usepackage{}` commands MUST be in the preamble of `main.tex` ONLY.

✅ **Correct** (in main.tex preamble):
```tex
\usepackage{amssymb}
\usepackage{tikz}
\usepackage{hyperref}
```

❌ **Wrong** (anywhere else):
```tex
% NEVER in modules or after \begin{document}
\usepackage{something}
```

### 2. Macro Definitions

Define reusable macros in the preamble or style files, NOT in individual modules.

✅ **Correct** (in preamble or .sty file):
```tex
\newcommand{\checkbox}{$\square$}
\newcommand{\checkedbox}{$\blacksquare$}
\newcommand{\textfield}[1]{\underline{\hspace{#1}}}
```

❌ **Wrong** (in modules):
```tex
\newcommand{\checkbox}{$\square$}  % Don't define in modules
```

### 3. Interactive Form Elements

Use the predefined macros from `style/form-elements.sty`:

```tex
% Checkboxes
\checkbox \text{Option 1}
\checkedbox \text{Selected option}

% Text fields
\textfield{3cm} % Creates 3cm underlined space
\largertextfield{5cm}{2cm} % Width x Height

% Rating scales
\ratingScale{5} % Creates 1-5 scale with circles
```

### 4. Color System

The CTMM color palette is defined in `style/ctmm-design.sty`:

```tex
% Use these predefined colors:
\textcolor{ctmmBlue}{Text}
\textcolor{ctmmGreen}{Text}
\textcolor{ctmmOrange}{Text}
\textcolor{ctmmPurple}{Text}

% Colored boxes:
\begin{ctmmBlueBox}{Title}
Content here
\end{ctmmBlueBox}
```

### 5. Module Development

When creating new modules:

1. **Reference in main.tex**:
   ```tex
   \input{modules/new-module-name}
   ```

2. **Run build system** to generate template:
   ```bash
   python3 ctmm_build.py
   ```

3. **Module structure** should be:
   ```tex
   \section{Module Title}
   
   \begin{ctmmBlueBox}{Introduction}
   Brief description of the module purpose.
   \end{ctmmBlueBox}
   
   % Content using predefined macros only
   ```

### 6. Build System Usage

#### Quick Build Test
```bash
python3 ctmm_build.py
```
- Scans `main.tex` for missing files
- Creates minimal templates for missing modules/styles
- Tests basic and full builds
- Generates TODO files for new templates

#### Advanced Analysis
```bash
python3 build_system.py --verbose
```
- Individual module testing
- Detailed build reports
- Granular error analysis
- Comprehensive logging

## Common Error Patterns & Solutions

### "Can be used only in preamble"
**Cause**: Package loaded after `\begin{document}`
**Solution**: Move `\usepackage{}` to main.tex preamble

### "Undefined control sequence"
**Cause**: Macro not defined or wrong scope
**Solutions**:
- Check if macro is defined in preamble/style files
- Never use `\Box` directly, use `\checkbox` macro instead
- Ensure consistent macro naming

### "Command already defined"
**Cause**: Duplicate macro definitions
**Solution**: Keep only one definition (preferably in style files)

### Missing File Errors
**Cause**: Referenced module doesn't exist
**Solution**: Run `ctmm_build.py` to auto-generate templates

## Interactive PDF Features

This system creates PDFs with interactive elements:

- **Fillable text fields** for journaling and exercises
- **Clickable checkboxes** for tracking and assessments  
- **Hyperlinked navigation** between sections
- **Form-compatible output** for digital therapy use

Always test interactivity by:
1. Compiling to PDF
2. Opening in a PDF reader
3. Verifying fields are clickable/fillable

## Best Practices for Copilot

### When Adding New Content
1. Check existing modules for similar patterns
2. Use established macros rather than creating new ones
3. Follow the CTMM color scheme and visual consistency
4. Keep modules focused on single therapy concepts

### When Fixing Build Errors
1. First check if it's a package loading issue (preamble)
2. Look for undefined macros and define them centrally
3. Use the build system to identify missing files
4. Never compromise the modular structure for quick fixes

### When Modifying Styles
1. Changes go in `style/*.sty` files, not modules
2. Test changes across multiple modules
3. Maintain backward compatibility with existing modules
4. Document new macros and their usage

## Testing Strategy

1. **Local Build**: `python3 ctmm_build.py`
2. **Module Testing**: `python3 build_system.py --verbose`
3. **CI Pipeline**: GitHub Actions builds PDF automatically
4. **Manual Verification**: Check PDF interactivity manually

## Therapy Content Guidelines

When working with CTMM content:
- Maintain clinical accuracy and sensitivity
- Use person-first language
- Focus on practical, actionable strategies
- Include space for personal reflection and journaling
- Ensure content is accessible and non-triggering

This system serves real therapeutic needs - quality and accuracy are paramount.