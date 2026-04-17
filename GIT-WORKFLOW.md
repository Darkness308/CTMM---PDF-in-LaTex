# Git Workflow für CTMM-LaTeX-Projekt

Dieses Dokument beschreibt den Git-Workflow für die effiziente und nachvollziehbare Entwicklung des CTMM-LaTeX-Projekts.

## 1. Branch-Struktur

- `main` - Stabile, produktionsreife Version (immer lauffähig)
- `develop` - Integrationsebene für neue Features und Fixes
- Feature-Branches - Für die Entwicklung neuer Module oder größerer Änderungen
  - Format: `feature/name-des-features`
- Bugfix-Branches - Für die Behebung von Fehlern
  - Format: `fix/kurze-fehlerbeschreibung`

## 2. Commit-Richtlinien

Alle Commits sollten einer klaren Konvention folgen:

- `[FIX]` - Fehlerbehebung (z.B. LaTeX-Syntax-Korrekturen)
- `[ADD]` - Hinzufügen neuer Inhalte/Module
- `[UPD]` - Aktualisierung bestehender Inhalte
- `[DOC]` - Dokumentations-Updates
- `[REF]` - Code-Refactoring ohne Funktionsänderung
- `[STY]` - Styling/Layout-Änderungen

Beispiel: `[ADD] Neues Modul für Emotionsregulation hinzugefügt`

## 3. Issue-Tracking

- Für jede Aufgabe ein Issue erstellen
- Issues mit Labels versehen (z.B. `bug`, `enhancement`, `documentation`)
- Commits mit Issues verknüpfen durch Referenzierung in der Commit-Nachricht:
  - `[FIX] Korrektur von Underscore-Escaping in Formularen (Fixes #42)`

## 4. Pull-Request-Workflow

1. Feature-Branch von `develop` erstellen
2. Änderungen implementieren und committen
3. Pull Request von Feature-Branch nach `develop` erstellen
4. Code-Review durchführen
5. Nach erfolgreicher Review und Tests: Merge in `develop`
6. Regelmäßig (bei Meilensteinen): `develop` in `main` mergen

## 5. Release-Prozess

1. Release-Branch von `develop` erstellen (z.B. `release/v1.2.0`)
2. Finale Tests und Korrekturen im Release-Branch
3. Nach erfolgreichen Tests: Merge in `main` und `develop`
4. Tag mit Versionsnummer erstellen (z.B. `v1.2.0`)
5. PDF-Build erstellen und als Release-Artefakt veröffentlichen

## 6. Praktische Befehle

### Neues Feature beginnen
```bash
git checkout develop
git pull
git checkout -b feature/mein-neues-feature
```

### Änderungen committen
```bash
git add modules/mein-modul.tex
git commit -m "[ADD] Beschreibung der Änderung"
```

### Feature abschließen
```bash
git push -u origin feature/mein-neues-feature
# Dann PR auf GitHub erstellen
```

### Nach erfolgreichem Merge
```bash
git checkout develop
git pull
git branch -d feature/mein-neues-feature
```
