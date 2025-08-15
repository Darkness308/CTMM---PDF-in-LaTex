# CTMM Module Generator

Ein automatisiertes System zur Erstellung von therapeutischen LaTeX-Modulen für das CTMM (Catch-Track-Map-Match) System.

## Überblick

Der CTMM Module Generator ermöglicht die schnelle und standardisierte Erstellung von drei Arten therapeutischer Module:

- **📝 Arbeitsblätter** - Interaktive therapeutische Arbeitsblätter mit Reflexionsfragen
- **🔧 Tools** - Therapeutische Techniken und Übungen mit Schritt-für-Schritt Anleitungen
- **🆘 Notfallkarten** - Krisenhilfe-Karten mit Sofortmaßnahmen

## Verwendung

### 1. Interaktiver Modus (Empfohlen)

**Shell Script (einfach):**
```bash
./create-module.sh
```

**JavaScript Generator (vollständig):**
```bash
node module-generator.js
```

Beide Modi führen Sie durch einen interaktiven Dialog zur Modulerstellung.

### 2. Kommandozeilen-Modus

**Schnelle Template-Erstellung:**
```bash
node module-generator.js <typ> <dateiname>
```

**Beispiele:**
```bash
node module-generator.js arbeitsblatt stimmungscheck
node module-generator.js tool atemtechnik  
node module-generator.js notfallkarte panikattacken
```

### 3. VS Code Integration

Über die Command Palette (`Ctrl+Shift+P`):
- `Tasks: Run Task` → `CTMM: Create Module (Interactive)`
- `Tasks: Run Task` → `CTMM: Generate Arbeitsblatt`
- `Tasks: Run Task` → `CTMM: Generate Tool`
- `Tasks: Run Task` → `CTMM: Generate Notfallkarte`

## Modul-Typen

### 📝 Arbeitsblatt (arbeitsblatt)

**Verwendung:** Therapeutische Selbstreflexion und Übungen

**Enthält:**
- Titel und Beschreibung
- Anleitung zur Verwendung
- Reflexionsfragen
- Interaktive Formularfelder
- Platz für Notizen
- Datum und Unterschrift

**Beispiel-Template:**
```tex
\section{Mein Arbeitsblatt}
\begin{ctmmBlueBox}{Arbeitsblatt: Titel}
    Beschreibung des Arbeitsblattes
\end{ctmmBlueBox}
```

### 🔧 Tool (tool)

**Verwendung:** Therapeutische Techniken und Methoden

**Enthält:**
- Titel und Anwendungsbereich
- Schritt-für-Schritt Anleitung
- Praktische Tipps
- Platz für persönliche Erfahrungen

**Beispiel-Template:**
```tex
\section{Mein Tool}
\begin{ctmmGreenBox}{Therapeutisches Tool}
    Beschreibung der Technik
\end{ctmmGreenBox}
```

### 🆘 Notfallkarte (notfallkarte)

**Verwendung:** Krisenhilfe und Sofortmaßnahmen

**Enthält:**
- Titel und Krisenbeschreibung
- 5 konkrete Sofortmaßnahmen
- Wichtige Kontakte
- Platz für persönliche Notizen

**Beispiel-Template:**
```tex
\section{Notfallkarte}
\begin{ctmmRedBox}{Notfallkarte}
    Krisensituation und Hilfe
\end{ctmmRedBox}
```

## Generierte Dateien

### Datei-Struktur
```
modules/
├── arbeitsblatt-[name].tex
├── tool-[name].tex
└── notfall-[name].tex
```

### Integration in main.tex

Nach der Generierung müssen Module in `main.tex` eingebunden werden:

```tex
\input{modules/arbeitsblatt-stimmungscheck}
\input{modules/tool-atemtechnik}
\input{modules/notfall-panikattacken}
```

**Automatisches Hinzufügen:**
Das Shell-Script `create-module.sh` bietet die Option, Module automatisch zu `main.tex` hinzuzufügen.

## Design-System Integration

### Farb-Schema

Die generierten Module nutzen das CTMM Farb-Schema:

