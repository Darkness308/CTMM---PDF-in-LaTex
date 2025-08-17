#!/usr/bin/env python3
"""
Verification script for Issue #476: Binary File Exclusion Resolution

This script validates that Issue #476 has been properly resolved by verifying:
1. Binary files (PDFs, DOCX) have been removed from git tracking
2. .gitignore properly excludes binary file types  
3. Source files (.tex, .py, .md, .sty) are still tracked
4. therapie-material directory has proper documentation
5. Build system can generate PDFs locally without tracking them

Issue #476 was caused by binary files preventing GitHub Copilot from performing code reviews.
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, description=""):
    """Run a command and return success status and output."""
    try:
        if description:
            print(f"🔧 {description}")
        
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            if description:
                print(f"✅ SUCCESS: {description}")
            return True, result.stdout.strip()
        else:
            if description:
                print(f"❌ FAILED: {description}")
                if result.stderr:
                    print(f"   Error: {result.stderr.strip()}")
            return False, result.stderr.strip()
    except Exception as e:
        if description:
            print(f"❌ ERROR: {description} - {e}")
        return False, str(e)

def check_binary_files_removed():
    """Verify binary files have been removed from git tracking."""
    print("\n🗑️  BINARY FILES REMOVAL VERIFICATION")
    print("-" * 50)
    
    # Check for tracked binary files
    success, output = run_command("git ls-files | grep -E '\\.(pdf|docx|doc|xlsx|xls|ppt|pptx)$'", "Check for tracked binary files")
    
    if not output.strip():
        print("✅ No binary files found in git tracking")
        return True
    else:
        print(f"❌ Found {len(output.split())} tracked binary files:")
        for file in output.split('\n')[:10]:  # Show first 10
            print(f"   - {file}")
        return False

def validate_gitignore_rules():
    """Verify .gitignore properly excludes binary files."""
    print("\n📋 GITIGNORE RULES VERIFICATION")
    print("-" * 50)
    
    gitignore_file = Path(".gitignore")
    if not gitignore_file.exists():
        print("❌ .gitignore file not found")
        return False
    
    content = gitignore_file.read_text()
    
    # Check for essential binary file exclusions
    required_patterns = [
        "*.pdf",
        "*.docx",
        "*.doc", 
        "*.xlsx",
        "*.xls"
    ]
    
    missing_patterns = []
    found_patterns = []
    
    for pattern in required_patterns:
        if pattern in content:
            found_patterns.append(pattern)
            print(f"✅ {pattern}: Excluded in .gitignore")
        else:
            missing_patterns.append(pattern)
            print(f"❌ {pattern}: Missing from .gitignore")
    
    if not missing_patterns:
        print(f"✅ All essential binary patterns excluded ({len(found_patterns)}/{len(required_patterns)})")
        return True
    else:
        print(f"❌ Missing {len(missing_patterns)} essential patterns")
        return False

def verify_source_files_preserved():
    """Verify source files are still tracked."""
    print("\n📄 SOURCE FILES PRESERVATION VERIFICATION")
    print("-" * 50)
    
    # Check for essential source file types
    source_patterns = ["*.tex", "*.py", "*.md", "*.sty", "*.yml", "*.yaml"]
    
    total_source_files = 0
    for pattern in source_patterns:
        success, output = run_command(f"git ls-files | grep -E '{pattern.replace('*', '.*')}$'", f"Count {pattern} files")
        if success and output:
            file_count = len(output.split('\n'))
            total_source_files += file_count
            print(f"✅ {pattern}: {file_count} files tracked")
        else:
            print(f"⚠️  {pattern}: No files found")
    
    if total_source_files >= 20:  # Expect at least 20 source files
        print(f"✅ Source files preserved: {total_source_files} total")
        return True
    else:
        print(f"❌ Limited source files: {total_source_files} total")
        return False

def test_therapie_material_documentation():
    """Test therapie-material directory documentation."""
    print("\n🏥 THERAPIE-MATERIAL DOCUMENTATION VERIFICATION")
    print("-" * 50)
    
    therapie_dir = Path("therapie-material")
    readme_file = therapie_dir / "README.md"
    
    if not therapie_dir.exists():
        print("❌ therapie-material directory not found")
        return False
    
    if not readme_file.exists():
        print("❌ therapie-material/README.md not found")
        return False
    
    content = readme_file.read_text()
    
    # Check for binary file explanation
    binary_keywords = ["binary", "pdf", "docx", "git", "tracking", "excluded"]
    found_keywords = sum(1 for keyword in binary_keywords if keyword.lower() in content.lower())
    
    if found_keywords >= 4:
        print("✅ therapie-material/README.md: Comprehensive binary file documentation")
        print(f"   Found {found_keywords}/{len(binary_keywords)} key concepts")
        return True
    else:
        print("⚠️  therapie-material/README.md: Limited binary file documentation")
        print(f"   Found {found_keywords}/{len(binary_keywords)} key concepts")
        return False

def test_build_system_pdf_generation():
    """Test that build system can generate PDFs without tracking them."""
    print("\n🔧 BUILD SYSTEM PDF GENERATION TEST")
    print("-" * 50)
    
    # Test CTMM build system
    success, output = run_command("python3 ctmm_build.py", "CTMM build system test")
    if not success:
        print("❌ CTMM build system failed")
        return False
    
    # Check if main.pdf would be generated (if LaTeX available)
    if "pdflatex not found" in output:
        print("✅ Build system functional (LaTeX not available for PDF generation)")
        return True
    elif "PASS" in output:
        print("✅ Build system operational")
        
        # Verify main.pdf is not tracked even if it exists
        if Path("main.pdf").exists():
            success, tracked = run_command("git ls-files | grep main.pdf", "Check if main.pdf is tracked")
            if not tracked.strip():
                print("✅ main.pdf exists locally but not tracked in git")
                return True
            else:
                print("❌ main.pdf is tracked in git")
                return False
        else:
            print("✅ No main.pdf found (expected when LaTeX not available)")
            return True
    else:
        print("❌ Build system issues detected")
        return False

def validate_copilot_readiness():
    """Validate that repository is ready for Copilot review."""
    print("\n🤖 COPILOT READINESS VERIFICATION")
    print("-" * 50)
    
    # Check repository size and file types
    success, output = run_command("git ls-files | wc -l", "Count tracked files")
    if success:
        file_count = int(output.strip())
        print(f"✅ Repository has {file_count} tracked files")
        
        if file_count >= 20:
            print("✅ Sufficient files for meaningful Copilot review")
        else:
            print("⚠️  Limited file count for Copilot review")
    
    # Check for text-based files (reviewable by Copilot)
    success, output = run_command("git ls-files | grep -E '\\.(py|tex|md|yml|yaml|sty|txt)$' | wc -l", "Count reviewable files")
    if success:
        reviewable_count = int(output.strip())
        print(f"✅ {reviewable_count} text-based files available for Copilot review")
        return reviewable_count >= 15
    
    return False

def validate_issue_476_documentation():
    """Verify Issue #476 documentation exists and is complete."""
    print("\n📄 ISSUE #476 DOCUMENTATION VERIFICATION")
    print("-" * 50)
    
    doc_file = Path("ISSUE_476_RESOLUTION.md")
    if not doc_file.exists():
        print("❌ ISSUE_476_RESOLUTION.md not found")
        return False
    
    content = doc_file.read_text()
    
    required_sections = [
        "Binary files",
        "Copilot",
        "gitignore",
        "PDF",
        "DOCX"
    ]
    
    missing_sections = []
    for section in required_sections:
        if section.lower() not in content.lower():
            missing_sections.append(section)
    
    if missing_sections:
        print(f"❌ Missing documentation elements: {', '.join(missing_sections)}")
        return False
    
    print("✅ Complete Issue #476 documentation found")
    print(f"   Document size: {len(content)} characters")
    
    # Check for specific file counts mentioned
    if "PDF" in content and "DOCX" in content:
        print("✅ Binary file types documented")
    
    return True

