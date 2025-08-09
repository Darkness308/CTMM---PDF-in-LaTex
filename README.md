# CTMM-System

Ein modulares LaTeX-Framework für Catch-Track-Map-Match Therapiematerialien mit automatisiertem Build-Management.

## Überblick

Dieses Repository enthält ein vollständiges LaTeX-System zur Erstellung von CTMM-Therapiedokumenten, einschließlich:
- Depression & Stimmungstief Module
- Trigger-Management
- Bindungsdynamik
- Formularelemente für therapeutische Dokumentation
- **Automatisiertes Build-Management mit Fehlerdiagnose**
- **Template-Generierung für fehlende Dateien**
- **CI/CD-Integration mit GitHub Actions**

## 🚀 Schnellstart

### Installation

```bash
# Repository klonen
git clone https://github.com/Darkness308/CTMM---PDF-in-LaTex.git
cd CTMM---PDF-in-LaTex

# Python-Abhängigkeiten installieren
make deps

# LaTeX-Installation (system-spezifisch)
make install-latex  # Zeigt Installationsanweisungen
```

### Verwendung

**Entwicklungsworkflow (empfohlen):**
```bash
make dev        # Kompletter Workflow: Check + Analyse + Build
```

**Einzelne Schritte:**
```bash
make analyze    # Umfassende Build-Analyse
make build      # PDF erstellen (main.pdf)
make check      # Schnelle Systemprüfung
```

**CI/Produktions-Workflow:**
```bash
make ci         # Kompletter CI-Workflow
make build-ci   # CI-Version erstellen (main_final.pdf)
```

## 🏗️ Build-System-Architektur

### Kernkomponenten

| Komponente | Zweck | Verwendung |
|------------|-------|------------|
| **`build_manager.py`** | Hauptsystem mit umfassender Analyse | `python3 build_manager.py` |
| **`ctmm_build.py`** | Schnelle Systemprüfung | `python3 ctmm_build.py` |
| **`main.tex`** | Entwicklungsversion | Lokale Builds |
| **`main_final.tex`** | CI/Produktionsversion | Automatisierte Builds |

### Automatische Funktionen

✅ **Datei-Erkennung**: Scannt `main.tex` nach `\usepackage{style/...}` und `\input{modules/...}`  
✅ **Template-Generierung**: Erstellt automatisch fehlende .sty und .tex Dateien  
✅ **Inkrementelle Tests**: Testet Module einzeln zur Fehleridentifikation  
✅ **Umfassende Reports**: Generiert `build_report.md` mit detaillierter Analyse  
✅ **Fehlerdiagnose**: Spezifische Fehlerlogs für jedes problematische Modul  

## 📋 Make-Kommandos

| Kommando | Beschreibung | Verwendung |
|----------|--------------|------------|
| `make analyze` | **Empfohlen**: Vollständige Analyse | Regelmäßige Entwicklung |
| `make build` | Entwicklungsversion erstellen | Lokale PDF-Erstellung |
| `make build-ci` | CI/Produktionsversion erstellen | Release-Builds |
| `make dev` | Kompletter Entwicklungsworkflow | Vollständiger lokaler Workflow |
| `make ci` | Kompletter CI-Workflow | Automatisierte Builds |
| `make clean` | Build-Artefakte entfernen | Vor Commits |
| `make clean-all` | Alle generierten Dateien entfernen | Neustart |

## 📂 Projektstruktur

```
CTMM-System/
├── main.tex                    # Entwicklungs-Build-Ziel
├── main_final.tex              # CI/Produktions-Build-Ziel
├── build_manager.py            # Haupt-Build-System ⭐
├── ctmm_build.py              # Schnellprüfung
├── BUILD_GUIDE.md             # Ausführliche Dokumentation
├── style/                     # Style-Pakete (.sty)
│   ├── ctmm-design.sty
│   ├── form-elements.sty
│   └── ctmm-diagrams.sty
├── modules/                   # Inhaltsmodule (.tex)
│   ├── navigation-system.tex
│   ├── depression.tex
│   └── ...
└── build/                     # Build-Artefakte (generiert)
    ├── build_report.md        # Analyse-Report
    └── build_error_*.log      # Fehlerprotokolle
```

