# CTMM Build System - Troubleshooting Guide

## Quick Resolution Summary

The build system requires specific LaTeX packages to compile successfully. This guide provides solutions for common build failures.

## [PASS] Dependencies Required

### Python Dependencies
```bash
pip install chardet
```

### LaTeX Dependencies

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install -y texlive-latex-base texlive-latex-extra texlive-fonts-recommended texlive-lang-german texlive-fonts-extra
```

**Complete LaTeX Installation (Recommended):**
```bash
sudo apt-get install -y texlive-full
```

### Required LaTeX Packages
- `texlive-lang-german` - German language support (babel ngerman)
- `texlive-fonts-extra` - FontAwesome5 and extra fonts
- `texlive-latex-extra` - Additional LaTeX packages
- `texlive-fonts-recommended` - Standard fonts

## [FIX] Common Build Errors & Solutions

### Error 1: "Unknown option 'ngerman'"
```
! Package babel Error: Unknown option 'ngerman'. Either you misspelled it
(babel)  or the language definition file ngerman.ldf
(babel)  was not found.
```

**Solution:**
```bash
sudo apt-get install texlive-lang-german
```

### Error 2: "File 'fontawesome5.sty' not found"
```
! LaTeX Error: File `fontawesome5.sty' not found.
```

**Solution:**
```bash
sudo apt-get install texlive-fonts-extra
```

### Error 3: "pdflatex not found"
```
WARNING: pdflatex not found - skipping LaTeX compilation test
```

**Solution:**
```bash
sudo apt-get install texlive-latex-base texlive-latex-extra
```

## [DEPLOY] Quick Start Commands

### 1. Install All Dependencies
```bash
# For Ubuntu/Debian systems
sudo apt-get update && sudo apt-get install -y \
  texlive-latex-base \
  texlive-latex-extra \
  texlive-fonts-recommended \
  texlive-lang-german \
  texlive-fonts-extra \
  texlive-science

# Install Python dependencies
pip install chardet
```

### 2. Test Build System
```bash
python3 ctmm_build.py
```

### 3. Build PDF
```bash
make build
# or
pdflatex -interaction=nonstopmode main.tex
```

## [SEARCH] Verification Steps

After installing dependencies, verify the build works:

```bash
# 1. Check Python build system
python3 ctmm_build.py

# Expected output should include:
# [OK] LaTeX validation: PASS
# [OK] Basic build: PASS
# [OK] Full build: PASS

# 2. Run unit tests
python3 test_ctmm_build.py

# Expected: All 56 tests should pass

# 3. Manual LaTeX test
pdflatex -interaction=nonstopmode main.tex

# Expected: Should generate main.pdf without errors
```

## [TEST] GitHub Actions Configuration

For CI/CD environments, the workflow already includes proper dependencies:

```yaml
- name: Set up LaTeX
  uses: dante-ev/latex-action@v0.2.0
  with:
  extra_system_packages: |
  texlive-lang-german
  texlive-fonts-recommended
  texlive-latex-recommended
  texlive-fonts-extra
  texlive-latex-extra
  texlive-science
  texlive-pstricks
```

## [BUG] Advanced Troubleshooting

### Check LaTeX Installation
```bash
# Verify pdflatex is available
which pdflatex

# Check LaTeX version
pdflatex --version

# Test minimal LaTeX compilation
echo '\documentclass{article}\begin{document}Hello\end{document}' > test.tex
pdflatex test.tex
```

### Check Package Availability
```bash
# Search for specific packages
apt-cache search texlive-lang-german
apt-cache search texlive-fonts-extra

# Check installed packages
dpkg -l | grep texlive
```

### Build System Debug Mode
```bash
# Detailed analysis
python3 build_system.py --verbose

# Enhanced build management
python3 ctmm_build.py --enhanced
```

## [TARGET] Environment-Specific Notes

### Docker/Containers
```dockerfile
RUN apt-get update && apt-get install -y \
  texlive-latex-base \
  texlive-latex-extra \
  texlive-fonts-recommended \
  texlive-lang-german \
  texlive-fonts-extra \
  python3 \
  python3-pip

RUN pip3 install chardet
```

### GitHub Codespaces
The codespace environment may need manual package installation:
```bash
sudo apt-get update
sudo apt-get install -y texlive-lang-german texlive-fonts-extra
```

##  Getting Help

If issues persist:

1. **Check build system output**: Look for specific error messages in `ctmm_build.py` output
2. **Check LaTeX logs**: Look for `.log` files for detailed error information
3. **Verify file permissions**: Ensure all files are readable
4. **Check disk space**: LaTeX installations can be large

## [PASS] Success Indicators

A successful build should show:
- All LaTeX validation checks pass
- PDF files generate successfully (main.pdf ~400KB+)
- Unit tests pass (56/56 tests)
- No ERROR messages in build output

---

**Last Updated**: August 2024  
**Version**: 1.0