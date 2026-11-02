# CTMM Scripts

This directory contains utility scripts for maintaining the CTMM repository.

## Available Scripts

### scan_disruptive_chars.py

**Purpose:** Scan all text files for disruptive characters that could cause issues with LaTeX compilation, Git operations, or cross-platform compatibility.

**Usage:**
```bash
# Basic scan
python3 scripts/scan_disruptive_chars.py

# Verbose mode (shows details for each file)
python3 scripts/scan_disruptive_chars.py --verbose
```

**What it checks:**
- ✅ BOM (Byte Order Mark) at file start
- ✅ NULL bytes in text files
- ✅ Merge conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`)
- ✅ Zero-width invisible characters (U+200B, U+FEFF, etc.)
- ✅ Directional marks (U+200E, U+200F)
- ✅ Problematic Unicode quotes („ " " ' ') in code/LaTeX files
- ✅ Invalid control characters

**File Types Scanned:**
- `.tex`, `.sty` - LaTeX files
- `.md` - Markdown documentation
- `.py` - Python scripts
- `.yml`, `.yaml`, `.json` - Configuration files
- `.sh` - Shell scripts
- `.txt`, `.csv` - Text data files

**Exit Codes:**
- `0` - Success (no issues found)
- `1` - Issues found (see output for details)

**When to use:**
- Before committing new files
- After resolving merge conflicts
- When experiencing unexplained LaTeX compilation errors
- As part of CI/CD validation

**Example Output:**

When clean:
```
✅ NO DISRUPTIVE CHARACTERS FOUND!

✓ All text files are clean:
  • No BOM markers
  • No NULL bytes
  • No merge conflict markers
  • No zero-width characters
  • No directional marks
  • No problematic Unicode quotes
  • No invalid control characters

✅ Repository is ready for PR!
```

When issues found:
```
================================================================================
DISRUPTIVE CHARACTERS FOUND:
================================================================================

📄 ./modules/example.tex
   Line 42: [QUOTE] „ (U+201E) in: Beispieltext mit falschen Anführungszeichen

================================================================================
TOTAL: 1 issues in 1 files

⚠️  ACTION REQUIRED: These disruptive characters should be removed!
```

## Adding New Scripts

When adding new utility scripts:
1. Use clear, descriptive names
2. Include a docstring explaining purpose and usage
3. Add command-line help with argparse
4. Update this README with usage information
5. Make scripts executable: `chmod +x scripts/yourscript.py`
