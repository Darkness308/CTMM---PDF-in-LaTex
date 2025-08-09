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

**CTMM Build Manager:**

Das Projekt verfügt über ein umfassendes automatisiertes Build-Management-System (`build_manager.py`), das folgende erweiterte Funktionen bietet:

### Automatisierte Build-Verwaltung
```bash
# Hauptbefehl - Umfassende Analyse
python3 build_manager.py

# Oder mit Make-Befehlen
make analyze     # Vollständige Analyse mit ausführlicher Ausgabe
make check       # Schnelle Überprüfung und Build-Test
make build       # PDF erstellen (main.tex)
make build-ci    # CI-Build (main_final.tex)
```

Das Build-Manager-System:
1. **Scannt main.tex** nach allen `\usepackage{style/...}` und `\input{modules/...}` Befehlen
2. **Erkennt fehlende Dateien** automatisch und erstellt minimale, gut strukturierte Templates
3. **Implementiert inkrementelle Tests** die modulspezifische Build-Fehler isolieren
4. **Erstellt umfassende Build-Reports** in `build_report.md`
5. **Bietet robuste Fehlerbehandlung** mit hilfreichen Installationsanleitungen
6. **Erstellt TODO-Dateien** für neue Template-Dateien mit Hinweisen zur Vervollständigung

### Template-Generierungssystem

**Automatische Erstellung:**
- **Style-Pakete** (`.sty`): Korrekt strukturiert mit `\ProvidesPackage` und TODO-Kommentaren
- **Module** (`.tex`): Mit Sections, Labels und Platzhalter-Inhalten
- **TODO-Dateien**: Detaillierte Anleitungen zur Vervollständigung

### Erweiterte Entwicklerworkflow

**Neue Make-Befehle:**
```bash
make help         # Zeigt alle verfügbaren Befehle
make dev-setup    # Komplette Entwicklungsumgebung einrichten
make report       # Aktuellen Build-Report anzeigen
make clean        # Build-Artefakte entfernen
make clean-all    # Alle generierten Dateien entfernen (Vorsicht!)
make deps         # Python-Abhängigkeiten installieren
```

### CI/CD-Verbesserungen

- **`main_final.tex`** dient als dediziertes CI-Build-Ziel
- **GitHub Actions Workflow** wurde repariert und auf `dante-ev/latex-action@v2.0.0` aktualisiert
- **Erweiterte Fehlerberichterstattung** und Artefakt-Sammlung für fehlgeschlagene Builds

### Verwendungsbeispiele

**Neues Modul hinzufügen:**
```bash
# 1. Referenz in main.tex hinzufügen:
\input{modules/mein-neues-modul}

# 2. Build-Manager ausführen:
make check
# oder
python3 build_manager.py

# 3. Automatisch erstellte Dateien:
#    - modules/mein-neues-modul.tex (Template mit Grundstruktur)
#    - modules/TODO_mein-neues-modul.md (Aufgabenliste)

# 4. Inhalt vervollständigen und TODO-Datei entfernen
```

**Fehlersuche:**
```bash
make analyze              # Umfassende Analyse mit inkrementellen Tests
make report              # Build-Report anzeigen
cat build_manager.log    # Detaillierte Protokolle prüfen
cat module_error_*.log   # Spezifische Modulfehler prüfen
```

### Modulare Test-Strategie

**Für Entwickler:**
- **Automatische Erkennung** aller Module und inkrementelle Tests
- **Isolation problematischer Module** durch schrittweise Tests
- **Detaillierte Fehlerprotokolle** für jedes problematische Modul
- **Templates mit sinnvoller Struktur** und ohne Dummy-Content

**Erweiterte Analyse:**
Das neue System ersetzt sowohl `ctmm_build.py` als auch `build_system.py` und bietet:
```bash
python3 build_manager.py --verbose    # Debug-Ausgabe aktivieren
python3 build_manager.py --main-tex myfile.tex  # Andere Hauptdatei verwenden
```

### GitHub Workflow Integration

Das GitHub Actions Workflow (`.github/workflows/latex-build.yml`) wurde verbessert:
- **Korrekte Syntax** und Update auf neueste Action-Version
- **Verwendet `main_final.tex`** als dediziertes CI-Build-Ziel  
- **Lädt `main_final.pdf`** als Artefakt hoch
- **Sammelt umfassende Fehlerprotokolle** bei Build-Fehlern

### Dokumentation

- **`BUILD_GUIDE.md`**: Umfassende Schnellstart-Dokumentation
- **`build_report.md`**: Automatisch generierter detaillierter Build-Report
- **`build_manager.log`**: Vollständige Protokolle aller Build-Operationen

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
