# Automated PR Merge and Build Testing Workflow

## Overview

The **Automated PR Merge and Build Testing** workflow provides a comprehensive solution for testing the integration of all open pull requests without affecting the main branch. This workflow creates a temporary test branch, merges all open PRs sequentially, and runs build validation after each merge.

## Robustness and Reliability

### 🛡️ **Enhanced Error Handling**
- **HTTP Response Validation**: All GitHub API calls include HTTP status code checking
- **Tool Validation**: Verifies that required tools (git, jq, curl) are available before execution
- **Rate Limiting Protection**: Includes delays between API calls to prevent rate limiting
- **Detailed Error Logging**: All operations include timestamps and comprehensive error details
- **Graceful Failure Handling**: Continues processing other PRs even when individual PRs fail

### 🔧 **Dependency Management**
- **Explicit Dependencies**: Automatically installs jq and curl to ensure availability
- **Python Dependencies**: Installs required Python packages (chardet, requests)
- **Tool Verification**: Validates all required command-line tools before proceeding

### 📊 **Enhanced Logging**
- **Timestamped Logs**: All log entries include timestamps for better debugging
- **Structured Output**: Separate log files for fetch, merge, build, and conflict operations
- **Error Context**: Detailed context information for all failures
- **Progress Tracking**: Clear progress indicators throughout the workflow

## Features

### 🔄 **Automated PR Processing**
- Discovers all open pull requests automatically
- Creates isolated test branches for safe testing
- Merges PRs sequentially to identify integration issues
- Handles merge conflicts gracefully without interruption

### 🏗️ **Comprehensive Build Testing**
- Runs CTMM build system validation after each merge
- Executes LaTeX syntax validation
- Performs enhanced build management checks
- Attempts full PDF generation for final validation
- Includes robust error handling and timeout protection
- Detailed logging with timestamps for all operations

### 📊 **Detailed Reporting**
- Generates comprehensive test result summaries
- Tracks successful and failed merges/builds
- Provides individual PR analysis logs
- Creates actionable recommendations for manual review

### 🔒 **Safe Operation**
- Never modifies the main branch directly
- Works only on temporary test branches
- Includes automatic cleanup after completion
- Handles external repository PRs safely
- Validates all required tools before execution
- Includes rate limiting protection for API calls
- Enhanced error handling with detailed logging and timestamps

## Usage

### Manual Execution

The workflow can be triggered manually through GitHub Actions:

1. Go to **Actions** tab in the repository
2. Select **Automated PR Merge and Build Testing**
3. Click **Run workflow**
4. Configure options:
   - **Base branch**: Branch to merge PRs into (default: `main`)
   - **Max PRs**: Maximum number of PRs to test (default: `10`)
   - **Cleanup branch**: Delete test branch after completion (default: `true`)

### Scheduled Execution

The workflow automatically runs:
- **Weekly on Sundays at 2 AM UTC**
- Processes all open PRs with default settings

### Input Parameters

| Parameter | Description | Default | Type |
|-----------|-------------|---------|------|
| `base_branch` | Base branch to merge PRs into | `main` | string |
| `max_prs` | Maximum number of PRs to test (0 = all) | `10` | string |
| `cleanup_branch` | Delete test branch after completion | `true` | boolean |

## Workflow Process

### 1. **Initialization**
```mermaid
graph LR
    A[Checkout Repository] --> B[Setup Python]
    B --> C[Install Dependencies]
    C --> D[Configure Git]
```

### 2. **Test Branch Creation**
- Creates uniquely named test branch: `automated-merge-test-YYYYMMDD-HHMMSS`
- Based on specified base branch (default: `main`)
- Pushes test branch to remote repository

### 3. **PR Discovery and Processing**
```mermaid
graph TD
    A[Fetch Open PRs] --> B{For Each PR}
    B --> C[Check Repository Source]
    C --> D{Same Repo?}
    D -->|Yes| E[Fetch PR Branch]
    D -->|No| F[Skip External PR]
    E --> G[Attempt Merge]
    G --> H{Merge Success?}
    H -->|Yes| I[Run Build Tests]
    H -->|No| J[Log Conflict]
    I --> K[Record Results]
    J --> K
    F --> K
    K --> L{More PRs?}
    L -->|Yes| B
    L -->|No| M[Final Build Test]
```

### 4. **Build Testing Sequence**

For each successfully merged PR:
1. **CTMM Build System Check** (`ctmm_build.py`)
2. **LaTeX Syntax Validation** (`validate_latex_syntax.py`)
3. **Result Logging** (individual PR logs)

After all PR processing:
1. **Final Combined Build Test**
2. **Enhanced Build Management**
3. **PDF Generation Attempt** (with LaTeX)
4. **Comprehensive Result Summary**

### 5. **Results and Cleanup**
- Uploads all test results as GitHub Actions artifacts
- Generates markdown summary with statistics
- Cleans up test branch (if enabled)
- Creates actionable recommendations

## Output Artifacts

### Test Results Structure
```
test_results/
├── summary.md                          # Main summary report
├── pr_XXX_build.log                   # Individual PR build logs
├── pr_XXX_merge.log                   # Individual PR merge logs
├── pr_XXX_merge_conflicts.log         # Merge conflict details
├── final_ctmm_build.log              # Final CTMM build log
├── final_latex_validation.log         # Final LaTeX validation log
├── final_enhanced_build.log           # Final enhanced build log
├── latex_error.log                    # LaTeX compilation errors
├── combined_test.pdf                  # Generated PDF (if successful)
├── successful_merges.count            # Success counters
├── failed_merges.count                # Failure counters
├── successful_builds.count            # Build success counters
└── failed_builds.count                # Build failure counters
```

