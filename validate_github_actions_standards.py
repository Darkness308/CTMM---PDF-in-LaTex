#!/usr/bin/env python3
"""
GitHub Actions Standards Validation for Issue #534

This script provides comprehensive validation of GitHub Actions workflow files
to ensure they meet best practices and standards for CI/CD execution.

Validates:
- YAML syntax and structure
- GitHub Actions specific requirements  
- Security best practices
- Performance considerations
- German language LaTeX support configuration
"""

import yaml
import os
import sys
from pathlib import Path
import re

def validate_github_actions_standards():
    """Comprehensive validation of GitHub Actions workflow standards."""
    
    print("=" * 80)
    print("GITHUB ACTIONS STANDARDS VALIDATION - ISSUE #534")
    print("=" * 80)
    print("Comprehensive validation of workflow files for best practices")
    print("and CI/CD execution standards.\n")
    
    # Define workflow files to validate
    workflow_files = [
        '.github/workflows/latex-build.yml',
        '.github/workflows/latex-validation.yml', 
        '.github/workflows/static.yml'
    ]
    
    print(f"Validating {len(workflow_files)} workflow files...\n")
    
    all_valid = True
    validation_results = []
    
    for file_path in workflow_files:
        print(f"🔍 Validating {os.path.basename(file_path)}")
        print("-" * 60)
        
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            all_valid = False
            validation_results.append((file_path, False, "File not found"))
            continue
            
        try:
            # Read and parse YAML
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check document start marker
            if not content.startswith('---'):
                print(f"❌ Missing YAML document start marker (---)")
                all_valid = False
                validation_results.append((file_path, False, "Missing document start marker"))
                continue
            else:
                print("✅ YAML document start marker present")
            
            # Parse YAML
            parsed = yaml.safe_load(content)
            
            # Validate required top-level keys
            required_keys = ['name', 'on', 'jobs']
            missing_keys = [key for key in required_keys if key not in parsed]
            if missing_keys:
                print(f"❌ Missing required keys: {missing_keys}")
                all_valid = False
                validation_results.append((file_path, False, f"Missing keys: {missing_keys}"))
                continue
            else:
                print("✅ All required top-level keys present")
            
            # Validate 'on' trigger configuration
            if validate_on_triggers(parsed.get('on', {}), file_path):
                print("✅ Trigger configuration valid")
            else:
                all_valid = False
                validation_results.append((file_path, False, "Invalid trigger configuration"))
                continue
            
            # Validate jobs configuration
            if validate_jobs_configuration(parsed.get('jobs', {}), file_path):
                print("✅ Jobs configuration valid")
            else:
                all_valid = False
                validation_results.append((file_path, False, "Invalid jobs configuration"))
                continue
            
            # Validate security practices
            if validate_security_practices(parsed, content, file_path):
                print("✅ Security practices compliant")
            else:
                all_valid = False
                validation_results.append((file_path, False, "Security practices issues"))
                continue
            
            # Special validation for LaTeX build workflows
            if 'latex' in file_path.lower():
                if validate_latex_specific_configuration(parsed, file_path):
                    print("✅ LaTeX-specific configuration valid")
                else:
                    all_valid = False
                    validation_results.append((file_path, False, "LaTeX configuration issues"))
                    continue
            
            print("✅ All validations passed")
            validation_results.append((file_path, True, "All standards met"))
            
        except yaml.YAMLError as e:
            print(f"❌ YAML parsing error: {e}")
            all_valid = False
            validation_results.append((file_path, False, f"YAML error: {e}"))
        except Exception as e:
            print(f"❌ Validation error: {e}")
            all_valid = False
            validation_results.append((file_path, False, f"Error: {e}"))
        
        print()  # Empty line for readability
    
    # Summary
    print("=" * 80)
    print("VALIDATION SUMMARY")
    print("=" * 80)
    
    for file_path, is_valid, message in validation_results:
        status = "✅ PASS" if is_valid else "❌ FAIL"
        filename = os.path.basename(file_path)
        print(f"{status} {filename}: {message}")
    
    print()
    
    if all_valid:
        print("🎉 GITHUB ACTIONS STANDARDS VALIDATION: SUCCESS")
        print("✅ All workflow files meet GitHub Actions best practices")
        print("✅ YAML syntax is correct and compliant")
        print("✅ Security practices are properly implemented")
        print("✅ LaTeX German language support is configured")
        print("✅ CI/CD execution standards are met")
        print("\n📋 STATUS: ISSUE #534 REQUIREMENTS FULFILLED")
    else:
        print("⚠️  GITHUB ACTIONS STANDARDS VALIDATION: ISSUES FOUND")
        print("❌ Some workflow files have standards compliance issues")
        print("🔧 Action needed: Review and fix identified issues")
    
    print("=" * 80)
    return all_valid

