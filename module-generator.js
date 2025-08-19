#!/usr/bin/env node

/**
 * CTMM Module Generator
 * 
 * A comprehensive JavaScript-based module generator for the CTMM LaTeX 
 * therapeutic materials system. Creates structured therapy modules with
 * proper German therapeutic conventions and CTMM methodology integration.
 * 
 * Supports three module types:
 * - arbeitsblatt (worksheets): Interactive forms for self-reflection
 * - tool (tools): Therapeutic techniques and coping strategies  
 * - notfallkarte (emergency cards): Crisis intervention protocols
 */

const fs = require('fs');
const path = require('path');
const readline = require('readline');

// CTMM Color scheme for consistent styling
const CTMM_COLORS = {
    blue: 'ctmmBlue',
    orange: 'ctmmOrange', 
    green: 'ctmmGreen',
    purple: 'ctmmPurple',
    red: 'ctmmRed',
    gray: 'ctmmGray',
    yellow: 'ctmmYellow'
};

/**
 * LaTeX Template for Arbeitsblatt (Worksheet) modules
 * Follows CTMM therapeutic worksheet conventions with interactive elements
 */
const ARBEITSBLATT_TEMPLATE = `% CTMM Arbeitsblatt: {{title}}
% Generiert am: {{date}}
% CTMM Methodology: Catch-Track-Map-Match
% 
% Dieses Arbeitsblatt unterstützt die strukturierte Selbstreflexion
% im Rahmen der CTMM-Therapiemethodik für neurodiverse Paare.

\\section{{{title}}}

\\begin{ctmmBlueBox}{Arbeitsblatt-Übersicht}
\\textbf{Zweck:} {{description}}

\\textbf{CTMM-Phase:} {{ctmm_phase}}

\\textbf{Zielgruppe:} {{target_group}}

\\textbf{Bearbeitungszeit:} {{duration}}
\\end{ctmmBlueBox}

\\subsection{Anleitung}

{{instructions}}

\\subsection{Reflexionsfragen}

\\begin{enumerate}
{{reflection_questions}}
\\end{enumerate}

\\subsection{Interaktive Elemente}

\\begin{tabular}{|p{0.7\\textwidth}|p{0.25\\textwidth}|}
\\hline
\\textbf{Bewertungskriterium} & \\textbf{Selbsteinschätzung} \\\\
\\hline
{{interactive_elements}}
\\hline
\\end{tabular}

\\subsection{Tracking und Dokumentation}

\\textbf{Datum:} \\ctmmTextField[4cm]{Datum}{datum}

\\textbf{Aktuelle Stimmung (1-10):} \\ctmmTextField[2cm]{Stimmung}{stimmung}

\\textbf{Notizen und Erkenntnisse:}

\\ctmmTextArea[\\textwidth]{5}{Notizen}{notizen}

\\subsection{Nächste Schritte}

\\begin{ctmmGreenBox}{Handlungsplan}
\\ctmmCheckBox[schritt1]{Nächster konkreter Schritt definiert}

\\ctmmCheckBox[schritt2]{Termin für Nachbesprechung vereinbart}

\\ctmmCheckBox[schritt3]{Supportperson informiert}

\\ctmmTextField[\\textwidth]{Konkreter nächster Schritt}{naechster_schritt}
\\end{ctmmGreenBox}

\\textcolor{ctmmGray}{\\small Dieses Arbeitsblatt ist Teil der CTMM-Therapiematerialien und unterstützt die Catch-Track-Map-Match Methodik für neurodiverse Paare.}
`;

/**
 * LaTeX Template for Tool modules  
 * Structured therapeutic techniques and coping strategies
 */
