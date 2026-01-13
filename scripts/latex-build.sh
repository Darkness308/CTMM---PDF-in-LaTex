#!/bin/bash
# Enhanced LaTeX Build Script for CTMM Project
# Implements pdflatex + BibTeX + multiple passes workflow

set -e

# Configuration
MAIN_FILE="${1:-main.tex}"
BUILD_DIR="build"
LOG_FILE="$BUILD_DIR/build-log.txt"
ERROR_SUMMARY="$BUILD_DIR/error-summary.txt"
WARNING_SUMMARY="$BUILD_DIR/warning-summary.txt"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Initialize build directory and logs
mkdir -p "$BUILD_DIR"
echo "CTMM LaTeX Build Log - $(date)" > "$LOG_FILE"
echo "==================================" >> "$LOG_FILE"

log_message() {
  echo -e "$1" | tee -a "$LOG_FILE"
}

check_dependencies() {
  log_message "${BLUE}Checking LaTeX dependencies...${NC}"

  if ! command -v pdflatex &> /dev/null; then
  log_message "${RED}Error: pdflatex not found${NC}"
  exit 1
  fi

  if ! command -v bibtex &> /dev/null; then
  log_message "${RED}Error: bibtex not found${NC}"
  exit 1
  fi

  log_message "${GREEN}[OK] All dependencies found${NC}"
}

