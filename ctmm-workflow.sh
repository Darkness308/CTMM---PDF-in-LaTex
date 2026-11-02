#!/bin/bash

# CTMM Git-Workflow-Helper
# Dieses Script unterstützt bei der Umsetzung des Git-Workflows für das CTMM-LaTeX-Projekt

# Farbdefinitionen für Terminal-Ausgabe
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funktion zum Anzeigen von Hilfe
show_help() {
    echo -e "${BLUE}CTMM Git-Workflow-Helper${NC}"
    echo ""
    echo "Befehle:"
    echo -e "  ${GREEN}checkup${NC}         - Prüft Umgebungseinstellungen und Git-Konfiguration"
    echo -e "  ${GREEN}feature${NC} <name>   - Erstellt einen neuen Feature-Branch von develop"
    echo -e "  ${GREEN}fix${NC} <name>       - Erstellt einen neuen Bugfix-Branch von develop"
    echo -e "  ${GREEN}commit${NC} <typ> <nachricht> - Erzeugt einen formatieren Commit"
    echo -e "                  Typen: fix, add, upd, doc, ref, sty"
    echo -e "  ${GREEN}push${NC}            - Pusht den aktuellen Branch und zeigt URL für PR-Erstellung"
    echo -e "  ${GREEN}finish${NC}          - Wechselt zurück zu develop und aktualisiert"
    echo -e "  ${GREEN}build${NC}           - Baut das komplette PDF und zeigt das Ergebnis"
    echo -e "  ${GREEN}release${NC} <version> - Erstellt einen Release-Branch und erzeugt ein Tag"
    echo -e "  ${GREEN}fix-latex${NC}       - Korrigiert bekannte LaTeX-Formularfeld-Probleme"
    echo ""
    echo "Beispiele:"
    echo "  ./ctmm-workflow.sh feature neues-modul"
    echo "  ./ctmm-workflow.sh commit add \"Neues Modul für Emotionsregulation\""
}

# Funktion zum Erstellen eines Feature-Branches
create_feature() {
    if [ -z "$1" ]; then
        echo -e "${RED}Fehler: Bitte Feature-Name angeben${NC}"
        echo "Beispiel: ./ctmm-workflow.sh feature mein-feature"
        exit 1
    fi

    echo -e "${YELLOW}Wechsle zu develop und aktualisiere...${NC}"
    git checkout develop || git checkout -b develop
    git pull origin develop || true

    branch_name="feature/$1"
    echo -e "${YELLOW}Erstelle neuen Feature-Branch: $branch_name${NC}"
    git checkout -b "$branch_name"
    echo -e "${GREEN}Feature-Branch $branch_name erstellt. Du kannst jetzt mit der Entwicklung beginnen.${NC}"
}

# Funktion zum Erstellen eines Bugfix-Branches
create_fix() {
    if [ -z "$1" ]; then
        echo -e "${RED}Fehler: Bitte Bugfix-Name angeben${NC}"
        echo "Beispiel: ./ctmm-workflow.sh fix latex-underscore-escaping"
        exit 1
    fi

    echo -e "${YELLOW}Wechsle zu develop und aktualisiere...${NC}"
    git checkout develop || git checkout -b develop
    git pull origin develop || true

    branch_name="fix/$1"
    echo -e "${YELLOW}Erstelle neuen Bugfix-Branch: $branch_name${NC}"
    git checkout -b "$branch_name"
    echo -e "${GREEN}Bugfix-Branch $branch_name erstellt. Du kannst jetzt mit der Fehlerbehebung beginnen.${NC}"
}

# Funktion zum Erstellen eines formatierten Commits
create_commit() {
    if [ -z "$1" ] || [ -z "$2" ]; then
        echo -e "${RED}Fehler: Bitte Typ und Nachricht angeben${NC}"
        echo "Beispiel: ./ctmm-workflow.sh commit add \"Neues Modul für Emotionsregulation\""
        echo "Verfügbare Typen: fix, add, upd, doc, ref, sty"
        exit 1
    fi

    case "$1" in
        fix) prefix="[FIX]";;
        add) prefix="[ADD]";;
        upd) prefix="[UPD]";;
        doc) prefix="[DOC]";;
        ref) prefix="[REF]";;
        sty) prefix="[STY]";;
        *)
            echo -e "${RED}Fehler: Ungültiger Commit-Typ. Verwende: fix, add, upd, doc, ref, sty${NC}"
            exit 1
            ;;
    esac

    commit_msg="$prefix $2"
    echo -e "${YELLOW}Erstelle Commit: $commit_msg${NC}"
    git commit -m "$commit_msg"
    echo -e "${GREEN}Commit erstellt.${NC}"
}

