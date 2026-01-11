#!/usr/bin/env python3
"""
Generate PR Analysis Report from Known Data
Uses the PR data already fetched to generate a comprehensive report.
"""

from datetime import datetime
from typing import List, Dict

# PR data from the GitHub API call we made earlier
OPEN_PRS = [
    {
        "number": 1189,
        "title": "löse alle offenen pull requests aus, die noch offen sind...",
        "state": "open",
        "html_url": "https://github.com/Darkness308/CTMM---PDF-in-LaTex/pull/1189",
        "head": {"ref": "copilot/fix-ef8fabe7-9c91-4cbc-940a-7f895afc77dc"},
        "base": {"ref": "main"},
        "draft": True,
        "mergeable_estimate": None,  # Current PR, status unknown
    },
    {
        "number": 572,
        "title": "Copilot/fix 314",
        "state": "open",
        "html_url": "https://github.com/Darkness308/CTMM---PDF-in-LaTex/pull/572",
        "head": {"ref": "copilot/fix-314"},
        "base": {"ref": "main"},
        "draft": False,
        "created_at": "2025-08-14T21:05:52Z",
        "mergeable_estimate": False,  # Old PR, likely has conflicts
    },
    {
        "number": 571,
        "title": "Copilot/fix 237",
        "state": "open",
        "html_url": "https://github.com/Darkness308/CTMM---PDF-in-LaTex/pull/571",
        "head": {"ref": "copilot/fix-237"},
        "base": {"ref": "main"},
        "draft": False,
        "created_at": "2025-08-14T20:58:59Z",
        "mergeable_estimate": False,
    },
    {
        "number": 569,
        "title": "Copilot/fix 8ae4eff1 3cf9 43fa b99a 6583150d5789",
        "state": "open",
        "html_url": "https://github.com/Darkness308/CTMM---PDF-in-LaTex/pull/569",
        "head": {"ref": "copilot/fix-8ae4eff1-3cf9-43fa-b99a-6583150d5789"},
        "base": {"ref": "main"},
        "draft": False,
        "created_at": "2025-08-14T20:28:05Z",
        "mergeable_estimate": False,
    },
    {
        "number": 555,
        "title": "Copilot/fix 300",
        "state": "open",
        "html_url": "https://github.com/Darkness308/CTMM---PDF-in-LaTex/pull/555",
        "head": {"ref": "copilot/fix-300"},
        "base": {"ref": "main"},
        "draft": False,
        "created_at": "2025-08-14T16:26:12Z",
        "mergeable_estimate": False,
    },
    {
        "number": 489,
        "title": "Fix CI workflow: resolve LaTeX package naming issue causing build failures",
        "state": "open",
        "html_url": "https://github.com/Darkness308/CTMM---PDF-in-LaTex/pull/489",
        "head": {"ref": "copilot/fix-488"},
        "base": {"ref": "copilot/fix-99"},  # Note: Not targeting main!
        "draft": False,
        "created_at": "2025-08-14T00:26:19Z",
        "mergeable_estimate": False,
    },
    {
        "number": 423,
        "title": "Fix CI workflow: correct LaTeX package names for German support",
        "state": "open",
        "html_url": "https://github.com/Darkness308/CTMM---PDF-in-LaTex/pull/423",
        "head": {"ref": "copilot/fix-422"},
        "base": {"ref": "copilot/fix-8ae4eff1-3cf9-43fa-b99a-6583150d5789"},  # Not targeting main!
        "draft": False,
        "created_at": "2025-08-13T13:52:17Z",
        "mergeable_estimate": False,
    },
    {
        "number": 307,
        "title": "Fix LaTeX syntax error: Add missing backslash to \\textcolor command",
        "state": "open",
        "html_url": "https://github.com/Darkness308/CTMM---PDF-in-LaTex/pull/307",
        "head": {"ref": "copilot/fix-306"},
        "base": {"ref": "main"},
        "draft": False,
        "created_at": "2025-08-09T14:47:17Z",
        "mergeable_estimate": False,
    },
    {
        "number": 232,
        "title": "Fix YAML syntax error in LaTeX build workflow",
        "state": "open",
        "html_url": "https://github.com/Darkness308/CTMM---PDF-in-LaTex/pull/232",
        "head": {"ref": "copilot/fix-231"},
        "base": {"ref": "main"},
        "draft": False,
        "created_at": "2025-08-09T10:45:08Z",
        "mergeable_estimate": False,
    },
    {
        "number": 3,
        "title": "Implement comprehensive LaTeX build and document conversion workflows",
        "state": "open",
        "html_url": "https://github.com/Darkness308/CTMM---PDF-in-LaTex/pull/3",
        "head": {"ref": "copilot/fix-fa98ffd6-ed8d-467a-826d-fe622b120467"},
        "base": {"ref": "main"},
        "draft": False,
        "created_at": "2025-08-06T03:10:14Z",
        "mergeable_estimate": False,
    },
]

