#!/bin/bash

# CTMM Create Module - Interactive Shell Script
# 
# Simplified wrapper for the CTMM Module Generator that provides
# a user-friendly interface for creating therapeutic modules with
# proper CTMM methodology integration.
#
# Author: CTMM Development Team
# Version: 1.0
# Compatible with: CTMM LaTeX therapeutic materials system

set -e  # Exit on any error

# Colors for enhanced UX
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# CTMM Logo and branding
print_header() {
    echo -e "${BLUE}"
    echo "  ╔══════════════════════════════════════════════════════════════════════╗"
    echo "  ║                        CTMM Module Creator                           ║"
    echo "  ║                  Catch-Track-Map-Match Therapy System                ║"
    echo "  ╚══════════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo ""
    echo -e "${CYAN}Erstelle strukturierte Therapiematerialien für neurodiverse Paare${NC}"
    echo ""
}

# Check prerequisites
check_prerequisites() {
    echo -e "${YELLOW}🔍 Überprüfe Systemvoraussetzungen...${NC}"
    
    # Check if Node.js is available
    if ! command -v node &> /dev/null; then
        echo -e "${RED}❌ Node.js ist nicht installiert oder nicht im PATH${NC}"
        echo -e "${YELLOW}💡 Bitte installiere Node.js für den Module Generator${NC}"
        echo ""
        echo "Installation auf verschiedenen Systemen:"
        echo "  • Ubuntu/Debian: sudo apt-get install nodejs"
        echo "  • macOS: brew install node"
        echo "  • Windows: https://nodejs.org/en/download/"
        echo ""
        exit 1
    fi
    
    # Check if we're in the right directory
    if [[ ! -f "main.tex" ]] || [[ ! -d "modules" ]]; then
        echo -e "${RED}❌ Nicht im CTMM-Projektverzeichnis${NC}"
        echo -e "${YELLOW}💡 Bitte führe dieses Script im Hauptverzeichnis des CTMM-Projekts aus${NC}"
        echo ""
        echo "Erwartete Struktur:"
        echo "  • main.tex (LaTeX Hauptdatei)"
        echo "  • modules/ (Module-Verzeichnis)"
        echo "  • ctmm_build.py (Build-System)"
        echo ""
        exit 1
    fi
    
    # Check if module generator exists
    if [[ ! -f "module-generator.js" ]]; then
        echo -e "${RED}❌ module-generator.js nicht gefunden${NC}"
        echo -e "${YELLOW}💡 Der JavaScript Module Generator ist erforderlich${NC}"
        exit 1
    fi
    
    # Check if Python and CTMM build system are available
    if ! command -v python3 &> /dev/null; then
        echo -e "${YELLOW}⚠️  Python3 nicht gefunden - Build-System wird nicht verfügbar sein${NC}"
    elif [[ ! -f "ctmm_build.py" ]]; then
        echo -e "${YELLOW}⚠️  CTMM Build System nicht gefunden${NC}"
    fi
    
    echo -e "${GREEN}✅ Grundvoraussetzungen erfüllt${NC}"
    echo ""
}

# Show quick start menu
show_quick_start() {
    echo -e "${PURPLE}🚀 Schnellstart-Optionen:${NC}"
    echo ""
    echo "1) 📋 Arbeitsblatt erstellen (Worksheet)"
    echo "   Interaktive Selbstreflexions-Formulare"
    echo ""
    echo "2) 🔧 Therapeutisches Tool erstellen"
    echo "   Bewältigungsstrategien und Techniken"
    echo ""
    echo "3) 🚨 Notfallkarte erstellen"
    echo "   Kriseninterventions-Protokolle"
    echo ""
    echo "4) 📖 Vollständiger interaktiver Modus"
    echo "   Detaillierte Konfiguration mit allen Optionen"
    echo ""
    echo "5) ❓ Hilfe und Dokumentation"
    echo ""
    echo "6) 🏃 Vorhandene Module anzeigen"
    echo ""
    echo "0) 🚪 Beenden"
    echo ""
    echo -n -e "${CYAN}Wähle eine Option (0-6): ${NC}"
}

