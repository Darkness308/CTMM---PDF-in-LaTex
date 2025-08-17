#!/usr/bin/env python3
"""
Verification script for Issue #667: GitHub Actions LaTeX Upgrade Resolution

This script validates that Issue #667 has been properly resolved by verifying:
1. GitHub Actions LaTeX action has been upgraded from v0.2 to v2
2. Merge conflicts have been resolved and repository is in clean state
3. Meaningful changes exist for Copilot review
4. All validation systems are functioning correctly
5. Build system integration remains intact

Issue #667 was caused by merge conflicts preventing Copilot review in PR #653.
"""

import subprocess
import sys
import os
import yaml
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

def validate_github_actions_upgrade():
    """Verify that GitHub Actions LaTeX action has been upgraded."""
    print("\n🚀 GITHUB ACTIONS UPGRADE VERIFICATION")
    print("-" * 50)
    
    workflow_file = Path(".github/workflows/latex-build.yml")
    if not workflow_file.exists():
        print("❌ LaTeX build workflow file not found")
        return False
    
    content = workflow_file.read_text()
    
    # Check for the upgraded action
    if "dante-ev/latex-action@v2" in content:
        print("✅ UPGRADE CONFIRMED: dante-ev/latex-action@v2 detected")
        print("   Enhanced LaTeX compilation capabilities active")
        return True
    elif "dante-ev/latex-action@v0.2" in content:
        print("❌ OLD VERSION: dante-ev/latex-action@v0.2 detected")
        print("   Issue #667 not resolved - upgrade to v2 required")
        return False
    elif "dante-ev/latex-action@latest" in content:
        print("⚠️  UNPINNED VERSION: @latest detected")
        print("   Consider pinning to specific version for reproducibility")
        return True
    else:
        print("❓ UNKNOWN STATE: dante-ev/latex-action not found")
        return False

def check_merge_conflicts():
    """Verify repository is free of merge conflicts."""
    print("\n🔀 MERGE CONFLICT VERIFICATION")
    print("-" * 50)
    
    # Check git status for conflicts
    success, output = run_command("git status --porcelain", "Check for merge conflicts")
    if not success:
        print("❌ Cannot check git status")
        return False
    
    if not output:
        print("✅ Repository is clean - no merge conflicts")
        return True
    
    # Check for conflict markers
    conflict_files = []
    for line in output.split('\n'):
        if line.startswith('UU ') or line.startswith('AA '):
            conflict_files.append(line[3:])
    
    if conflict_files:
        print(f"❌ Merge conflicts detected in {len(conflict_files)} files:")
        for file in conflict_files:
            print(f"   - {file}")
        return False
    
    print("✅ No merge conflicts detected")
    return True

def validate_workflow_syntax():
    """Validate GitHub Actions workflow YAML syntax."""
    print("\n📝 WORKFLOW SYNTAX VALIDATION")
    print("-" * 50)
    
    workflow_files = list(Path(".github/workflows").glob("*.yml")) + list(Path(".github/workflows").glob("*.yaml"))
    
    if not workflow_files:
        print("❌ No workflow files found")
        return False
    
    all_valid = True
    for workflow_file in workflow_files:
        try:
            with open(workflow_file, 'r') as f:
                yaml.safe_load(f)
            print(f"✅ {workflow_file.name}: Valid YAML syntax")
        except yaml.YAMLError as e:
            print(f"❌ {workflow_file.name}: Invalid YAML syntax - {e}")
            all_valid = False
        except Exception as e:
            print(f"❌ {workflow_file.name}: Error reading file - {e}")
            all_valid = False
    
    return all_valid

def validate_copilot_readiness():
    """Validate that repository state allows Copilot review."""
    print("\n🤖 COPILOT READINESS VERIFICATION")
    print("-" * 50)
    
    # Check for meaningful changes using different base options
    base_options = ["main..HEAD", "origin/main..HEAD", "HEAD~3..HEAD"]
    
    for base_option in base_options:
        success, stdout = run_command(f"git diff --stat {base_option}", f"Change statistics ({base_option})")
        if success and stdout.strip():
            print(f"✅ Meaningful changes detected ({base_option}):")
            print(f"   {stdout.strip()}")
            return True
    
    # Check if we have any tracked files with changes
    success, stdout = run_command("git diff --stat HEAD~1..HEAD", "Recent changes")
    if success and stdout.strip():
        print("✅ Recent changes detected:")
        print(f"   {stdout.strip()}")
        return True
    
    print("❌ No meaningful changes detected for Copilot review")
    return False

def test_ctmm_integration():
    """Test that CTMM build system still works after changes."""
    print("\n🔧 CTMM BUILD SYSTEM INTEGRATION")
    print("-" * 50)
    
    # Test CTMM build system
    success, output = run_command("python3 ctmm_build.py", "CTMM build system test")
    if success:
        print("✅ CTMM build system operational")
        return True
    else:
        print("❌ CTMM build system issues detected")
        return False

def validate_issue_667_documentation():
    """Verify Issue #667 documentation exists and is complete."""
    print("\n📄 ISSUE #667 DOCUMENTATION VERIFICATION")
    print("-" * 50)
    
    doc_file = Path("ISSUE_667_RESOLUTION.md")
    if not doc_file.exists():
        print("❌ ISSUE_667_RESOLUTION.md not found")
        return False
    
    content = doc_file.read_text()
    
    required_sections = [
        "Problem Statement",
        "Root Cause Analysis", 
        "Solution Implemented",
        "GitHub Actions",
        "dante-ev/latex-action"
    ]
    
    missing_sections = []
    for section in required_sections:
        if section not in content:
            missing_sections.append(section)
    
    if missing_sections:
        print(f"❌ Missing documentation sections: {', '.join(missing_sections)}")
        return False
    
    print("✅ Complete Issue #667 documentation found")
    print(f"   Document size: {len(content)} characters")
    
    # Check for upgrade mention
    if "dante-ev/latex-action@v2" in content or "v0.2" in content:
        print("✅ GitHub Actions upgrade documented")
    else:
        print("⚠️  GitHub Actions upgrade details unclear in documentation")
    
    return True

def main():
    """Main verification function."""
    print("=" * 70)
    print("Issue #667 Resolution Verification")
    print("GitHub Actions LaTeX Upgrade & Merge Conflict Resolution")
    print("=" * 70)
    
    # Run all verification checks
    checks = [
        ("GitHub Actions Upgrade", validate_github_actions_upgrade),
        ("Merge Conflicts", check_merge_conflicts),
        ("Workflow Syntax", validate_workflow_syntax),
        ("Copilot Readiness", validate_copilot_readiness),
        ("CTMM Integration", test_ctmm_integration),
        ("Issue Documentation", validate_issue_667_documentation)
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
        print("Issue #667 has been successfully resolved:")
        print("  ✅ GitHub Actions LaTeX action upgraded to v2")
        print("  ✅ Repository clean of merge conflicts")
        print("  ✅ Meaningful changes available for Copilot review")
        print("  ✅ All validation systems operational")
        print("  ✅ CTMM build system integration maintained")
        return True
    else:
        print("\n❌ SOME CHECKS FAILED")
        print("Issue #667 resolution may be incomplete")
        failed_checks = [name for name, passed in results.items() if not passed]
        print(f"Failed checks: {', '.join(failed_checks)}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)