- **ctmmBlue** (#003087) - Arbeitsblätter und Hauptinhalte
- **ctmmGreen** (#4CAF50) - Tools und positive Elemente  
- **ctmmRed** (#D32F2F) - Notfallkarten und Warnungen
- **ctmmGray** (#757575) - Sekundäre Texte

### Interaktive Elemente

**Verfügbare Form-Elemente:**
```tex
\ctmmCheckBox[field_name]{Label}
\ctmmTextField[width]{label}{name}
\ctmmTextArea[width]{lines}{label}{name}
\ctmmRadioButton{group}{value}{label}
```

## Workflow Integration

### Build-System Integration

Nach der Modulerstellung:

```bash
# 1. Build-System prüfen
python3 ctmm_build.py

# 2. LaTeX validieren  
make validate

# 3. Kompilieren
make build
```

### Automatisierte Tests

```bash
# Unit Tests
make unit-test

# LaTeX Syntax-Validierung
python3 validate_latex_syntax.py
```

## Beispiele

### Beispiel 1: Arbeitsblatt für Stimmungsmonitoring

```bash
./create-module.sh
# Wählen: 1) Arbeitsblatt erstellen
# Dateiname: stimmungsmonitoring
# Titel: Tägliches Stimmungsmonitoring
```

**Generiert:** `modules/arbeitsblatt-stimmungsmonitoring.tex`

### Beispiel 2: 5-4-3-2-1 Grounding Tool

```bash
node module-generator.js tool grounding-5-4-3-2-1
```

**Generiert:** `modules/tool-grounding-5-4-3-2-1.tex`

### Beispiel 3: Panikattacken Notfallkarte

```bash
node module-generator.js notfallkarte panikattacken
```

**Generiert:** `modules/notfall-panikattacken.tex`

## Anpassung und Erweiterung

### Template-Anpassung

Templates können in `module-generator.js` angepasst werden:

```javascript
getArbeitsblattTemplate() {
    return `% Ihr angepasstes Template
\\section{{{title}}}
// ... weitere Anpassungen
`;
}
```

### Neue Modul-Typen

Neue Modul-Typen können durch Hinzufügen von Templates implementiert werden:

```javascript
this.templates = {
    arbeitsblatt: this.getArbeitsblattTemplate(),
    tool: this.getToolTemplate(),
    notfallkarte: this.getNotfallkarteTemplate(),
    neuertyp: this.getNeuerTypTemplate()  // Neue Vorlage
};
```

## Troubleshooting

### Node.js nicht verfügbar

Wenn Node.js nicht installiert ist, bietet `create-module.sh` einen Fallback-Modus:

```bash
./create-module.sh
# Erstellt einfache Templates ohne JavaScript
```

### Berechtigungen

Scripts ausführbar machen:
```bash
chmod +x create-module.sh module-generator.js
```

### Encoding-Probleme

Alle generierten Dateien verwenden UTF-8 Encoding für deutsche Umlaute.

### Build-Fehler

Nach der Modulerstellung Build-System prüfen:
```bash
python3 ctmm_build.py
```

## Integration mit bestehenden Workflows

### GitHub Actions

Die generierten Module werden automatisch von der CI/CD-Pipeline erfasst:

```yaml
- name: Run CTMM Build System Check
  run: |
    python3 ctmm_build.py
```

### Makefile Targets

```bash
make check          # Build-System Check
make build          # PDF Erstellung  
make unit-test      # Tests ausführen
make validate       # LaTeX validieren
```

## Best Practices

1. **Aussagekräftige Namen:** Verwenden Sie beschreibende Dateinamen
2. **Inhalte anpassen:** Bearbeiten Sie generierte Platzhalter
3. **Tests ausführen:** Prüfen Sie das Build-System nach Änderungen
4. **Backup erstellen:** Sichern Sie wichtige Inhalte vor Änderungen
5. **Dokumentation:** Dokumentieren Sie spezielle Anpassungen

## Support

Bei Problemen oder Fragen:

1. **Build-System:** `python3 ctmm_build.py --help`
2. **Validierung:** `make validate`
3. **Tests:** `make unit-test` 
4. **Dokumentation:** Siehe README.md und weitere .md Dateien im Repository

---

**Version:** 1.0  
**Kompatibilität:** CTMM LaTeX System v2024+  
**Abhängigkeiten:** Node.js (optional), Python 3, LaTeX Distribution