#!/bin/bash

# More comprehensive script to fix all remaining over-escaped patterns

echo "Applying comprehensive fix for over-escaped LaTeX commands..."

processed=0
fixed=0

for file in converted/*.tex; do
  if [[ -f "$file" ]]; then
  echo "Processing $file..."
  processed=$((processed + 1))

  # Create a backup
  cp "$file" "${file}.backup"

  # More comprehensive fixes
  # Fix remaining \textbackslash{} patterns at end of commands
  sed -i 's/\\textbackslash{}}}/}}}/g' "$file"
  sed -i 's/\\textbackslash{}}/}/g' "$file"
  sed -i 's/\\textbackslash{}\([^a-zA-Z]\)/\\\1/g' "$file"

  # Fix command arguments that got mangled
  sed -i 's/{\\textbackslash{}%/{%/g' "$file"
  sed -i 's/\\textbackslash{}%/\\%/g' "$file"

  # Fix braces that got separated by textbackslash
  sed -i 's/}\\textbackslash{}}/}}/g' "$file"
  sed -i 's/{\\textbackslash{}/{/g' "$file"

  # Fix common patterns like }\textbackslash{}} -> }}
  sed -i 's/}\\textbackslash{}}}/}}}/g' "$file"

  # Fix line endings with \textbackslash{}
  sed -i 's/\\textbackslash{}}$/}/g' "$file"

  # Fix special characters that got over-escaped
  sed -i 's/\\textbackslash{}\\textbackslash{}/\\\\/g' "$file"

  # Check if file was changed
  if ! cmp -s "$file" "${file}.backup"; then
  echo "  [OK] Applied additional fixes to $file"
  fixed=$((fixed + 1))
  rm "${file}.backup"
  else
  echo "  - No additional changes needed in $file"
  rm "${file}.backup"
  fi
  fi
done

echo ""
echo "Comprehensive fix summary:"
echo "  Files processed: $processed"
echo "  Files with additional fixes: $fixed"
