# 🤖 Continuous Build Healing System

## Overview

Ja, wir haben Automatisierung! (Yes, we have automation!)

This document describes the automated build healing system that continuously monitors failed builds and applies fixes until they turn green.

## 🎯 Purpose

Addresses the German request:
> "haben wir keine automatisierung, die bei fehlgeschlagenen builds, die fehlerbehebung vornimmt und den build prozess neu startet bis er auf grün läuft."

Translation:
> "Don't we have automation that fixes failed builds and restarts the build process until it runs green?"

## 🔧 How It Works

The system operates in continuous cycles:

1. **Monitor** → Check all workflow runs for failures
2. **Analyze** → Identify error patterns and root causes
3. **Fix** → Apply automated corrections
4. **Restart** → Trigger workflow re-runs
5. **Verify** → Check if fixes worked
6. **Repeat** → Continue until all builds are green

## 📦 Components

### 1. Continuous Build Healer (`continuous_build_healer.py`)
Main orchestration script that runs the healing loop.

**Features:**
- Configurable iteration count and check intervals
- Automatic healing application
- Workflow restart attempts
- Summary reports and logging
- Dry-run mode for testing

**Usage:**
```bash
# Run with default settings (10 iterations, 5 min intervals)
python3 continuous_build_healer.py

# Quick healing (3 iterations, 1 min intervals)
python3 continuous_build_healer.py --max-iterations 3 --check-interval 60

# Patient healing (20 iterations, 10 min intervals)
python3 continuous_build_healer.py --max-iterations 20 --check-interval 600

# Dry run (check only, no fixes)
python3 continuous_build_healer.py --dry-run
```

### 2. Workflow Healing System (`workflow_healing_system.py`)
Intelligent error analysis and fix application.

**Capabilities:**
- Detects LaTeX action version issues
- Fixes missing package problems
- Adjusts timeout settings
- Corrects workflow syntax errors
- Creates PRs for manual review

**Usage:**
```bash
# Run automated healing
python3 workflow_healing_system.py

# Dry run mode
python3 workflow_healing_system.py --dry-run

# Check system status
python3 workflow_healing_system.py --status

# Debug mode
python3 workflow_healing_system.py --debug
```

### 3. Workflow Monitor (`workflow_monitor.py`)
Real-time monitoring of GitHub Actions workflows.

**Features:**
- Fetches failed workflow runs
- Retrieves job logs
- Identifies error patterns
- Tracks workflow status

**Usage:**
```bash
# Monitor recent failures
python3 workflow_monitor.py
```

### 4. PR Merge Resolver (`comprehensive_pr_merge_resolver.py`)
Analyzes and resolves PR merge conflicts.

**Capabilities:**
- Identifies mergeable PRs
- Detects merge conflicts
- Provides resolution strategies
- Auto-resolves simple conflicts

**Usage:**
```bash
# Analyze all open PRs
python3 comprehensive_pr_merge_resolver.py
```

## 🚀 Quick Start

### Option 1: Full Automated Healing
Run the continuous healer for automatic fix application:

```bash
python3 continuous_build_healer.py
```

This will:
1. Check workflow status every 5 minutes
2. Apply healing fixes automatically
3. Attempt to restart failed workflows
4. Continue for up to 10 iterations
5. Stop when all builds are green

### Option 2: One-Time Healing
Apply fixes once without continuous monitoring:

```bash
python3 workflow_healing_system.py
```

### Option 3: PR Analysis Only
Just analyze open PRs without applying changes:

```bash
python3 generate_pr_report.py
```

## 📊 Generated Reports

### PR Analysis Report (`PR_ANALYSIS_REPORT.md`)
Comprehensive report of all open PRs including:
- Merge conflict status
- Direct links to conflicting files
- Workflow failure information
- Resolution recommendations

### Healing Summary (`healing_summary_*.md`)
Summary of each healing session including:
- Number of iterations run
- Successfully healed workflows
- Failed healing attempts
- Overall success rate

## 🎛️ Configuration

### Environment Variables
```bash
export GITHUB_TOKEN="your_github_token"
export GITHUB_REPOSITORY_OWNER="Darkness308"
export GITHUB_REPOSITORY_NAME="CTMM---PDF-in-LaTex"
```

### Healing Config (`healing_config.py`)
Customize healing behavior:
- Error patterns to detect
- Fix strategies to apply
- PR creation settings
- Safety limits and timeouts