# Quick create functions for different module types
quick_create_arbeitsblatt() {
    echo -e "${GREEN}📋 Schnell-Erstellung: Arbeitsblatt${NC}"
    echo ""
    echo "Häufige Arbeitsblatt-Typen:"
    echo "1) Täglicher Stimmungscheck"
    echo "2) Trigger-Analyse"
    echo "3) Kommunikations-Reflexion"
    echo "4) Beziehungs-Monitoring"
    echo "5) Individuelles Arbeitsblatt"
    echo ""
    echo -n "Wähle einen Typ (1-5): "
    read -r quick_choice
    
    case $quick_choice in
        1)
            create_mood_check_worksheet
            ;;
        2)
            create_trigger_analysis_worksheet
            ;;
        3)
            create_communication_worksheet
            ;;
        4)
            create_relationship_worksheet
            ;;
        5)
            echo -e "${YELLOW}Starte interaktiven Modus für individuelles Arbeitsblatt...${NC}"
            node module-generator.js
            ;;
        *)
            echo -e "${RED}Ungültige Auswahl${NC}"
            return 1
            ;;
    esac
}

quick_create_tool() {
    echo -e "${GREEN}🔧 Schnell-Erstellung: Tool${NC}"
    echo ""
    echo "Häufige Tool-Typen:"
    echo "1) 5-4-3-2-1 Grounding Technique"
    echo "2) Atemtechnik für Krisenmomente"
    echo "3) Kommunikations-Tool für Paare"
    echo "4) Trigger-Management Tool"
    echo "5) Individuelles Tool"
    echo ""
    echo -n "Wähle einen Typ (1-5): "
    read -r quick_choice
    
    case $quick_choice in
        1)
            create_grounding_tool
            ;;
        2)
            create_breathing_tool
            ;;
        3)
            create_communication_tool
            ;;
        4)
            create_trigger_tool
            ;;
        5)
            echo -e "${YELLOW}Starte interaktiven Modus für individuelles Tool...${NC}"
            node module-generator.js
            ;;
        *)
            echo -e "${RED}Ungültige Auswahl${NC}"
            return 1
            ;;
    esac
}

quick_create_notfallkarte() {
    echo -e "${GREEN}🚨 Schnell-Erstellung: Notfallkarte${NC}"
    echo ""
    echo "Häufige Notfallkarte-Typen:"
    echo "1) Panikattacken-Protokoll"
    echo "2) Dissoziations-Notfallkarte"
    echo "3) Suizidale Gedanken - Hilfe"
    echo "4) Partner-Krise Support"
    echo "5) Individuelle Notfallkarte"
    echo ""
    echo -n "Wähle einen Typ (1-5): "
    read -r quick_choice
    
    case $quick_choice in
        1)
            create_panic_emergency_card
            ;;
        2)
            create_dissociation_card
            ;;
        3)
            create_suicidal_thoughts_card
            ;;
        4)
            create_partner_crisis_card
            ;;
        5)
            echo -e "${YELLOW}Starte interaktiven Modus für individuelle Notfallkarte...${NC}"
            node module-generator.js
            ;;
        *)
            echo -e "${RED}Ungültige Auswahl${NC}"
            return 1
            ;;
    esac
}