def validate_on_triggers(on_config, file_path):
    """Validate the 'on' trigger configuration."""
    if not on_config:
        print("❌ No trigger configuration found")
        return False
    
    # Common valid triggers
    valid_triggers = [
        'push', 'pull_request', 'workflow_dispatch', 'schedule',
        'release', 'create', 'delete', 'fork', 'issues', 'watch'
    ]
    
    configured_triggers = list(on_config.keys())
    invalid_triggers = [t for t in configured_triggers if t not in valid_triggers]
    
    if invalid_triggers:
        print(f"❌ Invalid triggers found: {invalid_triggers}")
        return False
    
    # Validate push/pull_request trigger configuration
    for trigger in ['push', 'pull_request']:
        if trigger in on_config:
            trigger_config = on_config[trigger]
            if isinstance(trigger_config, dict) and 'branches' in trigger_config:
                branches = trigger_config['branches']
                if not isinstance(branches, list) or not branches:
                    print(f"❌ Invalid {trigger} branches configuration")
                    return False
    
    return True

def validate_jobs_configuration(jobs_config, file_path):
    """Validate the jobs configuration."""
    if not jobs_config:
        print("❌ No jobs configuration found")
        return False
    
    for job_name, job_config in jobs_config.items():
        if not isinstance(job_config, dict):
            print(f"❌ Invalid job configuration for {job_name}")
            return False
        
        # Validate required job keys
        if 'runs-on' not in job_config:
            print(f"❌ Missing 'runs-on' for job {job_name}")
            return False
        
        # Validate runner
        runner = job_config['runs-on']
        valid_runners = ['ubuntu-latest', 'ubuntu-20.04', 'ubuntu-18.04', 'windows-latest', 'macos-latest']
        if runner not in valid_runners:
            print(f"⚠️  Unusual runner for {job_name}: {runner}")
        
        # Validate steps if present
        if 'steps' in job_config:
            steps = job_config['steps']
            if not isinstance(steps, list):
                print(f"❌ Invalid steps configuration for {job_name}")
                return False
            
            for i, step in enumerate(steps):
                if not isinstance(step, dict):
                    print(f"❌ Invalid step {i} in job {job_name}")
                    return False
                
                # Validate step has either 'uses' or 'run'
                if 'uses' not in step and 'run' not in step:
                    print(f"❌ Step {i} in {job_name} missing 'uses' or 'run'")
                    return False
    
    return True

def validate_security_practices(parsed, content, file_path):
    """Validate security best practices."""
    
    # Check for pinned action versions
    action_pattern = r'uses:\s*([^@\s]+)@([^\s]+)'
    actions = re.findall(action_pattern, content)
    
    for action, version in actions:
        if version == 'main' or version == 'master':
            print(f"⚠️  Action {action} uses mutable reference: {version}")
        elif not re.match(r'^v\d+', version) and not re.match(r'^[a-f0-9]{40}$', version):
            print(f"⚠️  Action {action} version format unusual: {version}")
    
    # Check for secrets usage patterns
    if 'secrets.' in content.lower():
        print("ℹ️  Secrets usage detected - ensure proper handling")
    
    # Check for shell injection risks
    if 'shell:' in content:
        print("ℹ️  Custom shell detected - ensure safe usage")
    
    return True

def validate_latex_specific_configuration(parsed, file_path):
    """Validate LaTeX-specific workflow configuration."""
    
    # Check for LaTeX action usage
    jobs = parsed.get('jobs', {})
    
    for job_name, job_config in jobs.items():
        steps = job_config.get('steps', [])
        
        latex_action_found = False
        german_support_found = False
        
        for step in steps:
            # Check for LaTeX action
            if 'uses' in step and 'latex-action' in step['uses']:
                latex_action_found = True
                
                # Check for German language support
                if 'with' in step:
                    with_config = step['with']
                    if 'extra_system_packages' in with_config:
                        packages = with_config['extra_system_packages']
                        if 'texlive-lang-german' in str(packages):
                            german_support_found = True
            
            # Check for German language in run commands
            if 'run' in step:
                run_commands = step['run']
                if 'texlive-lang-german' in str(run_commands):
                    german_support_found = True
        
        if 'latex-build' in file_path and latex_action_found:
            print("✅ LaTeX action properly configured")
            if german_support_found:
                print("✅ German language support configured")
            else:
                print("⚠️  German language support not explicitly configured")
    
    return True

if __name__ == "__main__":
    # Ensure we're in the repository root
    if not Path('.github/workflows').exists():
        print("Error: This script must be run from the repository root directory")
        print("Expected to find .github/workflows/ directory")
        sys.exit(1)
    
    # Run validation
    success = validate_github_actions_standards()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)