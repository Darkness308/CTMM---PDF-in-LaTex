# CTMM LaTeX Build System Makefile

.PHONY: build check clean test test-unit help comprehensive workflow unified-status unified-build unified-validate unified-test unified-fix-escaping

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

# ==========================================
# UNIFIED TOOL COMMANDS - NEW INTEGRATION
# ==========================================

# Unified tool status check
unified-status:
	@echo "Running CTMM Unified Tool Status..."
	python3 ctmm_unified_tool.py status

# Unified tool build command
unified-build:
	@echo "Running CTMM Unified Tool Build..."
	python3 ctmm_unified_tool.py build

# Unified tool validation
unified-validate:
	@echo "Running CTMM Unified Tool Validation..."
	python3 ctmm_unified_tool.py validate

# Unified tool comprehensive validation with integration tests
unified-validate-full:
	@echo "Running CTMM Unified Tool Full Validation..."
	python3 ctmm_unified_tool.py validate --integration

# Unified tool test suite
unified-test:
	@echo "Running CTMM Unified Tool Tests..."
	python3 ctmm_unified_tool.py test

# Unified tool test suite with integration tests
unified-test-full:
	@echo "Running CTMM Unified Tool Full Test Suite..."
	python3 ctmm_unified_tool.py test --integration

# Unified tool LaTeX de-escaping (example usage)
unified-fix-escaping:
	@echo "Running CTMM Unified Tool De-escaping (on converted/ if exists)..."
	@if [ -d "converted" ]; then \
		python3 ctmm_unified_tool.py fix-escaping converted/ --validate; \
	else \
		echo "No 'converted' directory found. Create test files or specify directory."; \
		echo "Usage: make unified-fix-escaping DIR=your_directory"; \
	fi

# Unified tool workflow execution
unified-workflow:
	@echo "Running CTMM Unified Tool Workflow..."
	python3 ctmm_unified_tool.py workflow

# Unified tool clean
unified-clean:
	@echo "Running CTMM Unified Tool Clean..."
	python3 ctmm_unified_tool.py clean

# Integration test suite
integration-test:
	@echo "Running CTMM Integration Test Suite..."
	python3 test_integration.py

# Help
help:
	@echo "CTMM LaTeX Build System - Comprehensive Toolset"
	@echo "==============================================="
	@echo "Available targets:"
	@echo ""
	@echo "BASIC COMMANDS:"
	@echo "  all                    - Run check and build (default)"
	@echo "  check                  - Check dependencies and run build system"
	@echo "  build                  - Build the PDF"
	@echo "  analyze                - Run detailed module analysis"
	@echo "  test                   - Quick test of build system + unit tests"
	@echo "  test-unit              - Run only unit tests for ctmm_build.py"
	@echo "  clean                  - Remove build artifacts"
	@echo "  deps                   - Install Python dependencies"
	@echo ""
	@echo "WORKFLOW COMMANDS:"
	@echo "  comprehensive          - Run complete workflow validation"
	@echo "  workflow               - Alias for comprehensive"
	@echo "  integration-test       - Run integration test suite"
	@echo ""
	@echo "UNIFIED TOOL COMMANDS (NEW):"
	@echo "  unified-status         - Show system status via unified tool"
	@echo "  unified-build          - Build system check via unified tool"
	@echo "  unified-validate       - Core validation via unified tool"
	@echo "  unified-validate-full  - Full validation with integration tests"
	@echo "  unified-test           - Test suite via unified tool"
	@echo "  unified-test-full      - Full test suite with integration tests"
	@echo "  unified-fix-escaping   - LaTeX de-escaping via unified tool"
	@echo "  unified-workflow       - Complete workflow via unified tool"
	@echo "  unified-clean          - Clean via unified tool"
	@echo ""
	@echo "For more information on unified tool commands:"
	@echo "  python3 ctmm_unified_tool.py --help"
