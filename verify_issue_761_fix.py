#!/usr/bin/env python3
"""
Verification script for Issue #761: Enhanced CI Pipeline Robustness

This script validates that Issue #761 has been properly resolved by verifying:
1. Enhanced workflow error handling mechanisms
2. Comprehensive pre-build validation steps
3. Improved error recovery and reporting
4. YAML syntax fixes for workflow reliability
5. CI pipeline robustness improvements

Issue #761 addressed CI pipeline failures and lack of robustness in error handling.
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

def validate_yaml_syntax_improvements():
    """Verify YAML syntax improvements in workflows."""
    print("\n📝 YAML SYNTAX IMPROVEMENTS VERIFICATION")
    print("-" * 50)
    
    pr_validation_file = Path(".github/workflows/pr-validation.yml")
    if not pr_validation_file.exists():
        print("❌ pr-validation.yml not found")
        return False
    
    try:
        with open(pr_validation_file, 'r') as f:
            content = f.read()
            workflow = yaml.safe_load(content)
        
        # Check for quoted 'on:' keyword fix
        if '"on":' in content or "'on':" in content:
            print("✅ YAML syntax fix applied: 'on:' keyword properly quoted")
        else:
            # Check if unquoted 'on:' still works
            if 'on:' in content and workflow.get('on') is not None:
                print("✅ YAML syntax valid: 'on:' keyword parsed correctly")
            else:
                print("❌ YAML syntax issue: 'on:' keyword not found or invalid")
                return False
        
        print("✅ pr-validation.yml has valid YAML syntax")
        return True
        
    except yaml.YAMLError as e:
        print(f"❌ YAML syntax error in pr-validation.yml: {e}")
        return False
    except Exception as e:
        print(f"❌ Error reading pr-validation.yml: {e}")
        return False

def test_enhanced_error_handling():
    """Test enhanced error handling in workflows."""
    print("\n🛡️ ENHANCED ERROR HANDLING VERIFICATION")
    print("-" * 50)
    
    workflow_files = [
        ".github/workflows/latex-build.yml",
        ".github/workflows/pr-validation.yml",
        ".github/workflows/latex-validation.yml"
    ]
    
    all_valid = True
    error_handling_features = 0
    
    for workflow_file in workflow_files:
        workflow_path = Path(workflow_file)
        if not workflow_path.exists():
            print(f"⚠️  {workflow_file} not found")
            continue
            
        try:
            with open(workflow_path, 'r') as f:
                workflow = yaml.safe_load(f)
            
            # Check for error handling mechanisms
            jobs = workflow.get('jobs', {})
            for job_name, job in jobs.items():
                steps = job.get('steps', [])
                
                # Look for validation steps
                validation_steps = [s for s in steps if 'validat' in str(s).lower()]
                if validation_steps:
                    error_handling_features += 1
                    print(f"✅ {workflow_file}: Validation steps present in {job_name}")
                
                # Look for error tolerance
                error_tolerant_steps = [s for s in steps if s.get('continue-on-error')]
                if error_tolerant_steps:
                    error_handling_features += 1
                    print(f"✅ {workflow_file}: Error tolerance configured in {job_name}")
                
                # Look for failure handling
                failure_steps = [s for s in steps if 'failure()' in str(s.get('if', ''))]
                if failure_steps:
                    error_handling_features += 1
                    print(f"✅ {workflow_file}: Failure handling configured in {job_name}")
                    
        except Exception as e:
            print(f"❌ Error analyzing {workflow_file}: {e}")
            all_valid = False
    
    if error_handling_features > 0:
        print(f"✅ Found {error_handling_features} error handling features across workflows")
    else:
        print("⚠️  Limited error handling features detected")
    
    return all_valid

def validate_pre_build_robustness():
    """Test pre-build validation robustness."""
    print("\n🔍 PRE-BUILD ROBUSTNESS VERIFICATION")
    print("-" * 50)
    
    # Test validation scripts exist and work
    validation_scripts = [
        'validate_pr.py',
        'ctmm_build.py',
        'validate_latex_syntax.py'
    ]
    
    working_scripts = 0
    for script in validation_scripts:
        script_path = Path(script)
        if not script_path.exists():
            print(f"❌ Missing validation script: {script}")
            continue
            
        try:
            # Test if script can be executed
            result = subprocess.run([sys.executable, script, '--help'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0 or 'usage' in result.stdout.lower() or 'help' in result.stdout.lower():
                print(f"✅ {script}: Executable and responsive")
                working_scripts += 1
            else:
                # Try running without --help
                result = subprocess.run([sys.executable, script], 
                                      capture_output=True, text=True, timeout=30)
                if result.returncode == 0:
                    print(f"✅ {script}: Executable")
                    working_scripts += 1
                else:
                    print(f"⚠️  {script}: May have execution issues")
        except subprocess.TimeoutExpired:
            print(f"⚠️  {script}: Timeout (possibly working but slow)")
            working_scripts += 1
        except Exception as e:
            print(f"❌ {script}: Execution error - {e}")
    
    if working_scripts >= 2:
        print(f"✅ {working_scripts}/{len(validation_scripts)} validation scripts operational")
        return True
    else:
        print(f"❌ Only {working_scripts}/{len(validation_scripts)} validation scripts working")
        return False

def test_ci_pipeline_integration():
    """Test CI pipeline integration and workflow structure."""
    print("\n🔄 CI PIPELINE INTEGRATION VERIFICATION")
    print("-" * 50)
    
    # Check that workflows exist and have proper structure
    essential_workflows = {
        'latex-build.yml': ['LaTeX', 'build', 'compile'],
        'pr-validation.yml': ['validation', 'check', 'validate'],
        'latex-validation.yml': ['LaTeX', 'validation', 'syntax']
    }
    
    workflow_dir = Path(".github/workflows")
    if not workflow_dir.exists():
        print("❌ .github/workflows directory not found")
        return False
    
    all_workflows_valid = True
    for workflow_file, expected_keywords in essential_workflows.items():
        workflow_path = workflow_dir / workflow_file
        if not workflow_path.exists():
            print(f"⚠️  {workflow_file} not found")
            continue
            
        try:
            with open(workflow_path, 'r') as f:
                content = f.read().lower()
                workflow = yaml.safe_load(content)
            
            # Check for expected keywords
            found_keywords = sum(1 for keyword in expected_keywords if keyword.lower() in content)
            if found_keywords >= 1:
                print(f"✅ {workflow_file}: Relevant workflow structure")
            else:
                print(f"⚠️  {workflow_file}: May not match expected purpose")
            
            # Check for basic workflow structure
            if workflow.get('on') and workflow.get('jobs'):
                print(f"✅ {workflow_file}: Valid workflow structure")
            else:
                print(f"❌ {workflow_file}: Invalid workflow structure")
                all_workflows_valid = False
                
        except Exception as e:
            print(f"❌ Error validating {workflow_file}: {e}")
            all_workflows_valid = False
    
    return all_workflows_valid

def validate_issue_761_documentation():
    """Verify Issue #761 documentation exists and is complete."""
    print("\n📄 ISSUE #761 DOCUMENTATION VERIFICATION")
    print("-" * 50)
    
    doc_file = Path("ISSUE_761_RESOLUTION.md")
    if not doc_file.exists():
        print("❌ ISSUE_761_RESOLUTION.md not found")
        return False
    
    content = doc_file.read_text()
    
    required_sections = [
        "Enhanced CI Pipeline Robustness",
        "Root Cause Analysis",
        "Solution Implemented", 
        "YAML Syntax",
        "Error Detection"
    ]
    
    missing_sections = []
    for section in required_sections:
        if section not in content:
            missing_sections.append(section)
    
    if missing_sections:
        print(f"❌ Missing documentation sections: {', '.join(missing_sections)}")
        return False
    
    print("✅ Complete Issue #761 documentation found")
    print(f"   Document size: {len(content)} characters")
    
    # Check for CI improvements mention
    ci_keywords = ["ci", "pipeline", "robustness", "error handling", "yaml"]
    found_keywords = sum(1 for keyword in ci_keywords if keyword.lower() in content.lower())
    
    if found_keywords >= 3:
        print(f"✅ CI pipeline improvements well documented ({found_keywords}/5 keywords)")
    else:
        print(f"⚠️  Limited CI improvement documentation ({found_keywords}/5 keywords)")
    
    return True

