#!/usr/bin/env python3
"""
Workflow Monitor - GitHub API Integration
Monitors GitHub Actions workflows for failures and retrieves error information.
"""

import os
import sys
import requests
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

from healing_config import config

@dataclass
class WorkflowRun:
    """Represents a GitHub Actions workflow run."""
    id: int
    workflow_name: str
    status: str
    conclusion: str
    created_at: str
    updated_at: str
    head_sha: str
    head_branch: str
    html_url: str
    jobs_url: str
    logs_url: str

@dataclass
class JobRun:
    """Represents a job within a workflow run."""
    id: int
    name: str
    status: str
    conclusion: str
    started_at: str
    completed_at: str
    html_url: str
    logs_url: str

class WorkflowMonitor:
    """Monitors GitHub Actions workflows for failures."""

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
            self.logger.warning("No GitHub token provided - API rate limits will apply")

    def get_failed_workflows(self, hours_back: int = None) -> List[WorkflowRun]:
        """Get all failed workflow runs within the specified time range."""
        if hours_back is None:
            hours_back = config.max_workflow_age_hours

        since = datetime.utcnow() - timedelta(hours=hours_back)
        failed_runs = []

        try:
            # Get workflow runs for the repository
            url = f"{config.api_base_url}/repos/{config.repo_owner}/{config.repo_name}/actions/runs"
            params = {
                'status': 'completed',
                'per_page': 100,
                'created': f'>{since.isoformat()}Z'
            }

            response = self.session.get(url, params=params)
            response.raise_for_status()

            data = response.json()

            for run_data in data.get('workflow_runs', []):
                # Check if this is a monitored workflow and has failed
                workflow_name = run_data['name']
                workflow_file = os.path.basename(run_data['path'])

                if (config.is_monitored_workflow(workflow_file) and
                    run_data['conclusion'] in config.failure_states):

                    workflow_run = WorkflowRun(
                        id=run_data['id'],
                        workflow_name=workflow_name,
                        status=run_data['status'],
                        conclusion=run_data['conclusion'],
                        created_at=run_data['created_at'],
                        updated_at=run_data['updated_at'],
                        head_sha=run_data['head_sha'],
                        head_branch=run_data['head_branch'],
                        html_url=run_data['html_url'],
                        jobs_url=run_data['jobs_url'],
                        logs_url=run_data['logs_url']
                    )

                    failed_runs.append(workflow_run)
                    self.logger.info(f"Found failed workflow: {workflow_name} (ID: {run_data['id']})")

            self.logger.info(f"Found {len(failed_runs)} failed workflow runs")
            return failed_runs

        except requests.RequestException as e:
            self.logger.error(f"Failed to fetch workflow runs: {e}")
            return []

    def get_workflow_jobs(self, run_id: int) -> List[JobRun]:
        """Get all jobs for a specific workflow run."""
        try:
            url = f"{config.api_base_url}/repos/{config.repo_owner}/{config.repo_name}/actions/runs/{run_id}/jobs"
            response = self.session.get(url)
            response.raise_for_status()

            data = response.json()
            jobs = []

            for job_data in data.get('jobs', []):
                job = JobRun(
                    id=job_data['id'],
                    name=job_data['name'],
                    status=job_data['status'],
                    conclusion=job_data.get('conclusion'),
                    started_at=job_data.get('started_at'),
                    completed_at=job_data.get('completed_at'),
                    html_url=job_data['html_url'],
                    logs_url=f"{config.api_base_url}/repos/{config.repo_owner}/{config.repo_name}/actions/jobs/{job_data['id']}/logs"
                )
                jobs.append(job)

            return jobs

        except requests.RequestException as e:
            self.logger.error(f"Failed to fetch jobs for run {run_id}: {e}")
            return []

    def get_job_logs(self, job_id: int) -> str:
        """Get the logs for a specific job."""
        try:
            url = f"{config.api_base_url}/repos/{config.repo_owner}/{config.repo_name}/actions/jobs/{job_id}/logs"
            response = self.session.get(url)
            response.raise_for_status()

            # The response is the raw log text
            return response.text

        except requests.RequestException as e:
            self.logger.error(f"Failed to fetch logs for job {job_id}: {e}")
            return ""

    def get_workflow_run_logs(self, run_id: int) -> Dict[str, str]:
        """Get logs for all jobs in a workflow run."""
        jobs = self.get_workflow_jobs(run_id)
        logs = {}

        for job in jobs:
            if job.conclusion in config.failure_states:
                job_logs = self.get_job_logs(job.id)
                logs[job.name] = job_logs
                self.logger.debug(f"Retrieved logs for failed job: {job.name}")

        return logs

    def restart_workflow(self, run_id: int) -> bool:
        """Restart a failed workflow run."""
        try:
            url = f"{config.api_base_url}/repos/{config.repo_owner}/{config.repo_name}/actions/runs/{run_id}/rerun"
            response = self.session.post(url)
            response.raise_for_status()

            self.logger.info(f"Successfully restarted workflow run {run_id}")
            return True

        except requests.RequestException as e:
            self.logger.error(f"Failed to restart workflow run {run_id}: {e}")
            return False

    def get_recent_workflow_status(self, workflow_name: str, branch: str = 'main') -> Optional[str]:
        """Get the status of the most recent run for a specific workflow."""
        try:
            url = f"{config.api_base_url}/repos/{config.repo_owner}/{config.repo_name}/actions/runs"
            params = {
                'workflow_id': workflow_name,
                'branch': branch,
                'per_page': 1
            }

            response = self.session.get(url, params=params)
            response.raise_for_status()

            data = response.json()
            runs = data.get('workflow_runs', [])

            if runs:
                return runs[0].get('conclusion')

            return None

        except requests.RequestException as e:
            self.logger.error(f"Failed to get workflow status for {workflow_name}: {e}")
            return None

    def wait_for_workflow_completion(self, run_id: int, timeout_minutes: int = 30) -> Optional[str]:
        """Wait for a workflow run to complete and return its conclusion."""
        import time

        start_time = time.time()
        timeout_seconds = timeout_minutes * 60

        while time.time() - start_time < timeout_seconds:
            try:
                url = f"{config.api_base_url}/repos/{config.repo_owner}/{config.repo_name}/actions/runs/{run_id}"
                response = self.session.get(url)
                response.raise_for_status()

                data = response.json()
                status = data.get('status')
                conclusion = data.get('conclusion')

                if status == 'completed':
                    self.logger.info(f"Workflow run {run_id} completed with conclusion: {conclusion}")
                    return conclusion

                self.logger.debug(f"Workflow run {run_id} still running (status: {status})")
                time.sleep(30)  # Check every 30 seconds

            except requests.RequestException as e:
                self.logger.error(f"Error checking workflow status: {e}")
                time.sleep(60)  # Wait longer on error

        self.logger.warning(f"Timeout waiting for workflow run {run_id} to complete")
        return None

    def get_open_pull_requests(self) -> List[Dict]:
        """Get all open pull requests for the repository."""
        try:
            url = f"{config.api_base_url}/repos/{config.repo_owner}/{config.repo_name}/pulls"
            params = {'state': 'open', 'per_page': 100}

            response = self.session.get(url, params=params)
            response.raise_for_status()

            return response.json()

        except requests.RequestException as e:
            self.logger.error(f"Failed to fetch open pull requests: {e}")
            return []

    def get_healing_prs(self) -> List[Dict]:
        """Get open pull requests created by the healing system."""
        prs = self.get_open_pull_requests()
        healing_prs = []

        for pr in prs:
            if (pr['head']['ref'].startswith(config.pr_settings['branch_prefix']) or
                pr['title'].startswith(config.pr_settings['pr_title_prefix'])):
                healing_prs.append(pr)

        return healing_prs

def main():
    """Test the workflow monitor functionality."""
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    monitor = WorkflowMonitor()

    print("🔍 Testing Workflow Monitor")
    print("=" * 50)

    # Test configuration validation
    config_issues = config.validate_config()
    if config_issues:
        print("❌ Configuration Issues:")
        for issue in config_issues:
            print(f"   - {issue}")
        return

    print("✅ Configuration validated")

    # Get failed workflows
    print("\n📋 Fetching failed workflows...")
    failed_workflows = monitor.get_failed_workflows()

    if not failed_workflows:
        print("✅ No failed workflows found")
    else:
        print(f"⚠️  Found {len(failed_workflows)} failed workflows:")
        for workflow in failed_workflows[:3]:  # Show first 3
            print(f"   - {workflow.workflow_name} (ID: {workflow.id}, Status: {workflow.conclusion})")

    # Check for healing PRs
    print("\n🔧 Checking for existing healing PRs...")
    healing_prs = monitor.get_healing_prs()
    print(f"Found {len(healing_prs)} existing healing PRs")

    print("\n✅ Workflow monitor test completed")

if __name__ == "__main__":
    main()
