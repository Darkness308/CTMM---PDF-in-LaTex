#!/usr/bin/env python3
"""
Verification script for Issue #735: GitHub Actions LaTeX Build Failure Resolution

This script validates that Issue #735 has been properly resolved by verifying:
1. GitHub Actions workflow uses correct dante-ev/latex-action version
2. No invalid version references in workflow files
3. Workflow YAML syntax is valid
4. LaTeX build workflow structure is correct
5. Version pinning follows best practices

Issue #735 was caused by referencing non-existent dante-ev/latex-action@v2.0.0 version.
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

def validate_latex_action_version():
    """Verify GitHub Actions uses correct dante-ev/latex-action version."""
    print("\n🎯 LATEX ACTION VERSION VERIFICATION")
    print("-" * 50)
    
    workflow_file = Path(".github/workflows/latex-build.yml")
    if not workflow_file.exists():
        print("❌ latex-build.yml workflow file not found")
        return False
    
    content = workflow_file.read_text()
    
    # Check for correct version usage
    if "dante-ev/latex-action@v2" in content and "dante-ev/latex-action@v2.0.0" not in content:
        print("✅ CORRECT VERSION: dante-ev/latex-action@v2 detected")
        print("   Using valid major version tag")
        
        # Show the specific line
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            if "dante-ev/latex-action@v2" in line:
                print(f"   Line {i}: {line.strip()}")
        
        return True
    elif "dante-ev/latex-action@v2.0.0" in content:
        print("❌ INVALID VERSION: dante-ev/latex-action@v2.0.0 still present")
        print("   Issue #735 not resolved - this version does not exist")
        return False
    elif "dante-ev/latex-action@v0.2" in content:
        print("✅ VALID ALTERNATIVE: dante-ev/latex-action@v0.2 detected")
        print("   Using valid specific version")
        return True
    elif "dante-ev/latex-action@latest" in content:
        print("⚠️  UNPINNED VERSION: dante-ev/latex-action@latest detected")
        print("   Functional but not recommended for reproducibility")
        return True
    else:
        print("❓ UNKNOWN STATE: dante-ev/latex-action not found or invalid format")
        return False

def validate_workflow_yaml_syntax():
    """Verify all workflow YAML files have valid syntax."""
    print("\n📝 WORKFLOW YAML SYNTAX VERIFICATION")
    print("-" * 50)
    
    workflow_dir = Path(".github/workflows")
    if not workflow_dir.exists():
        print("❌ .github/workflows directory not found")
        return False
    
    workflow_files = list(workflow_dir.glob("*.yml")) + list(workflow_dir.glob("*.yaml"))
    
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
            print(f"❌ {workflow_file.name}: YAML syntax error - {e}")
            all_valid = False
        except Exception as e:
            print(f"❌ {workflow_file.name}: Error reading file - {e}")
            all_valid = False
    
    return all_valid

def check_latex_build_workflow_structure():
    """Verify LaTeX build workflow has correct structure."""
    print("\n🏗️  LATEX BUILD WORKFLOW STRUCTURE VERIFICATION")
    print("-" * 50)
    
    workflow_file = Path(".github/workflows/latex-build.yml")
    if not workflow_file.exists():
        print("❌ latex-build.yml not found")
        return False
    
    try:
        with open(workflow_file, 'r') as f:
            workflow = yaml.safe_load(f)
        
        # Check basic workflow structure
        if not workflow.get('on'):
            print("❌ Missing 'on' trigger configuration")
            return False
        
        jobs = workflow.get('jobs', {})
        if not jobs:
            print("❌ No jobs defined in workflow")
            return False
        
        # Check for build job
        build_job = None
        for job_name, job_config in jobs.items():
            if 'latex' in job_name.lower() or 'build' in job_name.lower():
                build_job = job_config
                print(f"✅ Found LaTeX build job: {job_name}")
                break
        
        if not build_job:
            print("⚠️  No clearly identified LaTeX build job")
            build_job = list(jobs.values())[0]  # Use first job
        
        # Check for dante-ev/latex-action usage
        steps = build_job.get('steps', [])
        latex_action_found = False
        
        for step in steps:
            if isinstance(step, dict) and 'uses' in step:
                if 'dante-ev/latex-action' in step['uses']:
                    latex_action_found = True
                    print(f"✅ LaTeX action found: {step['uses']}")
                    break
        
        if not latex_action_found:
            print("❌ dante-ev/latex-action not found in workflow steps")
            return False
        
        print("✅ LaTeX build workflow structure is valid")
        return True
        
    except Exception as e:
        print(f"❌ Error analyzing latex-build.yml: {e}")
        return False

def test_version_pinning_practices():
    """Test that version pinning follows best practices."""
    print("\n📌 VERSION PINNING BEST PRACTICES VERIFICATION")
    print("-" * 50)
    
    workflow_files = list(Path(".github/workflows").glob("*.yml"))
    
    good_practices = 0
    total_actions = 0
    
    for workflow_file in workflow_files:
        try:
            with open(workflow_file, 'r') as f:
                workflow = yaml.safe_load(f)
            
            jobs = workflow.get('jobs', {})
            for job_name, job in jobs.items():
                steps = job.get('steps', [])
                for step in steps:
                    if isinstance(step, dict) and 'uses' in step:
                        action = step['uses']
                        total_actions += 1
                        
                        # Check for good version pinning practices
                        if '@v' in action and not action.endswith('@latest'):
                            good_practices += 1
                            if 'dante-ev/latex-action' in action:
                                print(f"✅ {workflow_file.name}: Good version pinning for {action}")
                        elif '@latest' in action:
                            print(f"⚠️  {workflow_file.name}: Using @latest for {action}")
                        else:
                            print(f"ℹ️  {workflow_file.name}: Action {action}")
                            
        except Exception as e:
            print(f"❌ Error analyzing {workflow_file}: {e}")
    
    if total_actions > 0:
        pinning_rate = good_practices / total_actions
        print(f"\n📊 Version Pinning Rate: {good_practices}/{total_actions} ({pinning_rate:.1%})")
        return pinning_rate >= 0.5  # 50% threshold
    else:
        print("⚠️  No GitHub Actions found to analyze")
        return True

def validate_ci_build_capability():
    """Validate that CI build configuration is functional."""
    print("\n🔧 CI BUILD CAPABILITY VERIFICATION")
    print("-" * 50)
    
    # Check if local build system works
    success, output = run_command("python3 ctmm_build.py", "Local build system test")
    if not success:
        print("❌ Local build system failed")
        return False
    
    # Verify workflow includes proper LaTeX compilation steps
    workflow_file = Path(".github/workflows/latex-build.yml")
    if workflow_file.exists():
        content = workflow_file.read_text()
        
        # Check for LaTeX-related keywords in workflow
        latex_keywords = ['latex', 'pdf', 'compile', 'build']
        found_keywords = sum(1 for keyword in latex_keywords if keyword.lower() in content.lower())
        
        if found_keywords >= 2:
            print(f"✅ LaTeX build workflow contains relevant keywords ({found_keywords}/4)")
        else:
            print(f"⚠️  Limited LaTeX build keywords in workflow ({found_keywords}/4)")
        
        # Check for outputs or artifacts
        if 'artifact' in content.lower() or 'upload' in content.lower():
            print("✅ Workflow includes artifact handling")
        else:
            print("ℹ️  No artifact handling detected")
    
    print("✅ CI build capability verified")
    return True

def validate_issue_735_documentation():
    """Verify Issue #735 documentation exists and is complete."""
    print("\n📄 ISSUE #735 DOCUMENTATION VERIFICATION")
    print("-" * 50)
    
    doc_file = Path("ISSUE_735_RESOLUTION.md")
    if not doc_file.exists():
        print("❌ ISSUE_735_RESOLUTION.md not found")
        return False
    
    content = doc_file.read_text()
    
    required_elements = [
        "dante-ev/latex-action",
        "v2.0.0",
        "v2",
        "GitHub Actions",
        "LaTeX"
    ]
    
    missing_elements = []
    for element in required_elements:
        if element not in content:
            missing_elements.append(element)
    
    if missing_elements:
        print(f"❌ Missing documentation elements: {', '.join(missing_elements)}")
        return False
    
    print("✅ Complete Issue #735 documentation found")
    print(f"   Document size: {len(content)} characters")
    
    # Check for version fix documentation
    if "v2.0.0" in content and "v2" in content:
        print("✅ Version fix documented (v2.0.0 → v2)")
    
    return True

def main():
    """Main verification function."""
    print("=" * 70)
    print("Issue #735 Resolution Verification")
    print("GitHub Actions LaTeX Build Failure Fix")
    print("=" * 70)
    
    # Run all verification checks
    checks = [
        ("LaTeX Action Version", validate_latex_action_version),
        ("Workflow YAML Syntax", validate_workflow_yaml_syntax),
        ("LaTeX Build Workflow Structure", check_latex_build_workflow_structure),
        ("Version Pinning Practices", test_version_pinning_practices),
        ("CI Build Capability", validate_ci_build_capability),
        ("Issue Documentation", validate_issue_735_documentation)
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
        print("Issue #735 has been successfully resolved:")
        print("  ✅ GitHub Actions uses correct dante-ev/latex-action version")
        print("  ✅ Invalid v2.0.0 version reference removed")
        print("  ✅ Workflow YAML syntax is valid")
        print("  ✅ LaTeX build workflow properly structured")
        print("  ✅ CI build capability verified")
        return True
    else:
        print("\n❌ SOME CHECKS FAILED")
        print("Issue #735 resolution may be incomplete")
        failed_checks = [name for name, passed in results.items() if not passed]
        print(f"Failed checks: {', '.join(failed_checks)}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)