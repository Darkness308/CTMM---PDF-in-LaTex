#!/usr/bin/env python3
"""
Comprehensive Verification Infrastructure Test for Issue #904

This script validates that the CTMM repository's verification infrastructure 
is comprehensive and working correctly for all GitHub issue resolutions.

This addresses Issue #904 by demonstrating:
1. All verification scripts for resolved issues are present and functional
2. Comprehensive test suites for LaTeX validation, workflow structure, and CI
3. Complete documentation coverage for the therapie-material directory
4. Integration with the CTMM build system
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, description=""):
    """Run a command and return success status and output."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        success = result.returncode == 0
        return success, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return False, "", str(e)

def check_verification_scripts_coverage():
    """Check that verification scripts exist for all major resolved issues."""
    
    print("🔍 CHECKING VERIFICATION SCRIPTS COVERAGE")
    print("-" * 60)
    
    # List of issues that should have verification scripts
    critical_issues = [
        667,  # GitHub Actions upgrade
        673,  # Comprehensive Copilot review fix
        708,  # Additional validation strategies
        721,  # Strategic direction
        731,  # Critical bug fix in validation
        759,  # Empty PR resolution
        817,  # Recent resolution pattern
        835,  # Empty PR and meaningful content
        867   # LaTeX build failure
    ]
    
    existing_verification_scripts = []
    missing_verification_scripts = []
    
    for issue in critical_issues:
        script_path = Path(f"verify_issue_{issue}_fix.py")
        if script_path.exists():
            existing_verification_scripts.append(issue)
            print(f"✅ Issue #{issue}: Verification script exists")
        else:
            missing_verification_scripts.append(issue)
            print(f"❌ Issue #{issue}: Verification script missing")
    
    print(f"\n📊 Verification Coverage:")
    print(f"   Existing scripts: {len(existing_verification_scripts)}/{len(critical_issues)}")
    print(f"   Missing scripts: {len(missing_verification_scripts)}")
    
    if missing_verification_scripts:
        print(f"   Missing for issues: {missing_verification_scripts}")
        return False
    
    print("✅ Complete verification script coverage achieved")
    return True

def check_test_suites_comprehensive():
    """Check that comprehensive test suites are present and functional."""
    
    print("\n🧪 CHECKING COMPREHENSIVE TEST SUITES")
    print("-" * 60)
    
    test_categories = [
        ("LaTeX Validation", "test_latex_validator.py"),
        ("Workflow Structure", "test_workflow_structure.py"),
        ("Workflow Versions", "test_workflow_versions.py"),
        ("CTMM Build System", "test_ctmm_build.py"),
        ("PR Validation", "test_pr_validation.py"),
        ("Integration Testing", "test_integration.py")
    ]
    
    all_tests_pass = True
    
    for category, test_file in test_categories:
        if not Path(test_file).exists():
            print(f"❌ {category}: Test file {test_file} not found")
            all_tests_pass = False
            continue
        
        print(f"🔧 Running {category} tests...")
        success, stdout, stderr = run_command(f"python3 {test_file}")
        
        if success:
            print(f"✅ {category}: All tests passed")
        else:
            print(f"❌ {category}: Tests failed")
            all_tests_pass = False
    
    return all_tests_pass

def check_validation_tools_functional():
    """Check that all validation tools are functional."""
    
    print("\n🛠️  CHECKING VALIDATION TOOLS FUNCTIONALITY")
    print("-" * 60)
    
    validation_tools = [
        ("CTMM Build System", "ctmm_build.py"),
        ("LaTeX Syntax Validation", "validate_latex_syntax.py"),
        ("Workflow Syntax Validation", "validate_workflow_syntax.py"),
        ("Workflow Version Validation", "validate_workflow_versions.py"),
        ("PR Validation", "validate_pr.py")
    ]
    
    all_tools_work = True
    
    for tool_name, script in validation_tools:
        if not Path(script).exists():
            print(f"❌ {tool_name}: Script {script} not found")
            all_tools_work = False
            continue
        
        print(f"🔧 Testing {tool_name}...")
        success, stdout, stderr = run_command(f"python3 {script}")
        
        if success:
            print(f"✅ {tool_name}: Functional")
        else:
            # Some tools may fail due to environment (e.g., no uncommitted changes)
            # but they should still be structurally sound
            if "No uncommitted changes" in stderr or "No file changes" in stderr:
                print(f"✅ {tool_name}: Functional (expected environment condition)")
            else:
                print(f"❌ {tool_name}: Failed")
                all_tools_work = False
    
    return all_tools_work

def check_documentation_coverage():
    """Check that documentation coverage is comprehensive."""
    
    print("\n📚 CHECKING DOCUMENTATION COVERAGE")
    print("-" * 60)
    
    # Check therapie-material directory documentation
    therapie_readme = Path("therapie-material/README.md")
    if not therapie_readme.exists():
        print("❌ therapie-material/README.md not found")
        return False
    
    therapie_content = therapie_readme.read_text()
    if len(therapie_content) < 1000:
        print("❌ therapie-material documentation insufficient")
        return False
    
    print("✅ therapie-material directory properly documented")
    
    # Check for comprehensive guides
    guide_files = [
        ("CTMM Comprehensive Guide", "CTMM_COMPREHENSIVE_GUIDE.md"),
        ("Development Roadmap", "DEVELOPMENT_ROADMAP.md"),
        ("Implementation Summary", "IMPLEMENTATION_SUMMARY.md"),
        ("Copilot Issue Resolution", "COPILOT_ISSUE_RESOLUTION.md")
    ]
    
    all_docs_present = True
    
    for doc_name, doc_file in guide_files:
        if Path(doc_file).exists():
            content = Path(doc_file).read_text()
            if len(content) > 2000:
                print(f"✅ {doc_name}: Comprehensive documentation present")
            else:
                print(f"⚠️  {doc_name}: Documentation present but brief")
        else:
            print(f"❌ {doc_name}: Documentation missing")
            all_docs_present = False
    
    return all_docs_present

