# CTMM LaTeX Build System Makefile

.PHONY: build check clean test help safe-check

# Default target
all: check build

# Check build system and dependencies
check:
	@echo "Running CTMM Build System check..."
	python3 ctmm_build.py

# Enhanced check with safe package name handling
safe-check:
	@echo "Running enhanced CTMM Build Manager with sanitization..."
	python3 build_manager.py

# Build PDF
build:
	@echo "Building CTMM PDF..."
	pdflatex -interaction=nonstopmode main.tex
	pdflatex -interaction=nonstopmode main.tex  # Second pass for references

# Full analysis (detailed module testing)
analyze:
	@echo "Running detailed build analysis..."
	python3 build_system.py --verbose

# Test package name sanitization
test-sanitization:
	@echo "Testing package name sanitization..."
	python3 test_sanitization.py

# Demonstrate the security fix
demo-fix:
	@echo "Demonstrating LaTeX command name security fix..."
	python3 demonstrate_fix.py

# Test only (without building)
test:
	@echo "Testing build system..."
	python3 ctmm_build.py | grep -E "(PASS|FAIL|ERROR|WARNING)" || true

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
	@echo "  all              - Run check and build (default)"
	@echo "  check            - Check dependencies and run build system"
	@echo "  safe-check       - Enhanced build manager with package name sanitization"
	@echo "  build            - Build the PDF"
	@echo "  analyze          - Run detailed module analysis"
	@echo "  test-sanitization - Test package name sanitization functionality"
	@echo "  demo-fix         - Demonstrate the LaTeX command name security fix"
	@echo "  test             - Quick test of build system"
	@echo "  clean            - Remove build artifacts"
	@echo "  deps             - Install Python dependencies"
	@echo "  help             - Show this help"