# CTMM LaTeX Build System Makefile

.PHONY: build check clean test test-unit help validate-pr

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

# Validate PR readiness (check if changes can be reviewed by Copilot)
validate-pr:
	@echo "Validating PR readiness..."
	python3 validate_pr_readiness.py

# Pre-commit validation (combine testing and PR validation)
pre-commit: test-unit validate-pr
	@echo "✅ Pre-commit validation complete"

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

# Help
help:
	@echo "CTMM LaTeX Build System"
	@echo "======================="
	@echo "Available targets:"
	@echo "  all          - Run check and build (default)"
	@echo "  check        - Check dependencies and run build system"
	@echo "  build        - Build the PDF"
	@echo "  analyze      - Run detailed module analysis"
	@echo "  test         - Quick test of build system + unit tests"
	@echo "  test-unit    - Run only unit tests for ctmm_build.py"
	@echo "  validate-pr  - Check if current branch is ready for PR (Copilot review)"
	@echo "  pre-commit   - Run all pre-commit validations (tests + PR check)"
	@echo "  clean        - Remove build artifacts"
	@echo "  deps         - Install Python dependencies"
	@echo "  help         - Show this help"
