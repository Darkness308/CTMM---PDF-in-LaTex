#!/usr/bin/env python3
"""
CTMM System Status Check - Comprehensive Health Validation

This module provides a complete health check for the CTMM system,
validating all components and providing detailed status reports.
Created as part of Issue #688 resolution.
"""

import os
import sys
import subprocess
from pathlib import Path
import json
from datetime import datetime

class CTMMStatusChecker:
    """Comprehensive status checker for CTMM system health."""
    
    def __init__(self):
        self.report = {
            'timestamp': datetime.now().isoformat(),
            'overall_status': 'UNKNOWN',
            'components': {},
            'metrics': {},
            'recommendations': []
        }
    
    def run_command(self, cmd, capture_output=True):
        """Run a shell command and return success status and output."""
        try:
            result = subprocess.run(
                cmd, shell=True, capture_output=capture_output, 
                text=True, timeout=60
            )
            return result.returncode == 0, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return False, "", "Command timed out"
        except Exception as e:
            return False, "", str(e)
    
    def check_file_structure(self):
        """Validate repository file structure."""
        print("🔍 Checking file structure...")
        
        required_files = [
            'main.tex', 'ctmm_build.py', 'validate_pr.py',
            'Makefile', 'README.md'
        ]
        
        required_dirs = [
            'modules', 'style', '.github', '.git'
        ]
        
        missing_files = []
        missing_dirs = []
        
        for file in required_files:
            if not Path(file).exists():
                missing_files.append(file)
        
        for dir in required_dirs:
            if not Path(dir).exists():
                missing_dirs.append(dir)
        
        status = len(missing_files) == 0 and len(missing_dirs) == 0
        
        self.report['components']['file_structure'] = {
            'status': 'PASS' if status else 'FAIL',
            'missing_files': missing_files,
            'missing_dirs': missing_dirs,
            'details': f"✅ All required files present" if status else f"❌ Missing {len(missing_files)} files, {len(missing_dirs)} directories"
        }
        
        if status:
            print("  ✅ File structure complete")
        else:
            print(f"  ❌ Missing files: {missing_files}")
            print(f"  ❌ Missing directories: {missing_dirs}")
        
        return status
    
    def check_latex_modules(self):
        """Check LaTeX modules and style files."""
        print("📄 Checking LaTeX modules...")
        
        modules_dir = Path('modules')
        style_dir = Path('style')
        
        if not modules_dir.exists() or not style_dir.exists():
            self.report['components']['latex_modules'] = {
                'status': 'FAIL',
                'details': "Required directories missing"
            }
            return False
        
        module_files = list(modules_dir.glob('*.tex'))
        style_files = list(style_dir.glob('*.sty'))
        
        # Count lines in modules
        total_lines = 0
        for module in module_files:
            try:
                with open(module, 'r', encoding='utf-8') as f:
                    total_lines += len(f.readlines())
            except:
                pass
        
        self.report['components']['latex_modules'] = {
            'status': 'PASS',
            'module_count': len(module_files),
            'style_count': len(style_files),
            'total_lines': total_lines,
            'details': f"✅ {len(module_files)} modules, {len(style_files)} styles, {total_lines} lines"
        }
        
        print(f"  ✅ {len(module_files)} modules, {len(style_files)} style files")
        print(f"  📊 {total_lines} total lines of LaTeX content")
        
        return True
    
    def check_build_system(self):
        """Test the CTMM build system."""
        print("🔧 Testing build system...")
        
        success, stdout, stderr = self.run_command("python3 ctmm_build.py")
        
        if success:
            # Parse output for metrics
            escaping_issues = "No LaTeX escaping issues found" in stdout
            build_passed = "✓ PASS" in stdout and "CTMM BUILD SYSTEM SUMMARY" in stdout
            
            self.report['components']['build_system'] = {
                'status': 'PASS' if build_passed else 'PARTIAL',
                'escaping_clean': escaping_issues,
                'details': "✅ Build system operational" if build_passed else "⚠️ Build system has warnings"
            }
            
            print("  ✅ Build system operational")
            if escaping_issues:
                print("  ✅ No LaTeX escaping issues")
            
            return True
        else:
            self.report['components']['build_system'] = {
                'status': 'FAIL',
                'error': stderr,
                'details': f"❌ Build failed: {stderr[:100]}..."
            }
            print(f"  ❌ Build failed: {stderr}")
            return False
    
    def check_validation_systems(self):
        """Test validation systems."""
        print("✅ Testing validation systems...")
        
        validators = {
            'pr_validation': 'python3 validate_pr.py --skip-build',
            'latex_validation': 'python3 latex_validator.py modules/',
        }
        
        results = {}
        all_passed = True
        
        for name, cmd in validators.items():
            success, stdout, stderr = self.run_command(cmd)
            results[name] = {
                'status': 'PASS' if success else 'FAIL',
                'command': cmd,
                'success': success
            }
            
            if success:
                print(f"  ✅ {name} working")
            else:
                print(f"  ❌ {name} failed")
                all_passed = False
        
        self.report['components']['validation_systems'] = {
            'status': 'PASS' if all_passed else 'PARTIAL',
            'validators': results,
            'details': f"✅ All validators working" if all_passed else "⚠️ Some validators have issues"
        }
        
        return all_passed
    
    def check_git_status(self):
        """Check git repository status."""
        print("🔄 Checking git status...")
        
        success, stdout, stderr = self.run_command("git status --porcelain")
        
        if success:
            uncommitted_files = len(stdout.strip().split('\n')) if stdout.strip() else 0
            
            # Get branch info
            branch_success, branch_out, _ = self.run_command("git branch --show-current")
            current_branch = branch_out.strip() if branch_success else "unknown"
            
            self.report['components']['git_status'] = {
                'status': 'PASS',
                'current_branch': current_branch,
                'uncommitted_files': uncommitted_files,
                'details': f"✅ On branch {current_branch}, {uncommitted_files} uncommitted files"
            }
            
            print(f"  ✅ On branch: {current_branch}")
            print(f"  📊 Uncommitted files: {uncommitted_files}")
            
            return True
        else:
            self.report['components']['git_status'] = {
                'status': 'FAIL',
                'error': stderr,
                'details': f"❌ Git error: {stderr}"
            }
            return False
    
    def generate_metrics(self):
        """Generate system metrics."""
        print("📊 Generating metrics...")
        
        # Count total files
        tex_files = len(list(Path('.').glob('**/*.tex')))
        py_files = len(list(Path('.').glob('**/*.py')))
        md_files = len(list(Path('.').glob('**/*.md')))
        
        # Calculate health score
        component_scores = []
        for component in self.report['components'].values():
            if component['status'] == 'PASS':
                component_scores.append(100)
            elif component['status'] == 'PARTIAL':
                component_scores.append(70)
            else:
                component_scores.append(0)
        
        health_score = sum(component_scores) / len(component_scores) if component_scores else 0
        
        self.report['metrics'] = {
            'health_score': round(health_score, 1),
            'file_counts': {
                'tex_files': tex_files,
                'python_files': py_files,
                'markdown_files': md_files
            },
            'component_count': len(self.report['components'])
        }
        
        print(f"  📈 System health score: {health_score:.1f}%")
        print(f"  📄 Files: {tex_files} LaTeX, {py_files} Python, {md_files} Markdown")
        
        return health_score
    
    def generate_recommendations(self):
        """Generate recommendations based on status."""
        recommendations = []
        
        # Check for failed components
        for name, component in self.report['components'].items():
            if component['status'] == 'FAIL':
                recommendations.append(f"Fix {name}: {component.get('details', 'Component failed')}")
            elif component['status'] == 'PARTIAL':
                recommendations.append(f"Review {name}: {component.get('details', 'Component has warnings')}")
        
        # System-wide recommendations
        if self.report['metrics']['health_score'] < 80:
            recommendations.append("System health below 80% - review failed components")
        
        if not recommendations:
            recommendations.append("System is healthy - no immediate actions required")
        
        self.report['recommendations'] = recommendations
        
        print("💡 Recommendations:")
        for rec in recommendations:
            print(f"  • {rec}")
    
    def run_comprehensive_check(self):
        """Run complete system health check."""
        print("🚀 CTMM System Status Check")
        print("=" * 50)
        
        checks = [
            self.check_file_structure,
            self.check_latex_modules,
            self.check_build_system,
            self.check_validation_systems,
            self.check_git_status
        ]
        
        all_passed = True
        for check in checks:
            try:
                result = check()
                if not result:
                    all_passed = False
            except Exception as e:
                print(f"  ❌ Check failed: {e}")
                all_passed = False
            print()
        
        health_score = self.generate_metrics()
        print()
        
        self.generate_recommendations()
        print()
        
        # Determine overall status
        if health_score >= 90:
            self.report['overall_status'] = 'EXCELLENT'
            status_icon = "🟢"
        elif health_score >= 80:
            self.report['overall_status'] = 'GOOD'
            status_icon = "🟡"
        elif health_score >= 60:
            self.report['overall_status'] = 'NEEDS_ATTENTION'
            status_icon = "🟠"
        else:
            self.report['overall_status'] = 'CRITICAL'
            status_icon = "🔴"
        
        print("=" * 50)
        print(f"{status_icon} Overall Status: {self.report['overall_status']} ({health_score:.1f}%)")
        print("=" * 50)
        
        return all_passed, self.report

def main():
    """Main function for command-line usage."""
    checker = CTMMStatusChecker()
    success, report = checker.run_comprehensive_check()
    
    # Optionally save report
    if '--save-report' in sys.argv:
        with open('ctmm_status_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        print("📄 Status report saved to ctmm_status_report.json")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())