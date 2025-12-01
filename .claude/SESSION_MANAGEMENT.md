# ⚠️ KRITISCH: Session-Management für AI-Entwickler

**WICHTIG**: Lese dies ZUERST bei jeder neuen Session!

---

## 🚨 Das Problem: Auto-Compact kann die Wissensdatenbank zerstören

### Was ist Auto-Compact?
Bei zu hoher Token-Nutzung (>180.000 Tokens) kann Claude Code automatisch große Dateien komprimieren, um Speicher zu sparen.

### Was passiert mit knowledge-base.md?
Die komplette Wissensdatenbank wird auf eine Zeile reduziert:
```
Siehe vorherige Edits - Datei zu lang für single Write
```

**ALLE 700+ Zeilen Dokumentation sind weg!** 😱

---

## 📊 Token-Budget Management

### Token-Zonen
```
   0 -  50.000 → ✅ SICHER (Grün)
  50.000 - 100.000 → ✅ SICHER (Grün)
 100.000 - 150.000 → ⚠️ VORSICHT (Gelb) - Backup erstellen!
 150.000 - 180.000 → 🔶 KRITISCH (Orange) - Nur kleine Edits!
 180.000 - 200.000 → 🚨 GEFAHR (Rot) - STOPP alle großen Edits!
```

### Was bei welcher Token-Zone tun?

#### Bei 100.000 Tokens (GELB)
```bash
# Erstelle Backup der Wissensdatenbank
cp .claude/knowledge-base.md .claude/knowledge-base-backup.md

# Optional: Committe in Git
git add .claude/knowledge-base.md
git commit -m "docs: Backup knowledge-base bei 100k Tokens"
```

#### Bei 150.000 Tokens (ORANGE)
**WICHTIG:**
1. ⛔ Keine großen Edits mehr an knowledge-base.md
2. ✅ Kleine Updates OK (1-3 Zeilen)
3. 💾 Committe alle wichtigen Änderungen
4. 🔄 Erwäge Session-Neustart

#### Bei 180.000 Tokens (ROT)
**SOFORT HANDELN:**
1. 🛑 **STOPPE ALLE Edits** an knowledge-base.md
2. 💾 **Committe sofort** alle aktuellen Änderungen
3. 📝 **Dokumentiere** Fortschritt in SESSION_LOG.md
4. ✅ **Beende Session** JETZT

**NIEMALS bei >180k Tokens:**
- ❌ knowledge-base.md bearbeiten (Write oder Edit)
- ❌ Mehrere aufeinanderfolgende große Edits
- ❌ Neue Features zur Doku hinzufügen
- ❌ Session ohne Commit fortsetzen

---

## 🔧 Wiederherstellung nach Auto-Compact

Falls die knowledge-base.md beschädigt wurde:

### Methode 1: Git Restore (EMPFOHLEN)
```bash
# 1. Prüfe letzten funktionierenden Stand
git log --oneline .claude/knowledge-base.md

# 2. Zeige letzten Commit-Inhalt
git show HEAD:.claude/knowledge-base.md | head -20

# 3. Stelle wieder her
git checkout HEAD -- .claude/knowledge-base.md

# ODER: Spezifischer Commit
git checkout e7f0362 -- .claude/knowledge-base.md
```

### Methode 2: Backup verwenden
```bash
# Falls Backup existiert
cp .claude/knowledge-base-backup.md .claude/knowledge-base.md
```

### Methode 3: Aus Git History extrahieren
```bash
# Extrahiere aus letztem Commit
git show HEAD:.claude/knowledge-base.md > .claude/knowledge-base-restored.md

# Prüfe Datei
wc -l .claude/knowledge-base-restored.md  # Sollte ~700 Zeilen sein

# Ersetze beschädigte Datei
mv .claude/knowledge-base-restored.md .claude/knowledge-base.md
```

---

## ✅ Best Practices für lange Sessions

### 1. Start jeder Session
```bash
# Prüfe Integrität der knowledge-base
Read: .claude/knowledge-base.md

# Falls beschädigt → Sofort wiederherstellen!
```

