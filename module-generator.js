#!/usr/bin/env node

/**
 * CTMM Module Generator
 * Generates LaTeX therapy modules (arbeitsblatt, tool, notfallkarte) for the CTMM system
 */

const fs = require('fs');
const path = require('path');
const readline = require('readline');

class CTMMModuleGenerator {
    constructor() {
        this.templates = {
            arbeitsblatt: this.getArbeitsblattTemplate(),
            tool: this.getToolTemplate(),
            notfallkarte: this.getNotfallkarteTemplate()
        };
    }

    /**
     * Template for therapeutic worksheets (Arbeitsblätter)
     */
    getArbeitsblattTemplate() {
        return `% {{title}}
% CTMM Arbeitsblatt - Automatisch generiert

\\section{{{title}}}

\\begin{ctmmBlueBox}{Arbeitsblatt: {{title}}}
    Dieses Arbeitsblatt hilft dabei, {{description}}.
\\end{ctmmBlueBox}

\\subsection{Anleitung}

{{instructions}}

\\subsection{Reflexionsfragen}

\\begin{enumerate}
    \\item {{question1}}
    \\item {{question2}}
    \\item {{question3}}
\\end{enumerate}

\\subsection{Meine Notizen}

\\ctmmTextArea[15cm]{5}{Notizen}{notes}

\\subsection{Datum und Unterschrift}

\\begin{tabular}{p{6cm}p{6cm}}
    \\textbf{Datum:} & \\ctmmTextField[4cm]{}{date} \\\\[1cm]
    \\textbf{Unterschrift:} & \\ctmmTextField[4cm]{}{signature} \\\\
\\end{tabular}

\\vfill
\\begin{center}
    \\textcolor{ctmmGray}{\\small Generiert mit CTMM Module Generator}
\\end{center}
`;
    }

    /**
     * Template for therapeutic tools
     */
    getToolTemplate() {
        return `% {{title}}
% CTMM Tool - Automatisch generiert

\\section{{{title}}}

\\begin{ctmmGreenBox}{Therapeutisches Tool}
    {{description}}
\\end{ctmmGreenBox}

\\subsection{Anwendung}

{{instructions}}

\\subsection{Schritte}

\\begin{enumerate}
    \\item {{step1}}
    \\item {{step2}}
    \\item {{step3}}
    \\item {{step4}}
    \\item {{step5}}
\\end{enumerate}

\\subsection{Tipps für die Praxis}

\\begin{itemize}
    \\item {{tip1}}
    \\item {{tip2}}
    \\item {{tip3}}
\\end{itemize}

\\subsection{Persönliche Erfahrungen}

\\ctmmTextArea[15cm]{4}{Meine Erfahrungen mit dieser Technik}{experiences}

\\vfill
\\begin{center}
    \\textcolor{ctmmGray}{\\small Generiert mit CTMM Module Generator}
\\end{center}
`;
    }

    /**
     * Template for emergency cards (Notfallkarten)
     */
    getNotfallkarteTemplate() {
        return `% {{title}}
% CTMM Notfallkarte - Automatisch generiert

\\section{{{title}}}

\\begin{ctmmRedBox}{Notfallkarte}
    \\textbf{{{title}}} \\\\
    {{description}}
\\end{ctmmRedBox}

\\subsection{Sofortmaßnahmen}

\\begin{enumerate}
    \\setlength{\\itemsep}{0.5em}
    \\item \\textbf{{{action1}}}
    \\item \\textbf{{{action2}}}
    \\item \\textbf{{{action3}}}
    \\item \\textbf{{{action4}}}
    \\item \\textbf{{{action5}}}
\\end{enumerate}

\\subsection{Wichtige Kontakte}

\\begin{tabular}{p{4cm}p{8cm}}
    \\textbf{Notfallnummer:} & \\ctmmTextField[6cm]{}{emergency_contact} \\\\[0.5cm]
    \\textbf{Therapeut:} & \\ctmmTextField[6cm]{}{therapist} \\\\[0.5cm]
    \\textbf{Vertrauensperson:} & \\ctmmTextField[6cm]{}{trusted_person} \\\\
\\end{tabular}

\\subsection{Persönliche Notizen}

\\ctmmTextArea[15cm]{3}{Was hilft mir in der Situation}{personal_notes}

\\vfill
\\begin{center}
    \\textcolor{ctmmRed}{\\small \\textbf{NOTFALLKARTE} - Generiert mit CTMM Module Generator}
\\end{center}
`;
    }

    /**
     * Create a new module file
     */
    async generateModule(type, filename, variables) {
        if (!this.templates[type]) {
            throw new Error(`Unknown module type: ${type}. Available types: ${Object.keys(this.templates).join(', ')}`);
        }

        let content = this.templates[type];
        
        // Replace all template variables
        for (const [key, value] of Object.entries(variables)) {
            const regex = new RegExp(`\\{\\{${key}\\}\\}`, 'g');
            content = content.replace(regex, value);
        }

        const filepath = path.join('modules', `${filename}.tex`);
        
        // Ensure modules directory exists
        if (!fs.existsSync('modules')) {
            fs.mkdirSync('modules', { recursive: true });
        }

        fs.writeFileSync(filepath, content, 'utf8');
        console.log(`✓ Generated ${type} module: ${filepath}`);
        
        return filepath;
    }

