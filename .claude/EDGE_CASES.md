# Edge Cases & Bekannte Limitierungen

Dokumentation von bekannten Problemen, Limitierungen und Workarounds.

---

## 🎯 Überblick

Diese Datei dokumentiert:
- Bekannte Edge Cases die Probleme verursachen
- Limitierungen des Systems
- Workarounds für häufige Probleme
- Was NICHT funktioniert (und warum)

---

## ⚠️ Bekannte Edge Cases

### 1. Sehr lange Passwörter (>1000 Zeichen)

**Problem:**
```python
# Passwort mit 10.000 Zeichen
password = "a" * 10000
encrypted = encryption_manager.encrypt(password)
# → Funktioniert, aber langsam
```

**Symptome:**
- UI friert kurz ein beim Speichern/Laden
- Verzögerung beim Anzeigen

**Ursache:**
- Fernet-Verschlüsselung hat Overhead
- Base64-Encoding vergrößert Daten

**Lösung:**
- Limit von 1000 Zeichen in UI (Feature-Request: src/gui/entry_dialog.py)
- Performance-Optimierung für >500 Zeichen

**Workaround:**
```python
# In src/gui/entry_dialog.py
self.password_input.setMaxLength(1000)  # Limit setzen
```

**Status:** ⚠️ Bekannt, kein Fix geplant (selten

 relevant)

---

### 2. Umlaute im Master-Passwort

**Problem:**
```python
# Master-Passwort mit Umlauten
master_password = "Pässwört123!"
# → Funktioniert seit Fix #42
```

**Früher:** UnicodeDecodeError
**Jetzt:** ✅ Funktioniert (explizites UTF-8 Encoding)

**Commit:** `f4194a8` - Fix für Bug #42

**Falls Problem auftritt:**
```python
# In src/core/encryption.py prüfen
def encrypt(self, plaintext: str) -> bytes:
    return self._fernet.encrypt(plaintext.encode('utf-8'))  # UTF-8 explizit!
```

**Status:** ✅ Behoben

---

### 3. Sehr viele Einträge (>10.000)

**Problem:**
```python
# Datenbank mit 50.000 Passwort-Einträgen
entries = db.get_all_password_entries()
# → Lädt alle auf einmal, UI friert ein
```

**Symptome:**
- Anwendung startet langsam (>10 Sekunden)
- Scrolling laggy
- Hoher Memory-Verbrauch

**Ursache:**
- Alle Einträge werden auf einmal geladen
- Keine Pagination
- Alle Passwörter entschlüsselt

**Workaround:**
```python
# Lazy Loading implementieren (nicht vorhanden)
# Oder: Suche nutzen statt "Alle Einträge" anzeigen
```

**Status:** ⚠️ Bekannt, Fix TODO (Pagination implementieren)

**Related:** Performance-Issue bei UI-Rendering

---

### 4. Master-Passwort vergessen

**Problem:**
```
User vergisst Master-Passwort → Datenbank nicht entschlüsselbar
```

**Symptome:**
- Login-Dialog zeigt Fehler
- "Falsches Passwort" (auch bei korrektem Passwort?)
- Datenbank nicht öffenbar

**Ursache:**
- Keine Passwort-Recovery (by design!)
- Argon2id Hash ist nicht umkehrbar
- Fernet-Verschlüsselung ohne Key nicht entschlüsselbar

**Lösung:**
- ❌ KEINE! Das ist ein Feature, kein Bug
- Sicherheit > Convenience

**User-Hinweis:**
```
"Master-Passwort vergessen? Leider können wir nicht helfen.
Deine Daten sind verloren. Das ist der Preis für Sicherheit.
Bitte erstelle eine neue Datenbank."
```

**Status:** ✅ By Design (dokumentiert)

---

### 5. Datenbank-Datei korrupt

**Problem:**
```bash
# .spdb Datei beschädigt (z.B. Festplatten-Fehler)
sqlite3.DatabaseError: file is not a database
```

**Symptome:**
- Login funktioniert, aber DB öffnet nicht
- Fehler beim Entschlüsseln
- Anwendung crashed

**Ursache:**
- Korrupte Daten (Hardware, Absturz während Speichern)
- Falsches Dateiformat

**Diagnose:**
```python
# Header prüfen
with open("database.spdb", "rb") as f:
    header = f.read(16)
    if header != b'SECUREPASS_DB_V1':
        print("Korrupt oder falsches Format!")
```

**Lösung:**
- ✅ Von Backup wiederherstellen
- ❌ Reparatur meist unmöglich (verschlüsselt!)

**Prävention:**
- Regelmäßige Backups empfehlen
- Auto-Backup Feature (TODO)

**Status:** ⚠️ Bekannt, Backup-Feature geplant

---

### 6. Temporäre Dateien bleiben nach Crash

**Problem:**
```bash
# Nach Absturz bleiben temp-Dateien
ls /tmp/securepass_*
# → Dutzende alte Dateien
```

**Symptome:**
- `/tmp/` Verzeichnis füllt sich
- Potentielle Sicherheitslücke (entschlüsselte DBs in /tmp!)

