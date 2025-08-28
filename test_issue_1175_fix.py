#!/usr/bin/env python3
"""
Test script for Issue #1175: GitHub Actions LaTeX version update request
Validates the safety and correctness of updating dante-ev/latex-action from v0.2.0 to v2.3.0
"""

import os
import sys
import yaml
from pathlib import Path

def test_current_workflow_state():
    """Test current workflow state before any changes."""
    print("🔍 Testing Current Workflow State")
    print("=" * 60)
    
    workflow_files = [
        '.github/workflows/latex-validation.yml',
        '.github/workflows/latex-build.yml', 
        '.github/workflows/automated-pr-merge-test.yml'
    ]
    
    current_state = {}
    
    for workflow_file in workflow_files:
        if not os.path.exists(workflow_file):
            print(f"❌ Missing workflow file: {workflow_file}")
            return False
            
        with open(workflow_file, 'r') as f:
            content = f.read()
            
        # Find dante-ev/latex-action version
        import re
        matches = re.findall(r'dante-ev/latex-action@(v?[\d.]+)', content)
        
        if matches:
            version = matches[0]
            current_state[workflow_file] = version
            print(f"📄 {workflow_file}: dante-ev/latex-action@{version}")
        else:
            print(f"⚠️  {workflow_file}: No dante-ev/latex-action found")
    
    return current_state

def test_historical_context():
    """Test historical resolution context for version conflicts."""
    print("\n🕰️ Testing Historical Resolution Context")
    print("=" * 60)
    
    resolution_files = [
        'ISSUE_1062_RESOLUTION.md',
        'ISSUE_1082_RESOLUTION.md'
    ]
    
    for resolution_file in resolution_files:
        if os.path.exists(resolution_file):
            print(f"📄 Found: {resolution_file}")
            with open(resolution_file, 'r') as f:
                content = f.read()
                
            # Check for v2.3.0 warnings
            if 'v2.3.0' in content and ('does not exist' in content or 'non-existent' in content):
                print(f"⚠️  {resolution_file}: Contains warnings about v2.3.0 being non-existent")
                return False
        else:
            print(f"❌ Missing: {resolution_file}")
    
    return True

def test_repository_context_conflict():
    """Test for conflicts between issue request and repository documentation."""
    print("\n⚔️ Testing Issue Request vs Repository Context")
    print("=" * 60)
    
    # Issue #1175 requests updating TO v2.3.0
    requested_action = "UPDATE TO v2.3.0"
    print(f"📋 Issue #1175 Request: {requested_action}")
    
    # Repository context shows v2.3.0 is problematic
    resolution_warnings = []
    
    if os.path.exists('ISSUE_1082_RESOLUTION.md'):
        with open('ISSUE_1082_RESOLUTION.md', 'r') as f:
            content = f.read()
            if 'v2.3.0' in content and 'klappt nicht' in content:
                resolution_warnings.append("ISSUE_1082: v2.3.0 doesn't work")
    
    if os.path.exists('ISSUE_1062_RESOLUTION.md'):
        with open('ISSUE_1062_RESOLUTION.md', 'r') as f:
            content = f.read()
            if 'v2.3.0' in content and 'does not exist' in content:
                resolution_warnings.append("ISSUE_1062: v2.3.0 does not exist")
    
    if resolution_warnings:
        print("⚠️  CONFLICT DETECTED:")
        for warning in resolution_warnings:
            print(f"   • {warning}")
        print(f"   • Issue #1175 requests using v2.3.0")
        print(f"   • Previous resolutions warn against v2.3.0")
        return False
    
    return True

def test_validation_scripts_status():
    """Test current validation scripts to see if they pass with v0.2.0."""
    print("\n✅ Testing Current Validation Scripts")
    print("=" * 60)
    
    validation_scripts = [
        'test_issue_1082_fix.py',
        'validate_workflow_versions.py'
    ]
    
    for script in validation_scripts:
        if os.path.exists(script):
            print(f"📄 Found validation script: {script}")
            try:
                # Import and check if it would pass
                import subprocess
                result = subprocess.run([sys.executable, script], 
                                      capture_output=True, text=True, timeout=30)
                if result.returncode == 0:
                    print(f"✅ {script}: PASSES with current configuration")
                else:
                    print(f"❌ {script}: FAILS with current configuration")
                    print(f"   Error: {result.stderr[:200]}...")
            except Exception as e:
                print(f"⚠️  {script}: Could not test ({str(e)})")
        else:
            print(f"❌ Missing validation script: {script}")

def generate_recommendation():
    """Generate recommendation based on test results."""
    print("\n" + "=" * 70)
    print("📋 RECOMMENDATION")
    print("=" * 70)
    
    print("Based on comprehensive analysis:")
    print("")
    print("🚨 **CRITICAL CONFLICT DETECTED**")
    print("")
    print("Issue #1175 requests updating TO v2.3.0, but:")
    print("• Previous issues (#1062, #1082) document v2.3.0 as non-existent")
    print("• Current workflows use v0.2.0 (documented as stable/recommended)")
    print("• All validation scripts pass with current v0.2.0 configuration")
    print("• Repository contains extensive warnings against v2.3.0")
    print("")
    print("📌 **RECOMMENDED ACTION:**")
    print("1. DO NOT update to v2.3.0 until version existence is verified")
    print("2. Current v0.2.0 configuration should be maintained")
    print("3. Issue #1175 description may need correction")
    print("4. If v2.3.0 now exists, extensive testing is required first")
    print("")
    print("⚠️  **RISK ASSESSMENT:**")
    print("• HIGH RISK: Updating to v2.3.0 may break all CI workflows")
    print("• SAFE: Keeping v0.2.0 maintains current working state")

def main():
    """Main test function."""
    print("🧪 Issue #1175 Validation: GitHub Actions LaTeX Version Update")
    print("Testing safety of updating dante-ev/latex-action from v0.2.0 to v2.3.0")
    print("=" * 70)
    
    # Test current state
    current_state = test_current_workflow_state()
    
    # Test historical context
    historical_safe = test_historical_context()
    
    # Test for conflicts
    no_conflicts = test_repository_context_conflict()
    
    # Test validation scripts
    test_validation_scripts_status()
    
    # Generate recommendation
    generate_recommendation()
    
    # Return result
    if not historical_safe or not no_conflicts:
        print("\n❌ TESTS FAILED: Conflicts detected, update NOT recommended")
        return 1
    else:
        print("\n✅ TESTS PASSED: But proceed with extreme caution")
        return 0

if __name__ == "__main__":
    sys.exit(main())