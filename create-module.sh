#!/bin/bash

# CTMM Module Creator - Interactive Shell Script
# Simplified interface for creating therapy modules

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "${BLUE}🏥 CTMM Module Creator${NC}"
echo -e "${BLUE}=====================${NC}"
echo ""

# Check if Node.js is available
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js ist nicht installiert.${NC}"
    echo "Installieren Sie Node.js um den JavaScript-Generator zu verwenden."
    echo "Fallback: Erstelle einfaches Template..."
    
    # Fallback: Create simple template without JavaScript
    read -p "Modulname (ohne .tex): " MODULE_NAME
    read -p "Modultitel: " MODULE_TITLE
    
    MODULE_FILE="modules/${MODULE_NAME}.tex"
    
    # Create modules directory if it doesn't exist
    mkdir -p modules
    
    cat > "$MODULE_FILE" << EOF
% ${MODULE_TITLE}
% CTMM Modul - Manuell erstellt

\\section{${MODULE_TITLE}}

\\begin{ctmmBlueBox}{${MODULE_TITLE}}
    Beschreibung des Moduls hier eingeben.
\\end{ctmmBlueBox}

\\subsection{Inhalt}

Hier den Inhalt des Moduls einfügen.

\\subsection{Interaktive Elemente}

\\ctmmCheckBox[checkbox1]{Beispiel Checkbox}

\\ctmmTextField[8cm]{Textfeld Beispiel}{textfield1}

\\ctmmTextArea[15cm]{3}{Notizen}{notes}

\\vfill
\\begin{center}
    \\textcolor{ctmmGray}{\\small Erstellt mit CTMM Module Creator}
\\end{center}
EOF
    
    echo -e "${GREEN}✅ Einfaches Template erstellt: ${MODULE_FILE}${NC}"
    exit 0
fi

# Check if module-generator.js exists
if [ ! -f "${SCRIPT_DIR}/module-generator.js" ]; then
    echo -e "${RED}❌ module-generator.js nicht gefunden.${NC}"
    echo "Stellen Sie sicher, dass sich das Skript im selben Verzeichnis befindet."
    exit 1
fi

# Function to show menu
show_menu() {
    echo -e "${YELLOW}Wählen Sie eine Option:${NC}"
    echo "1) 📝 Arbeitsblatt erstellen"
    echo "2) 🔧 Therapeutisches Tool erstellen"  
    echo "3) 🆘 Notfallkarte erstellen"
    echo "4) 🎯 Interaktiver Modus (alle Felder ausfüllen)"
    echo "5) ❓ Hilfe anzeigen"
    echo "6) 🚪 Beenden"
    echo ""
}

# Function to create quick template
create_quick_template() {
    local type=$1
    local default_name=$2
    
    read -p "Dateiname (ohne .tex) [${default_name}]: " filename
    filename=${filename:-$default_name}
    
    read -p "Titel des Moduls: " title
    
    echo -e "${BLUE}Erstelle ${type} Modul...${NC}"
    
    if node "${SCRIPT_DIR}/module-generator.js" "$type" "$filename" 2>/dev/null; then
        echo -e "${GREEN}✅ ${type^} erfolgreich erstellt: modules/${filename}.tex${NC}"
        
        # Offer to add to main.tex
        read -p "Soll das Modul zu main.tex hinzugefügt werden? (j/N): " add_to_main
        if [[ $add_to_main =~ ^[jJ]$ ]]; then
            add_to_main_tex "$filename"
        fi
        
        # Offer to run build system
        read -p "Soll das Build-System getestet werden? (j/N): " test_build
        if [[ $test_build =~ ^[jJ]$ ]]; then
            echo -e "${BLUE}Führe Build-System Test aus...${NC}"
            if python3 ctmm_build.py; then
                echo -e "${GREEN}✅ Build-System Test erfolgreich${NC}"
            else
                echo -e "${RED}❌ Build-System Test fehlgeschlagen${NC}"
            fi
        fi
    else
        echo -e "${RED}❌ Fehler beim Erstellen des Moduls${NC}"
    fi
}

# Function to add module reference to main.tex
add_to_main_tex() {
    local module_name=$1
    local main_file="main.tex"
    
    if [ ! -f "$main_file" ]; then
        echo -e "${RED}❌ main.tex nicht gefunden${NC}"
        return 1
    fi
    
    # Check if module is already referenced
    if grep -q "\\input{modules/${module_name}}" "$main_file"; then
        echo -e "${YELLOW}⚠️  Modul ist bereits in main.tex referenziert${NC}"
        return 0
    fi
    
    # Create backup
    cp "$main_file" "${main_file}.backup"
    
    # Find the last \input{modules/...} line and add after it
    if grep -q "\\input{modules/" "$main_file"; then
        # Add after the last module input
        sed -i "/\\\\input{modules\//a\\\\input{modules/${module_name}}" "$main_file"
    else
        # Add before \end{document}
        sed -i "/\\\\end{document}/i\\\\input{modules/${module_name}}" "$main_file"
    fi
    
    echo -e "${GREEN}✅ Modul zu main.tex hinzugefügt${NC}"
}

# Function to run interactive mode
run_interactive_mode() {
    echo -e "${BLUE}Starte interaktiven Modus...${NC}"
    echo "Sie werden durch alle Schritte geführt."
    echo ""
    
    node "${SCRIPT_DIR}/module-generator.js"
}

# Function to show help
show_help() {
    echo -e "${BLUE}🏥 CTMM Module Creator - Hilfe${NC}"
    echo ""
    echo "Dieses Skript hilft beim Erstellen von CTMM Therapie-Modulen:"
    echo ""
    echo -e "${YELLOW}📝 Arbeitsblatt:${NC} Therapeutische Arbeitsblätter mit Reflexionsfragen"
    echo -e "${YELLOW}🔧 Tool:${NC} Therapeutische Techniken und Übungen"
    echo -e "${YELLOW}🆘 Notfallkarte:${NC} Krisenhilfe und Sofortmaßnahmen"
    echo ""
    echo "Generierte Module werden im 'modules/' Verzeichnis erstellt."
    echo "Vergessen Sie nicht, das Modul in main.tex zu referenzieren!"
    echo ""
    echo -e "${BLUE}Dateien:${NC}"
    echo "• module-generator.js - JavaScript Generator"
    echo "• create-module.sh - Dieses Shell-Skript"
    echo ""
}

# Main menu loop
while true; do
    show_menu
    read -p "Ihre Wahl [1-6]: " choice
    echo ""
    
    case $choice in
        1)
            create_quick_template "arbeitsblatt" "arbeitsblatt-$(date +%Y%m%d)"
            ;;
        2)
            create_quick_template "tool" "tool-$(date +%Y%m%d)"
            ;;
        3)
            create_quick_template "notfallkarte" "notfall-$(date +%Y%m%d)"
            ;;
        4)
            run_interactive_mode
            ;;
        5)
            show_help
            ;;
        6)
            echo -e "${GREEN}Auf Wiedersehen! 👋${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}❌ Ungültige Auswahl. Bitte wählen Sie 1-6.${NC}"
            ;;
    esac
    
    echo ""
    read -p "Drücken Sie Enter um fortzufahren..."
    echo ""
done