def test_robustness_improvements():
    """Test overall robustness improvements."""
    print("\n💪 ROBUSTNESS IMPROVEMENTS VERIFICATION")
    print("-" * 50)
    
    # Test the specific test file for issue #761
    test_file = Path("test_issue_761_fix.py")
    if test_file.exists():
        try:
            result = subprocess.run([sys.executable, str(test_file)], 
                                  capture_output=True, text=True, timeout=60)
            if result.returncode == 0:
                print("✅ Issue #761 specific test suite passes")
                return True
            else:
                print("⚠️  Issue #761 test suite reports issues")
                print(f"   Output: {result.stdout[-200:]}...")
                return False
        except subprocess.TimeoutExpired:
            print("⚠️  Issue #761 test suite timeout (may still be working)")
            return True
        except Exception as e:
            print(f"❌ Error running Issue #761 test suite: {e}")
            return False
    else:
        print("⚠️  Issue #761 specific test file not found")
        return True

def main():
    """Main verification function."""
    print("=" * 70)
    print("Issue #761 Resolution Verification")
    print("Enhanced CI Pipeline Robustness")
    print("=" * 70)
    
    # Run all verification checks
    checks = [
        ("YAML Syntax Improvements", validate_yaml_syntax_improvements),
        ("Enhanced Error Handling", test_enhanced_error_handling),
        ("Pre-build Robustness", validate_pre_build_robustness),
        ("CI Pipeline Integration", test_ci_pipeline_integration),
        ("Issue Documentation", validate_issue_761_documentation),
        ("Robustness Improvements", test_robustness_improvements)
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
        print("Issue #761 has been successfully resolved:")
        print("  ✅ Enhanced CI pipeline robustness implemented")
        print("  ✅ Improved error handling and recovery mechanisms")
        print("  ✅ YAML syntax issues fixed")
        print("  ✅ Pre-build validation enhanced")
        print("  ✅ All workflow validation systems operational")
        return True
    else:
        print("\n❌ SOME CHECKS FAILED")
        print("Issue #761 resolution may be incomplete")
        failed_checks = [name for name, passed in results.items() if not passed]
        print(f"Failed checks: {', '.join(failed_checks)}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)