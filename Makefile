# CTMM LaTeX Build System Makefile

.PHONY: build check clean test test-unit validate-pr help unit-test validate validate-fix ctmm-check ctmm-fix ctmm-validate ctmm-workflow integration-test comprehensive workflow enhanced-build enhanced-testing test-workflow

# Default target
all: ctmm-check build

# Enhanced build management targets
enhanced-build:
	@echo "Running enhanced CTMM build management..."
	python3 ctmm_build.py --enhanced

enhanced-testing:
	@echo "Running enhanced incremental testing..."
	python3 -c "from build_system import enhanced_incremental_testing; enhanced_incremental_testing()"

# Advanced automation targets
automated-workflow:
	@echo "Running complete automated workflow..."
	@echo "Step 1: Enhanced build management"
	@make enhanced-build
	@echo "Step 2: Enhanced incremental testing"
	@make enhanced-testing
	@echo "Step 3: Comprehensive validation"
	@make comprehensive
	@echo "✅ Complete automated workflow finished successfully"

# Missing file detection and template generation
detect-missing:
	@echo "Detecting missing files and generating templates..."
	python3 -c "from ctmm_build import scan_references, check_missing_files, create_template; import sys; refs = scan_references(); missing = check_missing_files(refs['style_files'] + refs['module_files']); [create_template(f) for f in missing]; print(f'Generated {len(missing)} templates') if missing else print('No missing files found')"

# Template cleanup (removes TODO files for completed work)
cleanup-templates:
	@echo "Cleaning up completed template TODO files..."
	@find . -name "TODO_*.md" -exec sh -c 'echo "Remove $$1? (y/N):" && read ans && test "$$ans" = "y" && rm "$$1"' _ {} \;

# Comprehensive error analysis
error-analysis:
	@echo "Running comprehensive error analysis..."
	python3 build_system.py --verbose > error_analysis.log 2>&1 || true
	@echo "Error analysis saved to error_analysis.log"
	@grep -E "(ERROR|FAIL|WARNING)" error_analysis.log || echo "No errors found in analysis"

# Check build system and dependencies
check:
	@echo "Running CTMM Build System check..."
	python3 ctmm_build.py

# Validate PR content (for contributors)
validate-pr:
	@echo "Validating PR content for Copilot review..."
	python3 validate_pr.py

# Validate LaTeX files for escaping issues
validate:
	@echo "Validating LaTeX files for escaping issues..."
	python3 latex_validator.py modules/

# Fix LaTeX escaping issues (creates backups)
validate-fix:
	@echo "Fixing LaTeX escaping issues..."
	python3 latex_validator.py modules/ --fix

# CTMM Unified Tool Commands
ctmm-check:
	@echo "Running CTMM unified build check..."
	python3 ctmm_unified_tool.py build

ctmm-fix:
	@echo "Fixing over-escaped LaTeX files..."
	python3 ctmm_unified_tool.py de-escape --converted converted/ --backup

ctmm-validate:
	@echo "Validating complete CTMM project..."
	python3 ctmm_unified_tool.py validate

ctmm-workflow:
	@echo "Running complete CTMM workflow..."
	python3 ctmm_unified_tool.py workflow --converted converted/

# Integration testing
integration-test:
	@echo "Running CTMM integration test suite..."
	python3 test_integration.py

# Build PDF
build:
	@echo "Building CTMM PDF..."
	pdflatex -interaction=nonstopmode main.tex
	pdflatex -interaction=nonstopmode main.tex  # Second pass for references

# Full analysis (detailed module testing)
analyze:
	@echo "Running detailed build analysis..."
	python3 build_system.py --verbose

# Test only (without building)
test:
	@echo "Testing build system..."
	python3 ctmm_build.py | grep -E "(PASS|FAIL|ERROR|WARNING)" || true
	@echo "Running unit tests..."
	python3 test_ctmm_build.py

# Run only unit tests
test-unit:
	@echo "Running unit tests for ctmm_build.py..."
	python3 test_ctmm_build.py

# Run unit tests
unit-test:
	@echo "Running unit tests..."
	python3 test_ctmm_build.py
	python3 test_latex_validator.py

