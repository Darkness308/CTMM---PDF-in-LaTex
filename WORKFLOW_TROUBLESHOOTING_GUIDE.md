# Workflow Troubleshooting Guide

## Quick Reference for Workflow Issues

### If a Workflow Still Fails After These Fixes

#### 1. Check the Workflow Run Logs
```
1. Go to GitHub repository
2. Click "Actions" tab
3. Click on the failed workflow run
4. Expand the failed step
5. Read the error message
```

#### 2. Common Issues and Solutions

##### Issue: LaTeX Compilation Fails
**Symptom:** Error in "Set up LaTeX" or "Build PDF" step

**Possible Causes:**
- Missing LaTeX packages
- Syntax error in .tex files
- Package loading order issue

**Solutions:**
1. Check if all required packages are in `extra_system_packages`
2. Run locally: `python3 validate_latex_syntax.py`
3. Check package loading order in main.tex
4. Verify hyperref is loaded before custom style packages

##### Issue: Python Script Fails
**Symptom:** Error in steps running Python scripts

**Possible Causes:**
- Missing Python dependencies
- Python version incompatibility
- Script logic error

**Solutions:**
1. Verify Python dependencies are installed (chardet, pyyaml)
2. Check Python version is 3.x
3. Run script locally: `python3 ctmm_build.py`
4. Check script output for specific errors

##### Issue: Workflow Hangs/Times Out
**Symptom:** Workflow runs for a long time and then times out

**Possible Causes:**
- Interactive command waiting for input
- Infinite loop
- Network issue downloading packages

**Solutions:**
1. Check if timeout-minutes is set appropriately
2. Verify commands use non-interactive flags
   - `pdflatex -interaction=nonstopmode`
   - Git commands with `--no-pager`
3. Increase timeout if legitimate operation takes longer

##### Issue: Permission Denied
**Symptom:** Error about permissions or access denied

**Possible Causes:**
- Insufficient workflow permissions
- Protected branch rules
- Token permissions

**Solutions:**
1. Check `permissions:` section in workflow
2. Verify GITHUB_TOKEN has required scopes
3. Check repository settings for branch protection

##### Issue: File Not Found
**Symptom:** Error about missing file or directory

**Possible Causes:**
- Missing checkout step
- Wrong working directory
- File not committed to repository

**Solutions:**
1. Ensure `actions/checkout@v4` is first step
2. Check file exists in repository
3. Verify file path is correct (absolute vs relative)
4. Use `ls -la` step to debug file locations

#### 3. Debug Commands

Add these steps temporarily to debug issues:

```yaml
- name: Debug - List files
  run: |
    echo "Current directory:"
    pwd
    echo "Files in current directory:"
    ls -la
    echo "Files in .github/workflows:"
    ls -la .github/workflows/

- name: Debug - Check Python environment
  run: |
    echo "Python version:"
    python3 --version
    echo "Installed packages:"
    pip list
    echo "Python path:"
    which python3

- name: Debug - Check LaTeX environment
  run: |
    echo "pdflatex version:"
    pdflatex --version || echo "pdflatex not found"
    echo "TeX packages:"
    kpsewhich -var-value TEXMFDIST

- name: Debug - Environment variables
  run: |
    echo "GitHub context:"
    echo "Repository: ${{ github.repository }}"
    echo "Ref: ${{ github.ref }}"
    echo "SHA: ${{ github.sha }}"
    echo "Actor: ${{ github.actor }}"
```

#### 4. Local Testing Commands

Before pushing workflow changes, test locally:

```bash
# Validate YAML syntax
python3 validate_workflow_syntax.py

# Test workflow checks
python3 ctmm_build.py
python3 validate_latex_syntax.py

# Check for issues
python3 /tmp/analyze_workflows.py
python3 /tmp/check_workflow_runtime_issues.py

# Simulate workflow validation checks
bash /tmp/test_workflow_checks.sh
```

#### 5. Workflow-Specific Troubleshooting

##### latex-build.yml
- Check LaTeX packages are available
- Verify main.tex compiles locally
- Check PDF output location (build/ vs current directory)

##### latex-validation.yml
- Verify validation checks pass locally
- Check grep patterns match expected format
- Verify awk scripts work with your shell

##### pr-validation.yml
- Ensure PR has actual changes
- Check Python scripts execute successfully
- Verify GITHUB_TOKEN has required permissions

##### static.yml (GitHub Pages)
- Check Pages is enabled in repository settings
- Verify deploy permissions are set
- Check artifact upload/download steps

##### automated-pr-merge-test.yml
- Only runs on workflow_dispatch or schedule
- Requires open PRs to test
- Check git configuration steps

##### test-dante-version.yml
- Manual trigger only
- Tests LaTeX action availability
- Useful for debugging LaTeX action issues

## Monitoring Workflow Health

### Regular Checks
1. Review workflow runs weekly
2. Check for warning messages in logs
3. Monitor execution times for increases
4. Update action versions quarterly
5. Test workflows after major repository changes

### Performance Optimization
1. Use caching for dependencies when possible
2. Keep workflows focused and modular
3. Use `continue-on-error: true` for non-critical steps
4. Set appropriate timeout values
5. Cancel redundant runs with `concurrency` settings

## Getting Help

### Resources
1. GitHub Actions documentation: https://docs.github.com/actions
2. This repository's documentation in README.md
3. Copilot instructions in .github/copilot-instructions.md
4. Previous issue resolutions in ISSUE_*.md files

### Reporting Issues
When reporting workflow issues, include:
1. Workflow name and run number
2. Error message from logs
3. Changes made before failure
4. Local test results
5. Environment information (if relevant)

---

**Last Updated:** January 11, 2026
**Maintainer:** CTMM Project Team
