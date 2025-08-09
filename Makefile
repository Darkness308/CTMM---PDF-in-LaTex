# CTMM LaTeX Build System Makefile

.PHONY: build check clean test help convert

# Default target
all: check build

# Check build system and dependencies
check:
	@echo "Running CTMM Build System check..."
	python3 ctmm_build.py

# Build PDF with multi-pass compilation
build:
	@echo "Building CTMM PDF with multi-pass compilation..."
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

# Document conversion pipeline
convert:
	@echo "Running document conversion pipeline..."
	python3 conversion_pipeline.py --help

# Convert therapy tools
convert-tools:
	@echo "Creating therapy tool templates..."
	python3 conversion_pipeline.py --tool "Example Tool" --tool-number 25

# Clean build artifacts
clean:
	rm -f *.aux *.log *.out *.toc *.pdf
	rm -f main_basic_test.*
	rm -f *.temp.*
	rm -f build_error_*.log
	rm -f build_system.log
	rm -f conversion_pipeline.log
	@echo "Cleaned build artifacts"

# Install dependencies (for local development)
deps:
	@echo "Installing Python dependencies..."
	pip install chardet
	@echo "LaTeX packages should be installed via your system package manager"
	@echo "For Ubuntu/Debian: sudo apt-get install texlive-latex-extra texlive-lang-german"

# Help
help:
	@echo "CTMM LaTeX Build System"
	@echo "======================="
	@echo "Available targets:"
	@echo "  all      - Run check and build (default)"
	@echo "  check    - Check dependencies and run build system"
	@echo "  build    - Build the PDF with multi-pass compilation"
	@echo "  analyze  - Run detailed module analysis"
	@echo "  test     - Quick test of build system"
	@echo "  convert  - Show conversion pipeline help"
	@echo "  clean    - Remove build artifacts"
	@echo "  deps     - Install Python dependencies"
	@echo "  help     - Show this help"