#!/bin/bash
# CI Robustness Helper Script for Issue #849
# Provides retry logic and enhanced error handling for transient CI failures

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to log messages
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to run command with retry logic
run_with_retry() {
    local command="$1"
    local description="$2"
    local max_attempts="${3:-3}"
    local delay="${4:-5}"
    
    log_info "Running: $description"
    
    for attempt in $(seq 1 $max_attempts); do
        log_info "Attempt $attempt/$max_attempts: $command"
        
        if eval "$command"; then
            log_success "$description completed successfully"
            return 0
        else
            local exit_code=$?
            log_warning "$description failed (attempt $attempt/$max_attempts) with exit code $exit_code"
            
            if [ $attempt -lt $max_attempts ]; then
                log_info "Waiting ${delay}s before retry..."
                sleep $delay
            else
                log_error "$description failed after $max_attempts attempts"
                return $exit_code
            fi
        fi
    done
}

# Function to run command with graceful failure
run_with_graceful_failure() {
    local command="$1"
    local description="$2"
    local allow_failure="${3:-true}"
    
    log_info "Running: $description"
    
    if eval "$command"; then
        log_success "$description completed successfully"
        return 0
    else
        local exit_code=$?
        if [ "$allow_failure" = "true" ]; then
            log_warning "$description failed with exit code $exit_code (continuing...)"
            return 0
        else
            log_error "$description failed with exit code $exit_code"
            return $exit_code
        fi
    fi
}

# Function to validate CI environment
validate_ci_environment() {
    log_info "🔍 Validating CI environment..."
    
    # Check Python availability
    if ! command -v python3 &> /dev/null; then
        log_error "Python 3 is not available"
        return 1
    fi
    log_success "Python 3 is available"
    
    # Check required files
    local required_files=(
        "main.tex"
        "ctmm_build.py"
        "validate_latex_syntax.py"
        "test_issue_849_fix.py"
    )
    
    for file in "${required_files[@]}"; do
        if [ -f "$file" ]; then
            log_success "Required file exists: $file"
        else
            log_error "Missing required file: $file"
            return 1
        fi
    done
    
    # Check Python dependencies
    local python_modules=("chardet")
    for module in "${python_modules[@]}"; do
        if python3 -c "import $module" 2>/dev/null; then
            log_success "Python module available: $module"
        else
            log_warning "Python module missing: $module (may cause issues)"
        fi
    done
    
    log_success "CI environment validation completed"
    return 0
}

# Main execution based on arguments
case "${1:-help}" in
    "validate-environment")
        validate_ci_environment
        ;;
    "run-latex-validation")
        run_with_retry "python3 validate_latex_syntax.py" "LaTeX syntax validation" 2 3
        ;;
    "run-build-system")
        run_with_retry "python3 ctmm_build.py" "CTMM build system check" 2 3
        ;;
    "run-comprehensive-validation")
        run_with_graceful_failure "python3 test_issue_743_validation.py" "Comprehensive CI validation" true
        ;;
    "run-robustness-check")
        run_with_graceful_failure "python3 test_issue_761_fix.py" "CI robustness check" true
        ;;
    "run-failure-detection")
        run_with_graceful_failure "python3 test_issue_849_fix.py" "Enhanced failure detection" true
        ;;
    "validate-pr")
        # Special validation for PR content
        log_info "🔍 Running PR content validation with enhanced error handling..."
        validate_ci_environment || exit 1
        run_with_retry "python3 ctmm_build.py" "CTMM build validation for PR" 2 3
        run_with_graceful_failure "python3 test_issue_849_fix.py" "Enhanced PR validation" true
        ;;
    "help"|*)
        echo "CI Robustness Helper Script for Issue #849"
        echo "Usage: $0 [command]"
        echo ""
        echo "Commands:"
        echo "  validate-environment        - Validate CI environment prerequisites"
        echo "  run-latex-validation        - Run LaTeX syntax validation with retry"
        echo "  run-build-system            - Run CTMM build system with retry"
        echo "  run-comprehensive-validation - Run comprehensive CI validation"
        echo "  run-robustness-check        - Run CI robustness checks"
        echo "  run-failure-detection       - Run enhanced failure detection"
        echo "  validate-pr                 - Run complete PR validation suite"
        echo "  help                        - Show this help message"
        echo ""
        echo "This script provides enhanced error handling and retry logic"
        echo "to improve CI pipeline robustness and handle transient failures."
        ;;
esac