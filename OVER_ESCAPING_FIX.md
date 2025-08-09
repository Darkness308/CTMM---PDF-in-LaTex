# Over-Escaping Fix Tool

This document describes the over-escaping issue and the systematic fix implemented in the CTMM LaTeX project.

## Problem Description

Over-escaping occurs when LaTeX commands are unnecessarily escaped, often as a result of document conversion pipelines (e.g., pandoc converting from Markdown to LaTeX). This makes the source code less readable and maintainable.

## Common Over-Escaping Patterns

1. **Double-escaped ampersands**: `\\&` instead of `\&`
2. **Pandoc artifacts**: `\hypertarget{}` and `\texorpdfstring{}` commands
3. **Unnecessary quote wrapping**: List items wrapped in `\begin{quote}...\end{quote}`
4. **Improper quote formatting**: Double backticks `\`\`` instead of proper quotes
5. **Non-standard commands**: `\ul{}` instead of `\underline{}`

## Example

### Over-escaped (problematic):
```latex
\hypertarget{tool-22-safe-words}{%
\section{\texorpdfstring{\textbf{🛑 TOOL 22 -- SAFE-WORDS \\& SIGNALSYSTEME}}{TOOL 22}}
\label{tool-22-safe-words}}

\begin{itemize}
\item
  \begin{quote}
  \textbf{„Ich kann nicht mehr``}
  \end{quote}
\end{itemize}
```

### Properly escaped (correct):
```latex
\section*{\textcolor{ctmmRed}{\faStop~TOOL 22 -- SAFE-WORDS \& SIGNALSYSTEME}}
\label{sec:tool-22-safe-words}

\begin{itemize}
\item \textbf{„Ich kann nicht mehr"}
\end{itemize}
```

## Solution: Automated Fix Tool

The `fix_over_escaping.py` script systematically detects and fixes over-escaping issues:

### Usage

```bash
# Check for issues (dry run)
python3 fix_over_escaping.py --dry-run

# Fix specific files
python3 fix_over_escaping.py modules/safewords.tex

# Fix all modules
python3 fix_over_escaping.py

# Get help
python3 fix_over_escaping.py --help
```

### Integration with Build System

The over-escaping check is integrated into the main build system (`ctmm_build.py`):

```bash
python3 ctmm_build.py
```

The build system will automatically:
1. Check for over-escaping issues
2. Report any problems found
3. Suggest running the fix tool if issues are detected

## Prevention

To prevent over-escaping issues:

1. **Avoid automated conversions** when possible - write LaTeX directly
2. **Review converted content** if using tools like pandoc
3. **Run the build system regularly** to catch issues early
4. **Use proper CTMM styling** as defined in the style packages

## Technical Details

The fix tool uses regular expressions to identify and correct:

- `\\\\&` → `\\&` (ampersand escaping)
- `\hypertarget{...}{...}` → content extraction
- `\texorpdfstring{A}{B}` → `A` (keep first argument)
- Unnecessary quote blocks in lists
- Backtick quote formatting
- Non-standard underline commands

## Files Created/Modified

- `fix_over_escaping.py` - Main fix tool
- `ctmm_build.py` - Updated build system with over-escaping check
- `OVER_ESCAPING_FIX.md` - This documentation

The current repository is clean of over-escaping issues, and the prevention system is now in place.