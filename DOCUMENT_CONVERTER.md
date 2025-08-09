# CTMM Document Converter

The CTMM Document Converter is a tool that addresses the systematic LaTeX over-escaping problem and enables conversion of therapy documents from Word format to clean LaTeX.

## Quick Start

```bash
# Convert all Word documents in therapie-material/ to LaTeX
make convert

# Fix over-escaped LaTeX files in current directory  
make convert-clean

# Run tests
make test-converter
```

## Features

### Word Document Conversion
- Converts `.docx` files to clean LaTeX using pandoc
- Preserves German therapeutic content and special characters
- Post-processes output to be CTMM-compatible
- Adds appropriate module headers
- Successfully converts all 16 therapy documents from `therapie-material/`

### Over-Escape Fixing
Fixes systematic LaTeX over-escaping problems like:

**Before:**
```latex
\textbackslash{}section\textbackslash{}{\textbackslash{}texorpdfstring\textbackslash{}{📄 \textbackslash{}textbf\textbackslash{}{TOOL 23: TRIGGER-MANAGEMENT\textbackslash{}}\textbackslash{}}\textbackslash{}{📄 TOOL 23: TRIGGER-MANAGEMENT\textbackslash{}}\textbackslash{}}\textbackslash{}label\textbackslash{}{tool-23-trigger-management\textbackslash{}}\textbackslash{}}
```

**After:**
```latex  
\section{\texorpdfstring{📄 \textbf{TOOL 23: TRIGGER-MANAGEMENT}}{📄 TOOL 23: TRIGGER-MANAGEMENT}}\label{tool-23-trigger-management}
```

## Usage

### Command Line Interface

```bash
# Convert Word documents (default: therapie-material/ → converted/)
python3 document_converter.py

# Convert from custom directories
python3 document_converter.py --input docs --output output

# Fix over-escaped LaTeX files
python3 document_converter.py --clean

# Fix over-escaped files in specific directory
python3 document_converter.py --clean --search-dir /path/to/tex/files

# Show help
python3 document_converter.py --help
```

### Makefile Integration

```bash
make convert         # Convert Word documents to LaTeX
make convert-clean   # Fix over-escaped LaTeX files
make test-converter  # Run unit tests
```

## Output

### Converted Files
Converted LaTeX files are saved to the `converted/` directory with:
- CTMM module headers with metadata
- Clean LaTeX structure compatible with main document
- Preserved German therapeutic content
- Removed pandoc-specific document class definitions

### File Processing
- **Backup creation**: Original over-escaped files are backed up with `.backup` extension
- **Error handling**: Graceful handling of missing files, empty directories
- **Progress reporting**: Detailed status output during conversion

## Architecture

### Over-Escape Patterns
The converter fixes these common patterns (in order of specificity):

1. **Specific command patterns**: `\section\textbackslash{}{` → `\section{`
2. **Command-specific patterns**: `\section\textbackslash{}` → `\section`  
3. **Brace patterns**: `\textbackslash{}{` → `{`
4. **General patterns**: `\textbackslash{}command` → `\command`

### Post-Processing
Converted LaTeX files are post-processed to:
- Remove pandoc document class and environment
- Add CTMM module headers with conversion metadata
- Preserve section structure and therapeutic content
- Clean up German language package handling

## Testing

The converter includes comprehensive unit tests covering:
- Over-escape pattern fixing (simple and complex cases)
- Word document conversion workflow
- File handling (empty directories, missing files)
- LaTeX post-processing
- Integration scenarios

Run tests with:
```bash
make test-converter
# or
python3 test_document_converter.py
```

## Requirements

- **Python 3.6+** 
- **pandoc** for Word document conversion
- **LaTeX distribution** (for the broader CTMM system)

Install dependencies:
```bash
sudo apt-get install pandoc texlive-latex-base texlive-fonts-recommended
```

## Integration with CTMM

The document converter integrates seamlessly with the existing CTMM build system:
- Converted files can be included in `main.tex` modules
- Follows CTMM naming and structure conventions
- Compatible with existing style files and design system
- Supports the German therapeutic content workflow

## Troubleshooting

### Common Issues

**"No .docx files found"**: Verify files exist in `therapie-material/` directory
**"pandoc not found"**: Install pandoc with your system package manager
**"Permission denied"**: Ensure write access to output directory

### File Structure
```
CTMM---PDF-in-LaTex/
├── document_converter.py     # Main converter script
├── therapie-material/        # Input .docx files (16 files)
├── converted/               # Output .tex files (auto-created)
├── test_document_converter.py # Unit tests
└── Makefile                 # Build system integration
```

The document converter successfully addresses the root cause of PR #226's issue - providing actual file changes for Copilot to review and maintaining them properly within the CTMM system.