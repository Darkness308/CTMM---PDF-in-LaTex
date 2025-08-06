# CTMM-System

Ein modulares LaTeX-Framework für Catch-Track-Map-Match Therapiematerialien.

## Überblick
Dieses Repository enthält ein vollständiges LaTeX-System zur Erstellung von CTMM-Therapiedokumenten, einschließlich:
- Depression & Stimmungstief Module
- Trigger-Management
- Bindungsdynamik
- Formularelemente für therapeutische Dokumentation

## Build-System und Testing-Strategie

### Automatisierte Build-Verwaltung

Das Repository verfügt über ein automatisiertes Build-Management-System, das folgende Funktionen bietet:

1. **Vollständige Referenz-Analyse**: Scannt `main.tex` nach allen `\usepackage{style/...}` und `\input{modules/...}` Befehlen
2. **Fehlende Dateien-Erkennung**: Prüft automatisch, ob alle referenzierten Dateien existieren
3. **Template-Generierung**: Erstellt minimale, kommentierte Templates für fehlende Dateien
4. **Inkrementelle Testing**: Testet Module schrittweise durch temporäres Auskommentieren
5. **Detaillierte Berichte**: Generiert umfassende Build-Berichte mit Fehleranalyse

### Verwendung des Build-Managers

```bash
# Vollständige Build-Analyse ausführen
python3 build_manager.py

# Oder mit Makefile
make analyze

# Spezifische Datei testen
make test-file FILE=main.tex

# Standard Build
make build

# CI Build (für GitHub Actions)
make build-ci
```

### Build-Strategie

Das Build-System implementiert eine **granulare Testing-Strategie**:

1. **Grundgerüst-Test**: Alle Module werden temporär auskommentiert, nur das Grundgerüst wird getestet
2. **Inkrementelle Aktivierung**: Module werden einzeln reaktiviert und getestet
3. **Fehler-Isolation**: Jedes Modul, das Fehler verursacht, wird identifiziert und protokolliert
4. **Automatische Wiederherstellung**: Die ursprüngliche `main.tex` wird immer wiederhergestellt

### Template-System

Für fehlende Dateien werden automatisch erstellt:

**Style-Pakete (.sty)**:
- Vollständige `\ProvidesPackage` Struktur
- TODO-Kommentare für alle Bereiche
- Platzhalter-Definitionen

**Module (.tex)**:
- Automatische `\section` mit korrektem Label
- TODO-Kommentare für Inhalte
- Konsistente Struktur

### Fehlerbehandlung

Das System erkennt und behandelt:
- **Fehlende Dateien**: Automatische Template-Erstellung
- **Build-Fehler**: Detaillierte Protokollierung mit Kontext
- **Referenz-Probleme**: Identifizierung defekter Cross-References
- **Encoding-Probleme**: Robuste UTF-8 Behandlung

## Verwendung
1. Klone das Repository
2. Kompiliere main.tex mit einem LaTeX-Editor
3. Oder öffne das Projekt in einem GitHub Codespace
4. Nutze das Build-Management-System für automatisierte Tests

## Struktur
- `/style/` - Design-Dateien und gemeinsam verwendete Komponenten
- `/modules/` - Individuelle CTMM-Module als separate .tex-Dateien
- `/assets/` - Diagramme und visuelle Elemente
- `build_manager.py` - Automatisiertes Build-Management-System
- `Makefile` - Build-Automatisierung und Testing
- `build_report.md` - Automatisch generierte Build-Berichte

## Anforderungen
- LaTeX-Installation mit TikZ und hyperref
- Python 3.x für Build-Management
- Oder GitHub Codespace (vorkonfiguriert)

## LaTeX-Hinweise für Entwickler

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
- **README regelmäßig pflegen:**
  - Hinweise zu neuen Makros, Paketen oder typischen Stolperfallen hier dokumentieren.

**Automatisierte Qualitätssicherung:**

Das Build-Management-System hilft bei der Einhaltung dieser Best Practices:
- Automatische Erkennung fehlender Referenzen
- Granulare Testing verhindert großflächige Build-Fehler
- Template-System sorgt für konsistente Struktur
- Detaillierte Berichte ermöglichen schnelle Fehlerbehebung

**Tipp:**
Wenn du ein neues Modul schreibst, prüfe, ob du neue Pakete oder Makros brauchst – und ergänze sie zentral, nicht im Modul selbst. Nutze das Build-Management-System, um deine Änderungen automatisch zu testen.
