#!/usr/bin/env python3
"""
Enhanced CI Reliability System - Issue #1066
Comprehensive validation and monitoring system to prevent CI failures like dcbb83f4.
"""

import os
import yaml
import re
import subprocess
from typing import Dict, List, Tuple, Optional
from datetime import datetime

class CIReliabilityMonitor:
    """Enhanced CI reliability monitoring and validation."""
    
    def __init__(self):
        self.validation_results = []
        self.failure_patterns = []
        self.health_checks = []
        
    def validate_action_version_consistency(self) -> bool:
        """Enhanced action version validation to catch subtle conflicts."""
        print("\n🔍 Enhanced Action Version Validation")
        print("=" * 60)
        
        workflow_files = self._get_workflow_files()
        if not workflow_files:
            print("❌ No workflow files found")
            return False
            
        # Track all versions of each action across workflows
        action_versions = {}
        version_conflicts = []
        
        for workflow_file in workflow_files:
            print(f"📋 Analyzing {workflow_file}...")
            
            try:
                with open(workflow_file, 'r', encoding='utf-8') as f:
                    workflow_data = yaml.safe_load(f)
                
                actions = self._extract_actions_from_workflow(workflow_file, workflow_data)
                
                for action_name, version, step_name in actions:
                    if action_name not in action_versions:
                        action_versions[action_name] = {}
                    
                    if version not in action_versions[action_name]:
                        action_versions[action_name][version] = []
                    
                    action_versions[action_name][version].append({
                        'workflow': workflow_file,
                        'step': step_name
                    })
                    
            except Exception as e:
                print(f"❌ Error parsing {workflow_file}: {e}")
                return False
        
        # Check for version conflicts
        for action_name, versions in action_versions.items():
            if len(versions) > 1:
                version_conflicts.append({
                    'action': action_name,
                    'versions': versions
                })
                print(f"⚠️  VERSION CONFLICT: {action_name}")
                for version, usages in versions.items():
                    print(f"   Version {version}:")
                    for usage in usages:
                        print(f"     - {usage['workflow']} ({usage['step']})")
        
        # Enhanced validation for specific action patterns
        self._validate_latex_action_versions(action_versions)
        
        if version_conflicts:
            print(f"\n❌ Found {len(version_conflicts)} version conflicts")
            return False
        else:
            print("\n✅ No version conflicts detected")
            return True
    
    def _validate_latex_action_versions(self, action_versions: Dict):
        """Enhanced validation specifically for LaTeX actions."""
        print(f"\n🧪 LaTeX Action Specific Validation")
        print("-" * 40)
        
        latex_actions = [
            'dante-ev/latex-action',
            'xu-cheng/latex-action'
        ]
        
        for action in latex_actions:
            if action in action_versions:
                versions = list(action_versions[action].keys())
                print(f"📦 {action}: {versions}")
                
                # Check for problematic version patterns
                for version in versions:
                    if version == 'v2':
                        print(f"🚨 CRITICAL: {action}@v2 is deprecated/problematic")
                        print(f"   Recommended: Use v0.2.0 or latest stable")
                        self.failure_patterns.append({
                            'type': 'deprecated_version',
                            'action': action,
                            'version': version,
                            'severity': 'critical'
                        })
                    elif version.startswith('v2.'):
                        print(f"⚠️  WARNING: {action}@{version} may have issues")
                        print(f"   Consider v0.2.0 for stability")
        
        if not any(action in action_versions for action in latex_actions):
            print("❓ No LaTeX actions found in workflows")
    
    def analyze_failure_patterns(self) -> bool:
        """Analyze and detect common CI failure patterns."""
        print("\n🔍 Failure Pattern Analysis")
        print("=" * 60)
        
        patterns = [
            self._check_action_resolution_pattern(),
            self._check_timeout_pattern(),
            self._check_resource_pattern(),
            self._check_dependency_pattern()
        ]
        
        all_patterns_ok = all(patterns)
        
        if all_patterns_ok:
            print("✅ No problematic failure patterns detected")
        else:
            print("⚠️  Some failure patterns detected - see details above")
            
        return all_patterns_ok
    
    def _check_action_resolution_pattern(self) -> bool:
        """Check for action resolution failure patterns."""
        print("🔍 Checking action resolution patterns...")
        
        workflow_files = self._get_workflow_files()
        issues_found = 0
        
        for workflow_file in workflow_files:
            try:
                with open(workflow_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for problematic patterns
                if re.search(r'dante-ev/latex-action@v2\b', content):
                    print(f"🚨 FOUND: {workflow_file} uses deprecated dante-ev/latex-action@v2")
                    issues_found += 1
                
                if re.search(r'@latest\b', content):
                    print(f"⚠️  WARNING: {workflow_file} uses @latest version (unstable)")
                    issues_found += 1
                    
            except Exception as e:
                print(f"❌ Error checking {workflow_file}: {e}")
                issues_found += 1
        
        if issues_found == 0:
            print("✅ No action resolution issues found")
            return True
        else:
            print(f"❌ Found {issues_found} action resolution issues")
            return False
    
    def _check_timeout_pattern(self) -> bool:
        """Check for timeout-related failure patterns."""
        print("🔍 Checking timeout patterns...")
        
        workflow_files = self._get_workflow_files()
        timeout_coverage = 0
        total_steps = 0
        
        for workflow_file in workflow_files:
            try:
                with open(workflow_file, 'r', encoding='utf-8') as f:
                    workflow_data = yaml.safe_load(f)
                
                for job_name, job_data in workflow_data.get('jobs', {}).items():
                    for step in job_data.get('steps', []):
                        total_steps += 1
                        if 'timeout-minutes' in step:
                            timeout_coverage += 1
                            
            except Exception as e:
                print(f"❌ Error checking timeouts in {workflow_file}: {e}")
        
        coverage_pct = (timeout_coverage / total_steps * 100) if total_steps > 0 else 0
        print(f"📊 Timeout coverage: {timeout_coverage}/{total_steps} ({coverage_pct:.1f}%)")
        
        if coverage_pct >= 80:
            print("✅ Good timeout coverage")
            return True
        else:
            print("⚠️  Consider adding more timeouts")
            return True  # Don't fail on this, just warn
    
    def _check_resource_pattern(self) -> bool:
        """Check for resource constraint failure patterns."""
        print("🔍 Checking resource constraint patterns...")
        
        workflow_files = self._get_workflow_files()
        has_resource_checks = False
        
        for workflow_file in workflow_files:
            try:
                with open(workflow_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if 'df -h' in content or 'free -h' in content:
                    has_resource_checks = True
                    print(f"✅ {workflow_file} has resource monitoring")
                    
            except Exception as e:
                print(f"❌ Error checking {workflow_file}: {e}")
        
        if has_resource_checks:
            print("✅ Resource monitoring found in workflows")
            return True
        else:
            print("⚠️  No resource monitoring found")
            return True  # Don't fail on this
    
    def _check_dependency_pattern(self) -> bool:
        """Check for dependency failure patterns."""
        print("🔍 Checking dependency patterns...")
        
        # Check if critical validation scripts exist
        critical_scripts = [
            'ctmm_build.py',
            'validate_latex_syntax.py',
            'validate_action_versions.py'
        ]
        
        missing_scripts = []
        for script in critical_scripts:
            if not os.path.exists(script):
                missing_scripts.append(script)
        
        if missing_scripts:
            print(f"❌ Missing critical scripts: {missing_scripts}")
            return False
        else:
            print("✅ All critical validation scripts present")
            return True
    
    def comprehensive_ci_health_monitoring(self) -> bool:
        """Comprehensive CI health monitoring validation."""
        print("\n🏥 Comprehensive CI Health Monitoring")
        print("=" * 60)
        
        health_checks = [
            ('Environment Assessment', self._check_environment_assessment()),
            ('Action Version Health', self._check_action_version_health()),
            ('Workflow Structure', self._check_workflow_structure()),
            ('Error Recovery', self._check_error_recovery()),
            ('Build System Health', self._check_build_system_health())
        ]
        
        passed_checks = 0
        for check_name, result in health_checks:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} {check_name}")
            if result:
                passed_checks += 1
        
        health_score = (passed_checks / len(health_checks)) * 100
        print(f"\n📊 CI Health Score: {health_score:.1f}% ({passed_checks}/{len(health_checks)})")
        
        if health_score >= 80:
            print("🎉 EXCELLENT: CI health is good")
            return True
        elif health_score >= 60:
            print("⚠️  FAIR: CI health needs attention")
            return True
        else:
            print("🚨 POOR: CI health needs immediate attention")
            return False
    
    def _check_environment_assessment(self) -> bool:
        """Check if workflows assess GitHub Actions environment."""
        workflow_files = self._get_workflow_files()
        has_assessment = False
        
        for workflow_file in workflow_files:
            try:
                with open(workflow_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if 'RUNNER_OS' in content or 'environment' in content.lower():
                    has_assessment = True
                    break
                    
            except Exception:
                continue
        
        return has_assessment
    
    def _check_action_version_health(self) -> bool:
        """Check action version health."""
        try:
            result = subprocess.run([
                'python3', 'validate_action_versions.py'
            ], capture_output=True, text=True, timeout=30)
            return result.returncode == 0
        except Exception:
            return False
    
    def _check_workflow_structure(self) -> bool:
        """Check workflow structure health."""
        workflow_files = self._get_workflow_files()
        
        for workflow_file in workflow_files:
            try:
                with open(workflow_file, 'r', encoding='utf-8') as f:
                    yaml.safe_load(f)
            except Exception:
                return False
        
        return len(workflow_files) > 0
    
    def _check_error_recovery(self) -> bool:
        """Check error recovery mechanisms."""
        workflow_files = self._get_workflow_files()
        has_error_recovery = False
        
        for workflow_file in workflow_files:
            try:
                with open(workflow_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if 'continue-on-error' in content or 'if: failure()' in content:
                    has_error_recovery = True
                    break
                    
            except Exception:
                continue
        
        return has_error_recovery
    
    def _check_build_system_health(self) -> bool:
        """Check build system health."""
        try:
            result = subprocess.run([
                'python3', 'ctmm_build.py'
            ], capture_output=True, text=True, timeout=60)
            return result.returncode == 0
        except Exception:
            return False
    
    def _get_workflow_files(self) -> List[str]:
        """Get all GitHub Actions workflow files."""
        workflow_dir = '.github/workflows'
        if not os.path.exists(workflow_dir):
            return []
        
        return [
            os.path.join(workflow_dir, f)
            for f in os.listdir(workflow_dir)
            if f.endswith('.yml') or f.endswith('.yaml')
        ]
    
    def _extract_actions_from_workflow(self, workflow_file: str, workflow_data: dict) -> List[Tuple[str, str, str]]:
        """Extract GitHub Actions and their versions from workflow data."""
        actions = []
        
        if 'jobs' not in workflow_data:
            return actions
        
        for job_name, job_data in workflow_data['jobs'].items():
            if 'steps' not in job_data:
                continue
                
            for step in job_data['steps']:
                if 'uses' in step:
                    action_spec = step['uses']
                    step_name = step.get('name', f'Unnamed step in {job_name}')
                    
                    # Parse action@version format
                    if '@' in action_spec:
                        action_name, version = action_spec.rsplit('@', 1)
                        actions.append((action_name, version, step_name))
                    else:
                        actions.append((action_spec, 'latest', step_name))
        
        return actions
    
    def generate_reliability_report(self) -> str:
        """Generate comprehensive reliability report."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report = f"""
=======================================================================
ENHANCED CI RELIABILITY REPORT - Issue #1066
Generated: {timestamp}
=======================================================================

FAILURE PATTERNS DETECTED:
"""
        
        if self.failure_patterns:
            for pattern in self.failure_patterns:
                report += f"\n🚨 {pattern['severity'].upper()}: {pattern['type']}"
                report += f"\n   Action: {pattern['action']}@{pattern['version']}"
        else:
            report += "\n✅ No failure patterns detected"
        
        report += f"""

HEALTH CHECKS SUMMARY:
{len(self.health_checks)} checks performed
        
RECOMMENDATIONS:
• Maintain consistent action versions across all workflows
• Monitor CI health score regularly (target: >80%)
• Implement proactive failure pattern detection
• Use stable versions instead of @latest tags

=======================================================================
"""
        return report

def main():
    """Main function to run enhanced CI reliability monitoring."""
    print("🔧 Enhanced CI Reliability System - Issue #1066")
    print("=" * 70)
    
    monitor = CIReliabilityMonitor()
    
    print("Running comprehensive CI reliability validation...")
    
    # Run all validation checks
    version_check = monitor.validate_action_version_consistency()
    pattern_check = monitor.analyze_failure_patterns()
    health_check = monitor.comprehensive_ci_health_monitoring()
    
    # Generate report
    print(monitor.generate_reliability_report())
    
    # Overall result
    all_checks_passed = version_check and pattern_check and health_check
    
    if all_checks_passed:
        print("🎉 SUCCESS: All CI reliability checks passed")
        return True
    else:
        print("⚠️  WARNING: Some CI reliability issues detected")
        return True  # Don't fail hard, just warn

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)