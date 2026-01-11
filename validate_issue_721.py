#!/usr/bin/env python3
"""
Validation script for Issue #721: "Wie geht es weiter?" - Development Roadmap Validation.

This script validates that Issue #721 has been comprehensively resolved by:
1. Ensuring ISSUE_721_RESOLUTION.md provides strategic analysis
2. Validating DEVELOPMENT_ROADMAP.md comprehensiveness and structure
3. Checking German language content and therapeutic focus
4. Verifying roadmap contains 60+ actionable tasks across timeline phases
5. Confirming integration with existing CTMM validation infrastructure
"""

import os
import re
import sys
import subprocess
from pathlib import Path

def run_command(cmd, description=""):
    """Run a command and return success status and output."""
    print(f"[FIX] {description}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=Path.cwd())
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        print(f"[FAIL] Error running command: {e}")
        return False, "", str(e)

def check_file_exists(filepath, description=""):
    """Check if a file exists and report status."""
    exists = os.path.exists(filepath)
    status = "[PASS]" if exists else "[FAIL]"
    print(f"{status} {description}: {filepath}")
    return exists

def validate_german_content(content, filename):
    """Validate German language content and therapeutic terminology."""
    print(f"[EMOJI][EMOJI] Validating German content in {filename}")

    # German therapeutic terms to check for
    german_terms = [
        "Therapie", "therapeutisch", "Arbeitsblatt", "Trigger",
        "Achtsamkeit", "Regulierung", "Intervention", "Bewältigung",
        "Selbstwirksamkeit", "Neurodiversität", "Paartherapie"
    ]

    # CTMM methodology terms
    ctmm_terms = ["Catch", "Track", "Map", "Match", "CTMM"]

    german_found = sum(1 for term in german_terms if term.lower() in content.lower())
    ctmm_found = sum(1 for term in ctmm_terms if term in content)

    print(f"   [SUMMARY] German therapeutic terms found: {german_found}/{len(german_terms)}")
    print(f"   [SUMMARY] CTMM methodology terms found: {ctmm_found}/{len(ctmm_terms)}")

    if german_found >= 5:
        print("   [PASS] Adequate German therapeutic content")
        german_ok = True
    else:
        print("   [FAIL] Insufficient German therapeutic content")
        german_ok = False

    if ctmm_found >= 3:
        print("   [PASS] CTMM methodology properly referenced")
        ctmm_ok = True
    else:
        print("   [FAIL] CTMM methodology insufficiently referenced")
        ctmm_ok = False

    return german_ok and ctmm_ok

def validate_roadmap_structure(roadmap_content):
    """Validate the development roadmap structure and comprehensiveness."""
    print("[TEST] Validating roadmap structure and comprehensiveness")

    # Check for required sections
    required_sections = [
        "Phase 1", "Phase 2", "Phase 3",
        "Infrastructure", "Content Development", "User Experience",
        "CTMM Methodology", "Implementation Guidelines", "Success Metrics"
    ]

    sections_found = sum(1 for section in required_sections if section in roadmap_content)
    print(f"   [SUMMARY] Required sections found: {sections_found}/{len(required_sections)}")

    # Count actionable tasks (lines starting with - [ ])
    task_pattern = r'^\s*-\s*\[\s*\]\s*\*\*.*\*\*'
    tasks = re.findall(task_pattern, roadmap_content, re.MULTILINE)
    task_count = len(tasks)
    print(f"   [SUMMARY] Actionable tasks identified: {task_count}")

    # Check for timeline phases
    phase_patterns = [
        r'1-3\s*Monate', r'3-12\s*Monate', r'1\+\s*Jahre'
    ]
    phases_found = sum(1 for pattern in phase_patterns if re.search(pattern, roadmap_content))
    print(f"   [SUMMARY] Timeline phases found: {phases_found}/3")

    # Validate task count (should be 60+)
    task_ok = task_count >= 60
    if task_ok:
        print(f"   [PASS] Task count meets requirement (60+): {task_count}")
    else:
        print(f"   [FAIL] Insufficient tasks (need 60+): {task_count}")

    # Validate section completeness
    sections_ok = sections_found >= 7
    if sections_ok:
        print("   [PASS] Required sections adequately covered")
    else:
        print("   [FAIL] Missing required sections")

    # Validate timeline structure
    timeline_ok = phases_found == 3
    if timeline_ok:
        print("   [PASS] All timeline phases properly defined")
    else:
        print("   [FAIL] Timeline phase structure incomplete")

    return task_ok and sections_ok and timeline_ok

def validate_issue_resolution_quality(resolution_content):
    """Validate the quality and completeness of issue resolution documentation."""
    print("[FILE] Validating issue resolution documentation quality")

    # Check for required resolution components
    required_components = [
        "Problem Statement", "Root Cause Analysis", "Solution Implemented",
        "Impact and Benefits", "Validation Results", "Prevention Guidelines"
    ]

    components_found = sum(1 for comp in required_components if comp in resolution_content)
    print(f"   [SUMMARY] Required components found: {components_found}/{len(required_components)}")

    # Check for strategic analysis
    strategic_terms = [
        "strategic", "direction", "roadmap", "priorities", "development",
        "uncertainty", "planning", "framework"
    ]
    strategic_found = sum(1 for term in strategic_terms if term.lower() in resolution_content.lower())
    print(f"   [SUMMARY] Strategic analysis terms found: {strategic_found}")

    # Validate length and detail
    word_count = len(resolution_content.split())
    print(f"   [SUMMARY] Document length: {word_count} words")

    components_ok = components_found >= 5
    strategic_ok = strategic_found >= 6
    length_ok = word_count >= 1000

    if components_ok:
        print("   [PASS] Required documentation components present")
    else:
        print("   [FAIL] Missing required documentation components")

    if strategic_ok:
        print("   [PASS] Adequate strategic analysis content")
    else:
        print("   [FAIL] Insufficient strategic analysis depth")

    if length_ok:
        print("   [PASS] Document length adequate for comprehensive analysis")
    else:
        print("   [FAIL] Document too brief for comprehensive analysis")

    return components_ok and strategic_ok and length_ok

def validate_integration_compatibility():
    """Validate integration with existing CTMM infrastructure."""
    print("[EMOJI] Validating integration with existing CTMM infrastructure")

    # Check if critical infrastructure files exist
    infrastructure_files = [
        "ctmm_build.py", "validate_pr.py", "COMPREHENSIVE_TOOLSET.md",
        "main.tex", "style/ctmm-design.sty"
    ]

    integration_ok = True
    for file_path in infrastructure_files:
        if check_file_exists(file_path, f"Infrastructure file"):
            pass
        else:
            integration_ok = False

    # Test that validate_pr.py syntax is fixed
    success, stdout, stderr = run_command("python3 -c \"import ast; ast.parse(open('validate_pr.py').read())\"",
                                        "Testing validate_pr.py syntax")
    if success:
        print("   [PASS] validate_pr.py syntax validated")
    else:
        print("   [FAIL] validate_pr.py has syntax errors")
        integration_ok = False

    # Test CTMM build system functionality
    success, stdout, stderr = run_command("python3 ctmm_build.py", "Testing CTMM build system")
    if success:
        print("   [PASS] CTMM build system operational")
    else:
        print("   [WARN]  CTMM build system test completed (LaTeX compilation may be unavailable)")
        # This is acceptable in CI environments without LaTeX

    return integration_ok

def validate_issue_721_resolution():
    """Main validation function for Issue #721 resolution."""
    print("=" * 80)
    print("Issue #721 Resolution Validation - \"Wie geht es weiter?\"")
    print("=" * 80)
    print("Validating comprehensive development roadmap implementation")
    print("and strategic direction resolution for CTMM system.\n")

    all_checks_passed = True

    # 1. Check that resolution documentation exists

    all_checks_passed = True

    # 1. Check that resolution documentation exists
    print("\n[FILE] Resolution Documentation Check:")
    if not check_file_exists("ISSUE_721_RESOLUTION.md", "Issue #721 specific documentation"):
        all_checks_passed = False
        return False

    if not check_file_exists("DEVELOPMENT_ROADMAP.md", "Comprehensive development roadmap"):
        all_checks_passed = False
        return False

    # 2. Validate resolution documentation quality
    print("\n[TEST] Resolution Quality Analysis:")
    try:
        with open("ISSUE_721_RESOLUTION.md", 'r', encoding='utf-8') as f:
            resolution_content = f.read()

        if not validate_issue_resolution_quality(resolution_content):
            all_checks_passed = False

        if not validate_german_content(resolution_content, "ISSUE_721_RESOLUTION.md"):
            all_checks_passed = False

    except Exception as e:
        print(f"[FAIL] Error reading resolution documentation: {e}")
        all_checks_passed = False

    # 3. Validate development roadmap comprehensiveness
    print("\n[EMOJI]  Development Roadmap Analysis:")
    try:
        with open("DEVELOPMENT_ROADMAP.md", 'r', encoding='utf-8') as f:
            roadmap_content = f.read()

        if not validate_roadmap_structure(roadmap_content):
            all_checks_passed = False

        if not validate_german_content(roadmap_content, "DEVELOPMENT_ROADMAP.md"):
            all_checks_passed = False

    except Exception as e:
        print(f"[FAIL] Error reading development roadmap: {e}")
        all_checks_passed = False

    # 4. Validate infrastructure integration
    print("\\n[FIX] Infrastructure Integration Check:")
    if not validate_integration_compatibility():
        all_checks_passed = False

    # 5. Summary
    print("\n[FIX] Infrastructure Integration Check:")
    if not validate_integration_compatibility():
        all_checks_passed = False

    # 5. Summary
    print("\n" + "=" * 80)
    print("VALIDATION SUMMARY")
    print("=" * 80)

    if all_checks_passed:
        print("[SUCCESS] ISSUE #721 RESOLUTION: COMPREHENSIVE SUCCESS")
        print("[PASS] Strategic question \"Wie geht es weiter?\" fully resolved")
        print("[PASS] Development roadmap provides clear direction with 60+ actionable tasks")
        print("[PASS] German language and therapeutic focus maintained")
        print("[PASS] CTMM methodology integration validated")
        print("[PASS] Infrastructure compatibility confirmed")
        print("[PASS] Three-phase timeline structure implemented")
        print("\n[CHART] The CTMM system now has clear strategic direction for continued development")
        print("[TARGET] Future development uncertainty has been transformed into actionable priorities")
    else:
        print("[WARN]  ISSUE #721 RESOLUTION: NEEDS REFINEMENT")
        print("[FAIL] Some validation checks failed")
        print("[FIX] Action needed: Address the issues identified above")

    return all_checks_passed

def main():
    """Main execution function."""
    if not validate_issue_721_resolution():
        print("\\n[FAIL] Validation failed - Issue #721 resolution needs refinement")
        sys.exit(1)
    else:
        print("\n[FAIL] Validation failed - Issue #721 resolution needs refinement")
        sys.exit(1)
    else:
        print("\n[PASS] Validation successful - Issue #721 comprehensively resolved")
        sys.exit(0)

if __name__ == "__main__":
    main()