### 2. Vor großen Updates (ab 100k Tokens)
```bash
# IMMER Backup erstellen
cp .claude/knowledge-base.md .claude/knowledge-base-backup.md
```

### 3. Während der Session
- **Token-Tracking**: Kontinuierlich im Auge behalten
- **Kleine Commits**: Lieber 5 kleine als 1 großer Commit
- **Backup-First**: Immer Backup vor großen knowledge-base Edits

### 4. Bei wichtigen Änderungen (sofort committen!)
```bash
git add .claude/knowledge-base.md
git commit -m "docs: [Beschreibung der Änderung]"
```

### 5. Session-Ende
```bash
# Finaler Commit
git add .claude/
git commit -m "docs: Update Wissensdatenbank - Session Ende"
git push
```

---

## 📋 Checkliste für AI-Entwickler

### Beim Session-Start
- [ ] `Read: .claude/SESSION_MANAGEMENT.md` gelesen?
- [ ] `Read: .claude/knowledge-base.md` - Integrität geprüft?
- [ ] Aktuelle Token-Nutzung notiert?

### Bei ~100.000 Tokens
- [ ] Backup erstellt? (`cp .claude/knowledge-base.md .claude/knowledge-base-backup.md`)
- [ ] Wichtige Änderungen committed?

### Bei ~150.000 Tokens
- [ ] Nur noch kleine Edits an knowledge-base.md?
- [ ] Alle wichtigen Änderungen gesichert?
- [ ] Session-Neustart in Betracht gezogen?

### Bei ~180.000 Tokens
- [ ] ALLE Edits an knowledge-base.md gestoppt?
- [ ] Sofort committed?
- [ ] Session beendet oder neu gestartet?

---

## 🎯 Strategien für große Dokumentations-Updates

### ❌ SCHLECHT: Eine lange Session
```
Session 1: 0 → 190k Tokens
- Große knowledge-base Updates
- Auto-Compact schlägt zu
- Alles verloren!
```

### ✅ GUT: Mehrere kleine Sessions
```
Session 1: 0 → 100k Tokens
- Update Teil 1
- Commit & Push
- Session beenden

Session 2: 0 → 100k Tokens
- Update Teil 2
- Commit & Push
- Session beenden

Session 3: 0 → 100k Tokens
- Update Teil 3
- Commit & Push
- FERTIG!
```

---

## 🔍 Wie erkenne ich Auto-Compact?

### Anzeichen
1. knowledge-base.md zeigt nur: `Siehe vorherige Edits - Datei zu lang für single Write`
2. `wc -l .claude/knowledge-base.md` zeigt nur 1 Zeile (sollte ~700 sein)
3. `Read: .claude/knowledge-base.md` zeigt minimalen Inhalt

### Sofort-Reaktion
```bash
# 1. STOPP alles
# 2. NICHT speichern/committen
# 3. Wiederherstellen aus Git (siehe oben)
# 4. Session beenden
```

---

## 📚 Weitere Dokumentation

- **`.claude/QUICK_START.md`** - Session-Management Abschnitt
- **`.claude/knowledge-base.md`** - Abschnitt 0 (Session-Management)
- **`.claude/GIT_WORKFLOW.md`** - Git Best Practices

---

## 💡 Tipps

1. **Token-Bewusst arbeiten**: Große Read-Operationen vermeiden wenn möglich
2. **Git ist dein Freund**: Häufig committen = Sicherheitsnetz
3. **Backup-Paranoia ist gut**: Lieber 3 Backups zu viel als 1 zu wenig
4. **Klein denken**: 3 kleine Sessions > 1 große Session
5. **Dokumentiere deinen Fortschritt**: SESSION_LOG.md nutzen

---

**Erstellt**: 2025-12-01
**Letztes Update**: 2025-12-01
**Status**: Aktiv & Kritisch

**Bei Fragen**: Lese diese Datei nochmal oder konsultiere Git-History!
