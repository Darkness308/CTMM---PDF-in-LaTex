#!/usr/bin/env python3
"""
Enhanced CI Environment Validation and Diagnostics
Addresses Issue #1084: CI Insights Report Build Failures

This script provides comprehensive GitHub Actions environment validation,
resource monitoring, and proactive failure detection for the CTMM system.
"""

import os
import sys
import subprocess
import time
import platform
from pathlib import Path


def run_command(command, description, timeout=30):
    """Run a command with timeout and capture output."""
    print(f"🔍 {description}...")
    try:
        result = subprocess.run(
            command.split(), 
            capture_output=True, 
            text=True, 
            timeout=timeout
        )
        if result.returncode == 0:
            print(f"✅ {description}: SUCCESS")
            return True, result.stdout.strip()
        else:
            print(f"❌ {description}: FAILED")
            print(f"   Error: {result.stderr.strip()}")
            return False, result.stderr.strip()
    except subprocess.TimeoutExpired:
        print(f"⏰ {description}: TIMEOUT after {timeout}s")
        return False, f"Timeout after {timeout}s"
    except Exception as e:
        print(f"💥 {description}: EXCEPTION - {e}")
        return False, str(e)


def check_system_resources():
    """Check system resources and constraints."""
    print("\n" + "="*60)
    print("🔧 SYSTEM RESOURCES ANALYSIS")
    print("="*60)
    
    # Disk space check
    success, output = run_command("df -h", "Checking disk space")
    if success:
        lines = output.split('\n')
        for line in lines[1:]:  # Skip header
            if '/' in line and line.strip():
                parts = line.split()
                if len(parts) >= 5:
                    usage = parts[4].replace('%', '')
                    if usage.isdigit() and int(usage) > 90:
                        print(f"⚠️  WARNING: High disk usage: {usage}%")
                    else:
                        print(f"✅ Disk usage OK: {usage}%")
    
    # Memory check
    success, output = run_command("free -h", "Checking memory")
    if success and output:
        print(f"📊 Memory info: {output.split()[1] if output.split() else 'N/A'}")
    
    # CPU info
    success, output = run_command("nproc", "Checking CPU cores")
    if success:
        print(f"🖥️  CPU cores: {output}")
    
    return True


def check_github_actions_environment():
    """Check GitHub Actions specific environment."""
    print("\n" + "="*60)
    print("🏗️  GITHUB ACTIONS ENVIRONMENT")
    print("="*60)
    
    # Environment variables
    env_vars = [
        'GITHUB_ACTIONS', 'RUNNER_OS', 'RUNNER_ARCH', 'RUNNER_NAME',
        'GITHUB_WORKFLOW', 'GITHUB_EVENT_NAME', 'GITHUB_REF'
    ]
    
    is_github_actions = False
    for var in env_vars:
        value = os.environ.get(var, 'Not set')
        print(f"📋 {var}: {value}")
        if var == 'GITHUB_ACTIONS' and value == 'true':
            is_github_actions = True
    
    if is_github_actions:
        print("✅ Running in GitHub Actions environment")
    else:
        print("ℹ️  Running in local development environment")
    
    return is_github_actions


def check_package_dependencies():
    """Check critical package dependencies."""
    print("\n" + "="*60)
    print("📦 PACKAGE DEPENDENCIES CHECK")
    print("="*60)
    
    # Python packages
    python_packages = ['chardet']
    for package in python_packages:
        try:
            __import__(package)
            print(f"✅ Python package '{package}': AVAILABLE")
        except ImportError:
            print(f"❌ Python package '{package}': MISSING")
    
    # System commands
    system_commands = ['python3', 'git', 'pdflatex', 'latex']
    for cmd in system_commands:
        success, _ = run_command(f"which {cmd}", f"Checking {cmd}")
        
    return True


