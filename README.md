# CTMM-System - Automated Build Management

Ein modulares LaTeX-Framework für Catch-Track-Map-Match Therapiematerialien mit automatisiertem Build-Management-System.

## Überblick
Dieses Repository enthält ein vollständiges LaTeX-System zur Erstellung von CTMM-Therapiedokumenten, einschließlich:
- Depression & Stimmungstief Module
- Trigger-Management
- Bindungsdynamik
- Formularelemente für therapeutische Dokumentation
- **Automatisiertes Build-Management-System** für nahtlose Entwicklung

## Quick Start

### Entwicklung
```bash
# Umfassende Build-Analyse (EMPFOHLEN)
make analyze
# oder
python3 build_manager.py

# Standard PDF erstellen
make build

# CI-Build für automatisierte Tests
make build-ci

# Aufräumen
make clean
```

### Detaillierte Anleitung
Siehe [`BUILD_GUIDE.md`](BUILD_GUIDE.md) für umfassende Dokumentation.

## Struktur
- `/style/` - Design-Dateien und gemeinsam verwendete Komponenten
- `/modules/` - Individuelle CTMM-Module als separate .tex-Dateien
- `/build_manager.py` - **Hauptsystem** für automatisiertes Build-Management
- `/main_final.tex` - CI-optimierte Build-Zielversion
- `BUILD_GUIDE.md` - Umfassende Build-System-Dokumentation

## Automatisiertes Build-Management-System

### Hauptfunktionen
- **Automatische Abhängigkeitserkennung**: Scannt `main.tex` nach allen Referenzen
- **Template-Generierung**: Erstellt strukturierte Templates für fehlende Dateien
- **Inkrementelle Tests**: Isoliert problematische Module für einfaches Debugging
- **Umfassende Berichte**: Generiert detaillierte `build_report.md`
- **CI/CD Integration**: Dedizierte `main_final.tex` für automatisierte Builds

### Verfügbare Befehle

| Befehl | Beschreibung |
|--------|-------------|
| `make analyze` | **Hauptbefehl** - Umfassende Build-Analyse mit Fehlererkennung |
| `make build` | Standard PDF aus `main.tex` erstellen |
| `make build-ci` | CI PDF aus `main_final.tex` erstellen |
| `make test` | Schneller Test ohne PDF-Generierung |
| `make clean` | Build-Artefakte entfernen |
| `make clean-all` | Alle generierten Dateien entfernen (⚠️ inkl. Templates) |
| `make help` | Vollständige Befehlsreferenz anzeigen |

### Entwickler-Workflow

1. **Neue Module hinzufügen**
   ```latex
   % In main.tex
   \input{modules/neues-modul}
   ```

2. **Analyse ausführen**
   ```bash
   make analyze
   ```

3. **Templates vervollständigen**
   - Datei `modules/neues-modul.tex` bearbeiten
   - Anweisungen in `modules/TODO_neues-modul.md` befolgen
   - TODO-Datei löschen wenn fertig

4. **Testen und Build**
   ```bash
   make build
   ```

## Anforderungen
- Python 3.x mit `chardet` Paket
- LaTeX-Installation:
  - **Ubuntu/Debian**: `sudo apt install texlive-latex-base texlive-latex-extra texlive-fonts-recommended texlive-fonts-extra texlive-lang-german`
  - **MacOS**: `brew install mactex`
  - **Windows**: MiKTeX oder TeX Live Installation
- Oder GitHub Codespace (vorkonfiguriert)

## CI/CD Integration

Das System enthält dedizierte CI/CD-Unterstützung:
- **GitHub Actions**: Automatische Build-Verifikation bei jedem Push/PR
- **Fehlersammlung**: Detaillierte Logs und Berichte bei Build-Fehlern
- **Artefakt-Upload**: Automatischer Upload von PDFs und Build-Berichten

## Template-System

### Automatische Template-Generierung
Fehlende Dateien werden automatisch als strukturierte Templates erstellt:

#### Style-Pakete (`.sty`)
```latex
\NeedsTeXFormat{LaTeX2e}
\ProvidesPackage{paket-name}[datum Beschreibung]
% TODO: Paket-Inhalt hinzufügen
```

#### Module (`.tex`)
```latex
\section{Modul-Titel}
\label{sec:modul-name}
% TODO: Modul-Inhalt hinzufügen
```

### TODO-Dateien
Jedes generierte Template kommt mit einer entsprechenden `TODO_*.md` Datei, die:
- Detaillierte Vervollständigungsanweisungen enthält
- Qualitätskriterien definiert
- Teststrategien vorschlägt
- Nach Fertigstellung gelöscht werden sollte

## Fehlerbehebung

### Build-Fehler diagnostizieren
1. `make analyze` ausführen
2. `build_report.md` prüfen
3. `build_error_*.log` Dateien für spezifische Fehler ansehen
4. Probleme beheben und erneut testen

### Häufige Probleme
- **LaTeX nicht gefunden**: Installation prüfen (siehe Anforderungen)
- **Fehlende Pakete**: `texlive-*` Pakete installieren
- **Build-Fehler**: `make analyze` für detaillierte Diagnose

## Unterstützung und Ressourcen
- **Build-Berichte**: Immer zuerst `build_report.md` prüfen
- **Befehle**: `make help` für vollständige Referenz
- **Dokumentation**: `BUILD_GUIDE.md` für detaillierte Anweisungen
- **Templates**: Anweisungen in `TODO_*.md` Dateien befolgen

## Legacy Build System Notes

### LaTeX-Hinweise für Entwickler

**Typische Fehlerquellen und Best Practices:**

- **Pakete immer in der Präambel laden:**
  - `\usepackage{...}` darf nur in der Hauptdatei (z.B. `main.tex`) vor `\begin{document}` stehen, niemals in Modulen oder nach `\begin{document}`.
- **Makros und Befehle:**
  - Definiere neue Makros (z.B. Checkboxen, Textfelder) zentral in der Präambel oder in einem Style-File, nicht in einzelnen Modulen.
  - Beispiel für Checkboxen:
    ```tex
    % In der Präambel:
    \usepackage{amssymb}
    \newcommand{\checkbox}{$\square$}
    \newcommand{\checkedbox}{$\blacksquare$}
    ```
  - **Wichtig:** Verwende in Modulen und Tabellen ausschließlich die Makros `\checkbox` und `\checkedbox` für Checkboxen. Benutze niemals direkt `\Box` oder `\blacksquare`, da dies zu `Undefined control sequence`-Fehlern führen kann.
- **Module:**
  - Module sollten keine Pakete laden oder globale Makros definieren.
  - Nur Inhalte und Befehle verwenden, die in der Präambel bereitgestellt werden.
- **Fehlermeldungen:**
  - `Can be used only in preamble`: Ein Paket wurde im Fließtext geladen – in die Präambel verschieben!
  - `Undefined control sequence`: Ein Makro ist nicht definiert – Definition prüfen oder in die Präambel verschieben.
  - `Command ... already defined`: Ein Makro wurde doppelt definiert – nur eine Definition behalten (am besten zentral).

### Legacy Build Commands
Das Repository enthält auch ältere Build-Systeme für Kompatibilität:
```bash
python3 ctmm_build.py          # Einfaches Build-System (Legacy)
python3 build_system.py        # Detaillierte Analyse (Legacy)
make check                     # Legacy-Kompatibilität
```
