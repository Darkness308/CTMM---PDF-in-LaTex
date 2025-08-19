# GitHub Permissions and Integration - Troubleshooting Guide

## Überblick

Dieses Dokument behandelt häufige GitHub-Integrationsprobleme im CTMM-Projekt und bietet Lösungsansätze für Berechtigungen, Workflow-Probleme und CI/CD-Pipeline-Fehler.

## 🔐 GitHub Actions Permissions

### Aktuelle Workflow-Konfiguration

Die `.github/workflows/latex-build.yml` wurde erweitert um proper permissions handling:

```yaml
name: Build LaTeX PDF

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

permissions:
  contents: read
  actions: read
  checks: write
  pull-requests: write
  issues: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      # ... bestehende steps
```

### 🚨 Häufige Permission-Probleme

#### 1. Artifact Upload Failure

**Problem**: `Error: Resource not accessible by integration`

**Lösung**: 
```yaml
permissions:
  contents: read
  actions: write  # Required for artifact upload
```

**Enhanced Workflow Step**:
```yaml
- name: Upload PDF artifact
  uses: actions/upload-artifact@v4
  with:
    name: CTMM_PDF_${{ github.run_number }}
    path: main.pdf
    retention-days: 90
  if: success()
```

#### 2. Pull Request Comments

**Problem**: Bot kann keine PR-Kommentare erstellen

**Lösung**:
```yaml
permissions:
  pull-requests: write
  issues: write  # Sometimes required for PR comments
```

**Implementation**:
```yaml
- name: Comment on PR
  uses: actions/github-script@v7
  if: github.event_name == 'pull_request'
  with:
    script: |
      github.rest.issues.createComment({
        issue_number: context.issue.number,
        owner: context.repo.owner,
        repo: context.repo.repo,
        body: '✅ CTMM Build successful! PDF artifact uploaded.'
      })
```

#### 3. Status Checks

**Problem**: Workflow kann keine Status Checks setzen

**Lösung**:
```yaml
permissions:
  checks: write
  statuses: write
```

### 🔧 Enhanced Security Configuration

#### Minimal Required Permissions

```yaml
# Minimal permissions für basic build
permissions:
  contents: read      # Repository content lesen
  actions: read       # Workflow-Informationen lesen
  
# Erweiterte Permissions für full functionality  
permissions:
  contents: read      # Repository zugriff
  actions: write      # Artifact upload
  checks: write       # Status checks
  pull-requests: write # PR comments
  issues: write       # Issue comments
  packages: read      # Für private packages (wenn benötigt)
```

#### Branch Protection Integration

```yaml
# In repository settings -> Branches -> main
required_status_checks:
  strict: true
  contexts:
    - "Build LaTeX PDF"
    - "CTMM Build System Check"
    - "LaTeX Validation"
```

## 🔄 Workflow File Reference Issues

### Problem: Incorrect File References

**Häufiger Fehler**: Workflow referenziert falsche Dateien

**Before (Fehlerhaft)**:
```yaml
- name: Set up LaTeX
  uses: dante-ev/latex-action@v2
  with:
    root_file: ctmm-main.tex  # ❌ Falsche Datei
```

**After (Korrekt)**:
```yaml
- name: Set up LaTeX  
  uses: dante-ev/latex-action@v2
  with:
    root_file: main.tex  # ✅ Korrekte Hauptdatei
    args: -interaction=nonstopmode -halt-on-error -shell-escape
```

### Enhanced File Validation

```yaml
- name: Validate File Structure
  run: |
    echo "🔍 Validating CTMM project structure..."
    
    # Check for main files
    if [ ! -f "main.tex" ]; then
      echo "❌ main.tex not found"
      exit 1
    fi
    
    # Check for required directories
    if [ ! -d "modules" ]; then
      echo "❌ modules/ directory not found"
      exit 1
    fi
    
    if [ ! -d "style" ]; then
      echo "❌ style/ directory not found"  
      exit 1
    fi
    
    # Check for CTMM build system
    if [ ! -f "ctmm_build.py" ]; then
      echo "❌ ctmm_build.py not found"
      exit 1
    fi
    
    echo "✅ Project structure validated"
```

## 🚀 CI/CD Pipeline Optimization

### Multi-Stage Validation Pipeline

