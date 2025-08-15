# GitHub Permissions & Integration Troubleshooting Guide

Umfassende Anleitung zur Behebung von GitHub Actions Problemen und Berechtigungskonflikten im CTMM-System.

## Häufige Probleme und Lösungen

### 1. GitHub Actions Workflow-Fehler

#### Problem: Merge-Konflikte in Workflow-Dateien

**Symptome:**
```yaml
copilot/fix-288
        uses: dante-ev/latex-action@v2.0.0

copilot/fix-292
        uses: dante-ev/latex-action@v2.0.0
```

**Ursache:** Unvollständige Merge-Resolution

**Lösung:**
```yaml
# ✅ Korrekte Workflow-Syntax
- name: Set up LaTeX
  uses: dante-ev/latex-action@latest
  with:
    root_file: main.tex
    args: -pdf -interaction=nonstopmode
```

#### Problem: Fehlende Berechtigungen

**Fehler-Meldung:**
```
Error: Resource not accessible by integration
Permission denied to repository
```

**Lösung:**
```yaml
# Berechtigungen am Anfang der Workflow-Datei definieren
permissions:
  contents: read
  actions: write
  pull-requests: write  # Falls PR-Kommentare benötigt
  checks: write         # Falls Status-Checks gesetzt werden
```

### 2. Repository-Berechtigungen

#### Problem: Push/Pull Fehler

**Fehler:**
```bash
fatal: Authentication failed
Permission denied (publickey)
```

**Lösungsschritte:**

1. **Personal Access Token prüfen:**
   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "your.email@example.com"
   ```

2. **SSH-Schlüssel konfigurieren:**
   ```bash
   ssh-keygen -t ed25519 -C "your.email@example.com"
   eval "$(ssh-agent -s)"
   ssh-add ~/.ssh/id_ed25519
   ```

3. **Repository-URL prüfen:**
   ```bash
   git remote -v
   # Sollte HTTPS oder SSH verwenden, nicht gemischt
   ```

### 3. Action-spezifische Probleme

#### Problem: LaTeX Action Fehler

**Fehler:**
```
Error: Could not find root_file: main.tex
```

**Diagnose:**
```bash
# Datei-Pfad prüfen
ls -la main.tex
# Arbeitsverzeichnis prüfen in Action
pwd
```

**Lösung:**
```yaml
- name: Set up LaTeX
  uses: dante-ev/latex-action@latest
  with:
    root_file: ./main.tex  # Expliziter Pfad
    working_directory: .   # Arbeitsverzeichnis setzen
```

#### Problem: Veraltete Action-Versionen

**Symptom:** Deprecated Warnings oder Fehler

**Lösung:** Action-Versionen aktualisieren
```yaml
# ❌ Veraltet
uses: actions/checkout@v3

# ✅ Aktuell  
uses: actions/checkout@v4
```

### 4. Artifact Upload/Download Probleme

#### Problem: PDF-Upload fehlschlägt

**Fehler:**
```
Error: No files were found with the provided path: main.pdf
```

**Diagnose und Lösung:**
```yaml
- name: Debug file location
  run: |
    ls -la
    find . -name "*.pdf" -type f

- name: Upload PDF artifact
  uses: actions/upload-artifact@v4
  with:
    name: CTMM_PDF
    path: |
      main.pdf
      *.pdf
  if: always()  # Upload auch bei Fehlern
```

### 5. Build-System Integration Probleme

#### Problem: Python-Abhängigkeiten fehlen

**Fehler:**
```
ModuleNotFoundError: No module named 'chardet'
```

**Lösung:**
```yaml
- name: Install Python dependencies
  run: |
    pip install --upgrade pip
    pip install chardet
    pip install -r requirements.txt  # Falls vorhanden
```

#### Problem: LaTeX-Pakete fehlen

**Fehler:**
```
! LaTeX Error: File 'package.sty' not found
```

**Lösung:**
```yaml
extra_system_packages: |
  texlive-lang-german
  texlive-fonts-recommended  
  texlive-latex-recommended
  texlive-fonts-extra
  texlive-latex-extra
  texlive-science
  texlive-bibtex-extra      # Falls Bibliography benötigt
  texlive-formats-extra     # Für spezielle Formate
```

## Workflow-Validierung

### 1. Syntax-Prüfung

**Automatische Validierung:**
```bash
# YAML-Syntax prüfen
python3 test_workflow_structure.py

# Oder mit yamllint (falls installiert)
yamllint .github/workflows/
```

**Manuelle Prüfung:**
```bash
# GitHub CLI verwenden
gh workflow view latex-build.yml
gh workflow list
```

### 2. Lokale Simulation

**Act verwenden (GitHub Actions lokal testen):**
```bash
# Installation
npm install -g @nektos/act

# Workflow lokal ausführen
act -j build
```

### 3. Workflow-Debugging

**Debug-Modus aktivieren:**
```yaml
env:
  ACTIONS_STEP_DEBUG: true
  ACTIONS_RUNNER_DEBUG: true
