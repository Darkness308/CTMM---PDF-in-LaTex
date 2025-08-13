#!/bin/bash

# Fix CI Build Failure Script
# This script fixes the LaTeX workflow configuration that causes CI failures

set -e

echo "============================================================"
echo "CTMM CI Build Failure Fix Script"
echo "============================================================"
echo ""
echo "This script will fix the CI build failure by removing problematic"
echo "LaTeX configuration elements that cause security restrictions and"
echo "package availability issues in CI environments."
echo ""

# Check if we're in the right directory
if [ ! -f ".github/workflows/latex-build.yml" ]; then
    echo "❌ Error: .github/workflows/latex-build.yml not found"
    echo "Please run this script from the root of the CTMM repository"
    exit 1
fi

echo "✅ Found LaTeX workflow file"

# Check if the problematic elements exist
if grep -q "\-shell\-escape" .github/workflows/latex-build.yml; then
    echo "🔍 Found problematic -shell-escape argument"
    HAS_SHELL_ESCAPE=true
else
    echo "✅ No -shell-escape argument found"
    HAS_SHELL_ESCAPE=false
fi

if grep -q "texlive-latex-extra\|texlive-pictures\|texlive-science" .github/workflows/latex-build.yml; then
    echo "🔍 Found problematic additional LaTeX packages"
    HAS_EXTRA_PACKAGES=true
else
    echo "✅ No problematic additional packages found"
    HAS_EXTRA_PACKAGES=false
fi

# If no issues found, exit
if [ "$HAS_SHELL_ESCAPE" = false ] && [ "$HAS_EXTRA_PACKAGES" = false ]; then
    echo ""
    echo "✅ No CI build issues found in the workflow configuration"
    echo "✅ The workflow appears to already be in working condition"
    exit 0
fi

echo ""
echo "🛠️  Applying fixes..."

# Backup the original file
cp .github/workflows/latex-build.yml .github/workflows/latex-build.yml.backup
echo "✅ Created backup: .github/workflows/latex-build.yml.backup"

# Remove -shell-escape argument
if [ "$HAS_SHELL_ESCAPE" = true ]; then
    sed -i 's/-shell-escape//g' .github/workflows/latex-build.yml
    echo "✅ Removed -shell-escape argument"
fi

# Remove problematic packages
if [ "$HAS_EXTRA_PACKAGES" = true ]; then
    sed -i '/texlive-latex-extra/d' .github/workflows/latex-build.yml
    sed -i '/texlive-pictures/d' .github/workflows/latex-build.yml  
    sed -i '/texlive-science/d' .github/workflows/latex-build.yml
    echo "✅ Removed problematic LaTeX packages"
fi

echo ""
echo "🔍 Validating the fix..."

# Validate the YAML syntax
if command -v python3 >/dev/null 2>&1; then
    if python3 -c "import yaml; yaml.safe_load(open('.github/workflows/latex-build.yml'))" 2>/dev/null; then
        echo "✅ YAML syntax is valid"
    else
        echo "❌ YAML syntax error detected"
        echo "Restoring backup..."
        mv .github/workflows/latex-build.yml.backup .github/workflows/latex-build.yml
        exit 1
    fi
else
    echo "⚠️  Python3 not available - skipping YAML validation"
fi

# Run CTMM validation if available
if [ -f "validate_latex_syntax.py" ] && command -v python3 >/dev/null 2>&1; then
    echo "🔍 Running LaTeX validation..."
    if python3 validate_latex_syntax.py >/dev/null 2>&1; then
        echo "✅ LaTeX syntax validation passed"
    else
        echo "❌ LaTeX validation failed"
        echo "Restoring backup..."
        mv .github/workflows/latex-build.yml.backup .github/workflows/latex-build.yml
        exit 1
    fi
fi

echo ""
echo "============================================================"
echo "✅ CI BUILD FIX COMPLETED SUCCESSFULLY"
echo "============================================================"
echo ""
echo "Changes made:"
if [ "$HAS_SHELL_ESCAPE" = true ]; then
    echo "  • Removed -shell-escape argument (security restriction)"
fi
if [ "$HAS_EXTRA_PACKAGES" = true ]; then
    echo "  • Removed texlive-latex-extra package"
    echo "  • Removed texlive-pictures package"
    echo "  • Removed texlive-science package"
fi
echo ""
echo "The workflow now uses only well-supported packages and arguments"
echo "that are compatible with CI environments."
echo ""
echo "Next steps:"
echo "1. Review the changes: git diff .github/workflows/latex-build.yml"
echo "2. Test locally if possible"
echo "3. Commit the changes: git add . && git commit -m 'Fix CI build failure'"
echo "4. Push to trigger CI build test"
echo ""
echo "Backup saved as: .github/workflows/latex-build.yml.backup"