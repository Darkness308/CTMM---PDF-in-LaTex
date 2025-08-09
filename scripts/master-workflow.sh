#!/bin/bash
#
# CTMM Master Workflow Script
# Comprehensive document processing and LaTeX build workflow
# Fixes the over-escaping issue mentioned in PR #3
#

set -e  # Exit on any error

# Script configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
LOG_FILE="$PROJECT_ROOT/workflow.log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

log_info() {
    log "${BLUE}INFO${NC}: $1"
}

log_success() {
    log "${GREEN}SUCCESS${NC}: $1"
}

log_warning() {
    log "${YELLOW}WARNING${NC}: $1"
}

log_error() {
    log "${RED}ERROR${NC}: $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to fix LaTeX escaping issues
fix_latex_escaping() {
    log_info "Fixing LaTeX over-escaping issues..."
    cd "$PROJECT_ROOT"
    
    if [[ -f "scripts/fix_latex_escaping.py" ]]; then
        python3 scripts/fix_latex_escaping.py
        log_success "LaTeX escaping fix completed"
    else
        log_error "fix_latex_escaping.py not found"
        return 1
    fi
}

# Function to convert documents
convert_documents() {
    log_info "Converting documents to LaTeX..."
    cd "$PROJECT_ROOT"
    
    if command_exists pandoc; then
        if [[ -f "scripts/convert_documents.py" ]]; then
            python3 scripts/convert_documents.py
            log_success "Document conversion completed"
        else
            log_error "convert_documents.py not found"
            return 1
        fi
    else
        log_warning "Pandoc not available, skipping document conversion"
        log_info "To enable document conversion, install pandoc: apt-get install pandoc"
    fi
}

# Function to run build system check
build_system_check() {
    log_info "Running CTMM build system check..."
    cd "$PROJECT_ROOT"
    
    if [[ -f "ctmm_build.py" ]]; then
        python3 ctmm_build.py
        log_success "Build system check completed"
    else
        log_error "ctmm_build.py not found"
        return 1
    fi
}

# Function to build LaTeX PDF
build_pdf() {
    log_info "Building LaTeX PDF..."
    cd "$PROJECT_ROOT"
    
    if command_exists pdflatex; then
        # Multiple passes for proper reference resolution
        pdflatex -interaction=nonstopmode main.tex
        pdflatex -interaction=nonstopmode main.tex
        
        if [[ -f "main.pdf" ]]; then
            local pdf_size=$(stat -c%s "main.pdf" 2>/dev/null || echo "unknown")
            log_success "PDF build completed (size: $pdf_size bytes)"
        else
            log_error "PDF build failed - main.pdf not created"
            return 1
        fi
    else
        log_warning "pdflatex not available, skipping PDF build"
        log_info "To enable PDF building, install LaTeX: apt-get install texlive-latex-extra"
    fi
}

# Function to run analysis
analyze_system() {
    log_info "Running detailed system analysis..."
    cd "$PROJECT_ROOT"
    
    if [[ -f "build_system.py" ]]; then
        python3 build_system.py --verbose
        log_success "System analysis completed"
    else
        log_warning "build_system.py not found, skipping detailed analysis"
    fi
}

# Function to clean build artifacts
clean_artifacts() {
    log_info "Cleaning build artifacts..."
    cd "$PROJECT_ROOT"
    
    # Remove LaTeX temporary files
    rm -f *.aux *.log *.out *.toc
    rm -f main_basic_test.*
    rm -f *.temp.*
    rm -f build_error_*.log
    
    log_success "Build artifacts cleaned"
}

# Function to show usage
show_usage() {
    echo "CTMM Master Workflow Script"
    echo "=========================="
    echo ""
    echo "Usage: $0 [OPTION]"
    echo ""
    echo "Options:"
    echo "  --all         Run complete workflow (recommended)"
    echo "  --fix-escape  Fix LaTeX over-escaping issues only"
    echo "  --convert     Convert documents to LaTeX only"
    echo "  --build       Run build system check only"
    echo "  --pdf         Build PDF only"
    echo "  --analyze     Run detailed analysis only"
    echo "  --clean       Clean build artifacts only"
    echo "  --help        Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 --all                    # Run complete workflow"
    echo "  $0 --fix-escape            # Fix escaping issues"
    echo "  $0 --convert --build --pdf  # Convert, build check, and create PDF"
}

# Main workflow function
run_complete_workflow() {
    log_info "Starting CTMM complete workflow..."
    
    # Step 1: Fix LaTeX escaping issues (this is the main fix for the bug)
    fix_latex_escaping || log_warning "LaTeX escaping fix had issues"
    
    # Step 2: Convert documents (if pandoc available)
    convert_documents || log_warning "Document conversion had issues"
    
    # Step 3: Run build system check
    build_system_check || log_warning "Build system check had issues"
    
    # Step 4: Build PDF (if LaTeX available)
    build_pdf || log_warning "PDF build had issues"
    
    # Step 5: Run analysis
    analyze_system || log_warning "System analysis had issues"
    
    log_success "Complete workflow finished"
}

# Main script logic
main() {
    # Initialize log
    log_info "CTMM Master Workflow started with arguments: $*"
    
    # Parse command line arguments
    case "${1:-}" in
        --all)
            run_complete_workflow
            ;;
        --fix-escape)
            fix_latex_escaping
            ;;
        --convert)
            convert_documents
            ;;
        --build)
            build_system_check
            ;;
        --pdf)
            build_pdf
            ;;
        --analyze)
            analyze_system
            ;;
        --clean)
            clean_artifacts
            ;;
        --help|"")
            show_usage
            ;;
        *)
            log_error "Unknown option: $1"
            show_usage
            exit 1
            ;;
    esac
    
    log_info "CTMM Master Workflow completed"
}

# Run main function with all arguments
main "$@"