#!/usr/bin/env python3
"""
CI Failure Prevention and Pattern Analysis
Addresses Issue #1084: CI Insights Report Build Failures

This script analyzes common CI failure patterns and implements 
proactive measures to prevent intermittent build failures.
"""

import os
import re
import yaml
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple


class CIFailureAnalyzer:
    """Analyzes and prevents common CI failure patterns."""
    
    def __init__(self):
        self.failure_patterns = {
            'timeout_issues': [
                'timeout',
                'timed out',
                'killed by signal 15',
                'process killed'
            ],
            'resource_constraints': [
                'no space left on device',
                'cannot allocate memory',
                'disk quota exceeded',
                'out of memory'
            ],
            'network_issues': [
                'connection refused',
                'name resolution failed',
                'network unreachable',
                'timeout on read'
            ],
            'action_version_issues': [
                'deprecated action',
                'action not found',
                'invalid action version',
                'unsupported runner'
            ],
            'latex_specific': [
                'pdflatex: command not found',
                'package not found',
                'file not found',
                '! LaTeX Error'
            ]
        }
        
    def analyze_workflow_timeouts(self) -> List[str]:
        """Analyze workflow timeout configurations."""
        print("🕐 Analyzing workflow timeout configurations...")
        
        issues = []
        workflow_dir = Path('.github/workflows')
        
        if not workflow_dir.exists():
            issues.append("No .github/workflows directory found")
            return issues
            
        for workflow_file in workflow_dir.glob('*.yml'):
            print(f"   📄 Checking {workflow_file.name}...")
            
            try:
                with open(workflow_file, 'r') as f:
                    content = f.read()
                    
                # Check for timeout configurations
                if 'timeout-minutes:' not in content:
                    issues.append(f"{workflow_file.name}: No timeout configuration found")
                else:
                    # Parse timeout values
                    timeout_matches = re.findall(r'timeout-minutes:\s*(\d+)', content)
                    for timeout in timeout_matches:
                        if int(timeout) > 20:  # Flag very long timeouts
                            print(f"   ⚠️  Long timeout found: {timeout} minutes")
                        elif int(timeout) < 3:  # Flag very short timeouts
                            print(f"   ⚠️  Short timeout found: {timeout} minutes")
                        else:
                            print(f"   ✅ Reasonable timeout: {timeout} minutes")
                            
            except Exception as e:
                issues.append(f"{workflow_file.name}: Error reading file - {e}")
                
        return issues
    
    def check_action_versions(self) -> List[str]:
        """Check for problematic action versions."""
        print("📦 Checking GitHub Actions versions...")
        
        issues = []
        workflow_dir = Path('.github/workflows')
        
        # Known problematic patterns
        problematic_versions = {
            'dante-ev/latex-action': ['latest', 'master'],  # Should use specific versions
            'actions/setup-python': ['v1', 'v2'],  # Deprecated versions
            'actions/checkout': ['v1', 'v2'],  # Deprecated versions
        }
        
        for workflow_file in workflow_dir.glob('*.yml'):
            print(f"   📄 Checking {workflow_file.name}...")
            
            try:
                with open(workflow_file, 'r') as f:
                    content = f.read()
                    
                # Find action usages
                action_pattern = r'uses:\s*([^@\s]+)@([^\s]+)'
                matches = re.findall(action_pattern, content)
                
                for action, version in matches:
                    if action in problematic_versions:
                        if version in problematic_versions[action]:
                            issues.append(f"{workflow_file.name}: {action}@{version} is problematic")
                        else:
                            print(f"   ✅ {action}@{version} looks good")
                            
            except Exception as e:
                issues.append(f"{workflow_file.name}: Error checking actions - {e}")
                
        return issues
    
    def analyze_resource_usage_patterns(self) -> List[str]:
        """Analyze potential resource usage issues."""
        print("💾 Analyzing resource usage patterns...")
        
        issues = []
        
        # Check for large files that might cause issues
        large_files = []
        for file_path in Path('.').rglob('*'):
            if file_path.is_file():
                try:
                    size = file_path.stat().st_size
                    if size > 10 * 1024 * 1024:  # 10MB
                        large_files.append((str(file_path), size))
                except (OSError, PermissionError):
                    pass
        
        if large_files:
            print("   📊 Large files found:")
            for file_path, size in large_files:
                print(f"     • {file_path}: {size / (1024*1024):.1f}MB")
                if size > 50 * 1024 * 1024:  # 50MB
                    issues.append(f"Very large file may cause CI issues: {file_path}")
        else:
            print("   ✅ No large files detected")
            
        return issues
    
    def check_latex_dependencies(self) -> List[str]:
        """Check LaTeX-specific dependency issues."""
        print("📝 Checking LaTeX dependencies...")
        
        issues = []
        
        # Check workflow files for LaTeX packages
        workflow_dir = Path('.github/workflows')
        for workflow_file in workflow_dir.glob('*.yml'):
            if 'latex' in workflow_file.name.lower():
                print(f"   📄 Checking LaTeX config in {workflow_file.name}...")
                
                try:
                    with open(workflow_file, 'r') as f:
                        content = f.read()
                        
                    # Check for essential packages
                    essential_packages = [
                        'texlive-lang-german',
                        'texlive-latex-recommended',
                        'texlive-fonts-recommended'
                    ]
                    
                    for package in essential_packages:
                        if package in content:
                            print(f"   ✅ Found essential package: {package}")
                        else:
                            issues.append(f"Missing essential LaTeX package: {package}")
                            
                except Exception as e:
                    issues.append(f"Error checking LaTeX config: {e}")
                    
        return issues
    
    def generate_prevention_recommendations(self, all_issues: List[str]) -> Dict[str, List[str]]:
        """Generate recommendations based on identified issues."""
        print("\n💡 Generating prevention recommendations...")
        
        recommendations = {
            'immediate_fixes': [],
            'monitoring_improvements': [],
            'best_practices': []
        }
        
        if any('timeout' in issue.lower() for issue in all_issues):
            recommendations['immediate_fixes'].append(
                "Add or adjust timeout-minutes for long-running steps"
            )
            
        if any('version' in issue.lower() for issue in all_issues):
            recommendations['immediate_fixes'].append(
                "Update deprecated GitHub Actions to recommended versions"
            )
            
        if any('package' in issue.lower() for issue in all_issues):
            recommendations['immediate_fixes'].append(
                "Add missing LaTeX packages to workflow dependencies"
            )
            
        # Always recommend monitoring improvements
        recommendations['monitoring_improvements'].extend([
            "Add system resource checks before heavy operations",
            "Implement progress indicators for long-running steps",
            "Add artifact upload for debugging failed builds"
        ])
        
        # Best practices
        recommendations['best_practices'].extend([
            "Use specific action versions instead of 'latest'",
            "Implement gradual timeout escalation",
            "Add continue-on-error for non-critical validation steps",
            "Include environment assessment before resource-intensive operations"
        ])
        
        return recommendations
    
    def run_proactive_checks(self) -> Dict[str, any]:
        """Run all proactive CI failure checks."""
        print("🔍 Running proactive CI failure checks...")
        print("=" * 60)
        
        all_issues = []
        
        # Run all checks
        all_issues.extend(self.analyze_workflow_timeouts())
        all_issues.extend(self.check_action_versions())
        all_issues.extend(self.analyze_resource_usage_patterns())
        all_issues.extend(self.check_latex_dependencies())
        
        # Generate recommendations
        recommendations = self.generate_prevention_recommendations(all_issues)
        
        # Summary
        results = {
            'total_issues': len(all_issues),
            'issues': all_issues,
            'recommendations': recommendations,
            'status': 'healthy' if len(all_issues) == 0 else 'needs_attention'
        }
        
        return results


