#!/usr/bin/env python3
"""
Comprehensive validation test suite for Issue #743: CI failures prevention

This test suite provides comprehensive validation for:
- CI configuration and workflow syntax
- LaTeX package dependencies 
- Error detection capabilities
- Early validation before expensive LaTeX compilation

Created to address CI failures by ensuring robust validation and error detection.
"""

import yaml
import os
import sys
import subprocess
import re
from pathlib import Path

class CIValidationTestSuite:
    """Comprehensive CI validation test suite for CTMM system."""
    
    def __init__(self):
        self.test_results = []
        self.total_tests = 0
        self.passed_tests = 0
        
    def log_test(self, test_name, passed, message=""):
        """Log test result."""
        self.total_tests += 1
        if passed:
            self.passed_tests += 1
            status = "✅ PASS"
        else:
            status = "❌ FAIL"
            
        result = f"{status} {test_name}"
        if message:
            result += f": {message}"
        
        print(result)
        self.test_results.append((test_name, passed, message))
        return passed

    def test_workflow_syntax_validation(self):
        """Test that all GitHub Actions workflow files have valid YAML syntax."""
        workflow_files = [
            '.github/workflows/latex-build.yml',
            '.github/workflows/latex-validation.yml', 
            '.github/workflows/static.yml'
        ]
        
        all_valid = True
        for file_path in workflow_files:
            if not os.path.exists(file_path):
                self.log_test(f"Workflow file existence", False, f"{file_path} not found")
                all_valid = False
                continue
                
            try:
                with open(file_path, 'r') as f:
                    yaml.safe_load(f)
                self.log_test(f"YAML syntax {os.path.basename(file_path)}", True, "Valid YAML")
            except yaml.YAMLError as e:
                self.log_test(f"YAML syntax {os.path.basename(file_path)}", False, f"YAML error: {e}")
                all_valid = False
            except Exception as e:
                self.log_test(f"YAML syntax {os.path.basename(file_path)}", False, f"Error: {e}")
                all_valid = False
                
        return all_valid

    def test_ci_configuration_structure(self):
        """Test CI configuration structure and required components."""
        workflow_path = '.github/workflows/latex-build.yml'
        
        if not os.path.exists(workflow_path):
            return self.log_test("CI configuration structure", False, "Main workflow file missing")
            
        try:
            with open(workflow_path, 'r') as f:
                workflow = yaml.safe_load(f)
        except Exception as e:
            return self.log_test("CI configuration structure", False, f"Failed to parse workflow: {e}")
            
        # Test required fields
        required_fields = ['name', 'on', 'jobs']
        for field in required_fields:
            if field not in workflow:
                return self.log_test("CI configuration structure", False, f"Missing field: {field}")
                
        # Test job structure
        jobs = workflow.get('jobs', {})
        if 'build' not in jobs:
            return self.log_test("CI configuration structure", False, "Missing 'build' job")
            
        build_job = jobs['build']
        if 'runs-on' not in build_job:
            return self.log_test("CI configuration structure", False, "Missing 'runs-on' in build job")
            
        if 'steps' not in build_job:
            return self.log_test("CI configuration structure", False, "Missing 'steps' in build job")
            
        return self.log_test("CI configuration structure", True, "All required components present")

    def test_latex_package_dependencies(self):
        """Test LaTeX package dependencies are properly configured."""
        workflow_path = '.github/workflows/latex-build.yml'
        
        if not os.path.exists(workflow_path):
            return self.log_test("LaTeX package dependencies", False, "Workflow file missing")
            
        try:
            with open(workflow_path, 'r') as f:
                workflow = yaml.safe_load(f)
        except Exception as e:
            return self.log_test("LaTeX package dependencies", False, f"Failed to parse workflow: {e}")
            
        # Find LaTeX setup step
        build_job = workflow.get('jobs', {}).get('build', {})
        steps = build_job.get('steps', [])
        
        latex_step = None
        for step in steps:
            if step.get('name') == 'Set up LaTeX':
                latex_step = step
                break
                
        if not latex_step:
            return self.log_test("LaTeX package dependencies", False, "'Set up LaTeX' step not found")
            
        # Check for essential packages
        extra_packages = latex_step.get('with', {}).get('extra_system_packages', '')
        essential_packages = [
            'texlive-lang-german',
            'texlive-latex-recommended', 
            'texlive-latex-extra',
            'texlive-fonts-extra'
        ]
        
        missing_packages = []
        for pkg in essential_packages:
            if pkg not in extra_packages:
                missing_packages.append(pkg)
                
        if missing_packages:
            return self.log_test("LaTeX package dependencies", False, f"Missing packages: {missing_packages}")
            
        # Specifically check for pifont support (Issue #739)
        pifont_packages = ['texlive-pstricks', 'texlive-latex-extra', 'texlive-fonts-extra']
        has_pifont_support = any(pkg in extra_packages for pkg in pifont_packages)
        
        if not has_pifont_support:
            return self.log_test("LaTeX package dependencies", False, "No pifont package support found")
            
        return self.log_test("LaTeX package dependencies", True, "All essential packages configured")

    def test_validation_steps_order(self):
        """Test that validation steps run before expensive LaTeX compilation."""
        workflow_path = '.github/workflows/latex-build.yml'
        
        if not os.path.exists(workflow_path):
            return self.log_test("Validation steps order", False, "Workflow file missing")
            
        try:
            with open(workflow_path, 'r') as f:
                workflow = yaml.safe_load(f)
        except Exception as e:
            return self.log_test("Validation steps order", False, f"Failed to parse workflow: {e}")
            
        build_job = workflow.get('jobs', {}).get('build', {})
        steps = build_job.get('steps', [])
        
        # Find step indices
        validation_indices = []
        latex_index = None
        
        for i, step in enumerate(steps):
            step_name = step.get('name', '')
            if 'validation' in step_name.lower() or 'check' in step_name.lower():
                validation_indices.append(i)
            elif step_name == 'Set up LaTeX':
                latex_index = i
                
        if latex_index is None:
            return self.log_test("Validation steps order", False, "LaTeX setup step not found")
            
        # Check that validation steps come before LaTeX setup
        validation_before_latex = all(i < latex_index for i in validation_indices)
        
        if not validation_before_latex:
            return self.log_test("Validation steps order", False, "Some validation steps after LaTeX setup")
            
        if not validation_indices:
            return self.log_test("Validation steps order", False, "No validation steps found")
            
        return self.log_test("Validation steps order", True, f"Validation steps properly ordered before LaTeX")

    def test_error_detection_capabilities(self):
        """Test error detection and early failure capabilities."""
        # Test that validation tools are available
        validation_tools = [
            'validate_latex_syntax.py',
            'ctmm_build.py',
            'test_workflow_structure.py'
        ]
        
        missing_tools = []
        for tool in validation_tools:
            if not os.path.exists(tool):
                missing_tools.append(tool)
                
        if missing_tools:
            return self.log_test("Error detection capabilities", False, f"Missing tools: {missing_tools}")
            
        # Test that tools can be executed
        try:
            # Test LaTeX syntax validation
            result = subprocess.run([sys.executable, 'validate_latex_syntax.py'], 
                                  capture_output=True, text=True, timeout=30)
            if result.returncode not in [0, 1]:  # 0=success, 1=validation failure expected
                return self.log_test("Error detection capabilities", False, 
                                   f"LaTeX validation tool error: {result.stderr}")
        except Exception as e:
            return self.log_test("Error detection capabilities", False, f"Tool execution error: {e}")
            
        return self.log_test("Error detection capabilities", True, "All validation tools functional")

    def test_form_elements_dependency_consistency(self):
        """Test that form elements dependency is consistent with CI configuration."""
        # Check that form-elements.sty requires pifont
        form_elements_path = 'style/form-elements.sty'
        
        if not os.path.exists(form_elements_path):
            return self.log_test("Form elements dependency", False, "form-elements.sty not found")
            
        try:
            with open(form_elements_path, 'r') as f:
                content = f.read()
        except Exception as e:
            return self.log_test("Form elements dependency", False, f"Failed to read file: {e}")
            
        # Check for pifont requirement
        if '\\RequirePackage{pifont}' not in content:
            return self.log_test("Form elements dependency", False, "pifont package not required")
            
        # Check usage of pifont symbols
        if '\\ding{' not in content:
            return self.log_test("Form elements dependency", False, "pifont symbols not used")
            
        return self.log_test("Form elements dependency", True, "pifont dependency consistent")

    def test_comprehensive_validation_coverage(self):
        """Test that comprehensive validation covers all critical components."""
        critical_components = [
            'main.tex',
            'style/ctmm-design.sty',
            'style/form-elements.sty', 
            'style/ctmm-diagrams.sty'
        ]
        
        missing_components = []
        for component in critical_components:
            if not os.path.exists(component):
                missing_components.append(component)
                
        if missing_components:
            return self.log_test("Comprehensive validation coverage", False, 
                               f"Missing critical components: {missing_components}")
            
        # Test that build system covers these components
        try:
            result = subprocess.run([sys.executable, 'ctmm_build.py'], 
                                  capture_output=True, text=True, timeout=60)
            
            # Should mention style files and modules
            output = result.stdout + result.stderr
            if 'style files' not in output.lower() or 'module files' not in output.lower():
                return self.log_test("Comprehensive validation coverage", False, 
                                   "Build system doesn't validate all components")
                                   
        except Exception as e:
            return self.log_test("Comprehensive validation coverage", False, 
                               f"Build system test failed: {e}")
            
        return self.log_test("Comprehensive validation coverage", True, 
                           "All critical components covered")

    def run_all_tests(self):
        """Run all validation tests."""
        print("=" * 70)
        print("COMPREHENSIVE CI VALIDATION TEST SUITE - Issue #743")
        print("=" * 70)
        print("Testing CI configuration, package dependencies, and error detection...")
        print()
        
        # Run all test methods
        test_methods = [
            self.test_workflow_syntax_validation,
            self.test_ci_configuration_structure,
            self.test_latex_package_dependencies,
            self.test_validation_steps_order,
            self.test_error_detection_capabilities,
            self.test_form_elements_dependency_consistency,
            self.test_comprehensive_validation_coverage
        ]
        
        for test_method in test_methods:
            test_method()
            
        print()
        print("=" * 70)
        print("VALIDATION SUMMARY")
        print("=" * 70)
        
        for test_name, passed, message in self.test_results:
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"{status} {test_name}")
            if message and not passed:
                print(f"    {message}")
                
        print()
        print(f"Tests passed: {self.passed_tests}/{self.total_tests}")
        
        if self.passed_tests == self.total_tests:
            print("🎉 ALL TESTS PASSED - CI validation comprehensive and robust!")
            print()
            print("✅ CI configuration properly structured")
            print("✅ LaTeX package dependencies complete")
            print("✅ Validation steps run before compilation")
            print("✅ Error detection capabilities functional")
            print("✅ Package dependencies consistent")
            print("✅ Comprehensive validation coverage achieved")
            return True
        else:
            print("❌ SOME TESTS FAILED - CI validation needs improvement")
            failed_count = self.total_tests - self.passed_tests
            print(f"   {failed_count} test(s) failed out of {self.total_tests}")
            return False

def main():
    """Main test execution function."""
    test_suite = CIValidationTestSuite()
    success = test_suite.run_all_tests()
    return success

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)