#!/usr/bin/env python3
"""
Verification script to ensure repository is ready for GitHub Copilot reviews.

This script checks for common issues that prevent GitHub Copilot from
reviewing files in pull requests.
"""

import os
import yaml
import json
from pathlib import Path

def check_binary_files():
    """Check for binary files that might interfere with Copilot."""
    print("🔍 Checking for binary files...")
    
    binary_extensions = ['.pdf', '.docx', '.doc', '.xlsx', '.xls', '.pptx', '.ppt']
    binary_files = []
    
    for root, dirs, files in os.walk('.'):
        # Skip .git directory
        if '.git' in dirs:
            dirs.remove('.git')
        
        for file in files:
            file_path = os.path.join(root, file)
            if any(file.lower().endswith(ext) for ext in binary_extensions):
                binary_files.append(file_path)
    
    if binary_files:
        print(f"❌ Found {len(binary_files)} binary files:")
        for file in binary_files:
            print(f"   {file}")
        return False
    else:
        print("✅ No binary files found")
        return True

def check_workflow_syntax():
    """Check GitHub Actions workflow files for syntax errors."""
    print("\n🔍 Checking GitHub Actions workflows...")
    
    workflow_dir = Path('.github/workflows')
    if not workflow_dir.exists():
        print("⚠️  No .github/workflows directory found")
        return True
    
    workflow_files = list(workflow_dir.glob('*.yml')) + list(workflow_dir.glob('*.yaml'))
    if not workflow_files:
        print("⚠️  No workflow files found")
        return True
    
    all_valid = True
    for workflow_file in workflow_files:
        try:
            with open(workflow_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse YAML
            yaml.safe_load(content)
            print(f"✅ {workflow_file.name}: Valid YAML syntax")
            
        except yaml.YAMLError as e:
            print(f"❌ {workflow_file.name}: YAML syntax error - {e}")
            all_valid = False
        except Exception as e:
            print(f"❌ {workflow_file.name}: Error reading file - {e}")
            all_valid = False
    
    return all_valid

def check_text_file_encoding():
    """Check that text files are properly encoded."""
    print("\n🔍 Checking text file encoding...")
    
    text_extensions = ['.tex', '.py', '.md', '.yml', '.yaml', '.json', '.txt']
    problematic_files = []
    
    for root, dirs, files in os.walk('.'):
        # Skip .git directory
        if '.git' in dirs:
            dirs.remove('.git')
        
        for file in files:
            if any(file.lower().endswith(ext) for ext in text_extensions):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        f.read()
                except UnicodeDecodeError:
                    problematic_files.append(file_path)
                except Exception:
                    # Skip files that can't be read for other reasons
                    pass
    
    if problematic_files:
        print(f"❌ Found {len(problematic_files)} files with encoding issues:")
        for file in problematic_files:
            print(f"   {file}")
        return False
    else:
        print("✅ All text files have proper UTF-8 encoding")
        return True

def check_file_sizes():
    """Check for very large files that might cause issues."""
    print("\n🔍 Checking file sizes...")
    
    large_files = []
    size_limit = 1024 * 1024  # 1MB limit
    
    for root, dirs, files in os.walk('.'):
        # Skip .git directory
        if '.git' in dirs:
            dirs.remove('.git')
        
        for file in files:
            file_path = os.path.join(root, file)
            try:
                size = os.path.getsize(file_path)
                if size > size_limit:
                    large_files.append((file_path, size))
            except OSError:
                pass
    
    if large_files:
        print(f"⚠️  Found {len(large_files)} large files (>1MB):")
        for file_path, size in large_files:
            size_mb = size / (1024 * 1024)
            print(f"   {file_path}: {size_mb:.1f}MB")
        return len(large_files) == 0  # Return False if any large files
    else:
        print("✅ No large files found")
        return True

def check_gitignore():
    """Check that .gitignore properly excludes binary files."""
    print("\n🔍 Checking .gitignore configuration...")
    
    if not os.path.exists('.gitignore'):
        print("❌ No .gitignore file found")
        return False
    
    with open('.gitignore', 'r', encoding='utf-8') as f:
        gitignore_content = f.read()
    
    required_patterns = ['*.pdf', '*.docx', '*.doc']
    missing_patterns = []
    
    for pattern in required_patterns:
        if pattern not in gitignore_content:
            missing_patterns.append(pattern)
    
    if missing_patterns:
        print(f"❌ Missing .gitignore patterns: {missing_patterns}")
        return False
    else:
        print("✅ .gitignore properly configured for binary files")
        return True

def main():
    """Main verification function."""
    print("=" * 60)
    print("GITHUB COPILOT READINESS VERIFICATION")
    print("=" * 60)
    
    checks = [
        ("Binary Files", check_binary_files),
        ("Workflow Syntax", check_workflow_syntax),
        ("Text File Encoding", check_text_file_encoding),
        ("File Sizes", check_file_sizes),
        (".gitignore Configuration", check_gitignore),
    ]
    
    results = {}
    for check_name, check_func in checks:
        results[check_name] = check_func()
    
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    
    all_passed = True
    for check_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} {check_name}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 REPOSITORY IS READY FOR GITHUB COPILOT REVIEWS")
        print("All checks passed. Copilot should be able to review files in pull requests.")
    else:
        print("⚠️  REPOSITORY NEEDS FIXES FOR COPILOT COMPATIBILITY")
        print("Some issues need to be resolved before Copilot can review files properly.")
    print("=" * 60)
    
    return all_passed

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)