def check_workflow_files():
    """Check workflow file integrity."""
    print("\n" + "="*60)
    print("📄 WORKFLOW FILES VALIDATION")
    print("="*60)
    
    workflow_dir = Path('.github/workflows')
    if not workflow_dir.exists():
        print("❌ .github/workflows directory not found")
        return False
    
    workflow_files = [
        'latex-build.yml',
        'pr-validation.yml', 
        'latex-validation.yml'
    ]
    
    all_valid = True
    for workflow in workflow_files:
        file_path = workflow_dir / workflow
        if file_path.exists():
            print(f"✅ Found: {workflow}")
            # Basic YAML syntax check
            with open(file_path, 'r') as f:
                content = f.read()
                if '"on":' in content:
                    print(f"✅ {workflow}: Proper quoted 'on:' syntax")
                elif 'on:' in content:
                    print(f"⚠️  {workflow}: Unquoted 'on:' detected")
        else:
            print(f"❌ Missing: {workflow}")
            all_valid = False
    
    return all_valid


def check_latex_configuration():
    """Check LaTeX-specific configuration."""
    print("\n" + "="*60)
    print("📝 LATEX CONFIGURATION CHECK")
    print("="*60)
    
    # Check main.tex
    if Path('main.tex').exists():
        print("✅ main.tex found")
    else:
        print("❌ main.tex missing")
        return False
    
    # Check style files
    style_dir = Path('style')
    if style_dir.exists():
        style_files = list(style_dir.glob('*.sty'))
        print(f"✅ Style directory: {len(style_files)} files")
    else:
        print("❌ Style directory missing")
    
    # Check modules
    modules_dir = Path('modules')
    if modules_dir.exists():
        module_files = list(modules_dir.glob('*.tex'))
        print(f"✅ Modules directory: {len(module_files)} files")
    else:
        print("❌ Modules directory missing")
    
    return True


def run_diagnostic_tests():
    """Run diagnostic validation tests."""
    print("\n" + "="*60)
    print("🧪 DIAGNOSTIC TESTS")
    print("="*60)
    
    test_commands = [
        ("python3 validate_latex_syntax.py", "LaTeX syntax validation", 60),
        ("python3 ctmm_build.py", "CTMM build system", 120),
        ("python3 validate_action_versions.py", "GitHub Actions versions", 60)
    ]
    
    passed = 0
    total = len(test_commands)
    
    for cmd, desc, timeout in test_commands:
        success, _ = run_command(cmd, desc, timeout)
        if success:
            passed += 1
    
    print(f"\n📊 Diagnostic tests: {passed}/{total} passed")
    return passed == total


def generate_environment_report():
    """Generate comprehensive environment report."""
    print("\n" + "="*70)
    print("📋 CI ENVIRONMENT DIAGNOSTIC REPORT")
    print("="*70)
    
    report = {
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime()),
        'platform': platform.platform(),
        'python_version': sys.version,
        'working_directory': os.getcwd(),
        'environment': 'GitHub Actions' if os.environ.get('GITHUB_ACTIONS') == 'true' else 'Local'
    }
    
    for key, value in report.items():
        print(f"📋 {key.replace('_', ' ').title()}: {value}")
    
    return report


def main():
    """Main validation function."""
    print("="*70)
    print("🔍 ENHANCED CI ENVIRONMENT VALIDATION")
    print("Issue #1084: CI Insights Report Build Failures")
    print("="*70)
    
    results = []
    
    # Run all checks
    results.append(check_system_resources())
    results.append(check_github_actions_environment())
    results.append(check_package_dependencies())
    results.append(check_workflow_files())
    results.append(check_latex_configuration())
    results.append(run_diagnostic_tests())
    
    # Generate report
    generate_environment_report()
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    print("\n" + "="*70)
    print("📊 VALIDATION SUMMARY")
    print("="*70)
    print(f"✅ Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 ALL VALIDATION CHECKS PASSED!")
        print("✅ CI environment is ready for reliable builds")
        return True
    else:
        print("⚠️  Some validation checks failed")
        print("💡 Review the issues above to improve CI reliability")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)