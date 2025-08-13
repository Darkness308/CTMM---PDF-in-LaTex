# CTMM-System

Ein modulares LaTeX-Framework für Catch-Track-Map-Match Therapiematerialien.

## Überblick
Dieses Repository enthält ein vollständiges LaTeX-System zur Erstellung von CTMM-Therapiedokumenten, einschließlich:
- Depression & Stimmungstief Module
- Trigger-Management
- Bindungsdynamik
- Formularelemente für therapeutische Dokumentation

## Verwendung
1. Klone das Repository
2. Kompiliere main.tex mit einem LaTeX-Editor
3. Oder öffne das Projekt in einem GitHub Codespace

## Struktur
- `/style/` - Design-Dateien und gemeinsam verwendete Komponenten
- `/modules/` - Individuelle CTMM-Module als separate .tex-Dateien
- `/assets/` - Diagramme und visuelle Elemente

## Anforderungen
- LaTeX-Installation mit TikZ und hyperref
- Oder GitHub Codespace (vorkonfiguriert)

## LaTeX-Hinweise für Entwickler

**CTMM Build System:**

Das Projekt verfügt über ein automatisches Build-System (`ctmm_build.py`), das folgende Funktionen bietet:

### Automatisierte Build-Prüfung
```bash
# Standard Build-System Check
python3 ctmm_build.py

# Umfassende Build-Analyse (NEU!)
python3 build_manager.py
# oder
make comprehensive
```

Das Build-System:
1. **Scannt main.tex** nach allen `\usepackage{style/...}` und `\input{modules/...}` Befehlen
2. **Prüft Dateiexistenz** - erstellt minimale Templates für fehlende Dateien
3. **Testet Grundgerüst** - Build ohne Module zum Testen der Basis-Struktur
4. **Testet vollständigen Build** - mit allen Modulen
5. **Erstellt TODO-Dateien** für neue Template-Dateien mit Hinweisen zur Vervollständigung

### Neues Comprehensive Build Management

Das neue `build_manager.py` bietet erweiterte Funktionen:

**Incremental Testing Strategy:**
- Tests basic framework (ohne Module)
- Tests Module einzeln, um spezifische Fehler zu isolieren
- Strukturierte Schritt-für-Schritt-Analyse
- Automatische Backup/Restore Funktionalität

**Sophisticated Error Detection:**
- Konsistente `[INFO]` Log-Formatierung
- Detaillierte Fehleranalyse und -kategorisierung
- Automatische LaTeX-Installation-Hinweise
- Umfassende Build-Reports (Markdown-Format)

**Template Generation:**
- Automatische Erstellung von `.sty` Style-Package Templates
- Automatische Erstellung von `.tex` Modul Templates
- TODO-Kommentare und Struktur-Hilfen
- Integration mit vorhandenem Build-System

### Unit Tests

Das Build-System enthält Unit Tests für kritische Funktionen:

```bash
# Alle Unit Tests ausführen
make unit-test

# Nur ctmm_build.py Tests
python3 test_ctmm_build.py

# Nur build_manager.py Tests (NEU!)
python3 test_build_manager.py
# oder
make test-manager
```

Die Tests überprüfen:
- `filename_to_title()` Funktion mit verschiedenen Eingabeformaten
- **Build Manager Funktionalität:** datetime import, konsistente Log-Formatierung, Template-Erstellung
- **Integration Tests:** Schritt-Nummerierung, Backup/Restore, Incremental Testing

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

**Tipp:**
Wenn du ein neues Modul schreibst, prüfe, ob du neue Pakete oder Makros brauchst – und ergänze sie zentral, nicht im Modul selbst.
