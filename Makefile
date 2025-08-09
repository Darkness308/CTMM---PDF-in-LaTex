# CTMM LaTeX Build System Makefile

.PHONY: build check clean test help convert integrate enhanced-build

# Default target
all: check build

# Check build system and dependencies
check:
	@echo "Running CTMM Build System check..."
	python3 ctmm_build.py

# Build PDF
build:
	@echo "Building CTMM PDF..."
	pdflatex -interaction=nonstopmode main.tex
	pdflatex -interaction=nonstopmode main.tex  # Second pass for references

# Enhanced build with comprehensive analysis
enhanced-build:
	@echo "Running enhanced CTMM build pipeline..."
	python3 enhanced_build_system.py

# Convert documents from therapie-material to LaTeX
convert:
	@echo "Converting therapy documents to LaTeX..."
	python3 conversion_pipeline.py

# Integrate converted documents into main.tex
integrate:
	@echo "Integrating converted documents..."
	python3 integrate_documents.py

# Fix encoding and syntax issues
fix-converted:
	@echo "Fixing converted document issues..."
	python3 fix_converted_files.py

# Full workflow: convert, integrate, and build
full-workflow: convert fix-converted integrate enhanced-build

# Full analysis (detailed module testing)
analyze:
	@echo "Running detailed build analysis..."
	python3 build_system.py --verbose

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
	rm -f build_pass_*.log
	rm -f enhanced_build.log conversion_pipeline.log
	rm -rf build/
	@echo "Cleaned build artifacts"

# Clean everything including converted files
clean-all: clean
	rm -rf converted/
	rm -f *.backup
	rm -f *_report.md
	@echo "Cleaned all generated files"

# Install dependencies (for local development)
deps:
	@echo "Installing Python dependencies..."
	pip install chardet
	@echo "Installing LaTeX packages..."
	sudo apt-get update
	sudo apt-get install -y texlive-latex-base texlive-fonts-recommended texlive-latex-extra texlive-lang-german texlive-fonts-extra pandoc poppler-utils

# Help
help:
	@echo "Enhanced CTMM LaTeX Build System"
	@echo "================================"
	@echo "Available targets:"
	@echo "  all            - Run check and build (default)"
	@echo "  check          - Check dependencies and run build system"
	@echo "  build          - Build the PDF"
	@echo "  enhanced-build - Run enhanced build with quality analysis"
	@echo "  convert        - Convert Word documents to LaTeX"
	@echo "  integrate      - Integrate converted documents into main.tex"
	@echo "  fix-converted  - Fix encoding and syntax issues"
	@echo "  full-workflow  - Complete conversion and build pipeline"
	@echo "  analyze        - Run detailed module analysis"
	@echo "  test           - Quick test of build system"
	@echo "  clean          - Remove build artifacts"
	@echo "  clean-all      - Remove all generated files"
	@echo "  deps           - Install all dependencies"
	@echo "  help           - Show this help"