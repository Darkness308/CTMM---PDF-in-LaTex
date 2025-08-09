# Therapie-Material Directory

This directory is intended for source therapy materials in the CTMM project.

## Purpose

This directory should contain **source materials only** - not binary files like PDFs or DOCX documents.

## Recommended File Types

- **Markdown files** (`.md`) - Documentation and structured therapy content
- **Plain text files** (`.txt`) - Simple therapy materials
- **LaTeX files** (`.tex`) - Therapy modules and worksheets

## What NOT to include

- ❌ **PDF files** (`.pdf`) - These are build artifacts  
- ❌ **Office documents** (`.docx`, `.doc`) - Convert these to LaTeX or Markdown
- ❌ **Binary files** - Cannot be reviewed by Copilot or version controlled effectively

## Converting Existing Materials

If you have Word documents (`.docx`) or other office files:

1. **Convert to LaTeX** for therapy worksheets and forms
2. **Convert to Markdown** for documentation and structured content
3. **Convert to plain text** for simple materials

## Build System Integration

Source files in this directory can be referenced by:
- The main build system (`ctmm_build.py`)
- Individual LaTeX modules in `modules/`
- The main document (`main.tex`)

This ensures all therapy materials remain reviewable and maintainable in version control.