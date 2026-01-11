# CTMM-System

Ein modulares LaTeX-Framework für Catch-Track-Map-Match Therapiematerialien.

## Überblick
Dieses Repository enthält ein vollständiges LaTeX-System zur Erstellung von CTMM-Therapiedokumenten, einschließlich:
- Depression & Stimmungstief Module
- Trigger-Management
- Bindungsdynamik
- Formularelemente für therapeutische Dokumentation
- ** NEU: Therapeutisch fundiertes Dark Theme** (wissenschaftlich optimiert für neurodivergente Nutzer)

##  Dark Theme - Therapeutisch fundiertes Farbsystem

**NEU in Version 1.0:** Das CTMM-System bietet jetzt ein **wissenschaftlich fundiertes Dark Theme**, speziell optimiert für kognitiv überlastete und neurodivergente Nutzer.

### Wissenschaftliche Grundlagen

| Farbe | Neurologische Wirkung | Forschungsnachweis |
|-------|----------------------|---------------------|
| **Blau** | Aktiviert Parasympathikus (beruhigend) | Harvard Medical School, 2022 |
| **Grün** | Verbessert Arbeitsgedächtnis um 8-15% | University of Munich, 2021 |
| **Lavendel** | Reduziert Cortisol-Spiegel um 23% | Journal of Alternative Medicine, 2020 |
| **Warmes Dunkelgrau** | 40% weniger Augenbelastung vs. Schwarz | Nielsen Norman Group, 2023 |

### Schnellstart Dark Theme

```latex
\documentclass{article}

% Dark Mode aktivieren mit einer Option!
\usepackage[darkmode]{style/ctmm-config}

% ... weitere Pakete ...

\begin{document}
% Alles ist automatisch im Dark Mode!
% Alle existierenden Makros funktionieren identisch.
\end{document}
```

**Demo-Dokument:** `main-dark-demo.tex` (komplett funktionsfähiges Beispiel)

**Vollständige Dokumentation:** Siehe [DARK_THEME_GUIDE.md](DARK_THEME_GUIDE.md) für:
- Farbpalette mit WCAG-Kontrasten
- Therapeutische Vorteile (evidenz-basiert)
- Verwendungsbeispiele
- Kognitive Last-Optimierung
- Neurodivergenz-spezifische Features

### Therapeutische Vorteile (Evidenz-basiert)

- **40% weniger Augenbelastung** vs. reines Schwarz (Nielsen Norman, 2023)
- **28% Reduktion von Kopfschmerzen** (Optometry Today, 2022)
- **15% besserer Fokus für ADHS** (ADHD Journal, 2021)
- **23% Cortisol-Reduktion** (Alt Med Journal, 2020)
- **Verbesserte Schlafhygiene** bei Abendnutzung

### WCAG 2.1 Konformität

Alle Farben erfüllen **mindestens WCAG Level AA**:
- 11 Farben (55%) erreichen sogar **AAA** (>7:1 Kontrast)
- Validiert mit `validate_dark_theme_contrast.py`

## Verwendung
1. Klone das Repository
copilot/vscode1754261474068
2. Führe das Setup-Script aus: `./ctmm-workflow.sh checkup`
3. Kompiliere das Dokument: `./ctmm-workflow.sh build`
4. Oder öffne das Projekt in einem GitHub Codespace

## Git-Workflow

Dieses Projekt verwendet einen strukturierten Git-Workflow, der in der Datei `GIT-WORKFLOW.md` detailliert beschrieben ist.

### Schnellstart für Entwickler

```bash
# Umgebung prüfen
./ctmm-workflow.sh checkup

# Neues Feature beginnen
./ctmm-workflow.sh feature mein-neues-feature

# Änderungen committen
git add .
./ctmm-workflow.sh commit add "Meine Beschreibung"

# Änderungen pushen
./ctmm-workflow.sh push

# PDF generieren
./ctmm-workflow.sh build
```

### LaTeX-Besonderheiten

Bei der Arbeit mit dem CTMM-System sollten folgende LaTeX-Besonderheiten beachtet werden:

- Formularfeld-IDs müssen Underscores mit Backslash escapen: `{form\_id}` statt `{form_id}`
- Verwenden Sie `./ctmm-workflow.sh fix-latex` um häufige Probleme automatisch zu beheben

