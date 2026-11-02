#!/usr/bin/env python3
"""
Workflow Healing System - Main Orchestration
Main system that orchestrates the automated workflow error analysis and healing process.
"""

import sys
import os
import time
import logging
import argparse
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

from healing_config import config
from workflow_monitor import WorkflowMonitor, WorkflowRun
from error_analyzer import ErrorAnalyzer, ErrorAnalysis
from fix_strategies import FixStrategies, FixResult
from pr_manager import PRManager, HealingPR

@dataclass
class HealingSession:
    """Represents a complete healing session."""
    session_id: str
    start_time: datetime
    workflow_runs_analyzed: int
    errors_found: int
    fixes_applied: int
    prs_created: int
    success_rate: float
    status: str  # 'running', 'completed', 'failed', 'stopped'

class WorkflowHealingSystem:
    """Main orchestration system for automated workflow healing."""

    def __init__(self, debug: bool = False):
        # Set up logging
        log_level = logging.DEBUG if debug else getattr(logging, config.log_level)
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(config.log_file),
                logging.StreamHandler()
            ]
        )

        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing Workflow Healing System")

        # Initialize components
        self.monitor = WorkflowMonitor()
        self.analyzer = ErrorAnalyzer()
        self.fix_strategies = FixStrategies()
        self.pr_manager = PRManager()

        # Session tracking
        self.current_session: Optional[HealingSession] = None
        self.healing_history: List[HealingSession] = []

        # Safety limits
        self.max_iterations = config.max_iterations_per_run
        self.iteration_count = 0

    def start_healing_session(self,
                            hours_back: int = None,
                            dry_run: bool = False,
                            max_workflows: int = None) -> HealingSession:
        """Start a new healing session."""
        if hours_back is None:
            hours_back = config.max_workflow_age_hours

        session_id = f"healing-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

        self.current_session = HealingSession(
            session_id=session_id,
            start_time=datetime.now(),
            workflow_runs_analyzed=0,
            errors_found=0,
            fixes_applied=0,
            prs_created=0,
            success_rate=0.0,
            status='running'
        )

        self.logger.info(f"Starting healing session: {session_id}")
        self.logger.info(f"Parameters: hours_back={hours_back}, dry_run={dry_run}, max_workflows={max_workflows}")

        try:
            # Validate configuration
            self._validate_environment()

            # Clean up stale PRs first
            self._cleanup_stale_prs()

            # Get failed workflows
            failed_workflows = self._get_failed_workflows(hours_back, max_workflows)

            if not failed_workflows:
                self.logger.info("No failed workflows found")
                self.current_session.status = 'completed'
                return self.current_session

            # Process each failed workflow
            for workflow in failed_workflows:
                if self.iteration_count >= self.max_iterations:
                    self.logger.warning(f"Reached maximum iterations ({self.max_iterations})")
                    break

                try:
                    self._heal_workflow(workflow, dry_run)
                    self.iteration_count += 1

                    # Add delay between workflows to avoid overwhelming the system
                    if not dry_run:
                        time.sleep(30)

                except Exception as e:
                    self.logger.error(f"Error healing workflow {workflow.workflow_name}: {e}")
                    continue

            # Calculate success rate
            if self.current_session.workflow_runs_analyzed > 0:
                self.current_session.success_rate = (
                    self.current_session.fixes_applied /
                    self.current_session.workflow_runs_analyzed
                )

            self.current_session.status = 'completed'
            self.logger.info(f"Healing session completed: {self._get_session_summary()}")

        except Exception as e:
            self.logger.error(f"Healing session failed: {e}")
            self.current_session.status = 'failed'
            raise

        finally:
            self.healing_history.append(self.current_session)

        return self.current_session

    def _validate_environment(self) -> None:
        """Validate the environment is ready for healing operations."""
        self.logger.info("Validating environment...")

        # Check configuration
        config_issues = config.validate_config()
        if config_issues:
            raise RuntimeError(f"Configuration issues: {', '.join(config_issues)}")

        # Check if we're in a git repository
        try:
            import subprocess
            result = subprocess.run(['git', 'rev-parse', '--git-dir'],
                                  capture_output=True, check=True)
            self.logger.info("Git repository validated")
        except subprocess.CalledProcessError:
            raise RuntimeError("Not in a git repository")

        # Check GitHub API access
        try:
            healing_prs = self.pr_manager._get_open_healing_prs()
            self.logger.info(f"GitHub API access validated ({len(healing_prs)} healing PRs found)")
        except Exception as e:
            self.logger.warning(f"GitHub API access limited: {e}")

    def _cleanup_stale_prs(self) -> None:
        """Clean up stale healing pull requests."""
        self.logger.info("Cleaning up stale healing PRs...")

        try:
            closed_prs = self.pr_manager.close_stale_healing_prs(max_age_hours=48)
            if closed_prs:
                self.logger.info(f"Closed {len(closed_prs)} stale healing PRs")
            else:
                self.logger.info("No stale healing PRs found")
        except Exception as e:
            self.logger.error(f"Failed to cleanup stale PRs: {e}")

    def _get_failed_workflows(self, hours_back: int, max_workflows: Optional[int]) -> List[WorkflowRun]:
        """Get failed workflows to process."""
        self.logger.info(f"Fetching failed workflows from last {hours_back} hours...")

        failed_workflows = self.monitor.get_failed_workflows(hours_back)

        if max_workflows and len(failed_workflows) > max_workflows:
            self.logger.info(f"Limiting to {max_workflows} most recent workflows")
            failed_workflows = failed_workflows[:max_workflows]

        self.logger.info(f"Found {len(failed_workflows)} failed workflows to process")
        return failed_workflows

    def _heal_workflow(self, workflow: WorkflowRun, dry_run: bool) -> bool:
        """Heal a single failed workflow."""
        self.logger.info(f"Healing workflow: {workflow.workflow_name} (ID: {workflow.id})")

        try:
            # Update session stats
            self.current_session.workflow_runs_analyzed += 1

            # Get workflow logs
            job_logs = self.monitor.get_workflow_run_logs(workflow.id)
            if not job_logs:
                self.logger.warning(f"No logs found for workflow {workflow.id}")
                return False

            # Analyze errors
            analysis = self.analyzer.analyze_logs(workflow.id, workflow.workflow_name, job_logs)
            self.current_session.errors_found += analysis.total_errors

            self.logger.info(f"Analysis: {analysis.total_errors} errors in {len(analysis.error_categories)} categories")
            self.logger.info(f"Error categories: {', '.join(analysis.error_categories)}")
            self.logger.info(f"Solvable: {analysis.is_solvable}")

            if not analysis.is_solvable:
                self.logger.warning("Analysis indicates errors are not automatically solvable")
                return False

            if not analysis.error_categories:
                self.logger.warning("No error categories identified")
                return False

            # Apply fix strategies
            fix_results = self.fix_strategies.apply_fixes(analysis)

            successful_fixes = [r for r in fix_results if r.success]
            if not successful_fixes:
                self.logger.warning("No successful fixes could be applied")
                return False

            self.logger.info(f"Applied {len(successful_fixes)} successful fixes")
            self.current_session.fixes_applied += len(successful_fixes)

            if dry_run:
                self.logger.info("DRY RUN: Would create PR for fixes")
                self._log_dry_run_summary(analysis, fix_results)
                return True

            # Create pull request for fixes
            healing_pr = self.pr_manager.create_healing_pr(analysis, fix_results)
            if healing_pr:
                self.current_session.prs_created += 1
                self.logger.info(f"Created healing PR #{healing_pr.number}: {healing_pr.url}")

                # Monitor the PR and restart workflow if merged
                self._monitor_healing_pr(healing_pr, workflow)
                return True
            else:
                self.logger.error("Failed to create healing PR")
                return False

        except Exception as e:
            self.logger.error(f"Error healing workflow {workflow.workflow_name}: {e}")
            return False

    def _log_dry_run_summary(self, analysis: ErrorAnalysis, fix_results: List[FixResult]) -> None:
        """Log a summary for dry run mode."""
        self.logger.info("=== DRY RUN SUMMARY ===")
        self.logger.info(f"Workflow: {analysis.workflow_name}")
        self.logger.info(f"Errors: {analysis.total_errors} in categories: {', '.join(analysis.error_categories)}")

        for i, result in enumerate(fix_results, 1):
            status = "[PASS]" if result.success else "[FAIL]"
            self.logger.info(f"Fix {i}: {status} {result.description}")
            if result.files_modified:
                self.logger.info(f"   Files: {', '.join(result.files_modified)}")

        self.logger.info("=== END DRY RUN ===")

    def _monitor_healing_pr(self, healing_pr: HealingPR, original_workflow: WorkflowRun) -> None:
        """Monitor a healing PR and restart workflow when appropriate."""
        self.logger.info(f"Monitoring healing PR #{healing_pr.number}")

        # For now, just log the PR creation
        # In a full implementation, this could:
        # 1. Wait for PR to be merged
        # 2. Restart the original workflow
        # 3. Monitor the restarted workflow for success
        # 4. Create follow-up PRs if needed

        self.logger.info(f"Healing PR created for workflow {original_workflow.workflow_name}")
        self.logger.info(f"Manual review and merge required: {healing_pr.url}")

    def _get_session_summary(self) -> str:
        """Get a summary of the current healing session."""
        if not self.current_session:
            return "No active session"

        duration = datetime.now() - self.current_session.start_time

        summary = [
            f"Session: {self.current_session.session_id}",
            f"Duration: {duration}",
            f"Workflows analyzed: {self.current_session.workflow_runs_analyzed}",
            f"Errors found: {self.current_session.errors_found}",
            f"Fixes applied: {self.current_session.fixes_applied}",
            f"PRs created: {self.current_session.prs_created}",
            f"Success rate: {self.current_session.success_rate:.1%}",
            f"Status: {self.current_session.status}"
        ]

        return " | ".join(summary)

    def get_system_status(self) -> Dict:
        """Get the current status of the healing system."""
        status = {
            'system_version': '1.0.0',
            'config_valid': len(config.validate_config()) == 0,
            'monitored_workflows': config.monitored_workflows,
            'current_session': self.current_session.__dict__ if self.current_session else None,
            'total_sessions': len(self.healing_history),
            'last_run': self.healing_history[-1].__dict__ if self.healing_history else None
        }

        return status

