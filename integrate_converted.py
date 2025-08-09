#!/usr/bin/env python3
"""
CTMM Integration Tool
Integrates converted LaTeX files into the main document build system.

This script helps incorporate the clean converted LaTeX files into 
the CTMM build process, creating a comprehensive therapy document.
"""

import os
import re
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def create_integrated_content():
    """
    Create an integrated LaTeX file that includes all converted content.
    """
    converted_dir = Path("converted")
    
    if not converted_dir.exists():
        logger.error("Converted directory not found. Run convert_documents.py first.")
        return False
    
    # Get all converted .tex files
    tex_files = sorted(converted_dir.glob("*.tex"))
    
    if not tex_files:
        logger.error("No converted .tex files found.")
        return False
    
    # Create integrated content file
    integrated_content = []
    
    # Add header
    integrated_content.append("% Integrated CTMM Therapy Materials")
    integrated_content.append("% Auto-generated from converted documents")
    integrated_content.append("")
    
    # Process each converted file
    for tex_file in tex_files:
        logger.info(f"Processing {tex_file.name}...")
        
        try:
            with open(tex_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Clean up the content for integration
            # Remove document-level commands that shouldn't be in included files
            content = re.sub(r'\\documentclass.*?\n', '', content)
            content = re.sub(r'\\usepackage.*?\n', '', content)
            content = re.sub(r'\\begin{document}', '', content)
            content = re.sub(r'\\end{document}', '', content)
            content = re.sub(r'\\maketitle', '', content)
            
            # Add file header
            integrated_content.append(f"% ===== {tex_file.stem} =====")
            integrated_content.append("")
            integrated_content.append(content.strip())
            integrated_content.append("")
            integrated_content.append("\\newpage")
            integrated_content.append("")
            
        except Exception as e:
            logger.error(f"Error processing {tex_file.name}: {e}")
            continue
    
    # Write integrated file
    output_file = Path("modules/converted-content.tex")
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(integrated_content))
        
        logger.info(f"✓ Created integrated content file: {output_file}")
        return True
        
    except Exception as e:
        logger.error(f"Error writing integrated content: {e}")
        return False


def update_main_tex():
    """
    Update main.tex to include the converted content.
    """
    main_tex_path = Path("main.tex")
    
    if not main_tex_path.exists():
        logger.error("main.tex not found!")
        return False
    
    try:
        with open(main_tex_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if converted content is already included
        if "converted-content" in content:
            logger.info("Converted content already included in main.tex")
            return True
        
        # Find a good place to insert the content
        # Look for the end of other module includes
        insert_pattern = r'(\\input\{modules/[^}]+\}\s*\n)'
        matches = list(re.finditer(insert_pattern, content))
        
        if matches:
            # Insert after the last module include
            last_match = matches[-1]
            insert_pos = last_match.end()
            
            new_line = "\\input{modules/converted-content}  % Converted therapy materials\n"
            content = content[:insert_pos] + new_line + content[insert_pos:]
            
            with open(main_tex_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info("✓ Added converted content to main.tex")
            return True
        else:
            logger.warning("Could not find insertion point in main.tex")
            return False
            
    except Exception as e:
        logger.error(f"Error updating main.tex: {e}")
        return False


def main():
    """
    Main integration process.
    """
    logger.info("🔗 Starting CTMM Integration...")
    
    # Step 1: Create integrated content file
    if not create_integrated_content():
        logger.error("Failed to create integrated content")
        return 1
    
    # Step 2: Update main.tex to include converted content
    if not update_main_tex():
        logger.error("Failed to update main.tex")
        return 1
    
    logger.info("")
    logger.info("🎯 Integration Complete!")
    logger.info("   ✓ Converted content integrated")
    logger.info("   ✓ main.tex updated")
    logger.info("   📁 Check modules/converted-content.tex")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())