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

## 🎯 CTMM Comprehensive Toolset - "es ist nicht mehr weit"

**Status**: ✅ **COMPLETE AND OPERATIONAL**

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

### LaTeX Escaping Fix Tool

Das Projekt enthält ein spezielles Tool zur Behebung von übermäßig escapierten LaTeX-Befehlen, die durch Dokumentkonvertierungstools entstehen können:

**Grundlegende Verwendung:**
```bash
# Dateien direkt reparieren (in-place)
python3 fix_latex_escaping.py converted/

# Reparierte Kopien in neuem Verzeichnis erstellen
python3 fix_latex_escaping.py converted/ fixed/

# Mit Backup-Erstellung für Sicherheit
python3 fix_latex_escaping.py --backup converted/

# Validierung nach der Reparatur
python3 fix_latex_escaping.py --validate converted/

# Detaillierte Ausgabe für Debugging
python3 fix_latex_escaping.py --verbose converted/
```

**Behandelte Probleme:**
- `\textbackslash{}` Sequenzen → saubere LaTeX-Befehle
- Überkomplexe Hypertarget-Strukturen → vereinfachte Sektionen
- Doppelt-escapierte Zeichen → korrekte LaTeX-Syntax
- Auto-generierte Labels → lesbare Referenzen

**Integration in den Workflow:**
```bash
# Nach Dokumentkonvertierung ausführen
pandoc document.md -o converted/document.tex
python3 fix_latex_escaping.py --backup converted/

# In Build-Prozess integrieren
python3 fix_latex_escaping.py converted/ && python3 ctmm_build.py
```

Siehe [README_DE_ESCAPING.md](README_DE_ESCAPING.md) für ausführliche Dokumentation und Beispiele.

### Unit Tests

Das Build-System enthält Unit Tests für kritische Funktionen:

```bash
# Python-Unit-Tests ausführen
make unit-test
# oder direkt:
python3 test_ctmm_build.py
python3 test_latex_validator.py
```

Die Tests überprüfen:
- `filename_to_title()` Funktion mit verschiedenen Eingabeformaten
- LaTeX-Validator Funktionalität
- Escaping-Problem Erkennung und Behebung

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
