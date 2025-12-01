# Git Workflow für Claude Code

Best Practices für Version Control mit GitHub - optimiert für KI-gestützte Entwicklung.

---

## 🎯 Grundregel

**IMMER Branches für neue Features, Bugfixes und Änderungen erstellen!**

**NIEMALS direkt auf `main` committen!** (außer bei Hotfixes oder Dokumentation)

---

## 📋 Branch-Naming Convention

### Format
```
<typ>/<kurze-beschreibung>
```

### Typen

| Typ | Verwendung | Beispiel |
|-----|------------|----------|
| `feature/` | Neue Features | `feature/totp-support` |
| `fix/` | Bugfixes | `fix/destructor-exception-handling` |
| `refactor/` | Code-Refactoring | `refactor/database-singletons` |
| `docs/` | Dokumentation | `docs/update-readme` |
| `test/` | Tests hinzufügen/ändern | `test/encryption-coverage` |
| `chore/` | Dependencies, Config | `chore/update-pyqt6` |
| `hotfix/` | Kritische Fixes (direkt auf main) | `hotfix/security-vulnerability` |

### Beispiele für gute Branch-Namen
```bash
feature/category-multi-filter
fix/ui-layout-dialog-overlap
refactor/remove-old-database-code
docs/add-architecture-diagrams
test/password-generator-edge-cases
chore/setup-github-actions
```

---

## 🔄 Standard-Workflow

### 1. Feature/Fix starten

```bash
# Status prüfen
git status

# Aktuellen Stand holen
git pull origin main

# Neuen Branch erstellen
git checkout -b feature/mein-feature

# Oder für Bugfix
git checkout -b fix/bug-beschreibung
```

**Als Claude:**
```
Ich erstelle einen neuen Branch für dieses Feature:
git checkout -b feature/passwort-export
```

---

### 2. Entwickeln & Committen

#### Commit-Häufigkeit

**Committe regelmäßig bei:**
- ✅ Abgeschlossenen Teil-Features
- ✅ Funktionierenden Zwischenständen
- ✅ Vor größeren Refactorings
- ✅ Nach erfolgreichen Tests

**NICHT committen bei:**
- ❌ Code kompiliert/läuft nicht
- ❌ Tests schlagen fehl (außer du markierst es als WIP)
- ❌ Unvollständigen Gedanken

#### Commit-Message Format

```
<typ>: <Kurzbeschreibung in Imperativ>

<Optionaler Body mit Details>
<Was wurde geändert und warum>

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
```

**Typen für Commit-Messages:**
- `feat:` - Neues Feature
- `fix:` - Bugfix
- `refactor:` - Code-Umstrukturierung
- `test:` - Tests hinzufügen/ändern
- `docs:` - Dokumentation
- `style:` - Formatierung, keine Code-Änderung
- `chore:` - Wartung, Dependencies

**Beispiele:**

```bash
# Guter Commit
git commit -m "feat: Füge TOTP 2FA Unterstützung hinzu

- Implementiere TOTP-Generator mit pyotp
- Füge UI-Dialog für QR-Code Scan hinzu
- Verschlüssele TOTP-Secrets in Datenbank
- Teste mit Google Authenticator

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"

# Kurzer Commit (auch ok)
git commit -m "fix: Behebe Exception-Handling in database.py Destruktor

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### 3. Mehrere Commits während der Entwicklung

**Beispiel-Session:**

```bash
# Commit 1: Grundstruktur
git add src/totp/
git commit -m "feat: Erstelle TOTP-Modul Grundstruktur

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"

# Commit 2: UI
git add src/gui/totp_dialog.py
git commit -m "feat: Füge TOTP-Setup Dialog hinzu

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"

# Commit 3: Tests
git add tests/test_totp.py
git commit -m "test: Füge TOTP-Generator Tests hinzu

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"

# Commit 4: Integration
git add src/gui/entry_dialog.py src/core/database.py
git commit -m "feat: Integriere TOTP in Passwort-Einträge

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### 4. Branch pushen

```bash
# Ersten Push (erstellt Remote-Branch)
git push -u origin feature/mein-feature

# Weitere Pushes
git push
```

