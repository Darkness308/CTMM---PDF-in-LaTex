# CTMM LaTeX Build System Makefile
# Enhanced with comprehensive build management capabilities

.PHONY: build build-ci check analyze clean clean-all test help

# Default target
all: check build

# Check build system and dependencies
check:
	@echo "Running CTMM Build Manager check..."
	python3 build_manager.py

# Build PDF (main development target)
build:
	@echo "Building CTMM PDF..."
	pdflatex -interaction=nonstopmode main.tex
	pdflatex -interaction=nonstopmode main.tex  # Second pass for references

# Build CI target
build-ci:
	@echo "Building CTMM CI PDF..."
	pdflatex -interaction=nonstopmode main_final.tex
	pdflatex -interaction=nonstopmode main_final.tex  # Second pass for references

# Full analysis (detailed module testing)
analyze:
	@echo "Running comprehensive build analysis..."
	python3 build_manager.py --verbose

# Legacy support for existing build system
analyze-legacy:
	@echo "Running legacy detailed build analysis..."
	python3 build_system.py --verbose

# Test only (without building)
test:
	@echo "Testing build system..."
	python3 build_manager.py | grep -E "(PASS|FAIL|ERROR|WARNING)" || true

# Clean build artifacts
clean:
	rm -f *.aux *.log *.out *.toc *.pdf *.fls *.fdb_latexmk
	rm -f main_basic_test.* main_final_basic_test.*
	rm -f *.temp.* *.basic_test.* *.test_module_*
	rm -f build_error_*.log module_error_*.log
	rm -f basic_build_error.log full_build_error.log
	@echo "Cleaned build artifacts"

# Clean all generated files including templates and TODO files
clean-all: clean
	@echo "Removing generated template and TODO files..."
	find . -name "TODO_*.md" -delete 2>/dev/null || true
	@echo "Warning: This removes auto-generated templates. Use with caution."

# Install dependencies (for local development)
deps:
	@echo "Installing Python dependencies..."
	pip install chardet
	@echo "LaTeX packages should be installed via your system package manager:"
	@echo "  Ubuntu/Debian: sudo apt-get install texlive-latex-extra texlive-fonts-recommended"
	@echo "  macOS: brew install --cask mactex"
	@echo "  Windows: Install MiKTeX or TeX Live"

# Development helpers
dev-setup: deps
	@echo "Setting up development environment..."
	python3 build_manager.py
	@echo "Development setup complete. Check build_report.md for status."

# View build report
report:
	@if [ -f build_report.md ]; then \
		echo "=== CTMM Build Report ==="; \
		cat build_report.md; \
	else \
		echo "No build report found. Run 'make check' or 'make analyze' first."; \
	fi

# Help
help:
	@echo "CTMM LaTeX Build System"
	@echo "======================="
	@echo "Available targets:"
	@echo ""
	@echo "Build Commands:"
	@echo "  all           - Run check and build (default)"
	@echo "  build         - Build main.tex PDF"
	@echo "  build-ci      - Build main_final.tex for CI/CD"
	@echo ""
	@echo "Analysis Commands:"
	@echo "  check         - Check dependencies and run build manager"
	@echo "  analyze       - Run comprehensive build analysis with verbose output"
	@echo "  test          - Quick test of build system"
	@echo "  report        - View the latest build report"
	@echo ""
	@echo "Maintenance Commands:"
	@echo "  clean         - Remove build artifacts"
	@echo "  clean-all     - Remove all generated files (use with caution)"
	@echo "  deps          - Install Python dependencies"
	@echo "  dev-setup     - Complete development environment setup"
	@echo ""
	@echo "Legacy Commands:"
	@echo "  analyze-legacy - Run legacy build_system.py analysis"
	@echo ""
	@echo "Help:"
	@echo "  help          - Show this help"
	@echo ""
	@echo "Quick Start:"
	@echo "  make dev-setup    # Set up development environment"
	@echo "  make build        # Build the PDF"
	@echo "  make analyze      # Comprehensive analysis"