const TOOL_TEMPLATE = `% CTMM Tool: {{title}}
% Generiert am: {{date}}
% Therapeutic Tool für CTMM Methodology
% 
% Dieses Tool bietet strukturierte Techniken zur Bewältigung
% spezifischer Herausforderungen im Rahmen der CTMM-Therapie.

\\section{{{title}}}

\\begin{ctmmOrangeBox}{Tool-Übersicht}
\\textbf{Anwendungsbereich:} {{application_area}}

\\textbf{CTMM-Phase:} {{ctmm_phase}}

\\textbf{Schwierigkeitsgrad:} {{difficulty_level}}

\\textbf{Benötigte Zeit:} {{duration}}
\\end{ctmmOrangeBox}

\\subsection{Wann wird dieses Tool angewendet?}

{{when_to_use}}

\\subsection{Schritt-für-Schritt Anleitung}

\\begin{enumerate}
{{step_by_step_instructions}}
\\end{enumerate}

\\subsection{Beispiel-Anwendung}

\\begin{ctmmGrayBox}{Praxis-Beispiel}
{{example_application}}
\\end{ctmmGrayBox}

\\subsection{Anpassungen für neurodiverse Paare}

{{neurodiversity_adaptations}}

\\subsection{Erfolgsindikatoren}

\\begin{itemize}
{{success_indicators}}
\\end{itemize}

\\subsection{Troubleshooting}

\\textbf{Was tun, wenn das Tool nicht funktioniert?}

{{troubleshooting_guide}}

\\subsection{Integration in den Alltag}

\\begin{ctmmGreenBox}{Praktische Umsetzung}
\\ctmmCheckBox[integration1]{Tool in Krisenplan integriert}

\\ctmmCheckBox[integration2]{Partner über Tool informiert}

\\ctmmCheckBox[integration3]{Erste Anwendung geplant}

\\ctmmTextField[\\textwidth]{Reminder-System}{reminder_system}
\\end{ctmmGreenBox}

\\textcolor{ctmmGray}{\\small Dieses Tool ist Teil der CTMM-Therapiematerialien und unterstützt die Catch-Track-Map-Match Methodik für neurodiverse Paare.}
`;

/**
 * LaTeX Template for Notfallkarte (Emergency Card) modules
 * Crisis intervention protocols and emergency procedures
 */
const NOTFALLKARTE_TEMPLATE = `% CTMM Notfallkarte: {{title}}
% Generiert am: {{date}}
% Emergency Protocol für CTMM Crisis Intervention
% 
% Diese Notfallkarte bietet sofortige Unterstützung in Krisensituationen
% und folgt den CTMM-Prinzipien für neurodiverse Paare.

\\section{{{title}}}

\\begin{ctmmRedBox}{\\faExclamationTriangle\\space Notfall-Information}
\\textbf{Krisentyp:} {{crisis_type}}

\\textbf{Dringlichkeit:} {{urgency_level}}

\\textbf{Zielgruppe:} {{target_group}}
\\end{ctmmRedBox}

\\subsection{Sofortige Maßnahmen}

\\begin{ctmmYellowBox}{\\faHandStopO\\space STOPP - Erste Hilfe}
\\textbf{1. STOPP:} {{immediate_stop_action}}

\\textbf{2. ATMEN:} {{breathing_instruction}}

\\textbf{3. SICHERHEIT:} {{safety_check}}
\\end{ctmmYellowBox}

\\subsection{5-Schritt Notfall-Protokoll}

\\begin{enumerate}
\\item \\textbf{CATCH:} {{catch_step}}
\\item \\textbf{TRACK:} {{track_step}}  
\\item \\textbf{MAP:} {{map_step}}
\\item \\textbf{MATCH:} {{match_step}}
\\item \\textbf{FOLLOW-UP:} {{followup_step}}
\\end{enumerate}

\\subsection{Beruhigungstechniken}

{{calming_techniques}}

\\subsection{Kontakt-Informationen}

\\begin{ctmmBlueBox}{Wichtige Kontakte}
\\textbf{Therapeut/in:} \\ctmmTextField[6cm]{Therapeut}{therapeut}

\\textbf{Vertrauensperson:} \\ctmmTextField[6cm]{Vertrauensperson}{vertrauensperson}

\\textbf{Krisentelefon:} \\ctmmTextField[6cm]{Krisentelefon}{krisentelefon}

\\textbf{Notfall (112):} \\textcolor{ctmmRed}{\\textbf{112}}
\\end{ctmmBlueBox}

\\subsection{Nachsorge-Checkliste}

\\begin{ctmmGreenBox}{Nach der Krise}
\\ctmmCheckBox[nachsorge1]{Krise ist vorüber - Sicherheit bestätigt}

\\ctmmCheckBox[nachsorge2]{Partner/Vertrauensperson kontaktiert}

\\ctmmCheckBox[nachsorge3]{Therapeut/in informiert}

\\ctmmCheckBox[nachsorge4]{Nächster Termin vereinbart}

\\ctmmTextField[\\textwidth]{Erkenntnisse aus dieser Krise}{erkenntnisse}
\\end{ctmmGreenBox}

\\textcolor{ctmmRed}{\\small \\textbf{Wichtig:} Bei akuter Selbst- oder Fremdgefährdung sofort 112 wählen!}

\\textcolor{ctmmGray}{\\small Diese Notfallkarte ist Teil der CTMM-Therapiematerialien und folgt der Catch-Track-Map-Match Methodik für neurodiverse Paare.}
`;

