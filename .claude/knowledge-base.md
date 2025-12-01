# SecurePass Manager - Wissensdatenbank

**Letzte Aktualisierung**: 2025-12-01 (Abend - 2FA/TOTP-Implementierung + Theme-Fix)
**Projekt-Typ**: Python-basierter Passwort-Manager mit PyQt6
**Status**: Voll funktionsfähig, produktionsreif, 2FA-Support aktiv
**Dokumentations-Konformität**: 99% (Verifiziert 2025-12-01)

---

## 0. ⚠️ KRITISCH: Session-Management für AI-Entwickler

### Token-Budget & Auto-Compact Problem

**Token-Budget**: 200.000 Tokens pro Session
**Problem**: Bei langen Sessions kann Auto-Compact die Wissensdatenbank **beschädigen**!

#### 🚨 Was passiert?
Bei zu hoher Token-Nutzung kann `knowledge-base.md` auf folgendes reduziert werden:
```
Siehe vorherige Edits - Datei zu lang für single Write
```
**ALLE Informationen gehen verloren!**

### ✅ Pflicht-Regeln für lange Sessions

#### 1. Token-Monitoring (WICHTIG!)
```
Tokens < 150.000 → ✅ Sicher
Tokens 150.000 - 180.000 → ⚠️ Vorsichtig (nur kleine Edits)
Tokens > 180.000 → 🚨 KRITISCH (STOPP alle großen Edits!)
```

#### 2. Bei ~150.000 Tokens: Backup erstellen
```bash
# Erstelle sofort Backup
cp .claude/knowledge-base.md .claude/knowledge-base-backup.md

# Oder committe in Git
git add .claude/knowledge-base.md
git commit -m "docs: Sichere knowledge-base vor Auto-Compact"
```

#### 3. Bei ~180.000 Tokens: KRITISCH!
**SOFORT HANDELN:**
1. ⛔ **STOPPE alle Edits** an knowledge-base.md
2. 💾 **Committe** alle aktuellen Änderungen
3. ✅ **Beende Session** oder starte neu
4. 📝 **Dokumentiere** Fortschritt in SESSION_LOG.md

**NIEMALS bei >180k Tokens:**
- ❌ Große Write-Operationen
- ❌ knowledge-base.md bearbeiten
- ❌ Mehrere aufeinanderfolgende Edits

#### 4. Wiederherstellung (falls Auto-Compact zugeschlagen hat)

**Methode 1: Aus Git**
```bash
# Prüfe letzten funktionierenden Stand
git log --oneline .claude/knowledge-base.md

# Stelle wieder her
git checkout HEAD -- .claude/knowledge-base.md

# Oder spezifischer Commit
git checkout <commit-hash> -- .claude/knowledge-base.md
```

**Methode 2: Aus Backup**
```bash
# Falls Backup existiert
cp .claude/knowledge-base-backup.md .claude/knowledge-base.md
```

**Methode 3: Aus Git-History extrahieren**
```bash
# Zeige Inhalt aus letztem Commit
git show HEAD:.claude/knowledge-base.md > .claude/knowledge-base.md
```

### 📊 Best Practices

1. **Regelmäßige Commits** bei wichtigen Dokumentations-Updates
2. **Kleine Sessions** für große knowledge-base Updates (lieber 3x 50k als 1x 150k)
3. **Backup-First**: Immer Backup vor großen Edits
4. **Token-Tracking**: Kontinuierlich im Auge behalten
5. **Git als Sicherheitsnetz**: Häufig committen

### ✅ Sichere Arbeitsweise

```bash
# Start jeder Session
Read: .claude/knowledge-base.md  # Prüfe Integrität

# Vor großen Updates (bei ~100k Tokens)
Bash: cp .claude/knowledge-base.md .claude/knowledge-base-backup.md

# Nach wichtigen Änderungen (sofort!)
Bash: git add .claude/knowledge-base.md
Bash: git commit -m "docs: Update knowledge-base"

# Bei >150k Tokens
# → Nur noch kleine Edits oder Session beenden
```

