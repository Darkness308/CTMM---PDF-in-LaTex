#!/usr/bin/env python3
"""
Automated Workflow Healing System - Configuration
Configuration settings for the workflow error analysis and self-healing system.
"""

import os
from typing import Dict, List, Optional

class HealingConfig:
    """Configuration class for the workflow healing system."""

    def __init__(self):
        # GitHub API Configuration
        self.github_token = os.environ.get('GITHUB_TOKEN')
        self.repo_owner = os.environ.get('GITHUB_REPOSITORY_OWNER', 'Darkness308')
        self.repo_name = os.environ.get('GITHUB_REPOSITORY_NAME', 'CTMM---PDF-in-LaTex')
        self.api_base_url = 'https://api.github.com'

        # Workflow Monitoring Settings
        self.max_workflow_age_hours = 24  # Only analyze workflows from last 24 hours
        self.failure_states = ['failure', 'action_required', 'cancelled', 'timed_out']
        self.monitored_workflows = [
            'latex-build.yml',
            'pr-validation.yml',
            'latex-validation.yml',
            'static.yml',
            'automated-pr-merge-test.yml',
            'test-dante-version.yml'
        ]

        # Error Analysis Settings
        self.error_patterns = {
            'latex_action_version': [
                r'uses: dante-ev/latex-action@v[\d\.]+',
                r'Invalid version.*dante-ev/latex-action',
                r'The version.*does not exist'
            ],
            'package_missing': [
                r'Package .* not found',
                r'File .*.sty not found',
                r'LaTeX Error: File .* not found'
            ],
            'syntax_error': [
                r'LaTeX Error: .*',
                r'Undefined control sequence',
                r'Missing.*}',
                r'Runaway argument'
            ],
            'timeout': [
                r'The operation was canceled',
                r'timeout',
                r'exceeded.*time limit'
            ],
            'resource_limit': [
                r'No space left on device',
                r'out of memory',
                r'resource temporarily unavailable'
            ],
            'dependency_error': [
                r'pip.*failed',
                r'Unable to install',
                r'Could not find a version',
                r'No matching distribution found'
            ]
        }

        # Fix Strategy Configuration
        self.fix_strategies = {
            'latex_action_version': {
                'priority': 1,
                'max_attempts': 3,
                'known_good_versions': ['v2.3.0', 'v0.2.0'],
                'fallback_version': 'v2.3.0'
            },
            'package_missing': {
                'priority': 2,
                'max_attempts': 2,
                'package_sources': ['texlive-full', 'texlive-latex-extra']
            },
            'syntax_error': {
                'priority': 3,
                'max_attempts': 1,
                'validation_required': True
            },
            'timeout': {
                'priority': 2,
                'max_attempts': 2,
                'timeout_multiplier': 1.5
            },
            'dependency_error': {
                'priority': 2,
                'max_attempts': 3,
                'pip_upgrade': True
            }
        }

        # PR Management Settings
        self.pr_settings = {
            'branch_prefix': 'workflow-healing',
            'commit_message_prefix': '[Automated Fix]',
            'pr_title_prefix': '🔧 Automated Workflow Fix:',
            'labels': ['documentation', 'automated-fix'],
            'auto_merge': False,  # Require manual approval
            'delete_branch_after_merge': True
        }

        # Healing Process Limits
        self.max_healing_attempts = 5  # Max attempts per workflow
        self.max_concurrent_prs = 3    # Max open healing PRs at once
        self.cooldown_minutes = 30     # Wait time between healing attempts
        self.max_iterations_per_run = 10  # Safety limit for single execution

        # Logging Configuration
        self.log_level = 'INFO'
        self.log_file = 'workflow_healing.log'
        self.detailed_logs = True
        self.preserve_logs_days = 7

        # Validation Settings
        self.validation_commands = [
            'python3 ctmm_build.py',
            'python3 validate_latex_syntax.py',
            'python3 validate_workflow_syntax.py'
        ]

        # Unsolvable Error Patterns (stop healing attempts)
        self.unsolvable_patterns = [
            r'Permission denied',
            r'Access denied',
            r'Authentication failed',
            r'Repository not found',
            r'Invalid repository',
            r'Rate limit exceeded'
        ]

    def get_workflow_file_path(self, workflow_name: str) -> str:
        """Get the full path to a workflow file."""
        return f".github/workflows/{workflow_name}"

    def is_monitored_workflow(self, workflow_name: str) -> bool:
        """Check if a workflow should be monitored for healing."""
        return workflow_name in self.monitored_workflows

    def get_error_category(self, error_text: str) -> Optional[str]:
        """Categorize an error based on pattern matching."""
        import re
        for category, patterns in self.error_patterns.items():
            for pattern in patterns:
                if re.search(pattern, error_text, re.IGNORECASE):
                    return category
        return None

    def is_unsolvable_error(self, error_text: str) -> bool:
        """Check if an error is considered unsolvable."""
        import re
        for pattern in self.unsolvable_patterns:
            if re.search(pattern, error_text, re.IGNORECASE):
                return True
        return False

    def validate_config(self) -> List[str]:
        """Validate configuration and return any issues."""
        issues = []

        if not self.github_token:
            issues.append("GITHUB_TOKEN environment variable not set")

        if not self.repo_owner or not self.repo_name:
            issues.append("Repository owner and name must be configured")

        if self.max_healing_attempts <= 0:
            issues.append("max_healing_attempts must be positive")

        if self.max_concurrent_prs <= 0:
            issues.append("max_concurrent_prs must be positive")

        return issues

# Global configuration instance
config = HealingConfig()