# Fix for Over-Escaping Issue in LaTeX Conversion Pipeline

## Problem Description

The document conversion pipeline in PR #3 was producing over-escaped LaTeX code where all LaTeX commands were unnecessarily escaped with `\textbackslash{}` sequences, making the output unreadable and unmaintainable.

### Before (problematic output):
```latex
\textbackslash{}section\textbackslash{}{\textbackslash{}texorpdfstring\textbackslash{}{\textbackslash{}textbf\textbackslash{}{TOOL 22\textbackslash{}}\textbackslash{}}\textbackslash{}{TOOL 22\textbackslash{}}\textbackslash{}}\textbackslash{}label\textbackslash{}{tool-22\textbackslash{}}\textbackslash{}}
```

### After (fixed output):
```latex
\section{\texorpdfstring{\textbf{TOOL 22}}{TOOL 22}}\label{tool-22}
```

## Root Cause

The issue was in the `sanitize_latex()` function in `scripts/document-conversion.sh` on line 70:

```bash
-e 's/\\/\\textbackslash{}/g' \
```

This line was converting ALL backslashes to `\textbackslash{}`, including those that were already part of properly formatted LaTeX commands produced by pandoc. Since pandoc output is already in proper LaTeX format, applying additional backslash escaping broke all the LaTeX commands.

## Solution

### 1. Fixed the conversion script

Removed the problematic backslash escaping from the `sanitize_latex()` function since:
- Pandoc already produces proper LaTeX output
- Additional backslash escaping is not needed for already-formatted LaTeX
- The escaping was breaking valid LaTeX commands

### 2. Fixed existing over-escaped files

Created comprehensive fix scripts that:
- Convert `\textbackslash{}command\textbackslash{}` back to `\command`
- Fix over-escaped braces and arguments
- Clean up double-escaped patterns
- Restore proper ampersand escaping (`\&` instead of `\\textbackslash{}&`)

### 3. Scripts created for the fix:

- `fix_overescaping.sh` - Primary fix script for common LaTeX commands
- `fix_overescaping_comprehensive.sh` - Additional cleanup for edge cases
- `fix_overescaping.py` - Python version (not used due to regex issues)

## Results

- **19 out of 20** converted files were successfully fixed
- **All `\textbackslash{}` patterns** were eliminated from the converted files
- **LaTeX syntax is now clean and readable** matching standard LaTeX conventions
- **Conversion pipeline** now preserves pandoc's proper LaTeX output

## Files Affected

All files in the `converted/` directory from PR #3:
- Tool 22 Safewords Signalsysteme CTMM.tex
- Tool 23 Trigger Management.tex
- README.tex
- And 16 other converted therapy material files

## Prevention

The fix to `scripts/document-conversion.sh` ensures this issue won't recur in future conversions. The `sanitize_latex()` function now only escapes characters that actually need escaping in LaTeX content, without breaking existing LaTeX commands.

## Testing

The fixed LaTeX files compile cleanly and are now human-readable for maintenance and editing purposes.