    /**
     * Interactive module creation
     */
    async createInteractiveModule() {
        const rl = readline.createInterface({
            input: process.stdin,
            output: process.stdout
        });

        const question = (prompt) => new Promise((resolve) => {
            rl.question(prompt, resolve);
        });

        try {
            console.log('🏥 CTMM Module Generator');
            console.log('========================\n');

            const type = await question('Modultyp (arbeitsblatt/tool/notfallkarte): ');
            if (!this.templates[type]) {
                throw new Error(`Unbekannter Modultyp: ${type}`);
            }

            const filename = await question('Dateiname (ohne .tex): ');
            const title = await question('Titel: ');
            const description = await question('Beschreibung: ');

            const variables = { title, description };

            if (type === 'arbeitsblatt') {
                variables.instructions = await question('Anleitung: ');
                variables.question1 = await question('Reflexionsfrage 1: ');
                variables.question2 = await question('Reflexionsfrage 2: ');
                variables.question3 = await question('Reflexionsfrage 3: ');
            } else if (type === 'tool') {
                variables.instructions = await question('Anwendungshinweise: ');
                variables.step1 = await question('Schritt 1: ');
                variables.step2 = await question('Schritt 2: ');
                variables.step3 = await question('Schritt 3: ');
                variables.step4 = await question('Schritt 4: ');
                variables.step5 = await question('Schritt 5: ');
                variables.tip1 = await question('Tipp 1: ');
                variables.tip2 = await question('Tipp 2: ');
                variables.tip3 = await question('Tipp 3: ');
            } else if (type === 'notfallkarte') {
                variables.action1 = await question('Sofortmaßnahme 1: ');
                variables.action2 = await question('Sofortmaßnahme 2: ');
                variables.action3 = await question('Sofortmaßnahme 3: ');
                variables.action4 = await question('Sofortmaßnahme 4: ');
                variables.action5 = await question('Sofortmaßnahme 5: ');
            }

            const filepath = await this.generateModule(type, filename, variables);

            console.log(`\n✅ Modul erfolgreich erstellt: ${filepath}`);
            console.log('\n📝 Nächste Schritte:');
            console.log(`1. Fügen Sie diese Zeile zu main.tex hinzu: \\input{modules/${filename}}`);
            console.log('2. Führen Sie "python3 ctmm_build.py" aus, um das System zu testen');
            console.log('3. Kompilieren Sie das Dokument mit pdflatex oder VS Code');

        } catch (error) {
            console.error('❌ Fehler:', error.message);
        } finally {
            rl.close();
        }
    }

    /**
     * Command line interface
     */
    async run() {
        const args = process.argv.slice(2);

        if (args.length === 0) {
            return this.createInteractiveModule();
        }

        // Command line usage: node module-generator.js <type> <filename> [options]
        if (args[0] === '--help' || args[0] === '-h') {
            this.showHelp();
            return;
        }

        if (args.length < 2) {
            console.error('❌ Fehler: Typ und Dateiname erforderlich');
            this.showHelp();
            process.exit(1);
        }

        const [type, filename] = args;
        
        // Default variables for command line usage
        const variables = {
            title: filename.replace(/-/g, ' ').replace(/^\w/, c => c.toUpperCase()),
            description: 'Beschreibung hier eingeben',
            instructions: 'Anleitung hier eingeben',
            question1: 'Erste Reflexionsfrage',
            question2: 'Zweite Reflexionsfrage', 
            question3: 'Dritte Reflexionsfrage',
            step1: 'Erster Schritt',
            step2: 'Zweiter Schritt',
            step3: 'Dritter Schritt',
            step4: 'Vierter Schritt',
            step5: 'Fünfter Schritt',
            tip1: 'Erster Tipp',
            tip2: 'Zweiter Tipp',
            tip3: 'Dritter Tipp',
            action1: 'Erste Sofortmaßnahme',
            action2: 'Zweite Sofortmaßnahme',
            action3: 'Dritte Sofortmaßnahme',
            action4: 'Vierte Sofortmaßnahme',
            action5: 'Fünfte Sofortmaßnahme'
        };

        try {
            const filepath = await this.generateModule(type, filename, variables);
            console.log(`\n✅ Modul erstellt: ${filepath}`);
            console.log('📝 Bitte bearbeiten Sie die Platzhalter-Inhalte in der generierten Datei.');
        } catch (error) {
            console.error('❌ Fehler:', error.message);
            process.exit(1);
        }
    }

    showHelp() {
        console.log(`
🏥 CTMM Module Generator - Hilfe

VERWENDUNG:
    node module-generator.js                     # Interaktiver Modus
    node module-generator.js <typ> <dateiname>   # Kommandozeilen Modus

MODULTYPEN:
    arbeitsblatt    # Therapeutisches Arbeitsblatt
    tool           # Therapeutisches Tool/Technik
    notfallkarte   # Notfallkarte für Krisensituationen

BEISPIELE:
    node module-generator.js arbeitsblatt stimmungscheck
    node module-generator.js tool atemtechnik
    node module-generator.js notfallkarte panikattacken

OPTIONEN:
    --help, -h     # Diese Hilfe anzeigen
`);
    }
}

// Run the generator if called directly
if (require.main === module) {
    const generator = new CTMMModuleGenerator();
    generator.run().catch(error => {
        console.error('❌ Unerwarteter Fehler:', error);
        process.exit(1);
    });
}

module.exports = CTMMModuleGenerator;