# Pre-configured module creation functions
create_mood_check_worksheet() {
    echo -e "${YELLOW}Erstelle Täglicher Stimmungscheck Arbeitsblatt...${NC}"
    
    # Create the file directly with predefined content
    cat > "modules/arbeitsblatt-taeglicher-stimmungscheck.tex" << 'EOF'
% CTMM Arbeitsblatt: Täglicher Stimmungscheck
% Generiert am: $(date '+%d.%m.%Y')
% CTMM Methodology: Catch-Track-Map-Match
% 
% Dieses Arbeitsblatt unterstützt die strukturierte Selbstreflexion
% im Rahmen der CTMM-Therapiemethodik für neurodiverse Paare.

\section{Täglicher Stimmungscheck}

\begin{ctmmBlueBox}{Arbeitsblatt-Übersicht}
\textbf{Zweck:} Regelmäßige Erfassung und Reflexion der täglichen emotionalen Verfassung

\textbf{CTMM-Phase:} Track - Systematische Dokumentation emotionaler Muster

\textbf{Zielgruppe:} Neurodiverse Einzelpersonen und Paare

\textbf{Bearbeitungszeit:} 5-10 Minuten täglich
\end{ctmmBlueBox}

\subsection{Anleitung}

Nimm dir jeden Tag zur gleichen Zeit (idealerweise morgens und/oder abends) einige Minuten Zeit für diese Reflexion. 
Ehrlichkeit ist wichtiger als Perfektion - dokumentiere deine tatsächlichen Gefühle, nicht die erwünschten.

\subsection{Reflexionsfragen}

\begin{enumerate}
\item Wie würde ich meine heutige Grundstimmung beschreiben? (1-10 Skala)
\item Welche Emotionen waren heute besonders präsent?
\item Gab es heute Situationen, die meine Stimmung stark beeinflusst haben?
\item Wie gut konnte ich heute mit schwierigen Gefühlen umgehen?
\item Was hat mir heute geholfen, mich besser zu fühlen?
\end{enumerate}

\subsection{Interaktive Elemente}

\begin{tabular}{|p{0.7\textwidth}|p{0.25\textwidth}|}
\hline
\textbf{Bewertungskriterium} & \textbf{Selbsteinschätzung} \\
\hline
Allgemeine Stimmung (1-10) & \ctmmTextField[3cm]{Stimmung}{grundstimmung} \\
\hline
Energielevel (1-10) & \ctmmTextField[3cm]{Energie}{energielevel} \\
\hline
Stresslevel (1-10) & \ctmmTextField[3cm]{Stress}{stresslevel} \\
\hline
Beziehungsqualität (1-10) & \ctmmTextField[3cm]{Beziehung}{beziehung} \\
\hline
\end{tabular}

\subsection{Tracking und Dokumentation}

\textbf{Datum:} \ctmmTextField[4cm]{Datum}{datum}

\textbf{Uhrzeit:} \ctmmTextField[3cm]{Uhrzeit}{uhrzeit}

\textbf{Dominante Emotion heute:} \ctmmTextField[6cm]{Emotion}{emotion}

\textbf{Trigger oder besondere Ereignisse:}

\ctmmTextArea[\textwidth]{3}{Ereignisse}{ereignisse}

\textbf{Bewältigungsstrategien verwendet:}

\ctmmCheckBox[strategie1]{Atemtechniken angewendet}
\ctmmCheckBox[strategie2]{Partner kontaktiert}
\ctmmCheckBox[strategie3]{Auszeit genommen}
\ctmmCheckBox[strategie4]{Körperliche Aktivität}
\ctmmCheckBox[strategie5]{Andere: } \ctmmTextField[6cm]{Andere Strategie}{andere_strategie}

\subsection{Nächste Schritte}

\begin{ctmmGreenBox}{Handlungsplan}
\ctmmCheckBox[schritt1]{Muster in der Stimmung erkannt}

\ctmmCheckBox[schritt2]{Bewältigungsstrategie für morgen gewählt}

\ctmmCheckBox[schritt3]{Bei Bedarf Unterstützung organisiert}

\textbf{Priorität für morgen:} \ctmmTextField[\textwidth]{Priorität}{prioritaet}
\end{ctmmGreenBox}

\textcolor{ctmmGray}{\small Dieses Arbeitsblatt ist Teil der CTMM-Therapiematerialien und unterstützt die Catch-Track-Map-Match Methodik für neurodiverse Paare.}
EOF

    echo -e "${GREEN}✅ Arbeitsblatt 'Täglicher Stimmungscheck' erstellt!${NC}"
    echo -e "${CYAN}📁 Datei: modules/arbeitsblatt-taeglicher-stimmungscheck.tex${NC}"
}

