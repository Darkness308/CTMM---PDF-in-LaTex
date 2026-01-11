#!/bin/bash
# PDF Quality Optimization Tool for CTMM Project
# Optimizes LaTeX code for better compilation and maintainability

set -e

# Configuration
BUILD_DIR="build"
OPTIMIZATION_DIR="$BUILD_DIR/optimization"
OPTIMIZATION_REPORT="$OPTIMIZATION_DIR/optimization-report.txt"
BACKUP_DIR="$OPTIMIZATION_DIR/backup"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Initialize directories
mkdir -p "$OPTIMIZATION_DIR" "$BACKUP_DIR"

log_message() {
    echo -e "$1" | tee -a "$OPTIMIZATION_REPORT"
}

backup_files() {
    log_message "${BLUE}Creating backup of original files...${NC}"

    # Backup all .tex files
    find . -name "*.tex" -not -path "./build/*" -not -path "./.git/*" | while read -r file; do
        local backup_path="$BACKUP_DIR/${file//\//_}"
        cp "$file" "$backup_path"
        log_message "  Backed up: $file → $backup_path"
    done

    log_message "${GREEN}✓ Backup completed${NC}"
}

analyze_package_usage() {
    log_message "${BLUE}Analyzing package usage...${NC}"

    local all_packages=()
    local used_commands=()
    local unused_packages=()

    # Find all usepackage declarations
    while IFS= read -r line; do
        if [[ $line =~ \\usepackage(\[[^\]]*\])?\{([^}]+)\} ]]; then
            local package="${BASH_REMATCH[2]}"
            all_packages+=("$package")
        fi
    done < <(find . -name "*.tex" -not -path "./build/*" -exec cat {} \;)

    {
        echo ""
        echo "PACKAGE USAGE ANALYSIS"
        echo "====================="
        echo ""
        echo "All packages found:"
    } >> "$OPTIMIZATION_REPORT"

    for package in $(printf '%s\n' "${all_packages[@]}" | sort -u); do
        echo "  - $package" >> "$OPTIMIZATION_REPORT"

        # Check if package commands are used
        local package_used=false
        case "$package" in
            "amsmath")
                if grep -r "\\equation\|\\align\|\\gather\|\\multline" . --include="*.tex" &>/dev/null; then
                    package_used=true
                fi
                ;;
            "amssymb")
                if grep -r "\\mathbb\|\\mathfrak\|\\mathcal" . --include="*.tex" &>/dev/null; then
                    package_used=true
                fi
                ;;
            "graphicx")
                if grep -r "\\includegraphics\|\\rotatebox\|\\scalebox" . --include="*.tex" &>/dev/null; then
                    package_used=true
                fi
                ;;
            "xcolor")
                if grep -r "\\textcolor\|\\colorbox\|\\definecolor" . --include="*.tex" &>/dev/null; then
                    package_used=true
                fi
                ;;
            "hyperref")
                if grep -r "\\href\|\\url\|\\hyperref" . --include="*.tex" &>/dev/null; then
                    package_used=true
                fi
                ;;
            "tcolorbox")
                if grep -r "\\begin{tcolorbox}\|\\tcbox\|\\newtcolorbox" . --include="*.tex" &>/dev/null; then
                    package_used=true
                fi
                ;;
            *)
                # For other packages, check if any commands with the package name exist
                if grep -r "\\$package" . --include="*.tex" &>/dev/null; then
                    package_used=true
                fi
                ;;
        esac

        if [[ $package_used == false ]]; then
            unused_packages+=("$package")
        fi
    done

    if [[ ${#unused_packages[@]} -gt 0 ]]; then
        {
            echo ""
            echo "POTENTIALLY UNUSED PACKAGES:"
            for package in "${unused_packages[@]}"; do
                echo "  ⚠ $package"
            done
        } >> "$OPTIMIZATION_REPORT"

        log_message "${YELLOW}Found ${#unused_packages[@]} potentially unused packages${NC}"
    else
        log_message "${GREEN}✓ All packages appear to be used${NC}"
    fi
}

find_duplicate_definitions() {
    log_message "${BLUE}Identifying duplicate definitions...${NC}"

    {
        echo ""
        echo "DUPLICATE DEFINITION ANALYSIS"
        echo "============================"
        echo ""
    } >> "$OPTIMIZATION_REPORT"

    # Look for duplicate \newcommand, \newenvironment, \def
    local duplicates_found=false

    # Find all definitions
    declare -A definitions

    while IFS= read -r line; do
        if [[ $line =~ \\newcommand\{\\([^}]+)\} ]] ||
           [[ $line =~ \\def\\([^{]+) ]] ||
           [[ $line =~ \\newenvironment\{([^}]+)\} ]]; then
            local def_name="${BASH_REMATCH[1]}"
            if [[ -n "${definitions[$def_name]}" ]]; then
                echo "  DUPLICATE: $def_name" >> "$OPTIMIZATION_REPORT"
                duplicates_found=true
            else
                definitions[$def_name]="$line"
            fi
        fi
    done < <(find . -name "*.tex" -not -path "./build/*" -exec grep -n "\\newcommand\|\\def\|\\newenvironment" {} \;)

    if [[ $duplicates_found == false ]]; then
        echo "  No duplicate definitions found." >> "$OPTIMIZATION_REPORT"
        log_message "${GREEN}✓ No duplicate definitions found${NC}"
    else
        log_message "${YELLOW}⚠ Duplicate definitions found - see report${NC}"
    fi
}

optimize_image_inclusion() {
    log_message "${BLUE}Analyzing image inclusion...${NC}"

    {
        echo ""
        echo "IMAGE INCLUSION OPTIMIZATION"
        echo "==========================="
        echo ""
    } >> "$OPTIMIZATION_REPORT"

    # Find all includegraphics commands
    local image_issues=()

    while IFS= read -r line; do
        if [[ $line =~ \\includegraphics ]]; then
            # Check for missing width/height specifications
            if [[ ! $line =~ width=|height=|scale= ]]; then
                image_issues+=("Missing size specification: $line")
            fi

            # Check for absolute paths
            if [[ $line =~ /[^}]+ ]]; then
                image_issues+=("Absolute path used: $line")
            fi
        fi
    done < <(find . -name "*.tex" -not -path "./build/*" -exec grep -n "\\includegraphics" {} \;)

    if [[ ${#image_issues[@]} -gt 0 ]]; then
        echo "Image inclusion suggestions:" >> "$OPTIMIZATION_REPORT"
        for issue in "${image_issues[@]}"; do
            echo "  ⚠ $issue" >> "$OPTIMIZATION_REPORT"
        done
        echo "" >> "$OPTIMIZATION_REPORT"
        echo "Recommendations:" >> "$OPTIMIZATION_REPORT"
        echo "- Always specify width or height for images" >> "$OPTIMIZATION_REPORT"
        echo "- Use relative paths for better portability" >> "$OPTIMIZATION_REPORT"
        echo "- Consider using \\textwidth or \\columnwidth for responsive sizing" >> "$OPTIMIZATION_REPORT"

        log_message "${YELLOW}Found ${#image_issues[@]} image inclusion issues${NC}"
    else
        echo "No image inclusion issues found." >> "$OPTIMIZATION_REPORT"
        log_message "${GREEN}✓ Image inclusion looks good${NC}"
    fi
}

analyze_formatting_consistency() {
    log_message "${BLUE}Analyzing formatting consistency...${NC}"

    {
        echo ""
        echo "FORMATTING CONSISTENCY ANALYSIS"
        echo "=============================="
        echo ""
    } >> "$OPTIMIZATION_REPORT"

    local consistency_issues=()

    # Check section formatting consistency
    local section_formats=()
    while IFS= read -r line; do
        if [[ $line =~ \\section\{.*\} ]]; then
            section_formats+=("$line")
        fi
    done < <(find . -name "*.tex" -not -path "./build/*" -exec grep "\\section{" {} \;)

    # Check for inconsistent spacing
    local spacing_issues=$(find . -name "*.tex" -not -path "./build/*" -exec grep -c "  \+" {} \; | grep -v ":0" | wc -l)

    if [[ $spacing_issues -gt 0 ]]; then
        consistency_issues+=("Inconsistent spacing found in $spacing_issues files")
    fi

    # Check for mixed quote styles
    local quote_issues=$(find . -name "*.tex" -not -path "./build/*" -exec grep -c "\".*\"" {} \; | grep -v ":0" | wc -l)

    if [[ $quote_issues -gt 0 ]]; then
        consistency_issues+=("Mixed quote styles found (use `` and '' for LaTeX)")
    fi

    if [[ ${#consistency_issues[@]} -gt 0 ]]; then
        echo "Formatting consistency issues:" >> "$OPTIMIZATION_REPORT"
        for issue in "${consistency_issues[@]}"; do
            echo "  ⚠ $issue" >> "$OPTIMIZATION_REPORT"
        done

        log_message "${YELLOW}Found ${#consistency_issues[@]} formatting consistency issues${NC}"
    else
        echo "Formatting appears consistent." >> "$OPTIMIZATION_REPORT"
        log_message "${GREEN}✓ Formatting consistency looks good${NC}"
    fi
}

identify_inefficient_code() {
    log_message "${BLUE}Identifying inefficient code sections...${NC}"

    {
        echo ""
        echo "CODE EFFICIENCY ANALYSIS"
        echo "======================="
        echo ""
    } >> "$OPTIMIZATION_REPORT"

    local efficiency_issues=()

    # Look for repeated code patterns
    while IFS= read -r line; do
        if [[ $line =~ \\begin\{center\}.*\\end\{center\} ]] &&
           [[ $(echo "$line" | wc -c) -lt 50 ]]; then
            efficiency_issues+=("Short center environment could use \\centering: $line")
        fi

        # Check for manual spacing instead of proper commands
        if [[ $line =~ \\\\\\$ ]]; then
            efficiency_issues+=("Manual line breaks found, consider proper paragraph breaks")
        fi

        # Check for hardcoded values that could be variables
        if [[ $line =~ [0-9]+pt ]] && [[ $(grep -c "$(echo "$line" | grep -o '[0-9]\+pt')" . -r --include="*.tex") -gt 3 ]]; then
            efficiency_issues+=("Repeated hardcoded values found, consider using variables")
        fi
    done < <(find . -name "*.tex" -not -path "./build/*" -exec cat {} \;)

    if [[ ${#efficiency_issues[@]} -gt 0 ]]; then
        echo "Code efficiency suggestions:" >> "$OPTIMIZATION_REPORT"
        for issue in "${efficiency_issues[@]}"; do
            echo "  ⚠ $issue" >> "$OPTIMIZATION_REPORT"
        done

        log_message "${YELLOW}Found ${#efficiency_issues[@]} efficiency issues${NC}"
    else
        echo "Code appears efficient." >> "$OPTIMIZATION_REPORT"
        log_message "${GREEN}✓ Code efficiency looks good${NC}"
    fi
}

suggest_structure_improvements() {
    log_message "${BLUE}Analyzing document structure...${NC}"

    {
        echo ""
        echo "DOCUMENT STRUCTURE ANALYSIS"
        echo "=========================="
        echo ""
    } >> "$OPTIMIZATION_REPORT"

    # Count files and suggest organization
    local tex_files=$(find . -name "*.tex" -not -path "./build/*" | wc -l)
    local module_files=$(find modules/ -name "*.tex" 2>/dev/null | wc -l || echo "0")

    echo "Document structure overview:" >> "$OPTIMIZATION_REPORT"
    echo "- Total .tex files: $tex_files" >> "$OPTIMIZATION_REPORT"
    echo "- Module files: $module_files" >> "$OPTIMIZATION_REPORT"
    echo "" >> "$OPTIMIZATION_REPORT"

    # Check for consistent file organization
    if [[ -d "modules" ]]; then
        echo "✓ Good: Using modules directory for organization" >> "$OPTIMIZATION_REPORT"
    else
        echo "⚠ Consider organizing content into modules/" >> "$OPTIMIZATION_REPORT"
    fi

    # Check for style files
    if [[ -d "style" ]]; then
        echo "✓ Good: Using style directory for custom styles" >> "$OPTIMIZATION_REPORT"
    else
        echo "⚠ Consider creating style/ directory for custom packages" >> "$OPTIMIZATION_REPORT"
    fi

    log_message "${GREEN}✓ Structure analysis completed${NC}"
}

create_optimization_summary() {
    log_message "${BLUE}Creating optimization summary...${NC}"

    {
        echo ""
        echo "OPTIMIZATION SUMMARY"
        echo "==================="
        echo "Analysis completed: $(date)"
        echo ""
        echo "Files analyzed:"
        find . -name "*.tex" -not -path "./build/*" | while read -r file; do
            echo "  - $file"
        done
        echo ""
        echo "Backup location: $BACKUP_DIR"
        echo "Report location: $OPTIMIZATION_REPORT"
        echo ""
        echo "RECOMMENDATIONS:"
        echo "1. Review unused packages and remove if not needed"
        echo "2. Fix any duplicate definitions found"
        echo "3. Optimize image inclusion for better performance"
        echo "4. Standardize formatting throughout the document"
        echo "5. Refactor inefficient code sections"
        echo "6. Improve document structure organization"
        echo ""
    } >> "$OPTIMIZATION_REPORT"

    log_message "${GREEN}Optimization Summary:${NC}"
    log_message "  Report: $OPTIMIZATION_REPORT"
    log_message "  Backup: $BACKUP_DIR"
    log_message "  Analysis covers package usage, duplicates, images, formatting, efficiency, and structure"
}

main() {
    {
        echo "CTMM LaTeX Optimization Report"
        echo "============================="
        echo "Started: $(date)"
        echo ""
    } > "$OPTIMIZATION_REPORT"

    log_message "${GREEN}Starting LaTeX Code Optimization Analysis${NC}"

    # Create backup of original files
    backup_files

    # Analyze package usage
    analyze_package_usage

    # Find duplicate definitions
    find_duplicate_definitions

    # Optimize image inclusion
    optimize_image_inclusion

    # Analyze formatting consistency
    analyze_formatting_consistency

    # Identify inefficient code
    identify_inefficient_code

    # Suggest structure improvements
    suggest_structure_improvements

    # Create summary
    create_optimization_summary

    log_message "${GREEN}✓ Optimization analysis completed${NC}"
    log_message "Results available in: $OPTIMIZATION_DIR"
}

# Run main function
main "$@"
