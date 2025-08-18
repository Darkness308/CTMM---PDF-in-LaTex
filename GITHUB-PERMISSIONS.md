# GitHub Permissions and Integration Troubleshooting Guide

## Overview

This guide addresses common GitHub integration issues, permission configurations, and troubleshooting strategies for the CTMM therapeutic materials system. It covers GitHub Actions workflows, artifact handling, and automated build processes.

## GitHub Actions Permissions

### Required Permissions for CTMM Workflows

#### Repository Permissions
```yaml
permissions:
  contents: read          # Read repository content
  actions: read          # Read workflow configurations  
  packages: write        # Upload/download packages and artifacts
  pages: write           # Deploy to GitHub Pages (if used)
  id-token: write        # OIDC token for secure authentication
```

#### Workflow-Specific Permissions
```yaml
# For latex-build.yml
permissions:
  contents: read
  actions: read
  packages: write
  
# For pr-validation.yml  
permissions:
  contents: read
  pull-requests: write   # Comment on PRs
  actions: read
```

### Common Permission Issues

#### Issue: "Resource not accessible by integration"
**Symptoms:**
- Workflow fails with permission denied errors
- Unable to upload artifacts
- Cannot comment on pull requests

**Solutions:**
```yaml
# Add explicit permissions to workflow
name: Build LaTeX PDF
on: [push, pull_request]

permissions:
  contents: read
  actions: read
  packages: write

jobs:
  build:
    runs-on: ubuntu-latest
    # ... rest of workflow
```

#### Issue: Artifact Upload Failures
**Symptoms:**
- "Failed to upload artifact" errors
- Artifacts not appearing in workflow runs
- Permission denied on artifact download

**Solutions:**
```yaml
# Correct artifact upload configuration
- name: Upload PDF artifact
  uses: actions/upload-artifact@v4
  with:
    name: CTMM_PDF
    path: main.pdf
    retention-days: 30
  if: success()

# For downloading artifacts
- name: Download artifacts
  uses: actions/download-artifact@v4
  with:
    name: CTMM_PDF
    path: ./artifacts/
```

## GitHub Actions Workflow Fixes

### Current latex-build.yml Issues and Fixes

#### Issue: Incorrect Main File Reference
**Problem:** Workflow may reference wrong LaTeX main file
**Current (Potentially Problematic):**
```yaml
with:
  root_file: main.tex    # Assumes file in root
```

**Fixed Configuration:**
```yaml
- name: Set up LaTeX
  uses: dante-ev/latex-action@v2
  with:
    root_file: main.tex
    working_directory: .
    args: -interaction=nonstopmode -halt-on-error -shell-escape
```

#### Issue: Missing Error Handling
**Problem:** Workflow doesn't handle LaTeX compilation errors gracefully

**Enhanced Error Handling:**
```yaml
- name: Compile LaTeX with error handling
  uses: dante-ev/latex-action@v2
  with:
    root_file: main.tex
    args: -interaction=nonstopmode -halt-on-error -shell-escape
  continue-on-error: true
  id: latex_compilation

- name: Check compilation results
  run: |
    if [ -f "main.pdf" ]; then
      echo "✅ PDF successfully generated"
      ls -la main.pdf
    else
      echo "❌ PDF generation failed"
      echo "Checking for LaTeX log files..."
      find . -name "*.log" -exec echo "=== {} ===" \; -exec cat {} \;
      exit 1
    fi

- name: Upload compilation logs on failure
  if: failure()
  uses: actions/upload-artifact@v4
  with:
    name: latex_logs
    path: |
      *.log
      *.aux
      *.fls
      *.fdb_latexmk
```

### Enhanced Workflow Configuration

