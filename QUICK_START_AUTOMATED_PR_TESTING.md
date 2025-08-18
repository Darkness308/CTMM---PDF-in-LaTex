# Quick Start Guide: Automated PR Merge and Build Testing

## Overview
This guide shows how to use the new **Automated PR Merge and Build Testing** workflow to test all open pull requests in a safe, isolated environment.

## What the Workflow Does

1. **Creates a test branch** from main (or specified base branch)
2. **Finds all open pull requests** in the repository
3. **Merges each PR sequentially** into the test branch
4. **Runs build validation** after each successful merge
5. **Generates comprehensive reports** with results
6. **Cleans up automatically** when finished

## How to Use It

### Manual Execution (Recommended for First Use)

1. **Go to GitHub Actions**
   - Navigate to your repository
   - Click the **Actions** tab
   - Find **Automated PR Merge and Build Testing** in the workflow list

2. **Run the Workflow**
   - Click **Run workflow** button
   - Configure options (or use defaults):
     - **Base branch**: `main` (default)
     - **Max PRs**: `10` (default, 0 = all PRs)
     - **Cleanup branch**: `true` (default)
   - Click **Run workflow**

3. **Monitor Progress**
   - Watch the workflow execution in real-time
   - View individual PR merge and build results
   - Check the job summary for key metrics

4. **Review Results**
   - Download the test results artifact
   - Open `summary.md` for comprehensive report
   - Check individual PR logs for failure details

### Automatic Execution

The workflow runs automatically:
- **Every Sunday at 2 AM UTC**
- Processes up to 10 open PRs
- Uses default settings (main branch, cleanup enabled)

## Understanding the Results

### Example Summary Report

```markdown
# Automated PR Merge and Build Test Results

**Test Branch:** automated-merge-test-20240818-140532
**Total PRs Found:** 5

## Summary Statistics
| Metric | Count |
|--------|-------|
| Total PRs Found | 5 |
| Successful Merges | 4 |
| Failed Merges | 1 |
| Successful Builds | 4 |
| Failed Builds | 0 |

## Recommendations
- 🔍 Review merge conflicts: 1 PR(s) failed to merge
- ✅ Integration ready: All successfully merged PRs passed build validation
```

### What Each Status Means

- **✅ Successful Merge**: PR merged without conflicts
- **❌ Failed Merge**: Merge conflicts prevent integration
- **✅ Successful Build**: LaTeX and CTMM build tests passed
- **❌ Failed Build**: Build validation failed (syntax errors, etc.)
- **⏭️ Skipped**: Build skipped due to merge failure
- **⚠️ External PR**: Skipped for security (external repository)

## Common Use Cases

### Before Major Release
```bash
# Test all open PRs before release
# Use GitHub Actions UI with settings:
# - Base branch: main
# - Max PRs: 0 (test all)
# - Cleanup: true
```

### Weekly Integration Check
- Automatic execution every Sunday
- Reviews all pending changes
- Identifies integration issues early

### Before Merging Large PR Set
```bash
# Test specific number of PRs
# Use GitHub Actions UI with settings:
# - Base branch: main  
# - Max PRs: 5
# - Cleanup: true
```

## Troubleshooting

### No PRs Found
- **Check**: Are there actually open PRs?
- **Solution**: Verify PRs exist and are in "open" state

### Merge Conflicts
- **Issue**: PRs conflict with each other or base branch
- **Solution**: Review conflict logs, rebase PRs manually
- **File**: `pr_XXX_merge_conflicts.log`

### Build Failures
- **Issue**: PRs introduce LaTeX syntax errors or break CTMM build
- **Solution**: Review build logs, fix errors in PRs
- **File**: `pr_XXX_build.log`

### External Repository PRs
- **Behavior**: External PRs are automatically skipped
- **Reason**: Security - cannot safely merge external code
- **Solution**: Test external PRs manually if needed

## Integration with Existing Workflows

This workflow **complements** existing CI/CD:

- ✅ **Does not interfere** with normal PR workflows
- ✅ **Uses same build tools** (ctmm_build.py, validate_latex_syntax.py)
- ✅ **Safe operation** - only uses temporary test branches
- ✅ **Clean up** - removes test branches automatically

## Best Practices

### For Repository Maintainers
1. **Run weekly** to catch integration issues early
2. **Before releases** test all open PRs
3. **Review logs** for patterns in failures
4. **Communicate results** to PR authors

### For Contributors
1. **Keep PRs up to date** with base branch
2. **Resolve conflicts** before weekly runs
3. **Test locally** with `make check` before submitting
4. **Watch for workflow notifications** if your PR fails

## Quick Commands

```bash
# Validate the workflow locally
make test-workflow

# Check individual build system
make check

# Validate PR content
make validate-pr

# Test LaTeX syntax
python3 validate_latex_syntax.py
```

## Support

- **Documentation**: `AUTOMATED_PR_MERGE_WORKFLOW.md`
- **Workflow File**: `.github/workflows/automated-pr-merge-test.yml`
- **Validation**: `test_automated_pr_workflow.py`
- **Issues**: Check GitHub Issues for workflow-related problems