**Als Claude:**
```
Ich pushe den Branch jetzt:
git push -u origin feature/passwort-export
```

---

### 5. Pull Request erstellen

```bash
# Mit GitHub CLI (bevorzugt)
gh pr create --title "Feature: Passwort-Export" --body "$(cat <<'EOF'
## Zusammenfassung
- Fügt CSV/JSON Export hinzu
- Verschlüsselte Exporte optional
- CLI und GUI Unterstützung

## Änderungen
- Neues Modul: src/export/
- UI: Export-Dialog
- Tests: 95% Coverage

## Test-Plan
- [x] CSV Export getestet
- [x] JSON Export getestet
- [x] Verschlüsselung funktioniert
- [x] Alle Tests passing

🤖 Generated with Claude Code
EOF
)"
```

**Oder GitHub Web-UI:**
1. Gehe zu GitHub Repository
2. "Compare & pull request" Button
3. Fülle Titel und Beschreibung aus
4. Erstelle PR

---

## 🎨 Workflow für verschiedene Szenarien

### Szenario 1: Neues Feature

```bash
# 1. Branch erstellen
git checkout -b feature/dark-mode-improvements

# 2. Feature entwickeln + committen (mehrere Commits ok)
# ... Code ändern ...
git add src/gui/themes.py
git commit -m "feat: Füge Auto-Dark-Mode basierend auf Systemzeit hinzu"

# ... mehr Code ...
git add src/gui/settings_dialog.py
git commit -m "feat: Füge Dark-Mode Einstellungen in Settings hinzu"

# 3. Tests schreiben
git add tests/test_themes.py
git commit -m "test: Füge Theme-Tests hinzu"

# 4. Pushen
git push -u origin feature/dark-mode-improvements

# 5. PR erstellen
gh pr create --title "Feature: Verbesserte Dark-Mode Optionen"
```

**Als Claude-Workflow:**
1. Erstelle Branch
2. Entwickle Feature in logischen Schritten
3. Committe jeden abgeschlossenen Schritt
4. Pushe am Ende
5. Erstelle PR mit Zusammenfassung

---

### Szenario 2: Bugfix

```bash
# 1. Branch erstellen (von main)
git checkout main
git pull
git checkout -b fix/destructor-exception

# 2. Bug fixen
git add src/core/database.py
git commit -m "fix: Verbessere Exception-Handling in DatabaseManager Destruktor

- Füge spezifisches Exception-Handling hinzu
- Logge Fehler statt stillem Ignorieren
- Stelle sicher dass temp-Dateien gelöscht werden

Fixes #42

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"

# 3. Tests hinzufügen
git add tests/test_database.py
git commit -m "test: Füge Tests für Destruktor-Error-Handling hinzu"

# 4. Pushen und PR
git push -u origin fix/destructor-exception
gh pr create --title "Fix: Destruktor Exception-Handling" --body "Behebt #42"
```

---

### Szenario 3: Mehrere Issues gleichzeitig (NICHT EMPFOHLEN)

**❌ FALSCH:**
```bash
git checkout -b fix/multiple-fixes
# Fix für Issue 1, 2, 3, 4 alle zusammen...
```

**✅ RICHTIG:**
```bash
# Ein Branch pro Issue
git checkout -b fix/issue-42-destructor
# ... fix ...
git push -u origin fix/issue-42-destructor

git checkout main
git checkout -b fix/issue-43-layout
# ... fix ...
git push -u origin fix/issue-43-layout
```

**Grund:** Kleinere PRs sind einfacher zu reviewen und zu mergen.

---

### Szenario 4: Hotfix (kritischer Bug in Production)

```bash
# Direkt von main
git checkout main
git pull

# Hotfix-Branch
git checkout -b hotfix/security-password-leak

# Fix so schnell wie möglich
git add src/core/encryption.py
git commit -m "hotfix: Behebe kritische Sicherheitslücke bei Passwort-Anzeige

KRITISCH: Passwörter wurden in Logs geschrieben.
Entferne alle Debug-Print-Statements.

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"

# Sofort pushen und mergen
git push -u origin hotfix/security-password-leak
gh pr create --title "HOTFIX: Sicherheitslücke" --body "Kritischer Security-Fix"

# Nach Merge: Zurück zu main
git checkout main
git pull
```

