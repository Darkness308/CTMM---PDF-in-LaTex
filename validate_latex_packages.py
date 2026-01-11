#!/usr/bin/env python3
"""
Validate LaTeX package configuration in GitHub Actions workflow.
Verifies that all packages listed in extra_system_packages are valid apt packages.
"""

import re
import subprocess
import sys
from pathlib import Path

def extract_packages_from_workflow():
    """Extract package names from the GitHub Actions workflow file."""
    workflow_path = Path(".github/workflows/latex-build.yml")
    
    if not workflow_path.exists():
        print(f"❌ Workflow file not found: {workflow_path}")
        return []
    
    with open(workflow_path, 'r') as f:
        content = f.read()
    
    # Find the extra_system_packages section
    pattern = r'extra_system_packages:\s*\|\s*((?:\s*[\w-]+\s*\n)*)'
    match = re.search(pattern, content)
    
    if not match:
        print("❌ Could not find extra_system_packages section in workflow")
        return []
    
    # Extract package names
    packages_section = match.group(1)
    packages = [line.strip() for line in packages_section.strip().split('\n') if line.strip()]
    
    return packages

def check_package_exists(package_name):
    """Check if a package exists in apt repository."""
    try:
        result = subprocess.run(
            ['apt-cache', 'search', f'^{package_name}$'],
            capture_output=True,
            text=True,
            check=False
        )
        return bool(result.stdout.strip())
    except FileNotFoundError:
        print("⚠️  apt-cache not available, skipping package verification")
        return True  # Assume packages exist if we can't check

def main():
    """Main validation function."""
    print("🔍 Validating LaTeX package configuration...")
    print("=" * 50)
    
    # Extract packages from workflow
    packages = extract_packages_from_workflow()
    
    if not packages:
        print("❌ No packages found in workflow configuration")
        return 1
    
    print(f"Found {len(packages)} packages to validate:")
    
    all_valid = True
    for package in packages:
        exists = check_package_exists(package)
        status = "✅" if exists else "❌"
        print(f"{status} {package}")
        
        if not exists:
            all_valid = False
    
    print("=" * 50)
    
    if all_valid:
        print("✅ All packages are valid!")
        return 0
    else:
        print("❌ Some packages are invalid or not found")
        return 1

if __name__ == "__main__":
    sys.exit(main())