```yaml
name: CTMM Comprehensive Build

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

permissions:
  contents: read
  actions: write
  checks: write
  pull-requests: write

jobs:
  # Stage 1: Syntax and Structure Validation
  validate:
    runs-on: ubuntu-latest
    outputs:
      structure-valid: ${{ steps.structure.outputs.valid }}
      syntax-valid: ${{ steps.syntax.outputs.valid }}
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'
          
      - name: Install dependencies
        run: pip install chardet
        
      - name: Validate project structure
        id: structure
        run: |
          python3 ctmm_build.py --structure-only
          echo "valid=true" >> $GITHUB_OUTPUT
          
      - name: Validate LaTeX syntax
        id: syntax  
        run: |
          python3 validate_latex_syntax.py
          echo "valid=true" >> $GITHUB_OUTPUT

  # Stage 2: Module Testing
  test-modules:
    needs: validate
    if: needs.validate.outputs.structure-valid == 'true'
    runs-on: ubuntu-latest
    strategy:
      matrix:
        module-type: [arbeitsblatt, tool, notfallkarte]
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        
      - name: Test ${{ matrix.module-type }} modules
        run: |
          python3 build_system.py --test-module-type ${{ matrix.module-type }}

  # Stage 3: Full Build
  build:
    needs: [validate, test-modules]
    if: needs.validate.outputs.syntax-valid == 'true'
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'
          
      - name: Install Python dependencies
        run: pip install chardet
        
      - name: Run CTMM Build System
        run: python3 ctmm_build.py
        
      - name: Set up LaTeX
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
            texlive-pstricks
            
      - name: Verify PDF generation
        run: |
          if [ -f "main.pdf" ]; then
            echo "✅ PDF successfully generated"
            ls -la main.pdf
            file main.pdf
          else
            echo "❌ PDF generation failed"
            find . -name "*.log" -exec echo "=== {} ===" \; -exec cat {} \;
            exit 1
          fi
          
      - name: Upload build artifacts
        uses: actions/upload-artifact@v4
        with:
          name: CTMM_Build_${{ github.run_number }}
          path: |
            main.pdf
            *.log
            build/
          retention-days: 30
```

## 🔍 Debugging GitHub Actions

### Enhanced Logging

```yaml
- name: Debug Environment
  run: |
    echo "🔍 Environment Debug Information"
    echo "=================================="
    echo "GitHub Actor: ${{ github.actor }}"
    echo "GitHub Event: ${{ github.event_name }}"
    echo "GitHub Ref: ${{ github.ref }}"
    echo "GitHub SHA: ${{ github.sha }}"
    echo "Runner OS: ${{ runner.os }}"
    echo ""
    echo "📁 Workspace Contents:"
    ls -la
    echo ""
    echo "🐍 Python Version:"
    python3 --version
    echo ""
    echo "📝 LaTeX Installation:"
    which pdflatex || echo "pdflatex not found"
    echo ""
    echo "💾 Disk Usage:"
    df -h
```

### Conditional Execution

```yaml
- name: Run LaTeX Build (if available)
  run: |
    if command -v pdflatex &> /dev/null; then
      echo "📄 Running LaTeX compilation..."
      pdflatex -version
      pdflatex -interaction=nonstopmode -file-line-error main.tex
    else
      echo "⚠️  LaTeX not available, skipping PDF generation"
      echo "Running structure validation only..."
      python3 ctmm_build.py --no-compile
    fi
```

## 🛡️ Security Best Practices

### Secret Management

```yaml
# Für private repositories oder erweiterte Funktionen
- name: Authenticate with private registry
  if: github.repository == 'Darkness308/CTMM---PDF-in-LaTex'
  run: |
    echo "${{ secrets.CUSTOM_TOKEN }}" | docker login registry.example.com -u username --password-stdin
```

### Environment-Specific Configurations

```yaml
- name: Set environment variables
  run: |
    if [ "${{ github.ref }}" = "refs/heads/main" ]; then
      echo "CTMM_ENV=production" >> $GITHUB_ENV
      echo "CTMM_DEBUG=false" >> $GITHUB_ENV
    else
      echo "CTMM_ENV=development" >> $GITHUB_ENV  
      echo "CTMM_DEBUG=true" >> $GITHUB_ENV
    fi
```

## 📊 Monitoring und Alerts

### Build Status Notifications

```yaml
- name: Notify on build failure
  if: failure()
  uses: actions/github-script@v7
  with:
    script: |
      const { context } = require('@actions/github');
      
      github.rest.issues.createComment({
        issue_number: context.issue.number,
        owner: context.repo.owner,
        repo: context.repo.repo,
        body: `❌ **CTMM Build Failed**
        
        Build failed in workflow: ${{ github.workflow }}
        Commit: ${{ github.sha }}
        Actor: ${{ github.actor }}
        
        Please check the [build logs](${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}) for details.`
      });
```