create_grounding_tool() {
    echo -e "${YELLOW}Erstelle 5-4-3-2-1 Grounding Tool...${NC}"
    
    cat > "modules/tool-5-4-3-2-1-grounding.tex" << 'EOF'
% CTMM Tool: 5-4-3-2-1 Grounding Technique
% Generiert am: $(date '+%d.%m.%Y')
% Therapeutic Tool für CTMM Methodology
% 
% Dieses Tool bietet strukturierte Techniken zur Bewältigung
% spezifischer Herausforderungen im Rahmen der CTMM-Therapie.

\section{5-4-3-2-1 Grounding Technique}

\begin{ctmmOrangeBox}{Tool-Übersicht}
\textbf{Anwendungsbereich:} Akute Angst, Panikattacken, Dissoziation, Überforderung

\textbf{CTMM-Phase:} Catch - Frühzeitige Erkennung und Intervention bei Krisenmomenten

\textbf{Schwierigkeitsgrad:} Einfach - für alle Altersstufen und Kompetenzniveaus geeignet

\textbf{Benötigte Zeit:} 3-5 Minuten
\end{ctmmOrangeBox}

\subsection{Wann wird dieses Tool angewendet?}

Diese Technik hilft bei:
\begin{itemize}
\item Akuten Angstzuständen oder Panikattacken
\item Gefühlen der Dissoziation oder "Nicht-da-sein"
\item Überwältigung durch intensive Emotionen
\item Hypervigilanz oder übermäßiger Wachsamkeit
\item Flashbacks oder traumatischen Erinnerungen
\item Allgemeiner Unruhe und Stress
\end{itemize}

\subsection{Schritt-für-Schritt Anleitung}

\begin{enumerate}
\item \textbf{5 Dinge SEHEN:} Schaue dich um und benenne bewusst 5 Dinge, die du sehen kannst. Beschreibe sie in Gedanken (Farbe, Form, Größe).

\item \textbf{4 Dinge HÖREN:} Höre bewusst hin und identifiziere 4 verschiedene Geräusche um dich herum (Verkehr, Stimmen, Musik, Naturgeräusche).

\item \textbf{3 Dinge BERÜHREN:} Berühre 3 verschiedene Oberflächen oder Gegenstände. Konzentriere dich auf die Textur, Temperatur und Beschaffenheit.

\item \textbf{2 Dinge RIECHEN:} Identifiziere 2 verschiedene Gerüche in deiner Umgebung oder rieche bewusst an etwas (Parfüm, Essen, frische Luft).

\item \textbf{1 Ding SCHMECKEN:} Konzentriere dich auf einen Geschmack in deinem Mund oder nimm bewusst etwas zu dir (Kaugummi, Wasser, Bonbon).
\end{enumerate}

\subsection{Beispiel-Anwendung}

\begin{ctmmGrayBox}{Praxis-Beispiel}
\textbf{Situation:} Sarah spürt eine Panikattacke aufkommen während eines Termins.

\textbf{Anwendung:}
\begin{itemize}
\item \textbf{5 sehen:} "Ich sehe die blaue Wand, den schwarzen Computer, meine roten Schuhe, das grüne Buch, die weiße Tasse."
\item \textbf{4 hören:} "Ich höre Stimmen im Flur, das Summen des Computers, Verkehr draußen, meine eigene Atmung."
\item \textbf{3 berühren:} "Ich berühre die glatte Tischoberfläche, den weichen Stuhlbezug, meine warme Handfläche."
\item \textbf{2 riechen:} "Ich rieche Kaffee und das Papier der Dokumente."
\item \textbf{1 schmecken:} "Ich schmecke den Pfefferminzgeschmack meines Kaugummis."
\end{itemize}

\textbf{Ergebnis:} Sarah fühlt sich wieder geerdet und kann den Termin fortsetzen.
\end{ctmmGrayBox}

\subsection{Anpassungen für neurodiverse Paare}

\begin{itemize}
\item \textbf{ADHS:} Verwende eine verkürzte 3-2-1 Version bei Konzentrationsschwierigkeiten
\item \textbf{Autismus:} Erlaube vertraute Objekte als Grounding-Anker (Stimming-Toys, vertraute Texturen)
\item \textbf{Gemeinsame Anwendung:} Partner können sich gegenseitig durch die Schritte führen
\item \textbf{Nonverbal:} Bei nonverbalen Momenten reicht es, die Sinne stumm zu aktivieren
\end{itemize}

\subsection{Erfolgsindikatoren}

\begin{itemize}
\item Verlangsamung der Atmung und des Herzschlags
\item Reduzierte körperliche Anspannung
\item Klarerer, fokussierterer Geisteszustand
\item Stärkeres Gefühl der Verbindung zum "Hier und Jetzt"
\item Abnahme dissoziative Symptome
\item Erhöhte Handlungsfähigkeit
\end{itemize}

\subsection{Troubleshooting}

\textbf{Was tun, wenn das Tool nicht funktioniert?}

\begin{itemize}
\item \textbf{Zu überwältigt:} Beginne nur mit einer Sinneswahrnehmung und steigere langsam
\item \textbf{Keine Verbesserung:} Kombiniere mit langsamer, bewusster Atmung
\item \textbf{Ablenkung schwierig:} Sage die Wahrnehmungen laut aus oder schreibe sie auf
\item \textbf{Panik verstärkt sich:} Suche sofort professionelle Hilfe oder kontaktiere eine Vertrauensperson
\end{itemize}

\subsection{Integration in den Alltag}

\begin{ctmmGreenBox}{Praktische Umsetzung}
\ctmmCheckBox[integration1]{Tool in Krisenplan integriert}

\ctmmCheckBox[integration2]{Partner über Tool informiert und geschult}

\ctmmCheckBox[integration3]{Tägliche Übung (auch ohne Krise) geplant}

\textbf{Erinnerungshilfe:} \ctmmTextField[\textwidth]{Handy-Notiz, Kärtchen, etc.}{reminder_system}
\end{ctmmGreenBox}

\textcolor{ctmmGray}{\small Dieses Tool ist Teil der CTMM-Therapiematerialien und unterstützt die Catch-Track-Map-Match Methodik für neurodiverse Paare.}
EOF

    echo -e "${GREEN}✅ Tool '5-4-3-2-1 Grounding Technique' erstellt!${NC}"
    echo -e "${CYAN}📁 Datei: modules/tool-5-4-3-2-1-grounding.tex${NC}"
}

