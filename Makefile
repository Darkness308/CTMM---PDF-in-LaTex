# CTMM LaTeX Project Makefile
# Provides automated build management and testing

.PHONY: all build analyze clean test help

# Default target
all: build

# Main build target
build:
	@echo "Building CTMM LaTeX document..."
	pdflatex -interaction=nonstopmode main.tex
	@echo "Build complete: main.pdf"

# CI build target (for GitHub Actions)
build-ci:
	@echo "Building CTMM LaTeX document for CI..."
	pdflatex -interaction=nonstopmode main_final.tex
	@echo "CI build complete: main_final.pdf"

# Run comprehensive build analysis
analyze:
	@echo "Running CTMM Build Manager analysis..."
	python3 build_manager.py
	@echo "Analysis complete. Check build_report.md for results."

# Test specific file
test-file:
	@echo "Testing $(FILE)..."
	python3 build_manager.py $(FILE)

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	rm -f *.aux *.log *.out *.toc *.pdf *.fls *.fdb_latexmk *.synctex.gz
	rm -f build_report.md
	@echo "Clean complete."

# Full clean including backups
clean-all: clean
	@echo "Removing backup files..."
	rm -f *.backup
	@echo "Full clean complete."

# Help target
help:
	@echo "CTMM LaTeX Build System"
	@echo "======================="
	@echo ""
	@echo "Available targets:"
	@echo "  build      - Build main.tex to main.pdf"
	@echo "  build-ci   - Build main_final.tex for CI"
	@echo "  analyze    - Run comprehensive build analysis"
	@echo "  test-file  - Test specific file (use FILE=filename.tex)"
	@echo "  clean      - Remove build artifacts"
	@echo "  clean-all  - Remove all generated files including backups"
	@echo "  help       - Show this help message"
	@echo ""
	@echo "Examples:"
	@echo "  make build"
	@echo "  make analyze"
	@echo "  make test-file FILE=main.tex"
	@echo "  make clean"