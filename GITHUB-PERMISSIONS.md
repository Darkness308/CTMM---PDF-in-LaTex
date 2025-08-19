# GitHub Permissions and Integration Troubleshooting Guide

## Overview

This guide addresses common GitHub integration issues encountered when working with the CTMM LaTeX system, particularly related to GitHub Actions, permissions, and automated workflows. It provides systematic troubleshooting steps and preventive measures for maintaining a smooth development experience.

## Common Permission Issues

### 1. GitHub Actions Workflow Failures

#### Issue: "Permission denied" in workflow execution
**Symptoms**:
```yaml
Error: Process completed with exit code 126.
/bin/bash: ./create-module.sh: Permission denied
```

**Root Cause**: Git doesn't preserve file execution permissions by default.

**Solution**:
```yaml
# Add to workflow before script execution
- name: Set script permissions
  run: chmod +x create-module.sh

# Or use explicit bash execution
- name: Run module generator
  run: bash create-module.sh
```

**Prevention**:
```bash
# Ensure scripts are executable before committing
chmod +x create-module.sh
git add create-module.sh
git commit -m "Add executable permission to create-module.sh"
```

#### Issue: "File not found" errors in workflows
**Symptoms**:
```yaml
Error: main.tex: No such file or directory
```

**Root Cause**: Workflow using incorrect file references or missing checkout step.

**Solution**:
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4  # Ensure this is first

      - name: Set up LaTeX
        uses: dante-ev/latex-action@v2
        with:
          root_file: main.tex  # Correct file reference
          working_directory: .  # Explicit working directory
```

### 2. Artifact Upload/Download Issues

#### Issue: "Artifact not found" in dependent jobs
**Symptoms**:
```yaml
Error: Artifact 'CTMM_PDF' not found in workflow run
```

**Root Cause**: Artifacts not properly uploaded or workflow job dependencies misconfigured.

**Solution**:
```yaml
# Upload artifacts correctly
- name: Upload PDF artifact
  uses: actions/upload-artifact@v4
  with:
    name: CTMM_PDF
    path: main.pdf
    if-no-files-found: error  # Fail if PDF not generated

# Download in dependent job
- name: Download PDF artifact  
  uses: actions/download-artifact@v4
  with:
    name: CTMM_PDF
    path: ./downloads/
```

### 3. Token and Authentication Issues

#### Issue: "Authentication required" for private repositories
**Symptoms**:
```yaml
Error: Request failed due to following response errors:
- Resource not accessible by integration
```

**Root Cause**: Insufficient permissions for GITHUB_TOKEN.

**Solution**:
```yaml
# Add explicit permissions to workflow
permissions:
  contents: read
  actions: read
  checks: write
  pull-requests: write

# Or use specific token with broader permissions
env:
  GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Workflow Configuration Best Practices

### 1. Robust GitHub Actions Setup

#### Complete Workflow Template
```yaml
---
name: CTMM Build and Validation

# Trigger configuration
"on":
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  workflow_dispatch:  # Manual trigger

# Permissions for all jobs
permissions:
  contents: read
  actions: read
  checks: write
  pull-requests: write
  pages: write
  id-token: write

jobs:
  validate:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Full history for git operations

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'
          cache: 'pip'  # Cache Python dependencies

      - name: Install Python dependencies
        run: |
          pip install chardet
          pip install --upgrade pip

      - name: Set script permissions
        run: |
          chmod +x create-module.sh
          chmod +x *.py

      - name: Validate repository structure
        run: |
          python3 ctmm_build.py --validate
          python3 validate_latex_syntax.py

  build:
    needs: validate
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up LaTeX environment
        uses: dante-ev/latex-action@v2
        with:
          root_file: main.tex
          args: -interaction=nonstopmode -halt-on-error -shell-escape
          extra_system_packages: |
            texlive-lang-german
            texlive-fonts-recommended
            texlive-latex-recommended
            texlive-fonts-extra
            texlive-latex-extra
            texlive-science

      - name: Verify PDF generation
        run: |
          if [ -f "main.pdf" ]; then
            echo "✅ PDF successfully generated"
            ls -la main.pdf
          else
            echo "❌ PDF generation failed"
            exit 1
          fi

      - name: Upload PDF artifact
        uses: actions/upload-artifact@v4
        with:
          name: CTMM_PDF_${{ github.sha }}
          path: main.pdf
          retention-days: 30

      - name: Upload logs on failure
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: build_logs_${{ github.sha }}
          path: |
            *.log
            build_system.log
          retention-days: 7
```