analyze_log() {
  local tex_log="$1"
  local errors=()
  local warnings=()

  if [[ -f "$tex_log" ]]; then
  # Extract errors
  while IFS= read -r line; do
  errors+=("$line")
  done < <(grep -n "^!" "$tex_log" || true)

  # Extract warnings
  while IFS= read -r line; do
  warnings+=("$line")
  done < <(grep -n "Warning" "$tex_log" || true)

  # Write error summary
  {
  echo "LaTeX Error Summary - $(date)"
  echo "=============================="
  echo "Errors found: ${#errors[@]}"
  for error in "${errors[@]}"; do
  echo "ERROR: $error"
  done
  echo ""
  } > "$ERROR_SUMMARY"

  # Write warning summary
  {
  echo "LaTeX Warning Summary - $(date)"
  echo "==============================="
  echo "Warnings found: ${#warnings[@]}"
  for warning in "${warnings[@]}"; do
  echo "WARNING: $warning"
  done
  echo ""
  } > "$WARNING_SUMMARY"

  log_message "${BLUE}Found ${#errors[@]} errors and ${#warnings[@]} warnings${NC}"

  if [[ ${#errors[@]} -gt 0 ]]; then
  log_message "${RED}Build completed with errors - see $ERROR_SUMMARY${NC}"
  return 1
  fi
  fi

  return 0
}

run_pdflatex() {
  local pass_num="$1"
  local basename=$(basename "$MAIN_FILE" .tex)

  log_message "${BLUE}Running pdflatex pass $pass_num...${NC}"

  if pdflatex -output-directory="$BUILD_DIR" -interaction=nonstopmode "$MAIN_FILE" >> "$LOG_FILE" 2>&1; then
  log_message "${GREEN}[OK] pdflatex pass $pass_num completed${NC}"
  analyze_log "$BUILD_DIR/$basename.log"
  return $?
  else
  log_message "${RED}[ERROR] pdflatex pass $pass_num failed${NC}"
  analyze_log "$BUILD_DIR/$basename.log"
  return 1
  fi
}

run_bibtex() {
  local basename=$(basename "$MAIN_FILE" .tex)

  # Only run BibTeX if .bib files exist or citations are found
  if [[ -f "references.bib" ]] || grep -q "\\cite\|\\bibliography" "$MAIN_FILE" modules/*.tex 2>/dev/null; then
  log_message "${BLUE}Running BibTeX...${NC}"

  cd "$BUILD_DIR"
  if bibtex "$basename" >> "../$LOG_FILE" 2>&1; then
  cd ..
  log_message "${GREEN}[OK] BibTeX completed${NC}"
  return 0
  else
  cd ..
  log_message "${YELLOW}[WARN] BibTeX completed with warnings${NC}"
  return 0
  fi
  else
  log_message "${YELLOW}No bibliography found, skipping BibTeX${NC}"
  return 0
  fi
}

check_pdf_completeness() {
  local basename=$(basename "$MAIN_FILE" .tex)
  local pdf_file="$BUILD_DIR/$basename.pdf"

  log_message "${BLUE}Checking PDF completeness...${NC}"

  if [[ ! -f "$pdf_file" ]]; then
  log_message "${RED}[ERROR] PDF file not generated${NC}"
  return 1
  fi

  # Check PDF file size
  local pdf_size=$(stat -c%s "$pdf_file" 2>/dev/null || echo "0")
  if [[ $pdf_size -lt 1024 ]]; then
  log_message "${RED}[ERROR] PDF file too small (${pdf_size} bytes)${NC}"
  return 1
  fi

  # Try to extract text from PDF to verify it's not corrupted
  if command -v pdfinfo &> /dev/null; then
  if pdfinfo "$pdf_file" &> /dev/null; then
  local pages=$(pdfinfo "$pdf_file" | grep "^Pages:" | awk '{print $2}')
  log_message "${GREEN}[OK] PDF generated successfully with $pages pages (${pdf_size} bytes)${NC}"
  else
  log_message "${RED}[ERROR] PDF appears to be corrupted${NC}"
  return 1
  fi
  else
  log_message "${GREEN}[OK] PDF generated (${pdf_size} bytes)${NC}"
  fi

  return 0
}

check_latex_guidelines() {
  log_message "${BLUE}Checking LaTeX formatting guidelines...${NC}"

  local issues=0

  # Check for common formatting issues
  if grep -r "\\usepackage.*{amsmath}" . --include="*.tex" &> /dev/null &&
  grep -r "\\usepackage.*{amssymb}" . --include="*.tex" &> /dev/null; then
  log_message "${GREEN}[OK] AMS packages properly included${NC}"
  else
  log_message "${YELLOW}[WARN] Consider including amsmath/amssymb packages${NC}"
  ((issues++))
  fi

  # Check for UTF-8 encoding
  if grep -r "\\usepackage.*{inputenc}" . --include="*.tex" &> /dev/null; then
  log_message "${GREEN}[OK] Input encoding specified${NC}"
  else
  log_message "${YELLOW}[WARN] Consider specifying input encoding${NC}"
  ((issues++))
  fi

  # Check for proper font encoding
  if grep -r "\\usepackage.*{fontenc}" . --include="*.tex" &> /dev/null; then
  log_message "${GREEN}[OK] Font encoding specified${NC}"
  else
  log_message "${YELLOW}[WARN] Consider specifying font encoding${NC}"
  ((issues++))
  fi

  # Check for language support
  if grep -r "\\usepackage.*{babel}" . --include="*.tex" &> /dev/null; then
  log_message "${GREEN}[OK] Language support (babel) included${NC}"
  else
  log_message "${YELLOW}[WARN] Consider including babel for language support${NC}"
  ((issues++))
  fi

  log_message "${BLUE}Formatting guideline issues found: $issues${NC}"

  # Return 0 regardless of issues count for guidelines (these are recommendations)
  return 0
}

main() {
  log_message "${GREEN}Starting CTMM LaTeX Build Process${NC}"
  log_message "Main file: $MAIN_FILE"

  # Check dependencies
  check_dependencies

  # Clean previous build artifacts
  rm -f "$BUILD_DIR"/*.aux "$BUILD_DIR"/*.log "$BUILD_DIR"/*.toc "$BUILD_DIR"/*.bbl "$BUILD_DIR"/*.blg "$BUILD_DIR"/*.out

  # First pdflatex pass
  if ! run_pdflatex 1; then
  log_message "${RED}Build failed on first pass${NC}"
  exit 1
  fi

  # Run BibTeX
  run_bibtex

  # Second pdflatex pass (for bibliography)
  if ! run_pdflatex 2; then
  log_message "${RED}Build failed on second pass${NC}"
  exit 1
  fi

  # Third pdflatex pass (for cross-references)
  if ! run_pdflatex 3; then
  log_message "${RED}Build failed on third pass${NC}"
  exit 1
  fi

  # Check PDF completeness
  if ! check_pdf_completeness; then
  log_message "${RED}PDF completeness check failed${NC}"
  exit 1
  fi

  # Check LaTeX guidelines
  check_latex_guidelines

  # Copy PDF to root for easy access
  local basename=$(basename "$MAIN_FILE" .tex)
  cp "$BUILD_DIR/$basename.pdf" "$basename.pdf"

  log_message "${GREEN}[OK] Build completed successfully!${NC}"
  log_message "PDF: $basename.pdf"
  log_message "Build log: $LOG_FILE"
  log_message "Error summary: $ERROR_SUMMARY"
  log_message "Warning summary: $WARNING_SUMMARY"

  # Return success since PDF was generated
  return 0
}

# Run main function
main "$@"
