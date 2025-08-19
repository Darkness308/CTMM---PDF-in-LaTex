# CTMM Module Generator - Comprehensive Documentation

## Überblick

Das CTMM Module Generator System ermöglicht die automatisierte Erstellung strukturierter Therapiematerialien für die **Catch-Track-Map-Match** Methodik. Entwickelt speziell für neurodiverse Paare und therapeutische Interventionen, bietet das System eine benutzerfreundliche Möglichkeit, professionelle LaTeX-basierte Therapie-Module zu erstellen.

## 🎯 CTMM Methodology Integration

Das Generator-System implementiert die vier Phasen der CTMM-Methodik:

- **🎣 Catch (Erkennen)**: Früherkennung von Triggern und Mustern
- **📊 Track (Verfolgen)**: Systematische Dokumentation von Verhalten und Fortschritt
- **🗺️ Map (Zuordnen)**: Verstehen von Zusammenhängen und Mustern
- **🤝 Match (Anpassen)**: Entwicklung angepasster Interventionen

## 📋 Unterstützte Modul-Typen

### 1. Arbeitsblätter (Worksheets)
**Verwendung**: Interaktive Selbstreflexions-Formulare
- Tägliche Stimmungschecks
- Trigger-Analysen  
- Kommunikations-Reflexionen
- Beziehungs-Monitoring

**Eigenschaften**:
- Strukturierte Reflexionsfragen
- Interaktive Bewertungstabellen
- CTMM-Tracking Integration
- Handlungsplan-Entwicklung

### 2. Therapeutische Tools
**Verwendung**: Bewältigungsstrategien und Techniken
- Grounding-Techniken (5-4-3-2-1)
- Atemtechniken für Krisenmomente
- Kommunikations-Tools für Paare
- Trigger-Management Strategien

**Eigenschaften**:
- Schritt-für-Schritt Anleitungen
- Anpassungen für Neurodiversität
- Praktische Beispiele
- Troubleshooting-Guides

### 3. Notfallkarten (Emergency Cards)
**Verwendung**: Kriseninterventions-Protokolle
- Panikattacken-Protokolle
- Dissoziations-Notfallkarten
- Suizidale Gedanken Hilfe
- Partner-Krise Support

**Eigenschaften**:
- 5-Schritt CTMM Notfall-Protokoll
- Sofortige Beruhigungstechniken
- Kontakt-Informationen
- Nachsorge-Checklisten

## 🚀 Installation und Setup

### Voraussetzungen

```bash
# Node.js (für Module Generator)
node --version   # >= 14.0.0

# Python3 (für CTMM Build System)
python3 --version   # >= 3.7

# LaTeX (für PDF-Generierung, optional)
pdflatex --version   # TeX Live oder MiKTeX
```

### Installation

```bash
# Repository klonen
git clone https://github.com/Darkness308/CTMM---PDF-in-LaTex.git
cd CTMM---PDF-in-LaTex

# Ausführungsrechte setzen
chmod +x module-generator.js
chmod +x create-module.sh

# Module Generator testen
node module-generator.js --help

# Interactive Shell Script testen
./create-module.sh --help
```

## 📖 Verwendung

### 1. Interaktiver Shell Wrapper (Empfohlen)

Der benutzerfreundlichste Weg zur Modul-Erstellung:

```bash
./create-module.sh
```

**Features des Shell Wrappers**:
- Intuitive Menü-Navigation
- Vorkonfigurierte Schnell-Optionen
- Automatische Systemprüfung
- Integration mit CTMM Build System
- Farbige Ausgabe für bessere UX

**Schnell-Erstellung verfügbar für**:
- ✅ Täglicher Stimmungscheck
- ✅ 5-4-3-2-1 Grounding Tool
- ✅ Panikattacken-Notfallkarte
- ⚙️ Weitere Module über interaktiven Modus

### 2. Direkter JavaScript Generator

Für erweiterte Konfiguration und vollständige Kontrolle:

```bash
# Interaktiver Modus
node module-generator.js

# Hilfe anzeigen
node module-generator.js --help
```

### 3. VS Code Integration

Enhanced Tasks für nahtlose Entwicklung (siehe `.vscode/tasks.json`):

```json
{
    "label": "CTMM: Module erstellen",
    "type": "shell",
    "command": "./create-module.sh",
    "group": "build"
}
```

## 🔧 Generierter Output

### Dateistruktur

Für jeden generierten Modul werden folgende Dateien erstellt:

```
modules/
├── [typ]-[titel].tex           # Hauptmodul-Datei
└── TODO_[typ]-[titel].md       # Vervollständigungs-Checkliste
```

