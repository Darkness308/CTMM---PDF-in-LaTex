# [DEPLOY] CTMM LaTeX Workshop - Einfache Bedienung

## Was ist das?
Die **LaTeX Workshop Extension** macht das Arbeiten mit LaTeX in VS Code **viel einfacher**. Keine Befehle auswendig lernen!

## [TARGET] **Wie Sie es nutzen (3 einfache Wege):**

### **1. Automatisches Bauen (Empfohlen)**
- Öffnen Sie `main.tex` oder ein beliebiges `.tex` Modul
- **Speichern Sie** (`Ctrl+S`)
- **PDF wird automatisch erstellt!** [NEW]

### **2. Manuelle Kontrolle**
- `Ctrl+Shift+P` → "LaTeX Workshop: Build with recipe"
- Wählen Sie: **"CTMM: pdflatex × 2 (Standard)"**

### **3. Mit einem Klick**
- **Rechtsklick** in der `.tex` Datei
- "Build LaTeX project" auswählen

## [SUMMARY] **PDF anzeigen:**
- **Automatisch**: PDF öffnet sich als Tab in VS Code
- **Sync**: Doppelklick im PDF springt zum LaTeX-Code
- **Live-Reload**: PDF aktualisiert sich bei Änderungen

##  **Perfekt für CTMM-Module:**

### **Workflow für neue Module:**
1. **Modul erstellen**: Mit unserem `create-module.sh`
2. **In main.tex einbinden**: `\input{modules/ihr-modul}`
3. **Automatisch testen**: Einfach `main.tex` speichern
4. **PDF prüfen**: Wird automatisch aktualisiert

### **Module einzeln testen:**
1. **Modul öffnen** (z.B. `arbeitsblatt-taeglicher-stimmungscheck.tex`)
2. **Speichern** → PDF wird nur für dieses Modul erstellt
3. **Schnelle Vorschau** ohne das ganze Dokument zu kompilieren

## [FAST] **Vorteile gegenüber unseren Tasks:**

| LaTeX Workshop | Alte Tasks |
|----------------|------------|
| [PASS] Automatisch beim Speichern | [FAIL] Manuell ausführen |
| [PASS] PDF direkt in VS Code | [FAIL] Externe Viewer |
| [PASS] Fehler werden direkt angezeigt | [FAIL] Terminal-Output lesen |
| [PASS] Sync zwischen Code und PDF | [FAIL] Keine Verbindung |
| [PASS] Einzelne Module testbar | [FAIL] Nur komplettes Dokument |

## [TOOLS]️ **Wenn etwas nicht funktioniert:**

### **Build-Fehler anzeigen:**
- **Problems Panel**: `Ctrl+Shift+M`
- **LaTeX Workshop Log**: Unten in der Statusleiste

### **Cache leeren:**
- `Ctrl+Shift+P` → "LaTeX Workshop: Clean up auxiliary files"

### **Unser Tool für Syntaxprüfung:**
```bash
python3 latex-helper.py validate --module <modulname>
```

## [TEST] **Was passiert automatisch:**

### **Beim Speichern von main.tex:**
- Kompiliert komplettes CTMM-System
- Erstellt PDF mit allen Modulen
- Räumt temporäre Dateien auf

### **Beim Speichern einzelner Module:**
- Testet nur dieses Modul
- Schnelle Vorschau
- Syntax-Check

## [DESIGN] **Perfekt für Ihr Matching-Matrix Modul:**
1. **Öffnen**: `modules/corrected-matching-matrix.tex`
2. **Speichern**: `Ctrl+S`
3. **Anzeigen**: PDF öffnet sich automatisch
4. **Bearbeiten**: Live-Sync zwischen Code und PDF

---

** Ergebnis: LaTeX-Entwicklung ohne Terminal-Befehle!**

*Diese Konfiguration ist speziell für Ihr CTMM-Projekt optimiert.*