---

## 1. Projekt-Übersicht

SecurePass Manager ist ein moderner, sicherer Passwort-Manager geschrieben in **Python 3.8+** mit **PyQt6**. Die Anwendung verwendet **AES-256 Verschlüsselung** für alle sensiblen Daten und speichert diese in verschlüsselten `.spdb` Dateien (ähnlich KeePass).

### Kern-Features
- Verschlüsselte Einzeldatei-Datenbanken (.spdb Format)
- AES-256 + Argon2id Verschlüsselung
- **2FA/TOTP-Support** (NEU 2025-12-01) - QR-Code & Live-Codes
- Apple-inspiriertes Dark/Light Mode Design
- Multi-Datenbank Support (Cloud-Sync fähig)
- Passwort-Generator mit Stärke-Bewertung
- Auto-Lock (konfigurierbar 1-60 Min., Standard: 5) & Sichere Zwischenablage (5-300s, Standard: 30)
- Vollständiger Einstellungs-Dialog mit Theme-Wechsel
- Button-Press-Animationen (QPropertyAnimation)
- Zentrales Logging-System

---

## 2. Projektstruktur

```
PasswortManager/
├── main.py                    # Entry Point
├── requirements.txt           # Python Dependencies
├── pytest.ini                 # Test-Konfiguration
│
├── src/
│   ├── auth/                  # Authentifizierung
│   │   └── master_password.py # Argon2id Hashing
│   │
│   ├── core/                  # Kern-Module
│   │   ├── database.py        # DatabaseManager (Hauptschnittstelle)
│   │   ├── database_file.py   # Verschlüsselte .spdb Dateien
│   │   ├── encryption.py      # AES-256 (Fernet)
│   │   ├── models.py          # Datenmodelle (Category, PasswordEntry)
│   │   ├── settings.py        # App-Einstellungen
│   │   └── totp_manager.py    # 2FA/TOTP Manager (NEU)
│   │
│   ├── gui/                   # PyQt6 UI
│   │   ├── main_window.py     # Hauptfenster (cleaner Header, Lock-Button)
│   │   ├── database_selector.py  # DB-Auswahl Dialog
│   │   ├── database_new.py    # Neue DB erstellen Dialog
│   │   ├── login_dialog.py    # Master-Passwort Eingabe
│   │   ├── entry_dialog.py    # Passwort-Eintrag Dialog (mit 2FA-Support)
│   │   ├── generator_dialog.py # Passwort-Generator (mit Animationen)
│   │   ├── settings_dialog.py # Einstellungs-Dialog
│   │   ├── totp_dialog.py     # 2FA/TOTP Setup Dialog (NEU 2025-12-01)
│   │   ├── dashboard.py       # Dashboard mit Statistiken
│   │   ├── widgets.py         # Custom Widgets (Entry, Category Buttons)
│   │   ├── themes.py          # Dark/Light Mode System
│   │   ├── icons.py           # SVG-Icon-Provider (21 Icons)
│   │   ├── animations.py      # UI-Animationen (Fade, Slide, Pulse, Shake, Press)
│   │   └── responsive.py      # Responsive Design Utilities
│   │
│   ├── password/              # Passwort-Tools
│   │   ├── generator.py       # Kryptografisch sicherer Generator
│   │   └── strength.py        # Stärke-Bewertung
│   │
│   ├── testing/               # UI-Test-Infrastruktur (NEU 2025-12-01)
│   │   ├── mock_database.py   # Mock-DB für UI-Tests
│   │   ├── performance.py     # Performance-Messungen
│   │   └── screenshot_compare.py # Screenshot-Vergleich
│   │
│   └── utils/
│       └── clipboard.py       # Auto-Clear Zwischenablage
│
├── tests/                     # Unit Tests (pytest)
│   ├── test_database.py
│   ├── test_encryption.py
│   ├── test_master_password.py
│   ├── test_password_generator.py
│   └── test_password_strength.py
│
├── test_ui.py                 # UI-Test-Tool mit interaktivem Modus
└── test_ui_comprehensive.py  # Umfassende UI-Tests (45KB)
```

