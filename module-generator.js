#!/usr/bin/env node

/**
 * CTMM Module Generator
 * Purpose: Auto-generate new CTMM modules from templates
 * Usage: node module-generator.js <type> <name>
 * Angepasst für: /workspaces/CTMM---PDF-in-LaTex
 */

const fs = require('fs');
const path = require('path');

// CTMM Module Templates - angepasst an Ihre bestehende Struktur
const templates = {
    arbeitsblatt: `% =====================================================
% CTMM {{MODULE_NAME}} Arbeitsblatt
% Purpose: {{PURPOSE}}
% Context: Neurodiverse Paare - {{CONTEXT}}
% Author: CTMM-Team
% Integration: \\input{modules/{{FILENAME}}}
% =====================================================

\\section*{\\textcolor{{{COLOR}}}{\\{{ICON}}~{{TITLE}}}}

\\begin{quote}
\\textbf{\\textcolor{{{COLOR}}}{Worum geht's hier -- für Freunde?}}\\\\
{{DESCRIPTION}}
\\end{quote}

\\textit{{{USAGE_NOTE}}}

\\subsection*{\\textcolor{{{COLOR}}}{Ausfüllbereich}}

\\begin{{{BOX_TYPE}}}[title={{SECTION_TITLE}}]
\\begin{itemize}
  \\item \\textbf{Datum:} \\underline{\\hspace{3cm}} \\textbf{Zeit:} \\underline{\\hspace{2cm}}
  \\item \\textbf{{{FIELD_1}}:} \\underline{\\hspace{5cm}}
  \\item \\textbf{{{FIELD_2}}:} \\underline{\\hspace{5cm}}
  \\item \\textbf{{{FIELD_3}}:} \\underline{\\hspace{5cm}}
\\end{itemize}

\\vspace{0.5cm}
\\textbf{Notizen:}\\\\
\\underline{\\hspace{\\textwidth}}\\\\
\\underline{\\hspace{\\textwidth}}\\\\
\\underline{\\hspace{\\textwidth}}
\\end{{{BOX_TYPE}}}

\\subsection*{\\textcolor{ctmmPurple}{Reflexion}}
\\textbf{Was war heute anders:}\\\\
\\underline{\\hspace{\\textwidth}}\\\\
\\underline{\\hspace{\\textwidth}}

\\subsection*{\\textcolor{ctmmBlue}{CTMM-Navigation}}
\\begin{itemize}
  \\item \\texttt{{{RELATED_MODULE_1}}} ← {{RELATION_1}}
  \\item \\texttt{{{RELATED_MODULE_2}}} ← {{RELATION_2}}
\\end{itemize}`,

    tool: `% =====================================================
% CTMM Tool {{TOOL_NUMBER}}: {{MODULE_NAME}}
% Purpose: {{PURPOSE}}
% Context: {{CONTEXT}}
% Author: CTMM-Team
% Integration: \\input{modules/{{FILENAME}}}
% =====================================================

\\section*{\\textcolor{{{COLOR}}}{\\{{ICON}}~Tool {{TOOL_NUMBER}}: {{TITLE}}}}

\\begin{quote}
\\textbf{\\textcolor{{{COLOR}}}{Worum geht's hier?}}\\\\
{{DESCRIPTION}}
\\end{quote}

\\subsection*{\\textcolor{{{COLOR}}}{Anwendung}}

\\begin{{{BOX_TYPE}}}[title=Schritt-für-Schritt Anleitung]
\\begin{enumerate}
  \\item \\textbf{{{STEP_1}}}
  \\item \\textbf{{{STEP_2}}}
  \\item \\textbf{{{STEP_3}}}
  \\item \\textbf{{{STEP_4}}}
\\end{enumerate}
\\end{{{BOX_TYPE}}}

\\subsection*{\\textcolor{ctmmPurple}{Praxis-Beispiel}}
\\begin{{{BOX_TYPE_EXAMPLE}}}[title=So könnte es aussehen]
\\textbf{Situation:} {{EXAMPLE_SITUATION}}\\\\
\\textbf{Anwendung:} {{EXAMPLE_APPLICATION}}\\\\
\\textbf{Ergebnis:} {{EXAMPLE_RESULT}}
\\end{{{BOX_TYPE_EXAMPLE}}}

\\subsection*{\\textcolor{ctmmBlue}{CTMM-Navigation}}
\\begin{itemize}
  \\item \\texttt{{{RELATED_MODULE_1}}} ← {{RELATION_1}}
  \\item \\texttt{{{RELATED_MODULE_2}}} ← {{RELATION_2}}
\\end{itemize}`,

    notfallkarte: `% =====================================================
% CTMM {{MODULE_NAME}} Notfallkarte
% Purpose: Schnelle Hilfe in Krisensituationen
% Context: {{CONTEXT}}
% Author: CTMM-Team
% Integration: \\input{modules/{{FILENAME}}}
% =====================================================

\\section*{\\textcolor{ctmmRed}{\\faExclamationTriangle~{{TITLE}} -- Notfallkarte}}

\\begin{ctmmRedBox}[title=\\textcolor{white}{\\textbf{SOFORTMASSNAHMEN}}]
\\textcolor{white}{\\textbf{1. STOPP:}} \\textcolor{white}{{{STOP_ACTION}}}\\\\
\\textcolor{white}{\\textbf{2. SIGNAL:}} \\textcolor{white}{{{SIGNAL_ACTION}}}\\\\
\\textcolor{white}{\\textbf{3. HILFE:}} \\textcolor{white}{{{HELP_ACTION}}}\\\\
\\textcolor{white}{\\textbf{4. SICHERHEIT:}} \\textcolor{white}{{{SAFETY_ACTION}}}
\\end{ctmmRedBox}

\\subsection*{\\textcolor{ctmmOrange}{Safe-Words \& Signale}}
\\begin{ctmmOrangeBox}[title=Notfall-Kommunikation]
\\begin{itemize}
  \\item \\textbf{"{{SAFE_WORD_1}}"} → {{MEANING_1}}
  \\item \\textbf{"{{SAFE_WORD_2}}"} → {{MEANING_2}}
  \\item \\textbf{Körpersprache:} {{BODY_SIGNAL}}
\\end{itemize}
\\end{ctmmOrangeBox}

\\subsection*{\\textcolor{ctmmGreen}{Nach der Krise}}
\\begin{ctmmGreenBox}[title=Nachsorge \& Reflexion]
\\begin{enumerate}
  \\item \\textbf{Beruhigung:} {{CALM_DOWN}}
  \\item \\textbf{Gespräch:} {{TALK_STEP}}
  \\item \\textbf{Lernen:} {{LEARN_STEP}}
\\end{enumerate}
\\end{ctmmGreenBox}

\\subsection*{\\textcolor{ctmmBlue}{CTMM-Navigation}}
\\begin{itemize}
  \\item \\texttt{safewords} ← Grundlagen der Kommunikation
  \\item \\texttt{triggermanagement} ← Präventive Maßnahmen
\\end{itemize}`
};