# Clean build artifacts
clean:
	rm -f *.aux *.log *.out *.toc *.pdf
	rm -f main_basic_test.*
	rm -f *.temp.*
	rm -f build_error_*.log
	rm -f __pycache__/*.pyc
	@echo "Cleaned build artifacts"

# Install dependencies (for local development)
deps:
	@echo "Installing Python dependencies..."
	pip install chardet
	@echo "LaTeX packages should be installed via your system package manager"

# Comprehensive workflow
comprehensive:
	@echo "Running CTMM Comprehensive Workflow..."
	python3 comprehensive_workflow.py

# Comprehensive workflow (alias)
workflow:
	@echo "Running CTMM Comprehensive Workflow..."
	python3 comprehensive_workflow.py

# Test CI robustness (Issue #1044 fix)
test-ci-robustness:
	@echo "Testing CI pipeline robustness (Issue #1044)..."
	python3 test_issue_1044_ci_robustness.py

test-comprehensive-timeout:
	@echo "Testing comprehensive CI timeout coverage..."
	python3 test_comprehensive_ci_timeout_coverage.py

# Test automated PR merge workflow
test-workflow:
	@echo "Testing Automated PR Merge and Build Workflow..."
	python3 test_automated_pr_workflow.py

# Help
help:
	@echo "CTMM LaTeX Build System - Enhanced Automated Build Management"
	@echo "============================================================="
	@echo ""
	@echo "🚀 ENHANCED AUTOMATION TARGETS:"
	@echo "  enhanced-build     - Run enhanced CTMM build management with sophisticated error detection"
	@echo "  enhanced-testing   - Run enhanced incremental testing with module isolation"
	@echo "  automated-workflow - Complete automated workflow (build + testing + validation)"
	@echo "  detect-missing     - Detect missing files and generate enhanced templates"
	@echo "  cleanup-templates  - Clean up completed template TODO files"
	@echo "  error-analysis     - Run comprehensive error analysis and categorization"
	@echo ""
	@echo "📋 STANDARD BUILD TARGETS:"
	@echo "  all                - Run check and build (default)"
	@echo "  check              - Check dependencies and run build system"
	@echo "  build              - Build the PDF with LaTeX"
	@echo "  analyze            - Run detailed module analysis"
	@echo "  test               - Quick test of build system + unit tests"
	@echo "  test-unit          - Run only unit tests for ctmm_build.py"
	@echo "  unit-test          - Run unit tests for Python functions"
	@echo ""
	@echo "🔧 VALIDATION AND QUALITY:"
	@echo "  validate-pr        - Validate PR content for Copilot review"
	@echo "  validate           - Validate LaTeX files for escaping issues"
	@echo "  validate-fix       - Fix LaTeX escaping issues (creates backups)"
	@echo "  comprehensive      - Run complete workflow validation"
	@echo "  workflow           - Alias for comprehensive"
	@echo ""
	@echo "🧪 TESTING AND CI/CD:"
	@echo "  test-ci-robustness - Test CI pipeline robustness (Issue #1044)"
	@echo "  test-comprehensive-timeout - Test comprehensive CI timeout coverage"
	@echo "  test-workflow      - Test automated PR merge workflow"
	@echo "  integration-test   - Run CTMM integration test suite"
	@echo ""
	@echo "🛠️  CTMM UNIFIED TOOL COMMANDS:"
	@echo "  ctmm-check         - Run unified build system validation"
	@echo "  ctmm-fix           - Fix over-escaped LaTeX files"
	@echo "  ctmm-validate      - Complete project validation"
	@echo "  ctmm-workflow      - Run complete integration workflow"
	@echo ""
	@echo "🧹 MAINTENANCE:"
	@echo "  clean              - Remove build artifacts"
	@echo "  deps               - Install Python dependencies"
	@echo ""
	@echo "💡 QUICK START:"
	@echo "   make automated-workflow  # Complete automated build and testing"
	@echo "   make enhanced-build      # Enhanced build management only"
	@echo "   make help               # Show this help"
	@echo "  ctmm-fix      - Fix over-escaped LaTeX files"
	@echo "  ctmm-validate - Complete project validation"
	@echo "  ctmm-workflow - Run complete integration workflow"
	@echo "  integration-test - Run comprehensive integration tests"
	@echo ""
	@echo "  help          - Show this help"
