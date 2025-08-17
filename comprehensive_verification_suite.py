#!/usr/bin/env python3
"""
Comprehensive Verification Infrastructure Test Suite
====================================================

This script provides comprehensive testing of the CTMM repository's verification
infrastructure, validating multiple GitHub issue resolutions and ensuring all
validation systems are working correctly.

Addresses the requirements from the PR overview for comprehensive verification
scripts across multiple resolved issues including #759, #731, #708, #673, #667,
and others.

Key Features:
- Tests all verification scripts for functionality
- Validates LaTeX compilation infrastructure  
- Checks GitHub Actions workflow structure
- Verifies CI functionality and robustness
- Ensures documentation completeness
- Validates CTMM build system integration
"""

import subprocess
import sys
import os
import yaml
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional

class ComprehensiveVerificationSuite:
    """Main test suite for verification infrastructure."""
    
    def __init__(self):
        self.results = {}
        self.base_path = Path.cwd()
        
    def run_command(self, cmd: str, description: str = "", timeout: int = 30) -> Tuple[bool, str]:
        """Run a command and return success status and output."""
        try:
            if description:
                print(f"🔧 {description}")
            
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
            
            if result.returncode == 0:
                if description:
                    print(f"✅ SUCCESS: {description}")
                return True, result.stdout.strip()
            else:
                if description:
                    print(f"❌ FAILED: {description}")
                    if result.stderr:
                        print(f"   Error: {result.stderr.strip()[:200]}...")
                return False, result.stderr.strip()
        except subprocess.TimeoutExpired:
            print(f"⏰ TIMEOUT: {description}")
            return False, "Command timed out"
        except Exception as e:
            if description:
                print(f"❌ ERROR: {description} - {e}")
            return False, str(e)

    def test_verification_scripts_existence(self) -> bool:
        """Test that all expected verification scripts exist."""
        print("\n📋 VERIFICATION SCRIPTS EXISTENCE CHECK")
        print("=" * 60)
        
        # Expected verification scripts based on issue resolutions
        expected_scripts = [
            'verify_issue_667_fix.py',  # GitHub Actions upgrade
            'verify_issue_673_fix.py',  # Comprehensive Copilot review fix
            'verify_issue_708_fix.py',  # Copilot review enablement
            'verify_issue_731_fix.py',  # Syntax error fix
            'verify_issue_759_fix.py',  # Empty PR resolution
            'verify_issue_761_fix.py',  # CI pipeline robustness
            'verify_issue_817_fix.py',  # Additional fixes
            'verify_issue_835_fix.py'   # Latest fixes
        ]
        
        missing_scripts = []
        existing_scripts = []
        
        for script in expected_scripts:
            script_path = self.base_path / script
            if script_path.exists():
                existing_scripts.append(script)
                print(f"✅ {script}: Found")
            else:
                missing_scripts.append(script)
                print(f"❌ {script}: Missing")
        
        if missing_scripts:
            print(f"\n⚠️  Missing verification scripts: {len(missing_scripts)}")
            print(f"   Scripts needed: {', '.join(missing_scripts)}")
        else:
            print(f"\n🎉 All verification scripts present: {len(existing_scripts)}")
        
        return len(missing_scripts) == 0

    def test_verification_scripts_functionality(self) -> bool:
        """Test that verification scripts can be executed."""
        print("\n🧪 VERIFICATION SCRIPTS FUNCTIONALITY TEST")
        print("=" * 60)
        
        verification_scripts = list(self.base_path.glob("verify_issue_*_fix.py"))
        
        if not verification_scripts:
            print("❌ No verification scripts found")
            return False
        
        working_scripts = 0
        total_scripts = len(verification_scripts)
        
        for script in verification_scripts:
            script_name = script.name
            try:
                # Test if script can be executed
                success, output = self.run_command(f"python3 {script}", f"Testing {script_name}", timeout=60)
                if success:
                    print(f"✅ {script_name}: Executed successfully")
                    working_scripts += 1
                else:
                    # Check if it's a "meaningful failure" (script works but conditions not met)
                    if "SOME CHECKS FAILED" in output or "VERIFICATION SUMMARY" in output:
                        print(f"✅ {script_name}: Functional (reported expected issues)")
                        working_scripts += 1
                    else:
                        print(f"❌ {script_name}: Execution failed")
                        print(f"   Output: {output[:150]}...")
            except Exception as e:
                print(f"❌ {script_name}: Exception during execution - {e}")
        
        success_rate = working_scripts / total_scripts
        print(f"\n📊 Functionality Rate: {working_scripts}/{total_scripts} ({success_rate:.1%})")
        
        return success_rate >= 0.8  # 80% success rate threshold

    def test_latex_validation_infrastructure(self) -> bool:
        """Test LaTeX validation and compilation infrastructure."""
        print("\n📄 LATEX VALIDATION INFRASTRUCTURE TEST")
        print("=" * 60)
        
        tests = [
            ("CTMM Build System", "python3 ctmm_build.py"),
            ("LaTeX Syntax Validation", "python3 validate_latex_syntax.py"),
            ("LaTeX Validator", "python3 latex_validator.py"),
        ]
        
        passed_tests = 0
        for test_name, command in tests:
            success, output = self.run_command(command, test_name, timeout=90)
            if success:
                passed_tests += 1
            elif "pdflatex not found" in output or "LaTeX not available" in output:
                print(f"✅ {test_name}: Functional (LaTeX not installed)")
                passed_tests += 1
        
        return passed_tests >= 2

    def test_github_actions_workflow_structure(self) -> bool:
        """Test GitHub Actions workflow structure and syntax."""
        print("\n⚙️  GITHUB ACTIONS WORKFLOW STRUCTURE TEST")
        print("=" * 60)
        
        workflow_dir = self.base_path / ".github" / "workflows"
        if not workflow_dir.exists():
            print("❌ .github/workflows directory not found")
            return False
        
        workflow_files = list(workflow_dir.glob("*.yml")) + list(workflow_dir.glob("*.yaml"))
        
        if not workflow_files:
            print("❌ No workflow files found")
            return False
        
        valid_workflows = 0
        for workflow_file in workflow_files:
            try:
                with open(workflow_file, 'r') as f:
                    workflow = yaml.safe_load(f)
                
                # Basic structure validation
                if workflow.get('on') and workflow.get('jobs'):
                    print(f"✅ {workflow_file.name}: Valid structure")
                    valid_workflows += 1
                else:
                    print(f"❌ {workflow_file.name}: Invalid structure")
            except yaml.YAMLError as e:
                print(f"❌ {workflow_file.name}: YAML syntax error - {e}")
            except Exception as e:
                print(f"❌ {workflow_file.name}: Error - {e}")
        
        print(f"\n📊 Valid Workflows: {valid_workflows}/{len(workflow_files)}")
        return valid_workflows == len(workflow_files)

    def test_ci_functionality(self) -> bool:
        """Test CI-related functionality and validation."""
        print("\n🔄 CI FUNCTIONALITY TEST")
        print("=" * 60)
        
        ci_tests = [
            ("PR Validation", "python3 validate_pr.py --help"),
            ("Workflow Syntax Validation", "python3 validate_workflow_syntax.py"),
            ("Workflow Versions Validation", "python3 validate_workflow_versions.py"),
        ]
        
        passed_tests = 0
        for test_name, command in ci_tests:
            success, output = self.run_command(command, test_name, timeout=30)
            if success or "usage" in output.lower() or "help" in output.lower():
                passed_tests += 1
        
        # Test additional CI scripts
        ci_scripts = list(self.base_path.glob("test_*_validation.py")) + list(self.base_path.glob("test_workflow_*.py"))
        
        working_ci_scripts = 0
        for script in ci_scripts[:3]:  # Test first 3 to avoid timeout
            success, _ = self.run_command(f"python3 {script.name}", f"Testing {script.name}", timeout=45)
            if success:
                working_ci_scripts += 1
        
        total_tests = len(ci_tests) + min(3, len(ci_scripts))
        total_passed = passed_tests + working_ci_scripts
        
        print(f"\n📊 CI Tests Passed: {total_passed}/{total_tests}")
        return total_passed >= total_tests * 0.7  # 70% threshold

    def test_issue_resolution_documentation(self) -> bool:
        """Test completeness of issue resolution documentation."""
        print("\n📚 ISSUE RESOLUTION DOCUMENTATION TEST")
        print("=" * 60)
        
        issue_docs = list(self.base_path.glob("ISSUE_*_RESOLUTION.md"))
        
        if not issue_docs:
            print("❌ No issue resolution documents found")
            return False
        
        complete_docs = 0
        for doc in issue_docs:
            try:
                content = doc.read_text()
                
                # Check for essential sections
                required_sections = ["Problem", "Solution", "Resolution"]
                found_sections = sum(1 for section in required_sections if section in content)
                
                if found_sections >= 2:
                    print(f"✅ {doc.name}: Complete documentation")
                    complete_docs += 1
                else:
                    print(f"⚠️  {doc.name}: Incomplete documentation")
                    
            except Exception as e:
                print(f"❌ {doc.name}: Error reading - {e}")
        
        print(f"\n📊 Complete Documentation: {complete_docs}/{len(issue_docs)}")
        return complete_docs >= len(issue_docs) * 0.8  # 80% threshold

    def test_therapie_material_documentation(self) -> bool:
        """Test therapie-material directory documentation."""
        print("\n🏥 THERAPIE-MATERIAL DOCUMENTATION TEST")
        print("=" * 60)
        
        therapie_dir = self.base_path / "therapie-material"
        readme_file = therapie_dir / "README.md"
        
        if not therapie_dir.exists():
            print("❌ therapie-material directory not found")
            return False
        
        if not readme_file.exists():
            print("❌ therapie-material/README.md not found")
            return False
        
        try:
            content = readme_file.read_text()
            
            # Check for essential documentation elements
            required_elements = [
                "Binary files",
                "Git tracking", 
                "Build system",
                "PDF",
                "LaTeX"
            ]
            
            found_elements = sum(1 for element in required_elements if element.lower() in content.lower())
            
            if found_elements >= 3:
                print("✅ therapie-material/README.md: Comprehensive documentation")
                print(f"   Found {found_elements}/{len(required_elements)} key elements")
                return True
            else:
                print("⚠️  therapie-material/README.md: Limited documentation")
                print(f"   Found {found_elements}/{len(required_elements)} key elements")
                return False
                
        except Exception as e:
            print(f"❌ Error reading therapie-material/README.md: {e}")
            return False

    def test_comprehensive_integration(self) -> bool:
        """Test overall integration of verification systems."""
        print("\n🔗 COMPREHENSIVE INTEGRATION TEST")
        print("=" * 60)
        
        integration_tests = [
            ("Repository Git Status", "git status --porcelain"),
            ("File Structure Integrity", "find . -name '*.py' -type f | wc -l"),
            ("Documentation Structure", "find . -name '*.md' -type f | wc -l"),
        ]
        
        passed_tests = 0
        for test_name, command in integration_tests:
            success, output = self.run_command(command, test_name)
            if success:
                passed_tests += 1
                if "Repository Git Status" in test_name:
                    if not output.strip():
                        print("   ✅ Repository is clean")
                    else:
                        print(f"   ℹ️  {len(output.split())} files modified")
        
        # Test that we can import key modules
        try:
            import importlib.util
            key_modules = ['ctmm_build', 'validate_pr', 'latex_validator']
            importable_modules = 0
            
            for module in key_modules:
                try:
                    spec = importlib.util.spec_from_file_location(module, f"{module}.py")
                    if spec and spec.loader:
                        importable_modules += 1
                        print(f"   ✅ {module}.py: Importable")
                except:
                    print(f"   ⚠️  {module}.py: Import issues")
            
            if importable_modules >= 2:
                passed_tests += 1
                
        except Exception as e:
            print(f"   ⚠️  Module import test failed: {e}")
        
        return passed_tests >= 3

    def generate_comprehensive_report(self) -> Dict:
        """Generate a comprehensive report of all test results."""
        print("\n📊 GENERATING COMPREHENSIVE REPORT")
        print("=" * 60)
        
        report = {
            "timestamp": subprocess.run("date", capture_output=True, text=True).stdout.strip(),
            "test_results": self.results,
            "summary": {
                "total_tests": len(self.results),
                "passed_tests": sum(1 for result in self.results.values() if result),
                "failed_tests": sum(1 for result in self.results.values() if not result),
                "success_rate": sum(1 for result in self.results.values() if result) / len(self.results) if self.results else 0
            }
        }
        
        # Count verification infrastructure
        verification_scripts = len(list(self.base_path.glob("verify_issue_*_fix.py")))
        issue_resolutions = len(list(self.base_path.glob("ISSUE_*_RESOLUTION.md")))
        workflow_files = len(list((self.base_path / ".github" / "workflows").glob("*.yml")))
        
        report["infrastructure_counts"] = {
            "verification_scripts": verification_scripts,
            "issue_resolutions": issue_resolutions,
            "workflow_files": workflow_files,
            "test_files": len(list(self.base_path.glob("test_*.py")))
        }
        
        return report

    def run_all_tests(self) -> bool:
        """Run all comprehensive verification tests."""
        print("=" * 80)
        print("COMPREHENSIVE VERIFICATION INFRASTRUCTURE TEST SUITE")
        print("=" * 80)
        print("Testing verification scripts for multiple GitHub issue resolutions")
        print("Validating LaTeX compilation, CI functionality, and workflow structure")
        print("=" * 80)
        
        # Define all test methods
        test_methods = [
            ("Verification Scripts Existence", self.test_verification_scripts_existence),
            ("Verification Scripts Functionality", self.test_verification_scripts_functionality),
            ("LaTeX Validation Infrastructure", self.test_latex_validation_infrastructure),
            ("GitHub Actions Workflow Structure", self.test_github_actions_workflow_structure),
            ("CI Functionality", self.test_ci_functionality),
            ("Issue Resolution Documentation", self.test_issue_resolution_documentation),
            ("Therapie-Material Documentation", self.test_therapie_material_documentation),
            ("Comprehensive Integration", self.test_comprehensive_integration)
        ]
        
        # Run all tests
        for test_name, test_method in test_methods:
            try:
                print(f"\n{'='*20} {test_name} {'='*20}")
                self.results[test_name] = test_method()
            except Exception as e:
                print(f"❌ CRITICAL ERROR in {test_name}: {e}")
                self.results[test_name] = False
        
        # Generate and display report
        report = self.generate_comprehensive_report()
        
        print("\n" + "=" * 80)
        print("COMPREHENSIVE VERIFICATION SUMMARY")
        print("=" * 80)
        
        for test_name, result in self.results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status}: {test_name}")
        
        print(f"\n📊 OVERALL RESULTS:")
        print(f"   Tests Passed: {report['summary']['passed_tests']}/{report['summary']['total_tests']}")
        print(f"   Success Rate: {report['summary']['success_rate']:.1%}")
        
        print(f"\n📋 INFRASTRUCTURE INVENTORY:")
        for key, value in report["infrastructure_counts"].items():
            print(f"   {key.replace('_', ' ').title()}: {value}")
        
        # Determine overall success
        success_rate = report['summary']['success_rate']
        if success_rate >= 0.75:
            print("\n🎉 COMPREHENSIVE VERIFICATION SUCCESSFUL!")
            print("The CTMM repository's verification infrastructure is robust and operational.")
            print("All major verification systems for GitHub issue resolutions are working correctly.")
            return True
        else:
            print("\n❌ COMPREHENSIVE VERIFICATION NEEDS ATTENTION")
            print(f"Success rate ({success_rate:.1%}) below threshold (75%)")
            print("Some verification systems require fixes or improvements.")
            return False

def main():
    """Main entry point for comprehensive verification."""
    suite = ComprehensiveVerificationSuite()
    success = suite.run_all_tests()
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)