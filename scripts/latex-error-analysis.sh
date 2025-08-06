#!/bin/bash
# LaTeX Error Analysis and Debugging Tool for CTMM Project
# Comprehensive error detection, categorization, and solution proposals

set -e

# Configuration
MAIN_FILE="${1:-main.tex}"
BUILD_DIR="build"
ANALYSIS_DIR="$BUILD_DIR/error-analysis"
ERROR_REPORT="$ANALYSIS_DIR/error-analysis-report.txt"
SOLUTION_REPORT="$ANALYSIS_DIR/solution-proposals.txt"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Initialize directories
mkdir -p "$ANALYSIS_DIR"

log_message() {
    echo -e "$1" | tee -a "$ERROR_REPORT"
}

run_extended_compilation() {
    local basename=$(basename "$MAIN_FILE" .tex)
    
    log_message "${BLUE}Running LaTeX compilation with extended error output...${NC}"
    
    # Clean previous artifacts
    rm -f "$BUILD_DIR"/*.aux "$BUILD_DIR"/*.log "$BUILD_DIR"/*.toc "$BUILD_DIR"/*.out
    
    # Run pdflatex with maximum error detail
    pdflatex -output-directory="$BUILD_DIR" \
             -interaction=nonstopmode \
             -file-line-error \
             -recorder \
             "$MAIN_FILE" > "$ANALYSIS_DIR/compilation-output.txt" 2>&1 || true
    
    # Also run with -halt-on-error to get precise error location
    pdflatex -output-directory="$BUILD_DIR" \
             -interaction=nonstopmode \
             -halt-on-error \
             -file-line-error \
             "$MAIN_FILE" > "$ANALYSIS_DIR/halt-on-error-output.txt" 2>&1 || true
    
    log_message "${GREEN}✓ Extended compilation completed${NC}"
}

categorize_errors() {
    local log_file="$BUILD_DIR/$(basename "$MAIN_FILE" .tex).log"
    
    log_message "${BLUE}Categorizing errors...${NC}"
    
    # Initialize error categories
    declare -A error_categories
    error_categories["syntax"]=()
    error_categories["missing_packages"]=()
    error_categories["references"]=()
    error_categories["incompatible_packages"]=()
    error_categories["encoding"]=()
    error_categories["fonts"]=()
    error_categories["other"]=()
    
    # Error patterns
    declare -A error_patterns
    error_patterns["syntax"]="Undefined control sequence|Missing|Extra|Paragraph ended before|File ended while scanning"
    error_patterns["missing_packages"]="LaTeX Error.*package.*not found|Package.*not found|File.*not found"
    error_patterns["references"]="Reference.*undefined|Citation.*undefined|Label.*undefined"
    error_patterns["incompatible_packages"]="Package.*option clash|Package.*conflict|Option clash"
    error_patterns["encoding"]="Package inputenc Error|Unicode char.*not set up|Invalid UTF-8"
    error_patterns["fonts"]="Font.*not found|Font shape.*undefined|LaTeX Font Warning"
    
    if [[ -f "$log_file" ]]; then
        # Process each error line
        while IFS= read -r line; do
            if [[ $line =~ ^! ]]; then
                local error_found=false
                for category in "${!error_patterns[@]}"; do
                    if echo "$line" | grep -qE "${error_patterns[$category]}"; then
                        error_categories[$category]+=("$line")
                        error_found=true
                        break
                    fi
                done
                
                if [[ $error_found == false ]]; then
                    error_categories["other"]+=("$line")
                fi
            fi
        done < "$log_file"
    fi
    
    # Report categorized errors
    {
        echo ""
        echo "ERROR CATEGORIZATION REPORT"
        echo "=========================="
        echo "Analysis Date: $(date)"
        echo ""
    } >> "$ERROR_REPORT"
    
    for category in "${!error_categories[@]}"; do
        local count=${#error_categories[$category][@]}
        if [[ $count -gt 0 ]]; then
            {
                echo "$category errors: $count"
                for error in "${error_categories[$category][@]}"; do
                    echo "  - $error"
                done
                echo ""
            } >> "$ERROR_REPORT"
            
            log_message "${RED}$category: $count errors${NC}"
        fi
    done
}

locate_error_positions() {
    local log_file="$BUILD_DIR/$(basename "$MAIN_FILE" .tex).log"
    
    log_message "${BLUE}Locating exact error positions...${NC}"
    
    {
        echo ""
        echo "ERROR LOCATIONS"
        echo "==============="
        echo ""
    } >> "$ERROR_REPORT"
    
    if [[ -f "$log_file" ]]; then
        # Extract file-line-error format lines
        grep -n "^[^:]*:[0-9]*:" "$log_file" >> "$ERROR_REPORT" 2>/dev/null || true
        
        # Also extract line numbers from context
        awk '/^!/,/^$/' "$log_file" | while read -r line; do
            if [[ $line =~ l\.([0-9]+) ]]; then
                echo "Line ${BASH_REMATCH[1]}: $line" >> "$ERROR_REPORT"
            fi
        done
    fi
}

create_solution_proposals() {
    log_message "${BLUE}Creating solution proposals...${NC}"
    
    {
        echo "SOLUTION PROPOSALS"
        echo "=================="
        echo "Generated: $(date)"
        echo ""
    } > "$SOLUTION_REPORT"
    
    # Common solutions for different error types
    {
        echo "SYNTAX ERRORS:"
        echo "- Check for missing braces {} or brackets []"
        echo "- Verify all \begin{} have matching \end{}"
        echo "- Check for unescaped special characters: & % $ # _ ^ ~ \ { }"
        echo "- Look for typos in command names"
        echo ""
        
        echo "MISSING PACKAGES:"
        echo "- Add missing packages to the preamble with \\usepackage{package-name}"
        echo "- Check if packages are installed on the system"
        echo "- Consider using CTAN to find package documentation"
        echo "- Common missing packages: amsmath, amssymb, graphicx, xcolor, hyperref"
        echo ""
        
        echo "REFERENCE PROBLEMS:"
        echo "- Run pdflatex multiple times to resolve cross-references"
        echo "- Check for typos in \\label{} and \\ref{} commands"
        echo "- Verify labels are defined before they are referenced"
        echo "- Use \\pageref{} for page references"
        echo ""
        
        echo "INCOMPATIBLE PACKAGES:"
        echo "- Check package documentation for known conflicts"
        echo "- Load conflicting packages in the correct order"
        echo "- Use package options to resolve conflicts"
        echo "- Consider alternative packages"
        echo ""
        
        echo "ENCODING ISSUES:"
        echo "- Ensure \\usepackage[utf8]{inputenc} is included"
        echo "- Save files with UTF-8 encoding"
        echo "- Use \\usepackage[T1]{fontenc} for better font encoding"
        echo "- Escape non-ASCII characters or use LaTeX commands"
        echo ""
        
        echo "FONT PROBLEMS:"
        echo "- Install missing fonts on the system"
        echo "- Use \\usepackage{lmodern} for better font support"
        echo "- Check font package documentation"
        echo "- Consider using different font packages"
        echo ""
    } >> "$SOLUTION_REPORT"
    
    log_message "${GREEN}✓ Solution proposals created${NC}"
}

prioritize_errors() {
    local log_file="$BUILD_DIR/$(basename "$MAIN_FILE" .tex).log"
    
    log_message "${BLUE}Prioritizing errors by severity...${NC}"
    
    {
        echo ""
        echo "ERROR PRIORITY ANALYSIS"
        echo "======================"
        echo ""
    } >> "$ERROR_REPORT"
    
    # Define severity levels
    declare -A high_priority
    high_priority["Emergency stop"]="CRITICAL"
    high_priority["Fatal error"]="CRITICAL"
    high_priority["Undefined control sequence"]="HIGH"
    high_priority["Missing"]="HIGH"
    high_priority["Package.*not found"]="HIGH"
    
    declare -A medium_priority
    medium_priority["LaTeX Warning"]="MEDIUM"
    medium_priority["Package.*Warning"]="MEDIUM"
    medium_priority["Reference.*undefined"]="MEDIUM"
    
    declare -A low_priority
    low_priority["Overfull"]="LOW"
    low_priority["Underfull"]="LOW"
    low_priority["Font shape"]="LOW"
    
    if [[ -f "$log_file" ]]; then
        {
            echo "CRITICAL PRIORITY (Fix First):"
            grep -E "Emergency stop|Fatal error" "$log_file" | head -10 || echo "  None found"
            echo ""
            
            echo "HIGH PRIORITY:"
            grep -E "Undefined control sequence|Missing.*{|Package.*not found" "$log_file" | head -10 || echo "  None found"
            echo ""
            
            echo "MEDIUM PRIORITY:"
            grep -E "LaTeX Warning|Package.*Warning|Reference.*undefined" "$log_file" | head -10 || echo "  None found"
            echo ""
            
            echo "LOW PRIORITY:"
            grep -E "Overfull|Underfull|Font shape.*undefined" "$log_file" | head -5 || echo "  None found"
            echo ""
        } >> "$ERROR_REPORT"
    fi
}

create_fix_plan() {
    log_message "${BLUE}Creating step-by-step fix plan...${NC}"
    
    {
        echo ""
        echo "STEP-BY-STEP FIX PLAN"
        echo "===================="
        echo ""
        echo "1. IMMEDIATE ACTIONS (CRITICAL):"
        echo "   - Fix any emergency stops or fatal errors first"
        echo "   - Check main.tex for basic syntax issues"
        echo "   - Verify all required packages are available"
        echo ""
        echo "2. HIGH PRIORITY FIXES:"
        echo "   - Fix undefined control sequences"
        echo "   - Add missing packages to preamble"
        echo "   - Correct major syntax errors"
        echo ""
        echo "3. MEDIUM PRIORITY FIXES:"
        echo "   - Resolve reference warnings"
        echo "   - Fix package warnings"
        echo "   - Address encoding issues"
        echo ""
        echo "4. LOW PRIORITY IMPROVEMENTS:"
        echo "   - Fix overfull/underfull boxes"
        echo "   - Resolve font warnings"
        echo "   - Optimize formatting"
        echo ""
        echo "5. VERIFICATION STEPS:"
        echo "   - Run pdflatex multiple times"
        echo "   - Check PDF output quality"
        echo "   - Verify all content is present"
        echo ""
    } >> "$SOLUTION_REPORT"
    
    log_message "${GREEN}✓ Fix plan created${NC}"
}

generate_analysis_summary() {
    log_message "${BLUE}Generating analysis summary...${NC}"
    
    local log_file="$BUILD_DIR/$(basename "$MAIN_FILE" .tex).log"
    local total_errors=0
    local total_warnings=0
    
    if [[ -f "$log_file" ]]; then
        total_errors=$(grep -c "^!" "$log_file" 2>/dev/null || echo "0")
        total_warnings=$(grep -c "Warning" "$log_file" 2>/dev/null || echo "0")
    fi
    
    {
        echo ""
        echo "ANALYSIS SUMMARY"
        echo "================"
        echo "Analysis completed: $(date)"
        echo "Main file: $MAIN_FILE"
        echo "Total errors found: $total_errors"
        echo "Total warnings found: $total_warnings"
        echo ""
        echo "Generated files:"
        echo "- Error analysis report: $ERROR_REPORT"
        echo "- Solution proposals: $SOLUTION_REPORT"
        echo "- Compilation output: $ANALYSIS_DIR/compilation-output.txt"
        echo ""
    } >> "$ERROR_REPORT"
    
    log_message "${GREEN}Analysis Summary:${NC}"
    log_message "  Total errors: $total_errors"
    log_message "  Total warnings: $total_warnings"
    log_message "  Analysis report: $ERROR_REPORT"
    log_message "  Solution proposals: $SOLUTION_REPORT"
}

main() {
    {
        echo "CTMM LaTeX Error Analysis Report"
        echo "================================"
        echo "Started: $(date)"
        echo "Main file: $MAIN_FILE"
        echo ""
    } > "$ERROR_REPORT"
    
    log_message "${GREEN}Starting LaTeX Error Analysis${NC}"
    
    # Run compilation with extended error output
    run_extended_compilation
    
    # Categorize errors by type
    categorize_errors
    
    # Locate exact error positions
    locate_error_positions
    
    # Prioritize errors by severity
    prioritize_errors
    
    # Create solution proposals
    create_solution_proposals
    
    # Create step-by-step fix plan
    create_fix_plan
    
    # Generate summary
    generate_analysis_summary
    
    log_message "${GREEN}✓ Error analysis completed${NC}"
    log_message "Results available in: $ANALYSIS_DIR"
}

# Run main function
main "$@"