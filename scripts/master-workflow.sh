#!/bin/bash
# Master Workflow Script for CTMM LaTeX Project
# Orchestrates all build, conversion, analysis, and optimization workflows

set -e

# Configuration
SCRIPTS_DIR="scripts"
BUILD_DIR="build"
REPORTS_DIR="$BUILD_DIR/reports"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Initialize directories
mkdir -p "$REPORTS_DIR"

log_message() {
    echo -e "$1"
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$REPORTS_DIR/master-workflow.log"
}

show_help() {
    cat << EOF
CTMM LaTeX Master Workflow

Usage: $0 [OPTION]

Options:
    --build             Run enhanced LaTeX build only
    --convert          Run document conversion only
    --analyze          Run error analysis only
    --optimize         Run optimization analysis only
    --all              Run all workflows (default)
    --help             Show this help message

Workflows:
    1. LaTeX Build      - pdflatex + BibTeX + multiple passes
    2. Document Convert - Convert .txt, .md, .docx to LaTeX
    3. Error Analysis   - Comprehensive error detection & solutions
    4. Optimization     - Code quality and efficiency analysis

Examples:
    $0 --all           Run complete workflow
    $0 --build         Build PDF only
    $0 --convert       Convert documents only
EOF
}

make_executable() {
    local script="$1"
    if [[ -f "$script" ]]; then
        chmod +x "$script"
        log_message "Made executable: $script"
    fi
}

prepare_scripts() {
    log_message "${BLUE}Preparing scripts...${NC}"

    # Make all scripts executable
    make_executable "$SCRIPTS_DIR/latex-build.sh"
    make_executable "$SCRIPTS_DIR/document-conversion.sh"
    make_executable "$SCRIPTS_DIR/latex-error-analysis.sh"
    make_executable "$SCRIPTS_DIR/pdf-quality-optimization.sh"

    log_message "${GREEN}✓ Scripts prepared${NC}"
}

run_latex_build() {
    log_message "${PURPLE}=== Running LaTeX Build Workflow ===${NC}"

    if [[ -f "$SCRIPTS_DIR/latex-build.sh" ]]; then
        if ./"$SCRIPTS_DIR/latex-build.sh"; then
            log_message "${GREEN}✓ LaTeX build completed successfully${NC}"
            return 0
        else
            log_message "${RED}✗ LaTeX build failed${NC}"
            return 1
        fi
    else
        log_message "${RED}✗ LaTeX build script not found${NC}"
        return 1
    fi
}

run_document_conversion() {
    log_message "${PURPLE}=== Running Document Conversion Workflow ===${NC}"

    if [[ -f "$SCRIPTS_DIR/document-conversion.sh" ]]; then
        if ./"$SCRIPTS_DIR/document-conversion.sh"; then
            log_message "${GREEN}✓ Document conversion completed successfully${NC}"
            return 0
        else
            log_message "${YELLOW}⚠ Document conversion completed with issues${NC}"
            return 1
        fi
    else
        log_message "${RED}✗ Document conversion script not found${NC}"
        return 1
    fi
}

run_error_analysis() {
    log_message "${PURPLE}=== Running LaTeX Error Analysis Workflow ===${NC}"

    if [[ -f "$SCRIPTS_DIR/latex-error-analysis.sh" ]]; then
        if ./"$SCRIPTS_DIR/latex-error-analysis.sh"; then
            log_message "${GREEN}✓ Error analysis completed successfully${NC}"
            return 0
        else
            log_message "${YELLOW}⚠ Error analysis completed (errors found)${NC}"
            return 1
        fi
    else
        log_message "${RED}✗ Error analysis script not found${NC}"
        return 1
    fi
}

run_optimization() {
    log_message "${PURPLE}=== Running PDF Quality Optimization Workflow ===${NC}"

    if [[ -f "$SCRIPTS_DIR/pdf-quality-optimization.sh" ]]; then
        if ./"$SCRIPTS_DIR/pdf-quality-optimization.sh"; then
            log_message "${GREEN}✓ Optimization analysis completed successfully${NC}"
            return 0
        else
            log_message "${YELLOW}⚠ Optimization analysis completed with recommendations${NC}"
            return 1
        fi
    else
        log_message "${RED}✗ Optimization script not found${NC}"
        return 1
    fi
}