### Summary Report Example

```markdown
# Automated PR Merge and Build Test Results

**Test Branch:** automated-merge-test-20240818-140532
**Base Branch:** main
**Timestamp:** 2024-08-18 14:05:32 UTC
**Total PRs Found:** 5

## Individual PR Test Results

### PR #123: Fix LaTeX escaping issues
- **Head SHA:** abc123...
- **Head Ref:** fix-escaping
- **Repository:** Darkness308/CTMM---PDF-in-LaTex
- **Merge Status:** ✅ SUCCESS
- **Build Status:** ✅ SUCCESS

### PR #124: Add new therapy module
- **Head SHA:** def456...
- **Head Ref:** new-module
- **Repository:** Darkness308/CTMM---PDF-in-LaTex
- **Merge Status:** ❌ FAILED (merge conflicts)
- **Build Status:** ⏭️ SKIPPED (merge failed)

## Final Combined Build Results
- **Final Build Status:** ✅ SUCCESS
- **PDF Generation:** ✅ SUCCESS

## Summary Statistics
| Metric | Count |
|--------|-------|
| Total PRs Found | 5 |
| Successful Merges | 4 |
| Failed Merges | 1 |
| Successful Builds | 4 |
| Failed Builds | 0 |

## Recommendations for Manual Review
- 🔍 **Review merge conflicts:** 1 PR(s) failed to merge
- ✅ **Integration ready:** All successfully merged PRs passed build validation
- 📋 **Next steps:** Review individual PR logs for detailed failure analysis
```

## Integration with Existing Tools

### Reuses Established Components
- **CTMM Build System** (`ctmm_build.py`)
- **LaTeX Validation** (`validate_latex_syntax.py`)  
- **LaTeX Action** (`dante-ev/latex-action@v2.0.0`)
- **Artifact Upload** (GitHub Actions built-in)

### Extends Current Workflows
- Compatible with existing CI/CD pipelines
- Does not interfere with PR validation workflows
- Uses same LaTeX packages and dependencies
- Follows established error handling patterns

## Security Considerations

### Safe Operations
- ✅ **Isolated Testing**: Works only on temporary test branches
- ✅ **No Main Branch Modification**: Never touches main branch directly
- ✅ **Token Security**: Uses GitHub's built-in authentication
- ✅ **External PR Handling**: Safely skips external repository PRs
- ✅ **Automatic Cleanup**: Removes test branches after completion

### Branch Protection
- Test branches are created with unique timestamps
- All operations are logged and traceable
- Failed operations don't affect repository state
- Merge conflicts are handled without data loss

## Troubleshooting

### Common Issues

**No PRs Found**
- Check if there are actually open PRs in the repository
- Verify the `max_prs` parameter isn't set too low
- Ensure GitHub token has repository read permissions
- Check workflow logs for HTTP response codes from GitHub API

**API Request Failures**
- Review HTTP status codes in the workflow logs
- Check GitHub API rate limits and status
- Verify GitHub token has appropriate permissions
- Look for network connectivity issues in runner logs

**Tool Dependency Issues**
- The workflow now automatically installs jq and curl
- Check the "Configure git and validate tools" step for tool validation results
- Verify the Ubuntu runner has package manager access

**Merge Conflicts**
- Review individual PR merge logs for conflict details
- Consider rebasing conflicting PRs manually
- Check if PRs are based on outdated branches
- Use the enhanced conflict logs with git status information

**Build Failures**
- Review individual PR build logs for error details
- Check timestamps to understand when failures occurred
- Verify PRs don't introduce LaTeX syntax errors
- Check if PRs break CTMM build system requirements
- Look for timeout issues in long-running builds

**External Repository PRs**
- External PRs are automatically skipped for security
- This is expected behavior, not an error
- Manual testing required for external contributions

**Rate Limiting**
- The workflow includes automatic rate limiting protection
- Check for GitHub API rate limit headers in logs
- Consider reducing `max_prs` for repositories with many open PRs

### Log Analysis

**Merge Logs** (`pr_XXX_merge.log`)
```bash
# View merge attempt details
cat test_results/pr_123_merge.log
```

**Build Logs** (`pr_XXX_build.log`)
```bash
# View build validation output
cat test_results/pr_123_build.log
```

**Conflict Logs** (`pr_XXX_merge_conflicts.log`)
```bash
# View merge conflict details
cat test_results/pr_123_merge_conflicts.log
```

## Maintenance

### Workflow Updates
- Workflow configuration in `.github/workflows/automated-pr-merge-test.yml`
- Validation script: `test_automated_pr_workflow.py`
- Regular testing ensures continued compatibility

### Performance Tuning
- Adjust `max_prs` parameter for large repositories
- Modify cron schedule for different testing frequencies
- Configure cleanup behavior based on storage needs

### Monitoring
- Review GitHub Actions usage for resource consumption
- Monitor artifact storage for large result sets
- Track workflow success rates over time

## Contributing

### Workflow Modifications
1. Update workflow YAML file
2. Run validation: `python3 test_automated_pr_workflow.py`
3. Test manually with small PR set
4. Document changes in this file

### Adding New Validation Steps
1. Add build commands to appropriate workflow steps
2. Update result logging and summary generation
3. Test with various PR scenarios
4. Update troubleshooting documentation

---

**Workflow File**: `.github/workflows/automated-pr-merge-test.yml`  
**Validation Script**: `test_automated_pr_workflow.py`  
**Documentation**: This file (`AUTOMATED_PR_MERGE_WORKFLOW.md`)