#!/usr/bin/env python3
"""
GitHub Actions Version Validation - Issue #1064
Validates GitHub Actions versions across all workflows for compatibility and security.
"""

import os
import yaml
import re
from typing import Dict, List, Tuple, Optional

def get_workflow_files() -> List[str]:
    """Get all GitHub Actions workflow files."""
    workflow_dir = '.github/workflows'
    if not os.path.exists(workflow_dir):
        return []
    
    return [
        os.path.join(workflow_dir, f)
        for f in os.listdir(workflow_dir)
        if f.endswith('.yml') or f.endswith('.yaml')
    ]

def extract_actions_from_workflow(workflow_file: str) -> List[Tuple[str, str, str]]:
    """Extract GitHub Actions and their versions from a workflow file.
    
    Returns:
        List of tuples: (action_name, version, step_name)
    """
    actions = []
    
    try:
        with open(workflow_file, 'r', encoding='utf-8') as f:
            workflow_data = yaml.safe_load(f)
        
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
    
    except Exception as e:
        print(f"❌ Error parsing {workflow_file}: {e}")
    
    return actions

def get_known_action_versions() -> Dict[str, Dict[str, str]]:
    """Get known compatible and recommended versions for common GitHub Actions."""
    return {
        'actions/checkout': {
            'recommended': 'v4',
            'compatible': ['v3', 'v4'],
            'deprecated': ['v1', 'v2'],
            'description': 'Repository checkout action'
        },
        'actions/setup-python': {
            'recommended': 'v4',
            'compatible': ['v3', 'v4'],
            'deprecated': ['v1', 'v2'],
            'description': 'Python environment setup'
        },
        'actions/upload-artifact': {
            'recommended': 'v4',
            'compatible': ['v3', 'v4'],
            'deprecated': ['v1', 'v2'],
            'description': 'Artifact upload action'
        },
        'actions/github-script': {
            'recommended': 'v7',
            'compatible': ['v6', 'v7'],
            'deprecated': ['v1', 'v2', 'v3', 'v4', 'v5'],
            'description': 'GitHub API scripting'
        },
        'dante-ev/latex-action': {
            'recommended': 'v0.2.0',
            'compatible': ['v0.2.0'],
            'deprecated': ['v2', 'v0.1.0'],
            'description': 'LaTeX compilation action'
        }
    }

def validate_action_version(action_name: str, version: str, known_versions: Dict[str, Dict[str, str]]) -> Tuple[str, str]:
    """Validate a single action version.
    
    Returns:
        Tuple of (status, message) where status is 'ok', 'warning', 'deprecated', or 'unknown'
    """
    if action_name not in known_versions:
        return 'unknown', f'Unknown action: {action_name}'
    
    action_info = known_versions[action_name]
    
    if version == action_info['recommended']:
        return 'ok', f'Using recommended version {version}'
    elif version in action_info['compatible']:
        return 'warning', f'Using compatible version {version}, recommend {action_info["recommended"]}'
    elif version in action_info['deprecated']:
        return 'deprecated', f'Using deprecated version {version}, upgrade to {action_info["recommended"]}'
    else:
        return 'unknown', f'Unknown version {version}, recommend {action_info["recommended"]}'

def validate_action_versions():
    """Main validation function for GitHub Actions versions."""
    print("=" * 70)
    print("GitHub Actions Version Validation - Issue #1064")
    print("=" * 70)
    
    workflow_files = get_workflow_files()
    if not workflow_files:
        print("❌ No workflow files found")
        return False
    
    print(f"\n🔍 Scanning {len(workflow_files)} workflow files...")
    
    known_versions = get_known_action_versions()
    all_actions = []
    validation_results = []
    
    # Extract all actions from all workflows
    for workflow_file in workflow_files:
        print(f"\n📋 Analyzing {workflow_file}...")
        actions = extract_actions_from_workflow(workflow_file)
        
        for action_name, version, step_name in actions:
            all_actions.append((workflow_file, action_name, version, step_name))
            print(f"   📦 {action_name}@{version} in '{step_name}'")
    
    if not all_actions:
        print("❌ No GitHub Actions found in workflows")
        return False
    
    # Validate each action
    print(f"\n🔍 Validating {len(all_actions)} action usages...")
    print("-" * 50)
    
    status_counts = {'ok': 0, 'warning': 0, 'deprecated': 0, 'unknown': 0}
    
    for workflow_file, action_name, version, step_name in all_actions:
        status, message = validate_action_version(action_name, version, known_versions)
        status_counts[status] += 1
        
        # Format output based on status
        if status == 'ok':
            print(f"✅ {action_name}@{version}: {message}")
        elif status == 'warning':
            print(f"⚠️  {action_name}@{version}: {message}")
        elif status == 'deprecated':
            print(f"🔴 {action_name}@{version}: {message}")
        else:
            print(f"❓ {action_name}@{version}: {message}")
        
        validation_results.append({
            'workflow': os.path.basename(workflow_file),
            'action': action_name,
            'version': version,
            'step': step_name,
            'status': status,
            'message': message
        })
    
    # Summary
    print("\n" + "=" * 70)
    print("VALIDATION SUMMARY")
    print("=" * 70)
    
    total_actions = len(all_actions)
    print(f"📊 Actions analyzed: {total_actions}")
    print(f"✅ Recommended versions: {status_counts['ok']}")
    print(f"⚠️  Compatible versions: {status_counts['warning']}")
    print(f"🔴 Deprecated versions: {status_counts['deprecated']}")
    print(f"❓ Unknown actions/versions: {status_counts['unknown']}")
    
    # Calculate health score
    health_score = ((status_counts['ok'] + status_counts['warning']) / total_actions) * 100
    print(f"\n🎯 Version Health Score: {health_score:.1f}%")
    
    if health_score >= 90:
        print("🎉 EXCELLENT: GitHub Actions versions are well-maintained")
        overall_status = True
    elif health_score >= 75:
        print("✅ GOOD: Most GitHub Actions are using recommended versions")
        overall_status = True
    elif health_score >= 50:
        print("⚠️  WARNING: Some GitHub Actions need version updates")
        overall_status = True
    else:
        print("🔴 CRITICAL: Many GitHub Actions are using deprecated versions")
        overall_status = False
    
    # Recommendations
    if status_counts['deprecated'] > 0 or status_counts['unknown'] > 0:
        print("\n📋 RECOMMENDATIONS:")
        for result in validation_results:
            if result['status'] in ['deprecated', 'unknown']:
                print(f"   • Update {result['action']} in {result['workflow']}")
    
    return overall_status

if __name__ == "__main__":
    success = validate_action_versions()
    exit(0 if success else 1)