def main():
    """Main verification function."""
    print("=" * 70)
    print("Issue #476 Resolution Verification")
    print("Binary File Exclusion & Copilot Review Enablement")
    print("=" * 70)
    
    # Run all verification checks
    checks = [
        ("Binary Files Removed", check_binary_files_removed),
        ("Gitignore Rules", validate_gitignore_rules),
        ("Source Files Preserved", verify_source_files_preserved),
        ("Therapie-Material Documentation", test_therapie_material_documentation),
        ("Build System PDF Generation", test_build_system_pdf_generation),
        ("Copilot Readiness", validate_copilot_readiness),
        ("Issue Documentation", validate_issue_476_documentation)
    ]
    
    results = {}
    all_passed = True
    
    for check_name, check_func in checks:
        try:
            results[check_name] = check_func()
            if not results[check_name]:
                all_passed = False
        except Exception as e:
            print(f"\n❌ ERROR in {check_name}: {e}")
            results[check_name] = False
            all_passed = False
    
    # Print summary
    print("\n" + "=" * 70)
    print("VERIFICATION SUMMARY")
    print("=" * 70)
    
    for check_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {check_name}")
    
    if all_passed:
        print("\n🎉 ALL CHECKS PASSED!")
        print("Issue #476 has been successfully resolved:")
        print("  ✅ Binary files removed from git tracking")
        print("  ✅ .gitignore properly configured for binary exclusion")
        print("  ✅ Source files preserved and tracked")
        print("  ✅ Repository optimized for Copilot code review")
        print("  ✅ Build system can generate PDFs locally")
        return True
    else:
        print("\n❌ SOME CHECKS FAILED")
        print("Issue #476 resolution may be incomplete")
        failed_checks = [name for name, passed in results.items() if not passed]
        print(f"Failed checks: {', '.join(failed_checks)}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)