#!/bin/bash

# CTMM Module Generator Helper Script
# Vereinfacht die Erstellung neuer Module

echo " CTMM Module Generator"
echo "========================"

# Typ auswählen
echo "Welchen Modul-Typ möchten Sie erstellen?"
echo "1) Arbeitsblatt (arbeitsblatt)"
echo "2) Tool (tool)"  
echo "2) Tool (tool)"
echo "3) Notfallkarte (notfallkarte)"
echo ""
read -p "Wählen Sie (1-3): " choice

case $choice in
  1) type="arbeitsblatt";;
  2) type="tool";;
  3) type="notfallkarte";;
  *) echo "[FAIL] Ungültige Auswahl"; exit 1;;
esac

# Namen eingeben
echo ""
read -p "[NOTE] Wie soll das Modul heißen? " name

if [ -z "$name" ]; then
  echo "[FAIL] Name darf nicht leer sein"
  exit 1
fi

# Modul generieren
echo ""
echo "[SYNC] Erstelle Modul..."
node module-generator.js "$type" "$name"

# Erfolgsmeldung und nächste Schritte
if [ $? -eq 0 ]; then
  echo ""
  echo "[SUCCESS] Modul erfolgreich erstellt!"
  echo ""
  echo "[TEST] Nächste Schritte:"
  echo "1. Öffnen Sie main.tex"
  echo "2. Fügen Sie an der gewünschten Stelle ein:"
  
  # Dateiname generieren (vereinfacht)
  filename=$(echo "$name" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/-\+/-/g' | sed 's/^-\|-$//g')
  

  # Dateiname generieren (aus dem Modulnamen, ohne Leerzeichen und in Kleinbuchstaben)
  filename=$(echo "$name" | tr '[:upper:]' '[:lower:]' | sed 's/ /-/g')

  case $type in
  "arbeitsblatt") prefix="arbeitsblatt-";;
  "tool") prefix="tool-";;
  "notfallkarte") prefix="notfall-";;
  esac

  echo "  \\input{modules/${prefix}${filename}}"
  echo "3. Kompilieren Sie das Dokument"
  echo ""
  echo "[LINK] Das neue Modul liegt in: modules/${prefix}${filename}.tex"
fi