create_panic_emergency_card() {
    echo -e "${YELLOW}Erstelle Panikattacken Notfallkarte...${NC}"
    
    cat > "modules/notfall-panikattacken.tex" << 'EOF'
% CTMM Notfallkarte: Panikattacken-Protokoll
% Generiert am: $(date '+%d.%m.%Y')
% Emergency Protocol für CTMM Crisis Intervention
% 
% Diese Notfallkarte bietet sofortige Unterstützung in Krisensituationen
% und folgt den CTMM-Prinzipien für neurodiverse Paare.

\section{Notfallkarte: Panikattacken}

\begin{ctmmRedBox}{\faExclamationTriangle\space Notfall-Information}
\textbf{Krisentyp:} Akute Panikattacke - intensive Angst mit körperlichen Symptomen

\textbf{Dringlichkeit:} Hoch - sofortige Intervention erforderlich

\textbf{Zielgruppe:} Betroffene und unterstützende Partner
\end{ctmmRedBox}

\subsection{Sofortige Maßnahmen}

\begin{ctmmYellowBox}{\faHandStopO\space STOPP - Erste Hilfe}
\textbf{1. STOPP:} Stoppe alle Aktivitäten. Setze oder lege dich hin. Du bist sicher.

\textbf{2. ATMEN:} 4 Sekunden einatmen, 4 Sekunden halten, 6 Sekunden ausatmen. Wiederholen.

\textbf{3. SICHERHEIT:} Erinnere dich: "Das ist eine Panikattacke. Sie ist vorübergehend. Ich bin nicht in Gefahr."
\end{ctmmYellowBox}

\subsection{5-Schritt Notfall-Protokoll}

\begin{enumerate}
\item \textbf{CATCH:} Erkenne die Panikattacke frühzeitig: Herzrasen, Schwitzen, Atemnot, Schwindel, Übelkeit, Angst vor Kontrollverlust.

\item \textbf{TRACK:} Dokumentiere mental oder später schriftlich: Wo bin ich? Was ist passiert? Welche Symptome treten auf?

\item \textbf{MAP:} Verstehe den Zusammenhang: Ist dies ein bekannter Trigger? Welche Stressoren waren heute präsent?

\item \textbf{MATCH:} Wähle passende Bewältigungsstrategie: 5-4-3-2-1 Grounding, Atemtechnik, sicherer Ort, Unterstützung rufen.

\item \textbf{FOLLOW-UP:} Nach der Attacke: Ruhe, Selbstfürsorge, Partner informieren, bei Bedarf professionelle Hilfe kontaktieren.
\end{enumerate}

\subsection{Beruhigungstechniken}

\begin{itemize}
\item \textbf{Bauchatmung:} Hand auf Brust, Hand auf Bauch. Nur die untere Hand soll sich bewegen.
\item \textbf{5-4-3-2-1 Grounding:} 5 Dinge sehen, 4 hören, 3 berühren, 2 riechen, 1 schmecken.
\item \textbf{Positive Affirmationen:} "Das geht vorüber", "Ich bin sicher", "Ich habe das schon geschafft".
\item \textbf{Körperliche Techniken:} Kaltes Wasser ins Gesicht, Eiswürfel halten, feste Umarmung.
\item \textbf{Ablenkung:} Rückwärts von 100 in 7er-Schritten zählen, Gegenstände im Raum benennen.
\end{itemize}

\subsection{Kontakt-Informationen}

\begin{ctmmBlueBox}{Wichtige Kontakte}
\textbf{Therapeut/in:} \ctmmTextField[6cm]{Therapeut}{therapeut}

\textbf{Partner/Vertrauensperson:} \ctmmTextField[6cm]{Vertrauensperson}{partner}

\textbf{Krisentelefon:} \ctmmTextField[6cm]{0800 111 0 111 (kostenlos)}{krisentelefon}

\textbf{Notfall (112):} \textcolor{ctmmRed}{\textbf{112}} - bei Herzinfarkt-Verdacht!
\end{ctmmBlueBox}

\subsection{Für Partner und Unterstützende}

\begin{ctmmPurpleBox}{Partner-Hilfe}
\textbf{DO:}
\begin{itemize}
\item Ruhig und unterstützend bleiben
\item Fragen: "Wie kann ich dir helfen?"
\item Bei Atemtechniken anleiten
\item Physischen Kontakt anbieten (wenn gewünscht)
\item Im Hier und Jetzt halten: "Du bist bei mir, du bist sicher"
\end{itemize}

\textbf{DON'T:}
\begin{itemize}
\item Nicht sagen: "Beruhige dich" oder "Das ist nicht schlimm"
\item Nicht minimalisieren oder rationalisieren
\item Nicht ungeduldig werden
\item Nicht eigene Angst zeigen
\end{itemize}
\end{ctmmPurpleBox}

\subsection{Nachsorge-Checkliste}

\begin{ctmmGreenBox}{Nach der Panikattacke}
\ctmmCheckBox[nachsorge1]{Attacke ist vorüber - körperliche Sicherheit bestätigt}

\ctmmCheckBox[nachsorge2]{Partner/Vertrauensperson kontaktiert und informiert}

\ctmmCheckBox[nachsorge3]{Ausreichend Ruhe und Erholung eingeplant}

\ctmmCheckBox[nachsorge4]{Trigger-Analyse für Therapie dokumentiert}

\ctmmCheckBox[nachsorge5]{Bei häufigen Attacken: Therapeut/in kontaktiert}

\textbf{Erkenntnisse aus dieser Attacke:} \ctmmTextField[\textwidth]{Was hat geholfen/nicht geholfen?}{erkenntnisse}

\textbf{Nächster Therapie-Termin:} \ctmmTextField[4cm]{Datum}{naechster_termin}
\end{ctmmGreenBox}

\textcolor{ctmmRed}{\small \textbf{Wichtig:} Bei Verdacht auf Herzinfarkt (Brustschmerzen, Atemnot, Übelkeit, Schmerzen im linken Arm) sofort 112 wählen!}

\textcolor{ctmmGray}{\small Diese Notfallkarte ist Teil der CTMM-Therapiematerialien und folgt der Catch-Track-Map-Match Methodik für neurodiverse Paare.}
EOF

    echo -e "${GREEN}✅ Notfallkarte 'Panikattacken-Protokoll' erstellt!${NC}"
    echo -e "${CYAN}📁 Datei: modules/notfall-panikattacken.tex${NC}"
}

# Show existing modules
show_existing_modules() {
    echo -e "${BLUE}📚 Vorhandene Module im CTMM-System:${NC}"
    echo ""
    
    if [[ -d "modules" ]]; then
        echo -e "${YELLOW}Arbeitsblätter (Worksheets):${NC}"
        find modules -name "arbeitsblatt-*.tex" -exec basename {} \; | sed 's/^/  • /' | sed 's/.tex$//'
        echo ""
        
        echo -e "${YELLOW}Tools (Therapeutic Techniques):${NC}"
        find modules -name "tool-*.tex" -exec basename {} \; | sed 's/^/  • /' | sed 's/.tex$//'
        echo ""
        
        echo -e "${YELLOW}Notfallkarten (Emergency Cards):${NC}"
        find modules -name "notfall*.tex" -exec basename {} \; | sed 's/^/  • /' | sed 's/.tex$//'
        echo ""
        
        echo -e "${YELLOW}Andere Module:${NC}"
        find modules -name "*.tex" ! -name "arbeitsblatt-*" ! -name "tool-*" ! -name "notfall*" -exec basename {} \; | sed 's/^/  • /' | sed 's/.tex$//'
        echo ""
        
        echo -e "${CYAN}Gesamt: $(find modules -name "*.tex" | wc -l) Module${NC}"
    else
        echo -e "${RED}❌ Module-Verzeichnis nicht gefunden${NC}"
    fi
    echo ""
}

# Show help and documentation
show_help() {
    echo -e "${BLUE}📖 CTMM Module Creator - Hilfe${NC}"
    echo ""
    echo -e "${YELLOW}Über CTMM:${NC}"
    echo "CTMM steht für Catch-Track-Map-Match - eine strukturierte"
    echo "Therapiemethodik für neurodiverse Paare mit Fokus auf:"
    echo "  • Früherkennung (Catch) von Triggern und Mustern"
    echo "  • Systematische Dokumentation (Track) von Verhalten"
    echo "  • Mustererkennung (Map) und Zusammenhänge verstehen"
    echo "  • Angepasste Interventionen (Match) entwickeln"
    echo ""
    echo -e "${YELLOW}Modul-Typen:${NC}"
    echo "  📋 Arbeitsblätter: Interaktive Selbstreflexions-Formulare"
    echo "  🔧 Tools: Therapeutische Techniken und Bewältigungsstrategien"
    echo "  🚨 Notfallkarten: Kriseninterventions-Protokolle"
    echo ""
    echo -e "${YELLOW}Nach der Erstellung:${NC}"
    echo "  1. Inhalte in der generierten .tex-Datei vervollständigen"
    echo "  2. CTMM Build System ausführen: python3 ctmm_build.py"
    echo "  3. PDF testen und bei Bedarf anpassen"
    echo "  4. TODO-Datei löschen wenn fertig"
    echo ""
    echo -e "${YELLOW}Technische Anforderungen:${NC}"
    echo "  • Node.js (für den Module Generator)"
    echo "  • Python3 (für das Build System)"
    echo "  • LaTeX (für PDF-Generierung)"
    echo ""
}

# Test CTMM build system
test_build_system() {
    echo -e "${YELLOW}🔧 Teste CTMM Build System...${NC}"
    
    if [[ -f "ctmm_build.py" ]] && command -v python3 &> /dev/null; then
        if python3 ctmm_build.py; then
            echo -e "${GREEN}✅ CTMM Build System funktioniert korrekt${NC}"
        else
            echo -e "${RED}❌ CTMM Build System meldet Probleme${NC}"
            echo -e "${YELLOW}💡 Prüfe die Log-Ausgabe auf Details${NC}"
        fi
    else
        echo -e "${YELLOW}⚠️  CTMM Build System nicht verfügbar${NC}"
        echo "Überprüfe:"
        echo "  • Python3 installiert: $(command -v python3 >/dev/null && echo "✓" || echo "✗")"
        echo "  • ctmm_build.py vorhanden: $([[ -f "ctmm_build.py" ]] && echo "✓" || echo "✗")"
    fi
}

# Main execution loop
main() {
    print_header
    check_prerequisites
    
    while true; do
        show_quick_start
        read -r choice
        echo ""
        
        case $choice in
            1)
                quick_create_arbeitsblatt
                echo ""
                echo -e "${GREEN}✨ Möchtest du das Build System testen? (y/n)${NC}"
                read -r test_build
                if [[ $test_build == "y" || $test_build == "Y" ]]; then
                    test_build_system
                fi
                echo ""
                ;;
            2)
                quick_create_tool
                echo ""
                echo -e "${GREEN}✨ Möchtest du das Build System testen? (y/n)${NC}"
                read -r test_build
                if [[ $test_build == "y" || $test_build == "Y" ]]; then
                    test_build_system
                fi
                echo ""
                ;;
            3)
                quick_create_notfallkarte
                echo ""
                echo -e "${GREEN}✨ Möchtest du das Build System testen? (y/n)${NC}"
                read -r test_build
                if [[ $test_build == "y" || $test_build == "Y" ]]; then
                    test_build_system
                fi
                echo ""
                ;;
            4)
                echo -e "${YELLOW}Starte vollständigen interaktiven Modus...${NC}"
                node module-generator.js
                echo ""
                ;;
            5)
                show_help
                echo ""
                ;;
            6)
                show_existing_modules
                echo ""
                ;;
            0)
                echo -e "${GREEN}👋 Auf Wiedersehen! Viel Erfolg mit den CTMM-Therapiematerialien!${NC}"
                exit 0
                ;;
            *)
                echo -e "${RED}❌ Ungültige Auswahl. Bitte wähle 0-6.${NC}"
                echo ""
                ;;
        esac
    done
}

