#!/bin/bash
# Script to fix PR #571 merge conflicts
# This script resolves the unrelated histories issue by merging main into the PR branch

set -e  # Exit on error

echo "=== PR #571 Merge Conflict Fix Script ==="
echo ""

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "Error: Not in a git repository root directory"
    exit 1
fi

# Fetch latest changes
echo "Step 1: Fetching latest changes from origin..."
git fetch origin

# Checkout the PR branch
echo "Step 2: Checking out PR branch (copilot/fix-237)..."
git checkout copilot/fix-237

# Verify we're on the correct branch
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "copilot/fix-237" ]; then
    echo "Error: Failed to checkout copilot/fix-237"
    exit 1
fi

echo "Step 3: Merging main into PR branch with theirs strategy..."
echo "This will accept main's version for all conflicting files..."

# Attempt the merge
if git merge --allow-unrelated-histories -s recursive -X theirs origin/main -m "Merge main into PR branch, accepting main's changes for conflicts"; then
    echo ""
    echo "✓ Merge successful!"
    echo ""
    echo "Step 4: Reviewing changes..."
    git log --oneline -3
    echo ""
    echo "Files changed:"
    git diff --stat HEAD~1
    echo ""
    echo "=== Next Steps ==="
    echo "1. Review the merge commit above"
    echo "2. If satisfied, push to update PR #571:"
    echo "   git push origin copilot/fix-237"
    echo ""
    echo "3. The PR should now be mergeable without conflicts"
    echo ""
else
    echo "Error: Merge failed"
    echo "Check the output above for details"
    exit 1
fi

echo "=== Fix Complete ==="
