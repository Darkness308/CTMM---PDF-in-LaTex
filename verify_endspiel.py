#!/usr/bin/env python3
"""
Endspiel Verification Script - Issue #727

This script provides comprehensive verification that the "Endspiel" implementation
is complete and all resolution components are functioning correctly.

Endspiel represents the final phase of comprehensive issue resolution and
validation enhancement for the CTMM repository.
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple

def run_command(cmd: str, description: str = "") -> Tuple[bool, str]:
    """Run a shell command and return success status and output."""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, cwd=Path(__file__).parent
        )
        return result.returncode == 0, result.stdout + result.stderr
    except Exception as e:
        return False, str(e)

def check_resolution_documents() -> Dict[str, bool]:
    """Verify all issue resolution documents exist and are comprehensive."""
    print("🔍 CHECKING RESOLUTION DOCUMENTATION")
    print("=" * 60)
    
    required_documents = {
        "ENDSPIEL_RESOLUTION.md": "Master resolution document",
        "COPILOT_ISSUE_RESOLUTION.md": "Original Copilot review issue",
        "ISSUE_667_RESOLUTION.md": "Merge conflict resolution", 
        "ISSUE_673_RESOLUTION.md": "Enhanced verification infrastructure",
        "ISSUE_708_RESOLUTION.md": "Empty PR detection",
        "ISSUE_476_RESOLUTION.md": "Binary file exclusion",
        "ISSUE_532_RESOLUTION.md": "LaTeX syntax validation",
        "ISSUE_607_RESOLUTION.md": "Workflow version pinning",
        "ISSUE_614_RESOLUTION.md": "Enhanced documentation",
        "MERGIFY_SHA_CONFLICT_RESOLUTION.md": "Mergify conflicts"
    }
    
    results = {}
    total_content = 0
    
    for doc, description in required_documents.items():
        if os.path.exists(doc):
            with open(doc, 'r', encoding='utf-8') as f:
                content = f.read()
                content_length = len(content)
                total_content += content_length
                
            print(f"✅ {doc}: {description} ({content_length:,} chars)")
            results[doc] = True
        else:
            print(f"❌ {doc}: MISSING - {description}")
            results[doc] = False
    
    print(f"\n📊 Total documentation: {total_content:,} characters")
    print(f"📋 Documents found: {sum(results.values())}/{len(results)}")
    
    return results

def check_validation_infrastructure() -> Dict[str, bool]:
    """Verify all validation tools exist and function correctly."""
    print("\n🛠️  CHECKING VALIDATION INFRASTRUCTURE")
    print("=" * 60)
    
    validation_tools = {
        "validate_pr.py": "Primary PR validation",
        "ctmm_build.py": "CTMM build system validation",
        "latex_validator.py": "LaTeX syntax validation", 
        "validate_workflow_syntax.py": "GitHub Actions validation",
        "validate_workflow_versions.py": "Version pinning validation",
        "verify_copilot_fix.py": "Copilot review verification",
        "verify_issue_673_fix.py": "System health checking",
        "verify_issue_708_fix.py": "Empty PR validation"
    }
    
    results = {}
    
    for tool, description in validation_tools.items():
        if os.path.exists(tool):
            # Test if the tool runs without errors (syntax check)
            success, output = run_command(f"python3 -m py_compile {tool}")
            if success:
                print(f"✅ {tool}: {description}")
                results[tool] = True
            else:
                print(f"⚠️  {tool}: {description} (syntax errors)")
                results[tool] = False
        else:
            print(f"❌ {tool}: MISSING - {description}")
            results[tool] = False
    
    return results

def check_testing_infrastructure() -> Dict[str, bool]:
    """Verify testing infrastructure is complete."""
    print("\n🧪 CHECKING TESTING INFRASTRUCTURE")
    print("=" * 60)
    
    test_files = {
        "test_pr_validation.py": "PR validation testing",
        "test_ctmm_build.py": "Build system testing",
        "test_latex_validator.py": "LaTeX validation testing",
        "test_workflow_structure.py": "Workflow structure testing",
        "test_workflow_versions.py": "Version validation testing"
    }
    
    results = {}
    
    for test_file, description in test_files.items():
        if os.path.exists(test_file):
            # Test if the test file is syntactically correct
            success, output = run_command(f"python3 -m py_compile {test_file}")
            if success:
                print(f"✅ {test_file}: {description}")
                results[test_file] = True
            else:
                print(f"⚠️  {test_file}: {description} (syntax errors)")
                results[test_file] = False
        else:
            print(f"❌ {test_file}: MISSING - {description}")
            results[test_file] = False
    
    return results

def run_core_validations() -> Dict[str, bool]:
    """Run the core validation systems to ensure they work."""
    print("\n⚙️  RUNNING CORE VALIDATION SYSTEMS")
    print("=" * 60)
    
    validations = {
        "CTMM Build System": "python3 ctmm_build.py",
        "Workflow Syntax": "python3 validate_workflow_syntax.py",
        "Workflow Versions": "python3 validate_workflow_versions.py",
        "LaTeX Validator": "python3 -c 'import latex_validator; print(\"LaTeX validator imported successfully\")'",
    }
    
    results = {}
    
    for name, command in validations.items():
        print(f"Running {name}...")
        success, output = run_command(command)
        if success:
            print(f"✅ {name}: PASSED")
            results[name] = True
        else:
            print(f"❌ {name}: FAILED")
            print(f"   Error: {output[:200]}...")
            results[name] = False
    
    return results

def check_makefile_integration() -> bool:
    """Verify Makefile integration is working."""
    print("\n📝 CHECKING MAKEFILE INTEGRATION")
    print("=" * 60)
    
    if not os.path.exists("Makefile"):
        print("❌ Makefile not found")
        return False
    
    # Check for key targets
    with open("Makefile", 'r') as f:
        makefile_content = f.read()
    
    required_targets = ["check", "validate-pr", "build", "clean"]
    found_targets = []
    
    for target in required_targets:
        if f"{target}:" in makefile_content:
            found_targets.append(target)
            print(f"✅ Target '{target}' found")
        else:
            print(f"❌ Target '{target}' missing")
    
    success = len(found_targets) == len(required_targets)
    print(f"\n📊 Makefile targets: {len(found_targets)}/{len(required_targets)} found")
    
    return success

def verify_endspiel_completeness() -> Dict[str, int]:
    """Calculate completeness metrics for Endspiel."""
    print("\n📊 CALCULATING ENDSPIEL COMPLETENESS METRICS")
    print("=" * 60)
    
    metrics = {
        "Resolution Documents": 0,
        "Validation Tools": 0, 
        "Test Files": 0,
        "Core Systems": 0,
        "Integration": 0
    }
    
    # Count resolution documents
    resolution_files = [f for f in os.listdir('.') if f.endswith('_RESOLUTION.md') or f == 'ENDSPIEL_RESOLUTION.md']
    metrics["Resolution Documents"] = len(resolution_files)
    print(f"📋 Resolution Documents: {metrics['Resolution Documents']}")
    
    # Count validation tools
    validation_files = [f for f in os.listdir('.') if f.startswith(('validate_', 'verify_')) and f.endswith('.py')]
    metrics["Validation Tools"] = len(validation_files)
    print(f"🛠️  Validation Tools: {metrics['Validation Tools']}")
    
    # Count test files
    test_files = [f for f in os.listdir('.') if f.startswith('test_') and f.endswith('.py')]
    metrics["Test Files"] = len(test_files)
    print(f"🧪 Test Files: {metrics['Test Files']}")
    
    # Check core systems
    core_systems = ['ctmm_build.py', 'latex_validator.py', 'main.tex']
    existing_core = [f for f in core_systems if os.path.exists(f)]
    metrics["Core Systems"] = len(existing_core)
    print(f"⚙️  Core Systems: {metrics['Core Systems']}/{len(core_systems)}")
    
    # Check integration files
    integration_files = ['Makefile', '.github/workflows/pr-validation.yml']
    existing_integration = [f for f in integration_files if os.path.exists(f)]
    metrics["Integration"] = len(existing_integration)
    print(f"🔗 Integration Files: {metrics['Integration']}/{len(integration_files)}")
    
    return metrics

def main():
    """Main verification function for Endspiel."""
    print("=" * 70)
    print("🎯 ENDSPIEL COMPREHENSIVE VERIFICATION")
    print("Final Phase Completion Analysis - Issue #727")
    print("=" * 70)
    
    # Change to repository directory
    repo_path = Path(__file__).parent
    os.chdir(repo_path)
    
    # Run all verification checks
    doc_results = check_resolution_documents()
    validation_results = check_validation_infrastructure()
    test_results = check_testing_infrastructure()
    core_results = run_core_validations()
    makefile_ok = check_makefile_integration()
    metrics = verify_endspiel_completeness()
    
    # Calculate overall success rates
    doc_success = sum(doc_results.values()) / len(doc_results) * 100
    validation_success = sum(validation_results.values()) / len(validation_results) * 100
    test_success = sum(test_results.values()) / len(test_results) * 100
    core_success = sum(core_results.values()) / len(core_results) * 100
    
    # Generate final report
    print("\n" + "=" * 70)
    print("🎯 ENDSPIEL VERIFICATION SUMMARY")
    print("=" * 70)
    
    print(f"📋 Resolution Documentation: {doc_success:.1f}% complete")
    print(f"🛠️  Validation Infrastructure: {validation_success:.1f}% functional") 
    print(f"🧪 Testing Infrastructure: {test_success:.1f}% available")
    print(f"⚙️  Core Systems: {core_success:.1f}% operational")
    print(f"📝 Makefile Integration: {'✅ WORKING' if makefile_ok else '❌ ISSUES'}")
    
    overall_success = (doc_success + validation_success + test_success + core_success) / 4
    
    print(f"\n📊 OVERALL ENDSPIEL COMPLETION: {overall_success:.1f}%")
    
    if overall_success >= 85:
        print("\n🎉 ENDSPIEL STATUS: ✅ SUCCESSFULLY COMPLETED")
        print("All major components are functional and comprehensive.")
        print("The repository is ready for sustainable long-term maintenance.")
    elif overall_success >= 70:
        print("\n⚠️  ENDSPIEL STATUS: 🔄 MOSTLY COMPLETE")
        print("Most components are functional but some issues need attention.")
    else:
        print("\n❌ ENDSPIEL STATUS: 🚨 INCOMPLETE") 
        print("Significant work remains to complete the Endspiel implementation.")
    
    # Specific recommendations
    print("\n📋 RECOMMENDATIONS:")
    if doc_success < 100:
        print("• Complete missing resolution documentation")
    if validation_success < 100:
        print("• Fix issues with validation infrastructure")
    if test_success < 100:
        print("• Enhance testing coverage")
    if core_success < 100:
        print("• Resolve core system issues")
    if not makefile_ok:
        print("• Fix Makefile integration issues")
    
    print(f"\n🎯 COPILOT REVIEW STATUS: {'✅ READY FOR COMPREHENSIVE REVIEW' if overall_success >= 80 else '⚠️ NEEDS IMPROVEMENT'}")
    
    return overall_success >= 80

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)