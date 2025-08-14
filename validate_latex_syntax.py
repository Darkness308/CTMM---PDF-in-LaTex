#!/usr/bin/env python3
"""
LaTeX Syntax Validation Script for CI
Validates LaTeX structure without requiring LaTeX compilation.
"""

import re
import sys
from pathlib import Path


def validate_latex_syntax(main_tex_path="main.tex"):
    """Validate LaTeX syntax without compilation."""
    print(f"Validating LaTeX syntax in {main_tex_path}...")
    
    # Check main.tex exists and is readable
    main_file = Path(main_tex_path)
    if not main_file.exists():
        print(f'❌ {main_tex_path} not found')
        print(f'Current working directory: {Path.cwd()}')
        print(f'Directory contents: {list(Path(".").glob("*"))}')
        return False
        
    try:
        # Try reading with explicit encoding and error handling
        with open(main_file, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        print(f'✅ {main_tex_path} readable (length: {len(content)} chars)')
    except Exception as e:
        print(f'❌ Error reading {main_tex_path}: {e}')
        # Try with different encoding detection
        try:
            import chardet
            with open(main_file, 'rb') as f:
                raw_data = f.read()
                detected = chardet.detect(raw_data)
                print(f'   Detected encoding: {detected}')
        except Exception:
            pass
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
    try:
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
            print(f'Available style files: {list(Path("style").glob("*.sty")) if Path("style").exists() else "style/ not found"}')
            print(f'Available module files: {list(Path("modules").glob("*.tex")) if Path("modules").exists() else "modules/ not found"}')
            return False
        
        print(f'✅ All {len(style_files + module_files)} referenced files exist')
        
    except Exception as e:
        print(f'❌ Error checking referenced files: {e}')
        return False
    
    # Check for obvious syntax errors
    try:
        if content.count(r'\begin{document}') != content.count(r'\end{document}'):
            print('❌ Mismatched \\begin{document} and \\end{document}')
            return False
        
        # Basic brace matching (simplified)
        open_braces = content.count('{')
        close_braces = content.count('}')
        if abs(open_braces - close_braces) > 10:  # Allow some tolerance
            print(f'⚠️  Potential brace mismatch: {open_braces} open, {close_braces} close')
        
        print('✅ Basic LaTeX syntax validation passed')
        return True
        
    except Exception as e:
        print(f'❌ Error in syntax validation: {e}')
        return False


def main():
    """Run LaTeX syntax validation."""
    try:
        print("="*60)
        print("LATEX SYNTAX VALIDATION")
        print("="*60)
        
        # Add environment diagnostics for CI debugging
        import sys
        import os
        print(f"Python version: {sys.version}")
        print(f"Working directory: {os.getcwd()}")
        print(f"PYTHONPATH: {sys.path[:3]}...")  # Show first few entries
        
        success = validate_latex_syntax()
        
        if success:
            print("\n✅ All validation checks passed!")
            return 0
        else:
            print("\n❌ Validation failed!")
            return 1
            
    except Exception as e:
        print(f"\n❌ FATAL ERROR during validation: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except Exception as e:
        print(f"❌ CRITICAL ERROR: {e}")
        sys.exit(1)