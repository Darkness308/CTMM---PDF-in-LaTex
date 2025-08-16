# Therapie-Material Directory

## Overview

This directory is intended for binary therapy material files such as Word documents (.docx) and generated PDFs. These files are excluded from git tracking to keep the repository focused on source code.

## File Types (Not Tracked in Git)

- **Word Documents (.docx)**: Original therapy materials in editable format
- **PDF Files (.pdf)**: Generated output documents
- **Excel Files (.xlsx, .xls)**: Spreadsheets and data files  
- **PowerPoint Files (.pptx, .ppt)**: Presentation materials

## Why Binary Files Are Excluded

Binary files are excluded from git tracking because:

1. **Repository Size**: Binary files significantly increase repository size
2. **Version Control**: Git cannot meaningfully track changes in binary files
3. **Code Review**: AI tools like GitHub Copilot cannot review binary content
4. **Collaboration**: Text-based source files are better for collaborative development

## Recommended Workflow

1. **Source Files**: Keep LaTeX source files (.tex) in the `modules/` and `style/` directories
2. **Generated PDFs**: Use the build system (`python3 ctmm_build.py`) to generate PDFs locally
3. **Binary Materials**: Store original Word documents and other binary files locally or in a separate storage system
4. **Sharing**: Use GitHub Releases or external storage for sharing compiled PDFs and binary materials

## Build System

The main document can be built using:

```bash
# Build the LaTeX document
python3 ctmm_build.py

# Alternative using make
make build
```

This will generate `main.pdf` locally, which is excluded from git tracking.