# GitHub-Berechtigungen und Integration-Probleme

## Problem: "Resource not accessible by integration"

Dieser Fehler tritt auf, wenn GitHub-Aktionen oder CLI-Tools nicht ausreichende Berechtigungen haben, um auf Ressourcen zuzugreifen.

## Wo finde ich diesen Fehler?

### 1. GitHub Actions Workflows
- **Workflow-Läufe**: Repository → Actions → Workflow auswählen → Fehlgeschlagenen Lauf öffnen
- **Job-Logs**: Im fehlgeschlagenen Job die Logs erweitern
- **Fehlerdetails**: Rote Fehlermeldungen in den Logs suchen

### 2. GitHub CLI (gh)
```bash
# GitHub CLI Status prüfen
gh auth status

# GitHub CLI Login mit erweiterten Berechtigungen
gh auth login --scopes repo,workflow,admin:repo_hook
```

### 3. Repository-Einstellungen
- **Settings** → **Actions** → **General**
- **Workflow permissions** prüfen:
  - [PASS] "Read and write permissions" aktivieren
  - [PASS] "Allow GitHub Actions to create and approve pull requests" aktivieren

## Häufige Ursachen und Lösungen

### Workflow-Berechtigungen
```yaml
# In .github/workflows/*.yml
permissions:
  contents: write
  actions: write
  packages: write
  pull-requests: write
```

### Token-Berechtigungen
- **Personal Access Token (PAT)**: GitHub → Settings → Developer settings → Personal access tokens
- **Erforderliche Scopes**:
  - `repo` (Repository-Zugriff)
  - `workflow` (Workflow-Verwaltung)
  - `write:packages` (Pakete veröffentlichen)

### Repository-spezifische Probleme
1. **Geschützte Branches**: Branch-Protection-Rules können Aktionen blockieren
2. **Organisationsrichtlinien**: Enterprise-Richtlinien können Berechtigungen einschränken
3. **Fork-Beschränkungen**: Forks haben standardmäßig eingeschränkte Berechtigungen

## Debugging-Schritte

### 1. Workflow-Logs überprüfen
```bash
# Mit GitHub CLI
gh run list --limit 10
gh run view <run-id> --log
```

### 2. Berechtigungen testen
```bash
# Repository-Zugriff testen
gh repo view
gh api user

# Workflow-Berechtigungen testen
gh workflow list
```

### 3. Artifact-Zugriff
- **Problem**: Artifacts sind nicht zugänglich
- **Lösung**: Workflow muss erfolgreich abgeschlossen sein
- **Check**: Repository → Actions → Workflow → Artifacts

## Spezifische Fixes für dieses Repository

### LaTeX-Workflow-Problem
Das ursprüngliche Problem war:
- Workflow verwies auf nicht existierende `main_final.tex`
- Build schlug fehl → Artifacts wurden nicht erstellt
- "Resource not accessible" beim Versuch, nicht existierende Artifacts zu laden

**Fix**: Workflow-Datei korrigiert, um `main.tex` zu verwenden.

### Berechtigungen für PDF-Artifacts
```yaml
# Korrekte Workflow-Konfiguration
permissions:
  contents: read
  actions: write
  
jobs:
  build:
  runs-on: ubuntu-latest
  steps:
  - name: Upload PDF artifact
  uses: actions/upload-artifact@v4
  with:
  name: CTMM_PDF
  path: main.pdf
  retention-days: 30
```

## Weitere Hilfe

- **GitHub Docs**: https://docs.github.com/en/actions/security-guides/automatic-token-authentication
- **CLI Docs**: https://cli.github.com/manual/gh_auth_login
- **Workflow Permissions**: https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#permissions