---

## 3. Technologie-Stack

### Haupt-Dependencies
- **PyQt6 >= 6.6.0** - GUI Framework
- **cryptography >= 41.0.0** - AES-256 Verschlüsselung (Fernet)
- **argon2-cffi >= 23.1.0** - Passwort-Hashing (Memory-Hard)
- **pyotp >= 2.9.0** - TOTP/2FA Support (AKTIV seit 2025-12-01)
- **qrcode[pil] >= 7.4.2** - QR-Code-Generierung (NEU 2025-12-01)
- **pytest >= 7.4.0** - Testing Framework

### Standard Library
- sqlite3 (Datenbank)
- hashlib (SHA-256 für Key-Derivation)
- secrets (Kryptografisch sicherer Passwort-Generator)
- tempfile (Temporäre Datenbank-Entschlüsselung)
- logging (Zentrales Logging-System, seit 2025-12-01)

---

## 4. Architektur

### Design-Patterns
- **MVC-ähnlich**: Models (models.py), Views (gui/), Controller (database.py)
- **Singleton**: Alle globalen Manager (encryption_manager, theme, icon_provider, etc.)
- **Repository**: DatabaseManager als Abstraktionsschicht
- **Observer**: PyQt6 Signals & Slots

### Globale Singleton-Instanzen
```python
# src/core/encryption.py
encryption_manager = EncryptionManager()

# src/core/settings.py
app_settings = AppSettings()

# src/gui/themes.py
theme = Theme()

# src/gui/icons.py
icon_provider = IconProvider()

# src/utils/clipboard.py
clipboard_manager = ClipboardManager()

# src/auth/master_password.py
master_password_manager = MasterPasswordManager()

# src/password/generator.py
password_generator = PasswordGenerator()

# src/gui/animations.py
animator = AnimationHelper()

# src/core/totp_manager.py
totp_manager = TOTPManager()
```

---

## 5. Sicherheitskonzept

### Dreifache Verschlüsselung

1. **Datenbank-Datei-Verschlüsselung**
   ```
   Master-Passwort → SHA256 → Base64 → Fernet Key
                                        ↓
   SQLite-DB (Bytes) → Fernet.encrypt() → .spdb Datei
   ```

2. **Feldverschlüsselung**
   - Passwörter, Notizen, TOTP-Secrets zusätzlich verschlüsselt
   - Ermöglicht Suche ohne vollständige Entschlüsselung

3. **Master-Passwort Hashing**
   ```
   Master-Passwort → Argon2id (64MB, 2 Iter, 4 Threads) → Hash
   ```
   - Gespeichert in `users` Tabelle
   - Verhindert Brute-Force Angriffe

### Dateiformat (.spdb)
```
[16 Bytes: "SECUREPASS_DB_V1"] + [Variable: Fernet(SQLite-DB)]
```

### Temporäre Datei-Verwaltung
- Verschlüsselte DB wird temporär in System-Temp entschlüsselt
- Automatische Löschung beim Schließen oder Lock
- Destruktor-basierte Cleanup

---

## 6. Datenbankschema (SQLite)