// Konfiguration für verschiedene Modul-Typen
const moduleConfig = {
    arbeitsblatt: {
        color: 'ctmmGreen',
        icon: 'faEdit',
        folder: 'modules/',
        prefix: 'arbeitsblatt-',
        boxType: 'ctmmGreenBox',
        purpose: 'Strukturierte Selbstreflexion und Dokumentation',
        context: 'Tägliche Routine und Mustererkennung'
    },
    tool: {
        color: 'ctmmOrange', 
        icon: 'faCog',
        folder: 'modules/',
        prefix: 'tool-',
        boxType: 'ctmmOrangeBox',
        boxTypeExample: 'ctmmBlueBox',
        purpose: 'Praktische Intervention und Skill-Anwendung',
        context: 'Akutphasen und Ko-Regulation'
    },
    notfallkarte: {
        color: 'ctmmRed',
        icon: 'faExclamationTriangle', 
        folder: 'modules/',
        prefix: 'notfall-',
        boxType: 'ctmmRedBox',
        purpose: 'Sofortige Hilfe in Krisensituationen',
        context: 'Eskalationsmanagement und Sicherheit'
    }
};

function generateModule(type, name) {
    if (!templates[type]) {
        console.error(`❌ Unbekannter Modul-Typ: ${type}`);
        console.log(`✅ Verfügbare Typen: ${Object.keys(templates).join(', ')}`);
        return;
    }

    const config = moduleConfig[type];
    const template = templates[type];
    
    // Dateiname erstellen
    const baseFilename = name.toLowerCase()
        .replace(/ä/g, 'ae')
        .replace(/ö/g, 'oe') 
        .replace(/ü/g, 'ue')
        .replace(/ß/g, 'ss')
        .replace(/[^a-z0-9]/g, '-')
        .replace(/-+/g, '-')
        .replace(/^-|-$/g, '');
    
    const filename = `${config.prefix}${baseFilename}`;
    
    // Bestimme nächste Tool-Nummer für tool-Module
    let nextToolNumber = 1;
    if (type === 'tool') {
        const files = fs.readdirSync(config.folder);
        const numbers = [];
        files.forEach(file => {
            if (file.startsWith(config.prefix) && file.endsWith('.tex')) {
                const data = fs.readFileSync(path.join(config.folder, file), 'utf8');
                const m = data.match(/Tool\s+(\d+):/);
                if (m) numbers.push(parseInt(m[1], 10));
            }
        });
        if (numbers.length) {
            nextToolNumber = Math.max(...numbers) + 1;
        }
    }

    // Placeholder-Objekt erstellen
    const placeholders = {
        MODULE_NAME: name,
        TITLE: name.charAt(0).toUpperCase() + name.slice(1),
        COLOR: config.color,
        ICON: config.icon,
        PURPOSE: config.purpose,
        CONTEXT: config.context,
        DESCRIPTION: `Dieses ${type === 'arbeitsblatt' ? 'Arbeitsblatt' : type} unterstützt Sie bei ${name.toLowerCase()}.`,
        USAGE_NOTE: `Anwendung: Regelmäßig ausfüllen und als Teil Ihrer CTMM-Routine nutzen`,
        SECTION_TITLE: `${name} Dokumentation`,
        FIELD_1: 'Ausgangssituation',
        FIELD_2: 'Angewendete Strategie', 
        FIELD_3: 'Wirksamkeit (1-10)',
        TOOL_NUMBER: nextToolNumber,
        STEP_1: 'Situation erfassen und bewerten',
        STEP_2: 'Passende Intervention aus CTMM-System wählen', 
        STEP_3: 'Technik anwenden und beobachten',
        STEP_4: 'Wirkung dokumentieren und bei Bedarf anpassen',
        RELATED_MODULE_1: 'bindungsleitfaden',
        RELATED_MODULE_2: 'triggermanagement',
        RELATION_1: 'Grundlagen für sichere Anwendung',
        RELATION_2: 'Ergänzende Strategien und Vertiefung',
        BOX_TYPE: config.boxType,
        BOX_TYPE_EXAMPLE: config.boxTypeExample || config.boxType,
        FILENAME: filename,
        // Notfallkarten-spezifische Felder
        STOP_ACTION: 'Reizunterbrechung, Ort wechseln, tief durchatmen',
        SIGNAL_ACTION: 'Safe-Word verwenden oder vereinbartes Zeichen',
        HELP_ACTION: 'Support-Person kontaktieren oder Notfallkontakt',
        SAFETY_ACTION: 'Sicheren Rückzugsort aufsuchen',
        SAFE_WORD_1: 'ANKER',
        SAFE_WORD_2: 'RESET',
        MEANING_1: 'Sofortiger Stopp aller Aktivitäten, Beruhigung nötig',
        MEANING_2: 'Neustart des Gesprächs ohne Vorwürfe oder Schuldzuweisungen',
        BODY_SIGNAL: 'Hand auf Herz = "Ich brauche eine Pause"',
        CALM_DOWN: '10 Minuten Ruhe, bewusst atmen',
        TALK_STEP: 'Ruhiges Gespräch über Auslöser und Gefühle',
        LEARN_STEP: 'Was können wir beim nächsten Mal anders machen?',
        // Tool-spezifische Beispiele
        EXAMPLE_SITUATION: 'Partner zeigt Stress-Anzeichen, Spannung steigt',
        EXAMPLE_APPLICATION: 'Safe-Word "ANKER" verwenden, gemeinsam durchatmen',
        EXAMPLE_RESULT: 'Entspannung tritt ein, Gespräch wird möglich'
    };

    // Template mit Platzhaltern füllen
    let content = template;
    Object.entries(placeholders).forEach(([key, value]) => {
        const regex = new RegExp(`{{${key}}}`, 'g');
        content = content.replace(regex, value);
    });

    // Datei erstellen
    const filepath = path.join(config.folder, `${filename}.tex`);
    
    try {
        fs.writeFileSync(filepath, content);
        console.log(`✅ Modul erstellt: ${filepath}`);
        console.log(`🎨 Farbe: ${config.color}`);
        console.log(`📝 Typ: ${type}`);
        console.log(`🔗 Zum Einbinden in main.tex: \\input{${filename}}`);
        console.log(`📋 Kopieren Sie diese Zeile in Ihre main.tex an der gewünschten Stelle!`);
    } catch (error) {
        console.error(`❌ Fehler beim Erstellen: ${error.message}`);
    }
}

// CLI Interface
if (require.main === module) {
    const [,, type, name] = process.argv;
    
    if (!type || !name) {
        console.log(`
🧩 CTMM Module Generator für LaTeX-Projekt

Usage: node module-generator.js <type> <name>

Verfügbare Typen:
  arbeitsblatt  - Interaktive Formulare und Tracking-Bögen
  tool         - Interventions-Tools und Skill-Anleitungen  
  notfallkarte - Krisenprotokolle und Sofortmaßnahmen

Beispiele:
  node module-generator.js arbeitsblatt "Wochenreflexion"
  node module-generator.js tool "Atemtechnik-Guide"
  node module-generator.js notfallkarte "Disso-Protokoll"

Die generierten Dateien werden im modules/ Ordner erstellt.
        `);
        process.exit(1);
    }
    
    generateModule(type, name);
}

module.exports = { generateModule, templates, moduleConfig };
