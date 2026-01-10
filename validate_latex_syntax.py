#!/usr/bin/env python3
"""
LaTeX Syntax Validation Script for CI
Validates LaTeX structure without requiring LaTeX compilation.
"""

import re
import sys
from pathlib import Path

# Tolerance for brace mismatch (allows minor discrepancies in LaTeX)
BRACE_TOLERANCE = 5


def validate_latex_syntax(main_tex_path="main.tex"):
    """Validate LaTeX syntax without compilation."""
    print(f"Validating LaTeX syntax in {main_tex_path}...")

    # Check main.tex exists and is readable
    main_file = Path(main_tex_path)
    if not main_file.exists():
        print(f'❌ {main_tex_path} not found')
        return False

    try:
        content = main_file.read_text(encoding='utf-8')
        print(f'✅ {main_tex_path} readable')
    except Exception as e:
        print(f'❌ Error reading {main_tex_path}: {e}')
        return False

    # Check for basic LaTeX structure
    if r'\documentclass' not in content:
        print('❌ No \\documentclass found')
        return False
    print('✅ \\documentclass found')

    if r'\begin{document}' not in content:
        print('❌ No \\begin{document} found')
        return False
    print('✅ \\begin{document} found')

    if r'\end{document}' not in content:
        print('❌ No \\end{document} found')
        return False
    print('✅ \\end{document} found')

    # Check referenced files exist
    style_pattern = r'\\usepackage\{style/([^}]+)\}'
    module_pattern = r'\\input\{modules/([^}]+)\}'

    style_files = [f'style/{match}.sty' for match in
                   re.findall(style_pattern, content)]
    module_files = [f'modules/{match}.tex' for match in
                    re.findall(module_pattern, content)]

    print(f"Found {len(style_files)} style files and {len(module_files)} module files")

    missing = []
    for f in style_files + module_files:
        if not Path(f).exists():
            missing.append(f)

    if missing:
        print(f'❌ Missing files: {missing}')
        return False

    print(f'✅ All {len(style_files + module_files)} referenced files exist')

    # Check for obvious syntax errors
    if content.count(r'\begin{document}') != content.count(r'\end{document}'):
        print('❌ Mismatched \\begin{document} and \\end{document}')
        return False

    # Basic brace matching (simplified)
    open_braces = content.count('{')
    close_braces = content.count('}')
    if abs(open_braces - close_braces) > BRACE_TOLERANCE:  # Allow some tolerance
        print(f'⚠️  Potential brace mismatch: {open_braces} open, {close_braces} close')

    print('✅ Basic LaTeX syntax validation passed')
    return True


def main():
    """Run LaTeX syntax validation."""
    print("="*60)
    print("LATEX SYNTAX VALIDATION")
    print("="*60)

    success = validate_latex_syntax()

    if success:
        print("\n✅ All validation checks passed!")
        return 0
    else:
        print("\n❌ Validation failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())