/**
 * Module Generator Class
 * Handles the creation and customization of CTMM therapy modules
 */
class CTMMModuleGenerator {
    constructor() {
        this.moduleTypes = {
            'arbeitsblatt': {
                name: 'Arbeitsblatt (Worksheet)',
                template: ARBEITSBLATT_TEMPLATE,
                description: 'Interaktive Arbeitsblätter für strukturierte Selbstreflexion'
            },
            'tool': {
                name: 'Tool (Therapeutic Technique)',
                template: TOOL_TEMPLATE,
                description: 'Therapeutische Techniken und Bewältigungsstrategien'
            },
            'notfallkarte': {
                name: 'Notfallkarte (Emergency Card)',
                template: NOTFALLKARTE_TEMPLATE,
                description: 'Kriseninterventions-Protokolle und Notfallprozeduren'
            }
        };
        
        this.rl = readline.createInterface({
            input: process.stdin,
            output: process.stdout
        });
    }

    /**
     * Main entry point for interactive module generation
     */
    async generateModule() {
        try {
            console.log('\n🎯 CTMM Module Generator');
            console.log('=========================================');
            console.log('Erstelle therapeutische Module für die CTMM-Methodik\n');

            // Get module type
            const moduleType = await this.selectModuleType();
            
            // Get module details
            const moduleData = await this.collectModuleData(moduleType);
            
            // Generate filename
            const filename = this.generateFilename(moduleType, moduleData.title);
            
            // Generate module content
            const content = this.populateTemplate(moduleType, moduleData);
            
            // Save module
            await this.saveModule(filename, content);
            
            // Generate TODO file
            await this.generateTodoFile(filename, moduleData);
            
            console.log(`\n✅ Modul erfolgreich erstellt!`);
            console.log(`📁 Datei: modules/${filename}`);
            console.log(`📝 TODO: modules/TODO_${filename.replace('.tex', '.md')}`);
            console.log(`\n💡 Nächste Schritte:`);
            console.log(`   1. Inhalt in modules/${filename} vervollständigen`);
            console.log(`   2. CTMM Build System ausführen: python3 ctmm_build.py`);
            console.log(`   3. TODO-Datei löschen wenn fertig`);
            
        } catch (error) {
            console.error('❌ Fehler beim Generieren des Moduls:', error.message);
        } finally {
            this.rl.close();
        }
    }

    /**
     * Prompts user to select module type
     */
    async selectModuleType() {
        console.log('Verfügbare Modul-Typen:');
        Object.keys(this.moduleTypes).forEach((key, index) => {
            const type = this.moduleTypes[key];
            console.log(`${index + 1}. ${type.name}`);
            console.log(`   ${type.description}\n`);
        });

        const answer = await this.question('Wähle einen Modul-Typ (1-3): ');
        const choice = parseInt(answer) - 1;
        const types = Object.keys(this.moduleTypes);
        
        if (choice < 0 || choice >= types.length) {
            throw new Error('Ungültige Auswahl');
        }
        
        return types[choice];
    }