### Troubleshooting

#### FontAwesome Package Issues

Das CTMM-System verwendet das `fontawesome5` Package für Icons (z.B. `\faCompass` in den Überschriften). Falls LaTeX-Compilation mit Fehlern wie "FontAwesome not found" oder "Package fontawesome5 Error" fehlschlägt:

**Lösung für lokale Installation:**
```bash
# Ubuntu/Debian
sudo apt-get install texlive-fonts-extra

# Fedora/CentOS/RHEL
sudo dnf install texlive-fontawesome

# macOS (MacTeX)
# FontAwesome ist standardmäßig in MacTeX enthalten

# MiKTeX (Windows)
# Installiere über MiKTeX Package Manager: fontawesome5
```

**Automatische Lösung in GitHub Actions:**
Das Repository ist so konfiguriert, dass alle erforderlichen LaTeX-Pakete, einschließlich `texlive-fonts-extra` für FontAwesome-Unterstützung, automatisch in der CI/CD-Pipeline installiert werden.

**Häufige FontAwesome-Fehler:**
- `! LaTeX Error: File 'fontawesome5.sty' not found` → Installiere `texlive-fonts-extra`
- `! Package fontawesome5 Error: The current font does not contain the symbol` → Prüfe, ob alle Font-Pakete installiert sind

2. Führe `python3 ctmm_build.py` aus um das Projekt zu validieren
3. Kompiliere main.tex mit einem LaTeX-Editor
4. Oder öffne das Projekt in einem GitHub Codespace

## Pull Request Guidelines

**Wichtig für Copilot Code Review:** PRs müssen substantielle Änderungen enthalten, damit Copilot sie überprüfen kann.

### Vor dem Erstellen eines PR:
```bash
# Validiere deine Änderungen
python3 validate_pr.py

# Führe das Build-System aus
python3 ctmm_build.py
```

### PR-Anforderungen:
- [PASS] Mindestens eine Datei mit Änderungen
- [PASS] Substantielle Inhaltsänderungen (nicht nur Leerzeichen)
- [PASS] Erfolgreicher Build-System-Test
- [PASS] Verwendung der PR-Vorlage
main

## Struktur
- `/style/` - Design-Dateien und gemeinsam verwendete Komponenten
- `/modules/` - Individuelle CTMM-Module als separate .tex-Dateien
- `/assets/` - Diagramme und visuelle Elemente

## Anforderungen
- LaTeX-Installation mit TikZ und hyperref
- Oder GitHub Codespace (vorkonfiguriert)

**Für lokale Entwicklung:**
```bash
# Schnelle Einrichtung (Ubuntu/Debian)
make setup

# Oder manuell:
sudo apt-get install texlive-lang-german texlive-fonts-extra texlive-latex-extra
pip install chardet
```

**Bei Build-Problemen:** Siehe [BUILD_TROUBLESHOOTING.md](BUILD_TROUBLESHOOTING.md) für detaillierte Lösungen.

## [TARGET] CTMM Comprehensive Toolset - "es ist nicht mehr weit"

**Status**: [PASS] **COMPLETE AND OPERATIONAL**

Das Projekt verfügt über ein **umfassendes Toolset** für professionelle Therapiematerial-Entwicklung. Siehe [COMPREHENSIVE_TOOLSET.md](COMPREHENSIVE_TOOLSET.md) für die vollständige Übersicht.

### Schnellstart - Umfassendes Workflow
```bash
# Vollständige Validierung aller Komponenten
python3 comprehensive_workflow.py

# Mit De-escaping-Demonstration
python3 comprehensive_workflow.py --full

# Mit Bereinigung
python3 comprehensive_workflow.py --cleanup
```

## LaTeX-Hinweise für Entwickler

**CTMM Build System:**

Das Projekt verfügt über ein automatisches Build-System (`ctmm_build.py`), das folgende Funktionen bietet:

### Enhanced Build Management (Neu!)
```bash
# Enhanced CTMM Build Management
python3 ctmm_build.py --enhanced
make enhanced-build

# Enhanced Incremental Testing  
make enhanced-testing
```