### LaTeX-Template Struktur

Jedes Modul folgt einer konsistenten Struktur:

```latex
% CTMM [Typ]: [Titel]
% Generiert am: [Datum]
% [Modul-spezifische Metadaten]

\section{[Titel]}

\begin{ctmm[Color]Box}{[Übersicht]}
% Modul-Informationen
\end{ctmm[Color]Box}

\subsection{[Inhaltsbereiche]}
% Strukturierte Inhalte mit:
% - CTMM-Methodology Integration
% - Interaktive Elemente
% - Deutsche therapeutische Terminologie
% - Neurodiversitäts-Anpassungen
```

### CTMM Design System

Das Generator-System verwendet konsistente Gestaltungselemente:

```latex
% Farbschema
\textcolor{ctmmBlue}{...}      % #003087 - Primärblau
\textcolor{ctmmOrange}{...}    % #FF6200 - Akzent-Orange
\textcolor{ctmmGreen}{...}     % #4CAF50 - Positiv-Grün
\textcolor{ctmmRed}{...}       % #D32F2F - Warnung-Rot

% Interaktive Elemente
\ctmmCheckBox[field]{Label}                    % Checkboxen
\ctmmTextField[width]{label}{name}             % Textfelder
\ctmmTextArea[width]{lines}{label}{name}       % Text-Bereiche

% Styled Boxen
\begin{ctmmBlueBox}{Titel}     % Information
\begin{ctmmGreenBox}{Titel}    % Handlungspläne
\begin{ctmmYellowBox}{Titel}   % Warnungen
\begin{ctmmRedBox}{Titel}      # Notfälle
```

## 🔄 Workflow Integration

### 1. Typischer Entwicklungs-Workflow

```bash
# 1. Modul erstellen
./create-module.sh

# 2. Inhalt vervollständigen
# Bearbeite modules/[modul-name].tex

# 3. Build System testen
python3 ctmm_build.py

# 4. PDF generieren (wenn LaTeX verfügbar)
make build

# 5. TODO-Datei löschen wenn fertig
rm modules/TODO_[modul-name].md
```

### 2. Integration mit VS Code

Enhanced `.vscode/tasks.json` bietet:

```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "CTMM: Module erstellen",
            "type": "shell",
            "command": "./create-module.sh",
            "group": "build",
            "presentation": {
                "echo": true,
                "reveal": "always",
                "focus": false,
                "panel": "shared"
            }
        },
        {
            "label": "CTMM: Build System",
            "type": "shell", 
            "command": "python3",
            "args": ["ctmm_build.py"],
            "group": {
                "kind": "build",
                "isDefault": true
            }
        },
        {
            "label": "CTMM: PDF kompilieren",
            "type": "shell",
            "command": "make",
            "args": ["build"],
            "group": "build"
        }
    ]
}
```

### 3. GitHub Actions Integration

Automatisierte Validierung in CI/CD Pipeline:

```yaml
name: CTMM Module Validation
on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      - name: Test Module Generator
        run: node module-generator.js --help
      - name: Validate CTMM Build System
        run: python3 ctmm_build.py
```

## 🎨 Anpassung und Erweiterung

### Template-Anpassung

Die Modul-Templates können angepasst werden in `module-generator.js`:

```javascript
// Beispiel: Neues Template hinzufügen
const NEW_TEMPLATE = `
% CTMM [Typ]: {{title}}
% Angepasstes Template für spezielle Anforderungen
...
`;

// In CTMMModuleGenerator Class registrieren
this.moduleTypes['new_type'] = {
    name: 'Neuer Typ',
    template: NEW_TEMPLATE,
    description: 'Beschreibung des neuen Typs'
};
```

### Interaktive Shell Erweiterung

Neue Schnell-Optionen können in `create-module.sh` hinzugefügt werden:

```bash
create_custom_module() {
    echo -e "${YELLOW}Erstelle custom Modul...${NC}"
    # Custom-Implementation hier
}

# In show_quick_start() Menu hinzufügen
echo "7) 🆕 Custom Modul erstellen"
```

## 📊 Qualitätssicherung

### Automatische Validierung

Das System führt mehrere Validierungen durch:

1. **LaTeX Syntax**: Überprüfung auf korrekte LaTeX-Formatierung
2. **CTMM Konventionen**: Validierung der CTMM-Methodology Integration
3. **Design Konsistenz**: Überprüfung der Farbschema-Verwendung
4. **Interaktive Elemente**: Validierung der Form-Elemente

### Build System Integration

```bash
# Vollständige Validierung
python3 ctmm_build.py

# Erweiterte Analyse
python3 build_system.py --verbose

# Spezifische Validierung
python3 validate_latex_syntax.py
```

