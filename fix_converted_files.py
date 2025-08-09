#!/usr/bin/env python3
"""
Fix encoding and LaTeX syntax issues in converted documents.
"""

import re
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def fix_latex_syntax(content: str) -> str:
    """Fix common LaTeX syntax issues."""
    
    # Fix common Unicode issues
    replacements = [
        # Smart quotes
        ('"', '"'),
        ('"', '"'),
        (''', "'"),
        (''', "'"),
        
        # Dashes
        ('–', '--'),
        ('—', '---'),
        
        # Special characters that need escaping
        ('&', '\\&'),
        ('%', '\\%'),
        ('$', '\\$'),
        ('_', '\\_'),
        ('#', '\\#'),
        ('^', '\\textasciicircum{}'),
        ('~', '\\textasciitilde{}'),
        
        # Common problematic patterns
        ('{.underline}', ''),  # Remove invalid underline syntax
        ('**', '\\textbf{'),   # Start bold
        ('\\textbf{(.+?)**', '\\textbf{\\1}'),  # Fix bold endings
        
        # Fix malformed sections
        ('\\section{\\section{', '\\section{'),
        ('\\subsection{\\subsection{', '\\subsection{'),
        
        # Fix emoji and special symbols (using correct FontAwesome5 syntax)
        ('🧩', '\\textcolor{ctmmBlue}{\\faPuzzlePiece}'),
        ('🎯', '\\textcolor{ctmmGreen}{\\faBullseye}'),
        ('🧭', '\\textcolor{ctmmOrange}{\\faCompass}'),
        ('💡', '\\textcolor{ctmmYellow}{\\faLightbulb}'),
        ('🟢', '\\textcolor{ctmmGreen}{\\faCircle}'),
        ('🔴', '\\textcolor{ctmmRed}{\\faCircle}'),
        ('🟡', '\\textcolor{ctmmYellow}{\\faCircle}'),
        ('📝', '\\textcolor{ctmmBlue}{\\faEdit}'),
        ('🛑', '\\textcolor{ctmmRed}{\\faStop}'),
        ('🧠', '\\textcolor{ctmmPurple}{\\faBrain}'),
        
        # Fix incorrect FontAwesome syntax in converted files
        ('\\faIcon{puzzle-piece}', '\\faPuzzlePiece'),
        ('\\faIcon{target}', '\\faBullseye'),
        ('\\faIcon{compass}', '\\faCompass'),
        ('\\faIcon{lightbulb}', '\\faLightbulb'),
        ('\\faIcon{circle}', '\\faCircle'),
        ('\\faIcon{edit}', '\\faEdit'),
        ('\\faIcon{stop}', '\\faStop'),
        ('\\faIcon{brain}', '\\faBrain'),
    ]
    
    fixed_content = content
    for old, new in replacements:
        fixed_content = fixed_content.replace(old, new)
    
    # Fix specific patterns with regex
    patterns = [
        # Fix improperly nested formatting
        (r'\*\*(.+?)\*\*', r'\\textbf{\1}'),
        (r'\*(.+?)\*', r'\\textit{\1}'),
        
        # Fix improper section nesting
        (r'\\section\{(.+?)\}\s*\\section\{(.+?)\}', r'\\section{\1}\n\\subsection{\2}'),
        
        # Clean up multiple newlines
        (r'\n\s*\n\s*\n+', r'\n\n'),
        
        # Fix > quote blocks to LaTeX quotes
        (r'^>\s*(.+)$', r'\\begin{quote}\n\1\n\\end{quote}'),
        
        # Fix [text]{.style} patterns
        (r'\[([^\]]+)\]\{[^}]+\}', r'\1'),
    ]
    
    for pattern, replacement in patterns:
        fixed_content = re.sub(pattern, replacement, fixed_content, flags=re.MULTILINE)
    
    return fixed_content

def fix_converted_files():
    """Fix all converted LaTeX files."""
    converted_dir = Path("converted")
    
    if not converted_dir.exists():
        print("No converted directory found")
        return
    
    files_fixed = 0
    for tex_file in converted_dir.glob("*.tex"):
        try:
            print(f"Fixing {tex_file.name}...")
            
            # Read with error handling
            with open(tex_file, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
            
            # Apply fixes
            fixed_content = fix_latex_syntax(content)
            
            # Write back
            with open(tex_file, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            
            files_fixed += 1
            
        except Exception as e:
            print(f"Error fixing {tex_file}: {e}")
    
    print(f"Fixed {files_fixed} files")

if __name__ == "__main__":
    fix_converted_files()