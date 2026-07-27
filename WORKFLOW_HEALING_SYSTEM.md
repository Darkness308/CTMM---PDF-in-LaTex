# 🔧 CTMM Workflow Healing System

## Overview

The CTMM Workflow Healing System is an automated error analysis and self-healing system for GitHub Actions workflows. It monitors failed workflows, analyzes error logs, applies automated fixes, and creates pull requests for manual review.

## Architecture

### Core Components

1. **`healing_config.py`** - Configuration management and error pattern definitions
2. **`workflow_monitor.py`** - GitHub API integration for monitoring workflow failures
3. **`error_analyzer.py`** - Log analysis and error categorization engine
4. **`fix_strategies.py`** - Automated fix implementations for common errors
5. **`pr_manager.py`** - Pull request creation and management
6. **`workflow_healing_system.py`** - Main orchestration system

### System Flow

```
Failed Workflow Detection → Error Analysis → Fix Strategy Application → PR Creation → Manual Review
```

## Features

### 🔍 **Automated Monitoring**
- Monitors all configured GitHub Actions workflows
- Detects failures in real-time (within configured time window)
- Filters out external repository PRs safely
- Tracks error patterns and frequency

### 🧠 **Intelligent Error Analysis**
- Categorizes errors into solvable patterns:
  - LaTeX action version issues
  - Missing packages
  - Timeout problems
  - Python dependency errors
  - Font/FontAwesome issues
  - Workflow syntax errors
  - Resource limitation issues
- Extracts specific error details for targeted fixes
- Determines solvability based on error patterns

### ⚙️ **Automated Fix Strategies**
- **LaTeX Action Fixes**: Updates to known working versions (v2.3.0)
- **Package Installation**: Adds missing LaTeX packages to workflows
- **Timeout Adjustments**: Increases timeout values intelligently
- **Dependency Upgrades**: Adds upgrade flags to pip installations
- **Font Package Fixes**: Ensures FontAwesome packages are included
- **Syntax Corrections**: Basic YAML workflow syntax fixes

### 🔄 **PR Management**
- Creates descriptive pull requests for each fix attempt
- Includes detailed analysis and recommended changes
- Adds appropriate labels for categorization
- Prevents PR spam with concurrent limits
- Automatic cleanup of stale healing PRs

### 🛡️ **Safety Features**
- Never modifies main branch directly
- Requires manual review for all changes
- Validates fixes before creating PRs
- Respects rate limits and resource constraints
- Stops at unsolvable errors to prevent infinite loops

## Configuration

### Environment Variables

```bash
export GITHUB_TOKEN="your_github_token"
export GITHUB_REPOSITORY_OWNER="your_username"
export GITHUB_REPOSITORY_NAME="your_repo"
```

### Monitored Workflows

By default, monitors these workflow files:
- `latex-build.yml`
- `pr-validation.yml`
- `latex-validation.yml`
- `static.yml`
- `automated-pr-merge-test.yml`
- `test-dante-version.yml`

### Customization

Edit `healing_config.py` to modify:
- Error patterns and categories
- Fix strategy priorities
- PR creation settings
- Safety limits and timeouts

## Usage

### Basic Usage

```bash
# Start automated healing for last 24 hours
python3 workflow_healing_system.py

# Analyze specific time window
python3 workflow_healing_system.py --hours-back 48

# Limit number of workflows processed
python3 workflow_healing_system.py --max-workflows 5
```

### Dry Run Mode

```bash
# Analyze and plan fixes without creating PRs
python3 workflow_healing_system.py --dry-run
```

### System Status

```bash
# Check system status and configuration
python3 workflow_healing_system.py --status
```

### Debug Mode

```bash
# Enable detailed debug logging
python3 workflow_healing_system.py --debug
```

## Error Categories

### 🔴 High Priority (Critical)
- **latex_action_version**: Wrong LaTeX action versions
- **syntax_error**: LaTeX compilation errors
- **github_api_error**: API authentication issues
- **workflow_syntax**: GitHub Actions YAML errors

### 🟡 Medium Priority (Important)
- **package_missing**: Missing LaTeX packages
- **timeout**: Workflow step timeouts
- **dependency_error**: Python package issues
- **font_error**: FontAwesome/font problems

### 🟢 Low Priority (Minor)
- **resource_limit**: System resource constraints

## Fix Strategies

### LaTeX Action Version Fixes
- Detects outdated action versions
- Updates to tested stable versions (v2.3.0)
- Validates workflow syntax after changes

### Package Installation
- Identifies missing LaTeX packages
- Maps package names to texlive distributions
- Adds packages to workflow extra_system_packages

### Timeout Adjustments
- Analyzes timeout patterns
- Increases timeouts by configurable multiplier
- Ensures minimum timeout increases

### Dependency Management
- Adds upgrade flags to pip commands
- Ensures pip itself is upgraded first
- Handles version compatibility issues

## PR Creation

### PR Structure
- **Title**: Descriptive with automated fix prefix
- **Body**: Detailed analysis and applied fixes
- **Labels**: Categorized for easy review
- **Branch**: Timestamped healing branches

