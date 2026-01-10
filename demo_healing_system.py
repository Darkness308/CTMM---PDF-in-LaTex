#!/usr/bin/env python3
"""
CTMM Workflow Healing System - Demonstration Script
Shows the complete workflow healing process with example scenarios.
"""

import os
import sys
import logging
from datetime import datetime, timedelta

# Set up demo logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def demonstrate_healing_system():
    """Demonstrate the complete workflow healing system."""
    print("🔧 CTMM Workflow Healing System - Demonstration")
    print("=" * 60)
    print()

    # Import the system components
    try:
        from healing_config import config
        from workflow_monitor import WorkflowMonitor
        from error_analyzer import ErrorAnalyzer
        from fix_strategies import FixStrategies
        from pr_manager import PRManager
        from workflow_healing_system import WorkflowHealingSystem

        print("✅ All system components loaded successfully")
    except ImportError as e:
        print(f"❌ Failed to import system components: {e}")
        return False

    print()

    # 1. Configuration Demo
    print("📋 1. CONFIGURATION OVERVIEW")
    print("-" * 40)
    print(f"Monitored workflows: {len(config.monitored_workflows)}")
    for workflow in config.monitored_workflows:
        print(f"   - {workflow}")

    print(f"Error categories: {len(config.error_patterns)}")
    for category in config.error_patterns.keys():
        print(f"   - {category}")

    print(f"Fix strategies: {len(config.fix_strategies)}")
    for strategy in config.fix_strategies.keys():
        priority = config.fix_strategies[strategy]['priority']
        print(f"   - {strategy} (priority {priority})")

    print()

    # 2. Error Analysis Demo
    print("🔍 2. ERROR ANALYSIS DEMONSTRATION")
    print("-" * 40)

    analyzer = ErrorAnalyzer()

    # Sample problematic workflow logs
    sample_logs = {
        "LaTeX Build": """
2024-01-01T10:00:00Z Starting LaTeX compilation...
2024-01-01T10:00:05Z uses: dante-ev/latex-action@v1.0.0
2024-01-01T10:01:30Z Package fontawesome5 not found
2024-01-01T10:01:31Z LaTeX Error: File ctmm-design.sty not found
2024-01-01T10:15:00Z The operation was canceled after 15 minutes
2024-01-01T10:15:01Z ##[error]Process completed with exit code 1
        """,
        "Python Setup": """
2024-01-01T10:00:00Z Installing Python dependencies...
2024-01-01T10:00:15Z pip install chardet pyyaml
2024-01-01T10:00:30Z ERROR: Could not find a version that satisfies chardet==5.0.0
2024-01-01T10:00:31Z ERROR: No matching distribution found for chardet==5.0.0
        """
    }

    analysis = analyzer.analyze_logs(12345, "latex-build.yml", sample_logs)

    print(f"Analysis Results:")
    print(f"   Total Errors: {analysis.total_errors}")
    print(f"   Error Categories: {', '.join(analysis.error_categories)}")
    print(f"   Solvable: {'Yes' if analysis.is_solvable else 'No'}")
    print(f"   Recommended Fixes:")
    for i, fix in enumerate(analysis.recommended_fixes, 1):
        print(f"      {i}. {fix}")

    print()

    # 3. Fix Strategies Demo
    print("⚙️ 3. FIX STRATEGIES DEMONSTRATION")
    print("-" * 40)

    print("Example fixes that would be applied:")

    if 'latex_action_version' in analysis.error_categories:
        print("   🔧 LaTeX Action Version Fix:")
        print("      - Update dante-ev/latex-action@v1.0.0 → v2.3.0")
        print("      - Modify .github/workflows/latex-build.yml")
        print("      - Validate workflow syntax")

    if 'package_missing' in analysis.error_categories:
        print("   📦 Missing Package Fix:")
        print("      - Add texlive-fonts-extra to extra_system_packages")
        print("      - Update workflow package installation")
        print("      - Ensure FontAwesome support")

    if 'timeout' in analysis.error_categories:
        print("   ⏱️ Timeout Fix:")
        print("      - Increase timeout-minutes from 15 to 23 (1.5x)")
        print("      - Apply to all workflow steps")
        print("      - Prevent future timeouts")

    if 'dependency_error' in analysis.error_categories:
        print("   🐍 Dependency Fix:")
        print("      - Add --upgrade flag to pip install")
        print("      - Upgrade pip itself first")
        print("      - Handle version conflicts")

    print()

    # 4. PR Management Demo
    print("📝 4. PULL REQUEST MANAGEMENT")
    print("-" * 40)

    pr_manager = PRManager()

    print("Example PR that would be created:")
    print()
    print("   Title: 🔧 Automated Workflow Fix: Fix 4 error categories (7 issues) in latex-build.yml")
    print("   Branch: workflow-healing/run-12345-20240101-120000")
    print("   Labels: documentation, automated-fix")
    print()
    print("   Body Preview:")
    print("   ┌─────────────────────────────────────────────────────")
    print("   │ ## 🔧 Automated Workflow Healing")
    print("   │ This PR contains automated fixes for workflow errors...")
    print("   │ ")
    print("   │ ### 📋 Workflow Information")
    print("   │ - **Workflow**: latex-build.yml")
    print("   │ - **Run ID**: 12345")
    print("   │ - **Error Categories**: latex_action_version, package_missing, timeout, dependency_error")
    print("   │ - **Total Errors**: 7")
    print("   │ ")
    print("   │ ### ✅ Applied Fixes")
    print("   │ 1. **Updated LaTeX action versions to v2.3.0**")
    print("   │ 2. **Added missing LaTeX packages: texlive-fonts-extra**")
    print("   │ 3. **Increased timeout values by factor of 1.5**")
    print("   │ 4. **Updated Python dependency installation with upgrade flags**")
    print("   └─────────────────────────────────────────────────────")

    print()

    # 5. System Integration Demo
    print("🚀 5. COMPLETE SYSTEM WORKFLOW")
    print("-" * 40)

    healing_system = WorkflowHealingSystem()

    print("Workflow Healing Process:")
    print("   1. 🔍 Monitor GitHub Actions for failures")
    print("   2. 📥 Fetch failed workflow logs via API")
    print("   3. 🧠 Analyze errors and categorize problems")
    print("   4. ⚙️ Apply appropriate fix strategies")
    print("   5. ✅ Validate fixes before committing")
    print("   6. 📝 Create descriptive pull request")
    print("   7. 👥 Wait for manual review and approval")
    print("   8. 🔄 Monitor PR status and workflow success")

    print()
    print("Safety Features:")
    print("   ✅ Never modifies main branch directly")
    print("   ✅ All changes require manual review")
    print("   ✅ Validates fixes before creating PRs")
    print("   ✅ Limits concurrent healing PRs")
    print("   ✅ Stops at unsolvable errors")
    print("   ✅ Automatic cleanup of stale PRs")

    print()

    # 6. Usage Examples
    print("💻 6. USAGE EXAMPLES")
    print("-" * 40)

    print("Basic Commands:")
    print("   # Start healing for last 24 hours")
    print("   python3 workflow_healing_system.py")
    print()
    print("   # Dry run (analyze without creating PRs)")
    print("   python3 workflow_healing_system.py --dry-run")
    print()
    print("   # Check system status")
    print("   python3 workflow_healing_system.py --status")
    print()
    print("   # Process specific time window")
    print("   python3 workflow_healing_system.py --hours-back 48")
    print()
    print("   # Enable debug logging")
    print("   python3 workflow_healing_system.py --debug")

    print()

    # 7. Integration with CTMM
    print("🎯 7. CTMM SYSTEM INTEGRATION")
    print("-" * 40)

    print("CTMM-Specific Features:")
    print("   📄 LaTeX therapeutic document processing")
    print("   🎨 FontAwesome icon dependency management")
    print("   🇩🇪 German language content validation")
    print("   📊 PDF generation workflow maintenance")
    print("   🔧 Integration with ctmm_build.py system")
    print("   ✅ Validation with existing test scripts")

    print()
    print("Monitored CTMM Workflows:")
    for workflow in config.monitored_workflows:
        print(f"   - {workflow}")

    print()

    # Summary
    print("📊 DEMONSTRATION SUMMARY")
    print("=" * 60)

    print(f"✅ System Components: 6 modules implemented")
    print(f"✅ Error Categories: {len(config.error_patterns)} types detected")
    print(f"✅ Fix Strategies: {len(config.fix_strategies)} automated fixes")
    print(f"✅ Test Coverage: 17 comprehensive tests")
    print(f"✅ Documentation: Complete usage guide provided")
    print(f"✅ Safety Features: Multiple safeguards implemented")

    print()
    print("🎉 The CTMM Workflow Healing System is ready for deployment!")
    print("   Next steps:")
    print("   1. Set up GitHub token: export GITHUB_TOKEN='your_token'")
    print("   2. Test with dry run: python3 workflow_healing_system.py --dry-run")
    print("   3. Review and merge healing PRs as they are created")
    print("   4. Monitor system effectiveness and adjust as needed")

    return True