---

### Szenario 5: Experimentelles Feature (unsicher ob es funktioniert)

```bash
# Branch mit "experiment/" Prefix
git checkout -b experiment/neural-password-strength

# Experimentieren...
git add src/password/ai_strength.py
git commit -m "experiment: Teste neuronales Netz für Passwort-Stärke

WIP - noch nicht produktionsreif

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"

# Pushen für Backup
git push -u origin experiment/neural-password-strength

# Falls es nicht funktioniert: Branch einfach löschen
git branch -D experiment/neural-password-strength
git push origin --delete experiment/neural-password-strength
```

---

## 📝 Commit-Strategie als Claude

### Wann committen?

**Nach jedem logischen Schritt:**
1. ✅ Neues Modul erstellt → Commit
2. ✅ UI-Komponente hinzugefügt → Commit
3. ✅ Integration abgeschlossen → Commit
4. ✅ Tests geschrieben → Commit
5. ✅ Dokumentation aktualisiert → Commit

**Beispiel-Session (Claude-Perspektive):**

```
BENUTZER: Füge einen Export-Feature hinzu.

CLAUDE:
Ich erstelle einen neuen Branch:
[git checkout -b feature/password-export]

Schritt 1: Erstelle Export-Modul
[... Code schreiben ...]
[git add src/export/ && git commit -m "feat: Erstelle Export-Modul Grundstruktur"]

Schritt 2: Füge CSV-Export hinzu
[... Code schreiben ...]
[git add src/export/csv_exporter.py && git commit -m "feat: Implementiere CSV-Export"]

Schritt 3: Füge UI-Dialog hinzu
[... Code schreiben ...]
[git add src/gui/export_dialog.py && git commit -m "feat: Füge Export-Dialog hinzu"]

Schritt 4: Tests schreiben
[... Tests schreiben ...]
[git add tests/test_export.py && git commit -m "test: Füge Export-Tests hinzu"]

Alle Schritte abgeschlossen! Pushe Branch:
[git push -u origin feature/password-export]

Erstelle Pull Request:
[gh pr create ...]

Feature ist bereit für Review! 🎉
```

---

## 🔍 Code-Review Checkliste (für PR-Beschreibung)

```markdown
## Zusammenfassung
[Kurze Beschreibung der Änderungen]

## Änderungen
- [ ] Neue Dateien: [Liste]
- [ ] Geänderte Dateien: [Liste]
- [ ] Gelöschte Dateien: [Liste]

## Tests
- [ ] Unit-Tests hinzugefügt
- [ ] Alle Tests passing (`pytest`)
- [ ] Manuell getestet

## Sicherheit
- [ ] Keine neuen Sicherheitslücken
- [ ] Sensible Daten verschlüsselt
- [ ] Input-Validierung vorhanden

## Dokumentation
- [ ] Code-Kommentare hinzugefügt
- [ ] Wissensdatenbank aktualisiert (falls nötig)
- [ ] README aktualisiert (falls nötig)

## Screenshots (falls UI-Änderungen)
[Bilder einfügen]

🤖 Generated with Claude Code
```

---

## 🚫 Was NICHT tun

### ❌ NIEMALS:

1. **Direkt auf main committen** (außer Hotfixes)
   ```bash
   git checkout main
   git commit -m "quick fix"  # ❌ FALSCH!
   ```

2. **Große Commits mit vielen unrelated Änderungen**
   ```bash
   git add .
   git commit -m "fixed stuff"  # ❌ FALSCH!
   ```

3. **Secrets committen**
   ```bash
   git add .env
   git add credentials.json  # ❌ NIEMALS!
   ```

4. **Force-Push auf main**
   ```bash
   git push --force origin main  # ❌ KATASTROPHE!
   ```

5. **Commits ohne Message**
   ```bash
   git commit -m "."  # ❌ Nutzlos!
   ```

