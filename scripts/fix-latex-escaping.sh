#!/bin/bash
# Fix LaTeX Over-Escaping Script
# Cleans up converted files that have excessive \textbackslash{} escaping

set -e

# Configuration
CONVERTED_DIR="converted"
BACKUP_DIR="converted-backup"
FIX_LOG="build/latex-escaping-fix.log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Initialize directories and logs
mkdir -p build "$BACKUP_DIR"
echo "LaTeX Over-Escaping Fix Log - $(date)" > "$FIX_LOG"
echo "=======================================" >> "$FIX_LOG"

log_message() {
    echo -e "$1" | tee -a "$FIX_LOG"
}

backup_files() {
    log_message "${BLUE}Creating backup of converted files...${NC}"
    
    if [ -d "$CONVERTED_DIR" ]; then
        cp -r "$CONVERTED_DIR" "$BACKUP_DIR"
        log_message "${GREEN}✓ Backup created in $BACKUP_DIR${NC}"
    else
        log_message "${YELLOW}No converted directory found${NC}"
        return 1
    fi
}

fix_over_escaping() {
    local file="$1"
    local basename=$(basename "$file")
    
    log_message "${BLUE}Fixing over-escaping in $basename...${NC}"
    
    # Create temporary file for processing
    local temp_file="${file}.fixing"
    cp "$file" "$temp_file"
    
    # Comprehensive fix for over-escaped LaTeX commands
    # 1. Fix \textbackslash{} + LaTeX command -> \LaTeX command
    sed -i 's/\\textbackslash{}\([a-zA-Z][a-zA-Z]*\)/\\\1/g' "$temp_file"
    
    # 2. Fix over-escaped braces and syntax
    sed -i 's/\\textbackslash{}{/{/g' "$temp_file"
    sed -i 's/\\textbackslash{}}}/}/g' "$temp_file"
    
    # 3. Fix line continuation patterns that got over-escaped
    sed -i 's/\\textbackslash{}\\textbackslash{}/\\\\/g' "$temp_file"
    
    # 4. Fix specific common LaTeX patterns that might remain
    sed -i 's/\\textbackslash{}\([^a-zA-Z{}]\)/\\\1/g' "$temp_file"
    
    # 5. Remove any remaining isolated \textbackslash{} that don't serve a purpose
    # This is more aggressive but necessary for cleanup
    sed -i 's/\\textbackslash{}//g' "$temp_file"
    
    # 6. Fix any double escaping that might have been created
    sed -i 's/\\\\\\/\\\\/g' "$temp_file"
    sed -i 's/\\\\{/{/g' "$temp_file"
    sed -i 's/\\\\}/}/g' "$temp_file"
    
    # Replace original file with fixed version
    mv "$temp_file" "$file"
    
    log_message "${GREEN}✓ Fixed $basename${NC}"
}

process_converted_files() {
    log_message "${BLUE}Processing converted files...${NC}"
    
    if [ ! -d "$CONVERTED_DIR" ]; then
        log_message "${RED}Error: $CONVERTED_DIR directory not found${NC}"
        return 1
    fi
    
    local count=0
    while IFS= read -r -d '' file; do
        if [[ "$file" == *.tex ]]; then
            fix_over_escaping "$file"
            ((count++))
        fi
    done < <(find "$CONVERTED_DIR" -type f -print0)
    
    log_message "${GREEN}✓ Processed $count LaTeX files${NC}"
}

verify_fix() {
    log_message "${BLUE}Verifying fixes...${NC}"
    
    local problematic_files=0
    while IFS= read -r -d '' file; do
        if [[ "$file" == *.tex ]]; then
            local over_escaped_count=$(grep -c "\\textbackslash{}" "$file" 2>/dev/null || echo 0)
            if [ "$over_escaped_count" -gt 0 ]; then
                log_message "${YELLOW}Warning: $file still has $over_escaped_count over-escaped sequences${NC}"
                ((problematic_files++))
            fi
        fi
    done < <(find "$CONVERTED_DIR" -type f -print0)
    
    if [ "$problematic_files" -eq 0 ]; then
        log_message "${GREEN}✓ All files appear to be fixed${NC}"
    else
        log_message "${YELLOW}⚠ $problematic_files files may need manual review${NC}"
    fi
}

# Main execution
log_message "${BLUE}Starting LaTeX over-escaping fix...${NC}"

if backup_files; then
    process_converted_files
    verify_fix
    log_message "${GREEN}✓ LaTeX over-escaping fix completed${NC}"
    log_message "${BLUE}Backup available in $BACKUP_DIR${NC}"
else
    log_message "${RED}✗ Fix aborted - no files to process${NC}"
    exit 1
fi