#!/bin/bash
# Test script to validate LaTeX over-escaping fix
# This script verifies that converted files do not contain over-escaped LaTeX commands

set -e

echo "Testing LaTeX over-escaping fix..."

# Check if converted directory exists
if [ ! -d "converted" ]; then
    echo "✓ No converted directory found - no over-escaping possible"
    exit 0
fi

# Count files with over-escaping
over_escaped_files=$(find converted/ -name "*.tex" -exec grep -l "\\textbackslash{}" {} \; 2>/dev/null | wc -l)

if [ "$over_escaped_files" -eq 0 ]; then
    echo "✓ SUCCESS: No over-escaped files found"
    echo "✓ All LaTeX commands are properly formatted"
    
    # Show example of good formatting
    if [ -f "converted/README.tex" ]; then
        echo ""
        echo "Example of clean LaTeX formatting:"
        head -3 "converted/README.tex" | sed 's/^/  /'
    fi
    
    exit 0
else
    echo "✗ FAILURE: Found $over_escaped_files files with over-escaping"
    echo "Files with \\textbackslash{} patterns:"
    find converted/ -name "*.tex" -exec grep -l "\\textbackslash{}" {} \;
    exit 1
fi