# 🧩 CTMM Module Generator

Automatisches Generieren neuer CTMM-Module für Ihr LaTeX-Therapie-Workbook.

## 🚀 Schnellstart

### Option 1: Interaktives Script (empfohlen)
```bash
./create-module.sh
```

### Option 2: Direkte Nutzung
```bash
node module-generator.js <typ> "<name>"
```

## 📝 Verfügbare Modul-Typen

### 1. **Arbeitsblatt** (`arbeitsblatt`)
- 🎯 **Zweck**: Strukturierte Selbstreflexion und Dokumentation
- 🎨 **Farbe**: Grün (`ctmmGreen`)
- 📋 **Enthält**: Ausfüllfelder, Reflexionsbereich, CTMM-Navigation
- **Beispiele**: Täglicher Check-In, Wochenreflexion, Trigger-Tracking

### 2. **Tool** (`tool`)
- 🎯 **Zweck**: Praktische Interventions-Tools und Skill-Anleitungen
- 🎨 **Farbe**: Orange (`ctmmOrange`)
- 📋 **Enthält**: Schritt-für-Schritt Anleitung, Praxis-Beispiel, Navigation
- **Beispiele**: Atemtechniken, Grounding-Übungen, Kommunikations-Skills

### 3. **Notfallkarte** (`notfallkarte`)
- 🎯 **Zweck**: Schnelle Hilfe in Krisensituationen
- 🎨 **Farbe**: Rot (`ctmmRed`)
- 📋 **Enthält**: Sofortmaßnahmen, Safe-Words, Nachsorge-Plan
- **Beispiele**: Panikattacken, Dissoziation, Triggering

## ✨ Beispiele

```bash
# Arbeitsblatt erstellen
node module-generator.js arbeitsblatt "Täglicher Stimmungscheck"

# Tool erstellen
node module-generator.js tool "5-4-3-2-1 Grounding"

# Notfallkarte erstellen
node module-generator.js notfallkarte "Panikattacken"
```

## 🔧 Integration in main.tex

Nach der Erstellung wird Ihnen die Einbindungszeile angezeigt:

```latex
\input{modules/arbeitsblatt-taeglicher-stimmungscheck}
```

Diese Zeile fügen Sie an der gewünschten Stelle in Ihre `main.tex` ein.

## 🎨 Design-Features

- ✅ Nutzt Ihr bestehendes CTMM-Farbschema
- ✅ Integriert `ctmmBlueBox`, `ctmmGreenBox`, etc.
- ✅ Folgt Ihrer LaTeX-Struktur
- ✅ Automatische CTMM-Navigation zwischen Modulen
- ✅ Konsistente Formatierung und Header

## 📁 Datei-Organisation

```
modules/
├── arbeitsblatt-*.tex    # Alle Arbeitsblätter
├── tool-*.tex           # Alle Tools
└── notfall-*.tex        # Alle Notfallkarten
```

## 🔄 Workflow

1. **Erstellen**: `./create-module.sh` oder `node module-generator.js`
2. **Anpassen**: Öffnen Sie die erstellte `.tex` Datei und passen Sie Inhalte an
3. **Einbinden**: Fügen Sie `\input{modules/...}` in `main.tex` ein
4. **Kompilieren**: Nutzen Sie den CTMM-Build-Task oder `pdflatex`

## 💡 Tipps

- **Deutsche Umlaute** werden automatisch in LaTeX-kompatible Form umgewandelt
- **Dateinamen** werden automatisch erstellt (Kleinbuchstaben, Bindestriche)
- **CTMM-Navigation** verlinkt automatisch zu verwandten Modulen
- **Konsistenz** durch vordefinierte Templates garantiert

## 🛠 Anpassungen

Sie können die Templates in `module-generator.js` nach Ihren Bedürfnissen anpassen:

- **Farben**: Ändern Sie die `color` Werte in `moduleConfig`
- **Felder**: Passen Sie die Placeholder in der `generateModule` Funktion an
- **Struktur**: Modifizieren Sie die `templates` für andere Layouts

---

**🎯 Dieses Tool spart Ihnen Zeit und sorgt für konsistente, professionelle CTMM-Module!**