generate_master_report() {
    local master_report="$REPORTS_DIR/master-workflow-summary.txt"

    log_message "${BLUE}Generating master workflow report...${NC}"

    {
        echo "CTMM LaTeX Master Workflow Summary"
        echo "================================="
        echo "Completed: $(date)"
        echo ""
        echo "Workflow Status:"
        echo "---------------"

        # Check if each workflow completed successfully
        if [[ -f "build/build-log.txt" ]]; then
            if grep -q "Build completed successfully" "build/build-log.txt" 2>/dev/null; then
                echo "✓ LaTeX Build: SUCCESS"
            else
                echo "✗ LaTeX Build: FAILED"
            fi
        else
            echo "- LaTeX Build: NOT RUN"
        fi

        if [[ -f "build/conversion-log.txt" ]]; then
            echo "✓ Document Conversion: COMPLETED"
        else
            echo "- Document Conversion: NOT RUN"
        fi

        if [[ -f "build/error-analysis/error-analysis-report.txt" ]]; then
            echo "✓ Error Analysis: COMPLETED"
        else
            echo "- Error Analysis: NOT RUN"
        fi

        if [[ -f "build/optimization/optimization-report.txt" ]]; then
            echo "✓ Optimization Analysis: COMPLETED"
        else
            echo "- Optimization Analysis: NOT RUN"
        fi

        echo ""
        echo "Generated Files:"
        echo "---------------"

        # List important output files
        [[ -f "main.pdf" ]] && echo "✓ main.pdf - Final PDF output"
        [[ -f "build/build-log.txt" ]] && echo "✓ build/build-log.txt - Build log"
        [[ -f "build/error-summary.txt" ]] && echo "✓ build/error-summary.txt - Error summary"
        [[ -f "build/warning-summary.txt" ]] && echo "✓ build/warning-summary.txt - Warning summary"
        [[ -f "build/conversion-log.txt" ]] && echo "✓ build/conversion-log.txt - Conversion log"
        [[ -f "converted/integrated-content.tex" ]] && echo "✓ converted/integrated-content.tex - Integrated converted content"
        [[ -f "build/error-analysis/error-analysis-report.txt" ]] && echo "✓ build/error-analysis/error-analysis-report.txt - Error analysis"
        [[ -f "build/error-analysis/solution-proposals.txt" ]] && echo "✓ build/error-analysis/solution-proposals.txt - Solution proposals"
        [[ -f "build/optimization/optimization-report.txt" ]] && echo "✓ build/optimization/optimization-report.txt - Optimization analysis"

        echo ""
        echo "Quick Access:"
        echo "------------"
        echo "Main PDF: main.pdf"
        echo "All logs: build/"
        echo "Converted documents: converted/"
        echo "Analysis reports: build/error-analysis/ and build/optimization/"
        echo ""

    } > "$master_report"

    log_message "${GREEN}✓ Master report generated: $master_report${NC}"
}

run_all_workflows() {
    log_message "${GREEN}Starting CTMM Complete Workflow${NC}"

    local workflow_errors=0

    # Prepare scripts
    prepare_scripts

    # Run document conversion first (if there are documents to convert)
    if ! run_document_conversion; then
        log_message "${YELLOW}Document conversion had issues but continuing...${NC}"
        ((workflow_errors++))
    fi

    # Run error analysis before build to identify existing issues
    if ! run_error_analysis; then
        log_message "${YELLOW}Error analysis found issues but continuing...${NC}"
        ((workflow_errors++))
    fi

    # Run main build
    if ! run_latex_build; then
        log_message "${YELLOW}LaTeX build had issues but continuing...${NC}"
        ((workflow_errors++))
    fi

    # Run optimization analysis
    if ! run_optimization; then
        log_message "${YELLOW}Optimization analysis had recommendations but continuing...${NC}"
        ((workflow_errors++))
    fi

    # Generate master report
    generate_master_report

    if [[ $workflow_errors -eq 0 ]]; then
        log_message "${GREEN}✓ All workflows completed successfully${NC}"
    else
        log_message "${YELLOW}⚠ Workflows completed with $workflow_errors issues/recommendations${NC}"
    fi

    log_message "${BLUE}Master workflow completed. Check $REPORTS_DIR/master-workflow-summary.txt for details.${NC}"

    return 0  # Return 0 so workflow continues
}

main() {
    # Initialize master log
    echo "CTMM Master Workflow Log - $(date)" > "$REPORTS_DIR/master-workflow.log"
    echo "=================================" >> "$REPORTS_DIR/master-workflow.log"

    case "${1:-}" in
        --build)
            prepare_scripts
            run_latex_build
            ;;
        --convert)
            prepare_scripts
            run_document_conversion
            ;;
        --analyze)
            prepare_scripts
            run_error_analysis
            ;;
        --optimize)
            prepare_scripts
            run_optimization
            ;;
        --all|"")
            run_all_workflows
            ;;
        --help|-h)
            show_help
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"
