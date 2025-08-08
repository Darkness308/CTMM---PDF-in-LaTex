# CTMM LaTeX Project Makefile
# Provides automated build management and testing

.PHONY: all build build-ci analyze clean clean-all test help

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

# Test with existing ctmm_build.py
test:
	@echo "Testing build system..."
	python3 ctmm_build.py | grep -E "(PASS|FAIL|ERROR|WARNING)" || true

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

# Install dependencies (for local development)
deps:
	@echo "Installing Python dependencies..."
	pip install chardet
	@echo "LaTeX packages should be installed via your system package manager"

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
	@echo "  test       - Quick test of build system"
	@echo "  clean      - Remove build artifacts"
	@echo "  clean-all  - Remove all generated files including backups"
	@echo "  deps       - Install Python dependencies"
	@echo "  help       - Show this help message"
	@echo ""
	@echo "Examples:"
	@echo "  make build"
	@echo "  make analyze"
	@echo "  make test-file FILE=main.tex"
	@echo "  make clean"