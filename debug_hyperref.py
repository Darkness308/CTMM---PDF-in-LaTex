#!/usr/bin/env python3
"""
Simple test to verify the hyperref conditional logic.
"""

def analyze_hyperref_logic():
    """Analyze the hyperref conditional logic in detail."""
    
    with open('style/form-elements.sty', 'r') as f:
        content = f.read()
    
    lines = content.split('\n')
    
    print("HYPERREF CONDITIONAL LOGIC ANALYSIS")
    print("=" * 60)
    
    # Find the conditional block
    start_line = -1
    for i, line in enumerate(lines):
        if r'\@ifpackageloaded{hyperref}{%' in line:
            start_line = i
            break
    
    if start_line == -1:
        print("❌ Conditional logic not found!")
        return
    
    print(f"Found conditional logic starting at line {start_line + 1}")
    print("\nExact code:")
    print("-" * 40)
    
    # Print the relevant lines
    for i in range(start_line, min(start_line + 10, len(lines))):
        line_num = i + 1
        line_content = lines[i]
        print(f"{line_num:2d}: {line_content}")
        
        # Analyze each line
        if r'\RequirePackage{hyperref}' in line_content:
            # Determine which branch this is in
            if i <= start_line + 2:  # Rough estimate for true branch
                print(f"    ^^^ ❌ PROBLEM: Loading hyperref in TRUE branch (already loaded)")
            else:
                print(f"    ^^^ ✅ OK: Loading hyperref in FALSE branch (not loaded)")
    
    print("\nLogic Analysis:")
    print("-" * 40)
    
    # Check for hyperref loading occurrences within the conditional
    hyperref_loads = []
    for i in range(start_line, min(start_line + 8, len(lines))):
        if r'\RequirePackage{hyperref}' in lines[i]:
            hyperref_loads.append(i + 1)
    
    print(f"Lines with \\RequirePackage{{hyperref}}: {hyperref_loads}")
    
    if len(hyperref_loads) == 0:
        print("❌ ERROR: No hyperref loading found in conditional")
    elif len(hyperref_loads) == 1:
        load_line = hyperref_loads[0] - 1
        # Check if it's in the false branch (should be after the }{%)
        context_lines = lines[start_line:load_line+1]
        false_branch_marker = False
        for line in context_lines:
            if '}{% ' in line or line.strip() == '}{%':
                false_branch_marker = True
        
        if false_branch_marker:
            print("✅ CORRECT: Hyperref only loaded in FALSE branch (when not already present)")
        else:
            print("❌ PROBLEM: Hyperref loaded in TRUE branch (when already present)")
    else:
        print(f"❌ PROBLEM: Hyperref loaded {len(hyperref_loads)} times in conditional")

if __name__ == "__main__":
    analyze_hyperref_logic()