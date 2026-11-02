# GitHub Copilot für Git

Diese Dokumentation beschreibt, wie Sie den GitHub Copilot für Git im CTMM-Projekt effektiv nutzen können.

## Was ist GitHub Copilot für Git?

GitHub Copilot für Git ist ein KI-Assistent, der Sie bei Git-Operationen unterstützt. Er kann:

- Commit-Nachrichten vorschlagen
- Code-Änderungen analysieren
- Pull-Request-Beschreibungen erstellen
- Branch-Namen empfehlen
- Bei der Behebung von Merge-Konflikten helfen

## Installation und Einrichtung

### Voraussetzungen

- GitHub CLI (`gh`) installiert
- GitHub Copilot-Abonnement
- Ein Terminal oder eine Konsole

### Schritt 1: GitHub CLI installieren (falls noch nicht vorhanden)

```bash
# Für Ubuntu/Debian
sudo apt install gh

# Für macOS
brew install gh

# Für Windows (mit Chocolatey)
choco install gh
```

### Schritt 2: Bei GitHub CLI anmelden

```bash
gh auth login
```

Folgen Sie den Anweisungen und authentifizieren Sie sich bei GitHub.

### Schritt 3: GitHub Copilot CLI-Erweiterung installieren

```bash
gh extension install github/gh-copilot
```

### Schritt 4: Einrichtung abschließen

```bash
gh copilot auth
```

## Verwendung im CTMM-Projekt

### Commit-Nachrichten generieren lassen

Nach dem Hinzufügen von Änderungen mit `git add`:

```bash
gh copilot suggest -t "commit"
```

### Pull-Request-Beschreibung generieren

```bash
gh copilot suggest -t "pr"
```

### Merge-Konflikte auflösen

```bash
gh copilot suggest -t "resolve"
```

### Hilfe bei Git-Befehlen bekommen

```bash
gh copilot explain "git rebase -i HEAD~3"
```

## Integration in den CTMM-Workflow

Das `ctmm-workflow.sh`-Script enthält bereits Funktionen für den grundlegenden Git-Workflow. Für komplexere Git-Operationen können Sie GitHub Copilot für Git als Unterstützung verwenden:

1. Erstellen Sie einen Feature-Branch mit unserem Script:
  ```bash
  ./ctmm-workflow.sh feature neues-feature
  ```

2. Machen Sie Ihre Änderungen und fügen Sie sie hinzu:
  ```bash
  git add .
  ```

3. Lassen Sie sich eine Commit-Nachricht generieren:
  ```bash
  gh copilot suggest -t "commit"
  ```

4. Pushen Sie den Branch:
  ```bash
  ./ctmm-workflow.sh push
  ```

5. Lassen Sie sich eine PR-Beschreibung generieren:
  ```bash
  gh copilot suggest -t "pr"
  ```

## Beispiel-Workflow

```bash
# Neues Feature beginnen
./ctmm-workflow.sh feature neues-module

# Änderungen vornehmen...
# [Bearbeiten Sie die LaTeX-Dateien]

# Änderungen hinzufügen
git add .

# Commit-Nachricht generieren
gh copilot suggest -t "commit"

# Änderungen pushen
./ctmm-workflow.sh push

# PR-Beschreibung generieren
gh copilot suggest -t "pr"
```

## Tipps für die effektive Nutzung

1. **Kontext bereitstellen**: Je mehr Kontext Sie GitHub Copilot für Git geben, desto besser werden die Vorschläge.

2. **Vorschläge überprüfen**: Überprüfen Sie immer die generierten Vorschläge, bevor Sie sie verwenden.

3. **Iteratives Arbeiten**: Wenn ein Vorschlag nicht Ihren Erwartungen entspricht, können Sie ihn verfeinern und erneut generieren lassen.

4. **Mit dem Team abstimmen**: Stellen Sie sicher, dass alle Teammitglieder wissen, dass Sie GitHub Copilot für Git verwenden, damit sie mit dem Workflow vertraut sind.
