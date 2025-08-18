#!/bin/bash
# CTMM Module Creation Shell Script
# Interactive wrapper for the CTMM Module Generator
# Provides simplified workflow for creating therapeutic modules

# CTMM Color codes for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
ORANGE='\033[0;33m'
PURPLE='\033[0;35m'
GRAY='\033[0;37m'
NC='\033[0m' # No Color

# CTMM banner
echo -e "${BLUE}════════════════════════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}                            CTMM Module Generator                               ${NC}"
echo -e "${BLUE}        Catch-Track-Map-Match Therapeutic Materials Creation System            ${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════════════════════${NC}"
echo ""

# Check if Node.js is available
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Error: Node.js is not installed or not in PATH${NC}"
    echo -e "${ORANGE}💡 Please install Node.js to use the CTMM Module Generator${NC}"
    echo -e "${GRAY}   You can download it from: https://nodejs.org/${NC}"
    exit 1
fi

# Check if module-generator.js exists
if [[ ! -f "module-generator.js" ]]; then
    echo -e "${RED}❌ Error: module-generator.js not found${NC}"
    echo -e "${ORANGE}💡 Please ensure you're running this script from the CTMM project root${NC}"
    exit 1
fi

# Function to show help
show_help() {
    echo -e "${GREEN}🎯 CTMM Module Creation Tool${NC}"
    echo ""
    echo -e "${BLUE}Usage:${NC}"
    echo "  $0 [OPTIONS]"
    echo ""
    echo -e "${BLUE}Options:${NC}"
    echo "  -h, --help          Show this help message"
    echo "  -i, --interactive   Start interactive module creation (default)"
    echo "  -l, --list          List existing modules"
    echo "  -v, --validate      Validate CTMM build system"
    echo "  -q, --quick <type> <title> <filename>  Quick module creation"
    echo ""
    echo -e "${BLUE}Module Types:${NC}"
    echo "  arbeitsblatt        Therapeutic worksheet for couples"
    echo "  tool               Therapeutic tool for immediate application"
    echo "  notfallkarte       Emergency intervention card"
    echo ""
    echo -e "${BLUE}Examples:${NC}"
    echo "  $0                  # Interactive mode"
    echo "  $0 --list           # Show existing modules"
    echo "  $0 --quick tool \"Atemtechnik\" \"atemtechnik.tex\""
    echo ""
    echo -e "${GRAY}For more information, see MODULE-GENERATOR-README.md${NC}"
}

# Function to list existing modules
list_modules() {
    echo -e "${GREEN}📁 Existing CTMM Modules:${NC}"
    echo ""
    
    if [[ -d "modules" ]]; then
        local count=0
        for file in modules/*.tex; do
            if [[ -f "$file" ]]; then
                local basename=$(basename "$file" .tex)
                local title=$(grep -m1 "\\\\section{" "$file" 2>/dev/null | sed 's/.*{//; s/}.*//' | head -1)
                if [[ -z "$title" ]]; then
                    title="(No title found)"
                fi
                echo -e "  ${BLUE}•${NC} ${basename}.tex - ${title}"
                ((count++))
            fi
        done
        
        if [[ $count -eq 0 ]]; then
            echo -e "  ${GRAY}No modules found in modules/ directory${NC}"
        else
            echo ""
            echo -e "${GREEN}Total: $count modules${NC}"
        fi
    else
        echo -e "  ${RED}modules/ directory not found${NC}"
    fi
}

# Function to validate build system
validate_build() {
    echo -e "${GREEN}🔧 Validating CTMM Build System...${NC}"
    echo ""
    
    # Check for Python
    if command -v python3 &> /dev/null; then
        echo -e "${GREEN}✅ Python 3 found${NC}"
        
        # Check for ctmm_build.py
        if [[ -f "ctmm_build.py" ]]; then
            echo -e "${GREEN}✅ CTMM build system found${NC}"
            
            # Run build validation
            echo -e "${BLUE}Running build validation...${NC}"
            python3 ctmm_build.py
            
            if [[ $? -eq 0 ]]; then
                echo -e "${GREEN}✅ Build system validation passed${NC}"
            else
                echo -e "${ORANGE}⚠️  Build system validation had warnings${NC}"
            fi
        else
            echo -e "${RED}❌ ctmm_build.py not found${NC}"
        fi
    else
        echo -e "${RED}❌ Python 3 not found${NC}"
    fi
    
    # Check for LaTeX
    if command -v pdflatex &> /dev/null; then
        echo -e "${GREEN}✅ LaTeX (pdflatex) found${NC}"
    else
        echo -e "${ORANGE}⚠️  LaTeX not found (optional for development)${NC}"
    fi
}

