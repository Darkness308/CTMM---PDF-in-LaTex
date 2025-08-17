# CTMM LaTeX Build System Makefile

.PHONY: build check clean test test-unit validate-pr help unit-test validate validate-fix ctmm-check ctmm-fix ctmm-validate ctmm-workflow integration-test comprehensive workflow

# Default target
all: ctmm-check build

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
	@echo "Running comprehensive unit tests..."
	python3 test_ctmm_build.py
	python3 test_latex_validator.py

# Run unit tests with coverage analysis
test-coverage:
	@echo "Running unit tests with coverage analysis..."
	python3 test_coverage.py

# Run performance benchmarks
test-performance:
	@echo "Running performance benchmarks..."
	python3 -c "import test_ctmm_build; import unittest; suite = unittest.TestLoader().loadTestsFromTestCase(test_ctmm_build.TestPerformanceBenchmarks); unittest.TextTestRunner(verbosity=2).run(suite)"

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

# Help
help:
	@echo "CTMM LaTeX Build System - Comprehensive Toolset"
	@echo "==============================================="
	@echo "Available targets:"
	@echo "  all           - Run check and build (default)"
	@echo "  check         - Check dependencies and run build system"
	@echo "  validate-pr   - Validate PR content for Copilot review"
	@echo "  validate      - Validate LaTeX files for escaping issues"
	@echo "  validate-fix  - Fix LaTeX escaping issues (creates backups)"
	@echo "  build         - Build the PDF"
	@echo "  analyze       - Run detailed module analysis"
	@echo "  test          - Quick test of build system + unit tests"
	@echo "  test-unit     - Run only unit tests for ctmm_build.py"
	@echo "  unit-test     - Run comprehensive unit tests for Python functions"
	@echo "  test-coverage - Run unit tests with coverage analysis"
	@echo "  test-performance - Run performance benchmarks"
	@echo "  clean         - Remove build artifacts"
	@echo "  deps          - Install Python dependencies"
	@echo "  comprehensive - Run complete workflow validation"
	@echo "  workflow      - Alias for comprehensive"
	@echo ""
	@echo "CTMM Unified Tool Commands:"
	@echo "  ctmm-check    - Run unified build system validation"
	@echo "  ctmm-fix      - Fix over-escaped LaTeX files"
	@echo "  ctmm-validate - Complete project validation"
	@echo "  ctmm-workflow - Run complete integration workflow"
	@echo "  integration-test - Run comprehensive integration tests"
	@echo ""
	@echo "  help          - Show this help"