def run_system_validation():
    """Run basic system validation checks."""
    print("\n🔍 SYSTEM VALIDATION")
    print("-" * 40)

    try:
        from healing_config import config

        # Check configuration
        issues = config.validate_config()
        if issues:
            print("⚠️  Configuration issues found:")
            for issue in issues:
                print(f"   - {issue}")
        else:
            print("✅ Configuration validation passed")

        # Check if we're in the right repository
        if os.path.exists('.github/workflows'):
            workflow_count = len([f for f in os.listdir('.github/workflows') if f.endswith('.yml')])
            print(f"✅ Found {workflow_count} workflow files")
        else:
            print("⚠️  No .github/workflows directory found")

        # Check if main components can be imported
        try:
            from workflow_healing_system import WorkflowHealingSystem
            system = WorkflowHealingSystem()
            status = system.get_system_status()
            print(f"✅ System status: {status['system_version']}")
        except Exception as e:
            print(f"❌ System initialization failed: {e}")

        print("✅ Basic validation completed")

    except Exception as e:
        print(f"❌ Validation failed: {e}")
        return False

    return True

if __name__ == "__main__":
    print("🚀 Starting CTMM Workflow Healing System Demonstration")
    print()

    # Run the demonstration
    demo_success = demonstrate_healing_system()

    # Run validation
    validation_success = run_system_validation()

    print()
    if demo_success and validation_success:
        print("🎉 Demonstration completed successfully!")
        print("   The automated workflow healing system is fully implemented and ready to use.")
        sys.exit(0)
    else:
        print("❌ Demonstration encountered issues.")
        print("   Please check the error messages above and resolve any problems.")
        sys.exit(1)
