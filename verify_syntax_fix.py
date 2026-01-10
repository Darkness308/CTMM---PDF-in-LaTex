#!/usr/bin/env python3
"""
Verification script for ctmm_build.py syntax fix.
Confirms that the try-except block structure is correct in the template creation section.
"""

import ast
import sys
from pathlib import Path


def verify_syntax():
    """Verify that ctmm_build.py has correct Python syntax."""
    try:
        with open('ctmm_build.py', 'r') as f:
            code = f.read()
        ast.parse(code)
        print("✓ ctmm_build.py has valid Python syntax")
        return True
    except SyntaxError as e:
        print(f"✗ Syntax error in ctmm_build.py:")
        print(f"  Line {e.lineno}: {e.msg}")
        print(f"  {e.text}")
        return False


def verify_try_except_structure():
    """Verify that the template creation section has proper try-except structure."""
    with open('ctmm_build.py', 'r') as f:
        lines = f.readlines()
    
    # Find the template creation section
    template_creation_start = None
    for i, line in enumerate(lines):
        if 'Creating templates for missing files' in line:
            template_creation_start = i
            break
    
    if template_creation_start is None:
        print("✗ Could not find template creation section")
        return False
    
    # Check structure in the next 15 lines
    found_try = False
    found_except = False
    try_line = None
    except_line = None
    
    for i in range(template_creation_start, min(template_creation_start + 15, len(lines))):
        line = lines[i].strip()
        if line.startswith('try:'):
            found_try = True
            try_line = i + 1
        elif line.startswith('except Exception as e:'):
            found_except = True
            except_line = i + 1
    
    if found_try and found_except:
        print(f"✓ Template creation section has proper try-except structure")
        print(f"  - try: block at line {try_line}")
        print(f"  - except: block at line {except_line}")
        return True
    elif not found_try and found_except:
        print(f"✗ Found except without matching try (line {except_line})")
        return False
    else:
        print("✓ Template creation section structure is valid")
        return True


def main():
    """Main verification function."""
    print("Verifying ctmm_build.py syntax fix...")
    print("=" * 60)
    
    syntax_ok = verify_syntax()
    structure_ok = verify_try_except_structure()
    
    print("=" * 60)
    if syntax_ok and structure_ok:
        print("✅ All checks passed! The syntax fix is correctly applied.")
        return 0
    else:
        print("❌ Verification failed. Please review the code.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