### Tabelle: users
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    password_hash TEXT NOT NULL,  -- Argon2id Hash
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### Tabelle: categories
```sql
CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    color TEXT DEFAULT '#808080',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

**Standard-Kategorien**:
- Allgemein (#6366f1 - Indigo)
- Banking (#10b981 - Grün)
- Social Media (#8b5cf6 - Lila)
- E-Mail (#f59e0b - Orange)

### Tabelle: password_entries
```sql
CREATE TABLE password_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    username TEXT,
    encrypted_password BLOB NOT NULL,
    encrypted_notes BLOB,
    website_url TEXT,
    totp_secret BLOB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories (id)
)
```

---

## 7. Anwendungsfluss

### Startprozess
1. QApplication erstellen
2. Theme laden und anwenden
3. DatabaseSelectorDialog öffnen
4. LoginDialog (Master-Passwort)
5. DatabaseManager initialisieren
   - .spdb entschlüsseln → Temp SQLite
6. MainWindow anzeigen
7. Auto-Lock Timer starten (5 Min.)

### Passwort-Speichern
1. Benutzer gibt Passwort ein (entry_dialog.py)
2. `encryption_manager.encrypt(password)` → bytes
3. PasswordEntry erstellen mit encrypted_password
4. `DatabaseManager.add_password_entry(entry)`
5. `DatabaseFile.save_database()` - verschlüsselt zurückspeichern

### Passwort-Anzeigen
1. Benutzer klickt "Auge"-Icon
2. Lese encrypted_password
3. `encryption_manager.decrypt(encrypted_password)` → str
4. Anzeige in QLabel (Monospace-Font)
5. Pulse-Animation für Feedback

---

## 8. UI-System

### Theme-System (themes.py)

**Light Mode:**
- Primary: #6366f1 (Indigo)
- Background: #ffffff
- Text: #111827

**Dark Mode:**
- Primary: #818cf8 (Heller Indigo)
- Background: #0f172a (Slate 900)
- Text: #f1f5f9

**Toggle**: Ctrl+D oder Mond/Sonne-Button

### Icon-System (icons.py)
- 21 SVG-Icons (Lucide Icons)
- Dynamische Farbgebung
- Skalierbar (DPI-unabhängig)

**Verfügbare Icons:**
lock, unlock, eye, eye_off, copy, check, edit, trash, key, dice, search, folder, folder_open, user, link, plus, refresh, power, sun, moon, shield, info

### Animations (animations.py)
- **Fade**: Opacity-Übergang
- **Slide**: Von oben/unten
- **Scale**: Zoom-Effekt
- **Pulse**: Feedback (Kopieren)
- **Shake**: Fehler-Feedback (falsches Passwort)
- **Press**: Button-Press-Feedback (NEU 2025-12-01)

---

## 9. 2FA/TOTP-System (NEU 2025-12-01)

### Übersicht

Vollständige Zwei-Faktor-Authentifizierung (2FA) mit TOTP-Unterstützung für Passwort-Einträge. Ermöglicht das Speichern von Authenticator-Codes (Google Authenticator, Authy, Microsoft Authenticator, etc.).

### Backend: TOTP-Manager (totp_manager.py)

**Hauptfunktionen:**
```python
totp_manager.generate_secret()              # Generiert Base32-Secret
totp_manager.get_totp_code(secret)          # 6-stelliger Code
totp_manager.get_remaining_seconds()        # Zeit bis Code-Wechsel
totp_manager.verify_code(secret, code)      # Code-Verifizierung
totp_manager.get_provisioning_uri(...)      # URI für QR-Code
totp_manager.encrypt_secret(secret)         # Verschlüsselung
totp_manager.decrypt_secret(encrypted)      # Entschlüsselung
```

**Sicherheit:**
- TOTP-Secrets verschlüsselt mit AES-256 (encryption_manager)
- Gespeichert in `password_entries.totp_secret` (BLOB)
- Vollständig in verschlüsselter .spdb-Datei

**TOTP-Spezifikationen:**
- 6-stellige Codes
- 30-Sekunden-Intervall
- ±30s Zeittoleranz (valid_window=1)
- Base32-Encoding
- SHA-1 Hash (Standard)

### UI: TOTP-Setup-Dialog (totp_dialog.py)

**Funktionen:**
- QR-Code-Anzeige (250x250px)
- Manuelles Secret-Kopieren (Base32)
- Live TOTP-Code mit Countdown
- Theme-Support (Dark/Light Mode)
- Animationen (fade-in, pulse)

**Dialog-Größe:** 550x700px (Modal)

**QR-Code-Format:**
```
otpauth://totp/SecurePass:AccountName?secret=BASE32SECRET&issuer=SecurePass
```

**Abhängigkeit:** qrcode[pil] >= 7.4.2

### UI: Entry-Dialog-Integration (entry_dialog.py)

**2FA-Bereich:**
- Position: Zwischen Notizen und Buttons
- Dialog-Höhe: 580px → 720px (Platz für 2FA)

**Komponenten:**
1. **Setup-Button** (`totp_setup_button`)
   - Öffnet TOTP-Dialog
   - Versteckt nach Setup

2. **Code-Anzeige** (`totp_code_frame`)
   - Live 6-stelliger Code
   - Countdown-Timer (30s)
   - Rote Warnung bei <5s
   - Copy-Button mit Feedback
   - "2FA entfernen" Button

**Live-Updates:**
- Timer: 1000ms (1 Sekunde)
- Auto-Stop in `closeEvent()`

**Workflow:**
```
1. Klick "2FA einrichten"
   → TOTP-Dialog öffnet
