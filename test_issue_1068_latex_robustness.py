#!/usr/bin/env python3
"""
Test suite for Issue #1068 LaTeX Robustness Improvements

This comprehensive test validates the robustness improvements and fallback mechanisms
implemented to fix CI pipeline failures related to LaTeX compilation.

Key areas tested:
- Migration from dante-ev/latex-action to xu-cheng/latex-action@v3
- Fallback mechanism validation
- Enhanced PDF verification
- Error recovery mechanisms
"""

import os
import subprocess
import yaml
import sys
from pathlib import Path
import tempfile
import shutil


def run_command(command, description="", check=True):
    """Run a shell command and return success status and output."""
    try:
        print(f"Running: {description if description else command}")
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, timeout=60
        )
        if check and result.returncode != 0:
            print(f"❌ Command failed: {command}")
            print(f"   stdout: {result.stdout}")
            print(f"   stderr: {result.stderr}")
            return False, result.stdout, result.stderr
        return True, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        print(f"❌ Command timed out: {command}")
        return False, "", "Command timed out"
    except Exception as e:
        print(f"❌ Command error: {command} - {e}")
        return False, "", str(e)


def test_workflow_migration():
    """Test that workflows have been migrated from dante-ev to xu-cheng LaTeX action."""
    print("\n📋 TESTING WORKFLOW MIGRATION")
    print("=" * 50)
    
    success = True
    workflows_to_check = [
        ".github/workflows/latex-build.yml",
        ".github/workflows/automated-pr-merge-test.yml"
    ]
    
    for workflow_file in workflows_to_check:
        if not Path(workflow_file).exists():
            print(f"❌ Workflow file not found: {workflow_file}")
            success = False
            continue
            
        with open(workflow_file, 'r') as f:
            content = f.read()
            
        # Check that dante-ev/latex-action is no longer used (except in comments)
        lines = content.split('\n')
        problematic_lines = []
        for i, line in enumerate(lines, 1):
            if 'dante-ev/latex-action' in line and not line.strip().startswith('#'):
                problematic_lines.append((i, line.strip()))
        
        if problematic_lines:
            print(f"❌ {workflow_file}: Still contains dante-ev/latex-action references:")
            for line_num, line in problematic_lines:
                print(f"   Line {line_num}: {line}")
            success = False
        else:
            print(f"✅ {workflow_file}: No dante-ev/latex-action references found")
            
        # Check that xu-cheng/latex-action@v3 is present
        if 'xu-cheng/latex-action@v3' in content:
            print(f"✅ {workflow_file}: xu-cheng/latex-action@v3 found")
        else:
            print(f"❌ {workflow_file}: xu-cheng/latex-action@v3 not found")
            success = False
    
    return success


def test_fallback_mechanism():
    """Test that fallback mechanisms are properly implemented."""
    print("\n🔄 TESTING FALLBACK MECHANISM")
    print("=" * 50)
    
    success = True
    workflows_to_check = [
        ".github/workflows/latex-build.yml",
        ".github/workflows/automated-pr-merge-test.yml"
    ]
    
    for workflow_file in workflows_to_check:
        if not Path(workflow_file).exists():
            print(f"❌ Workflow file not found: {workflow_file}")
            success = False
            continue
            
        with open(workflow_file, 'r') as f:
            content = f.read()
            
        # Check for fallback step
        fallback_indicators = [
            "Set up LaTeX (Fallback",
            "Manual TeX Live",
            "steps.latex_primary.outcome == 'failure'",
            "sudo apt-get install"
        ]
        
        found_indicators = []
        for indicator in fallback_indicators:
            if indicator in content:
                found_indicators.append(indicator)
        
        if len(found_indicators) >= 3:  # Should have at least 3 of these indicators
            print(f"✅ {workflow_file}: Fallback mechanism properly implemented")
            print(f"   Found indicators: {', '.join(found_indicators)}")
        else:
            print(f"❌ {workflow_file}: Fallback mechanism missing or incomplete")
            print(f"   Found only: {', '.join(found_indicators)}")
            success = False
    
    return success


