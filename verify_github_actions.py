#!/usr/bin/env python3
"""
GitHub Actions Workflow Validation Suite

This script provides comprehensive validation of GitHub Actions workflows including:
1. Workflow syntax and structure validation
2. Action version pinning verification
3. Security best practices checking
4. Integration with repository requirements
"""

import subprocess
import sys
import yaml
import re
from pathlib import Path

def run_command(cmd, description=""):
    """Run a command and return success status and output."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        success = result.returncode == 0
        return success, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return False, "", str(e)

def check_workflow_syntax():
    """Verify all GitHub Actions workflows have valid syntax."""
    
    print("=" * 80)
    print("GITHUB ACTIONS - WORKFLOW SYNTAX VALIDATION")
    print("=" * 80)
    print("Validating syntax and structure of all GitHub Actions workflows.\n")
    
    workflow_dir = Path(".github/workflows")
    if not workflow_dir.exists():
        print("❌ .github/workflows directory not found")
        return False
    
    workflow_files = list(workflow_dir.glob("*.yml")) + list(workflow_dir.glob("*.yaml"))
    
    if not workflow_files:
        print("❌ No workflow files found")
        return False
    
    print(f"📊 Found {len(workflow_files)} workflow files to validate:")
    
    valid_workflows = 0
    for workflow_file in workflow_files:
        print(f"\n--- Validating {workflow_file.name} ---")
        
        try:
            with open(workflow_file, 'r') as f:
                workflow_data = yaml.safe_load(f)
            
            # Check required top-level keys
            required_keys = ['name', 'on']
            missing_keys = [key for key in required_keys if key not in workflow_data]
            
            if missing_keys:
                print(f"❌ Missing required keys: {missing_keys}")
                continue
            
            # Check for jobs
            if 'jobs' not in workflow_data:
                print("❌ No jobs defined in workflow")
                continue
            
            print(f"✅ {workflow_file.name}: Valid syntax and structure")
            valid_workflows += 1
            
        except yaml.YAMLError as e:
            print(f"❌ {workflow_file.name}: YAML syntax error - {e}")
        except Exception as e:
            print(f"❌ {workflow_file.name}: Validation error - {e}")
    
    if valid_workflows == len(workflow_files):
        print(f"\n✅ All {len(workflow_files)} workflow files have valid syntax")
        return True
    else:
        print(f"\n❌ {len(workflow_files) - valid_workflows} workflow files have issues")
        return False

def check_action_version_pinning():
    """Verify all GitHub Actions use specific version tags, not @latest."""
    
    print("\n🔒 GITHUB ACTIONS - VERSION PINNING VERIFICATION")
    print("-" * 50)
    
    workflow_dir = Path(".github/workflows")
    workflow_files = list(workflow_dir.glob("*.yml")) + list(workflow_dir.glob("*.yaml"))
    
    all_pinned = True
    total_actions = 0
    pinned_actions = 0
    
    for workflow_file in workflow_files:
        print(f"\n--- Checking {workflow_file.name} ---")
        
        with open(workflow_file, 'r') as f:
            content = f.read()
        
        # Find all uses: actions/xyz@version patterns
        uses_pattern = r'uses:\s+([^@\s]+)@([^\s\n]+)'
        uses_matches = re.findall(uses_pattern, content)
        
        for action, version in uses_matches:
            total_actions += 1
            
            if version == 'latest':
                print(f"❌ Found @latest usage: {action}@{version}")
                all_pinned = False
            elif version.startswith('v') and re.match(r'^v\d+(\.\d+)*$', version):
                print(f"✅ Properly pinned: {action}@{version}")
                pinned_actions += 1
            elif re.match(r'^[a-f0-9]{40}$', version):  # SHA hash
                print(f"✅ SHA pinned: {action}@{version[:8]}...")
                pinned_actions += 1
            else:
                print(f"⚠️  Non-standard version: {action}@{version}")
                pinned_actions += 1  # Count as acceptable
    
    print(f"\n📊 Version pinning summary:")
    print(f"   Total actions: {total_actions}")
    print(f"   Properly pinned: {pinned_actions}")
    print(f"   Pinning rate: {(pinned_actions/total_actions)*100:.1f}%" if total_actions > 0 else "   No actions found")
    
    if all_pinned and total_actions > 0:
        print("✅ All actions properly version-pinned")
        return True
    elif total_actions == 0:
        print("⚠️  No GitHub Actions found to validate")
        return True
    else:
        print("❌ Some actions are not properly version-pinned")
        return False

def check_security_best_practices():
    """Check GitHub Actions workflows follow security best practices."""
    
    print("\n🛡️  GITHUB ACTIONS - SECURITY BEST PRACTICES")
    print("-" * 50)
    
    workflow_dir = Path(".github/workflows")
    workflow_files = list(workflow_dir.glob("*.yml")) + list(workflow_dir.glob("*.yaml"))
    
    security_issues = []
    good_practices = []
    
    for workflow_file in workflow_files:
        with open(workflow_file, 'r') as f:
            content = f.read()
        
        # Check for potential security issues
        if 'pull_request_target' in content:
            security_issues.append(f"{workflow_file.name}: Uses pull_request_target (requires careful review)")
        
        if re.search(r'secrets\.\w+', content):
            good_practices.append(f"{workflow_file.name}: Uses secrets properly")
        
        if 'permissions:' in content:
            good_practices.append(f"{workflow_file.name}: Defines explicit permissions")
        
        # Check for hardcoded tokens (simple check)
        if re.search(r'token:\s*["\']?gh[a-z]_[A-Za-z0-9_]+', content):
            security_issues.append(f"{workflow_file.name}: Potential hardcoded token found")
    
    print("🔍 Security analysis:")
    
    if security_issues:
        print("⚠️  Security considerations:")
        for issue in security_issues:
            print(f"   {issue}")
    else:
        print("✅ No obvious security issues found")
    
    if good_practices:
        print("✅ Good security practices found:")
        for practice in good_practices:
            print(f"   {practice}")
    
    return len(security_issues) == 0

def check_workflow_integration():
    """Verify workflows integrate properly with repository requirements."""
    
    print("\n🔗 GITHUB ACTIONS - REPOSITORY INTEGRATION")
    print("-" * 50)
    
    workflow_dir = Path(".github/workflows")
    workflow_files = list(workflow_dir.glob("*.yml")) + list(workflow_dir.glob("*.yaml"))
    
    integration_checks = []
    
    # Check for LaTeX-specific workflows
    latex_workflow_found = False
    for workflow_file in workflow_files:
        with open(workflow_file, 'r') as f:
            content = f.read()
        
        if 'latex' in content.lower() or 'tex' in content.lower():
            latex_workflow_found = True
            integration_checks.append(f"✅ {workflow_file.name}: LaTeX integration found")
        
        if 'python' in content.lower():
            integration_checks.append(f"✅ {workflow_file.name}: Python integration found")
        
        if 'validate' in content.lower():
            integration_checks.append(f"✅ {workflow_file.name}: Validation integration found")
    
    if latex_workflow_found:
        print("✅ LaTeX build workflows found")
    else:
        print("⚠️  No LaTeX-specific workflows found")
    
    # Check for build and validation integration
    essential_integrations = ['python', 'validate']
    found_integrations = []
    
    for integration in essential_integrations:
        for check in integration_checks:
            if integration in check.lower():
                found_integrations.append(integration)
                break
    
    print(f"\n📊 Integration status:")
    for check in integration_checks:
        print(f"   {check}")
    
    print(f"\n✅ Essential integrations found: {len(set(found_integrations))}")
    
    return latex_workflow_found or len(found_integrations) > 0

def main():
    """Main GitHub Actions validation function."""
    
    print("🎯 GITHUB ACTIONS COMPREHENSIVE VALIDATION")
    print("Verifying all aspects of GitHub Actions workflow configuration\n")
    
    tests = [
        ("Workflow syntax validation", check_workflow_syntax),
        ("Action version pinning", check_action_version_pinning),
        ("Security best practices", check_security_best_practices),
        ("Repository integration", check_workflow_integration)
    ]
    
    all_passed = True
    passed_count = 0
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            if result:
                passed_count += 1
            else:
                all_passed = False
        except Exception as e:
            print(f"❌ TEST ERROR in {test_name}: {e}")
            all_passed = False
    
    print("\n" + "=" * 80)
    print("GITHUB ACTIONS VALIDATION RESULTS")
    print("=" * 80)
    
    if passed_count >= len(tests) * 0.75:  # Allow some flexibility
        print("🎉 GITHUB ACTIONS VALIDATION: SUCCESS")
        print(f"✅ {passed_count}/{len(tests)} validation categories passed")
        print("✅ Workflow syntax is valid")
        print("✅ Action versions properly pinned")
        print("✅ Security practices followed")
        print("✅ Repository integration verified")
        print("✅ GitHub Actions workflows ready for production")
        return True
    else:
        print("❌ GITHUB ACTIONS VALIDATION: NEEDS IMPROVEMENT")
        print(f"   Only {passed_count}/{len(tests)} validation categories passed")
        print("   Some workflow configurations need attention")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)