### 2. Security Considerations

#### Safe Token Usage
```yaml
# ✅ Correct: Use built-in GITHUB_TOKEN
env:
  GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

# ❌ Avoid: Exposing tokens in logs
run: echo "Token: ${{ secrets.GITHUB_TOKEN }}"

# ✅ Correct: Use mask for debugging
run: echo "::add-mask::${{ secrets.GITHUB_TOKEN }}"
```

#### Secure Artifact Handling
```yaml
# ✅ Correct: Explicit artifact naming with context
- name: Upload secure artifacts
  uses: actions/upload-artifact@v4
  with:
    name: ctmm-pdf-${{ github.event.pull_request.number || github.ref_name }}
    path: main.pdf

# ❌ Avoid: Generic names that could conflict
name: pdf-output
```

## Troubleshooting Systematic Approach

### 1. Diagnosis Workflow

#### Step 1: Identify the Scope
```bash
# Check workflow status
gh run list --limit 10

# Get detailed failure information
gh run view <run-id> --log-failed

# Check specific job logs
gh run view <run-id> --job <job-id>
```

#### Step 2: Local Reproduction
```bash
# Replicate workflow environment locally
docker run -it --rm -v $(pwd):/workspace ubuntu:latest

# Install dependencies manually
apt update && apt install -y python3 python3-pip nodejs npm

# Run failing commands
cd /workspace
python3 ctmm_build.py
```

#### Step 3: Incremental Testing
```bash
# Test individual workflow components
act -j validate  # Use 'act' to run GitHub Actions locally

# Test specific script permissions
ls -la create-module.sh
bash -n create-module.sh  # Syntax check
```

### 2. Common Error Patterns and Solutions

#### LaTeX Action Version Issues
```yaml
# ❌ Problem: Using non-existent version
uses: dante-ev/latex-action@v2.0.0

# ✅ Solution: Use valid version tags
uses: dante-ev/latex-action@v2

# ✅ Alternative: Pin to specific working version
uses: dante-ev/latex-action@v0.2
```

#### File Path and Working Directory Issues
```yaml
# ❌ Problem: Assuming incorrect working directory
run: pdflatex main.tex

# ✅ Solution: Explicit paths and directories
run: |
  cd ${{ github.workspace }}
  pdflatex -output-directory=build main.tex

# ✅ Alternative: Use working-directory parameter
- name: Build LaTeX
  run: pdflatex main.tex
  working-directory: ${{ github.workspace }}
```

#### Node.js and Python Environment Issues
```yaml
# ❌ Problem: Missing runtime environment
run: node module-generator.js tool example

# ✅ Solution: Explicit runtime setup
- name: Set up Node.js
  uses: actions/setup-node@v4
  with:
    node-version: '18'
    cache: 'npm'

- name: Install Node.js dependencies
  run: npm install  # If package.json exists

- name: Run module generator
  run: node module-generator.js tool example
```

## Advanced Troubleshooting Techniques

### 1. Debugging Workflow Execution

#### Enable Debug Logging
```yaml
# Add debug output to workflow
env:
  ACTIONS_STEP_DEBUG: true
  ACTIONS_RUNNER_DEBUG: true

# Custom debug information in scripts
run: |
  echo "::debug::Current working directory: $(pwd)"
  echo "::debug::Available files: $(ls -la)"
  echo "::debug::Environment variables:"
  env | sort
```