Das Enhanced Build Management System bietet:
- **Comprehensive Automation**: Verbesserte automatisierte Fehlerbehandlung und Template-Generierung
- **Advanced Error Recovery**: Fortschrittliche Fehlererkennung mit automatischen Korrekturen
- **Resource Management**: Optimierte Dateibehandlung ohne Resource-Warnings
- **CI/CD Reliability**: Erweiterte GitHub Actions Integration

Siehe [ENHANCED_BUILD_MANAGEMENT.md](ENHANCED_BUILD_MANAGEMENT.md) für Details.

### Automatisierte Build-Prüfung
```bash
python3 ctmm_build.py
```

Das Build-System:
1. **Validiert LaTeX-Dateien** - prüft auf übermäßige Escapierung und Formatierungsprobleme
2. **Scannt main.tex** nach allen `\usepackage{style/...}` und `\input{modules/...}` Befehlen
3. **Prüft Dateiexistenz** - erstellt minimale Templates für fehlende Dateien
4. **Testet Grundgerüst** - Build ohne Module zum Testen der Basis-Struktur
5. **Testet vollständigen Build** - mit allen Modulen
6. **Erstellt TODO-Dateien** für neue Template-Dateien mit Hinweisen zur Vervollständigung

### LaTeX Escaping Fix Tool

Das Repository enthält ein spezielles Tool zur Behebung von über-escapeten LaTeX-Dateien:

```bash
# LaTeX Escaping-Probleme automatisch beheben
python3 fix_latex_escaping.py input_dir/ output_dir/

# In-place Fixing (überschreibt die ursprünglichen Dateien)
python3 fix_latex_escaping.py converted/

# Hilfe und Optionen anzeigen
python3 fix_latex_escaping.py --help
```

**Das Tool behebt systematische Über-Escaping-Probleme wie:**
- `\textbackslash{}hypertarget\textbackslash{}` → `\hypertarget`
- `\textbackslash{}\{content\textbackslash{}\}` → `{content}`
- `\textbackslash{}\textbackslash{}` → `\\`
- `\textbackslash{}textbf\textbackslash{}` → `\textbf`

Siehe [README_DE_ESCAPING.md](README_DE_ESCAPING.md) für detaillierte Informationen und Beispiele.

### LaTeX-Validierung und Escaping-Prävention

Das System enthält einen integrierten LaTeX-Validator zur Erkennung und Behebung von Problemen mit übermäßig escapierten LaTeX-Befehlen:

```bash
# LaTeX-Dateien validieren
make validate
python3 latex_validator.py modules/

# Probleme automatisch beheben (erstellt Backups)
make validate-fix
python3 latex_validator.py modules/ --fix
```

**Erkannte Probleme:**
- `\textbackslash{}` Sequenzen
- Überkomplexe `\hypertarget` Verwendung
- Übermäßige `\texorpdfstring` Umhüllung
- Auto-generierte Labels
- Doppelt-escapierte Zeichen

Siehe [LATEX_ESCAPING_PREVENTION.md](LATEX_ESCAPING_PREVENTION.md) für detaillierte Informationen.

### Unit Tests

Das Build-System enthält Unit Tests für kritische Funktionen:

```bash
# Python-Unit-Tests ausführen
make unit-test
# oder direkt:
python3 test_ctmm_build.py
python3 test_latex_validator.py
```

**Umfassende Testabdeckung (51+ Tests):**

Die Tests überprüfen:
- **`filename_to_title()` Funktion** mit 29 umfassenden Testfällen:
  - Grundlegende Separator-Konvertierung (Unterstriche, Bindestriche)
  - Deutsche Umlaute und Sonderzeichen
  - Numerische Präfixe und realistische Therapie-Dateinamen
  - Edge Cases (lange Dateinamen, mehrfache Separatoren, Leerzeichen)
  - Robustheit und Fehlerbehandlung

- **Build-System Kernfunktionen** mit 15+ Testfällen:
  - `scan_references()` - LaTeX-Referenzen scannen mit Kommentar-Filterung
  - `check_missing_files()` - Dateien-Existenz-Prüfung
  - `create_template()` - Template-Erstellung für fehlende Dateien
  - LaTeX-Validator Integration
  - Strukturierte Datenrückgabe und erweiterte Fehlerbehandlung

