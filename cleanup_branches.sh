#!/bin/bash
# Branch Cleanup Script für CTMM Repository
# Ausführen mit: bash cleanup_branches.sh
#
# Dieses Script löscht alte/unbenutzte Branches:
# - Option A: 41 sichere Branches (gemergte + Test-Branches)
# - Option B: Alle restlichen ~376 copilot/fix-* Branches

set -e

echo "=========================================="
echo "  CTMM Branch Cleanup Script"
echo "=========================================="
echo ""

# Option A: Sichere Branches
echo "=== OPTION A: Lösche 41 sichere Branches ==="
echo ""

echo "--- 15 gemergte copilot/fix Branches ---"
MERGED_BRANCHES=(
  "copilot/fix-1182"
  "copilot/fix-1180"
  "copilot/fix-1177"
  "copilot/fix-1165"
  "copilot/fix-1157"
  "copilot/fix-1153"
  "copilot/fix-1149"
  "copilot/fix-1134"
  "copilot/fix-1132"
  "copilot/fix-1130"
  "copilot/fix-1128"
  "copilot/fix-1126"
  "copilot/fix-1124"
  "copilot/fix-1118"
  "copilot/fix-1110"
)

for branch in "${MERGED_BRANCHES[@]}"; do
  echo "Lösche $branch..."
  git push origin --delete "$branch" 2>/dev/null || echo "  [WARN]️  $branch existiert nicht oder bereits gelöscht"
done

echo ""
echo "--- 26 automated-merge-test Branches ---"
git fetch --prune origin
TEST_BRANCHES=$(git branch -r | grep 'origin/automated-merge-test-' | sed 's|origin/||' || true)
if [ -n "$TEST_BRANCHES" ]; then
  echo "$TEST_BRANCHES" | while read branch; do
  echo "Lösche $branch..."
  git push origin --delete "$branch" 2>/dev/null || echo "  [WARN]️  $branch bereits gelöscht"
  done
else
  echo "Keine automated-merge-test Branches gefunden."
fi

echo ""
echo "=== OPTION A abgeschlossen ==="
echo ""

# Option B: Alle restlichen copilot/fix-* Branches
read -p "Weiter mit Option B (ALLE restlichen copilot/fix-* löschen)? [y/N] " confirm
if [[ $confirm == [yY] || $confirm == [jJ] ]]; then
  echo ""
  echo "=== OPTION B: Lösche alle restlichen copilot/fix Branches ==="
  echo "[WARN]️  WARNUNG: Dies löscht ~376 Branches permanent!"
  read -p "Bist du sicher? [y/N] " confirm2

  if [[ $confirm2 == [yY] || $confirm2 == [jJ] ]]; then
  git fetch --prune origin
  REMAINING=$(git branch -r | grep 'origin/copilot/fix-' | sed 's|origin/||' || true)
  if [ -n "$REMAINING" ]; then
  COUNT=$(echo "$REMAINING" | wc -l)
  echo "Lösche $COUNT Branches..."
  echo "$REMAINING" | while read branch; do
  echo "  Lösche $branch..."
  git push origin --delete "$branch" 2>/dev/null || true
  done
  else
  echo "Keine copilot/fix-* Branches mehr vorhanden."
  fi
  echo "=== OPTION B abgeschlossen ==="
  else
  echo "Option B abgebrochen."
  fi
else
  echo "Option B übersprungen."
fi

echo ""
echo "=========================================="
echo "  Cleanup abgeschlossen!"
echo "=========================================="
echo ""
echo "Führe 'git fetch --prune' aus um lokale Referenzen zu aktualisieren."
