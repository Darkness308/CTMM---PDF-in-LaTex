# CTMM LaTeX Helper Tool 

Ein Python-Skript zur automatisierten Analyse und Fehlerüberprüfung des CTMM LaTeX-Projekts.

## Funktionen

### [SUMMARY] Project Analysis (`analyze`)
- Analysiert alle `.tex` Module im `modules/` Verzeichnis
- Zählt Wörter, Abschnitte und Formularelemente
- Erkennt CTMM-Farbenverwendung
- Zeigt Package-Nutzung an

### [FAIL] Error Checking (`check-errors`)
- Überprüft LaTeX Build-Logs auf Fehler und Warnungen
- Erkennt fehlende Packages
- Zeigt Seitenzahl des fertigen PDFs

###  Detailed Statistics (`stats`)
- Generiert umfassende Projekt-Statistiken
- Exportiert Daten als JSON-Report
- Kategorisiert Module nach Typen

## Verwendung

### Kommandozeile
```bash
# Schnelle Analyse
python3 latex-helper.py analyze

# Fehlerüberprüfung nach Build
python3 latex-helper.py check-errors

# Detaillierte Statistiken mit JSON-Export
python3 latex-helper.py stats -o build/report.json
```

### VS Code Tasks
Das Tool ist als VS Code Tasks integriert:

- **CTMM: Quick Module Analysis** - Schnelle Übersicht
- **CTMM: Analyze Project Statistics** - Mit JSON-Export
- **CTMM: Check Build Errors** - Fehleranalyse

Ausführung über `Ctrl+Shift+P` → "Tasks: Run Task"

## Erkannte Elemente

### [DESIGN] CTMM Design Elements
- `ctmmGreen`, `ctmmBlue`, `ctmmPurple`, `ctmmOrange`, `ctmmRed`, `ctmmYellow`, `ctmmGray`
- Formularelemente: `\ctmmTextField`, `\ctmmCheckBox`, `\ctmmRadioButton`
- tcolorbox-Verwendung

### [NOTE] LaTeX Struktur
- Sections, Subsections, Subsubsections
- Package-Abhängigkeiten
- Wortanzahl und Zeilenzahl

### [SEARCH] Build-Analyse
- LaTeX-Fehler und Warnungen
- Fehlende Packages
- Seitenzahl des fertigen PDFs

## Output-Beispiel

```
 CTMM LaTeX Project Analysis
==================================================
 Module gefunden: 18
[NOTE] Wörter gesamt: 5,033
[PACKAGE] Packages verwendet: 8

 Module nach Kategorien:
  • root: 18 Module, 5,033 Wörter, 188 Formularfelder

[DESIGN] CTMM-Farben Verwendung:
  • ctmmBlue: 28x
  • ctmmPurple: 26x
  • ctmmOrange: 23x
  • ctmmGreen: 18x
```

## Integration Workflow

1. **Entwicklung**: Nutze `analyze` für schnelle Übersicht während der Modulerstellung
2. **Build-Check**: Nutze `check-errors` nach LaTeX-Kompilierung
3. **Dokumentation**: Nutze `stats` für Projektdokumentation und Reports

## JSON Export Schema

```json
{
  "summary": {
  "total_modules": 18,
  "total_words": 5033,
  "total_packages": 8,
  "categories": ["root"]
  },
  "modules_by_category": {
  "root": {
  "count": 18,
  "total_words": 5033,
  "total_form_elements": 188,
  "modules": [...]
  }
  },
  "ctmm_color_usage": {
  "ctmmBlue": 28,
  "ctmmPurple": 26
  },
  "form_elements_total": 188
}
```

## Erweiterungsmöglichkeiten

- Automatische Abhängigkeitsprüfung zwischen Modulen
- Vollständigkeitschecks für CTMM-Richtlinien
- Integration in CI/CD Pipeline
- Automatische Qualitätschecks für neue Module

---
*Tool integriert in CTMM Build System - Automatisierte LaTeX-Projektanalyse für therapeutische Materialien*