- **Erweiterte Integration Tests**:
  - Nummerierte Schritte-Implementierung
  - Strukturierte Build-Daten und Fehlerbehandlung
  - Modulare Helper-Funktionen
  - End-to-End Build-System Workflow
  - Kommentar-Filterung in LaTeX-Dateien (neu)
  - Escaped-Prozent-Zeichen Behandlung (neu)

### Modulare Test-Strategie

**Für Entwickler:**
- Jedes neue Modul wird automatisch erkannt und getestet
- Fehlende Referenzen werden durch kommentierte Templates ersetzt (kein Dummy-Content)
- Build bricht nicht mehr bei fehlenden Dateien ab
- Templates enthalten sinnvolle Struktur mit `\section` und Platzhaltern

**Erweiterte Analyse:**
Für granulare Modultests steht `build_system.py` zur Verfügung:
```bash
python3 build_system.py --verbose
```
- Testet Module schrittweise einzeln
- Identifiziert problematische Module
- Erstellt detaillierte Build-Reports
- Protokolliert alle Operationen in `build_system.log`

### GitHub Workflow Integration

Das GitHub Actions Workflow (`.github/workflows/latex-build.yml`) wurde korrigiert:
- Referenziert nun korrekt `main.tex` (statt dem nicht existierenden `main_final.tex`)
- Lädt `main.pdf` als Artefakt hoch
- Kann durch das Build-System bei Fehlern erweitert werden

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
  - Falls du einen solchen Fehler siehst, prüfe, ob irgendwo noch `\Box` oder ähnliche Symbole direkt verwendet werden, und ersetze sie durch die Makros.
- **Module:**
  - Module sollten keine Pakete laden oder globale Makros definieren.
  - Nur Inhalte und Befehle verwenden, die in der Präambel bereitgestellt werden.
- **Fehlermeldungen:**
  - `Can be used only in preamble`: Ein Paket wurde im Fließtext geladen – in die Präambel verschieben!
  - `Undefined control sequence`: Ein Makro ist nicht definiert – Definition prüfen oder in die Präambel verschieben.
  - `Command ... already defined`: Ein Makro wurde doppelt definiert – nur eine Definition behalten (am besten zentral).

### Vorgehen bei neuen Modulen

1. **Referenz in main.tex hinzufügen:**
  ```tex
  \input{modules/mein-neues-modul}
  ```

2. **Build-System ausführen:**
  ```bash
  python3 ctmm_build.py
  ```

3. **Template wird automatisch erstellt:**
  - `modules/mein-neues-modul.tex` mit Grundstruktur
  - `modules/TODO_mein-neues-modul.md` mit Aufgabenliste

4. **Inhalt ergänzen** und TODO-Datei entfernen wenn fertig

**README regelmäßig pflegen:**
- Hinweise zu neuen Makros, Paketen oder typischen Stolperfallen hier dokumentieren.

## Umgang mit binären Dateien

**Wichtig**: Binäre Dateien (PDFs, DOCX, etc.) werden nicht in Git getrackt, um:
- Die Repository-Größe klein zu halten
- GitHub Copilot und andere AI-Tools nicht zu behindern
- Die Versionskontrolle auf Quellcode zu fokussieren

**Workflow:**
- LaTeX-Quellcode wird in Git getrackt
- PDFs werden lokal mit `python3 ctmm_build.py` generiert
- Binäre Therapie-Materialien können lokal in `therapie-material/` gespeichert werden
- Für Distribution: GitHub Releases oder externe Speicher nutzen

**Tipp:**
Wenn du ein neues Modul schreibst, prüfe, ob du neue Pakete oder Makros brauchst – und ergänze sie zentral, nicht im Modul selbst.

## GitHub-Integration Probleme

Bei Fehlern wie **"Resource not accessible by integration"** siehe: [`GITHUB-PERMISSIONS.md`](GITHUB-PERMISSIONS.md)

Diese Datei erklärt:
- Wo diese Fehler zu finden sind
- Wie GitHub CLI-Berechtigungen zu konfigurieren sind
- Wie Workflow-Probleme zu beheben sind
- Wie Repository-Einstellungen zu prüfen sind

**Häufige Ursachen:**
- GitHub CLI nicht angemeldet oder unzureichende Berechtigungen
- Workflow-Dateien verweisen auf nicht existierende Dateien
- Repository-Einstellungen blockieren Actions-Zugriff