# Function to run quick module creation
quick_create() {
    local type="$1"
    local title="$2"
    local filename="$3"
    local description="$4"
    
    if [[ -z "$type" || -z "$title" || -z "$filename" ]]; then
        echo -e "${RED}❌ Error: Missing required parameters for quick creation${NC}"
        echo -e "${ORANGE}Usage: $0 --quick <type> <title> <filename> [description]${NC}"
        exit 1
    fi
    
    # Validate module type
    case "$type" in
        arbeitsblatt|tool|notfallkarte)
            echo -e "${GREEN}Creating ${type} module: ${title}${NC}"
            ;;
        *)
            echo -e "${RED}❌ Error: Invalid module type '${type}'${NC}"
            echo -e "${ORANGE}Valid types: arbeitsblatt, tool, notfallkarte${NC}"
            exit 1
            ;;
    esac
    
    # Add .tex extension if not present
    if [[ "$filename" != *.tex ]]; then
        filename="${filename}.tex"
    fi
    
    # Check if file already exists
    if [[ -f "modules/$filename" ]]; then
        echo -e "${ORANGE}⚠️  Warning: File modules/$filename already exists${NC}"
        read -p "Overwrite? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo -e "${GRAY}Operation cancelled${NC}"
            exit 0
        fi
    fi
    
    # Create module
    node module-generator.js "$type" "$title" "$filename" "$description"
    
    if [[ $? -eq 0 ]]; then
        echo ""
        echo -e "${GREEN}✅ Module created successfully!${NC}"
        echo -e "${BLUE}📋 Next steps:${NC}"
        echo -e "  1. Add to main.tex: ${GRAY}\\\\input{modules/${filename%.tex}}${NC}"
        echo -e "  2. Run build system: ${GRAY}python3 ctmm_build.py${NC}"
        echo -e "  3. Test module: ${GRAY}make build${NC}"
    else
        echo -e "${RED}❌ Module creation failed${NC}"
        exit 1
    fi
}

# Function to show interactive menu
interactive_mode() {
    echo -e "${GREEN}🎯 Interactive Module Creation${NC}"
    echo ""
    echo -e "${BLUE}What would you like to do?${NC}"
    echo "  1. Create new module"
    echo "  2. List existing modules"
    echo "  3. Validate build system"
    echo "  4. Show help"
    echo "  5. Exit"
    echo ""
    
    read -p "Choose option (1-5): " choice
    
    case $choice in
        1)
            echo ""
            echo -e "${GREEN}Starting module creation...${NC}"
            node module-generator.js
            ;;
        2)
            echo ""
            list_modules
            echo ""
            read -p "Press Enter to continue..."
            interactive_mode
            ;;
        3)
            echo ""
            validate_build
            echo ""
            read -p "Press Enter to continue..."
            interactive_mode
            ;;
        4)
            echo ""
            show_help
            echo ""
            read -p "Press Enter to continue..."
            interactive_mode
            ;;
        5)
            echo -e "${GRAY}Goodbye!${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}Invalid option. Please choose 1-5.${NC}"
            sleep 1
            interactive_mode
            ;;
    esac
}

# Parse command line arguments
case "${1:-}" in
    -h|--help)
        show_help
        ;;
    -l|--list)
        list_modules
        ;;
    -v|--validate)
        validate_build
        ;;
    -q|--quick)
        shift
        quick_create "$@"
        ;;
    -i|--interactive|"")
        interactive_mode
        ;;
    *)
        echo -e "${RED}❌ Unknown option: $1${NC}"
        echo -e "${ORANGE}Use '$0 --help' for usage information${NC}"
        exit 1
        ;;
esac