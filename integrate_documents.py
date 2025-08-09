#!/usr/bin/env python3
"""
CTMM Document Integration System
Integrates converted documents into the main LaTeX document structure.
"""

import re
from pathlib import Path
import logging
import shutil

logger = logging.getLogger(__name__)

def integrate_converted_documents():
    """Integrate key converted documents into main.tex."""
    
    # Select key documents to integrate (avoiding overwhelming the system)
    key_documents = [
        "Tool 23 Trigger Management",
        "Tool 22 Safewords Signalsysteme CTMM",
        "Matching Matrix Trigger Reaktion Intervention CTMM",
        "Matching Matrix Wochenlogik",
        "Trigger Notfallkarten"
    ]
    
    # Read current main.tex
    main_tex_path = Path("main.tex")
    with open(main_tex_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the end of the arbeitsblätter section
    arbeitsblatt_section = content.find("\\input{modules/demo-interactive}")
    if arbeitsblatt_section == -1:
        print("Could not find demo-interactive module to insert after")
        return False
    
    # Find the end of that line
    insert_point = content.find('\n', arbeitsblatt_section) + 1
    
    # Create new section for converted documents
    new_section = """
\\newpage
\\part*{KAPITEL 6: KONVERTIERTE THERAPIE-TOOLS}
\\addcontentsline{toc}{part}{KAPITEL 6: KONVERTIERTE THERAPIE-TOOLS}

% Key converted therapy documents
"""
    
    # Add input commands for key documents
    for doc_name in key_documents:
        converted_path = f"converted/{doc_name}"
        if Path(f"{converted_path}.tex").exists():
            new_section += f"\\input{{{converted_path}}}\n"
            print(f"Added {doc_name} to main.tex")
    
    new_section += "\n"
    
    # Insert the new section
    new_content = content[:insert_point] + new_section + content[insert_point:]
    
    # Backup original
    shutil.copy2(main_tex_path, "main.tex.backup")
    
    # Write updated content
    with open(main_tex_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Integrated {len(key_documents)} converted documents into main.tex")
    print("Backup saved as main.tex.backup")
    return True

if __name__ == "__main__":
    integrate_converted_documents()