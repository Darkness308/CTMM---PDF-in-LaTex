# [TARGET] CTMM Form Elements - Komplette Anleitung

## [PASS] **Was Sie jetzt haben:**

Ihr `form-elements.sty` Paket kann **zwei Modi**:
- **[MOBILE] Interaktiver Modus** (mit hyperref): Echte PDF-Formularfelder
- **️ Print-Modus** (ohne hyperref): Saubere Unterstriche zum Handausfüllen

## [TOOLS]️ **Sofort verfügbare Befehle:**

### **Basis-Eingaben:**
```latex
\ctmmTextField[6cm]{Default Text}{fieldname}  % Einzeiliges Textfeld
\ctmmTextArea[12cm]{3}{fieldname}{Default}  % Mehrzeiliger Text (3 Zeilen)
\ctmmCheckBox[fieldname]{Label}  % Checkbox
\ctmmRadioButton{group}{value}{label}  % Radio Button
```

### **Datum & Zeit:**
```latex
\ctmmDate{prefix}  % "Datum: [____]"
\ctmmTime{prefix}  % "Zeit: [____] Uhr"
```

### **CTMM-Spezifische Skalen:**
```latex
\ctmmEmotionScale{Stimmung}{fieldgroup}  % 1-10 Skala mit Radio Buttons
\ctmmStressLevel{prefix}  % Stresslevel 10-100
\ctmmTriggerScale{prefix}  % Grün/Orange/Rot Trigger-Intensität
\ctmmYesNo{prefix}  % Ja/Nein Checkboxen
```

### **Fertige Komponenten:**
```latex
\ctmmSafeWordOptions{prefix}  % Anker/Reset/Eiszeit + Freitext
\ctmmWeeklyPattern{prefix}  % Mo-So Wochentabelle
\ctmmDailyTracker{prefix}  % Kompletter Tagescheck
\ctmmCrisisForm{prefix}  % Krisen-Protokoll (rot)
```

## [DESIGN] **Praktische Beispiele:**

### **1. Einfaches Tages-Arbeitsblatt:**
```latex
\begin{ctmmGreenBox}[title=Mein Tagescheck]
\ctmmDate{heute} \quad \ctmmTime{heute}

\ctmmEmotionScale{Morgenstimmung}{heute-morgen}
\ctmmStressLevel{heute}

\textbf{Notizen:}
\ctmmTextArea[14cm]{3}{heute-notizen}{}
\end{ctmmGreenBox}
```

### **2. Trigger-Management:**
```latex
\begin{ctmmOrangeBox}[title=Trigger-Analyse]
\ctmmTriggerScale{trigger01}
\ctmmSafeWordOptions{trigger01}

\textbf{Verwendete Strategien:}
\ctmmCheckBox[t01-breathing]{Atemtechnik} \quad
\ctmmCheckBox[t01-grounding]{Grounding} \quad
\ctmmCheckBox[t01-pause]{Pause}
\end{ctmmOrangeBox}
```

### **3. Krisen-Protokoll:**
```latex
\ctmmCrisisForm{notfall01}
```

## [TEST] **Integration in Ihre Module:**

**Schritt 1:** In beliebiges .tex-Modul einfügen:
```latex
% Ihr gewöhnlicher Modultext...

% Dann Interactive Form:
\subsection*{\textcolor{ctmmBlue}{Interaktiver Bereich}}
\ctmmDailyTracker{modulname}
```

**Schritt 2:** PDF bauen mit Ctrl+S (automatisch!)

## [SYNC] **Zwei Ausgabeversionen:**

1. **Digital** (am Computer ausfüllen):
  - Formularfelder anklickbar
  - Daten speicherbar
  - Professioneller Look

2. **Print** (handschriftlich ausfüllen):
  - Saubere Unterstriche
  - Optimiert für Handschrift
  - Identisches Layout

## [TARGET] **Nächste Schritte:**

1. **Testen:** Öffnen Sie `build/main.pdf` → Seite 25-27 anschauen
2. **Experimentieren:** Kopieren Sie eines der Beispiele in ein neues Modul
3. **Anpassen:** Verwenden Sie `\ctmmTextField` in bestehenden Arbeitsblättern

## [IDEA] **Pro-Tipps:**

- **Feldnamen:** Verwenden Sie eindeutige Präfixe (z.B. `woche01`, `trigger05`)
- **Breiten:** `[3cm]` für kurze Felder, `[12cm]` für längere Texte
- **Zeilen:** Bei `\ctmmTextArea` → `{3}` = 3 Zeilen
- **Farben:** Nutzen Sie die CTMM-Farbboxen für thematische Gruppierung

**Ihr Form-Elements-System ist einsatzbereit! [DEPLOY]**