# Funktion zum Pushen des aktuellen Branches
push_branch() {
    current_branch=$(git branch --show-current)
    echo -e "${YELLOW}Pushe aktuellen Branch: $current_branch${NC}"
    git push -u origin "$current_branch"

    # Repository-URL ermitteln
    remote_url=$(git remote get-url origin)
    repo_url=$(echo "$remote_url" | sed -e 's/^git@github.com:/https:\/\/github.com\//' -e 's/\.git$//' -e 's/^https:\/\/github.com\//https:\/\/github.com\//')

    echo -e "${GREEN}Branch wurde gepusht. PR erstellen:${NC}"
    echo -e "${BLUE}$repo_url/pull/new/$current_branch${NC}"
}

# Funktion zum Abschließen eines Features
finish_feature() {
    current_branch=$(git branch --show-current)
    echo -e "${YELLOW}Wechsle zu develop und aktualisiere...${NC}"
    git checkout develop || git checkout -b develop
    git pull origin develop || true

    echo -e "${YELLOW}Lösche lokalen Branch: $current_branch${NC}"
    git branch -d "$current_branch" || echo -e "${RED}Branch konnte nicht gelöscht werden. Möglicherweise wurden Änderungen noch nicht gemerged.${NC}"
    echo -e "${GREEN}Feature abgeschlossen. Du befindest dich jetzt im develop-Branch.${NC}"
}

# Funktion zum Bauen des Projekts
build_project() {
    echo -e "${YELLOW}Baue komplettes PDF...${NC}"
    mkdir -p build
    pdflatex -synctex=1 -interaction=nonstopmode -file-line-error -output-directory=build main.tex
    pdflatex -synctex=1 -interaction=nonstopmode -file-line-error -output-directory=build main.tex  # Zweiter Lauf für Referenzen

    if [ -f build/main.pdf ]; then
        echo -e "${GREEN}PDF erfolgreich erstellt: build/main.pdf${NC}"
        echo "Öffne PDF im Standardviewer..."
        xdg-open build/main.pdf || open build/main.pdf || start build/main.pdf || echo "PDF kann nicht automatisch geöffnet werden"
    else
        echo -e "${RED}Fehler beim Erstellen des PDFs.${NC}"
    fi
}

# Funktion zum Erstellen eines Release
create_release() {
    if [ -z "$1" ]; then
        echo -e "${RED}Fehler: Bitte Version angeben${NC}"
        echo "Beispiel: ./ctmm-workflow.sh release 1.2.0"
        exit 1
    fi

    version="v$1"

    echo -e "${YELLOW}Wechsle zu develop und aktualisiere...${NC}"
    git checkout develop || git checkout -b develop
    git pull origin develop || true

    branch_name="release/$version"
    echo -e "${YELLOW}Erstelle neuen Release-Branch: $branch_name${NC}"
    git checkout -b "$branch_name"

    # Build erstellen und Versionsnummer setzen
    echo -e "${YELLOW}Aktualisiere Version...${NC}"
    echo "$version" > VERSION
    git add VERSION
    git commit -m "[REL] Version $version vorbereiten"

    echo -e "${GREEN}Release-Branch $branch_name erstellt.${NC}"
    echo -e "${BLUE}Nächste Schritte:${NC}"
    echo "1. Führe Tests durch"
    echo "2. Merge in main: git checkout main && git merge $branch_name"
    echo "3. Erstelle Tag: git tag $version"
    echo "4. Pushe alles: git push origin main && git push origin $version"
    echo "5. Merge zurück in develop: git checkout develop && git merge $branch_name"
}