**Ursache:**
- Destruktor wird bei Crash nicht aufgerufen
- Temporäre Dateien nicht gelöscht

**Lösung:**
```python
# In DatabaseFile.__del__() - bereits vorhanden, aber bei Crash nicht aufgerufen
# TODO: Context Manager implementieren (with-Statement)
```

**Workaround:**
```bash
# Manuell löschen
rm /tmp/securepass_*.db
```

**Status:** ⚠️ Bekannt (Issue #1 - Exception-Handling im Destruktor)

---

### 7. Mehrere Instanzen gleichzeitig

**Problem:**
```bash
# Zwei Instanzen öffnen gleiche Datenbank
# Instanz 1: Ändert Passwort
# Instanz 2: Weiß nichts davon
# → Datenverlust!
```

**Symptome:**
- Änderungen gehen verloren
- Letzte speichernde Instanz gewinnt

**Ursache:**
- Keine File-Locks
- Keine Multi-Instanz-Detection

**Status:** ⚠️ Bekannt, kein Fix geplant (Feature-Request: File-Locking)

**User-Hinweis:**
```
"Öffne dieselbe Datenbank nicht in mehreren Instanzen gleichzeitig!"
```

---

### 8. Clipboard Auto-Clear und andere Apps

**Problem:**
```
1. User kopiert Passwort
2. Wechselt zu Browser
3. Zwischenablage wird gelöscht (30s Timer)
4. User kann nicht mehr einfügen
```

**Symptome:**
- Zwischenablage leer beim Einfügen
- User-Frustration

**Ursache:**
- Auto-Clear Feature (Sicherheit)
- Timer läuft auch wenn User noch nicht eingefügt hat

**Workaround:**
- Timer-Dauer erhöhen (src/core/settings.py)
- Copy-Button mehrmals klicken

**Status:** ✅ By Design (Sicherheit > Convenience)

**Konfiguration:**
```python
# In src/core/settings.py
"clipboard_clear_seconds": 30  # Auf 60 erhöhen?
```

---

### 9. PyQt6 auf älteren Systemen

**Problem:**
```bash
# Ubuntu 18.04 oder Windows 7
ImportError: PyQt6 requires Python 3.8+
# Oder: Qt library missing
```

**Symptome:**
- Import-Fehler
- Anwendung startet nicht

**Ursache:**
- PyQt6 benötigt Python 3.8+
- Qt6 benötigt moderne OS-Versionen

**Lösung:**
- Python aktualisieren auf 3.8+
- OS aktualisieren
- Oder: PyQt5 nutzen (Projekt-Fork nötig)

**Status:** ✅ Dokumentiert (requirements.txt)

**Mindest-Anforderungen:**
- Python 3.8+
- Windows 10+ / macOS 10.14+ / Ubuntu 20.04+

---

### 10. Auto-Lock während Eingabe

**Problem:**
```
User tippt langes Passwort (5+ Minuten)
→ Auto-Lock triggert
→ Eingabe verloren!
```

**Symptome:**
- Plötzlicher Lock während Arbeit
- Datenverlust

**Ursache:**
- Timer wird nur bei Maus/Tastatur-Events zurückgesetzt
- Aber nicht bei Eingabe in QLineEdit?

**Workaround:**
- Auto-Lock Timeout erhöhen (15 Min. statt 5)

**Status:** ⚠️ Bekannt, besseres Event-Handling TODO

---

## 🚫 Bekannte Limitierungen

### 1. Keine Cloud-Sync (nativ)

**Was funktioniert NICHT:**
```
Automatische Synchronisation zwischen Geräten
```

**Warum:**
- Keine Cloud-Integration implementiert
- .spdb Datei muss manuell synced werden

**Workaround:**
```
Speichere .spdb in Dropbox/Google Drive/OneDrive
→ Manuelle Sync funktioniert
```

**Status:** Feature-Request (nicht geplant)

---

### 2. Keine Browser-Integration

**Was funktioniert NICHT:**
```
Auto-Fill in Browser (wie LastPass/1Password)
```

**Warum:**
- Keine Browser-Extensions
- Keine native Messaging

**Workaround:**
```
Kopieren → Manuell einfügen (Ctrl+V)
```

**Status:** Feature-Request (siehe FEATURES.md)

---

### 3. Keine Passwort-Sharing

**Was funktioniert NICHT:**
```
Passwörter mit anderen Usern teilen
```

**Warum:**
- Single-User Design
- Keine Public-Key-Crypto für Sharing

**Workaround:**
```
Separates Einträge in geteilter Datenbank
→ Beide kennen Master-Passwort
```

**Status:** By Design (Feature-Request: Multi-User)

---

### 4. Keine TOTP/2FA (noch)

**Was funktioniert NICHT:**
```
TOTP-Token generieren (Google Authenticator-Ersatz)
```

**Warum:**
- Feature noch nicht implementiert
- pyotp bereits installiert, aber nicht genutzt

**Status:** 🚧 In Planung (siehe FEATURES.md)

---

### 5. Keine Passwort-Historie

**Was funktioniert NICHT:**
```
Alte Passwörter wiederherstellen nach Änderung
```

**Warum:**
- Nicht implementiert
- Datenbank-Schema unterstützt es nicht

**Workaround:**
```
Manuelles Backup vor Änderung
```

**Status:** Feature-Request

---

### 6. Keine Attachments

**Was funktioniert NICHT:**
```
Dateien an Passwort-Einträge anhängen (PDFs, Keys, etc.)
```

**Warum:**
- Nicht implementiert
- Würde Datenbank-Größe stark erhöhen

**Status:** Feature-Request (niedrige Priorität)

---

### 7. Keine Import/Export (noch)

**Was funktioniert NICHT:**
```
Import von LastPass/1Password/KeePass
Export zu CSV/JSON
```

**Warum:**
- Nicht implementiert

**Status:** 🚧 Geplant (siehe FEATURES.md - Branch: feature/import-export)

---

## 🛠️ Plattform-Spezifische Issues

### Windows

#### 1. Temporäre Dateien in C:\Users\<User>\AppData\Local\Temp

**Problem:** Windows löscht temp-Dateien nicht automatisch

**Lösung:** Manuell löschen oder Cleanup-Script

---

#### 2. Antivirus False-Positives

**Problem:** Einige Antivirus-Programme flaggen verschlüsselte .spdb Dateien

**Lösung:** Exception hinzufügen

---

### macOS

#### 1. Gatekeeper Warnung

**Problem:** "App ist von unbekanntem Entwickler"

**Lösung:**
```bash
# Rechtsklick → Öffnen (statt Doppelklick)
# Oder: Code-Signing (kostenpflichtig)
```

---

#### 2. Clipboard Auto-Clear und Universal Clipboard

**Problem:** Auto-Clear funktioniert nicht bei Universal Clipboard (iOS/macOS Sync)

**Status:** ⚠️ Bekannt, kein Fix möglich (OS-Limitation)

---

### Linux

#### 1. X11 vs Wayland

**Problem:** Clipboard-Management unterschiedlich je nach Display-Server

**Status:** ⚠️ Funktioniert auf beiden, aber unterschiedliches Verhalten

---

#### 2. Dark Mode Detection

**Problem:** Desktop-Environment-abhängig (GNOME, KDE, XFCE)

**Status:** ⚠️ Manueller Toggle funktioniert immer

---

## 🔧 Workarounds-Sammlung

### Langsame Performance

```python
# 1. Index auf häufig gesuchte Spalten
CREATE INDEX idx_name ON password_entries(name);
CREATE INDEX idx_category ON password_entries(category_id);

# 2. Nur sichtbare Einträge entschlüsseln (Lazy Loading)
# TODO: Implementieren

# 3. Virtual Scrolling für UI
# TODO: Implementieren
```

---

### Memory-Leaks

```python
# Explizit aufräumen
encryption_manager.clear()
db.close()
app.quit()
```

---

### UI friert ein

```python
# Langläufige Operationen in Threads
from PyQt6.QtCore import QThread

class WorkerThread(QThread):
    def run(self):
        # Langwierige Operation
        pass

# TODO: Implementieren für große DB-Operationen
```

---

## 📋 User-Facing Limitations (Dokumentieren!)

**In README.md / User-Docs:**

```markdown
## Bekannte Einschränkungen

- ❌ Kein automatisches Cloud-Sync (manuell über Dropbox/Drive möglich)
- ❌ Keine Browser-Integration (Copy-Paste notwendig)
- ❌ Kein Passwort-Recovery bei vergessenem Master-Passwort
- ❌ Keine Multi-User/Sharing Features
- ⚠️ Langsam bei >10.000 Einträgen
- ⚠️ Nicht geeignet für mehrere gleichzeitige Instanzen
```

---

## 🎯 Zusammenfassung für Claude

**Als Claude-Assistent:**

### Vor Implementierung prüfen:

```
1. Ist dieses Feature in EDGE_CASES.md als "funktioniert NICHT"?
   → User fragen ob trotzdem implementieren

2. Ist das ein bekanntes Problem mit Workaround?
   → Workaround verwenden

3. Ist das plattform-spezifisch?
   → Plattform-Check implementieren
```

### Bei Bug-Reports:

```
1. Prüfe EDGE_CASES.md - ist das bekannt?
2. Falls ja → Erkläre Limitation/Workaround
3. Falls nein → Debugge normal (siehe DEBUGGING.md)
```

### Bei Feature-Requests:

```
1. Prüfe "Bekannte Limitierungen"
2. Falls dort → "Das ist aktuell nicht unterstützt weil..."
3. Verweise auf FEATURES.md für Roadmap
```

---

**Letzte Aktualisierung**: 2025-12-01
**Status**: Living Document (wird erweitert bei neuen Edge Cases)

**Bei neuen Edge Cases:**
1. Dokumentiere hier
2. Update SESSION_LOG.md
3. Ggf. Issue erstellen