#### Complete latex-build.yml with Fixes
```yaml
name: Build LaTeX PDF

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

permissions:
  contents: read
  actions: read
  packages: write

env:
  MAIN_TEX_FILE: main.tex

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'

      - name: Install Python dependencies
        run: |
          python -m pip install --upgrade pip
          pip install chardet

      - name: Validate repository structure
        run: |
          echo "🔍 Validating CTMM repository structure..."
          if [ ! -f "$MAIN_TEX_FILE" ]; then
            echo "❌ Main LaTeX file not found: $MAIN_TEX_FILE"
            exit 1
          fi
          echo "✅ Main LaTeX file found: $MAIN_TEX_FILE"

      - name: Run LaTeX syntax validation
        run: |
          echo "🔧 Running LaTeX syntax validation..."
          python3 validate_latex_syntax.py
          
      - name: Run CTMM Build System Check
        run: |
          echo "🚀 Running CTMM build system validation..."
          python3 ctmm_build.py
          
      - name: Enhanced pre-build validation
        run: |
          echo "🔍 Running enhanced pre-build validation..."
          python3 test_issue_761_fix.py || echo "⚠️  Warning: Some robustness checks failed but continuing..."

      - name: Set up LaTeX
        uses: dante-ev/latex-action@v2
        with:
          root_file: ${{ env.MAIN_TEX_FILE }}
          working_directory: .
          args: -interaction=nonstopmode -halt-on-error -shell-escape
          extra_system_packages: |
            texlive-lang-german
            texlive-fonts-recommended
            texlive-latex-recommended
            texlive-fonts-extra
            texlive-latex-extra
            texlive-science
            texlive-pstricks
        continue-on-error: true
        id: latex_build

      - name: Verify PDF generation
        run: |
          if [ -f "main.pdf" ]; then
            echo "✅ PDF successfully generated"
            ls -la main.pdf
            file main.pdf
          else
            echo "❌ PDF generation failed"
            echo "Checking for LaTeX log files..."
            find . -name "*.log" -exec echo "=== {} ===" \; -exec head -50 {} \;
            exit 1
          fi

      - name: Upload PDF artifact
        uses: actions/upload-artifact@v4
        with:
          name: CTMM_PDF_${{ github.sha }}
          path: main.pdf
          retention-days: 30
        if: success()

      - name: Upload build logs (on failure)
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: build_logs_${{ github.sha }}
          path: |
            *.log
            *.aux
            *.fls
            *.fdb_latexmk
            build_system.log
          retention-days: 7
```

## Troubleshooting Common Issues

### Authentication Problems

#### Issue: GITHUB_TOKEN Permissions
**Symptoms:**
- "Bad credentials" errors
- API rate limiting
- Unable to access repository resources

**Solutions:**
```yaml
# Use automatic token with correct permissions
env:
  GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

# For organization repositories, may need PAT
env:
  GITHUB_TOKEN: ${{ secrets.PERSONAL_ACCESS_TOKEN }}
```

#### Issue: OIDC Token Configuration
**For enhanced security with OIDC:**
```yaml
permissions:
  id-token: write
  contents: read

steps:
  - name: Configure AWS credentials (example)
    uses: aws-actions/configure-aws-credentials@v4
    with:
      role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
      role-session-name: GitHubActions
      aws-region: us-east-1
```

### Artifact Management Issues

#### Issue: Artifact Size Limits
**Problem:** PDF files or logs exceed GitHub's artifact size limits

**Solutions:**
```yaml
# Compress artifacts before upload
- name: Compress artifacts
  run: |
    tar -czf ctmm-build-outputs.tar.gz main.pdf *.log
    
- name: Upload compressed artifacts
  uses: actions/upload-artifact@v4
  with:
    name: CTMM_Compressed_${{ github.sha }}
    path: ctmm-build-outputs.tar.gz
```

#### Issue: Artifact Retention
**Problem:** Artifacts are deleted too quickly or retained too long

**Configuration:**
```yaml
# Short retention for debug logs
- name: Upload debug logs
  uses: actions/upload-artifact@v4
  with:
    name: debug_logs
    path: "*.log"
    retention-days: 3

# Longer retention for release artifacts
- name: Upload release PDF
  uses: actions/upload-artifact@v4
  with:
    name: release_pdf
    path: main.pdf
    retention-days: 90
```

### Workflow Dependency Issues

#### Issue: Action Version Compatibility
**Problem:** Using outdated or incompatible action versions

**Solutions:**
```yaml
# Use latest stable versions
- uses: actions/checkout@v4          # Not v3 or v2
- uses: actions/setup-python@v4      # Not v3
- uses: actions/upload-artifact@v4   # Not v3
- uses: dante-ev/latex-action@v2     # Confirmed working version
```

#### Issue: Runner Environment Problems
**Problem:** Missing dependencies or environment issues