    /**
     * Collects module-specific data from user
     */
    async collectModuleData(moduleType) {
        const data = {
            title: await this.question('📝 Titel des Moduls: '),
            date: new Date().toLocaleDateString('de-DE'),
            ctmm_phase: await this.question('🎯 CTMM-Phase (Catch/Track/Map/Match): '),
            target_group: await this.question('👥 Zielgruppe: '),
            duration: await this.question('⏱️  Geschätzte Bearbeitungszeit: ')
        };

        // Module-specific questions
        switch (moduleType) {
            case 'arbeitsblatt':
                data.description = await this.question('📋 Beschreibung/Zweck: ');
                data.instructions = await this.question('📖 Kurze Anleitung: ');
                data.reflection_questions = await this.question('❓ Reflexionsfragen (mit \\item getrennt): ');
                data.interactive_elements = await this.question('🔲 Interaktive Elemente (Tabellenzeillen): ');
                break;
                
            case 'tool':
                data.application_area = await this.question('🔧 Anwendungsbereich: ');
                data.difficulty_level = await this.question('📊 Schwierigkeitsgrad (Einfach/Mittel/Schwer): ');
                data.when_to_use = await this.question('⚡ Wann anwenden: ');
                data.step_by_step_instructions = await this.question('📝 Schritte (mit \\item getrennt): ');
                data.example_application = await this.question('💡 Beispiel-Anwendung: ');
                data.neurodiversity_adaptations = await this.question('🧠 Anpassungen für Neurodiversität: ');
                data.success_indicators = await this.question('✅ Erfolgsindikatoren (mit \\item getrennt): ');
                data.troubleshooting_guide = await this.question('🔧 Troubleshooting-Hinweise: ');
                break;
                
            case 'notfallkarte':
                data.crisis_type = await this.question('🚨 Krisentyp: ');
                data.urgency_level = await this.question('⚠️  Dringlichkeit (Niedrig/Mittel/Hoch/Kritisch): ');
                data.immediate_stop_action = await this.question('🛑 Sofortige STOPP-Aktion: ');
                data.breathing_instruction = await this.question('🫁 Atemtechnik-Anweisung: ');
                data.safety_check = await this.question('🔒 Sicherheitscheck: ');
                data.catch_step = await this.question('🎯 CATCH-Schritt: ');
                data.track_step = await this.question('📊 TRACK-Schritt: ');
                data.map_step = await this.question('🗺️  MAP-Schritt: ');
                data.match_step = await this.question('🤝 MATCH-Schritt: ');
                data.followup_step = await this.question('📋 FOLLOW-UP-Schritt: ');
                data.calming_techniques = await this.question('😌 Beruhigungstechniken: ');
                break;
        }

        return data;
    }

    /**
     * Generates appropriate filename based on module type and title
     */
    generateFilename(moduleType, title) {
        // Convert title to URL-friendly format
        const slug = title
            .toLowerCase()
            .replace(/[äöüß]/g, match => ({
                'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'ß': 'ss'
            })[match])
            .replace(/[^a-z0-9]/g, '-')
            .replace(/-+/g, '-')
            .replace(/^-|-$/g, '');
            
        return `${moduleType}-${slug}.tex`;
    }

