#!/usr/bin/env python3
"""
Comprehensive CI Health Monitoring - Issue #1064
Monitors the overall health of the CI ecosystem and validates system reliability.
"""

import os
import subprocess
import time
import yaml
from typing import Dict, List, Tuple, Optional

def test_workflow_file_integrity() -> Dict[str, any]:
    """Test the integrity of all workflow files."""
    print("📋 Testing Workflow File Integrity")
    print("-" * 50)
    
    workflow_dir = '.github/workflows'
    integrity_results = {
        'total_files': 0,
        'valid_files': 0,
        'issues': []
    }
    
    if not os.path.exists(workflow_dir):
        integrity_results['issues'].append('Workflow directory not found')
        return integrity_results
    
    workflow_files = [f for f in os.listdir(workflow_dir) if f.endswith('.yml') or f.endswith('.yaml')]
    integrity_results['total_files'] = len(workflow_files)
    
    for workflow_file in workflow_files:
        workflow_path = os.path.join(workflow_dir, workflow_file)
        print(f"🔍 Checking {workflow_file}...")
        
        try:
            with open(workflow_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Basic checks
            if not content.strip():
                integrity_results['issues'].append(f'{workflow_file} is empty')
                continue
            
            # YAML syntax check
            yaml_data = yaml.safe_load(content)
            if not yaml_data:
                integrity_results['issues'].append(f'{workflow_file} has invalid YAML')
                continue
            
            # Required fields check
            required_fields = ['name', 'on', 'jobs']
            missing_fields = [field for field in required_fields if field not in yaml_data and f'"{field}"' not in yaml_data]
            
            if missing_fields:
                integrity_results['issues'].append(f'{workflow_file} missing fields: {missing_fields}')
                continue
            
            # Job validation
            jobs_key = 'jobs' if 'jobs' in yaml_data else '"jobs"'
            jobs = yaml_data.get(jobs_key, {})
            
            if not jobs:
                integrity_results['issues'].append(f'{workflow_file} has no jobs defined')
                continue
            
            # Check each job has required fields
            for job_name, job_data in jobs.items():
                if not isinstance(job_data, dict):
                    integrity_results['issues'].append(f'{workflow_file} job {job_name} is not a dict')
                    continue
                
                if 'runs-on' not in job_data:
                    integrity_results['issues'].append(f'{workflow_file} job {job_name} missing runs-on')
                    continue
            
            integrity_results['valid_files'] += 1
            print(f"   ✅ {workflow_file} is valid")
            
        except yaml.YAMLError as e:
            integrity_results['issues'].append(f'{workflow_file} YAML syntax error: {str(e)[:100]}')
            print(f"   ❌ {workflow_file} has YAML syntax error")
        except Exception as e:
            integrity_results['issues'].append(f'{workflow_file} error: {str(e)[:100]}')
            print(f"   ❌ {workflow_file} has error: {e}")
    
    print(f"\n📊 File integrity: {integrity_results['valid_files']}/{integrity_results['total_files']} valid")
    return integrity_results

def test_build_system_health() -> Dict[str, any]:
    """Test the health of the CTMM build system."""
    print("\n🔧 Testing Build System Health")
    print("-" * 50)
    
    health_results = {
        'tests_run': 0,
        'tests_passed': 0,
        'test_details': [],
        'issues': []
    }
    
    # Test 1: Basic CTMM build
    print("🏗️  Testing basic CTMM build...")
    try:
        start_time = time.time()
        result = subprocess.run(
            ['python3', 'ctmm_build.py'],
            capture_output=True,
            text=True,
            timeout=120
        )
        duration = time.time() - start_time
        
        health_results['tests_run'] += 1
        success = result.returncode == 0
        
        if success:
            health_results['tests_passed'] += 1
            print(f"   ✅ Basic build passed ({duration:.1f}s)")
        else:
            print(f"   ❌ Basic build failed ({duration:.1f}s)")
            health_results['issues'].append('Basic CTMM build failed')
        
        health_results['test_details'].append({
            'name': 'Basic CTMM Build',
            'passed': success,
            'duration': duration,
            'output': result.stdout[-200:] if result.stdout else '',
            'error': result.stderr[-200:] if result.stderr else ''
        })
        
    except subprocess.TimeoutExpired:
        print("   ⏱️  Basic build timed out")
        health_results['tests_run'] += 1
        health_results['issues'].append('Basic CTMM build timeout')
    except Exception as e:
        print(f"   ❌ Basic build error: {e}")
        health_results['tests_run'] += 1
        health_results['issues'].append(f'Basic CTMM build error: {e}')
    
    # Test 2: LaTeX syntax validation
    print("📝 Testing LaTeX syntax validation...")
    try:
        start_time = time.time()
        result = subprocess.run(
            ['python3', 'validate_latex_syntax.py'],
            capture_output=True,
            text=True,
            timeout=60
        )
        duration = time.time() - start_time
        
        health_results['tests_run'] += 1
        success = result.returncode == 0
        
        if success:
            health_results['tests_passed'] += 1
            print(f"   ✅ LaTeX validation passed ({duration:.1f}s)")
        else:
            print(f"   ❌ LaTeX validation failed ({duration:.1f}s)")
            health_results['issues'].append('LaTeX syntax validation failed')
        
        health_results['test_details'].append({
            'name': 'LaTeX Syntax Validation',
            'passed': success,
            'duration': duration
        })
        
    except Exception as e:
        print(f"   ❌ LaTeX validation error: {e}")
        health_results['tests_run'] += 1
        health_results['issues'].append(f'LaTeX validation error: {e}')
    
    # Test 3: Action version validation
    print("📦 Testing action version validation...")
    try:
        start_time = time.time()
        result = subprocess.run(
            ['python3', 'validate_action_versions.py'],
            capture_output=True,
            text=True,
            timeout=60
        )
        duration = time.time() - start_time
        
        health_results['tests_run'] += 1
        success = result.returncode == 0
        
        if success:
            health_results['tests_passed'] += 1
            print(f"   ✅ Action version validation passed ({duration:.1f}s)")
        else:
            print(f"   ❌ Action version validation failed ({duration:.1f}s)")
            health_results['issues'].append('Action version validation failed')
        
        health_results['test_details'].append({
            'name': 'Action Version Validation',
            'passed': success,
            'duration': duration
        })
        
    except Exception as e:
        print(f"   ❌ Action version validation error: {e}")
        health_results['tests_run'] += 1
        health_results['issues'].append(f'Action version validation error: {e}')
    
    return health_results

def test_dependency_health() -> Dict[str, any]:
    """Test the health of system dependencies."""
    print("\n📦 Testing Dependency Health")
    print("-" * 50)
    
    dependency_results = {
        'python_version': None,
        'required_modules': [],
        'missing_modules': [],
        'issues': []
    }
    
    # Check Python version
    try:
        import sys
        dependency_results['python_version'] = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        print(f"🐍 Python version: {dependency_results['python_version']}")
    except Exception as e:
        dependency_results['issues'].append(f'Cannot determine Python version: {e}')
    
    # Check required Python modules
    required_modules = ['yaml', 'chardet', 'subprocess', 'os', 're']
    
    for module_name in required_modules:
        try:
            __import__(module_name)
            dependency_results['required_modules'].append(module_name)
            print(f"   ✅ {module_name} available")
        except ImportError:
            dependency_results['missing_modules'].append(module_name)
            dependency_results['issues'].append(f'Missing required module: {module_name}')
            print(f"   ❌ {module_name} missing")
    
    # Check for chardet specifically (required by CTMM build system)
    try:
        import chardet
        print(f"   ✅ chardet version: {chardet.__version__}")
    except ImportError:
        dependency_results['issues'].append('chardet module missing - required for CTMM build')
        print("   ❌ chardet missing - required for CTMM build")
    except Exception as e:
        dependency_results['issues'].append(f'chardet issue: {e}')
    
    return dependency_results

def test_file_system_health() -> Dict[str, any]:
    """Test the health of the file system structure."""
    print("\n📁 Testing File System Health")
    print("-" * 50)
    
    filesystem_results = {
        'required_directories': [],
        'missing_directories': [],
        'required_files': [],
        'missing_files': [],
        'issues': []
    }
    
    # Check required directories
    required_dirs = [
        '.github/workflows',
        'modules',
        'style',
        'converted'
    ]
    
    for directory in required_dirs:
        if os.path.exists(directory) and os.path.isdir(directory):
            filesystem_results['required_directories'].append(directory)
            print(f"   ✅ {directory}/ exists")
        else:
            filesystem_results['missing_directories'].append(directory)
            filesystem_results['issues'].append(f'Missing required directory: {directory}')
            print(f"   ❌ {directory}/ missing")
    
    # Check required files
    required_files = [
        'main.tex',
        'ctmm_build.py',
        'validate_latex_syntax.py',
        'validate_workflow_syntax.py',
        'Makefile'
    ]
    
    for file_path in required_files:
        if os.path.exists(file_path) and os.path.isfile(file_path):
            filesystem_results['required_files'].append(file_path)
            print(f"   ✅ {file_path} exists")
        else:
            filesystem_results['missing_files'].append(file_path)
            filesystem_results['issues'].append(f'Missing required file: {file_path}')
            print(f"   ❌ {file_path} missing")
    
    return filesystem_results

def test_issue_1064_ci_health():
    """Main function for comprehensive CI health monitoring."""
    print("=" * 70)
    print("COMPREHENSIVE CI HEALTH MONITORING - Issue #1064")
    print("=" * 70)
    
    start_time = time.time()
    
    # Run all health tests
    test_results = {}
    test_results['workflow_integrity'] = test_workflow_file_integrity()
    test_results['build_system'] = test_build_system_health()
    test_results['dependencies'] = test_dependency_health()
    test_results['filesystem'] = test_file_system_health()
    
    total_duration = time.time() - start_time
    
    # Generate comprehensive summary
    print("\n" + "=" * 70)
    print("CI HEALTH MONITORING SUMMARY")
    print("=" * 70)
    
    total_issues = 0
    total_tests = 0
    total_passed = 0
    
    # Workflow integrity summary
    workflow_results = test_results['workflow_integrity']
    workflow_health = (workflow_results['valid_files'] / workflow_results['total_files'] * 100) if workflow_results['total_files'] > 0 else 0
    print(f"📋 Workflow Integrity: {workflow_results['valid_files']}/{workflow_results['total_files']} files valid ({workflow_health:.1f}%)")
    total_issues += len(workflow_results['issues'])
    
    # Build system summary
    build_results = test_results['build_system']
    if build_results['tests_run'] > 0:
        build_health = (build_results['tests_passed'] / build_results['tests_run'] * 100)
        print(f"🔧 Build System Health: {build_results['tests_passed']}/{build_results['tests_run']} tests passed ({build_health:.1f}%)")
        total_tests += build_results['tests_run']
        total_passed += build_results['tests_passed']
    total_issues += len(build_results['issues'])
    
    # Dependency summary
    dependency_results = test_results['dependencies']
    if dependency_results['required_modules']:
        dependency_health = (len(dependency_results['required_modules']) / (len(dependency_results['required_modules']) + len(dependency_results['missing_modules'])) * 100)
        print(f"📦 Dependency Health: {len(dependency_results['required_modules'])} modules available ({dependency_health:.1f}%)")
    total_issues += len(dependency_results['issues'])
    
    # Filesystem summary
    filesystem_results = test_results['filesystem']
    if filesystem_results['required_files'] or filesystem_results['required_directories']:
        total_required = len(filesystem_results['required_files']) + len(filesystem_results['required_directories'])
        total_found = len(filesystem_results['required_files']) + len(filesystem_results['required_directories'])
        filesystem_health = (total_found / total_required * 100) if total_required > 0 else 100
        print(f"📁 Filesystem Health: {total_found}/{total_required} required items found ({filesystem_health:.1f}%)")
    total_issues += len(filesystem_results['issues'])
    
    # Overall assessment
    print(f"\n⏱️  Total Duration: {total_duration:.1f} seconds")
    print(f"🎯 Total Issues: {total_issues}")
    if total_tests > 0:
        overall_test_success = (total_passed / total_tests * 100)
        print(f"🧪 Overall Test Success: {total_passed}/{total_tests} ({overall_test_success:.1f}%)")
    
    # Health score calculation
    health_score = 100
    if total_issues > 0:
        health_score -= min(total_issues * 10, 50)  # Deduct points for issues
    if total_tests > 0 and total_passed < total_tests:
        health_score -= ((total_tests - total_passed) / total_tests) * 30  # Deduct for failed tests
    
    print(f"\n🎯 CI Health Score: {health_score:.1f}/100")
    
    if health_score >= 95:
        print("🎉 EXCELLENT: CI ecosystem is in excellent health")
        return True
    elif health_score >= 80:
        print("✅ GOOD: CI ecosystem is healthy with minor issues")
        return True
    elif health_score >= 60:
        print("⚠️  WARNING: CI ecosystem has moderate issues")
        return True
    else:
        print("🔴 CRITICAL: CI ecosystem has significant health issues")
        return False

if __name__ == "__main__":
    success = test_issue_1064_ci_health()
    exit(0 if success else 1)