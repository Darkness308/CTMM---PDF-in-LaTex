# CTMM LaTeX Build System Makefile

.PHONY: build check clean test test-unit validate-pr help unit-test validate validate-fix ctmm-check ctmm-fix ctmm-validate ctmm-workflow integration-test comprehensive workflow enhanced-build enhanced-testing test-workflow setup

# Default target
all: ctmm-check build

# Enhanced build management targets
enhanced-build:
	@echo "Running enhanced CTMM build management..."
	python3 ctmm_build.py --enhanced

enhanced-testing:
	@echo "Running enhanced incremental testing..."
	python3 -c "from build_system import enhanced_incremental_testing; enhanced_incremental_testing()"

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
	@echo ""
	@echo "LaTeX dependencies required:"
	@echo "  sudo apt-get install -y texlive-latex-base texlive-latex-extra texlive-fonts-recommended texlive-lang-german texlive-fonts-extra"
	@echo ""
	@echo "For complete installation: sudo apt-get install -y texlive-full"
	@echo "See BUILD_TROUBLESHOOTING.md for detailed setup instructions"

# Full setup (install all dependencies)
setup:
	@echo "Setting up CTMM build environment..."
	@echo "Installing Python dependencies..."
	pip install chardet
	@echo ""
	@echo "Installing LaTeX dependencies (requires sudo)..."
	sudo apt-get update
	sudo apt-get install -y texlive-latex-base texlive-latex-extra texlive-fonts-recommended texlive-lang-german texlive-fonts-extra
	@echo ""
	@echo "Testing build system..."
	python3 ctmm_build.py
	@echo ""
	@echo "✅ Setup complete! Try 'make build' to generate PDF"

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
	@echo "CTMM LaTeX Build System - Comprehensive Toolset"
	@echo "==============================================="
	@echo "Available targets:"
	@echo "  all           - Run check and build (default)"
	@echo "  setup         - Install all dependencies and test build"
	@echo "  check         - Check dependencies and run build system"
	@echo "  validate-pr   - Validate PR content for Copilot review"
	@echo "  validate      - Validate LaTeX files for escaping issues"
	@echo "  validate-fix  - Fix LaTeX escaping issues (creates backups)"
	@echo "  build         - Build the PDF"
	@echo "  analyze       - Run detailed module analysis"
	@echo "  test          - Quick test of build system + unit tests"
	@echo "  test-unit     - Run only unit tests for ctmm_build.py"
	@echo "  unit-test     - Run unit tests for Python functions"
	@echo "  clean         - Remove build artifacts"
	@echo "  deps          - Show dependency installation commands"
	@echo "  comprehensive - Run complete workflow validation"
	@echo "  workflow      - Alias for comprehensive"
	@echo "  test-ci-robustness - Test CI pipeline robustness (Issue #1044)"
	@echo "  test-comprehensive-timeout - Test comprehensive CI timeout coverage"
	@echo "  enhanced-build  - Run enhanced CTMM build management"
	@echo "  enhanced-testing - Run enhanced incremental testing"
	@echo ""
	@echo "CTMM Unified Tool Commands:"
	@echo "  ctmm-check    - Run unified build system validation"
	@echo "  ctmm-fix      - Fix over-escaped LaTeX files"
	@echo "  ctmm-validate - Complete project validation"
	@echo "  ctmm-workflow - Run complete integration workflow"
	@echo "  integration-test - Run comprehensive integration tests"
	@echo ""
	@echo "  help          - Show this help"
	@echo ""
	@echo "Quick Start:"
	@echo "  make setup    - One-command setup with dependency installation"
	@echo "  make build    - Generate PDF after setup"
	@echo ""
	@echo "Troubleshooting: See BUILD_TROUBLESHOOTING.md for detailed help"