def test_enhanced_pdf_verification():
    """Test that enhanced PDF verification is implemented."""
    print("\n📄 TESTING ENHANCED PDF VERIFICATION")
    print("=" * 50)
    
    success = True
    workflows_to_check = [
        ".github/workflows/latex-build.yml",
        ".github/workflows/automated-pr-merge-test.yml"
    ]
    
    for workflow_file in workflows_to_check:
        if not Path(workflow_file).exists():
            print(f"❌ Workflow file not found: {workflow_file}")
            success = False
            continue
            
        with open(workflow_file, 'r') as f:
            content = f.read()
            
        # Check for enhanced verification features
        enhancement_indicators = [
            "Enhanced PDF verification",
            "PDF File Analysis",
            "pdfinfo",
            "file main.pdf",
            "Diagnostic Information",
            "tail -30"
        ]
        
        found_indicators = []
        for indicator in enhancement_indicators:
            if indicator in content:
                found_indicators.append(indicator)
        
        if len(found_indicators) >= 4:  # Should have at least 4 of these indicators
            print(f"✅ {workflow_file}: Enhanced PDF verification implemented")
            print(f"   Found indicators: {', '.join(found_indicators)}")
        else:
            print(f"❌ {workflow_file}: Enhanced PDF verification missing or incomplete")
            print(f"   Found only: {', '.join(found_indicators)}")
            success = False
    
    return success


def test_workflow_syntax():
    """Test that workflows have valid YAML syntax."""
    print("\n✅ TESTING WORKFLOW SYNTAX")
    print("=" * 50)
    
    success = True
    workflows_to_check = [
        ".github/workflows/latex-build.yml",
        ".github/workflows/automated-pr-merge-test.yml"
    ]
    
    for workflow_file in workflows_to_check:
        if not Path(workflow_file).exists():
            print(f"❌ Workflow file not found: {workflow_file}")
            success = False
            continue
            
        try:
            with open(workflow_file, 'r') as f:
                yaml.safe_load(f)
            print(f"✅ {workflow_file}: Valid YAML syntax")
        except yaml.YAMLError as e:
            print(f"❌ {workflow_file}: Invalid YAML syntax")
            print(f"   Error: {e}")
            success = False
        except Exception as e:
            print(f"❌ {workflow_file}: Error reading file")
            print(f"   Error: {e}")
            success = False
    
    return success


def test_error_recovery_mechanisms():
    """Test that error recovery mechanisms are properly implemented."""
    print("\n🛡️ TESTING ERROR RECOVERY MECHANISMS")
    print("=" * 50)
    
    success = True
    workflows_to_check = [
        ".github/workflows/latex-build.yml",
        ".github/workflows/automated-pr-merge-test.yml"
    ]
    
    for workflow_file in workflows_to_check:
        if not Path(workflow_file).exists():
            print(f"❌ Workflow file not found: {workflow_file}")
            success = False
            continue
            
        with open(workflow_file, 'r') as f:
            content = f.read()
            
        # Check for error recovery features
        recovery_indicators = [
            "continue-on-error: true",
            "timeout-minutes:",
            "if: failure()",
            "upload-artifact",
            "outcome == 'failure'"
        ]
        
        found_indicators = []
        for indicator in recovery_indicators:
            if indicator in content:
                found_indicators.append(indicator)
        
        if len(found_indicators) >= 3:  # Should have at least 3 of these indicators
            print(f"✅ {workflow_file}: Error recovery mechanisms implemented")
            print(f"   Found indicators: {', '.join(found_indicators)}")
        else:
            print(f"❌ {workflow_file}: Error recovery mechanisms insufficient")
            print(f"   Found only: {', '.join(found_indicators)}")
            success = False
    
    return success


