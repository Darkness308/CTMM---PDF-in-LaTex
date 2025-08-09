# CTMM LaTeX Build System Makefile
# Enhanced with comprehensive build management capabilities

.PHONY: build build-ci analyze check test clean clean-all deps help install

# Default target
all: check build

# Build main.tex (development build)
build:
	@echo "Building CTMM PDF (development version)..."
	pdflatex -interaction=nonstopmode main.tex
	pdflatex -interaction=nonstopmode main.tex  # Second pass for references
	@echo "✓ Development build complete: main.pdf"

# Build main_final.tex (CI/production build)
build-ci:
	@echo "Building CTMM PDF (CI/production version)..."
	pdflatex -interaction=nonstopmode main_final.tex
	pdflatex -interaction=nonstopmode main_final.tex  # Second pass for references
	@echo "✓ CI build complete: main_final.pdf"

# Run comprehensive build analysis with build_manager.py
analyze:
	@echo "Running comprehensive CTMM Build Manager analysis..."
	python3 build_manager.py
	@echo "✓ Analysis complete - check build_report.md for details"

# Quick dependency and system check
check:
	@echo "Running CTMM Build System quick check..."
	python3 ctmm_build.py
	@echo "✓ Quick check complete"

# Detailed module testing (legacy system)
test-legacy:
	@echo "Running detailed legacy build analysis..."
	python3 build_system.py --verbose

# Test only (without building) - extract key status info
test:
	@echo "Testing build system status..."
	@python3 build_manager.py | grep -E "(✓|✗|⚠|ERROR|WARNING|PASS|FAIL)" || echo "Build system test completed"

# Clean build artifacts (standard cleanup)
clean:
	@echo "Cleaning build artifacts..."
	rm -f *.aux *.log *.out *.toc *.pdf *.fls *.fdb_latexmk
	rm -f main_basic_test.* main.temp.* main_final.temp.*
	rm -f *.test_*.tex
	rm -f build_error_*.log
	@echo "✓ Build artifacts cleaned"

# Clean all generated files (including templates and reports)
clean-all: clean
	@echo "Cleaning all generated files..."
	rm -f build_report.md build_manager.log build_system.log
	rm -f modules/TODO_*.md style/TODO_*.md
	@echo "✓ All generated files cleaned"

# Install Python dependencies for build system
deps:
	@echo "Installing Python dependencies for CTMM Build System..."
	pip install chardet
	@echo "✓ Python dependencies installed"
	@echo "Note: LaTeX packages should be installed via your system package manager"

# Install LaTeX dependencies (system-specific guidance)
install-latex:
	@echo "LaTeX Installation Guide:"
	@echo "========================"
	@echo "Ubuntu/Debian: sudo apt-get install texlive-full"
	@echo "CentOS/RHEL:   sudo yum install texlive-scheme-full"
	@echo "macOS:         brew install mactex"
	@echo "Windows:       Download MiKTeX from https://miktex.org/"
	@echo ""
	@echo "For minimal installation, you need:"
	@echo "- pdflatex"
	@echo "- LaTeX packages: geometry, hyperref, xcolor, fontawesome5, tcolorbox, tabularx, amssymb"

# Development workflow helper
dev:
	@echo "Running development workflow..."
	@echo "1. Checking system..."
	@$(MAKE) check
	@echo ""
	@echo "2. Running analysis..."
	@$(MAKE) analyze
	@echo ""
	@echo "3. Building development version..."
	@$(MAKE) build

# CI workflow helper
ci:
	@echo "Running CI workflow..."
	@echo "1. Installing dependencies..."
	@$(MAKE) deps
	@echo ""
	@echo "2. Running comprehensive analysis..."
	@$(MAKE) analyze
	@echo ""
	@echo "3. Building CI version..."
	@$(MAKE) build-ci

# Help target with comprehensive usage information
help:
	@echo "CTMM LaTeX Build System"
	@echo "======================="
	@echo ""
	@echo "MAIN TARGETS:"
	@echo "  build        Build main.tex (development version)"
	@echo "  build-ci     Build main_final.tex (CI/production version)"
	@echo "  analyze      Run comprehensive build analysis (recommended)"
	@echo "  check        Quick dependency and system check"
	@echo ""
	@echo "TESTING:"
	@echo "  test         Quick test of build system status"
	@echo "  test-legacy  Detailed module testing (legacy system)"
	@echo ""
	@echo "MAINTENANCE:"
	@echo "  clean        Remove build artifacts"
	@echo "  clean-all    Remove all generated files (including reports)"
	@echo "  deps         Install Python dependencies"
	@echo "  install-latex Show LaTeX installation instructions"
	@echo ""
	@echo "WORKFLOWS:"
	@echo "  dev          Complete development workflow (check + analyze + build)"
	@echo "  ci           Complete CI workflow (deps + analyze + build-ci)"
	@echo ""
	@echo "USAGE EXAMPLES:"
	@echo "  make analyze    # Recommended: comprehensive analysis"
	@echo "  make build      # Build development PDF"
	@echo "  make dev        # Full development workflow"
	@echo "  make clean      # Clean up before committing"
	@echo ""
	@echo "For detailed documentation, see BUILD_GUIDE.md"