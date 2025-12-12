#!/usr/bin/env python3
"""
Validate GitHub Actions workflow files for version pinning best practices.
Checks for @latest tag usage and recommends specific version pinning.
"""

import os
import re
import yaml

def validate_workflow_versions():
    """Validate that all GitHub Actions use specific version tags, not @latest."""
    
    print("=" * 70)
    print("GitHub Actions Version Pinning Validation - Issue #607")
    print("=" * 70)
    print("Checking for @latest tag usage and version pinning best practices\n")
    
    # Define the workflow files to check
    workflow_files = [
        '.github/workflows/latex-build.yml',
        '.github/workflows/latex-validation.yml', 
        '.github/workflows/pr-validation.yml',
        '.github/workflows/static.yml'
    ]
    
    # In test environments, also check any test workflow files
    if os.path.exists('.github/workflows/test.yml'):
        workflow_files.append('.github/workflows/test.yml')
    
    print(f"Checking {len(workflow_files)} workflow files...\n")
    
    all_pinned = True
    results = []
    
    for file_path in workflow_files:
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            all_pinned = False
            continue
            
        print(f"--- Analyzing {file_path} ---")
        
        # Read the file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all uses: actions/xyz@version patterns
        uses_pattern = r'uses:\s+([^@]+)@([^\s\n]+)'
        uses_matches = re.findall(uses_pattern, content)
        
        latest_found = False
        unpinned_actions = []
        
        for action, version in uses_matches:
            if version == 'latest':
                latest_found = True
                unpinned_actions.append(f"{action}@{version}")
                print(f"❌ Found @latest usage: {action}@{version}")
            elif version.startswith('v') and re.match(r'^v\d+(\.\d+)*$', version):
                print(f"✅ Properly pinned: {action}@{version}")
            else:
                print(f"⚠️  Non-standard version: {action}@{version}")
        
        if latest_found:
            all_pinned = False
            results.append((file_path, False, f"Uses @latest: {', '.join(unpinned_actions)}"))
        else:
            results.append((file_path, True, "All actions properly version-pinned"))
    
    # Summary
    print("\n" + "=" * 70)
    print("VALIDATION SUMMARY")
    print("=" * 70)
    
    for file_path, is_pinned, message in results:
        status = "✅ PASS" if is_pinned else "❌ FAIL"
        print(f"{status} {os.path.basename(file_path)}: {message}")
    
    if all_pinned:
        print("\n🎉 ALL ACTIONS PROPERLY VERSION-PINNED")
        print("No @latest tags found. All GitHub Actions use specific versions.")
        print("This ensures reproducible builds and prevents unexpected failures.")
    else:
        print("\n⚠️  SOME ACTIONS USE @latest TAGS")
        print("Replace @latest with specific version tags for reproducible builds.")
        print("Example: dante-ev/latex-action@latest → dante-ev/latex-action@v0.2")
    
    print(f"\nStatus: {'SUCCESS' if all_pinned else 'NEEDS_FIXES'}")
    return all_pinned

if __name__ == "__main__":
    validate_workflow_versions()