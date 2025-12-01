# Claude Wissensdatenbank

Dieses Verzeichnis enthält die kontinuierliche Wissensbasis für Claude Code Assistenten, um bei jedem neuen Chat-Fenster den gleichen Wissensstand zu haben.

---

## ⚡ Schnellstart für neue Chats

**NEU IM PROJEKT? START HIER:** [`HOW_TO_USE.md`](HOW_TO_USE.md)

→ Enthält **fertige Prompts** zum Kopieren für neue Chat-Fenster!

## 🚨 KRITISCH: Session-Management

**FÜR AI-ENTWICKLER: LESE DIES ZUERST!** [`SESSION_MANAGEMENT.md`](SESSION_MANAGEMENT.md)

→ **Auto-Compact kann die Wissensdatenbank zerstören!**
→ Token-Budget Management & Wiederherstellungs-Strategien

---

## Dateien-Übersicht

### 🚨 `SESSION_MANAGEMENT.md` (KRITISCH - ZUERST LESEN!)
**Zweck**: Verhindere Auto-Compact Beschädigung der Wissensdatenbank

**Inhalt**:
- Token-Budget Management (Grün/Gelb/Orange/Rot Zonen)
- Was tun bei 100k, 150k, 180k Tokens
- Backup-Strategien
- Wiederherstellung nach Auto-Compact
- Best Practices für lange Sessions

**Wann lesen**:
- **Bei JEDER neuen Session** - Pflichtlektüre!
- **Bei ~100k Tokens** - Backup-Strategien aktivieren
- **Bei ~150k Tokens** - Kritische Zone erreicht
- **Nach Auto-Compact** - Wiederherstellung

⚠️ **WICHTIG**: Diese Datei kann dich vor Datenverlust bewahren!

---

### 🎯 `HOW_TO_USE.md` (START HIER!)
**Zweck**: Anleitung für neue Chat-Fenster mit fertigen Prompts

**Inhalt**:
- Fertige Prompts zum Kopieren
- Beispiele für verschiedene Szenarien
- Welche Datei wofür lesen
- Häufige Fehler vermeiden

**Wann lesen**:
- **Beim ersten Mal** - Verstehe, wie du Claude die Wissensdatenbank nutzen lässt
- **Vor jedem neuen Chat** - Kopiere den passenden Prompt

### 📚 `knowledge-base.md` (HAUPTDATEI)
**Zweck**: Vollständige, detaillierte Wissensbasis über das Projekt

**Inhalt**:
- Projekt-Übersicht
- Technologie-Stack & Dependencies
- Architektur & Design-Patterns
- Sicherheitskonzept (Verschlüsselung)
- Datenbankschema
- UI-System (Theme, Icons, Animationen)
- Bekannte Issues
- Code-Referenzen
- Build & Run Anleitungen
- Entwicklungs-Empfehlungen

**Wann lesen**:
- Bei jedem neuen Chat (Nachfolger-Assistent)
- Vor größeren Änderungen
- Bei Fragen zur Architektur

---

### 🚀 `QUICK_START.md`
**Zweck**: Schnelle 2-Minuten-Einführung

**Inhalt**:
- Projekt-Übersicht (1 Absatz)
- Wichtigste Dateien
- Aktuelle Probleme (priorisiert)
- Häufige Aufgaben (Code-Snippets)
- Checkliste für Nachfolger

**Wann lesen**:
- Erster Einstieg in das Projekt
- Schnelle Referenz
- Wenn keine Zeit für `knowledge-base.md`

---

### 🔀 `GIT_WORKFLOW.md`
**Zweck**: Git Best Practices für KI-gestützte Entwicklung

**Inhalt**:
- Branch-Naming Conventions
- Commit-Message Format
- Wann und wie committen
- Pull Request Workflow
- Beispiele für alle Szenarien

**Wann lesen**:
- **Vor dem ersten Commit** - Verstehe den Workflow
- **Bei neuen Features** - Branching-Strategie
- **Bei Unsicherheiten** - Nachschlagen

---

### 🧪 `TESTING.md` ⭐ NEU
**Zweck**: Testing-Guide und Best Practices

**Inhalt**:
- Wie Tests ausführen (pytest)
- Coverage-Anforderungen (80%+)
- Test-Driven Development
- Fixtures & Helpers
- Pre-Push Checkliste

