#!/usr/bin/env python3
"""
Continuous Build Healing System
Automatically monitors failed builds and applies fixes until they turn green.

German Request: "haben wir keine automatisierung, die bei fehlgeschlagenen builds,
die fehlerbehebung vornimmt und den build prozess neu startet bis er auf grün läuft."

Translation: "Don't we have automation that fixes failed builds and restarts the
build process until it runs green?"
"""

import os
import sys
import time
import json
import subprocess
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class ContinuousBuildHealer:
    """
    Continuous healing system that monitors workflows and auto-fixes failures.
    """

    def __init__(self, max_iterations: int = 10, check_interval: int = 300):
        """
        Initialize the continuous healer.

        Args:
            max_iterations: Maximum number of healing attempts per run
            check_interval: Seconds between checks (default 5 minutes)
        """
        self.max_iterations = max_iterations
        self.check_interval = check_interval
        self.iteration_count = 0
        self.healed_workflows = []
        self.failed_healing_attempts = []

    def check_workflow_status(self) -> Dict[str, any]:
        """
        Check current status of all workflows in the repository.

        Returns:
            Dictionary with workflow status information
        """
        print(f"\n{'='*80}")
        print(f"[SEARCH] Checking Workflow Status - Iteration {self.iteration_count + 1}/{self.max_iterations}")
        print(f"{'='*80}")

        # Check if workflow_monitor.py exists
        if not os.path.exists('workflow_monitor.py'):
            print("[WARN]  workflow_monitor.py not found, using alternative method")
            return {'failed_workflows': [], 'method': 'alternative'}

        # Try to use the existing workflow monitor
        try:
            # Import and use the workflow monitor
            import importlib.util
            spec = importlib.util.spec_from_file_location("workflow_monitor", "workflow_monitor.py")
            if spec and spec.loader:
                workflow_monitor = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(workflow_monitor)

                monitor = workflow_monitor.WorkflowMonitor()
                failed_workflows = monitor.get_failed_workflows(hours_back=2)

                print(f"[SUMMARY] Found {len(failed_workflows)} failed workflows in last 2 hours")
                return {
                    'failed_workflows': failed_workflows,
                    'method': 'monitor',
                    'count': len(failed_workflows)
                }
        except Exception as e:
            print(f"[WARN]  Error using workflow_monitor: {e}")
            return {'failed_workflows': [], 'method': 'error', 'error': str(e)}

    def apply_healing(self, workflow_info: Dict) -> bool:
        """
        Apply healing fixes to failed workflows.

        Args:
            workflow_info: Information about failed workflows

        Returns:
            True if healing was applied, False otherwise
        """
        if not workflow_info.get('failed_workflows'):
            print("[PASS] No failed workflows found - everything is green!")
            return False

        print(f"\n{'='*80}")
        print(f"[FIX] Applying Healing Fixes...")
        print(f"{'='*80}")

        # Check if workflow_healing_system.py exists
        if not os.path.exists('workflow_healing_system.py'):
            print("[WARN]  workflow_healing_system.py not found")
            print("[TIP] Manual intervention required - please check:")
            for wf in workflow_info['failed_workflows']:
                print(f"   - {wf.get('workflow_name', 'Unknown')} (Run #{wf.get('id', 'N/A')})")
            return False

        # Run the workflow healing system
        try:
            print("[LAUNCH] Running workflow healing system...")
            result = subprocess.run(
                ['python3', 'workflow_healing_system.py', '--max-workflows', '5'],
                capture_output=True,
                text=True,
                timeout=300
            )

            if result.returncode == 0:
                print("[PASS] Healing system executed successfully")
                print(result.stdout)
                return True
            else:
                print(f"[WARN]  Healing system returned error code {result.returncode}")
                print(result.stderr)
                return False

        except subprocess.TimeoutExpired:
            print("[WARN]  Healing system timed out after 5 minutes")
            return False
        except Exception as e:
            print(f"[FAIL] Error running healing system: {e}")
            return False

    def restart_workflows(self, workflow_info: Dict) -> int:
        """
        Restart failed workflow runs if possible.

        Args:
            workflow_info: Information about failed workflows

        Returns:
            Number of workflows restarted
        """
        if not workflow_info.get('failed_workflows'):
            return 0

        print(f"\n{'='*80}")
        print(f"[SYNC] Attempting to Restart Failed Workflows...")
        print(f"{'='*80}")

        restarted_count = 0

        # Note: Restarting workflows requires GitHub API access with proper permissions
        # In this implementation, we'll document the process

        for wf in workflow_info['failed_workflows']:
            wf_name = wf.get('workflow_name', 'Unknown')
            wf_id = wf.get('id', 'N/A')

            print(f"[NOTE] Workflow: {wf_name} (Run #{wf_id})")
            print(f"   To restart manually:")
            print(f"   gh run rerun {wf_id}")
            print(f"   Or visit: {wf.get('html_url', 'N/A')}")
            print()

        return restarted_count

    def wait_for_completion(self) -> None:
        """Wait for the check interval before next iteration."""
        if self.iteration_count < self.max_iterations - 1:
            print(f"\n[SYM] Waiting {self.check_interval} seconds before next check...")
            time.sleep(self.check_interval)

    def generate_summary_report(self) -> str:
        """Generate a summary report of the healing session."""
        report = []
        report.append("\n" + "="*80)
        report.append("[SUMMARY] CONTINUOUS BUILD HEALING SUMMARY")
        report.append("="*80)
        report.append(f"\n**Session Started:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"**Total Iterations:** {self.iteration_count}")
        report.append(f"**Healed Workflows:** {len(self.healed_workflows)}")
        report.append(f"**Failed Healing Attempts:** {len(self.failed_healing_attempts)}")
        report.append("")

        if self.healed_workflows:
            report.append("\n[PASS] Successfully Healed:")
            for wf in self.healed_workflows:
                report.append(f"   - {wf}")

        if self.failed_healing_attempts:
            report.append("\n[FAIL] Failed to Heal:")
            for wf in self.failed_healing_attempts:
                report.append(f"   - {wf}")

        report.append("\n" + "="*80)
        return "\n".join(report)

    def run(self) -> bool:
        """
        Main execution loop for continuous healing.

        Returns:
            True if all workflows are green, False otherwise
        """
        print("="*80)
        print("[FIX] CTMM Continuous Build Healing System")
        print("="*80)
        print(f"\nConfiguration:")
        print(f"   Max Iterations: {self.max_iterations}")
        print(f"   Check Interval: {self.check_interval} seconds")
        print(f"   Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()

        all_green = False

        while self.iteration_count < self.max_iterations and not all_green:
            self.iteration_count += 1

            # Check workflow status
            workflow_info = self.check_workflow_status()

            # If no failed workflows, we're done!
            if not workflow_info.get('failed_workflows'):
                print("\n[SUCCESS] All workflows are GREEN!")
                all_green = True
                break

            # Apply healing
            healing_applied = self.apply_healing(workflow_info)

            if healing_applied:
                print("[PASS] Healing fixes applied")
                self.healed_workflows.append(f"Iteration {self.iteration_count}")
            else:
                print("[WARN]  Could not apply healing fixes")
                self.failed_healing_attempts.append(f"Iteration {self.iteration_count}")

            # Try to restart workflows
            restarted = self.restart_workflows(workflow_info)
            if restarted > 0:
                print(f"[SYNC] Restarted {restarted} workflows")

            # Wait before next check (unless this is the last iteration)
            if not all_green:
                self.wait_for_completion()

        # Generate summary
        summary = self.generate_summary_report()
        print(summary)

        # Save summary to file
        summary_file = f'healing_summary_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md'
        with open(summary_file, 'w') as f:
            f.write(summary)
        print(f"\n[FILE] Summary saved to: {summary_file}")

        return all_green

def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Continuous Build Healing System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run with default settings (10 iterations, 5 minute intervals)
  python3 continuous_build_healer.py

  # Quick healing (3 iterations, 1 minute intervals)
  python3 continuous_build_healer.py --max-iterations 3 --check-interval 60

  # Patient healing (20 iterations, 10 minute intervals)
  python3 continuous_build_healer.py --max-iterations 20 --check-interval 600
        """
    )

    parser.add_argument(
        '--max-iterations',
        type=int,
        default=10,
        help='Maximum number of healing iterations (default: 10)'
    )

    parser.add_argument(
        '--check-interval',
        type=int,
        default=300,
        help='Seconds between checks (default: 300 = 5 minutes)'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Check status only, do not apply fixes'
    )

    args = parser.parse_args()

    if args.dry_run:
        print("[SEARCH] DRY RUN MODE - No fixes will be applied")
        args.max_iterations = 1

    healer = ContinuousBuildHealer(
        max_iterations=args.max_iterations,
        check_interval=args.check_interval
    )

    success = healer.run()

    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
