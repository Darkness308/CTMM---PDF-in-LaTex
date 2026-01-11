#!/bin/bash

# LaTeX-Formularfeld-Fixer
# Dieses Script findet und korrigiert bekannte Probleme in LaTeX-Formularfeldern des CTMM-Projekts

# Farbdefinitionen
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}CTMM LaTeX-Formularfeld-Fixer${NC}"
echo "Scanne alle .tex-Dateien nach bekannten Problemen..."

# Problem 1: Underscores in Formularfeld-IDs
echo -e "${YELLOW}Problem 1: Nicht-escapte Underscores in Formularfeld-IDs${NC}"
find modules -name "*.tex" -type f | while read -r file; do
  # Suche nach ctmmTextField, ctmmTextArea, ctmmCheckBox mit Underscores in IDs
  if grep -q -E "ct(mm|mmm)(TextField|TextArea|CheckBox).*\{\}\{[^}]*_[^}]*\}" "$file"; then
  echo -e "${RED}Gefunden in $file${NC}"
  # Ersetze Underscores mit escapten Underscores in den IDs
  sed -i -E 's/(ct(mm|mmm)(TextField|TextArea|CheckBox).*\{\}\{[^}]*)_([^}]*\})/\1\\_\2/g' "$file"
  echo -e "${GREEN}Korrigiert: Underscores in IDs escapt${NC}"
  fi
done

# Problem 2: Tabularx mit fehlenden Definitionen
echo -e "${YELLOW}Problem 2: Probleme mit tabularx-Umgebungen${NC}"
find modules -name "*.tex" -type f | while read -r file; do
  # Prüfe auf tabularx, die besser als tabular formatiert werden sollten
  if grep -q -E "\\\\begin\{tabularx\}" "$file"; then
  echo -e "${RED}tabularx gefunden in $file - prüfe Struktur${NC}"
  # Für komplexere Ersetzungen wäre ein Python-Script besser,
  # aber für einfache Fälle kann sed verwendet werden
  if grep -q -E "\\\\begin\{tabularx\}.*\{\\\\textwidth\}" "$file"; then
  echo -e "${YELLOW}Überprüfe tabularx-Struktur in $file${NC}"
  fi
  fi
done

# Problem 3: Nicht geschlossene Umgebungen (center, etc.)
echo -e "${YELLOW}Problem 3: Nicht ordnungsgemäß geschlossene Umgebungen${NC}"
find modules -name "*.tex" -type f | while read -r file; do
  # Einfache Prüfung: Anzahl von \begin{...} sollte der Anzahl von \end{...} entsprechen
  begins=$(grep -c "\\\\begin{" "$file")
  ends=$(grep -c "\\\\end{" "$file")

  if [ "$begins" != "$ends" ]; then
  echo -e "${RED}Potentiell nicht geschlossene Umgebung in $file${NC}"
  echo -e "  Anzahl \\begin: $begins"
  echo -e "  Anzahl \\end: $ends"
  echo -e "${YELLOW}Bitte manuell überprüfen!${NC}"
  fi
done

# Problem 4: Prüfe auf doppelte Modulimporte
echo -e "${YELLOW}Problem 4: Doppelte Modulimporte in main.tex${NC}"
duplicates=$(grep -n "\\\\input{modules/" main.tex | sort | uniq -d -f 1)
if [ -n "$duplicates" ]; then
  echo -e "${RED}Doppelte Modulimporte gefunden:${NC}"
  echo "$duplicates"
  echo -e "${YELLOW}Bitte entfernen Sie die doppelten Importe!${NC}"
else
  echo -e "${GREEN}Keine doppelten Modulimporte gefunden.${NC}"
fi

echo -e "${GREEN}LaTeX-Formularfeld-Check abgeschlossen!${NC}"
echo "Weitere manuelle Überprüfung wird empfohlen für:"
echo "1. Komplexere tabularx-Strukturen"
echo "2. Verschachtelte Umgebungen"
echo "3. Spezielle Zeichenprobleme (Umlaute in Math-Umgebungen etc.)"
