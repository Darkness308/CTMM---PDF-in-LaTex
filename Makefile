# CTMM Automated Build Management System Makefile

.PHONY: build build-ci check analyze test clean clean-all deps help

# Default target
all: analyze build

# Comprehensive build analysis (primary command)
analyze:
	@echo "Running CTMM Build Management System comprehensive analysis..."
	python3 build_manager.py

# Standard build (main.tex)
build:
	@echo "Building CTMM PDF from main.tex..."
	pdflatex -interaction=nonstopmode main.tex
	pdflatex -interaction=nonstopmode main.tex  # Second pass for references
	@echo "✓ Build complete: main.pdf"

# CI build (main_final.tex for continuous integration)
build-ci:
	@echo "Building CTMM CI PDF from main_final.tex..."
	pdflatex -interaction=nonstopmode main_final.tex
	pdflatex -interaction=nonstopmode main_final.tex  # Second pass for references
	@echo "✓ CI Build complete: main_final.pdf"

# Quick check (legacy compatibility)
check:
	@echo "Running CTMM Build System quick check..."
	python3 ctmm_build.py

# Detailed legacy analysis
analyze-legacy:
	@echo "Running detailed legacy build analysis..."
	python3 build_system.py --verbose

# Test only (without building PDFs)
test:
	@echo "Testing build system functionality..."
	python3 build_manager.py | grep -E "(PASS|FAIL|ERROR|WARNING|✓|✗)" || true

# Clean build artifacts only
clean:
	@echo "Cleaning build artifacts..."
	rm -f *.aux *.log *.out *.toc *.pdf
	rm -f main_basic_test.*
	rm -f *.temp.*
	rm -f *.test_*.tex
	rm -f build_error_*.log
	rm -f build_system.log
	@echo "✓ Build artifacts cleaned"

# Clean everything including generated templates and reports
clean-all: clean
	@echo "Cleaning all generated files..."
	rm -f build_report.md
	rm -f modules/TODO_*.md
	rm -f style/TODO_*.md
	@echo "⚠️  Warning: This removes generated templates and TODO files!"
	@echo "✓ All generated files cleaned"

# Install dependencies
deps:
	@echo "Installing Python dependencies..."
	pip install chardet
	@echo "Installing LaTeX packages..."
	@echo "  Ubuntu/Debian: sudo apt install texlive-latex-base texlive-latex-extra texlive-fonts-recommended texlive-fonts-extra texlive-lang-german"
	@echo "  MacOS: brew install mactex"
	@echo "  Windows: Install MiKTeX or TeX Live"

# Show comprehensive help
help:
	@echo "CTMM Automated Build Management System"
	@echo "======================================"
	@echo ""
	@echo "🚀 PRIMARY COMMANDS:"
	@echo "  analyze    - Run comprehensive build analysis (RECOMMENDED)"
	@echo "  build      - Build main.tex to PDF"
	@echo "  build-ci   - Build main_final.tex for CI/CD"
	@echo ""
	@echo "🔧 UTILITY COMMANDS:"
	@echo "  check      - Quick build system check (legacy)"
	@echo "  test       - Test build system without generating PDFs"
	@echo "  clean      - Remove build artifacts"
	@echo "  clean-all  - Remove all generated files (templates, reports)"
	@echo "  deps       - Show dependency installation instructions"
	@echo ""
	@echo "📖 USAGE EXAMPLES:"
	@echo "  make analyze   # Full analysis with error detection"
	@echo "  make build     # Standard PDF build"
	@echo "  make clean     # Clean up after build"
	@echo ""
	@echo "📋 BUILD WORKFLOW:"
	@echo "  1. Run 'make analyze' to check system and create templates"
	@echo "  2. Complete any TODO files for missing content"
	@echo "  3. Run 'make build' to generate final PDF"
	@echo "  4. Use 'make clean' to remove temporary files"
	@echo ""
	@echo "For detailed documentation, see BUILD_GUIDE.md"