# Placeholder functions for remaining quick-create options
create_trigger_analysis_worksheet() {
    echo -e "${YELLOW}ℹ️  Trigger-Analyse Arbeitsblatt wird erstellt...${NC}"
    echo -e "${CYAN}Verwende interaktiven Modus für detailliertere Konfiguration.${NC}"
    node module-generator.js
}

create_communication_worksheet() {
    echo -e "${YELLOW}ℹ️  Kommunikations-Reflexion Arbeitsblatt wird erstellt...${NC}"
    echo -e "${CYAN}Verwende interaktiven Modus für detailliertere Konfiguration.${NC}"
    node module-generator.js
}

create_relationship_worksheet() {
    echo -e "${YELLOW}ℹ️  Beziehungs-Monitoring Arbeitsblatt wird erstellt...${NC}"
    echo -e "${CYAN}Verwende interaktiven Modus für detailliertere Konfiguration.${NC}"
    node module-generator.js
}

create_breathing_tool() {
    echo -e "${YELLOW}ℹ️  Atemtechnik Tool wird erstellt...${NC}"
    echo -e "${CYAN}Verwende interaktiven Modus für detailliertere Konfiguration.${NC}"
    node module-generator.js
}

create_communication_tool() {
    echo -e "${YELLOW}ℹ️  Kommunikations-Tool wird erstellt...${NC}"
    echo -e "${CYAN}Verwende interaktiven Modus für detailliertere Konfiguration.${NC}"
    node module-generator.js
}

