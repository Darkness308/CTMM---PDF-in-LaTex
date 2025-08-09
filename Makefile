# CTMM LaTeX Build System Makefile with Security Enhancements

.PHONY: build check clean test help safe-check test-sanitization demo-fix

# Default target
all: check build

# Check build system and dependencies
check:
	@echo "Running CTMM Build System check..."
	python3 ctmm_build.py

# Enhanced security check with sanitization
safe-check:
	@echo "Running CTMM Enhanced Build Manager with security validation..."
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

# Test sanitization system
test-sanitization:
	@echo "Testing package name sanitization system..."
	python3 test_sanitization.py

# Demonstrate security fix
demo-fix:
	@echo "Demonstrating security vulnerability fix..."
	python3 demonstrate_fix.py

# Test build manager sanitization functions
test-manager:
	@echo "Testing build manager sanitization functions..."
	python3 build_manager.py --test-sanitization

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
	@echo "CTMM LaTeX Build System with Security Enhancements"
	@echo "=================================================="
	@echo "Available targets:"
	@echo "  all             - Run check and build (default)"
	@echo "  check           - Check dependencies and run build system"
	@echo "  safe-check      - Enhanced security check with sanitization"
	@echo "  build           - Build the PDF"
	@echo "  analyze         - Run detailed module analysis"
	@echo "  test-sanitization - Test package name sanitization system"
	@echo "  demo-fix        - Demonstrate security vulnerability fix"
	@echo "  test-manager    - Test build manager sanitization functions"
	@echo "  test            - Quick test of build system"
	@echo "  clean           - Remove build artifacts"
	@echo "  deps            - Install Python dependencies"
	@echo "  help            - Show this help"
	@echo ""
	@echo "Security Features:"
	@echo "  ✅ Package name sanitization (hyphens/underscores → camelCase)"
	@echo "  ✅ LaTeX command validation (prevents compilation errors)"
	@echo "  ✅ Safe template generation with security checks"
	@echo "  ✅ Comprehensive test suite for edge cases"