**Wann lesen**:
- **Vor neuen Features** - Wie Tests schreiben
- **Bei Bugfixes** - Test für Bug erstellen
- **Vor jedem Push** - Coverage prüfen

### 🐛 `DEBUGGING.md` ⭐ NEU
**Zweck**: Troubleshooting und häufige Fehler

**Inhalt**:
- Häufige Fehler & Lösungen
- Debugging-Strategien (pdb, logging)
- Performance-Profiling
- Troubleshooting-Checkliste

**Wann lesen**:
- **Bei Problemen** - Lösungen finden
- **Bei Bugs** - Debug-Workflow
- **Performance-Issues** - Profiling-Tools

### 💬 `CLAUDE_GUIDE.md` ⭐ NEU
**Zweck**: Kommunikations-Protokoll für KI-Assistenten

**Inhalt**:
- Wann Benutzer fragen
- Wie Änderungen präsentieren
- Fehler kommunizieren
- Best Practices

**Wann lesen**:
- **Vor jeder Session** - Kommunikations-Grundlagen
- **Bei Unsicherheiten** - Soll ich fragen?
- **Komplexe Entscheidungen** - Wie präsentieren

### 📐 `CONVENTIONS.md` ⭐ NEU
**Zweck**: Code-Style und Projektspezifisches

**Inhalt**:
- PEP 8 + Projekt-Regeln
- Naming Conventions
- Wo neue Dateien hinzufügen
- Import-Reihenfolge
- PyQt6-spezifisch

**Wann lesen**:
- **Vor neuen Dateien** - Wo hinzufügen
- **Neue Features** - Struktur-Konventionen
- **Code-Review** - Standards prüfen

### ⚠️ `EDGE_CASES.md` ⭐ NEU
**Zweck**: Bekannte Limitierungen und Workarounds

**Inhalt**:
- Bekannte Edge Cases
- System-Limitierungen
- Plattform-spezifische Issues
- Workarounds

**Wann lesen**:
- **Vor Features** - Ist das möglich?
- **Bei Bugs** - Bekanntes Problem?
- **User-Reports** - Limitation erklären

### 🔒 `SECURITY_CHECKLIST.md` ⭐ NEU
**Zweck**: Security-Review für neuen Code

**Inhalt**:
- Security-Review Checkliste
- Goldene Regeln (keine Klartext-PWs!)
- Verschlüsselungs-Patterns
- Häufige Sicherheitslücken
- Security-Tests

**Wann lesen**:
- **VOR jedem Commit** - Security-Review
- **Verschlüsselung** - Patterns nutzen
- **Input-Handling** - Validation prüfen

### 📝 `SESSION_LOG.md`
**Zweck**: Protokoll aller durchgeführten Analysen und Änderungen

**Inhalt**:
- Durchgeführte Analysen (pro Session)
- Erkenntnisse
- Verwendete Agenten
- Nächste Schritte
- Changelog

**Wann aktualisieren**:
- Am Ende jeder Session
- Bei größeren Änderungen
- Bei neuen Erkenntnissen

---

### ⚙️ `settings.local.json`
**Zweck**: Claude Code Einstellungen (automatisch generiert)

**Nicht bearbeiten**: Diese Datei wird automatisch von Claude Code verwaltet.

---

## Workflow für Nachfolger-Assistenten

### 1. Neues Chat-Fenster startet
```
1. ⚠️ PFLICHT: Lese `.claude/SESSION_MANAGEMENT.md` (Token-Budget!)
2. Lese `.claude/QUICK_START.md` (2 Min.)
3. Konsultiere `.claude/knowledge-base.md` bei Bedarf
4. Schaue in `.claude/SESSION_LOG.md` für letzten Stand
5. Beginne mit Arbeit
```

### 2. Während der Arbeit
```
- ⚠️ Token-Tracking: Überwache kontinuierlich Token-Nutzung
- Bei ~100k Tokens: Erstelle Backup (siehe SESSION_MANAGEMENT.md)
- Bei Fragen: Konsultiere `knowledge-base.md`
- Bei Code-Suche: Nutze Datei-Referenzen (Pfad:Zeile)
- Bei Issues: Schaue in "Bekannte Issues" Sektion
```

