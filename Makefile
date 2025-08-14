# CTMM LaTeX Build System Makefile

.PHONY: build check clean test test-unit validate-packages help

# Default target
all: check build

# Check build system and dependencies
check:
	@echo "Running CTMM Build System check..."
	python3 ctmm_build.py

# Validate LaTeX packages (useful for CI environments)
validate-packages:
	@echo "Validating LaTeX package dependencies..."
	python3 validate_latex_packages.py

# Build PDF
build:
	@echo "Building CTMM PDF..."
	pdflatex -interaction=nonstopmode main.tex
	pdflatex -interaction=nonstopmode main.tex  # Second pass for references

# Full analysis (detailed module testing)
analyze:
	@echo "Running detailed build analysis..."
	python3 build_system.py --verbose

# Comprehensive validation (syntax + packages + build system)
validate:
	@echo "Running comprehensive validation..."
	@echo "1. LaTeX syntax validation..."
	python3 validate_latex_syntax.py
	@echo "2. LaTeX package validation..."
	python3 validate_latex_packages.py
	@echo "3. Build system validation..."
	python3 ctmm_build.py

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
	rm -f package_test_*.tex
	rm -f test_*.tex test_*.aux test_*.log test_*.pdf
	rm -f __pycache__/*.pyc
	@echo "Cleaned build artifacts"

# Install dependencies (for local development)
deps:
	@echo "Installing Python dependencies..."
	pip install chardet
	@echo "LaTeX packages should be installed via your system package manager"
	@echo "Run 'make validate-packages' to check LaTeX package availability"

# Help
help:
	@echo "CTMM LaTeX Build System"
	@echo "======================="
	@echo "Available targets:"
	@echo "  all              - Run check and build (default)"
	@echo "  check            - Check dependencies and run build system"
	@echo "  validate-packages - Validate LaTeX package dependencies"
	@echo "  validate         - Comprehensive validation (syntax + packages + build)"
	@echo "  build            - Build the PDF"
	@echo "  analyze          - Run detailed module analysis"
	@echo "  test             - Quick test of build system + unit tests"
	@echo "  test-unit        - Run only unit tests for ctmm_build.py"
	@echo "  clean            - Remove build artifacts"
	@echo "  deps             - Install Python dependencies"
	@echo "  help             - Show this help"