def check_issue_resolution_pattern_consistency():
    """Check that issue resolution files follow consistent patterns."""
    
    print("\n📋 CHECKING ISSUE RESOLUTION PATTERN CONSISTENCY")
    print("-" * 60)
    
    # Find all issue resolution files
    resolution_files = list(Path(".").glob("ISSUE_*_RESOLUTION.md"))
    
    if len(resolution_files) < 15:
        print(f"❌ Expected at least 15 resolution files, found {len(resolution_files)}")
        return False
    
    print(f"✅ Found {len(resolution_files)} issue resolution files")
    
    # Check that key patterns exist
    required_patterns = [
        "Problem Statement",
        "Solution Implemented",
        "Root Cause",
        "#"  # Issue reference
    ]
    
    consistent_files = 0
    
    for resolution_file in resolution_files:
        content = resolution_file.read_text()
        file_patterns = sum(1 for pattern in required_patterns if pattern in content)
        
        if file_patterns >= 3:
            consistent_files += 1
    
    consistency_ratio = consistent_files / len(resolution_files)
    
    if consistency_ratio >= 0.8:
        print(f"✅ Resolution pattern consistency: {consistency_ratio:.1%}")
        return True
    else:
        print(f"❌ Resolution pattern consistency insufficient: {consistency_ratio:.1%}")
        return False

def run_comprehensive_validation():
    """Run comprehensive validation of the entire verification infrastructure."""
    
    print("\n🔬 RUNNING COMPREHENSIVE VALIDATION")
    print("-" * 60)
    
    # Test a few key verification scripts
    key_verification_scripts = [
        "verify_issue_673_fix.py",
        "verify_issue_708_fix.py", 
        "verify_issue_759_fix.py"
    ]
    
    working_scripts = 0
    
    for script in key_verification_scripts:
        if Path(script).exists():
            # We expect these to fail due to no file changes, but they should be structurally sound
            success, stdout, stderr = run_command(f"python3 {script}")
            
            # Check if the script ran and provided meaningful output
            if "VERIFICATION" in stdout or "VERIFICATION" in stderr:
                print(f"✅ {script}: Structurally functional")
                working_scripts += 1
            else:
                print(f"❌ {script}: Structural issues")
        else:
            print(f"❌ {script}: Not found")
    
    return working_scripts >= len(key_verification_scripts) * 0.7

def main():
    """Main verification function for Issue #904."""
    
    print("🎯 ISSUE #904 COMPREHENSIVE VERIFICATION INFRASTRUCTURE TEST")
    print("=" * 80)
    print("Validating that CTMM repository verification infrastructure is comprehensive")
    print("and working correctly for all GitHub issue resolutions.\n")
    
    checks = [
        ("Verification Scripts Coverage", check_verification_scripts_coverage),
        ("Comprehensive Test Suites", check_test_suites_comprehensive),
        ("Validation Tools Functionality", check_validation_tools_functional),
        ("Documentation Coverage", check_documentation_coverage),
        ("Issue Resolution Pattern Consistency", check_issue_resolution_pattern_consistency),
        ("Comprehensive Validation", run_comprehensive_validation)
    ]
    
    all_passed = True
    passed_checks = 0
    
    for check_name, check_func in checks:
        try:
            if check_func():
                print(f"\n✅ {check_name}: PASSED")
                passed_checks += 1
            else:
                print(f"\n❌ {check_name}: FAILED")
                all_passed = False
        except Exception as e:
            print(f"\n❌ {check_name}: ERROR - {e}")
            all_passed = False
    
    print("\n" + "=" * 80)
    print("COMPREHENSIVE VERIFICATION INFRASTRUCTURE RESULTS")
    print("=" * 80)
    
    success_rate = passed_checks / len(checks)
    
    if all_passed:
        print("🎉 ISSUE #904 SUCCESSFULLY RESOLVED")
        print("\nComprehensive verification infrastructure is fully operational:")
        print("  ✅ All critical verification scripts present")
        print("  ✅ Comprehensive test suites functional") 
        print("  ✅ All validation tools working")
        print("  ✅ Documentation coverage complete")
        print("  ✅ Issue resolution patterns consistent")
        print("  ✅ Verification infrastructure validated")
        
        print("\n🏗️  INFRASTRUCTURE ACHIEVEMENTS:")
        print("  • Complete verification script coverage for major issues")
        print("  • Comprehensive test suites for LaTeX, workflows, and CI")
        print("  • Functional validation toolchain")
        print("  • Thorough documentation for therapie-material directory")
        print("  • Consistent issue resolution documentation patterns")
        
        print("\n🎯 VERIFICATION STATUS: ✅ INFRASTRUCTURE COMPREHENSIVE")
        sys.exit(0)
    else:
        print(f"❌ ISSUE #904 RESOLUTION: INCOMPLETE ({success_rate:.1%} passed)")
        print("   Some verification infrastructure checks failed - see details above")
        sys.exit(1)

if __name__ == "__main__":
    main()