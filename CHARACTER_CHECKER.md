# Character Issue Checker Documentation

## Overview

The `check_character_issues.py` script is a comprehensive tool for detecting problematic characters in the CTMM LaTeX project that could cause compilation errors or git issues.

## What It Checks

### 1. Merge Conflict Markers
- `<<<<<<<` - Merge conflict start
- `=======` - Merge conflict separator
- `>>>>>>>` - Merge conflict end

### 2. Invisible Unicode Characters
The following invisible characters can cause LaTeX compilation issues:

| Character | Code | Issue | LaTeX Alternative |
|-----------|------|-------|-------------------|
| Non-breaking space | U+00A0 | Invisible spacing | `~` or `\nobreakspace` |
| Zero-width space | U+200B | Invisible character | Remove |
| Zero-width non-joiner | U+200C | Invisible character | Remove |
| Zero-width joiner | U+200D | Invisible character | Remove |
| Soft hyphen | U+00AD | Invisible hyphenation | `\-` |
| BOM/Zero-width no-break space | U+FEFF | File encoding issue | Remove |

### 3. Control Characters
Any ASCII control characters (0x00-0x1F) except:
- Tab (`\t` / 0x09)
- Newline (`\n` / 0x0A)
- Carriage return (`\r` / 0x0D)

## Usage

### Command Line
```bash
# Run directly
python3 check_character_issues.py

# Run via Makefile
make check-chars
```

### Exit Codes
- `0` - No issues found (repository is clean)
- `1` - Issues found (see output for details)

### Example Output

#### Clean Repository
```
======================================================================
CTMM Character Issue Checker
======================================================================

🔍 Scanning repository: /path/to/CTMM---PDF-in-LaTex

📊 Scan Results:
   Files scanned: 30
   Lines scanned: 2954

✅ SUCCESS: Repository is clean!
   ✓ No merge conflict markers
   ✓ No invisible Unicode characters
   ✓ No problematic control characters

The repository is ready for LaTeX compilation.
```

#### Issues Found
```
======================================================================
CTMM Character Issue Checker
======================================================================

🔍 Scanning repository: /path/to/CTMM---PDF-in-LaTex

📊 Scan Results:
   Files scanned: 30
   Lines scanned: 2954

⚠️  WARNING: Found 2 issue(s):

  MERGE CONFLICT (1 issues):
    📄 modules/example.tex:45
       Git merge conflict marker: <<<<<<<
       Content: <<<<<<< HEAD

  INVISIBLE CHAR (1 issues):
    📄 style/example.sty:12
       Non-breaking space (U+00A0) - use ~ or \nobreakspace in LaTeX
       Content: 'example text'
```

## Integration

### Pre-commit Hook
Add to `.git/hooks/pre-commit`:
```bash
#!/bin/bash
python3 check_character_issues.py
if [ $? -ne 0 ]; then
    echo "❌ Commit blocked: Fix character issues before committing"
    exit 1
fi
```

### GitHub Actions
Add to `.github/workflows/check.yml`:
```yaml
- name: Check for problematic characters
  run: python3 check_character_issues.py
```

### Continuous Integration
```bash
# Add to your CI pipeline
make check-chars
```

## Files Scanned

The checker scans the following file types:
- `.tex` - LaTeX document files
- `.sty` - LaTeX style files
- `.py` - Python scripts
- `.md` - Markdown documentation
- `.sh` - Shell scripts
- `.yml`, `.yaml` - YAML configuration files
- `.txt` - Text files

## Directories Excluded

The following directories are automatically skipped:
- `.git` - Git metadata
- `build` - Build artifacts
- `__pycache__` - Python cache
- `node_modules` - Node.js dependencies
- `.venv` - Python virtual environment

## Technical Details

### Character Detection
The script uses UTF-8 encoding to read files and checks each character against known problematic Unicode code points. It provides context around detected issues to help locate and fix them.

### Performance
The checker is optimized for speed:
- Processes files in a single pass
- Groups issues by type for easier review
- Limits output for files with many issues

## Common Issues and Solutions

### Non-breaking Space in LaTeX
**Problem:** Copy-pasted text from web browsers may contain non-breaking spaces (U+00A0)

**Solution:** Replace with `~` (tilde) for non-breaking space in LaTeX:
```latex
% Instead of: Prof. Müller  (with U+00A0)
% Use: Prof.~Müller
```

### Soft Hyphen
**Problem:** Word processors insert soft hyphens for word breaking

**Solution:** Use LaTeX's `\-` for discretionary hyphens:
```latex
% Instead of: Donau­dampf­schiff­fahrts­gesell­schaft  (with U+00AD)
% Use: Donau\-dampf\-schiff\-fahrts\-gesell\-schaft
```

### Merge Conflicts
**Problem:** Git merge conflicts not resolved

**Solution:** Resolve the merge conflict in your editor and remove conflict markers:
```diff
- <<<<<<< HEAD
- Your version
- =======
- Their version
- >>>>>>>
+ Resolved version
```

## Maintenance

### Adding New Checks
To add a new problematic character to check:

1. Add to `PROBLEMATIC_CHARS` dictionary in `check_character_issues.py`:
   ```python
   PROBLEMATIC_CHARS = {
       '\uXXXX': 'Description and solution',
       # ... existing entries
   }
   ```

2. Test with a sample file containing the character

3. Update this documentation

### Testing
Create test files with known issues to verify the checker works:
```bash
# Create test file with non-breaking space
printf "Test\u00A0text" > test_file.tex

# Run checker
python3 check_character_issues.py

# Clean up
rm test_file.tex
```

## See Also

- [Main README](README.md) - Project overview
- [Build System](ctmm_build.py) - LaTeX build automation
- [Makefile](Makefile) - Build commands