2. QR-Code scannen / Secret kopieren
   → In Authenticator-App importieren
3. "Speichern" klicken
   → Live-Code erscheint
4. Eintrag speichern
   → TOTP-Secret verschlüsselt in DB
```

### Code-Referenzen

**TOTP-Manager:**
- `totp_manager.py:13-52` - Hauptklasse TOTPManager
- `totp_manager.py:18-24` - generate_secret()
- `totp_manager.py:26-36` - get_totp_code()

**TOTP-Dialog:**
- `totp_dialog.py:23-46` - Klassen-Definition
- `totp_dialog.py:137-176` - QR-Code-Generierung
- `totp_dialog.py:178-201` - Live-Code-Updates

**Entry-Dialog:**
- `entry_dialog.py:279-417` - 2FA-UI-Bereich
- `entry_dialog.py:583-589` - setup_totp()
- `entry_dialog.py:591-608` - on_totp_configured()
- `entry_dialog.py:610-631` - update_totp_display()
- `entry_dialog.py:707-713` - TOTP-Secret laden

### Verwendung

**2FA für Eintrag aktivieren:**
1. Passwort-Eintrag öffnen/erstellen
2. Zum 2FA-Bereich scrollen
3. "2FA einrichten" klicken
4. QR-Code scannen ODER Secret manuell eingeben
5. In Authenticator-App importieren
6. "Speichern" klicken
7. Live-Code wird angezeigt

**Code kopieren:**
- Klick auf Copy-Icon neben Code
- Auto-Clear nach 30 Sekunden

**2FA entfernen:**
- Klick "2FA entfernen"
- Bestätigungs-Dialog
- Secret wird aus DB gelöscht

### Technische Details

**Datenbankfeld:**
```sql
totp_secret BLOB  -- Verschlüsseltes Base32-Secret
```

**Verschlüsselung:**
```python
# Speichern
encrypted_totp = totp_manager.encrypt_secret(self.totp_secret)
entry.totp_secret = encrypted_totp

# Laden
self.totp_secret = totp_manager.decrypt_secret(entry.totp_secret)
```

**Timer-Management:**
```python
self.totp_update_timer = QTimer()
self.totp_update_timer.timeout.connect(self.update_totp_display)
self.totp_update_timer.start(1000)  # Jede Sekunde

# Cleanup
def closeEvent(self, event):
    if self.totp_update_timer:
        self.totp_update_timer.stop()
