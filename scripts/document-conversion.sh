#!/bin/bash
# Document Conversion Workflow for CTMM Project
# Converts .txt, .md, .docx, .markdown files to LaTeX format

set -e

# Configuration
CONVERSION_LOG="build/conversion-log.txt"
CONVERTED_DIR="converted"
INTEGRATION_FILE="converted/integrated-content.tex"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Initialize directories and logs
mkdir -p build "$CONVERTED_DIR"
echo "CTMM Document Conversion Log - $(date)" > "$CONVERSION_LOG"
echo "=======================================" >> "$CONVERSION_LOG"

log_message() {
  echo -e "$1" | tee -a "$CONVERSION_LOG"
}

check_dependencies() {
  log_message "${BLUE}Checking conversion dependencies...${NC}"
  
  if ! command -v pandoc &> /dev/null; then
  log_message "${RED}Error: pandoc not found${NC}"
  exit 1
  fi
  
  log_message "${GREEN}[OK] All dependencies found${NC}"
}

find_documents() {
  echo "Finding documents to convert..." >> "$CONVERSION_LOG"
  
  # Find all target documents
  local files=()
  while IFS= read -r -d '' file; do
  files+=("$file")
  done < <(find . -type f \( -name "*.txt" -o -name "*.md" -o -name "*.docx" -o -name "*.markdown" \) -not -path "./build/*" -not -path "./.git/*" -not -path "./converted/*" -print0)
  
  echo "Found ${#files[@]} documents to convert:" >> "$CONVERSION_LOG"
  for file in "${files[@]}"; do
  echo "  - $file" >> "$CONVERSION_LOG"
  done
  
  printf '%s\n' "${files[@]}"
}

sanitize_latex() {
  local input_file="$1"
  local temp_file="${input_file}.tmp"
  
  # Replace non-LaTeX compatible characters with LaTeX commands
  # NOTE: We do NOT escape backslashes here because pandoc already produces proper LaTeX
  # Escaping backslashes would break all LaTeX commands like \section, \textbf, etc.
  sed -e 's/&/\\&/g' \
  -e 's/%/\\%/g' \
  -e 's/\$/\\$/g' \
  -e 's/#/\\#/g' \
  -e 's/_/\\_/g' \
  -e 's/\^/\\textasciicircum{}/g' \
  -e 's/~/\\textasciitilde{}/g' \
  -e 's/"/``/g' \
  -e "s/'/'/g" \
  "$input_file" > "$temp_file"
  
  mv "$temp_file" "$input_file"
}

check_latex_syntax() {
  local tex_file="$1"
  local basename=$(basename "$tex_file" .tex)
  local check_dir="build/syntax-check"
  
  mkdir -p "$check_dir"
  
  log_message "${BLUE}Checking LaTeX syntax for $tex_file...${NC}"
  
  # Create a minimal document to test the converted content
  cat > "$check_dir/test-$basename.tex" << EOF
\\documentclass{article}
\\usepackage[T1]{fontenc}
\\usepackage[utf8]{inputenc}
\\usepackage[ngerman]{babel}
\\usepackage{hyperref}
\\usepackage{xcolor}
\\usepackage{tcolorbox}
\\begin{document}
\\input{../../$tex_file}
\\end{document}
EOF
  
  # Try to compile the test document
  cd "$check_dir"
  if pdflatex -interaction=nonstopmode "test-$basename.tex" >> "../../$CONVERSION_LOG" 2>&1; then
  cd ../..
  log_message "${GREEN}[OK] LaTeX syntax check passed for $tex_file${NC}"
  return 0
  else
  cd ../..
  log_message "${RED}[ERROR] LaTeX syntax errors found in $tex_file${NC}"
  
  # Extract errors from log
  if [[ -f "$check_dir/test-$basename.log" ]]; then
  grep "^!" "$check_dir/test-$basename.log" >> "$CONVERSION_LOG" || true
  fi
  
  return 1
  fi
}

convert_file() {
  local input_file="$1"
  local file_ext="${input_file##*.}"
  local basename=$(basename "$input_file" ".$file_ext")
  local output_file="$CONVERTED_DIR/${basename}.tex"
  
  log_message "${BLUE}Converting $input_file to LaTeX...${NC}"
  
  case "$file_ext" in
  "md"|"markdown")
  # Convert markdown to LaTeX
  if pandoc -f markdown -t latex --wrap=preserve "$input_file" -o "$output_file"; then
  log_message "${GREEN}[OK] Converted $input_file (Markdown)${NC}"
  else
  log_message "${RED}[ERROR] Failed to convert $input_file${NC}"
  return 1
  fi
  ;;
  "txt")
  # Convert plain text to LaTeX
  {
  echo "% Converted from $input_file"
  echo "\\section{$(basename "$input_file" .txt)}"
  echo "\\begin{verbatim}"
  cat "$input_file"
  echo "\\end{verbatim}"
  } > "$output_file"
  log_message "${GREEN}[OK] Converted $input_file (Plain Text)${NC}"
  ;;
  "docx")
  # Convert DOCX to LaTeX using pandoc
  if pandoc -f docx -t latex --wrap=preserve "$input_file" -o "$output_file"; then
  log_message "${GREEN}[OK] Converted $input_file (DOCX)${NC}"
  else
  log_message "${RED}[ERROR] Failed to convert $input_file${NC}"
  return 1
  fi
  ;;
  *)
  log_message "${YELLOW}[WARN] Unsupported file type: $file_ext${NC}"
  return 1
  ;;
  esac
  
  # Sanitize LaTeX special characters
  sanitize_latex "$output_file"
  
  # Check syntax
  if check_latex_syntax "$output_file"; then
  log_message "  → Output: $output_file"
  echo "$output_file" >> "build/converted-files.list"
  return 0
  else
  log_message "  → Syntax errors found, file may need manual review"
  echo "$output_file" >> "build/converted-files-with-errors.list"
  return 0  # Continue processing other files
  fi
}

