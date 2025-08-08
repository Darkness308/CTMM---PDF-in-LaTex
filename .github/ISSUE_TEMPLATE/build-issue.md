---
name: LaTeX Build Issue
about: Report problems with LaTeX compilation or build system
title: '[BUILD] '
labels: 'bug, build'
assignees: ''
---

## Build Issue Description
A clear description of what went wrong.

## Error Output
```
Paste the full error message here
```

## Build System Output
```bash
# Run this command and paste the output:
python3 ctmm_build.py
```

## Environment
- Operating System: [e.g., Windows 10, macOS, Ubuntu]
- LaTeX Distribution: [e.g., TeX Live 2023, MiKTeX]
- Python Version: [run `python3 --version`]

## Files Modified
List any files you modified before the error occurred:
- [ ] main.tex
- [ ] modules/*.tex
- [ ] style/*.sty
- [ ] Other: ___________

## Expected Behavior
What should have happened?

## Additional Context
Any other relevant information or screenshots.

## Build System Checklist
- [ ] I ran `python3 ctmm_build.py` to check for missing files
- [ ] I verified no `\usepackage{}` commands are outside main.tex preamble
- [ ] I checked that all custom macros are defined in style files
- [ ] The error occurs even with a clean repository clone