### Example PR
```
🔧 Automated Workflow Fix: Fix 2 error categories (5 issues) in latex-build.yml

## 🔧 Automated Workflow Healing

### 📋 Workflow Information
- **Workflow**: latex-build.yml
- **Run ID**: 12345
- **Error Categories**: latex_action_version, package_missing
- **Total Errors**: 5

### ✅ Applied Fixes
1. **Updated LaTeX action versions to v2.3.0**
   - Files modified: `.github/workflows/latex-build.yml`
   - Updated dante-ev/latex-action from v1.0.0 to v2.3.0

2. **Added missing LaTeX packages: texlive-fonts-extra**
   - Files modified: `.github/workflows/latex-build.yml`
   - Added package texlive-fonts-extra
```

## Testing

### Run Test Suite
```bash
# Run comprehensive tests
python3 test_workflow_healing.py

# Test individual components
python3 healing_config.py
python3 error_analyzer.py
python3 fix_strategies.py
```

### Test Coverage
- Configuration validation: 5 tests
- Workflow monitoring: 2 tests
- Error analysis: 3 tests
- Fix strategies: 2 tests
- PR management: 2 tests
- System integration: 2 tests
- **Total: 16 tests**

## Limitations

### What the System CAN Do
✅ Fix common workflow configuration issues
✅ Update action versions automatically
✅ Install missing packages
✅ Adjust timeouts intelligently
✅ Create detailed PRs for review
✅ Validate fixes before applying

### What the System CANNOT Do
❌ Fix complex logic errors in code
❌ Resolve authentication/permission issues
❌ Handle custom or proprietary actions
❌ Merge PRs automatically (safety feature)
❌ Fix fundamental architecture problems

## Safety Mechanisms

### Unsolvable Error Detection
The system stops processing when it encounters:
- Permission denied errors
- Authentication failures
- Rate limit exceeded
- Repository access issues

### Limits and Constraints
- **Max healing attempts**: 5 per workflow
- **Max concurrent PRs**: 3 healing PRs open at once
- **Cooldown period**: 30 minutes between attempts
- **Max iterations**: 10 per execution
- **PR age limit**: 48 hours before automatic cleanup

## Monitoring and Maintenance

### Log Files
- **`workflow_healing.log`**: Detailed execution logs
- **Console output**: Real-time status updates
- **PR descriptions**: Comprehensive change documentation

### Regular Tasks
1. **Review healing PRs**: Check and merge successful fixes
2. **Monitor success rates**: Track system effectiveness
3. **Update error patterns**: Add new error types as needed
4. **Clean up stale branches**: Remove old healing branches

### Performance Metrics
- **Success rate**: Percentage of workflows successfully healed
- **Error coverage**: Types of errors the system can handle
- **Response time**: How quickly fixes are applied
- **PR merge rate**: How often healing PRs are accepted

## Integration with CTMM System

### Existing Tools Integration
- Uses `ctmm_build.py` for validation
- Leverages `validate_*.py` scripts
- Follows existing testing patterns
- Integrates with current CI/CD pipeline

### CTMM-Specific Features
- Handles LaTeX therapeutic document builds
- Manages FontAwesome icon dependencies
- Supports German language content validation
- Maintains PDF generation workflows

## Troubleshooting

### Common Issues

#### "No GitHub token provided"
```bash
export GITHUB_TOKEN="your_personal_access_token"
```

#### "Config validation failed"
Check environment variables and repository settings.

#### "No failed workflows found"
This is normal if all workflows are passing.

#### "Validation failed after fixes"
The system detected the fix might cause new issues.

### Debug Steps
1. Check configuration: `python3 workflow_healing_system.py --status`
2. Run dry run: `python3 workflow_healing_system.py --dry-run`
3. Enable debug logging: `python3 workflow_healing_system.py --debug`
4. Review logs: Check `workflow_healing.log`

## Contributing

### Adding New Error Patterns
1. Update `error_patterns` in `healing_config.py`
2. Add corresponding fix strategy in `fix_strategies.py`
3. Create tests in `test_workflow_healing.py`
4. Update documentation

### Extending Fix Strategies
1. Implement new fix method in `FixStrategies` class
2. Add configuration in `healing_config.py`
3. Update priority ordering
4. Test with dry run mode

## Future Enhancements

### Planned Features
- **Workflow restart automation**: Automatically restart workflows after PR merge
- **Success tracking**: Monitor fix effectiveness over time
- **Machine learning**: Improve error pattern recognition
- **Integration webhooks**: Real-time workflow failure notifications
- **Advanced validation**: More sophisticated fix validation

### Integration Opportunities
- **CI/CD pipeline integration**: Automatic healing in build pipelines
- **Slack/Discord notifications**: Team notifications for healing activities
- **Metrics dashboard**: Visual tracking of healing system performance
- **Custom action marketplace**: Shareable healing strategies

---

*This healing system represents a significant advancement in automated DevOps practices for the CTMM LaTeX documentation system, providing intelligent error resolution while maintaining safety and human oversight.*
