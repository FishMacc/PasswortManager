# Wie du die Wissensdatenbank in einem neuen Chat nutzt

---

## ⚡ TL;DR - Schnellversion

**🚨 FÜR AI-ENTWICKLER: Kopiere diesen Prompt in ein neues Chat-Fenster:**

```
Lies bitte die Wissensdatenbank im .claude/ Verzeichnis, damit du das Projekt verstehst:
- .claude/SESSION_MANAGEMENT.md - KRITISCH! Token-Budget Management (lese ZUERST!)
- .claude/QUICK_START.md für einen schnellen Überblick
- .claude/knowledge-base.md für Details bei Bedarf
- .claude/PROJECT_MAP.md für visuelle Orientierung

Danach können wir mit der Arbeit starten.
```

**Das war's!** Claude liest automatisch die Dateien und ist auf dem gleichen Stand.

⚠️ **WICHTIG**: SESSION_MANAGEMENT.md ZUERST lesen - verhindert Auto-Compact Datenverlust!

---

## 📖 Detaillierte Anleitung

### Option 1: Minimaler Prompt (empfohlen für einfache Aufgaben)

```
Schau dir .claude/QUICK_START.md an bevor wir starten.
```

**Wann verwenden:**
- Kleine Bugfixes
- Einfache Features
- Schnelle Fragen

**Dauer:** ~30 Sekunden

---

### Option 2: Mittlerer Prompt (empfohlen für normale Arbeit)

```
Lies bitte die Wissensdatenbank:
- .claude/SESSION_MANAGEMENT.md (Token-Budget - WICHTIG!)
- .claude/QUICK_START.md (Überblick)
- .claude/knowledge-base.md (Details)

Dann helfe mir bei [DEINE AUFGABE].
```

**Wann verwenden:**
- Neue Features entwickeln
- Größere Refactorings
- Komplexere Bugfixes
- Du bist länger nicht im Projekt gewesen

**Dauer:** ~1-2 Minuten

---

### Option 3: Vollständiger Prompt (empfohlen für komplexe Aufgaben)

```
Ich arbeite am SecurePass Manager (Python Passwort-Manager).

Bitte lies die vollständige Wissensdatenbank im .claude/ Verzeichnis:
1. .claude/SESSION_MANAGEMENT.md - Token-Budget Management (ZUERST LESEN!)
2. .claude/QUICK_START.md - Schneller Überblick
3. .claude/knowledge-base.md - Vollständige Dokumentation
4. .claude/PROJECT_MAP.md - Visuelle Projekt-Struktur
5. .claude/SESSION_LOG.md - Letzte Änderungen

Danach möchte ich [DEINE AUFGABE].
```

**Wann verwenden:**
- Architektur-Änderungen
- Sicherheits-kritische Änderungen
- Mehrere zusammenhängende Aufgaben
- Neues Teammitglied (du kennst das Projekt noch nicht gut)

**Dauer:** ~3-5 Minuten

---

## 🎯 Beispiel-Prompts für verschiedene Szenarien

### Szenario 1: Bugfix

```
Schau dir .claude/QUICK_START.md an.

Ich habe einen Bug gefunden: [BESCHREIBUNG].
Kannst du helfen, das zu fixen?
```

---

### Szenario 2: Neues Feature

```
Lies die Wissensdatenbank:
- .claude/QUICK_START.md
- .claude/knowledge-base.md (Abschnitt 4: Architektur)

Ich möchte ein neues Feature hinzufügen: [BESCHREIBUNG].
Lass uns das gemeinsam planen und implementieren.
```

---

### Szenario 3: Code verstehen

```
Schau dir .claude/PROJECT_MAP.md an.

Ich verstehe nicht, wie [MODUL/FUNKTION] funktioniert.
Kannst du mir das erklären?
```

---

### Szenario 4: Issue aus der Liste beheben

