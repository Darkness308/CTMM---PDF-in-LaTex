# CI Build Failure Fix - Usage Instructions

## Quick Fix for copilot/fix-442 Branch

To fix the CI build failure on the `copilot/fix-442` branch, run these commands:

```bash
# 1. Checkout the problematic branch
git checkout copilot/fix-442

# 2. Get the fix script from this branch
git checkout copilot/fix-454 -- fix_ci_build.sh

# 3. Run the automated fix
chmod +x fix_ci_build.sh
./fix_ci_build.sh

# 4. Commit the fix
git add .github/workflows/latex-build.yml
git commit -m "Fix CI build failure: remove -shell-escape and problematic packages"

# 5. Push to test the CI build
git push
```

## What the Fix Does

**Removes these problematic elements:**
- `-shell-escape` argument (security restricted in CI environments) 
- `texlive-latex-extra` package (may not be available)
- `texlive-pictures` package (may not be available)
- `texlive-science` package (may not be available)

**Preserves these working elements:**
- All YAML formatting improvements
- Essential LaTeX packages (texlive-lang-german, texlive-fonts-recommended, etc.)
- All other workflow configuration

## Verification

After applying the fix, all these should pass:
- ✅ `python3 validate_latex_syntax.py`
- ✅ `python3 ctmm_build.py` 
- ✅ `python3 test_ctmm_build.py`
- ✅ CI build job should complete successfully

## Files

- `CI_BUILD_FIX.md` - Detailed technical analysis
- `fix_ci_build.sh` - Automated fix script  
- `QUICK_FIX_INSTRUCTIONS.md` - This file

The solution provides minimal, surgical changes that preserve all working functionality while removing only the problematic elements causing the CI failure.