6. **Branches nicht löschen nach Merge**
   ```bash
   # Nach PR-Merge:
   git branch -d feature/mein-feature  # ✅ Aufräumen!
   ```

---

## 🎯 Branch-Lifecycle

```
1. CREATE
   git checkout -b feature/xyz

2. DEVELOP
   [Multiple commits]

3. PUSH
   git push -u origin feature/xyz

4. PR
   gh pr create

5. REVIEW
   [Code-Review, Änderungen, weitere Commits]

6. MERGE
   [PR wird gemerged]

7. CLEANUP
   git checkout main
   git pull
   git branch -d feature/xyz
   git remote prune origin
```

---

## 📊 Wann Branches mergen?

### Main Branch
- **Nur Production-Ready Code**
- **Alle Tests müssen passing sein**
- **Code-Review abgeschlossen**
- **Keine Breaking Changes** (außer mit Major-Version)

### Develop Branch (falls vorhanden)
- Integration-Branch für Features
- Staging für Testing
- Wird regelmäßig in main gemerged

---

## 🤖 Claude-Spezifische Best Practices

### 1. Branch-Name im Kontext behalten
```
CLAUDE: Ich arbeite auf Branch feature/totp-support.
        Alle folgenden Commits werden dort gemacht.
```

### 2. Commit-Zusammenfassung am Ende
```
CLAUDE: Ich habe 4 Commits erstellt:
        1. feat: TOTP-Modul erstellt
        2. feat: UI-Dialog hinzugefügt
        3. test: Tests geschrieben
        4. docs: README aktualisiert

        Branch ist bereit für PR!
```

### 3. Konflikt-Handling
```
CLAUDE: Es gibt Merge-Konflikte mit main.
        Soll ich:
        1. main in Branch mergen (git merge main)
        2. Branch auf main rebasen (git rebase main)
        3. Dich manuell lösen lassen

        Empfehlung: Option 1 (Merge) ist sicherer.
```

### 4. Branch-Status transparent machen
```
CLAUDE: Aktueller Branch: feature/export
        Commits ahead of main: 3
        Status: Alle Tests passing ✅
        Bereit für: Pull Request
```

---

## 📚 Wissensdatenbank aktualisieren

**Nach größeren Features:**

```bash
# Wissensdatenbank auf separatem Branch updaten
git checkout -b docs/update-knowledge-base

# Dateien aktualisieren
# - .claude/knowledge-base.md
# - .claude/SESSION_LOG.md

git add .claude/
git commit -m "docs: Aktualisiere Wissensdatenbank nach TOTP-Feature

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"

git push -u origin docs/update-knowledge-base
gh pr create --title "Docs: Update Wissensdatenbank"
```

**Oder direkt auf main** (bei reinen Docs-Änderungen):
```bash
git checkout main
git pull
git add .claude/SESSION_LOG.md
git commit -m "docs: Update SESSION_LOG mit neuem Feature"
git push
```

---

## 🎓 Zusammenfassung

### Goldene Regeln:

1. ✅ **Immer Branches** für Features/Fixes
2. ✅ **Kleine, logische Commits** mit guten Messages
3. ✅ **Regelmäßig pushen** (Backup!)
4. ✅ **PRs für alle Merges** in main
5. ✅ **Tests vor Push** ausführen
6. ✅ **Branch-Namen aussagekräftig**
7. ✅ **Nach Merge aufräumen** (Branches löschen)

### Typischer Claude-Workflow:

```bash
1. git checkout -b feature/xyz        # Branch erstellen
2. [Entwickeln + Committen] x N       # Mehrere Commits
3. git push -u origin feature/xyz     # Pushen
4. gh pr create                       # PR erstellen
5. [Merge von Maintainer]             # Warten auf Merge
6. git checkout main && git pull      # Zurück zu main
7. git branch -d feature/xyz          # Cleanup
```

---

**Letzte Aktualisierung**: 2025-12-01
**Gilt für**: Alle Claude Code Sessions

**Bei Fragen**: Konsultiere diese Datei bevor du commitest!