```
Lies .claude/knowledge-base.md (Abschnitt 9: Bekannte Issues).

Ich möchte das kritische Issue #1 (Exception-Handling im Destruktor) beheben.
Lass uns das zusammen angehen.
```

---

### Szenario 5: Weiterarbeit nach längerer Pause

```
Ich habe länger nicht am SecurePass Manager gearbeitet.

Bitte lies:
- .claude/knowledge-base.md - Vollständige Dokumentation
- .claude/SESSION_LOG.md - Was hat sich geändert?

Dann gib mir einen kurzen Überblick, wo wir stehen.
```

---

## 🤖 Funktioniert das automatisch?

**Nein, Claude liest die Dateien NICHT automatisch.**

Du musst Claude **explizit bitten**, die Wissensdatenbank zu lesen. Claude Code hat zwar Zugriff auf alle Dateien im Projekt, aber öffnet sie nur auf Anfrage.

### Warum nicht automatisch?

- **Performance**: Nicht jede Aufgabe braucht den vollen Kontext
- **Token-Effizienz**: Spart API-Kosten
- **Flexibilität**: Du entscheidest, wie viel Kontext nötig ist

---

## 💡 Pro-Tipps

### Tipp 1: Kombiniere mit konkreter Aufgabe

**Gut:**
```
Lies .claude/QUICK_START.md.
Dann füge einen neuen Kategorie-Filter hinzu.
```

**Besser:**
```
Lies die Wissensdatenbank (.claude/QUICK_START.md und knowledge-base.md).

Ich möchte einen neuen Kategorie-Filter hinzufügen, der:
1. Mehrere Kategorien gleichzeitig filtert
2. Im Header neben der Suche angezeigt wird
3. Mit Checkboxen arbeitet

Lass uns das zusammen umsetzen.
```

---

### Tipp 2: Verweise auf spezifische Abschnitte

**Bei bekannten Issues:**
```
Lies .claude/knowledge-base.md (Abschnitt 9: Bekannte Issues).
Behebe Issue #1 (Kritisch - Exception-Handling).
```

**Bei Architektur-Fragen:**
```
Lies .claude/knowledge-base.md (Abschnitt 4: Architektur).
Erkläre mir, wie die Singleton-Instanzen funktionieren.
```

---

### Tipp 3: Verwende die PROJECT_MAP für visuelle Orientierung

```
Schau dir .claude/PROJECT_MAP.md an.
Zeige mir, wo ich anfangen muss für [AUFGABE].
```

---

### Tipp 4: Nutze SESSION_LOG für Kontext

```
Lies .claude/SESSION_LOG.md.
Was wurde zuletzt geändert? Wo müssen wir weitermachen?
```

---

## 🔀 Git Workflow beachten!

**WICHTIG für alle Code-Änderungen:**

Claude wird automatisch Branches erstellen und committen.
Vollständige Details: **`.claude/GIT_WORKFLOW.md`**

**Grundregeln:**
- ✅ Immer Branches für Features/Fixes
- ✅ NIEMALS direkt auf main committen
- ✅ Pull Requests für alle Merges
- ✅ Tests vor Push ausführen

**Standard-Workflow:**
```bash
1. git checkout -b feature/xyz
2. [Entwickeln + Committen]
3. git push -u origin feature/xyz
4. gh pr create
```

---

## 📋 Checkliste für neuen Chat

**Bevor du startest:**

- [ ] Überlege: Wie komplex ist meine Aufgabe?
  - Einfach → QUICK_START.md
  - Mittel → QUICK_START.md + knowledge-base.md
  - Komplex → Alle Dateien

- [ ] Kopiere passenden Prompt (siehe oben)
- [ ] Ergänze deine konkrete Aufgabe
- [ ] Sende Prompt ab
- [ ] Warte, bis Claude die Dateien gelesen hat (~1-2 Min.)
- [ ] Starte mit der Arbeit!

---

## 🎬 Beispiel-Session (von Start bis Finish)