# Funktion zur Überprüfung der Umgebungseinstellungen
check_environment() {
    echo -e "${YELLOW}Überprüfe Git-Konfiguration...${NC}"

    # Git-Konfiguration überprüfen
    git_user=$(git config --get user.name)
    git_email=$(git config --get user.email)

    if [ -z "$git_user" ] || [ -z "$git_email" ]; then
        echo -e "${RED}Git-Benutzer nicht vollständig konfiguriert!${NC}"
        echo "Bitte konfigurieren Sie Git mit folgenden Befehlen:"
        echo "  git config --global user.name \"Dein Name\""
        echo "  git config --global user.email \"deine.email@beispiel.de\""
    else
        echo -e "${GREEN}Git-Benutzer konfiguriert als: $git_user <$git_email>${NC}"
    fi

    # Branch-Struktur überprüfen
    echo -e "${YELLOW}Überprüfe Branch-Struktur...${NC}"
    if ! git rev-parse --verify develop &>/dev/null; then
        echo -e "${RED}Develop-Branch existiert nicht!${NC}"
        echo -e "Möchten Sie einen develop-Branch erstellen? [j/n] "
        read -r answer
        if [[ "$answer" =~ ^[Jj] ]]; then
            git checkout -b develop
            echo -e "${GREEN}Develop-Branch erstellt.${NC}"
        fi
    else
        echo -e "${GREEN}Develop-Branch existiert.${NC}"
    fi

    # LaTeX-Umgebung überprüfen
    echo -e "${YELLOW}Überprüfe LaTeX-Umgebung...${NC}"
    if command -v pdflatex &>/dev/null; then
        echo -e "${GREEN}pdflatex ist installiert.${NC}"

        # Verzeichnisstruktur prüfen
        for dir in "build" "modules" "style"; do
            if [ ! -d "$dir" ]; then
                echo -e "${RED}Verzeichnis $dir fehlt.${NC}"
                mkdir -p "$dir"
                echo -e "${GREEN}Verzeichnis $dir erstellt.${NC}"
            else
                echo -e "${GREEN}Verzeichnis $dir existiert.${NC}"
            fi
        done
    else
        echo -e "${RED}pdflatex ist nicht installiert!${NC}"
        echo "Bitte installieren Sie TeX Live oder eine vergleichbare LaTeX-Distribution."
    fi
}

# Funktion zum Korrigieren von LaTeX-Formularfeldern
fix_latex_fields() {
    echo -e "${YELLOW}Korrigiere LaTeX-Formularfelder...${NC}"

    # Zähler für gefundene und korrigierte Fehler
    found=0
    fixed=0

    # Suche nach Formularfeldern mit Underscores ohne Escape
    echo -e "${YELLOW}Suche nach nicht-escapten Underscores in Formularfeldern...${NC}"
    files=$(find modules -name "*.tex" -type f)

    for file in $files; do
        # Suche nach Mustern wie {name_id} und ersetze sie mit {name\_id}
        while IFS= read -r line; do
            if [[ "$line" =~ ctmmTextField|ctmmTextArea|ctmmCheckBox ]]; then
                if [[ "$line" =~ \{\}\{[^}]*_[^}]*\} ]]; then
                    found=$((found+1))
                    echo -e "${YELLOW}Gefunden in $file:${NC} $line"

                    # Ersetzt Underscores innerhalb von {}
                    fixed_line=$(echo "$line" | sed -E 's/(\{\}\{[^}]*)_([^}]*\})/\1\\_\2/g')
                    sed -i "s/$line/$fixed_line/" "$file" && fixed=$((fixed+1))
                fi
            fi
        done < "$file"
    done

    echo -e "${GREEN}Formularfeld-Überprüfung abgeschlossen:${NC}"
    echo "Gefundene Probleme: $found"
    echo "Korrigierte Probleme: $fixed"
}

# Hauptlogik
case "$1" in
    checkup)
        check_environment
        ;;
    feature)
        create_feature "$2"
        ;;
    fix)
        create_fix "$2"
        ;;
    commit)
        create_commit "$2" "$3"
        ;;
    push)
        push_branch
        ;;
    finish)
        finish_feature
        ;;
    build)
        build_project
        ;;
    release)
        create_release "$2"
        ;;
    fix-latex)
        fix_latex_fields
        ;;
    *)
        show_help
        ;;
esac
