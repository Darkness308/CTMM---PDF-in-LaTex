#!/usr/bin/env python3
"""
CTMM Code Optimization Tool
Automatically fixes common issues found by the error analyzer.
"""

import re
import subprocess
import sys
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class CTMMOptimizer:
    def __init__(self):
        self.fixes_applied = 0
        
    def optimize_converted_documents(self):
        """Optimize all converted LaTeX documents."""
        logger.info("Starting optimization of converted documents...")
        
        converted_dir = Path("converted")
        if not converted_dir.exists():
            logger.error("Converted directory not found")
            return False
        
        tex_files = list(converted_dir.glob("*.tex"))
        logger.info(f"Found {len(tex_files)} files to optimize")
        
        for tex_file in tex_files:
            self._optimize_file(tex_file)
        
        logger.info(f"Optimization complete. Applied {self.fixes_applied} fixes")
        return True
    
    def _optimize_file(self, file_path: Path):
        """Optimize a single LaTeX file."""
        logger.info(f"Optimizing {file_path.name}...")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Fix checkbox commands
            content = self._fix_checkboxes(content)
            
            # Fix color usage
            content = self._fix_colors(content)
            
            # Fix table environments
            content = self._fix_tables(content)
            
            # Fix spacing issues
            content = self._fix_spacing(content)
            
            # Only write if changes were made
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                logger.info(f"✓ Optimized {file_path.name}")
            else:
                logger.debug(f"No changes needed for {file_path.name}")
                
        except Exception as e:
            logger.error(f"Failed to optimize {file_path.name}: {e}")
    
    def _fix_checkboxes(self, content: str) -> str:
        """Fix checkbox commands to use CTMM standard."""
        # Replace various checkbox representations
        fixes = [
            (r'\$\\square\$', r'\\checkbox'),
            (r'\\square', r'\\checkbox'),
            (r'\$\\Box\$', r'\\checkbox'),
            (r'\\Box', r'\\checkbox'),
            (r'\$\\blacksquare\$', r'\\checkedbox'),
            (r'\\blacksquare', r'\\checkedbox'),
            # Fix inline math checkboxes
            (r'\$\\checkbox\$', r'\\checkbox'),
        ]
        
        for pattern, replacement in fixes:
            old_content = content
            content = re.sub(pattern, replacement, content)
            if content != old_content:
                self.fixes_applied += content.count(replacement) - old_content.count(replacement)
        
        return content
    
    def _fix_colors(self, content: str) -> str:
        """Fix color usage to prefer CTMM colors."""
        # Replace common colors with CTMM equivalents
        color_fixes = [
            (r'\\textcolor\{blue\}', r'\\textcolor{ctmmBlue}'),
            (r'\\textcolor\{orange\}', r'\\textcolor{ctmmOrange}'),
            (r'\\textcolor\{green\}', r'\\textcolor{ctmmGreen}'),
            (r'\\textcolor\{purple\}', r'\\textcolor{ctmmPurple}'),
        ]
        
        for pattern, replacement in color_fixes:
            old_content = content
            content = re.sub(pattern, replacement, content)
            if content != old_content:
                self.fixes_applied += 1
        
        return content
    
    def _fix_tables(self, content: str) -> str:
        """Fix table environments for better compatibility."""
        # Replace tabular with tabularx where appropriate
        # This is a simple heuristic - tables with many columns benefit from tabularx
        lines = content.split('\\n')
        modified = False
        
        for i, line in enumerate(lines):
            if '\\begin{tabular}' in line and '{|' in line:
                # Count columns
                column_spec = re.search(r'\\begin\{tabular\}\{([^}]+)\}', line)
                if column_spec and column_spec.group(1).count('|') > 3:
                    # Replace with tabularx for tables with many columns
                    lines[i] = line.replace('\\begin{tabular}', '\\begin{tabularx}{\\textwidth}')
                    modified = True
                    self.fixes_applied += 1
            elif '\\end{tabular}' in line and modified:
                lines[i] = line.replace('\\end{tabular}', '\\end{tabularx}')
        
        return '\\n'.join(lines)
    
    def _fix_spacing(self, content: str) -> str:
        """Fix spacing issues."""
        # Fix excessive vertical spacing
        content = re.sub(r'\\vspace\{([0-9]+)cm\}', lambda m: f'\\vspace{{{min(int(m.group(1)), 3)}cm}}', content)
        
        # Fix multiple consecutive newlines
        content = re.sub(r'\\n\\s*\\n\\s*\\n+', r'\\n\\n', content)
        
        return content

def main():
    """Run the CTMM optimization tool."""
    optimizer = CTMMOptimizer()
    
    # Optimize converted documents
    success = optimizer.optimize_converted_documents()
    
    if success:
        logger.info("Running post-optimization build test...")
        # Test build after optimization
        result = subprocess.run(['python3', 'ctmm_build.py'], capture_output=True, text=True)
        if result.returncode == 0:
            logger.info("✓ Build test passed after optimization")
        else:
            logger.warning("⚠ Build test failed after optimization, manual review needed")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())