create_integration_file() {
  log_message "${BLUE}Creating integration file...${NC}"
  
  {
  echo "% Integrated converted content - Generated $(date)"
  echo "% This file contains all converted documents"
  echo ""
  echo "\\part{Converted Documents}"
  echo ""
  } > "$INTEGRATION_FILE"
  
  # Add successfully converted files
  if [[ -f "build/converted-files.list" ]]; then
  while IFS= read -r tex_file; do
  local basename=$(basename "$tex_file" .tex)
  echo "\\section{$basename}" >> "$INTEGRATION_FILE"
  echo "\\input{../$tex_file}" >> "$INTEGRATION_FILE"
  echo "" >> "$INTEGRATION_FILE"
  done < "build/converted-files.list"
  fi
  
  log_message "${GREEN}[OK] Integration file created: $INTEGRATION_FILE${NC}"
}

generate_conversion_summary() {
  local total_files=0
  local successful_conversions=0
  local failed_conversions=0
  local files_with_errors=0
  
  # Count files
  if [[ -f "build/converted-files.list" ]]; then
  successful_conversions=$(wc -l < "build/converted-files.list")
  fi
  
  if [[ -f "build/converted-files-with-errors.list" ]]; then
  files_with_errors=$(wc -l < "build/converted-files-with-errors.list")
  fi
  
  total_files=$((successful_conversions + files_with_errors + failed_conversions))
  
  # Create summary
  {
  echo ""
  echo "CONVERSION SUMMARY"
  echo "=================="
  echo "Total files processed: $total_files"
  echo "Successful conversions: $successful_conversions"
  echo "Conversions with syntax errors: $files_with_errors"
  echo "Failed conversions: $failed_conversions"
  echo ""
  echo "Successfully converted files:"
  if [[ -f "build/converted-files.list" ]]; then
  while IFS= read -r file; do
  echo "  [OK] $file"
  done < "build/converted-files.list"
  fi
  echo ""
  echo "Files with syntax errors:"
  if [[ -f "build/converted-files-with-errors.list" ]]; then
  while IFS= read -r file; do
  echo "  [WARN] $file"
  done < "build/converted-files-with-errors.list"
  fi
  echo ""
  echo "Integration file: $INTEGRATION_FILE"
  echo ""
  } >> "$CONVERSION_LOG"
  
  log_message "${GREEN}Conversion Summary:${NC}"
  log_message "  Total files: $total_files"
  log_message "  Successful: $successful_conversions"
  log_message "  With errors: $files_with_errors"
  log_message "  Failed: $failed_conversions"
}

main() {
  log_message "${GREEN}Starting CTMM Document Conversion Workflow${NC}"
  
  # Check dependencies
  check_dependencies
  
  # Clean previous conversion results
  rm -f build/converted-files.list build/converted-files-with-errors.list
  rm -rf "$CONVERTED_DIR"
  mkdir -p "$CONVERTED_DIR"
  
  # Find all documents
  log_message "${BLUE}Scanning for documents to convert...${NC}"
  local files=()
  while IFS= read -r file; do
  [[ -n "$file" ]] && files+=("$file")
  done < <(find_documents)
  
  log_message "Found ${#files[@]} documents to convert"
  
  if [[ ${#files[@]} -eq 0 ]]; then
  log_message "${YELLOW}No documents found to convert${NC}"
  exit 0
  fi
  
  # Convert each file
  local conversion_errors=0
  for file in "${files[@]}"; do
  if ! convert_file "$file"; then
  ((conversion_errors++))
  log_message "${YELLOW}Continuing with next file...${NC}"
  fi
  done
  
  # Create integration file
  create_integration_file
  
  # Generate summary
  generate_conversion_summary
  
  log_message "${GREEN}[OK] Document conversion workflow completed${NC}"
  log_message "Conversion log: $CONVERSION_LOG"
  log_message "Converted files directory: $CONVERTED_DIR"
  log_message "Integration file: $INTEGRATION_FILE"
  
  if [[ $conversion_errors -gt 0 ]]; then
  log_message "${YELLOW}[WARN] $conversion_errors files had conversion issues${NC}"
  return 0  # Return success so workflow continues
  fi
}

# Run main function
main "$@"