def test_latex_packages_configuration():
    """Test that LaTeX package configuration is maintained across both actions."""
    print("\n📦 TESTING LATEX PACKAGES CONFIGURATION")
    print("=" * 50)
    
    success = True
    required_packages = [
        "texlive-lang-german",
        "texlive-fonts-recommended", 
        "texlive-latex-recommended",
        "texlive-fonts-extra",
        "texlive-latex-extra",
        "texlive-science",
        "texlive-pstricks"
    ]
    
    workflows_to_check = [
        ".github/workflows/latex-build.yml",
        ".github/workflows/automated-pr-merge-test.yml"
    ]
    
    for workflow_file in workflows_to_check:
        if not Path(workflow_file).exists():
            print(f"❌ Workflow file not found: {workflow_file}")
            success = False
            continue
            
        with open(workflow_file, 'r') as f:
            content = f.read()
            
        missing_packages = []
        for package in required_packages:
            if package not in content:
                missing_packages.append(package)
        
        if missing_packages:
            print(f"❌ {workflow_file}: Missing required packages: {', '.join(missing_packages)}")
            success = False
        else:
            print(f"✅ {workflow_file}: All required LaTeX packages configured")
            
        # Check that packages appear in both primary and fallback sections
        primary_count = content.count("extra_system_packages:")
        fallback_count = content.count("sudo apt-get install")
        
        if primary_count > 0 and fallback_count > 0:
            print(f"✅ {workflow_file}: Packages configured in both primary and fallback")
        else:
            print(f"❌ {workflow_file}: Package configuration missing in primary or fallback")
            success = False
    
    return success


def test_comprehensive_integration():
    """Test overall integration and completeness of the robustness improvements."""
    print("\n🔧 TESTING COMPREHENSIVE INTEGRATION")
    print("=" * 50)
    
    success = True
    
    # Test that both workflows exist and are readable
    required_files = [
        ".github/workflows/latex-build.yml",
        ".github/workflows/automated-pr-merge-test.yml"
    ]
    
    for file_path in required_files:
        if not Path(file_path).exists():
            print(f"❌ Required file missing: {file_path}")
            success = False
        else:
            print(f"✅ Required file found: {file_path}")
    
    # Test that the improvements are cohesive across workflows
    workflow_contents = {}
    for file_path in required_files:
        if Path(file_path).exists():
            with open(file_path, 'r') as f:
                workflow_contents[file_path] = f.read()
    
    if len(workflow_contents) == 2:
        # Check that both workflows use the same LaTeX action version
        latex_actions_1 = workflow_contents[required_files[0]].count("xu-cheng/latex-action@v3")
        latex_actions_2 = workflow_contents[required_files[1]].count("xu-cheng/latex-action@v3")
        
        if latex_actions_1 > 0 and latex_actions_2 > 0:
            print("✅ Both workflows use xu-cheng/latex-action@v3")
        else:
            print(f"❌ Inconsistent LaTeX action usage: {latex_actions_1} vs {latex_actions_2}")
            success = False
    
    return success


def main():
    """Main test execution function."""
    print("=" * 70)
    print("Issue #1068 LaTeX Robustness Test Suite")
    print("=" * 70)
    print("Testing CI pipeline improvements and fallback mechanisms")
    print()
    
    # Change to repository directory if needed
    repo_path = Path(__file__).parent
    os.chdir(repo_path)
    
    # Run all tests
    tests = [
        ("Workflow Migration", test_workflow_migration),
        ("Fallback Mechanism", test_fallback_mechanism),
        ("Enhanced PDF Verification", test_enhanced_pdf_verification),
        ("Workflow Syntax", test_workflow_syntax),
        ("Error Recovery Mechanisms", test_error_recovery_mechanisms),
        ("LaTeX Packages Configuration", test_latex_packages_configuration),
        ("Comprehensive Integration", test_comprehensive_integration),
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ Test '{test_name}' failed with exception: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:.<40} {status}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED")
        print("✅ LaTeX robustness improvements successfully implemented!")
        print("✅ CI pipeline should now be more reliable and robust")
        return True
    else:
        print(f"\n⚠️  {total - passed} TESTS FAILED")
        print("❌ Some robustness improvements need attention")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)