### Performance Monitoring

```yaml
- name: Build performance tracking
  run: |
    echo "📊 Build Performance Metrics"
    echo "============================"
    
    # Start time tracking
    start_time=$(date +%s)
    
    # Run build
    python3 ctmm_build.py
    
    # Calculate duration
    end_time=$(date +%s)
    duration=$((end_time - start_time))
    
    echo "Build Duration: ${duration}s"
    
    # Store metric for analysis
    echo "build_duration=${duration}" >> $GITHUB_OUTPUT
```

## 🔧 Repository Configuration

### Branch Protection Rules

Empfohlene Einstellungen für den `main` branch:

```yaml
# In GitHub Settings -> Branches -> Add rule
branch_protection_rules:
  main:
    required_status_checks:
      strict: true
      contexts:
        - "Build LaTeX PDF"
        - "validate"
        - "test-modules"
    enforce_admins: false
    required_pull_request_reviews:
      required_approving_review_count: 1
      dismiss_stale_reviews: true
    restrictions: null
```

### Webhook Configuration

```yaml
# Für externe Integrationen
webhook_config:
  url: "https://hooks.example.com/ctmm"
  content_type: "json"
  events:
    - push
    - pull_request
    - release
```

## 📋 Troubleshooting Checklist

### ✅ Pre-flight Checks

- [ ] Repository permissions korrekt konfiguriert
- [ ] Workflow-Datei Syntax ist gültig
- [ ] Alle referenzierten Dateien existieren
- [ ] Required secrets sind konfiguriert
- [ ] Branch protection rules sind angemessen

### 🔍 Common Issues Diagnostic

#### Issue: "Resource not accessible by integration"

```bash
# Check permissions in workflow file
grep -A 10 "permissions:" .github/workflows/*.yml

# Verify repository settings
# Go to Settings -> Actions -> General -> Workflow permissions
```

#### Issue: "File not found" in LaTeX build

```bash
# Verify file references
python3 ctmm_build.py --list-files

# Check file paths in workflow
grep -n "root_file\|input\|include" .github/workflows/*.yml
```

#### Issue: Artifact upload fails

```bash
# Check artifact configuration
grep -A 5 "upload-artifact" .github/workflows/*.yml

# Verify file exists before upload
ls -la main.pdf build/
```

## 🚀 Advanced Configuration

### Multi-Environment Deployments

```yaml
deploy:
  if: github.ref == 'refs/heads/main'
  needs: build
  runs-on: ubuntu-latest
  environment: 
    name: production
    url: https://ctmm-docs.example.com
  steps:
    - name: Deploy to production
      run: |
        echo "🚀 Deploying CTMM documentation..."
        # Deployment logic here
```

### Matrix Builds for Multiple Configurations

```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest, macos-latest]
    python-version: ['3.8', '3.9', '3.10', '3.11']
    latex-engine: [pdflatex, xelatex, lualatex]
  fail-fast: false
  
steps:
  - name: Test on ${{ matrix.os }} with Python ${{ matrix.python-version }}
    run: |
      python${{ matrix.python-version }} ctmm_build.py --engine ${{ matrix.latex-engine }}
```

## 📚 Resources und Links

### GitHub Documentation
- [GitHub Actions Permissions](https://docs.github.com/en/actions/security-guides/automatic-token-authentication)
- [Workflow Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [Branch Protection](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/defining-the-mergeability-of-pull-requests/about-protected-branches)

### CTMM-Specific
- [CTMM Build System](ctmm_build.py)
- [LaTeX Validator](validate_latex_syntax.py)
- [PR Validation](validate_pr.py)

---

## 📝 Changelog

### Version 1.2.0 (Current)
- ✅ Enhanced permissions handling
- ✅ Improved file reference validation
- ✅ Multi-stage pipeline implementation
- ✅ Comprehensive error handling

### Version 1.1.0
- ✅ Basic GitHub Actions integration
- ✅ Simple PDF build workflow
- ✅ Artifact upload functionality

### Version 1.0.0
- ✅ Initial workflow configuration
- ✅ Basic LaTeX compilation

---

*Dieses Dokument wird regelmäßig aktualisiert basierend auf neuen GitHub Features und Community Feedback. Bei Problemen, die hier nicht behandelt werden, erstelle ein GitHub Issue mit detaillierter Beschreibung.*