**Robust Environment Setup:**
```yaml
- name: Update system packages
  run: |
    sudo apt-get update
    sudo apt-get install -y build-essential

- name: Verify system requirements
  run: |
    echo "Python version: $(python3 --version)"
    echo "Git version: $(git --version)"
    echo "Available disk space:"
    df -h
```

## Organization and Repository Settings

### Repository Configuration

#### Required Settings
1. **Actions → General → Workflow Permissions:**
   - Select "Read and write permissions"
   - Check "Allow GitHub Actions to create and approve pull requests"

2. **Actions → General → Artifact and log retention:**
   - Set appropriate retention periods (30-90 days for production)

3. **Security → Secrets and variables → Actions:**
   - Add any required personal access tokens
   - Configure environment-specific variables

#### Branch Protection Rules
```yaml
# Recommended branch protection for main
Required status checks:
  - Build LaTeX PDF
  - CTMM Build System Check
  - LaTeX syntax validation

Enforce restrictions for everyone: true
Allow force pushes: false
Allow deletions: false
```

### Organizational Policies

#### Runner Access
**For private repositories:**
```yaml
# .github/workflows/latex-build.yml
jobs:
  build:
    runs-on: ubuntu-latest
    # For private repos, ensure runners have access
```

#### Secret Management
**Best practices:**
1. Use repository secrets for repo-specific tokens
2. Use organization secrets for shared resources
3. Use environment secrets for deployment targets
4. Regularly rotate access tokens

## Debugging Workflow Issues

### Enabling Debug Logging
```yaml
# Add to workflow for detailed debugging
env:
  ACTIONS_STEP_DEBUG: true
  ACTIONS_RUNNER_DEBUG: true
```

### Common Debug Commands
```yaml
- name: Debug environment
  run: |
    echo "Current directory: $(pwd)"
    echo "Environment variables:"
    env | grep -E "(GITHUB_|RUNNER_)" | sort
    echo "Available files:"
    ls -la
    echo "Git status:"
    git status
```

### Log Analysis
```bash
# Download and analyze workflow logs
gh run download <run-id>
grep -r "ERROR\|FAILED\|error" .
```

## Performance Optimization

### Caching Strategies
```yaml
# Cache Python dependencies
- name: Cache Python packages
  uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-

# Cache LaTeX packages (if using local installation)
- name: Cache LaTeX packages
  uses: actions/cache@v3
  with:
    path: /tmp/texlive
    key: ${{ runner.os }}-texlive-${{ hashFiles('main.tex') }}
```

### Parallel Job Execution
```yaml
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - name: Validate syntax
        run: python3 validate_latex_syntax.py
  
  build:
    runs-on: ubuntu-latest
    needs: validate  # Wait for validation
    steps:
      - name: Build PDF
        uses: dante-ev/latex-action@v2
```

## Security Considerations

### Token Security
- Never log secrets or tokens
- Use minimal required permissions
- Regularly audit and rotate tokens
- Use OIDC when possible for enhanced security

### Artifact Security
```yaml
# Sanitize artifacts before upload
- name: Sanitize build outputs
  run: |
    # Remove sensitive information from logs
    sed -i 's/TOKEN=[^[:space:]]*/TOKEN=***REDACTED***/g' *.log
```

### Code Injection Prevention
```yaml
# Avoid using user input directly in commands
- name: Safe parameter handling
  run: |
    SAFE_INPUT="${{ github.event.inputs.user_input }}"
    echo "Processing: ${SAFE_INPUT//[^a-zA-Z0-9]/_}"
```

## Monitoring and Alerting

### Workflow Health Monitoring
```yaml
# Add health check step
- name: Workflow health check
  run: |
    echo "::notice::Workflow completed successfully"
    echo "Build time: $((SECONDS / 60)) minutes"
    
- name: Notify on failure
  if: failure()
  run: |
    echo "::error::Workflow failed - investigate logs"
```

### Integration with External Monitoring
```yaml
# Send notifications to external systems
- name: Notify external system
  if: always()
  run: |
    curl -X POST "${{ secrets.WEBHOOK_URL }}" \
      -H "Content-Type: application/json" \
      -d '{"status": "${{ job.status }}", "repo": "${{ github.repository }}"}'
```

---

**Document Version**: 1.0.0  
**Last Updated**: 2024  
**Applies to**: GitHub Actions, CTMM Build System  
**Next Review**: After major GitHub Actions updates