## 🔍 Monitoring Workflow Status

### Check Which Workflows Are Failing
```bash
# Method 1: Use workflow monitor
python3 workflow_monitor.py

# Method 2: Check GitHub Actions page
# Visit: https://github.com/Darkness308/CTMM---PDF-in-LaTex/actions

# Method 3: Use PR analysis report
python3 generate_pr_report.py
```

### Identify Failing Branches
The PR analysis report shows:
- Which PR branches have failing workflows
- Which specific workflows are failing
- Direct links to workflow run logs
- Error categories and patterns

## 🛠️ Troubleshooting

### "No failed workflows found"
✅ This is good! It means all builds are green.

### "Healing system timed out"
- Increase timeout in the script
- Check if there are network issues
- Review GitHub Actions status page

### "Could not apply healing fixes"
- Review the error log for specific issues
- Some errors require manual intervention
- Check if GitHub API token has proper permissions

### "Workflow restart failed"
- Workflow restarts require GitHub CLI or API access
- Manual restart: Visit the workflow run page and click "Re-run failed jobs"
- Or use: `gh run rerun <run-id>`

## 📈 Best Practices

### For Continuous Healing
1. **Start with dry-run** to see what will be changed
2. **Use reasonable intervals** (5-10 minutes) to avoid rate limits
3. **Limit iterations** (10-20) to prevent infinite loops
4. **Monitor logs** to ensure fixes are working
5. **Review PRs** created by the healing system

### For PR Management
1. **Close stale PRs** that are no longer relevant
2. **Resolve conflicts** using direct links provided
3. **Fix base branches** for PRs targeting wrong branches
4. **Merge ready PRs** quickly to reduce backlog

### For Workflow Failures
1. **Check logs first** using the direct links
2. **Use automated healing** for common issues
3. **Manual intervention** for complex problems
4. **Document fixes** for future reference

## 🔐 Safety Features

### Automatic Safety Limits
- **Max healing attempts**: 5 per workflow
- **Max concurrent PRs**: 3 healing PRs at once
- **Cooldown period**: 30 minutes between attempts
- **Max iterations**: Configurable (default 10)
- **No direct main branch changes**: All fixes via PR

### What Won't Be Auto-Fixed
❌ Authentication/permission errors  
❌ Complex logic bugs  
❌ Custom action failures  
❌ Fundamental architecture issues  
❌ Manual review required items  

### What Will Be Auto-Fixed
✅ LaTeX action version issues  
✅ Missing package installations  
✅ Timeout configuration  
✅ Workflow syntax errors  
✅ Common CI patterns  

## 📚 Additional Resources

### Documentation
- [Workflow Healing System](WORKFLOW_HEALING_SYSTEM.md) - Detailed healing system docs
- [PR Analysis Report](PR_ANALYSIS_REPORT.md) - Current open PR status
- [Automated PR Merge Workflow](AUTOMATED_PR_MERGE_WORKFLOW.md) - PR merge automation

### Scripts
- `continuous_build_healer.py` - Main continuous healing loop
- `workflow_healing_system.py` - Intelligent fix application
- `workflow_monitor.py` - Workflow status monitoring
- `generate_pr_report.py` - PR analysis report generator
- `analyze_all_open_prs.py` - Detailed PR analysis tool

## 🎯 Success Metrics

Track the effectiveness of the healing system:

1. **Time to Green**: How long until all builds pass
2. **Auto-Fix Rate**: Percentage of issues fixed automatically
3. **Manual Intervention**: Issues requiring human review
4. **PR Backlog**: Number of open PRs over time

## 💡 Next Steps

1. **Review the PR Analysis Report** for current status
2. **Run continuous healer** to fix any failures
3. **Monitor progress** through generated reports
4. **Merge ready PRs** to reduce backlog
5. **Close stale PRs** that are no longer needed

---

**Zusammenfassung auf Deutsch:**

Ja, wir haben eine umfassende Automatisierung für fehlgeschlagene Builds:

- **Kontinuierliche Überwachung** aller Workflows
- **Automatische Fehlerbehebung** durch intelligente Analyse
- **Neustart von Workflows** bis sie grün sind
- **Mehrere Tools** für verschiedene Szenarien
- **Vollständige Dokumentation** und Berichte

Nutze `python3 continuous_build_healer.py` um den automatischen Heilungsprozess zu starten!