def main():
    """Main entry point for the workflow healing system."""
    parser = argparse.ArgumentParser(description='CTMM Workflow Healing System')
    parser.add_argument('--hours-back', type=int, default=24,
                       help='How many hours back to look for failed workflows (default: 24)')
    parser.add_argument('--max-workflows', type=int,
                       help='Maximum number of workflows to process')
    parser.add_argument('--dry-run', action='store_true',
                       help='Analyze and plan fixes without creating PRs')
    parser.add_argument('--debug', action='store_true',
                       help='Enable debug logging')
    parser.add_argument('--status', action='store_true',
                       help='Show system status and exit')

    args = parser.parse_args()

    # Create healing system
    healing_system = WorkflowHealingSystem(debug=args.debug)

    if args.status:
        status = healing_system.get_system_status()
        print("[FIX] CTMM Workflow Healing System Status")
        print("=" * 50)
        print(f"System Version: {status['system_version']}")
        print(f"Config Valid: {'[PASS]' if status['config_valid'] else '[FAIL]'}")
        print(f"Monitored Workflows: {len(status['monitored_workflows'])}")

        if status['current_session']:
            print(f"Current Session: {status['current_session']['session_id']}")
            print(f"Session Status: {status['current_session']['status']}")
        else:
            print("Current Session: None")

        if status['last_run']:
            print(f"Last Run: {status['last_run']['session_id']}")
            print(f"Last Success Rate: {status['last_run']['success_rate']:.1%}")

        return

    # Start healing session
    print("[LAUNCH] Starting CTMM Workflow Healing System")
    print("=" * 50)

    try:
        session = healing_system.start_healing_session(
            hours_back=args.hours_back,
            dry_run=args.dry_run,
            max_workflows=args.max_workflows
        )

        print("\n[PASS] Healing session completed successfully")
        print(f"[SUMMARY] Results: {healing_system._get_session_summary()}")

        if session.prs_created > 0:
            print(f"\n[EMOJI] Created {session.prs_created} healing PRs")
            print("   Please review and merge the PRs to apply the fixes")

        return 0

    except KeyboardInterrupt:
        print("\n[SYM]  Healing session interrupted by user")
        if healing_system.current_session:
            healing_system.current_session.status = 'stopped'
        return 1

    except Exception as e:
        print(f"\n[FAIL] Healing session failed: {e}")
        healing_system.logger.exception("Healing session failed")
        return 1

if __name__ == "__main__":
    exit(main())
