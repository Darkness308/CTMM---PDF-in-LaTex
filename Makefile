# CTMM LaTeX Build System Makefile

.PHONY: build check clean test help unit-test validate validate-fix

# Default target
all: check build

# Check build system and dependencies
check:
	@echo "Running CTMM Build System check..."
	python3 ctmm_build.py

# Validate LaTeX files for escaping issues
validate:
	@echo "Validating LaTeX files for escaping issues..."
	python3 latex_validator.py modules/

# Fix LaTeX escaping issues (creates backups)
validate-fix:
	@echo "Fixing LaTeX escaping issues..."
	python3 latex_validator.py modules/ --fix

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
	@echo "  validate     - Validate LaTeX files for escaping issues"
	@echo "  validate-fix - Fix LaTeX escaping issues (creates backups)"
	@echo "  build        - Build the PDF"
	@echo "  analyze      - Run detailed module analysis"
	@echo "  test         - Quick test of build system"
	@echo "  unit-test    - Run unit tests for Python functions"
	@echo "  clean        - Remove build artifacts"
	@echo "  deps         - Install Python dependencies"
	@echo "  help         - Show this help"