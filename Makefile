# CTMM LaTeX Build System Makefile

.PHONY: build check clean test help analyze build-ci clean-all

# Default target
all: check build

# Run build manager check and analysis
check:
	@echo "Running CTMM Build Manager check..."
	python3 build_manager.py

# Build main PDF
build:
	@echo "Building CTMM PDF..."
	pdflatex -interaction=nonstopmode main.tex
	pdflatex -interaction=nonstopmode main.tex  # Second pass for references

# Build CI target (main_final.tex)
build-ci:
	@echo "Building CTMM PDF for CI..."
	pdflatex -interaction=nonstopmode main_final.tex
	pdflatex -interaction=nonstopmode main_final.tex  # Second pass for references

# Full analysis (detailed module testing)
analyze:
	@echo "Running comprehensive build analysis..."
	python3 build_manager.py --verbose

# Test only (without building)
test:
	@echo "Testing build system..."
	python3 ctmm_build.py | grep -E "(PASS|FAIL|ERROR|WARNING)" || true

# Clean build artifacts
clean:
	rm -f *.aux *.log *.out *.toc
	rm -f main_basic_test.*
	rm -f *.temp.*
	rm -f main_test_*.tex
	rm -f *.basic_test.*
	rm -f build_error_*.log
	@echo "Cleaned build artifacts"

# Clean all generated files including PDFs and templates
clean-all: clean
	rm -f *.pdf
	rm -f modules/TODO_*.md
	rm -f style/TODO_*.md
	rm -f build_report.md
	rm -f build_manager.log
	rm -f build_system.log
	@echo "Cleaned all generated files"

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
	@echo "  all       - Run check and build (default)"
	@echo "  check     - Check dependencies and run build manager"
	@echo "  build     - Build the main PDF (main.tex)"
	@echo "  build-ci  - Build the CI PDF (main_final.tex)"
	@echo "  analyze   - Run comprehensive build analysis"
	@echo "  test      - Quick test of build system"
	@echo "  clean     - Remove build artifacts"
	@echo "  clean-all - Remove all generated files including PDFs"
	@echo "  deps      - Install Python dependencies"
	@echo "  help      - Show this help"