    /**
     * Populates template with user data
     */
    populateTemplate(moduleType, data) {
        let template = this.moduleTypes[moduleType].template;
        
        // Replace all placeholders
        Object.keys(data).forEach(key => {
            const placeholder = `{{${key}}}`;
            template = template.replace(new RegExp(placeholder.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g'), data[key] || '');
        });
        
        return template;
    }

    /**
     * Saves generated module to file
     */
    async saveModule(filename, content) {
        const modulesDir = path.join(process.cwd(), 'modules');
        const filePath = path.join(modulesDir, filename);
        
        // Ensure modules directory exists
        if (!fs.existsSync(modulesDir)) {
            fs.mkdirSync(modulesDir, { recursive: true });
        }
        
        // Check if file already exists
        if (fs.existsSync(filePath)) {
            const overwrite = await this.question(`⚠️  Datei ${filename} existiert bereits. Überschreiben? (y/n): `);
            if (overwrite.toLowerCase() !== 'y') {
                throw new Error('Vorgang abgebrochen');
            }
        }
        
        fs.writeFileSync(filePath, content, 'utf8');
    }

    /**
     * Generates TODO file for module completion tracking
     */
    async generateTodoFile(filename, moduleData) {
        const todoContent = `# TODO: ${filename}

## Modul-Vervollständigung

Dieses Modul wurde automatisch generiert und benötigt noch inhaltliche Vervollständigung.

### ✅ Bereits erstellt
- [x] Grundstruktur mit CTMM-Template
- [x] LaTeX-Formatierung und Farbschema
- [x] Interaktive Elemente (Checkboxen, Textfelder)
- [x] CTMM-Methodologie Integration

### 📝 Noch zu vervollständigen
- [ ] Detaillierte Inhalte ergänzen
- [ ] Beispiele und Praxis-Szenarien hinzufügen
- [ ] Therapeutische Anweisungen verfeinern
- [ ] Qualitätskontrolle und Review
- [ ] Integration mit anderen Modulen prüfen

### 🎯 CTMM-Spezifische Anforderungen
- [ ] Catch-Track-Map-Match Methodik korrekt implementiert
- [ ] Deutsche therapeutische Terminologie verwendet
- [ ] Neurodiversitäts-Aspekte berücksichtigt
- [ ] Paartherapie-Kontext integriert

### 🔧 Technische Prüfung
- [ ] LaTeX-Syntax validiert
- [ ] CTMM Build System Test erfolgreich
- [ ] PDF-Generierung funktioniert
- [ ] Interaktive Elemente funktional

### 📚 Referenzen
- CTMM Methodology: Catch-Track-Map-Match
- Zielgruppe: ${moduleData.target_group}
- CTMM-Phase: ${moduleData.ctmm_phase}

**Wichtig:** Lösche diese TODO-Datei, wenn das Modul vollständig ist!
`;

        const todoFilename = `TODO_${filename.replace('.tex', '.md')}`;
        const todoPath = path.join(process.cwd(), 'modules', todoFilename);
        
        fs.writeFileSync(todoPath, todoContent, 'utf8');
    }

    /**
     * Utility method for readline questions
     */
    question(query) {
        return new Promise(resolve => {
            this.rl.question(query, resolve);
        });
    }
}

// CLI interface
if (require.main === module) {
    const generator = new CTMMModuleGenerator();
    
    // Handle command line arguments
    const args = process.argv.slice(2);
    
    if (args.includes('--help') || args.includes('-h')) {
        console.log(`
🎯 CTMM Module Generator - Hilfe

VERWENDUNG:
  node module-generator.js                    # Interaktiver Modus
  node module-generator.js --help             # Diese Hilfe anzeigen

MODUL-TYPEN:
  arbeitsblatt    Interaktive Arbeitsblätter für Selbstreflexion
  tool           Therapeutische Techniken und Bewältigungsstrategien  
  notfallkarte   Kriseninterventions-Protokolle

CTMM METHODOLOGY:
  Die generierten Module folgen der Catch-Track-Map-Match Methodik
  für neurodiverse Paare und therapeutische Interventionen.

AUSGABE:
  modules/[typ]-[titel].tex           # Generiertes LaTeX-Modul
  modules/TODO_[typ]-[titel].md       # Vervollständigungs-Checkliste

INTEGRATION:
  Nach der Generierung das CTMM Build System ausführen:
  python3 ctmm_build.py
        `);
        process.exit(0);
    }
    
    // Start interactive module generation
    generator.generateModule().catch(error => {
        console.error('❌ Unerwarteter Fehler:', error);
        process.exit(1);
    });
}

module.exports = CTMMModuleGenerator;