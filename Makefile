# CTMM LaTeX Build System Makefile - Enhanced Workflow System

.PHONY: build check clean test help convert optimize error-analysis workflow

# Default target - Complete workflow
all: workflow

# Complete CTMM workflow pipeline
workflow:
	@echo "=========================================="
	@echo "CTMM COMPREHENSIVE WORKFLOW PIPELINE"
	@echo "=========================================="
	@echo "Phase 1: Document Conversion..."
	@$(MAKE) convert
	@echo "\nPhase 2: Code Optimization..."
	@$(MAKE) optimize
	@echo "\nPhase 3: Build System Check..."
	@$(MAKE) check
	@echo "\nPhase 4: Error Analysis..."
	@$(MAKE) error-analysis
	@echo "\nPhase 5: Final Build..."
	@$(MAKE) build
	@echo "\n✅ CTMM Workflow Complete!"

# Document conversion pipeline
convert:
	@echo "Converting Word/Markdown documents to LaTeX..."
	python3 document_converter.py

# Code optimization
optimize:
	@echo "Optimizing LaTeX code..."
	python3 optimizer.py

# Advanced error analysis
error-analysis:
	@echo "Running advanced error analysis..."
	python3 error_analyzer.py || echo "⚠️ Issues detected - check analysis report"

# Check build system and dependencies
check:
	@echo "Running CTMM Build System check..."
	python3 ctmm_build.py

# Build PDF with multi-pass compilation
build:
	@echo "Building CTMM PDF with multi-pass compilation..."
	pdflatex -interaction=nonstopmode main.tex
	pdflatex -interaction=nonstopmode main.tex  # Second pass for references
	@echo "✓ PDF build complete"

# Full analysis (detailed module testing)
analyze:
	@echo "Running detailed build analysis..."
	python3 build_system.py --verbose

# Test only (without building)
test:
	@echo "Testing build system..."
	python3 ctmm_build.py | grep -E "(PASS|FAIL|ERROR|WARNING)" || true

# Quality assurance workflow
qa: convert optimize check error-analysis
	@echo "Quality assurance workflow complete"

# Development workflow
dev: check build error-analysis
	@echo "Development workflow complete"

# Production workflow
prod: convert optimize check build
	@echo "Production workflow complete"

# Clean build artifacts
clean:
	rm -f *.aux *.log *.out *.toc *.pdf
	rm -f main_basic_test.*
	rm -f *.temp.*
	rm -f build_error_*.log
	rm -f error_analysis_*.md
	rm -f ctmm_analysis.json ctmm_analysis_report.md
	rm -f conversion.log error_analysis.log build_system.log
	@echo "Cleaned build artifacts and logs"

# Deep clean (including converted files)
clean-all: clean
	rm -rf converted/
	@echo "Deep clean complete"

# Install dependencies (for local development)
deps:
	@echo "Installing system dependencies..."
	sudo apt-get update
	sudo apt-get install -y pandoc texlive-lang-german texlive-fonts-extra
	@echo "Installing Python dependencies..."
	pip install chardet
	@echo "Dependencies installed"

# Generate project statistics
stats:
	@echo "CTMM Project Statistics:"
	@echo "========================"
	@find . -name "*.tex" | wc -l | awk '{print "LaTeX files: " $$1}'
	@find . -name "*.sty" | wc -l | awk '{print "Style files: " $$1}'
	@find . -name "*.docx" | wc -l | awk '{print "Word docs: " $$1}'
	@find converted/ -name "*.tex" 2>/dev/null | wc -l | awk '{print "Converted files: " $$1}' || echo "Converted files: 0"
	@wc -l *.tex 2>/dev/null | tail -1 | awk '{print "Total lines: " $$1}' || echo "Total lines: 0"

# Validate all systems
validate:
	@echo "Validating CTMM systems..."
	@python3 -c "import ctmm_build; print('✓ Build system OK')" 2>/dev/null || echo "✗ Build system issues"
	@python3 -c "import document_converter; print('✓ Converter OK')" 2>/dev/null || echo "✗ Converter issues"
	@python3 -c "import error_analyzer; print('✓ Analyzer OK')" 2>/dev/null || echo "✗ Analyzer issues"
	@python3 -c "import optimizer; print('✓ Optimizer OK')" 2>/dev/null || echo "✗ Optimizer issues"
	@which pdflatex >/dev/null && echo "✓ LaTeX OK" || echo "✗ LaTeX missing"
	@which pandoc >/dev/null && echo "✓ Pandoc OK" || echo "✗ Pandoc missing"

# Help
help:
	@echo "CTMM LaTeX Comprehensive Workflow System"
	@echo "========================================"
	@echo "Main Workflows:"
	@echo "  all         - Complete workflow pipeline (default)"
	@echo "  workflow    - Complete workflow with all phases"
	@echo "  qa          - Quality assurance workflow"
	@echo "  dev         - Development workflow"
	@echo "  prod        - Production workflow"
	@echo ""
	@echo "Individual Components:"
	@echo "  convert     - Convert Word/Markdown to LaTeX"
	@echo "  optimize    - Optimize LaTeX code"
	@echo "  check       - Check build system"
	@echo "  build       - Build PDF"
	@echo "  error-analysis - Run advanced error analysis"
	@echo "  analyze     - Detailed module analysis"
	@echo "  test        - Quick build test"
	@echo ""
	@echo "Maintenance:"
	@echo "  clean       - Remove build artifacts"
	@echo "  clean-all   - Deep clean including converted files"
	@echo "  deps        - Install dependencies"
	@echo "  validate    - Validate all systems"
	@echo "  stats       - Show project statistics"
	@echo "  help        - Show this help"