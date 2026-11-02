#!/bin/bash

# Script to fix over-escaped LaTeX commands in converted files
# Fixes patterns like \textbackslash{}section\textbackslash{} -> \section

echo "Fixing over-escaped LaTeX commands in converted files..."

# Counter for processed files
processed=0
fixed=0

# Process each .tex file in the converted directory
for file in converted/*.tex; do
  if [[ -f "$file" ]]; then
  echo "Processing $file..."
  processed=$((processed + 1))
  
  # Create a backup
  cp "$file" "${file}.backup"
  
  # Apply fixes using sed
  # Fix basic LaTeX commands
  sed -i 's/\\textbackslash{}section\\textbackslash{}/\\section/g' "$file"
  sed -i 's/\\textbackslash{}subsection\\textbackslash{}/\\subsection/g' "$file"
  sed -i 's/\\textbackslash{}textbf\\textbackslash{}/\\textbf/g' "$file"
  sed -i 's/\\textbackslash{}textit\\textbackslash{}/\\textit/g' "$file"
  sed -i 's/\\textbackslash{}emph\\textbackslash{}/\\emph/g' "$file"
  sed -i 's/\\textbackslash{}ul\\textbackslash{}/\\ul/g' "$file"
  sed -i 's/\\textbackslash{}begin\\textbackslash{}/\\begin/g' "$file"
  sed -i 's/\\textbackslash{}end\\textbackslash{}/\\end/g' "$file"
  sed -i 's/\\textbackslash{}item\\textbackslash{}/\\item/g' "$file"
  sed -i 's/\\textbackslash{}label\\textbackslash{}/\\label/g' "$file"
  sed -i 's/\\textbackslash{}hypertarget\\textbackslash{}/\\hypertarget/g' "$file"
  sed -i 's/\\textbackslash{}texorpdfstring\\textbackslash{}/\\texorpdfstring/g' "$file"
  sed -i 's/\\textbackslash{}texttt\\textbackslash{}/\\texttt/g' "$file"
  sed -i 's/\\textbackslash{}tightlist\\textbackslash{}/\\tightlist/g' "$file"
  sed -i 's/\\textbackslash{}arabic\\textbackslash{}/\\arabic/g' "$file"
  sed -i 's/\\textbackslash{}labelenumi\\textbackslash{}/\\labelenumi/g' "$file"
  sed -i 's/\\textbackslash{}def\\textbackslash{}/\\def/g' "$file"
  
  # Fix over-escaped braces
  sed -i 's/\\textbackslash{}{\([^}]*\)\\textbackslash{}}/{\1}/g' "$file"
  
  # Fix remaining patterns where \textbackslash{} appears before LaTeX commands
  sed -i 's/\\textbackslash{}\([a-zA-Z][a-zA-Z]*\)/\\\1/g' "$file"
  
  # Check if file was changed
  if ! cmp -s "$file" "${file}.backup"; then
  echo "  [OK] Fixed over-escaping in $file"
  fixed=$((fixed + 1))
  rm "${file}.backup"
  else
  echo "  - No changes needed in $file"
  rm "${file}.backup"
  fi
  fi
done

echo ""
echo "Summary:"
echo "  Files processed: $processed"
echo "  Files fixed: $fixed"
echo "  Files unchanged: $((processed - fixed))"