## 🔧 Entwicklung neuer Module

### 1. Modul referenzieren
```latex
% In main.tex hinzufügen:
\input{modules/mein-neues-modul}
```

### 2. Analyse ausführen
```bash
make analyze
```

### 3. Automatisch generierte Templates bearbeiten
- `modules/mein-neues-modul.tex` - Modulvorlage mit TODO-Kommentaren
- `modules/TODO_mein-neues-modul.md` - Aufgabenliste

### 4. Implementation testen
```bash
make build
```

## 🎨 LaTeX Best Practices

### Kritische Regeln

**📦 Pakete nur in der Präambel:**
```latex
% ✅ Richtig - in main.tex vor \begin{document}
\usepackage{style/ctmm-design}

% ❌ Falsch - niemals in Modulen oder nach \begin{document}
```

**🔧 Makros zentral definieren:**
```latex
% ✅ Richtig - in Präambel oder Style-Datei
\newcommand{\checkbox}{$\square$}
\newcommand{\checkedbox}{$\blacksquare$}

% In Modulen verwenden:
\checkbox~Option 1
\checkedbox~Option 2
```

**❌ Häufige Fehler vermeiden:**
- `Can be used only in preamble` → Paket in die Präambel verschieben
- `Undefined control sequence` → Makro-Definition prüfen
- `Command already defined` → Doppelte Definitionen entfernen

### Checkbox-Konvention

**Immer verwenden:**
```latex
\checkbox        % Leere Checkbox: □
\checkedbox      % Gefüllte Checkbox: ■
```

**Niemals verwenden:**
```latex
\Box            % Kann zu Fehlern führen
\blacksquare    % Kann zu Fehlern führen
```

## 🔍 Fehlerdiagnose

### Build-Report prüfen
```bash
cat build_report.md
```

### Spezifische Fehlerlogs
```bash
ls build_error_*.log
cat build_error_module-name.log
```

### Inkrementelles Debugging
1. Problematische Module in `main.tex` auskommentieren
2. Erfolgreich builden
3. Module einzeln wieder aktivieren

## 🔄 CI/CD Integration

### GitHub Actions

Das System integriert sich nahtlos mit GitHub Actions:

```yaml
- name: CTMM Build System Check
  run: python3 build_manager.py

- name: Build LaTeX PDF
  uses: dante-ev/latex-action@v2.0.0
  with:
    root_file: main_final.tex
```

### Build-Artefakte

CI-Builds erzeugen:
- `main_final.pdf` - Produktions-PDF
- `build_report.md` - Analyse-Report
- Fehlerlogs (bei Problemen)

## 📚 Weiterführende Dokumentation

- **[BUILD_GUIDE.md](BUILD_GUIDE.md)** - Vollständige Build-System-Dokumentation
- **[GitHub Actions](.github/workflows/)** - CI/CD-Konfiguration
- **[Style-Pakete](style/)** - Design-System-Dokumentation

## ⚡ Typische Workflows

### Tägliche Entwicklung
```bash
# Nach Änderungen:
make analyze    # Status prüfen
make build      # PDF erstellen
```

### Vor Commits
```bash
make clean      # Aufräumen
make analyze    # Finale Prüfung
```

### Release-Vorbereitung
```bash
make ci         # Vollständiger CI-Test
```

## 🆘 Hilfe und Support

### Build-Probleme
1. `build_report.md` konsultieren
2. Fehlerlogs in `build_error_*.log` prüfen
3. `make clean && make analyze` ausführen

### LaTeX-Installationsprobleme
```bash
make install-latex  # Installationsanweisungen
```

### Erweiterte Analyse
```bash
python3 build_manager.py --verbose
```

---

**🎯 Tipp**: Verwende `make analyze` regelmäßig - es ist der beste Weg, Probleme frühzeitig zu erkennen und das System gesund zu halten!

**📖 Vollständige Dokumentation**: Siehe [BUILD_GUIDE.md](BUILD_GUIDE.md) für detaillierte Informationen zu allen Features und erweiterten Verwendungsmöglichkeiten.
