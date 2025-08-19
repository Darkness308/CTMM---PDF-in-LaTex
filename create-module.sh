#!/bin/bash

# CTMM Interactive Module Creator
# Interactive shell script for simplified module creation workflow
# 
# This script provides a user-friendly interface for the CTMM module generator,
# guiding users through the process of creating new therapeutic modules.
#
# Author: CTMM-Team
# Version: 1.0.0

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# CTMM branding
CTMM_LOGO="
${BLUE}   ____  _______  __  __  __  __
  / ___|___| |_ _|  \/  |\/  |
 | |     | |   | || |\/| |\/| |
 | |___  | |   | || |  | |  | |
  \____| |_|  |___|_|  |_|  |_|${NC}
  
${PURPLE}Catch-Track-Map-Match Module Generator${NC}
"

# Function to print colored output
print_header() {
    echo -e "${BLUE}=================================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}=================================================${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Function to check prerequisites
check_prerequisites() {
    print_header "Checking Prerequisites"
    
    # Check if Node.js is available
    if ! command -v node &> /dev/null; then
        print_error "Node.js is not installed or not in PATH"
        echo "Please install Node.js to use this script."
        echo "Visit: https://nodejs.org/"
        exit 1
    fi
    
    # Check if module-generator.js exists
    if [ ! -f "module-generator.js" ]; then
        print_error "module-generator.js not found in current directory"
        echo "Please run this script from the CTMM repository root."
        exit 1
    fi
    
    # Check if modules directory exists, create if not
    if [ ! -d "modules" ]; then
        print_warning "modules directory not found, creating it..."
        mkdir -p modules
        print_success "Created modules directory"
    fi
    
    print_success "All prerequisites met"
    echo
}

# Function to show module type information
show_module_types() {
    echo -e "${PURPLE}📚 CTMM Module Types:${NC}"
    echo
    echo -e "${BLUE}1. arbeitsblatt${NC} - Interactive worksheets for therapy exercises"
    echo "   Examples: Daily mood check, trigger diary, self-reflection"
    echo "   Features: Form fields, reflection questions, progress tracking"
    echo
    echo -e "${BLUE}2. tool${NC} - Techniques and methods for specific situations"
    echo "   Examples: Grounding techniques, breathing exercises, communication skills"
    echo "   Features: Step-by-step instructions, practice areas, effectiveness tracking"
    echo
    echo -e "${BLUE}3. notfallkarte${NC} - Emergency cards with crisis management steps"
    echo "   Examples: Panic attack protocol, safety strategies, emergency contacts"
    echo "   Features: Quick access info, contact lists, immediate action steps"
    echo
}

# Function to get user input for module details
get_module_details() {
    print_header "Module Configuration"
    
    # Show available types
    show_module_types
    
    # Get module type
    while true; do
        echo -e "${YELLOW}What type of module do you want to create?${NC}"
        read -p "Enter type (arbeitsblatt/tool/notfallkarte): " MODULE_TYPE
        
        if [[ "$MODULE_TYPE" =~ ^(arbeitsblatt|tool|notfallkarte)$ ]]; then
            break
        else
            print_error "Invalid module type. Please choose: arbeitsblatt, tool, or notfallkarte"
        fi
    done
    
    # Get module name
    while true; do
        echo
        echo -e "${YELLOW}What should your module be called?${NC}"
        echo "Examples:"
        echo "  arbeitsblatt: taeglicher-stimmungscheck, trigger-analyse, selbstreflexion"
        echo "  tool: 5-4-3-2-1-grounding, atemtechnik, kommunikation"
        echo "  notfallkarte: panikattacken, dissoziative-episoden, selbstverletzung"
        echo
        read -p "Enter module name (use hyphens for spaces): " MODULE_NAME
        
        if [ -z "$MODULE_NAME" ]; then
            print_error "Module name cannot be empty"
            continue
        fi
        
        # Check if module already exists
        MODULE_FILE="modules/${MODULE_TYPE}-${MODULE_NAME}.tex"
        if [ -f "$MODULE_FILE" ]; then
            print_warning "Module $MODULE_FILE already exists"
            read -p "Do you want to overwrite it? (y/N): " OVERWRITE
            if [[ "$OVERWRITE" =~ ^[Yy]$ ]]; then
                break
            else
                continue
            fi
        else
            break
        fi
    done
    
    print_success "Module type: $MODULE_TYPE"
    print_success "Module name: $MODULE_NAME"
    echo
}

# Function to generate the module
generate_module() {
    print_header "Generating Module"
    
    print_info "Running CTMM module generator..."
    
    # Run the Node.js generator
    if node module-generator.js "$MODULE_TYPE" "$MODULE_NAME"; then
        MODULE_FILE="modules/${MODULE_TYPE}-${MODULE_NAME}.tex"
        print_success "Module generated successfully: $MODULE_FILE"
        echo
        
        # Show file size and basic info
        if [ -f "$MODULE_FILE" ]; then
            FILE_SIZE=$(wc -c < "$MODULE_FILE")
            LINE_COUNT=$(wc -l < "$MODULE_FILE")
            print_info "File size: $FILE_SIZE bytes, $LINE_COUNT lines"
        fi
    else
        print_error "Module generation failed"
        exit 1
    fi
}

# Function to validate the generated module
validate_module() {
    print_header "Validating Generated Module"
    
    MODULE_FILE="modules/${MODULE_TYPE}-${MODULE_NAME}.tex"
    
    # Basic LaTeX syntax check
    print_info "Checking LaTeX syntax..."
    
    # Check for balanced braces
    OPEN_BRACES=$(grep -o '{' "$MODULE_FILE" | wc -l)
    CLOSE_BRACES=$(grep -o '}' "$MODULE_FILE" | wc -l)
    
    if [ "$OPEN_BRACES" -eq "$CLOSE_BRACES" ]; then
        print_success "Braces are balanced ($OPEN_BRACES pairs)"
    else
        print_warning "Brace mismatch: $OPEN_BRACES open, $CLOSE_BRACES close"
    fi
    
    # Check for CTMM-specific elements
    print_info "Checking CTMM design elements..."
    
    if grep -q "ctmm.*Box" "$MODULE_FILE"; then
        print_success "CTMM colored boxes found"
    fi
    
    if grep -q "ctmmTextField\|ctmmTextArea\|ctmmCheckBox" "$MODULE_FILE"; then
        print_success "CTMM form elements found"
    fi
    
    if grep -q "textcolor{ctmm" "$MODULE_FILE"; then
        print_success "CTMM color scheme used"
    fi
    
    # Check if it follows CTMM conventions
    if grep -q "addcontentsline{toc}" "$MODULE_FILE"; then
        print_success "Table of contents integration present"
    fi
    
    if grep -q "label{sec:" "$MODULE_FILE"; then
        print_success "Section labels for cross-references present"
    fi
    
    echo
}

# Function to integrate with build system
integrate_with_build_system() {
    print_header "Integration Options"
    
    MODULE_FILE="modules/${MODULE_TYPE}-${MODULE_NAME}.tex"
    INPUT_LINE="\\input{modules/${MODULE_TYPE}-${MODULE_NAME}}"
    
    echo -e "${YELLOW}Integration with CTMM build system:${NC}"
    echo
    echo "To include your new module in the main document:"
    echo "1. Add this line to main.tex:"
    echo -e "   ${GREEN}$INPUT_LINE${NC}"
    echo
    echo "2. Run the CTMM build system:"
    echo -e "   ${GREEN}python3 ctmm_build.py${NC}"
    echo
    
    read -p "Do you want to automatically add the module to main.tex? (y/N): " AUTO_ADD
    
    if [[ "$AUTO_ADD" =~ ^[Yy]$ ]]; then
        if [ -f "main.tex" ]; then
            # Find a good place to insert the module
            # Look for the section where modules are included
            if grep -q "input{modules/" main.tex; then
                print_info "Adding module to main.tex..."
                
                # Create a backup
                cp main.tex main.tex.backup
                
                # Find the last \input{modules/...} line and add after it
                LAST_MODULE_LINE=$(grep -n "input{modules/" main.tex | tail -1 | cut -d: -f1)
                
                if [ -n "$LAST_MODULE_LINE" ]; then
                    # Insert the new line after the last module input
                    sed -i "${LAST_MODULE_LINE}a\\$INPUT_LINE" main.tex
                    print_success "Module added to main.tex after line $LAST_MODULE_LINE"
                    print_info "Backup created: main.tex.backup"
                else
                    print_warning "Could not find module input section in main.tex"
                    print_info "Please add manually: $INPUT_LINE"
                fi
            else
                print_warning "No module inputs found in main.tex"
                print_info "Please add manually: $INPUT_LINE"
            fi
        else
            print_warning "main.tex not found in current directory"
            print_info "Please add manually to your main LaTeX file: $INPUT_LINE"
        fi
    fi
    
    echo
}

# Function to run build system test
run_build_test() {
    print_header "Build System Test"
    
    echo -e "${YELLOW}Do you want to test the module with the CTMM build system?${NC}"
    read -p "This will run 'python3 ctmm_build.py' (y/N): " RUN_TEST
    
    if [[ "$RUN_TEST" =~ ^[Yy]$ ]]; then
        print_info "Running CTMM build system..."
        echo
        
        if python3 ctmm_build.py; then
            print_success "Build system test passed!"
            echo
            print_info "Your module is ready for use in the CTMM system"
        else
            print_warning "Build system reported issues"
            echo "Please check the output above for any problems."
            echo "You may need to review and edit your module."
        fi
    fi
    
    echo
}

# Function to show next steps
show_next_steps() {
    print_header "Next Steps"
    
    MODULE_FILE="modules/${MODULE_TYPE}-${MODULE_NAME}.tex"
    
    echo -e "${PURPLE}🎯 Your CTMM module is ready!${NC}"
    echo
    echo -e "${GREEN}Generated file:${NC} $MODULE_FILE"
    echo
    echo -e "${YELLOW}What you can do now:${NC}"
    echo
    echo "1. 📝 Review and customize the module content:"
    echo "   - Edit therapeutic content for your specific needs"
    echo "   - Adjust form fields and questions"
    echo "   - Modify colors and styling if needed"
    echo
    echo "2. 🔗 Integrate with your CTMM system:"
    echo "   - Add to main.tex if not done automatically"
    echo "   - Run: python3 ctmm_build.py"
    echo "   - Generate PDF: make build (if LaTeX is installed)"
    echo
    echo "3. 📖 Documentation and examples:"
    echo "   - Check existing modules in modules/ for patterns"
    echo "   - See MODULE-GENERATOR-README.md for detailed docs"
    echo "   - Follow CTMM design guidelines"
    echo
    echo "4. 🧪 Testing and validation:"
    echo "   - Test form functionality in PDF"
    echo "   - Validate therapeutic content with professionals"
    echo "   - Gather feedback from users"
    echo
    echo -e "${BLUE}🔄 To create another module, run this script again!${NC}"
    echo
}

# Main function
main() {
    # Clear screen and show logo
    clear
    echo -e "$CTMM_LOGO"
    echo
    
    # Run the workflow
    check_prerequisites
    get_module_details
    generate_module
    validate_module
    integrate_with_build_system
    run_build_test
    show_next_steps
    
    print_success "Module creation workflow completed!"
}

# Help function
show_help() {
    echo "CTMM Interactive Module Creator v1.0.0"
    echo
    echo "Usage:"
    echo "  ./create-module.sh              - Run interactive module creation"
    echo "  ./create-module.sh --help       - Show this help message"
    echo "  ./create-module.sh --types      - Show available module types"
    echo "  ./create-module.sh --validate   - Validate existing modules"
    echo
    echo "This script provides an interactive interface for creating CTMM therapeutic modules."
    echo "It guides you through the process of generating LaTeX modules that follow"
    echo "CTMM design patterns and therapeutic best practices."
    echo
    echo "Prerequisites:"
    echo "  - Node.js (for running the module generator)"
    echo "  - CTMM repository (with module-generator.js)"
    echo "  - Optional: Python 3 and LaTeX for build testing"
    echo
}

# Parse command line arguments
case "${1:-}" in
    --help|-h)
        show_help
        exit 0
        ;;
    --types|-t)
        show_module_types
        exit 0
        ;;
    --validate|-v)
        print_header "Validating Existing Modules"
        if [ -d "modules" ] && [ "$(ls -A modules/*.tex 2>/dev/null)" ]; then
            for module in modules/*.tex; do
                echo "Checking $module..."
                # Basic validation logic here
            done
        else
            print_info "No modules found to validate"
        fi
        exit 0
        ;;
    "")
        # No arguments - run interactive mode
        main
        ;;
    *)
        print_error "Unknown argument: $1"
        echo "Use --help for usage information"
        exit 1
        ;;
esac