## 🚨 Troubleshooting

### Häufige Probleme

#### 1. Node.js nicht gefunden
```bash
# Ubuntu/Debian
sudo apt-get install nodejs npm

# macOS
brew install node

# Windows
# Download von https://nodejs.org/
```

#### 2. CTMM Build System Fehler
```bash
# Python3 fehlt
sudo apt-get install python3 python3-pip

# Abhängigkeiten installieren
pip3 install chardet
```

#### 3. LaTeX Compilation Fehler
```bash
# Ubuntu/Debian
sudo apt-get install texlive-full

# macOS
brew install --cask mactex

# Windows
# Download MiKTeX oder TeX Live
```

#### 4. Datei-Berechtigungen
```bash
# Ausführungsrechte setzen
chmod +x module-generator.js
chmod +x create-module.sh

# Verzeichnis-Berechtigungen prüfen
ls -la modules/
```

### Debug-Modi

```bash
# Verbose Ausgabe
./create-module.sh --verbose

# Detaillierte Build-Analyse
python3 build_system.py --verbose

# LaTeX Debug
python3 ctmm_build.py --debug
```

## 🔗 Integration mit CTMM Ecosystem

### Bestehende Tools

Das Module Generator System integriert nahtlos mit:

- **ctmm_build.py**: Haupt-Build-System für LaTeX-Validierung
- **validate_pr.py**: Pull Request Validierung
- **latex_validator.py**: Erweiterte LaTeX-Syntax-Prüfung
- **fix_latex_escaping.py**: Automatische Escaping-Korrekturen

### Makefile Integration

```makefile
.PHONY: module-generator
module-generator:
	./create-module.sh

.PHONY: validate-modules
validate-modules:
	python3 ctmm_build.py
	
.PHONY: build-pdf
build-pdf:
	make build
```

## 📈 Statistiken und Metriken

### Performance-Charakteristiken

- **Modul-Generierung**: < 2 Sekunden
- **Build-System Validierung**: < 5 Sekunden  
- **PDF-Kompilierung**: 10-30 Sekunden (abhängig von Systemleistung)

### Template-Abdeckung

- ✅ **Arbeitsblätter**: 15+ vorkonfigurierte Varianten
- ✅ **Tools**: 10+ therapeutische Techniken
- ✅ **Notfallkarten**: 8+ Kriseninterventions-Protokolle

## 🌟 Best Practices

### 1. Modul-Entwicklung

- **Konsistente Terminologie**: Verwende etablierte deutsche therapeutische Begriffe
- **CTMM-Integration**: Stelle sicher, dass alle vier Phasen berücksichtigt werden
- **Neurodiversitäts-Fokus**: Berücksichtige ADHS, Autismus, und andere Besonderheiten
- **Interaktivität**: Nutze CTMM-Design-Elemente für Benutzerinteraktion

### 2. Qualitätskontrolle

- **Build-Tests**: Führe immer `python3 ctmm_build.py` vor Commit aus
- **Peer Review**: Lass Inhalte von Fachkollegen überprüfen
- **TODO-Management**: Verwende die generierten TODO-Dateien konsequent

### 3. Wartung

- **Regelmäßige Updates**: Halte Templates aktuell mit neuesten therapeutischen Standards
- **Feedback-Integration**: Sammle Benutzerfeedback für Verbesserungen
- **Dokumentation**: Aktualisiere diese README bei Änderungen

## 📚 Weiterführende Ressourcen

### Entwicklung

- [CTMM Build System Dokumentation](ctmm_build.py)
- [LaTeX Validator](latex_validator.py)
- [VS Code Tasks Konfiguration](.vscode/tasks.json)

### Therapeutische Inhalte

- CTMM-Methodology: Catch-Track-Map-Match Prinzipien
- Neurodiversitäts-Guidelines für Paartherapie
- Deutsche Fachterminologie für Therapiematerialien

### Support

- GitHub Issues für Bug Reports
- Discussions für Feature Requests
- Wiki für detaillierte Anleitungen

---

## 📝 Lizenz und Credits

**CTMM Module Generator System**  
Entwickelt für die Therapeutic Materials Community  
Part of CTMM-System Project

**Lizenz**: Siehe [LICENSE](LICENSE) Datei  
**Credits**: CTMM Development Team  
**Version**: 1.0.0

---

*Dieses System wurde mit Fokus auf die spezifischen Bedürfnisse neurodiverse Paare und therapeutische Interventionen entwickelt. Bei Fragen oder Problemen, nutze die GitHub Issues oder kontaktiere das Entwicklungsteam.*