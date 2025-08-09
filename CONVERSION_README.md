# CTMM Document Conversion Tool

This tool fixes the LaTeX over-escaping issue identified in PR #3 where converted documents contained excessive `\textbackslash{}` escaping that made the code unreadable and unmaintainable.

## Problem Description

When documents are converted from Word (.docx) or other formats to LaTeX, sometimes the conversion process creates over-escaped LaTeX code like this:

```latex
\textbackslash{}section\textbackslash{}{\textbackslash{}texorpdfstring\textbackslash{}{📄 \textbackslash{}textbf\textbackslash{}{TOOL 23: TRIGGER-MANAGEMENT\textbackslash{}}\textbackslash{}}\textbackslash{}{📄 TOOL 23: TRIGGER-MANAGEMENT\textbackslash{}}\textbackslash{}}\textbackslash{}label\textbackslash{}{tool-23-trigger-management\textbackslash{}}\textbackslash{}}
```

## Solution

The `document_converter.py` script provides:

1. **Document Conversion**: Converts Word documents to clean LaTeX
2. **Over-escaping Cleanup**: Fixes existing over-escaped LaTeX files
3. **Automated Processing**: Batch processing of multiple documents

## Usage

### Convert Word Documents to LaTeX
```bash
python3 document_converter.py --source therapie-material --output converted
```
or
```bash
make convert
```

### Clean Over-escaped LaTeX Files
```bash
python3 document_converter.py --clean --output converted
```
or 
```bash
make convert-clean
```

### Convert Single File
```bash
python3 document_converter.py --file "therapie-material/Tool 23 Trigger Management.docx"
```

## Before and After Example

### Before (Over-escaped):
```latex
\textbackslash{}hypertarget\textbackslash{}{tool-23-trigger-management\textbackslash{}}\textbackslash{}{\textbackslash{}%
\textbackslash{}section\textbackslash{}{\textbackslash{}texorpdfstring\textbackslash{}{📄 \textbackslash{}textbf\textbackslash{}{TOOL 23: TRIGGER-MANAGEMENT\textbackslash{}}\textbackslash{}}\textbackslash{}{📄 TOOL 23: TRIGGER-MANAGEMENT\textbackslash{}}\textbackslash{}}\textbackslash{}label\textbackslash{}{tool-23-trigger-management\textbackslash{}}\textbackslash{}}

🧩 \textbackslash{}emph\textbackslash{}{\textbackslash{}textbf\textbackslash{}{Modul zur Selbsthilfe \textbackslash{}\textbackslash{}\& Co-Regulation\textbackslash{}}\textbackslash{}}
```

### After (Clean LaTeX):
```latex
\hypertarget{tool-23-trigger-management}{\%
\section{\texorpdfstring{📄 \textbf{TOOL 23: TRIGGER-MANAGEMENT}}{📄 TOOL 23: TRIGGER-MANAGEMENT}}\label{tool-23-trigger-management}}

🧩 \emph{\textbf{Modul zur Selbsthilfe \\\& Co-Regulation}}
```

## How It Works

The script uses sophisticated regular expressions to:

1. **Identify over-escaped patterns**: Detects `\textbackslash{}` sequences that shouldn't be there
2. **Convert to proper LaTeX**: Replaces over-escaped commands with correct LaTeX syntax
3. **Preserve proper escaping**: Maintains necessary escaping for special characters
4. **Handle complex structures**: Properly processes nested commands and environments

## Key Features

- ✅ **Automatic Detection**: Identifies and fixes all common over-escaping patterns
- ✅ **Batch Processing**: Handles multiple files at once
- ✅ **Safe Operation**: Preserves original files and creates cleaned versions
- ✅ **Integration**: Works with existing CTMM build system
- ✅ **Flexible Input**: Supports Word documents, Markdown, and existing LaTeX files

## Fixed Patterns

The tool fixes these common over-escaping patterns:

- Section commands: `\textbackslash{}section` → `\section`
- Text formatting: `\textbackslash{}textbf\textbackslash{}{text\textbackslash{}}` → `\textbf{text}`
- Hyperlinks: `\textbackslash{}hypertarget` → `\hypertarget`
- Environments: `\textbackslash{}begin\textbackslash{}{itemize\textbackslash{}}` → `\begin{itemize}`
- Line breaks: `\textbackslash{}\textbackslash{}` → `\\`

## Dependencies

- **Python 3.6+**: Core functionality
- **Pandoc (optional)**: For Word document conversion
  - Install: `apt-get install pandoc` (Ubuntu/Debian)
  - If not available, creates placeholder LaTeX files

## Integration with CTMM Build System

The conversion tool is integrated into the CTMM build system:

```bash
make convert       # Convert Word documents
make convert-clean # Clean over-escaped LaTeX
make check         # Verify build system
make build         # Build PDF
```

## Example Workflow

1. **Place Word documents** in `therapie-material/` directory
2. **Convert to LaTeX**: `make convert`
3. **Clean any over-escaping**: `make convert-clean` (if needed)
4. **Review converted files** in `converted/` directory
5. **Include in main document** by adding `\input{converted/filename}` to `main.tex`
6. **Build PDF**: `make build`

## Output Structure

```
converted/
├── Tool 23 Trigger Management.tex          # Individual converted files
├── Tool 22 Safewords Signalsysteme.tex
├── ...
└── all_converted_documents.tex             # Combined file with all content
```

## Troubleshooting

### Common Issues

1. **"Pandoc not found"**: Install pandoc or use placeholder mode
2. **Permission errors**: Ensure write access to output directory
3. **Encoding issues**: Files are processed with UTF-8 encoding
4. **Complex formatting**: Manual review may be needed for complex documents

### Getting Help

```bash
python3 document_converter.py --help
make help
```

## Contributing

When adding new conversion patterns:

1. Add the pattern to `clean_over_escaped_latex()` method
2. Test with sample over-escaped content
3. Verify the output is valid LaTeX
4. Update this documentation

## Related Files

- `document_converter.py`: Main conversion script
- `Makefile`: Build system integration
- `ctmm_build.py`: CTMM build system
- `main.tex`: Main LaTeX document