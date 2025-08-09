#!/bin/bash
# CTMM Workspace Cleanup Script
# Removes generated files and directories that could cause git conflicts

echo "🧹 Cleaning CTMM workspace..."

# Remove conversion directories that might be generated during processing
echo "Removing conversion directories..."
rm -rf converted/ converted_files/ processed/ || true

# Clean LaTeX auxiliary files (already in .gitignore but good to clean)
echo "Removing LaTeX auxiliary files..."
rm -f *.aux *.lof *.log *.lot *.fls *.out *.toc *.fmt *.fot *.cb *.cb2 .*.lb || true

# Clean CTMM build system temporary files
echo "Removing CTMM build system files..."
rm -f build_system.log build_report.md build_error_*.log main_basic_test.* *.temp.* *.test_*.* || true

# Clean Python cache
echo "Removing Python cache..."
rm -rf __pycache__/ || true
find . -name "*.pyc" -delete || true
find . -name "*.pyo" -delete || true

# Clean any git-ignored files (use carefully!)
if [ "$1" = "--deep" ]; then
    echo "Performing deep clean (removing all git-ignored files)..."
    git clean -fdX || true
fi

echo "✅ Workspace cleanup complete!"
echo ""
echo "💡 Usage:"
echo "  ./scripts/cleanup-workspace.sh          # Standard cleanup"
echo "  ./scripts/cleanup-workspace.sh --deep   # Deep clean (removes all git-ignored files)"