```

**Debug-Ausgaben hinzufügen:**
```yaml
- name: Debug Environment
  run: |
    echo "PWD: $(pwd)"
    echo "Files: $(ls -la)"
    echo "ENV: $(env | sort)"
```

## Berechtigungs-Matrix

### Repository-Level Berechtigungen

| Berechtigung | Benötigt für | Empfehlung |
|--------------|--------------|------------|
| `contents: read` | Repository auschecken | ✅ Immer |
| `contents: write` | Dateien ändern/pushen | ⚠️ Nur bei Bedarf |
| `actions: read` | Action-Status lesen | ✅ Standard |
| `actions: write` | Workflows triggern | ⚠️ Nur für spezielle Workflows |
| `pull-requests: write` | PR-Kommentare | ⚠️ Nur für Bot-Funktionen |
| `checks: write` | Status-Checks setzen | ⚠️ Nur für Quality Gates |

### Workflow-spezifische Berechtigungen

```yaml
# Minimale Berechtigungen für LaTeX-Build
permissions:
  contents: read
  actions: read

# Erweiterte Berechtigungen für CI/CD
permissions:
  contents: read
  actions: write
  pull-requests: write
  checks: write
```

## Sicherheits-Best-Practices

### 1. Secrets Management

**Sichere Secret-Verwendung:**
```yaml
- name: Use secret
  run: echo "${{ secrets.SECRET_NAME }}"
  env:
    SECRET_NAME: ${{ secrets.SECRET_NAME }}
```

**Secrets validieren:**
```yaml
- name: Validate secrets
  run: |
    if [ -z "${{ secrets.REQUIRED_SECRET }}" ]; then
      echo "Required secret is missing"
      exit 1
    fi
```

### 2. Third-Party Actions Sicherheit

**Vertrauenswürdige Actions verwenden:**
```yaml
# ✅ Offizielle GitHub Actions
uses: actions/checkout@v4

# ✅ Verifizierte Actions mit spezifischer Version
uses: dante-ev/latex-action@v2.0.0

# ❌ Unspezifische Versionen vermeiden
uses: some-action@main
```

### 3. Eingabe-Validierung

**User-Input validieren:**
```yaml
- name: Validate input
  run: |
    if [[ ! "${{ github.event.inputs.version }}" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
      echo "Invalid version format"
      exit 1
    fi
```

## Monitoring und Alerts

### 1. Workflow-Monitoring

**Fehlgeschlagene Workflows überwachen:**
```yaml
- name: Notify on failure
  if: failure()
  uses: actions/upload-artifact@v4
  with:
    name: error-logs
    path: |
      *.log
      build_error_*.log
```

### 2. Performance-Monitoring

**Build-Zeiten überwachen:**
```yaml
- name: Record build time
  run: |
    echo "Build started: $(date)"
    # Build commands...
    echo "Build finished: $(date)"
```

## Häufige Fehlermeldungen

### LaTeX-spezifische Fehler

| Fehler | Ursache | Lösung |
|--------|---------|---------|
| `Package inputenc Error` | Encoding-Probleme | UTF-8 verwenden |
| `! Undefined control sequence` | Fehlende Pakete | Package hinzufügen |
| `! Emergency stop` | Syntax-Fehler | LaTeX-Syntax prüfen |

### GitHub Actions Fehler

| Fehler | Ursache | Lösung |
|--------|---------|---------|
| `The run was canceled` | Timeout erreicht | Timeout erhöhen |
| `Resource not accessible` | Fehlende Berechtigungen | Permissions hinzufügen |
| `File not found` | Falscher Pfad | Pfad korrigieren |

## Troubleshooting-Checkliste

### Vor dem Problem-Report

- [ ] Workflow-Syntax mit YAML-Validator geprüft
- [ ] Berechtigungen entsprechend Berechtigungs-Matrix gesetzt
- [ ] Action-Versionen aktualisiert
- [ ] Lokale Build erfolgreich
- [ ] Dependencies in requirements oder workflow definiert

### Problem-Report Template

```markdown
**Beschreibung:** Kurze Beschreibung des Problems

**Workflow-Datei:** `.github/workflows/[datei].yml`

**Fehler-Log:**
```
[Error log hier einfügen]
```

**Environment:**
- Runner: ubuntu-latest/windows-latest/macos-latest
- Python Version: 3.x
- LaTeX Distribution: TeX Live

**Reproduktion:**
1. Schritt 1
2. Schritt 2
3. ...

**Erwartetes Verhalten:** Was sollte passieren

**Tatsächliches Verhalten:** Was passiert tatsächlich
```

## Support-Ressourcen

### GitHub Dokumentation
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [Permissions](https://docs.github.com/en/actions/using-jobs/assigning-permissions-to-jobs)

### CTMM-spezifische Hilfe
```bash
# Build-System Hilfe
python3 ctmm_build.py --help

# Workflow-Tests
python3 test_workflow_structure.py

# LaTeX-Validierung
python3 validate_latex_syntax.py
```

---

**Letzte Aktualisierung:** $(date)  
**Version:** 1.0  
**Kontakt:** CTMM Development Team