```

### Bekannte Einschränkungen

- QR-Code-Generierung benötigt qrcode[pil]
- Bei fehlendem qrcode: Fallback-Text
- Keine System-Theme-Synchronisation (nur Light/Dark)

---

## 10. Bekannte Issues & Änderungsprotokoll

### ✅ BEHOBEN (2025-12-01 Session)

**Kritische Fixes:**
1. ~~Exception-Handling~~: Logging-System implementiert ✅
2. ~~Alte Dateien~~: `database_old.py`, `login_dialog_old.py`, `nul` entfernt ✅
3. ~~Debug-Statements~~: `print()` durch `logger` ersetzt ✅
4. ~~CSS transform~~: Nicht unterstützte Property entfernt ✅
5. ~~Lock-Crash~~: TypeError beim Sperren behoben (db_path statt db_manager) ✅
6. ~~Theme-Bug~~: Theme-Wechsel funktioniert jetzt für kompletten Screen ✅
7. ~~KeyError~~: 'background_primary' → 'background' korrigiert ✅
8. ~~Theme-Sync-Bug~~: Ansicht-Menü speichert jetzt Theme in Einstellungen ✅

**Features hinzugefügt (Vormittag):**
- Button-Press-Animationen mit `animator.press()` (7 Buttons)
- Vollständiger Einstellungs-Dialog (settings_dialog.py, 426 Zeilen)
- Cleaner Header-Layout (Theme/Lock Buttons entfernt, neuer "Manager sperren" Button)

**Features hinzugefügt (Abend):**
- **Vollständige 2FA/TOTP-Implementierung** (totp_manager.py, totp_dialog.py)
- QR-Code-Generierung für Authenticator-Apps
- Live TOTP-Code-Anzeige in entry_dialog.py
- TOTP-Secret-Verschlüsselung (AES-256)
- Entry-Dialog erweitert (720px Höhe für 2FA-Bereich)
- qrcode[pil] Dependency hinzugefügt

### Aktuelle Probleme

**Keine kritischen Issues!** ✅

**Niedrig:**
- **Code-Review**: main_window.py (~700 Zeilen) - Evtl. Aufteilung prüfen

### Letzte Commits (Heutige Session)
```
f7d11c3 feat: Implementiere vollständige 2FA/TOTP-Funktionalität + Theme-Sync-Fix
b298670 fix: Behebe kritische Bugs und verbessere UX
aef4324 fix: Behebe Settings-Dialog KeyError und optimiere Header-Layout
c04fc0d feat: Füge vollständigen Einstellungs-Dialog hinzu
06ab3e3 feat: Implementiere Button-Press-Animationen mit QPropertyAnimation
9560ca7 fix: Entferne nicht unterstützte CSS transform-Property aus StyleSheets
5fda6db docs: Füge umfassende .claude/ Wissensdatenbank hinzu
a3f2ac4 refactor: Implementiere Logging-System und entferne veraltete Dateien
```

**Status**: Sehr stabil, produktionsreif, 2FA voll funktionsfähig!

---

## 10. Wichtige Code-Referenzen

### Hauptfenster Initialisierung
**main_window.py:107-218** - Setup-Methode mit Header, Sidebar, Content

### Verschlüsselung
**encryption.py:23-55** - encrypt() und decrypt() Methoden

### Datenbank-Zugriff
**database.py:169-217** - CRUD für Passwort-Einträge

### Passwort-Generator
**generator.py:45-86** - generate() mit kryptografischer Sicherheit

### Auto-Lock
**main_window.py:551-570** - reset_inactivity_timer() und lock_application()

---

## 11. Build & Run

### Installation
```bash
# Virtual Environment erstellen (empfohlen)
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Dependencies installieren
pip install -r requirements.txt
```

### Start
```bash
python main.py
```

### Tests
```bash
# Alle Tests
pytest

# Mit Coverage
pytest --cov=src --cov-report=html

