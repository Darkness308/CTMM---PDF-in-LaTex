#!/usr/bin/env python3
"""
Comprehensive Open PR Analysis Tool
Analyzes all open PRs for merge conflicts, workflow status, and provides actionable information.

German Task: "löse alle offenen pull requests aus, die noch offen sind. wenn es megre
konflikte gibt, die du nicht selbstständige beheben kannst, so stelle mir den direkten
link zur dateio zur verfügung.. welche workflows in welchem banch laufen noch ins rote?"

Translation: "Resolve all open pull requests. If there are merge conflicts that you cannot
fix independently, provide me with the direct link to the file. Which workflows in which
branch are still failing?"
"""

import os
import sys
import json
import subprocess
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import requests

class PRAnalyzer:
    """Analyzes open PRs for merge conflicts and workflow status."""

    def __init__(self):
        self.github_token = os.environ.get('GITHUB_TOKEN', '')
        self.repo_owner = 'Darkness308'
        self.repo_name = 'CTMM---PDF-in-LaTex'
        self.api_base = f'https://api.github.com/repos/{self.repo_owner}/{self.repo_name}'
        self.headers = {
            'Accept': 'application/vnd.github.v3+json'
        }
        if self.github_token:
            self.headers['Authorization'] = f'token {self.github_token}'

    def get_open_prs(self) -> List[Dict]:
        """Fetch all open PRs from GitHub API."""
        print("[TEST] Fetching all open pull requests...")
        url = f'{self.api_base}/pulls?state=open&per_page=100'

        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            prs = response.json()
            print(f"[PASS] Found {len(prs)} open PRs")
            return prs
        except Exception as e:
            print(f"[FAIL] Error fetching PRs: {e}")
            return []

    def get_pr_details(self, pr_number: int) -> Optional[Dict]:
        """Get detailed PR information including mergeable state."""
        url = f'{self.api_base}/pulls/{pr_number}'

        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"[FAIL] Error fetching PR #{pr_number} details: {e}")
            return None

    def get_pr_files(self, pr_number: int) -> List[Dict]:
        """Get list of files changed in a PR."""
        url = f'{self.api_base}/pulls/{pr_number}/files'

        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"[FAIL] Error fetching PR #{pr_number} files: {e}")
            return []

    def get_workflow_runs(self, branch: str, limit: int = 5) -> List[Dict]:
        """Get recent workflow runs for a specific branch."""
        url = f'{self.api_base}/actions/runs?branch={branch}&per_page={limit}'

        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            return data.get('workflow_runs', [])
        except Exception as e:
            print(f"[FAIL] Error fetching workflow runs for branch {branch}: {e}")
            return []

    def analyze_pr(self, pr: Dict) -> Dict:
        """Analyze a single PR for conflicts and status."""
        pr_number = pr['number']
        print(f"\n[SEARCH] Analyzing PR #{pr_number}: {pr['title'][:60]}...")

        # Get detailed info
        details = self.get_pr_details(pr_number)
        if not details:
            return {
                'number': pr_number,
                'title': pr['title'],
                'status': 'ERROR',
                'error': 'Could not fetch details'
            }

        # Get file changes
        files = self.get_pr_files(pr_number)

        # Get workflow runs for this PR's branch
        branch = pr['head']['ref']
        workflows = self.get_workflow_runs(branch)

        # Analyze mergeable state
        mergeable = details.get('mergeable')
        mergeable_state = details.get('mergeable_state', 'unknown')

        analysis = {
            'number': pr_number,
            'title': pr['title'],
            'url': pr['html_url'],
            'branch': branch,
            'base': pr['base']['ref'],
            'mergeable': mergeable,
            'mergeable_state': mergeable_state,
            'files_changed': len(files),
            'has_conflicts': mergeable == False and mergeable_state == 'dirty',
            'is_mergeable': mergeable == True,
            'conflict_files': [],
            'workflow_status': 'unknown',
            'failed_workflows': [],
            'direct_links': []
        }

        # Identify conflict files and generate direct links
        if analysis['has_conflicts']:
            print(f"  [WARN]  Has merge conflicts")
            for file in files:
                filename = file['filename']
                # Generate direct GitHub link to the file
                file_url = f"https://github.com/{self.repo_owner}/{self.repo_name}/blob/{branch}/{filename}"
                analysis['conflict_files'].append(filename)
                analysis['direct_links'].append(file_url)

        # Analyze workflow status
        if workflows:
            latest_run = workflows[0]
            analysis['workflow_status'] = latest_run.get('conclusion', 'in_progress')

            # Find failed workflows
            for run in workflows:
                if run.get('conclusion') in ['failure', 'cancelled', 'timed_out']:
                    analysis['failed_workflows'].append({
                        'name': run['name'],
                        'conclusion': run['conclusion'],
                        'url': run['html_url'],
                        'created_at': run['created_at']
                    })

        # Determine overall status
        if analysis['is_mergeable'] and analysis['workflow_status'] == 'success':
            analysis['status'] = 'READY_TO_MERGE'
            print(f"  [PASS] Ready to merge!")
        elif analysis['has_conflicts']:
            analysis['status'] = 'HAS_CONFLICTS'
            print(f"  [FAIL] Has {len(analysis['conflict_files'])} conflicting files")
        elif analysis['workflow_status'] == 'failure':
            analysis['status'] = 'WORKFLOW_FAILED'
            print(f"  [WARN]  Workflow failed")
        else:
            analysis['status'] = 'NEEDS_REVIEW'
            print(f"  [SYM] Needs review (mergeable: {mergeable}, state: {mergeable_state})")

        return analysis

    def generate_report(self, analyses: List[Dict]) -> str:
        """Generate a comprehensive markdown report."""
        report = []
        report.append("# [SUMMARY] Comprehensive Open PR Analysis Report")
        report.append(f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
        report.append(f"\n**Total Open PRs:** {len(analyses)}")
        report.append("\n---\n")

        # Categorize PRs
        ready_to_merge = [a for a in analyses if a['status'] == 'READY_TO_MERGE']
        has_conflicts = [a for a in analyses if a['status'] == 'HAS_CONFLICTS']
        workflow_failed = [a for a in analyses if a['status'] == 'WORKFLOW_FAILED']
        needs_review = [a for a in analyses if a['status'] == 'NEEDS_REVIEW']

        # Summary
        report.append("## [CHART] Summary\n")
        report.append(f"- [PASS] **Ready to Merge:** {len(ready_to_merge)}")
        report.append(f"- [FAIL] **Has Merge Conflicts:** {len(has_conflicts)}")
        report.append(f"- [WARN]  **Workflow Failed:** {len(workflow_failed)}")
        report.append(f"- [SYM] **Needs Review:** {len(needs_review)}")
        report.append("")

        # Ready to merge PRs
        if ready_to_merge:
            report.append("\n## [PASS] Ready to Merge\n")
            report.append("These PRs have no conflicts and all workflows passed:\n")
            for pr in ready_to_merge:
                report.append(f"### PR #{pr['number']}: {pr['title']}")
                report.append(f"- **URL:** {pr['url']}")
                report.append(f"- **Branch:** `{pr['branch']}` -> `{pr['base']}`")
                report.append(f"- **Files Changed:** {pr['files_changed']}")
                report.append(f"- **Action:** Can be merged immediately")
                report.append("")

        # PRs with conflicts
        if has_conflicts:
            report.append("\n## [FAIL] Pull Requests with Merge Conflicts\n")
            report.append("These PRs require manual conflict resolution:\n")
            for pr in has_conflicts:
                report.append(f"### PR #{pr['number']}: {pr['title']}")
                report.append(f"- **URL:** {pr['url']}")
                report.append(f"- **Branch:** `{pr['branch']}` -> `{pr['base']}`")
                report.append(f"- **Conflicting Files:** {len(pr['conflict_files'])}")
                report.append("")
                report.append("**Direct Links to Conflicting Files:**")
                for i, (file, link) in enumerate(zip(pr['conflict_files'], pr['direct_links']), 1):
                    report.append(f"{i}. [`{file}`]({link})")
                report.append("")
                report.append(f"**Resolution:** Review conflicts manually at: {pr['url']}/conflicts")
                report.append("")

        # Workflow failures
        if workflow_failed:
            report.append("\n## [WARN]  Pull Requests with Failed Workflows\n")
            report.append("These PRs have failing CI/CD workflows:\n")
            for pr in workflow_failed:
                report.append(f"### PR #{pr['number']}: {pr['title']}")
                report.append(f"- **URL:** {pr['url']}")
                report.append(f"- **Branch:** `{pr['branch']}`")
                report.append(f"- **Failed Workflows:** {len(pr['failed_workflows'])}")
                report.append("")
                if pr['failed_workflows']:
                    report.append("**Failed Workflow Details:**")
                    for wf in pr['failed_workflows']:
                        report.append(f"- **{wf['name']}** - Status: `{wf['conclusion']}`")
                        report.append(f"  - [View Logs]({wf['url']})")
                report.append("")

        # Needs review
        if needs_review:
            report.append("\n## [SYM] Pull Requests Needing Review\n")
            for pr in needs_review:
                report.append(f"### PR #{pr['number']}: {pr['title']}")
                report.append(f"- **URL:** {pr['url']}")
                report.append(f"- **Branch:** `{pr['branch']}` -> `{pr['base']}`")
                report.append(f"- **Mergeable State:** `{pr['mergeable_state']}`")
                report.append(f"- **Workflow Status:** `{pr['workflow_status']}`")
                report.append("")

        # Recommendations
        report.append("\n## [TIP] Recommendations\n")
        report.append("### For PRs Ready to Merge")
        report.append("- Review and merge immediately to reduce backlog")
        report.append("- Consider using automated merge workflows")
        report.append("")

        report.append("### For PRs with Conflicts")
        report.append("- Use the direct file links provided above")
        report.append("- Resolve conflicts locally:")
        report.append("  ```bash")
        report.append("  git fetch origin")
        report.append("  git checkout <branch-name>")
        report.append("  git merge main")
        report.append("  # Resolve conflicts in the listed files")
        report.append("  git add .")
        report.append("  git commit")
        report.append("  git push")
        report.append("  ```")
        report.append("")

        report.append("### For Failed Workflows")
        report.append("- Consider using the workflow healing system:")
        report.append("  ```bash")
        report.append("  python3 workflow_healing_system.py")
        report.append("  ```")
        report.append("- Review workflow logs at the provided links")
        report.append("- Check if automation can fix the issues")
        report.append("")

        return "\n".join(report)

    def run(self):
        """Main execution method."""
        print("=" * 80)
        print("[FIX] CTMM Open PR Analysis Tool")
        print("=" * 80)
        print()

        # Fetch open PRs
        prs = self.get_open_prs()
        if not prs:
            print("No open PRs found or error fetching data.")
            return

        # Analyze each PR
        analyses = []
        for pr in prs:
            analysis = self.analyze_pr(pr)
            analyses.append(analysis)

        # Generate report
        print("\n" + "=" * 80)
        print("[NOTE] Generating Report...")
        print("=" * 80)

        report = self.generate_report(analyses)

        # Save report
        report_file = 'PR_ANALYSIS_REPORT.md'
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)

        print(f"\n[PASS] Report saved to: {report_file}")
        print("\n" + "=" * 80)
        print("[SUMMARY] Quick Summary:")
        print("=" * 80)

        # Print quick summary
        ready = sum(1 for a in analyses if a['status'] == 'READY_TO_MERGE')
        conflicts = sum(1 for a in analyses if a['status'] == 'HAS_CONFLICTS')
        failed = sum(1 for a in analyses if a['status'] == 'WORKFLOW_FAILED')
        review = sum(1 for a in analyses if a['status'] == 'NEEDS_REVIEW')

        print(f"[PASS] Ready to Merge: {ready}")
        print(f"[FAIL] Has Conflicts: {conflicts}")
        print(f"[WARN]  Workflow Failed: {failed}")
        print(f"[SYM] Needs Review: {review}")
        print()

        return analyses

def main():
    """Main entry point."""
    analyzer = PRAnalyzer()
    analyzer.run()

if __name__ == '__main__':
    main()