def generate_report():
    """Generate comprehensive PR analysis report."""

    report = []
    report.append("# [SUMMARY] Comprehensive Open PR Analysis Report")
    report.append(f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    report.append(f"\n**Total Open PRs:** {len(OPEN_PRS)}")
    report.append("\n---\n")

    # Categorize PRs
    draft_prs = [pr for pr in OPEN_PRS if pr.get('draft', False)]
    non_main_base = [pr for pr in OPEN_PRS if pr['base']['ref'] != 'main']
    old_prs = [pr for pr in OPEN_PRS if pr.get('created_at', '2025-08-14') < '2025-08-10']

    report.append("## [CHART] Summary\n")
    report.append(f"- [RED] **Total Open PRs:** {len(OPEN_PRS)}")
    report.append(f"- [NOTE] **Draft PRs:** {len(draft_prs)}")
    report.append(f"- [WARN]  **PRs Not Targeting Main:** {len(non_main_base)}")
    report.append(f"- [TIME] **Old PRs (>2 months):** {len(old_prs)}")
    report.append("")

    report.append("## [SEARCH] Detailed Analysis\n")
    report.append("### Key Issues Identified\n")
    report.append("1. **Many PRs are very old** (from August 2025) - likely have merge conflicts with current main")
    report.append("2. **Some PRs target other feature branches** instead of main - these need special handling")
    report.append("3. **PR chain issues** - Some PRs depend on other PRs being merged first")
    report.append("")

    report.append("## [TEST] All Open Pull Requests\n")

    for i, pr in enumerate(OPEN_PRS, 1):
        report.append(f"### {i}. PR #{pr['number']}: {pr['title']}")
        report.append(f"- **URL:** {pr['html_url']}")
        report.append(f"- **Branch:** `{pr['head']['ref']}` -> `{pr['base']['ref']}`")
        if pr.get('created_at'):
            report.append(f"- **Created:** {pr['created_at']}")
        if pr.get('draft'):
            report.append(f"- **Status:** [EMOJI] DRAFT")
        if pr['base']['ref'] != 'main':
            report.append(f"- **[WARN]  Warning:** Targets `{pr['base']['ref']}` instead of `main`")
        report.append("")

        # Provide direct links for conflict resolution
        report.append(f"**Direct Links:**")
        report.append(f"- [View PR]({pr['html_url']})")
        report.append(f"- [View Files Changed]({pr['html_url']}/files)")
        report.append(f"- [View Conflicts (if any)]({pr['html_url']}/conflicts)")
        report.append(f"- [View Commits]({pr['html_url']}/commits)")
        report.append("")

    report.append("\n## [WARN]  Special Cases\n")

    if non_main_base:
        report.append("### PRs Not Targeting Main Branch\n")
        report.append("These PRs target other feature branches and may need to be rebased:\n")
        for pr in non_main_base:
            report.append(f"- **PR #{pr['number']}**: `{pr['head']['ref']}` -> `{pr['base']['ref']}`")
            report.append(f"  - [Change base branch]({pr['html_url']})")
        report.append("")

    report.append("\n## [TIP] Recommendations\n")
    report.append("### Immediate Actions\n")
    report.append("1. **Close stale/duplicate PRs** - Many of these PRs are 2+ months old")
    report.append("2. **Fix base branches** - Update PRs #489 and #423 to target `main`")
    report.append("3. **Resolve merge conflicts** - Use the direct links above to access conflict resolution")
    report.append("4. **Test workflow automation** - Run the workflow healing system:")
    report.append("   ```bash")
    report.append("   python3 workflow_healing_system.py")
    report.append("   ```")
    report.append("")

    report.append("### For Merge Conflict Resolution\n")
    report.append("Use this command pattern for each PR:")
    report.append("```bash")
    report.append("# For each PR branch:")
    report.append("git fetch origin")
    report.append("git checkout <branch-name>")
    report.append("git merge origin/main")
    report.append("# If conflicts:")
    report.append("#   1. Click the 'View Conflicts' link above")
    report.append("#   2. Resolve conflicts in GitHub web editor")
    report.append("#   3. Or resolve locally and push")
    report.append("```")
    report.append("")

    report.append("### Workflow Failure Analysis\n")
    report.append("To check which workflows are failing:\n")
    report.append("1. Visit each PR's 'Checks' tab")
    report.append("2. Look for red [FAIL] indicators")
    report.append("3. Click on failed checks to see logs")
    report.append("4. Common issues:")
    report.append("   - LaTeX package errors")
    report.append("   - Merge conflicts")
    report.append("   - Timeout issues")
    report.append("   - GitHub Actions configuration")
    report.append("")

    report.append("\n## [EMOJI] Automated Healing System\n")
    report.append("The repository already has a workflow healing system:")
    report.append("")
    report.append("### Check Workflow Status")
    report.append("```bash")
    report.append("python3 workflow_monitor.py")
    report.append("```")
    report.append("")
    report.append("### Run Automated Healing")
    report.append("```bash")
    report.append("python3 workflow_healing_system.py --dry-run  # Test mode")
    report.append("python3 workflow_healing_system.py            # Apply fixes")
    report.append("```")
    report.append("")
    report.append("### Merge PR Analysis")
    report.append("```bash")
    report.append("python3 comprehensive_pr_merge_resolver.py")
    report.append("```")
    report.append("")

    report.append("\n## [TARGET] Action Items\n")
    report.append("- [ ] Review each PR using the direct links above")
    report.append("- [ ] Close PRs that are no longer relevant")
    report.append("- [ ] Update base branches for PRs #489 and #423")
    report.append("- [ ] Resolve merge conflicts using GitHub web interface")
    report.append("- [ ] Run workflow healing system to fix CI failures")
    report.append("- [ ] Merge PRs that are ready")
    report.append("")

    return "\n".join(report)

def main():
    """Main execution."""
    print("=" * 80)
    print("[SUMMARY] Generating PR Analysis Report...")
    print("=" * 80)
    print()

    report = generate_report()

    # Save report
    report_file = 'PR_ANALYSIS_REPORT.md'
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"[PASS] Report generated: {report_file}")
    print()
    print("[TEST] Quick Summary:")
    print(f"   Total Open PRs: {len(OPEN_PRS)}")
    print(f"   Draft PRs: {sum(1 for pr in OPEN_PRS if pr.get('draft'))}")
    print(f"   PRs Not Targeting Main: {sum(1 for pr in OPEN_PRS if pr['base']['ref'] != 'main')}")
    print()
    print("[TIP] Next Steps:")
    print("   1. Review the generated report: PR_ANALYSIS_REPORT.md")
    print("   2. Use the direct links to resolve conflicts")
    print("   3. Run workflow healing system if needed")
    print()

if __name__ == '__main__':
    main()
