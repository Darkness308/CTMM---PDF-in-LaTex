#!/usr/bin/env python3
"""
PR Manager - Pull Request Creation and Management
Manages the creation of pull requests for automated fixes.
"""

import os
import json
import requests
import logging
import subprocess
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

from healing_config import config
from fix_strategies import FixResult
from error_analyzer import ErrorAnalysis

@dataclass
class HealingPR:
    """Represents a healing pull request."""
    number: int
    title: str
    branch: str
    url: str
    created_at: str
    workflow_run_id: int
    error_categories: List[str]
    fix_results: List[FixResult]

class PRManager:
    """Manages pull request creation and tracking for workflow healing."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.session = requests.Session()

        # Set up authentication
        if config.github_token:
            self.session.headers.update({
                'Authorization': f'token {config.github_token}',
                'Accept': 'application/vnd.github.v3+json',
                'User-Agent': 'CTMM-Workflow-Healing-System/1.0'
            })
        else:
            self.logger.warning("No GitHub token provided - PR operations will fail")

    def create_healing_pr(self, analysis: ErrorAnalysis, fix_results: List[FixResult]) -> Optional[HealingPR]:
        """Create a pull request for workflow healing fixes."""
        if not fix_results or not any(r.success for r in fix_results):
            self.logger.warning("No successful fixes to create PR for")
            return None

        # Check if we've reached the maximum number of open healing PRs
        existing_prs = self._get_open_healing_prs()
        if len(existing_prs) >= config.max_concurrent_prs:
            self.logger.warning(f"Maximum healing PRs ({config.max_concurrent_prs}) already open")
            return None

        # Create a new branch for the fixes
        branch_name = self._create_healing_branch(analysis)
        if not branch_name:
            return None

        # Apply fixes to the branch
        if not self._apply_fixes_to_branch(branch_name, fix_results):
            self._cleanup_branch(branch_name)
            return None

        # Create the pull request
        pr_data = self._create_pull_request(analysis, fix_results, branch_name)
        if not pr_data:
            self._cleanup_branch(branch_name)
            return None

        healing_pr = HealingPR(
            number=pr_data['number'],
            title=pr_data['title'],
            branch=branch_name,
            url=pr_data['html_url'],
            created_at=pr_data['created_at'],
            workflow_run_id=analysis.workflow_run_id,
            error_categories=list(analysis.error_categories),
            fix_results=fix_results
        )

        self.logger.info(f"Created healing PR #{healing_pr.number}: {healing_pr.title}")
        return healing_pr

    def _create_healing_branch(self, analysis: ErrorAnalysis) -> Optional[str]:
        """Create a new branch for healing fixes."""
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        branch_name = f"{config.pr_settings['branch_prefix']}/run-{analysis.workflow_run_id}-{timestamp}"

        try:
            # Get current main branch SHA
            result = subprocess.run(
                ['git', 'rev-parse', 'HEAD'],
                capture_output=True,
                text=True,
                check=True
            )
            base_sha = result.stdout.strip()

            # Create and checkout new branch
            subprocess.run(
                ['git', 'checkout', '-b', branch_name],
                check=True,
                capture_output=True
            )

            self.logger.info(f"Created healing branch: {branch_name}")
            return branch_name

        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to create healing branch: {e}")
            return None

    def _apply_fixes_to_branch(self, branch_name: str, fix_results: List[FixResult]) -> bool:
        """Apply fixes to the healing branch and commit changes."""
        try:
            files_to_commit = set()

            # Collect all modified files
            for result in fix_results:
                if result.success:
                    files_to_commit.update(result.files_modified)

            if not files_to_commit:
                self.logger.warning("No files to commit")
                return False

            # Stage the files
            for file_path in files_to_commit:
                subprocess.run(['git', 'add', file_path], check=True)

            # Create commit message
            commit_message = self._generate_commit_message(fix_results)

            # Commit the changes
            subprocess.run(
                ['git', 'commit', '-m', commit_message],
                check=True,
                capture_output=True
            )

            # Push the branch
            subprocess.run(
                ['git', 'push', 'origin', branch_name],
                check=True,
                capture_output=True
            )

            self.logger.info(f"Committed and pushed fixes to {branch_name}")
            return True

        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to apply fixes to branch: {e}")
            return False

    def _create_pull_request(self, analysis: ErrorAnalysis, fix_results: List[FixResult], branch_name: str) -> Optional[Dict]:
        """Create the pull request via GitHub API."""
        try:
            title = self._generate_pr_title(analysis, fix_results)
            body = self._generate_pr_body(analysis, fix_results)

            pr_data = {
                'title': title,
                'body': body,
                'head': branch_name,
                'base': 'main',
                'maintainer_can_modify': True
            }

            url = f"{config.api_base_url}/repos/{config.repo_owner}/{config.repo_name}/pulls"
            response = self.session.post(url, json=pr_data)
            response.raise_for_status()

            pr_response = response.json()

            # Add labels if configured
            if config.pr_settings['labels']:
                self._add_labels_to_pr(pr_response['number'], config.pr_settings['labels'])

            return pr_response

        except requests.RequestException as e:
            self.logger.error(f"Failed to create pull request: {e}")
            return None

    def _generate_commit_message(self, fix_results: List[FixResult]) -> str:
        """Generate a commit message for the fixes."""
        prefix = config.pr_settings['commit_message_prefix']

        successful_fixes = [r for r in fix_results if r.success]
        if len(successful_fixes) == 1:
            return f"{prefix} {successful_fixes[0].description}"
        else:
            categories = set()
            for result in successful_fixes:
                # Extract category from description
                if 'LaTeX action' in result.description:
                    categories.add('LaTeX action versions')
                elif 'packages' in result.description:
                    categories.add('package dependencies')
                elif 'timeout' in result.description:
                    categories.add('timeouts')
                elif 'dependency' in result.description:
                    categories.add('Python dependencies')
                else:
                    categories.add('workflow issues')

            return f"{prefix} Fix {', '.join(categories)}"

    def _generate_pr_title(self, analysis: ErrorAnalysis, fix_results: List[FixResult]) -> str:
        """Generate a title for the pull request."""
        prefix = config.pr_settings['pr_title_prefix']

        successful_fixes = [r for r in fix_results if r.success]
        if len(successful_fixes) == 1:
            return f"{prefix} {successful_fixes[0].description}"

        # Summarize multiple fixes
        categories = len(analysis.error_categories)
        errors = analysis.total_errors

        return f"{prefix} Fix {categories} error categories ({errors} issues) in {analysis.workflow_name}"

    def _generate_pr_body(self, analysis: ErrorAnalysis, fix_results: List[FixResult]) -> str:
        """Generate the body content for the pull request."""
        lines = []

        lines.append("## [FIX] Automated Workflow Healing")
        lines.append("")
        lines.append("This PR contains automated fixes for workflow errors identified by the healing system.")
        lines.append("")

        # Workflow information
        lines.append("### [TEST] Workflow Information")
        lines.append(f"- **Workflow**: {analysis.workflow_name}")
        lines.append(f"- **Run ID**: {analysis.workflow_run_id}")
        lines.append(f"- **Error Categories**: {', '.join(analysis.error_categories)}")
        lines.append(f"- **Total Errors**: {analysis.total_errors}")
        lines.append("")

        # Applied fixes
        lines.append("### [PASS] Applied Fixes")
        lines.append("")

        successful_fixes = [r for r in fix_results if r.success]
        failed_fixes = [r for r in fix_results if not r.success]

        for i, result in enumerate(successful_fixes, 1):
            lines.append(f"**{i}. {result.description}**")
            if result.files_modified:
                lines.append(f"  - Files modified: `{', '.join(result.files_modified)}`")
            if result.changes_made:
                for change in result.changes_made:
                    lines.append(f"  - {change}")
            lines.append(f"  - Validation: {'[PASS] Passed' if result.validation_passed else '[WARN] Skipped'}")
            lines.append("")

        if failed_fixes:
            lines.append("### [FAIL] Failed Fixes")
            lines.append("")
            for i, result in enumerate(failed_fixes, 1):
                lines.append(f"**{i}. {result.description}**")
                if result.error_message:
                    lines.append(f"  - Error: {result.error_message}")
                lines.append("")

        # Recommendations
        lines.append("### [NOTE] Recommendations")
        lines.append("")
        if analysis.recommended_fixes:
            for i, fix in enumerate(analysis.recommended_fixes, 1):
                status = "[PASS]" if any(fix.lower() in r.description.lower() for r in successful_fixes) else "[SYNC]"
                lines.append(f"{i}. {status} {fix}")
        else:
            lines.append("No specific recommendations generated.")
        lines.append("")

        # Testing instructions
        lines.append("### [TEST] Testing")
        lines.append("")
        lines.append("After merging this PR, the following workflows should be tested:")
        lines.append("")
        for workflow in config.monitored_workflows:
            lines.append(f"- [ ] {workflow}")
        lines.append("")

        # Footer
        lines.append("---")
        lines.append("")
        lines.append("*This PR was created automatically by the CTMM Workflow Healing System.*")
        lines.append(f"*Analysis timestamp: {analysis.analysis_timestamp}*")
        lines.append("")
        lines.append("**[WARN] Manual Review Required**: Please review all changes before merging.")

        return '\n'.join(lines)

    def _add_labels_to_pr(self, pr_number: int, labels: List[str]) -> bool:
        """Add labels to a pull request."""
        try:
            url = f"{config.api_base_url}/repos/{config.repo_owner}/{config.repo_name}/issues/{pr_number}/labels"
            response = self.session.post(url, json={'labels': labels})
            response.raise_for_status()

            self.logger.info(f"Added labels to PR #{pr_number}: {', '.join(labels)}")
            return True

        except requests.RequestException as e:
            self.logger.error(f"Failed to add labels to PR #{pr_number}: {e}")
            return False

    def _get_open_healing_prs(self) -> List[Dict]:
        """Get all open healing pull requests."""
        try:
            url = f"{config.api_base_url}/repos/{config.repo_owner}/{config.repo_name}/pulls"
            params = {'state': 'open', 'per_page': 100}

            response = self.session.get(url, params=params)
            response.raise_for_status()

            prs = response.json()
            healing_prs = []

            for pr in prs:
                if (pr['head']['ref'].startswith(config.pr_settings['branch_prefix']) or
                    pr['title'].startswith(config.pr_settings['pr_title_prefix'])):
                    healing_prs.append(pr)

            return healing_prs

        except requests.RequestException as e:
            self.logger.error(f"Failed to get open healing PRs: {e}")
            return []

    def _cleanup_branch(self, branch_name: str) -> bool:
        """Clean up a healing branch after failed PR creation."""
        try:
            # Switch back to main
            subprocess.run(['git', 'checkout', 'main'], check=True, capture_output=True)

            # Delete the local branch
            subprocess.run(['git', 'branch', '-D', branch_name], check=True, capture_output=True)

            # Try to delete remote branch if it exists
            try:
                subprocess.run(['git', 'push', 'origin', '--delete', branch_name],
                             check=True, capture_output=True)
            except subprocess.CalledProcessError:
                pass  # Remote branch might not exist yet

            self.logger.info(f"Cleaned up healing branch: {branch_name}")
            return True

        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to cleanup branch {branch_name}: {e}")
            return False

    def get_pr_status(self, pr_number: int) -> Optional[Dict]:
        """Get the current status of a pull request."""
        try:
            url = f"{config.api_base_url}/repos/{config.repo_owner}/{config.repo_name}/pulls/{pr_number}"
            response = self.session.get(url)
            response.raise_for_status()

            return response.json()

        except requests.RequestException as e:
            self.logger.error(f"Failed to get PR status for #{pr_number}: {e}")
            return None

    def close_stale_healing_prs(self, max_age_hours: int = 48) -> List[int]:
        """Close healing PRs that are older than the specified age."""
        closed_prs = []

        try:
            healing_prs = self._get_open_healing_prs()

            for pr in healing_prs:
                created_at = datetime.fromisoformat(pr['created_at'].replace('Z', '+00:00'))
                age_hours = (datetime.now().astimezone() - created_at).total_seconds() / 3600

                if age_hours > max_age_hours:
                    if self._close_pr(pr['number'], "Closing stale automated healing PR"):
                        closed_prs.append(pr['number'])

                        # Also cleanup the branch
                        branch_name = pr['head']['ref']
                        self._cleanup_branch(branch_name)

            return closed_prs

        except Exception as e:
            self.logger.error(f"Failed to close stale healing PRs: {e}")
            return []

    def _close_pr(self, pr_number: int, reason: str) -> bool:
        """Close a pull request."""
        try:
            url = f"{config.api_base_url}/repos/{config.repo_owner}/{config.repo_name}/pulls/{pr_number}"
            data = {'state': 'closed'}

            response = self.session.patch(url, json=data)
            response.raise_for_status()

            # Add a comment explaining why it was closed
            self._add_pr_comment(pr_number, f"[EMOJI] {reason}")

            self.logger.info(f"Closed PR #{pr_number}: {reason}")
            return True

        except requests.RequestException as e:
            self.logger.error(f"Failed to close PR #{pr_number}: {e}")
            return False

    def _add_pr_comment(self, pr_number: int, comment: str) -> bool:
        """Add a comment to a pull request."""
        try:
            url = f"{config.api_base_url}/repos/{config.repo_owner}/{config.repo_name}/issues/{pr_number}/comments"
            response = self.session.post(url, json={'body': comment})
            response.raise_for_status()

            return True

        except requests.RequestException as e:
            self.logger.error(f"Failed to add comment to PR #{pr_number}: {e}")
            return False

def main():
    """Test the PR manager functionality."""
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    pr_manager = PRManager()

    print("[FIX] Testing PR Manager")
    print("=" * 50)

    # Test configuration validation
    config_issues = config.validate_config()
    if config_issues:
        print("[FAIL] Configuration Issues:")
        for issue in config_issues:
            print(f"  - {issue}")
        return

    print("[PASS] Configuration validated")

    # Check for existing healing PRs
    print("\n[TEST] Checking for existing healing PRs...")
    healing_prs = pr_manager._get_open_healing_prs()
    print(f"Found {len(healing_prs)} existing healing PRs")

    for pr in healing_prs:
        print(f"  - PR #{pr['number']}: {pr['title']}")

    # Test stale PR cleanup (dry run)
    print("\n[EMOJI] Testing stale PR detection...")
    if healing_prs:
        for pr in healing_prs:
            created_at = datetime.fromisoformat(pr['created_at'].replace('Z', '+00:00'))
            age_hours = (datetime.now().astimezone() - created_at).total_seconds() / 3600
            print(f"  - PR #{pr['number']}: {age_hours:.1f} hours old")
    else:
        print("  No healing PRs to check")

    print("\n[PASS] PR manager test completed")

if __name__ == "__main__":
    main()
