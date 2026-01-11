#  CTMM Module Generator

Automatisches Generieren neuer CTMM-Module für Ihr LaTeX-Therapie-Workbook.

## [DEPLOY] Schnellstart

### Option 1: Interaktives Script (empfohlen)
```bash
./create-module.sh
```

### Option 2: Direkte Nutzung  
```bash
node module-generator.js <typ> "<name>"
```

## [NOTE] Verfügbare Modul-Typen

### 1. **Arbeitsblatt** (`arbeitsblatt`)
- [TARGET] **Zweck**: Strukturierte Selbstreflexion und Dokumentation
- [DESIGN] **Farbe**: Grün (`ctmmGreen`)
- [TEST] **Enthält**: Ausfüllfelder, Reflexionsbereich, CTMM-Navigation
- **Beispiele**: Täglicher Check-In, Wochenreflexion, Trigger-Tracking

### 2. **Tool** (`tool`)
- [TARGET] **Zweck**: Praktische Interventions-Tools und Skill-Anleitungen
- [DESIGN] **Farbe**: Orange (`ctmmOrange`)
- [TEST] **Enthält**: Schritt-für-Schritt Anleitung, Praxis-Beispiel, Navigation
- **Beispiele**: Atemtechniken, Grounding-Übungen, Kommunikations-Skills

### 3. **Notfallkarte** (`notfallkarte`)
- [TARGET] **Zweck**: Schnelle Hilfe in Krisensituationen
- [DESIGN] **Farbe**: Rot (`ctmmRed`)
- [TEST] **Enthält**: Sofortmaßnahmen, Safe-Words, Nachsorge-Plan
- **Beispiele**: Panikattacken, Dissoziation, Triggering

## [NEW] Beispiele

```bash
# Arbeitsblatt erstellen
node module-generator.js arbeitsblatt "Täglicher Stimmungscheck"

# Tool erstellen  
node module-generator.js tool "5-4-3-2-1 Grounding"

# Notfallkarte erstellen
node module-generator.js notfallkarte "Panikattacken"
```

## [FIX] Integration in main.tex

Nach der Erstellung wird Ihnen die Einbindungszeile angezeigt:

```latex
\input{modules/arbeitsblatt-taeglicher-stimmungscheck}
```

Diese Zeile fügen Sie an der gewünschten Stelle in Ihre `main.tex` ein.

## [DESIGN] Design-Features

- [PASS] Nutzt Ihr bestehendes CTMM-Farbschema
- [PASS] Integriert `ctmmBlueBox`, `ctmmGreenBox`, etc.
- [PASS] Folgt Ihrer LaTeX-Struktur
- [PASS] Automatische CTMM-Navigation zwischen Modulen
- [PASS] Konsistente Formatierung und Header

##  Datei-Organisation

```
modules/
├── arbeitsblatt-*.tex  # Alle Arbeitsblätter
├── tool-*.tex  # Alle Tools
└── notfall-*.tex  # Alle Notfallkarten
```

## [SYNC] Workflow

1. **Erstellen**: `./create-module.sh` oder `node module-generator.js`
2. **Anpassen**: Öffnen Sie die erstellte `.tex` Datei und passen Sie Inhalte an
3. **Einbinden**: Fügen Sie `\input{modules/...}` in `main.tex` ein  
4. **Kompilieren**: Nutzen Sie den CTMM-Build-Task oder `pdflatex`

## [IDEA] Tipps

- **Deutsche Umlaute** werden automatisch in LaTeX-kompatible Form umgewandelt
- **Dateinamen** werden automatisch erstellt (Kleinbuchstaben, Bindestriche)
- **CTMM-Navigation** verlinkt automatisch zu verwandten Modulen
- **Konsistenz** durch vordefinierte Templates garantiert

## [TOOLS] Anpassungen

Sie können die Templates in `module-generator.js` nach Ihren Bedürfnissen anpassen:

- **Farben**: Ändern Sie die `color` Werte in `moduleConfig`
- **Felder**: Passen Sie die Placeholder in der `generateModule` Funktion an  
- **Struktur**: Modifizieren Sie die `templates` für andere Layouts

---

**[TARGET] Dieses Tool spart Ihnen Zeit und sorgt für konsistente, professionelle CTMM-Module!**