### 3. Am Ende der Session
```
1. 💾 WICHTIG: Committe knowledge-base.md (falls geändert)
2. Aktualisiere `SESSION_LOG.md` (Changelog)
3. Bei größeren Änderungen: Aktualisiere `knowledge-base.md`
4. Finaler Commit & Push
```

---

## Wartung der Wissensdatenbank

### Wann `knowledge-base.md` aktualisieren?

**JA - Aktualisiere bei**:
- Neuen Modulen/Dateien
- Architektur-Änderungen
- Neuen Sicherheitsfeatures
- Datenbankschema-Änderungen
- Neuen Dependencies
- Gelösten/neuen Issues

**NEIN - Nicht aktualisieren bei**:
- Kleinen Bugfixes
- UI-Anpassungen
- Code-Refactoring (ohne Architektur-Änderung)

### Wann `SESSION_LOG.md` aktualisieren?

**Immer bei**:
- Abschluss einer Session
- Größeren Analysen
- Neuen Erkenntnissen
- Gelösten Issues

---

## Struktur der Wissensdatenbank

### `knowledge-base.md` Abschnitte

1. **Projekt-Übersicht** - Was ist das Projekt?
2. **Projektstruktur** - Verzeichnisbaum
3. **Technologie-Stack** - Dependencies & Tools
4. **Architektur** - Design-Patterns & Singletons
5. **Sicherheitskonzept** - Verschlüsselung (3-Schicht)
6. **Datenbankschema** - SQLite-Tabellen
7. **Anwendungsfluss** - Start bis Lock
8. **UI-System** - Theme, Icons, Animationen
9. **Bekannte Issues** - Priorisierte Liste
10. **Code-Referenzen** - Wichtige Datei:Zeile
11. **Build & Run** - Installation & Start
12. **Einstellungen & Daten** - Konfiguration
13. **Tastenkombinationen** - Shortcuts
14. **Entwicklungs-Empfehlungen** - Best Practices
15. **Wichtige Hinweise** - Philosophie & Standards

---

## Verwendung durch Benutzer (Entwickler)

### Du kannst diese Dateien nutzen um:
1. **Projekt-Übersicht** zu bekommen
2. **Architektur** zu verstehen
3. **Bekannte Issues** zu sehen
4. **Code-Referenzen** zu finden

### Du musst diese Dateien NICHT bearbeiten:
- Claude Code Assistenten aktualisieren sie automatisch
- Du kannst sie aber manuell anpassen, wenn gewünscht

---

## Best Practices

### Für Claude Assistenten

**DO**:
- ✅ `knowledge-base.md` zu Beginn lesen
- ✅ `SESSION_LOG.md` am Ende aktualisieren
- ✅ Code-Referenzen mit `Pfad:Zeile` angeben
- ✅ Issues mit Prioritäten dokumentieren
- ✅ Changelog führen

**DON'T**:
- ❌ Wissensdatenbank bei jedem kleinen Bugfix aktualisieren
- ❌ Redundante Informationen duplizieren
- ❌ Unstrukturierte Notizen hinzufügen
- ❌ Veraltete Informationen stehen lassen

---

## Dateigröße & Wartung

**Aktuelle Größe**:
- `knowledge-base.md`: ~400 Zeilen
- `QUICK_START.md`: ~150 Zeilen
- `SESSION_LOG.md`: ~200 Zeilen
- **Gesamt**: ~750 Zeilen

**Wartung**:
- Bei >500 Zeilen: Überlegen, Abschnitte auszulagern
- Bei veralteten Infos: Aktualisieren oder entfernen
- Changelog regelmäßig bereinigen (ältere Einträge archivieren)

---

## Kontakt & Fragen

Wenn du als Entwickler Fragen hast:
1. Lese `knowledge-base.md`
2. Konsultiere Claude Code Assistent
3. Schaue in Projekt-Dokumentation (`README.md`, `DATABASE.md`, etc.)

Wenn du als Claude Assistent unsicher bist:
1. Lese `knowledge-base.md` vollständig
2. Suche im Code mit Grep/Glob
3. Frage den Benutzer bei Unklarheiten

---

**Ziel**: Kontinuierlicher Wissenstransfer zwischen Chat-Sessions

**Status**: ✅ Vollständig eingerichtet (2025-12-01)

**Nächste Schritte**: Nutzen und bei Bedarf aktualisieren