def main():
    """Main analysis function."""
    print("=" * 70)
    print("🛡️  CI FAILURE PREVENTION ANALYSIS")
    print("Issue #1084: CI Insights Report Build Failures")
    print("=" * 70)
    
    analyzer = CIFailureAnalyzer()
    results = analyzer.run_proactive_checks()
    
    print("\n" + "=" * 60)
    print("📊 ANALYSIS SUMMARY")
    print("=" * 60)
    
    print(f"🔍 Issues identified: {results['total_issues']}")
    print(f"🎯 Status: {results['status'].upper()}")
    
    if results['issues']:
        print("\n❌ Issues found:")
        for i, issue in enumerate(results['issues'], 1):
            print(f"   {i}. {issue}")
    else:
        print("\n✅ No major issues detected!")
    
    print(f"\n💡 Recommendations:")
    for category, items in results['recommendations'].items():
        if items:
            print(f"\n   {category.replace('_', ' ').title()}:")
            for item in items:
                print(f"   • {item}")
    
    print(f"\n🎯 Prevention Strategy:")
    print("   1. Implement enhanced monitoring and diagnostics")
    print("   2. Add proactive environment validation")
    print("   3. Improve error handling and recovery")
    print("   4. Regular maintenance of action versions")
    
    return results['status'] == 'healthy'


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)