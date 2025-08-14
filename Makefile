# CTMM LaTeX Build System Makefile

.PHONY: build check clean test test-unit help comprehensive workflow unified status de-escape integration-test

# Default target
all: check build

# Check build system and dependencies
check:
	@echo "Running CTMM Build System check..."
	python3 ctmm_build.py

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

# Unified tool commands
unified:
	@echo "CTMM Unified Tool - Available commands:"
	python3 ctmm_unified_tool.py --help

# Unified tool status
status:
	@echo "Checking CTMM system status..."
	python3 ctmm_unified_tool.py status

# Unified tool build
unified-build:
	@echo "Running unified build..."
	python3 ctmm_unified_tool.py build

# Unified tool validation
unified-validate:
	@echo "Running unified validation..."
	python3 ctmm_unified_tool.py validate

# Unified tool workflow
unified-workflow:
	@echo "Running unified workflow..."
	python3 ctmm_unified_tool.py workflow

# Unified tool tests
unified-test:
	@echo "Running unified tests..."
	python3 ctmm_unified_tool.py test

# De-escape LaTeX files
de-escape:
	@echo "Running LaTeX de-escaping..."
	python3 ctmm_unified_tool.py de-escape converted

# Integration tests
integration-test:
	@echo "Running CTMM integration tests..."
	python3 test_integration.py

# Quick integration tests
integration-test-quick:
	@echo "Running quick integration tests..."
	python3 test_integration.py --quick

# Help
help:
	@echo "CTMM LaTeX Build System - Comprehensive Toolset"
	@echo "==============================================="
	@echo "Available targets:"
	@echo "  all              - Run check and build (default)"
	@echo "  comprehensive    - Run complete workflow validation"
	@echo "  workflow         - Alias for comprehensive"
	@echo ""
	@echo "Classic Commands:"
	@echo "  check            - Check dependencies and run build system"
	@echo "  build            - Build the PDF"
	@echo "  analyze          - Run detailed module analysis"
	@echo "  test             - Quick test of build system + unit tests"
	@echo "  test-unit        - Run only unit tests for ctmm_build.py"
	@echo "  clean            - Remove build artifacts"
	@echo "  deps             - Install Python dependencies"
	@echo ""
	@echo "Unified Tool Commands:"
	@echo "  unified          - Show unified tool help"
	@echo "  status           - Check system status"
	@echo "  unified-build    - Run unified build"
	@echo "  unified-validate - Run unified validation"
	@echo "  unified-workflow - Run unified workflow"
	@echo "  unified-test     - Run unified tests"
	@echo "  de-escape        - Fix LaTeX over-escaping"
	@echo ""
	@echo "Testing:"
	@echo "  integration-test - Run comprehensive integration tests"
	@echo "  integration-test-quick - Run quick integration tests"
	@echo ""
	@echo "  help             - Show this help"