create_trigger_tool() {
    echo -e "${YELLOW}ℹ️  Trigger-Management Tool wird erstellt...${NC}"
    echo -e "${CYAN}Verwende interaktiven Modus für detailliertere Konfiguration.${NC}"
    node module-generator.js
}

create_dissociation_card() {
    echo -e "${YELLOW}ℹ️  Dissoziations-Notfallkarte wird erstellt...${NC}"
    echo -e "${CYAN}Verwende interaktiven Modus für detailliertere Konfiguration.${NC}"
    node module-generator.js
}

create_suicidal_thoughts_card() {
    echo -e "${YELLOW}ℹ️  Suizidale Gedanken Hilfe-Karte wird erstellt...${NC}"
    echo -e "${CYAN}Verwende interaktiven Modus für detailliertere Konfiguration.${NC}"
    node module-generator.js
}

create_partner_crisis_card() {
    echo -e "${YELLOW}ℹ️  Partner-Krise Support Karte wird erstellt...${NC}"
    echo -e "${CYAN}Verwende interaktiven Modus für detailliertere Konfiguration.${NC}"
    node module-generator.js
}

# Handle command line arguments
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    # Check for help argument
    if [[ "$1" == "--help" || "$1" == "-h" ]]; then
        show_help
        exit 0
    fi
    
    # Check for existing modules argument
    if [[ "$1" == "--list" || "$1" == "-l" ]]; then
        show_existing_modules
        exit 0
    fi
    
    # Start main interactive session
    main
fi