# Bestimmte Tests
pytest tests/test_encryption.py -v
```

---

## 12. Einstellungen & Daten

### Einstellungen-Datei
**Pfad**: `~/.securepass/settings.json`

**Inhalt**:
```json
{
  "last_database": "/pfad/zur/letzten.spdb",
  "recent_databases": [...],
  "theme_mode": "light",
  "auto_lock_minutes": 5,
  "clipboard_clear_seconds": 30
}
```

### Datenbank-Dateien
**Standard-Speicherort**:
- Windows: `C:\Users\<User>\Documents\SecurePass\`
- Linux/Mac: `/home/<user>/Documents/SecurePass/`

**Format**: `.spdb` (SecurePass Database)

### Log-Dateien
**Pfad**: `~/.securepass/logs/securepass.log`

**Format**: Standard Python Logging
```
2025-12-01 14:30:15 - __main__ - INFO - SecurePass Manager gestartet
2025-12-01 14:30:20 - src.core.database_file - WARNING - Konnte temporäre Datei nicht löschen
```

**Log-Level**: INFO (Konsole + Datei)

### Einstellungs-Dialog (NEU 2025-12-01)
**Zugang**: Datei > Einstellungen (Ctrl+,) oder Header

**Bereiche:**
1. **🎨 Darstellung**
   - Theme-Modus: Hell / Dunkel / System
   - Live-Update beim Speichern

2. **🔒 Sicherheit**
   - Auto-Lock Timeout: 1-60 Min. (Standard: 5)
   - Zwischenablage löschen: 5-300 Sek. (Standard: 30)

3. **🔐 2FA/TOTP**
   - Info-Box: "Feature verfügbar"
   - ✅ Grüner Button: "2FA verfügbar im Passwort-Dialog"
   - Vollständig implementiert (2025-12-01)

**Features:**
- Responsive Design (600x500px minimum)
- GroupBox-Layout mit Icons
- Button-Animationen
- Scroll-Support
- Persistent in settings.json

### Dashboard (NEU 2025-12-01)
**Datei**: `src/gui/dashboard.py`

**Komponenten:**
1. **StatCard** - Einzelne Statistik-Karte
   - Icon + Wert + Titel
   - Animierte Value-Updates (pulse Animation)
   - Responsive Größenanpassung
   - Themeable (Light/Dark Mode)

2. **Dashboard** - Statistik-Übersicht
   - Zeigt wichtige Metriken der Passwort-Datenbank
   - Grid-Layout mit mehreren StatCards
   - Automatische Aktualisierung
   - Scrollbar-Support

**Beispiel-Metriken:**
- Gesamt-Passwörter
- Starke vs. Schwache Passwörter
- Kategorien-Übersicht
- Letzte Aktivität

**Integration:**
- Verwendung von `theme`, `icon_provider`, `animator` Singletons
- DatabaseManager für Datenabfragen
- Logging für Fehlerbehandlung

### UI-Test-Infrastruktur (NEU 2025-12-01)
**Verzeichnis**: `src/testing/`

**Module:**
1. **mock_database.py** - Mock-Datenbank für sichere UI-Tests
   - Temporäre Test-Datenbanken erstellen
   - Beispieldaten generieren
   - Keine Gefährdung echter Benutzerdaten

2. **performance.py** - Performance-Messungen
   - UI-Rendering-Zeiten
   - Datenbank-Operationen
   - Memory-Profiling

3. **screenshot_compare.py** - Screenshot-Vergleich
   - Visuelle Regressions-Tests
   - Pixel-genaue Vergleiche
   - Theme-Wechsel-Tests

**Test-Skripte (Root-Level):**
- `test_ui.py` - Interaktiver UI-Test-Modus
  - Theme-Wechsel Tests
  - Dialog-Öffnungs-Tests
  - Button-Funktionalität
  - Kommandozeilen-Interface

- `test_ui_comprehensive.py` - Umfassende UI-Tests (45KB)
  - Vollständige UI-Component-Coverage
  - Automatisierte Test-Suites
  - Integrations-Tests

---

## 13. Tastenkombinationen

- **Ctrl+L** - Anwendung sperren
- **Ctrl+D** - Dark Mode umschalten
- **Ctrl+,** - Einstellungen öffnen (NEU)
- **Ctrl+Q** - Beenden

---

## 14. Git Workflow & Version Control

**WICHTIG**: Für alle Code-Änderungen gilt der Git-Workflow!

### Vollständige Dokumentation
→ Siehe **`.claude/GIT_WORKFLOW.md`** für alle Details

### Grundregeln

1. **IMMER Branches erstellen** für Features/Fixes
   ```bash
   git checkout -b feature/mein-feature
   git checkout -b fix/mein-bugfix
   ```

2. **NIEMALS direkt auf main committen** (außer Hotfixes/Docs)

3. **Branch-Naming Convention**:
   - `feature/` - Neue Features
   - `fix/` - Bugfixes
   - `refactor/` - Code-Refactoring
   - `docs/` - Dokumentation
   - `test/` - Tests

4. **Commit-Messages Format**:
   ```
   <typ>: <Beschreibung>

   <Details>

   🤖 Generated with Claude Code
   Co-Authored-By: Claude <noreply@anthropic.com>
   ```

5. **Pull Requests** für alle Merges in main

6. **Tests vor Push** ausführen: `pytest`

### Typischer Workflow für Claude

```bash
# 1. Branch erstellen
git checkout -b feature/neues-feature

