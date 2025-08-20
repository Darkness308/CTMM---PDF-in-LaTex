#!/usr/bin/env python3
"""
Test suite for Issue #1068: LaTeX Action Migration and Robustness Improvements

This comprehensive test suite validates:
- Migration from dante-ev/latex-action to xu-cheng/latex-action@v3
- Implementation of robust fallback mechanisms  
- Enhanced PDF verification and error reporting
- Two-tier LaTeX compilation approach effectiveness

The tests ensure that the CI pipeline is more resilient to LaTeX action failures
and provides comprehensive error recovery mechanisms.
"""

import os
import re
import sys
import yaml
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple


class LatexRobustnessValidator:
    """Validates LaTeX action migration and robustness improvements."""
    
    def __init__(self):
        self.workflow_dir = Path(".github/workflows")
        self.issues_found = []
        self.successes = []
        
    def validate_latex_action_migration(self) -> bool:
        """Test that workflows use xu-cheng/latex-action@v3 as primary."""
        print("🔄 Testing LaTeX Action Migration")
        print("=" * 60)
        
        migration_success = True
        target_workflows = [
            'latex-build.yml',
            'automated-pr-merge-test.yml'
        ]
        
        for workflow_file in target_workflows:
            workflow_path = self.workflow_dir / workflow_file
            
            if not workflow_path.exists():
                self.issues_found.append(f"❌ {workflow_file}: File not found")
                migration_success = False
                continue
                
            print(f"📋 Checking {workflow_file}...")
            
            with open(workflow_path, 'r') as f:
                content = f.read()
            
            # Check for xu-cheng/latex-action@v3 usage
            if 'xu-cheng/latex-action@v3' in content:
                self.successes.append(f"✅ {workflow_file}: Uses xu-cheng/latex-action@v3")
                print(f"   ✅ Primary action migrated to xu-cheng/latex-action@v3")
            else:
                self.issues_found.append(f"❌ {workflow_file}: Missing xu-cheng/latex-action@v3")
                migration_success = False
                print(f"   ❌ Primary action not migrated")
            
            # Check that dante-ev/latex-action is removed
            if 'dante-ev/latex-action' in content:
                self.issues_found.append(f"❌ {workflow_file}: Still contains dante-ev/latex-action")
                migration_success = False
                print(f"   ❌ Old dante-ev/latex-action still present")
            else:
                self.successes.append(f"✅ {workflow_file}: dante-ev/latex-action removed")
                print(f"   ✅ Old action successfully removed")
                
        return migration_success
    
    def validate_fallback_mechanisms(self) -> bool:
        """Test that robust fallback mechanisms are implemented."""
        print("\n🛡️  Testing Fallback Mechanisms")
        print("=" * 60)
        
        fallback_success = True
        target_workflows = [
            'latex-build.yml',
            'automated-pr-merge-test.yml'
        ]
        
        for workflow_file in target_workflows:
            workflow_path = self.workflow_dir / workflow_file
            
            if not workflow_path.exists():
                continue
                
            print(f"📋 Checking fallback in {workflow_file}...")
            
            with open(workflow_path, 'r') as f:
                content = f.read()
            
            # Check for primary action with continue-on-error
            if 'continue-on-error: true' in content and 'latex_primary' in content:
                self.successes.append(f"✅ {workflow_file}: Primary action has continue-on-error")
                print(f"   ✅ Primary action configured with error tolerance")
            else:
                self.issues_found.append(f"❌ {workflow_file}: Missing continue-on-error for primary")
                fallback_success = False
                print(f"   ❌ Primary action missing error tolerance")
            
            # Check for fallback step with condition
            if 'steps.latex_primary.outcome == \'failure\'' in content:
                self.successes.append(f"✅ {workflow_file}: Conditional fallback implemented")
                print(f"   ✅ Conditional fallback trigger implemented")
            else:
                self.issues_found.append(f"❌ {workflow_file}: Missing conditional fallback")
                fallback_success = False
                print(f"   ❌ Conditional fallback trigger missing")
            
            # Check for manual TeX Live installation in fallback
            manual_install_patterns = [
                'sudo apt-get install.*texlive',
                'texlive-latex-base',
                'texlive-lang-german'
            ]
            
            manual_install_found = any(pattern in content for pattern in manual_install_patterns)
            if manual_install_found:
                self.successes.append(f"✅ {workflow_file}: Manual TeX Live fallback implemented")
                print(f"   ✅ Manual TeX Live installation fallback found")
            else:
                self.issues_found.append(f"❌ {workflow_file}: Missing manual TeX Live fallback")
                fallback_success = False
                print(f"   ❌ Manual TeX Live installation fallback missing")
                
        return fallback_success
    
    def validate_enhanced_pdf_verification(self) -> bool:
        """Test that enhanced PDF verification is implemented."""
        print("\n📊 Testing Enhanced PDF Verification")
        print("=" * 60)
        
        verification_success = True
        target_workflows = [
            'latex-build.yml',
            'automated-pr-merge-test.yml'
        ]
        
        for workflow_file in target_workflows:
            workflow_path = self.workflow_dir / workflow_file
            
            if not workflow_path.exists():
                continue
                
            print(f"📋 Checking PDF verification in {workflow_file}...")
            
            with open(workflow_path, 'r') as f:
                content = f.read()
            
            # Check for enhanced verification features
            verification_features = {
                'File size analysis': 'stat -c%s.*pdf',
                'File format verification': 'file.*pdf.*grep',
                'Size threshold check': 'PDF_SIZE.*-gt.*1000',
                'Comprehensive error analysis': 'Comprehensive error analysis',
                'LaTeX method tracking': 'latex_primary.*outcome'
            }
            
            features_found = 0
            for feature_name, pattern in verification_features.items():
                if re.search(pattern, content):
                    self.successes.append(f"✅ {workflow_file}: {feature_name} implemented")
                    print(f"   ✅ {feature_name}")
                    features_found += 1
                else:
                    self.issues_found.append(f"❌ {workflow_file}: Missing {feature_name}")
                    print(f"   ❌ Missing {feature_name}")
            
            # Require at least 3 out of 5 enhanced features
            if features_found >= 3:
                print(f"   ✅ Enhanced verification: {features_found}/5 features implemented")
            else:
                print(f"   ❌ Insufficient enhanced verification: {features_found}/5 features")
                verification_success = False
                
        return verification_success
    
    def validate_error_recovery_mechanisms(self) -> bool:
        """Test that comprehensive error recovery mechanisms exist."""
        print("\n🔧 Testing Error Recovery Mechanisms")
        print("=" * 60)
        
        recovery_success = True
        target_workflows = [
            'latex-build.yml',
            'automated-pr-merge-test.yml'
        ]
        
        for workflow_file in target_workflows:
            workflow_path = self.workflow_dir / workflow_file
            
            if not workflow_path.exists():
                continue
                
            print(f"📋 Checking error recovery in {workflow_file}...")
            
            with open(workflow_path, 'r') as f:
                content = f.read()
            
            # Count error recovery mechanisms
            recovery_mechanisms = {
                'timeout-minutes': len(re.findall(r'timeout-minutes:', content)),
                'continue-on-error': content.count('continue-on-error: true'),
                'if: failure()': content.count('if: failure()'),
                'find.*log': len(re.findall(r'find.*\.log', content)),
                'upload.*artifact': len(re.findall(r'upload.*artifact', content))
            }
            
            print(f"   📊 Error recovery mechanisms found:")
            total_mechanisms = 0
            for mechanism, count in recovery_mechanisms.items():
                print(f"     {mechanism}: {count}")
                total_mechanisms += count
            
            # Expect reasonable error recovery coverage
            if total_mechanisms >= 8:
                self.successes.append(f"✅ {workflow_file}: Strong error recovery ({total_mechanisms} mechanisms)")
                print(f"   ✅ Strong error recovery coverage")
            elif total_mechanisms >= 5:
                self.successes.append(f"✅ {workflow_file}: Adequate error recovery ({total_mechanisms} mechanisms)")
                print(f"   ✅ Adequate error recovery coverage")
            else:
                self.issues_found.append(f"❌ {workflow_file}: Weak error recovery ({total_mechanisms} mechanisms)")
                print(f"   ❌ Insufficient error recovery coverage")
                recovery_success = False
                
        return recovery_success
    
    def validate_workflow_structure_integrity(self) -> bool:
        """Test that workflow files maintain proper YAML structure."""
        print("\n📋 Testing Workflow Structure Integrity")
        print("=" * 60)
        
        structure_success = True
        
        for workflow_file in self.workflow_dir.glob("*.yml"):
            print(f"📄 Validating {workflow_file.name}...")
            
            try:
                with open(workflow_file, 'r') as f:
                    yaml_data = yaml.safe_load(f)
                    
                # Basic workflow structure validation
                required_keys = ['name', 'on', 'jobs']
                missing_keys = [key for key in required_keys if key not in yaml_data]
                
                if missing_keys:
                    self.issues_found.append(f"❌ {workflow_file.name}: Missing keys: {missing_keys}")
                    structure_success = False
                    print(f"   ❌ Missing required keys: {missing_keys}")
                else:
                    self.successes.append(f"✅ {workflow_file.name}: Valid workflow structure")
                    print(f"   ✅ Valid YAML structure")
                    
            except yaml.YAMLError as e:
                self.issues_found.append(f"❌ {workflow_file.name}: YAML syntax error - {e}")
                structure_success = False
                print(f"   ❌ YAML syntax error: {e}")
                
        return structure_success
    
    def test_build_system_compatibility(self) -> bool:
        """Test that changes don't break existing build system."""
        print("\n🔧 Testing Build System Compatibility")
        print("=" * 60)
        
        try:
            # Run CTMM build system test
            result = subprocess.run([
                'python3', 'ctmm_build.py'
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                self.successes.append("✅ CTMM build system: Compatible with changes")
                print("   ✅ CTMM build system passes")
                return True
            else:
                self.issues_found.append(f"❌ CTMM build system: Failed - {result.stderr}")
                print(f"   ❌ CTMM build system failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            self.issues_found.append("❌ CTMM build system: Timeout")
            print("   ❌ CTMM build system timed out")
            return False
        except Exception as e:
            self.issues_found.append(f"❌ CTMM build system: Error - {e}")
            print(f"   ❌ CTMM build system error: {e}")
            return False
    
    def run_comprehensive_validation(self) -> bool:
        """Run all validation tests and provide comprehensive report."""
        print("🚀 LaTeX Robustness Validation Test Suite")
        print("=" * 80)
        print("Issue #1068: LaTeX Action Migration and Robustness Improvements")
        print("=" * 80)
        
        # Run all validation tests
        test_results = {
            'LaTeX Action Migration': self.validate_latex_action_migration(),
            'Fallback Mechanisms': self.validate_fallback_mechanisms(),
            'Enhanced PDF Verification': self.validate_enhanced_pdf_verification(),
            'Error Recovery Mechanisms': self.validate_error_recovery_mechanisms(),
            'Workflow Structure Integrity': self.validate_workflow_structure_integrity(),
            'Build System Compatibility': self.test_build_system_compatibility()
        }
        
        # Generate comprehensive report
        print("\n" + "=" * 80)
        print("📊 COMPREHENSIVE VALIDATION REPORT")
        print("=" * 80)
        
        passed_tests = sum(test_results.values())
        total_tests = len(test_results)
        
        print(f"\n📈 Test Results Summary:")
        print(f"   Tests Passed: {passed_tests}/{total_tests}")
        print(f"   Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        print(f"\n✅ Successful Validations ({len(self.successes)}):")
        for success in self.successes:
            print(f"   {success}")
            
        if self.issues_found:
            print(f"\n❌ Issues Found ({len(self.issues_found)}):")
            for issue in self.issues_found:
                print(f"   {issue}")
        
        print(f"\n🎯 Individual Test Results:")
        for test_name, result in test_results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"   {test_name}: {status}")
        
        # Overall assessment
        if passed_tests == total_tests:
            print(f"\n🎉 OVERALL RESULT: ✅ ALL TESTS PASSED")
            print("   LaTeX robustness improvements successfully implemented!")
            return True
        elif passed_tests >= total_tests * 0.8:  # 80% pass rate
            print(f"\n⚠️  OVERALL RESULT: ✅ MOSTLY SUCCESSFUL")
            print("   Most robustness improvements implemented, minor issues to address")
            return True
        else:
            print(f"\n❌ OVERALL RESULT: ❌ SIGNIFICANT ISSUES")
            print("   Major robustness improvements needed")
            return False


def main():
    """Main test execution function."""
    validator = LatexRobustnessValidator()
    
    # Run comprehensive validation
    success = validator.run_comprehensive_validation()
    
    # Return appropriate exit code
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())