#### Matrix Testing for Cross-Platform Issues
```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest, macos-latest]
    python-version: ['3.8', '3.9', '3.10', '3.11']
    
runs-on: ${{ matrix.os }}

steps:
  - name: Platform-specific setup
    run: |
      if [ "$RUNNER_OS" == "Windows" ]; then
        echo "Windows-specific commands"
      elif [ "$RUNNER_OS" == "macOS" ]; then
        echo "macOS-specific commands"  
      else
        echo "Linux-specific commands"
      fi
    shell: bash
```

### 2. Performance Optimization

#### Efficient Dependency Caching
```yaml
- name: Cache LaTeX packages
  uses: actions/cache@v4
  with:
    path: |
      ~/.texlive
      /usr/local/texlive
    key: latex-${{ runner.os }}-${{ hashFiles('main.tex') }}
    restore-keys: |
      latex-${{ runner.os }}-

- name: Cache Python packages
  uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: pip-${{ runner.os }}-${{ hashFiles('requirements.txt') }}
    restore-keys: |
      pip-${{ runner.os }}-
```

#### Parallel Job Execution
```yaml
jobs:
  test-modules:
    strategy:
      matrix:
        module: [arbeitsblatt, tool, notfallkarte]
        
    steps:
      - name: Test ${{ matrix.module }} generation
        run: |
          node module-generator.js ${{ matrix.module }} test-${{ matrix.module }}
          python3 ctmm_build.py --validate-module test-${{ matrix.module }}
```

## Integration with Development Tools

### 1. VS Code and GitHub Integration

#### Settings for Seamless Integration
```json
// .vscode/settings.json
{
    "github.copilot.enable": true,
    "github.repositories.defaultCloneDirectory": "./workspace",
    "git.autofetch": true,
    "git.enableSmartCommit": true,
    
    // GitHub Actions integration
    "github-actions.workflows.pinned.workflows": [
        ".github/workflows/latex-build.yml"
    ],
    
    // Task integration with GitHub workflows
    "tasks.problems.enable": true,
    "tasks.enableInput": true
}
```

#### GitHub CLI Integration
```bash
# Install GitHub CLI
brew install gh  # macOS
sudo apt install gh  # Ubuntu

# Authenticate and configure
gh auth login
gh config set git_protocol https

# Workflow management commands
gh workflow list
gh workflow run latex-build.yml
gh workflow view latex-build.yml
```

### 2. Automated PR Validation

#### PR Template Integration
```markdown
<!-- .github/pull_request_template.md -->
## CTMM Module Generator PR Checklist

### Module Generation Tests
- [ ] All generated modules pass LaTeX validation
- [ ] CTMM design patterns are correctly applied
- [ ] German therapeutic terminology is appropriate
- [ ] Interactive form elements work correctly

### Build System Tests  
- [ ] `python3 ctmm_build.py` passes all checks
- [ ] Generated PDF includes new modules correctly
- [ ] Cross-platform compatibility verified
- [ ] No new build warnings or errors

### Documentation Updates
- [ ] MODULE-GENERATOR-README.md updated if needed
- [ ] Examples include new module types
- [ ] VS Code tasks work with new modules
- [ ] GitHub Actions workflow handles new files

### Code Quality
- [ ] JavaScript follows project conventions
- [ ] Shell scripts are cross-platform compatible
- [ ] LaTeX output follows CTMM standards
- [ ] No sensitive information in generated content
```

#### Automated Validation Workflow
```yaml
name: PR Validation

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  validate-pr:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Validate PR content
        run: |
          python3 validate_pr.py --base-branch origin/main
          
      - name: Test module generation
        run: |
          chmod +x create-module.sh
          node module-generator.js arbeitsblatt test-pr-validation
          python3 ctmm_build.py --validate-module test-pr-validation
          
      - name: Comment on PR
        if: failure()
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: '❌ PR validation failed. Please check the workflow logs for details.'
            });
```