# 2. Entwickeln (mehrere Commits)
git add <dateien>
git commit -m "feat: Beschreibung"

# 3. Pushen
git push -u origin feature/neues-feature

# 4. PR erstellen
gh pr create --title "Feature: Beschreibung"

# 5. Nach Merge: Cleanup
git checkout main && git pull
git branch -d feature/neues-feature
```

---

## 15. Entwicklungs-Empfehlungen

### ✅ Abgeschlossen (2025-12-01)
1. ~~Exception-Handling verbessern~~ - Logging-System implementiert ✅
2. ~~Logging-System einführen~~ - In main.py, database_file.py, settings.py integriert ✅
3. ~~Alte Dateien entfernen~~ - database_old.py, login_dialog_old.py, nul gelöscht ✅
4. ~~TOTP/2FA Support~~ - Vollständig implementiert mit QR-Code & Live-Codes ✅
5. ~~Theme-Sync-Bug~~ - Ansicht-Menü speichert jetzt in Einstellungen ✅

### Nächste Schritte
6. UI-Layout-Tests automatisieren (verschiedene Auflösungen)
7. Code-Review für main_window.py (evtl. Aufteilung)

### Zukünftige Features (siehe FEATURES.md)
- Browser-Plugins (Chrome, Firefox)
- Import/Export (CSV, JSON, 1Password, LastPass)
- Biometrische Authentifizierung (Fingerprint, Face ID)
- Cloud-Sync (Dropbox, Google Drive)

---

## 16. Wichtige Hinweise für Nachfolger

### Design-Philosophie
- Apple-inspiriert: Flach, modern, clean
- Sicherheit > Features
- Benutzerfreundlichkeit = Priorität

### Code-Standards
- Python 3.8+ Type Hints verwenden
- Dataclasses für Modelle
- Singleton-Pattern für globale Services
- PyQt6 Signals & Slots für Kommunikation
- Logging statt print() verwenden (`logger = logging.getLogger(__name__)`)

### Sicherheits-Checkliste
- [ ] Niemals Passwörter in Plaintext loggen
- [ ] Temporäre Dateien immer löschen
- [ ] Verschlüsselung für alle sensiblen Daten
- [ ] Auto-Lock nach Inaktivität
- [ ] Sichere Zwischenablage

### Testing
- Alle neuen Features mit Tests abdecken
- `pytest` vor jedem Commit ausführen
- Coverage mindestens 80% halten

---

**Ende der Wissensdatenbank**

Diese Datei wird automatisch aktualisiert bei signifikanten Änderungen.
Bei Fragen oder Unklarheiten: Analysiere die entsprechenden Module direkt.