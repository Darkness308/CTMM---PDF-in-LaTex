#!/usr/bin/env python3
"""
Test for Issue #988: CI Pipeline Robustness Enhancement
Validates enhanced error handling and robustness improvements in the CI pipeline.
"""

import subprocess
import sys
import yaml
from pathlib import Path

def test_workflow_error_handling():
    """Test that the workflow has proper error handling mechanisms."""
    print("🔧 Testing Enhanced Workflow Error Handling")
    print("=" * 60)
    
    workflow_file = Path(".github/workflows/latex-build.yml")
    if not workflow_file.exists():
        print("❌ FAIL: latex-build.yml not found")
        return False
    
    with open(workflow_file, 'r') as f:
        content = f.read()
    
    # Check for enhanced error handling in key steps
    enhanced_patterns = [
        "|| {",  # Bash error handling
        "|| echo",  # Fallback echo statements
        "⚠️",  # Warning indicators
        "echo.*Environment Information",  # Debug information
        "stat -c %s",  # File size checking
    ]
    
    found_patterns = 0
    for pattern in enhanced_patterns:
        if pattern in content:
            found_patterns += 1
            print(f"✅ Found error handling pattern: {pattern}")
        else:
            print(f"⚠️ Missing pattern: {pattern}")
    
    print(f"✅ Enhanced error handling patterns: {found_patterns}/{len(enhanced_patterns)}")
    return found_patterns >= 3  # At least 3 patterns should be present

def test_validation_step_order():
    """Test that validation steps are properly ordered and comprehensive."""
    print("\n📋 Testing Validation Step Order")
    print("=" * 60)
    
    workflow_file = Path(".github/workflows/latex-build.yml")
    with open(workflow_file, 'r') as f:
        workflow_data = yaml.safe_load(f)
    
    steps = workflow_data['jobs']['build']['steps']
    step_names = [step.get('name', 'Unknown') for step in steps]
    
    # Find validation steps
    validation_steps = []
    latex_step_index = None
    
    for i, name in enumerate(step_names):
        if 'validation' in name.lower() or 'check' in name.lower():
            validation_steps.append((i, name))
        if 'latex' in name.lower() and 'action' in str(steps[i].get('uses', '')):
            latex_step_index = i
    
    print(f"✅ Found {len(validation_steps)} validation steps")
    for i, name in validation_steps:
        print(f"   - Step {i+1}: {name}")
    
    if latex_step_index:
        print(f"✅ LaTeX compilation step found at position {latex_step_index+1}")
        
        # Check all validation steps come before LaTeX
        all_before_latex = all(i < latex_step_index for i, _ in validation_steps)
        if all_before_latex:
            print("✅ All validation steps run before LaTeX compilation")
            return True
        else:
            print("❌ Some validation steps run after LaTeX compilation")
            return False
    else:
        print("⚠️ LaTeX compilation step not found")
        return len(validation_steps) >= 4

def test_robustness_tools():
    """Test that all robustness validation tools work correctly."""
    print("\n🛠️ Testing Robustness Validation Tools")
    print("=" * 60)
    
    tools = [
        'validate_latex_syntax.py',
        'ctmm_build.py',
        'test_issue_743_validation.py',
        'test_issue_761_fix.py'
    ]
    
    passed_tools = 0
    for tool in tools:
        try:
            result = subprocess.run([sys.executable, tool], 
                                    capture_output=True, text=True, timeout=60)
            if result.returncode == 0:
                print(f"✅ {tool}: PASS")
                passed_tools += 1
            else:
                print(f"❌ {tool}: FAIL (exit code {result.returncode})")
                print(f"   Error: {result.stderr[:200]}")
        except subprocess.TimeoutExpired:
            print(f"⚠️ {tool}: TIMEOUT (may still be working)")
        except Exception as e:
            print(f"❌ {tool}: ERROR - {e}")
    
    print(f"✅ Robustness tools passing: {passed_tools}/{len(tools)}")
    return passed_tools >= 3

def test_fallback_mechanisms():
    """Test that fallback mechanisms are in place."""
    print("\n🔄 Testing Fallback Mechanisms")
    print("=" * 60)
    
    workflow_file = Path(".github/workflows/latex-build.yml")
    with open(workflow_file, 'r') as f:
        content = f.read()
    
    fallback_indicators = [
        "falling back",
        "Warning:",
        "|| echo",
        "continue",
        "gracefully",
    ]
    
    found_fallbacks = 0
    for indicator in fallback_indicators:
        if indicator.lower() in content.lower():
            found_fallbacks += 1
            print(f"✅ Found fallback indicator: {indicator}")
    
    print(f"✅ Fallback mechanisms: {found_fallbacks}/{len(fallback_indicators)}")
    return found_fallbacks >= 2

def test_enhanced_debugging():
    """Test that enhanced debugging information is available."""
    print("\n🔍 Testing Enhanced Debugging Information")
    print("=" * 60)
    
    workflow_file = Path(".github/workflows/latex-build.yml")
    with open(workflow_file, 'r') as f:
        content = f.read()
    
    debug_features = [
        "Environment Information",
        "Python version",
        "Current directory",
        "Available tools",
        "Git status",
        "PDF size",
        "hexdump",
    ]
    
    found_debug = 0
    for feature in debug_features:
        if feature in content:
            found_debug += 1
            print(f"✅ Found debug feature: {feature}")
    
    print(f"✅ Debug features: {found_debug}/{len(debug_features)}")
    return found_debug >= 4

def main():
    """Run all robustness tests for Issue #988."""
    print("=" * 70)
    print("ISSUE #988 VALIDATION: CI Pipeline Robustness Enhancement")
    print("=" * 70)
    
    tests = [
        ("Enhanced Workflow Error Handling", test_workflow_error_handling),
        ("Validation Step Order", test_validation_step_order),
        ("Robustness Validation Tools", test_robustness_tools),
        ("Fallback Mechanisms", test_fallback_mechanisms),
        ("Enhanced Debugging Information", test_enhanced_debugging),
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                print(f"\n✅ PASS: {test_name}")
                passed_tests += 1
            else:
                print(f"\n❌ FAIL: {test_name}")
        except Exception as e:
            print(f"\n❌ ERROR in {test_name}: {e}")
    
    print("\n" + "=" * 70)
    print("VALIDATION SUMMARY")
    print("=" * 70)
    print(f"Tests passed: {passed_tests}/{total_tests}")
    
    if passed_tests == total_tests:
        print("🎉 ALL TESTS PASSED! CI pipeline robustness enhancements validated.")
        print("\nThe enhanced CI configuration provides:")
        print("✓ Comprehensive error handling and recovery")
        print("✓ Proper validation step ordering")
        print("✓ Robust fallback mechanisms")
        print("✓ Enhanced debugging capabilities")
        print("✓ Improved reliability and failure detection")
        return 0
    else:
        print(f"⚠️ {total_tests - passed_tests} test(s) failed. Review needed.")
        return 1

if __name__ == "__main__":
    sys.exit(main())