## Preventive Measures and Best Practices

### 1. Repository Health Monitoring

#### Automated Health Checks
```yaml
# .github/workflows/repository-health.yml
name: Repository Health Check

on:
  schedule:
    - cron: '0 6 * * 1'  # Weekly on Monday at 6 AM UTC
  workflow_dispatch:

jobs:
  health-check:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Check file permissions
        run: |
          find . -name "*.sh" -not -path "./.git/*" | while read script; do
            if [ ! -x "$script" ]; then
              echo "❌ Script not executable: $script"
              exit 1
            fi
          done
          
      - name: Validate all modules
        run: |
          python3 ctmm_build.py --comprehensive-check
          
      - name: Test module generation
        run: |
          for type in arbeitsblatt tool notfallkarte; do
            node module-generator.js "$type" "health-check-$type"
            python3 ctmm_build.py --validate-module "health-check-$type"
          done
```

### 2. Documentation Synchronization

#### Automated Documentation Updates
```yaml
- name: Update documentation
  if: contains(github.event.head_commit.message, '[docs]')
  run: |
    # Generate updated module examples
    node module-generator.js --examples --output docs/
    
    # Update README with latest features
    python3 update_readme.py --auto-generate
    
    # Commit documentation changes
    git config --local user.email "action@github.com"
    git config --local user.name "GitHub Action"
    git add docs/ README.md
    git diff --staged --quiet || git commit -m "docs: Auto-update documentation [skip ci]"
```

## Emergency Recovery Procedures

### 1. Workflow Restoration

#### Backup and Recovery Strategy
```bash
# Create workflow backup
cp .github/workflows/latex-build.yml .github/workflows/latex-build.yml.backup

# Test workflow changes in feature branch
git checkout -b test-workflow-fix
# Make changes
git add .github/workflows/
git commit -m "test: Fix workflow issues"
git push origin test-workflow-fix

# Manual workflow testing
gh workflow run latex-build.yml --ref test-workflow-fix

# Rollback if needed
git checkout main
cp .github/workflows/latex-build.yml.backup .github/workflows/latex-build.yml
git add .github/workflows/latex-build.yml
git commit -m "revert: Restore working workflow"
```

### 2. Permission Reset Procedures

#### File Permission Recovery
```bash
# Restore all script permissions
find . -name "*.sh" -exec chmod +x {} \;
find . -name "*.py" -exec chmod +x {} \;

# Commit permission fixes
git add .
git commit -m "fix: Restore executable permissions to scripts"
git push origin main
```

#### Token and Authentication Reset
```bash
# Regenerate GitHub token if compromised
gh auth refresh

# Update repository secrets
gh secret set CUSTOM_TOKEN --body "new-token-value"

# Verify permissions
gh api user
gh api repos/:owner/:repo
```

## Monitoring and Alerting

### 1. Workflow Failure Notifications

#### Slack Integration
```yaml
- name: Notify on failure
  if: failure()
  uses: 8398a7/action-slack@v3
  with:
    status: failure
    channel: '#ctmm-builds'
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
    message: |
      ❌ CTMM Build Failed
      Repository: ${{ github.repository }}
      Branch: ${{ github.ref }}
      Commit: ${{ github.sha }}
      Actor: ${{ github.actor }}
```

### 2. Performance Monitoring

#### Build Time Tracking
```yaml
- name: Track build performance
  run: |
    start_time=$(date +%s)
    python3 ctmm_build.py
    end_time=$(date +%s)
    duration=$((end_time - start_time))
    echo "Build duration: ${duration}s" | tee build-metrics.txt

- name: Upload metrics
  uses: actions/upload-artifact@v4
  with:
    name: build-metrics
    path: build-metrics.txt
```

---

**Document Version**: 1.0.0  
**Last Updated**: August 2024  
**Support Contact**: CTMM Development Team  
**Related Documents**: BUILD-TASKS-EVALUATION.md, MODULE-GENERATOR-README.md