### Schritt 1: Chat öffnen
```
DU: Lies die Wissensdatenbank (.claude/QUICK_START.md und knowledge-base.md).
    Dann helfe mir, das Auto-Lock Feature zu testen.

CLAUDE: [Liest Dateien...]
        Ich habe die Wissensdatenbank gelesen. Das Auto-Lock Feature
        ist in src/gui/main_window.py:550-580 implementiert.

        Soll ich:
        1. Bestehende Tests in tests/ ansehen?
        2. Neue Tests schreiben?
        3. Das Feature manuell testen?
```

### Schritt 2: Arbeiten
```
DU: Schreib bitte einen Unit-Test dafür.

CLAUDE: [Schreibt Test...]
```

### Schritt 3: Am Ende
```
DU: Super, danke! Aktualisiere bitte die SESSION_LOG.md.

CLAUDE: [Aktualisiert SESSION_LOG...]
```

---

## ⚠️ Häufige Fehler

### ❌ Fehler 1: Gar nichts sagen
```
DU: Füge einen Dark Mode Toggle hinzu.
```
**Problem**: Claude kennt das Projekt nicht → Ineffizient

### ✅ Richtig:
```
DU: Lies .claude/QUICK_START.md.
    Füge einen Dark Mode Toggle hinzu.
```

---

### ❌ Fehler 2: Zu viele Details verlangen
```
DU: Lies ALLE Dateien im .claude/ Verzeichnis und auch alle
    Python-Dateien im src/ Verzeichnis und erkläre mir alles.
```
**Problem**: Überforderung → Dauert ewig

### ✅ Richtig:
```
DU: Lies .claude/knowledge-base.md.
    Gib mir einen kurzen Überblick über die Architektur.
```

---

### ❌ Fehler 3: Falsche Datei für Aufgabe
```
DU: Lies .claude/PROJECT_MAP.md.
    [Komplexe Architektur-Änderung]
```
**Problem**: PROJECT_MAP ist nur visuell, nicht detailliert genug

### ✅ Richtig:
```
DU: Lies .claude/knowledge-base.md (Abschnitt 4: Architektur).
    [Komplexe Architektur-Änderung]
```

---

## 🔄 Update-Workflow

**Am Ende deiner Session:**

```
Aktualisiere bitte die Wissensdatenbank:
1. SESSION_LOG.md - Füge Changelog-Eintrag hinzu
2. knowledge-base.md - [Nur bei größeren Änderungen]
```

**Nächster Chat:**
```
Lies .claude/SESSION_LOG.md.
Was wurde zuletzt geändert?
```

---

## 📚 Welche Datei wofür?

| Datei | Zweck | Wann lesen? |
|-------|-------|-------------|
| `SESSION_MANAGEMENT.md` ⚠️ | Token-Budget Management | **IMMER ZUERST! (Pflicht)** |
| `QUICK_START.md` | Schneller Überblick | Immer (Standard) |
| `knowledge-base.md` | Vollständige Doku | Komplexe Aufgaben |
| `PROJECT_MAP.md` | Visuelle Struktur | Orientierung, neue Features |
| `SESSION_LOG.md` | Änderungshistorie | Nach Pause, Kontext |
| `README.md` | Erklärung .claude/ | Nur zum Verstehen des Systems |

---

## 🎯 Zusammenfassung

### Der perfekte Prompt für 90% der Fälle:

```
Lies die Wissensdatenbank im .claude/ Verzeichnis:
- .claude/SESSION_MANAGEMENT.md (Token-Budget - ZUERST!)
- .claude/QUICK_START.md (Überblick)
- .claude/knowledge-base.md (Details)

Dann helfe mir bei [DEINE AUFGABE].
```

**Das war's!**

⚠️ **KRITISCH**: SESSION_MANAGEMENT.md verhindert Auto-Compact Datenverlust!

---

**Zuletzt aktualisiert**: 2025-12-01
**Funktioniert mit**: Claude Code (alle Versionen)
