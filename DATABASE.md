# Datenbank-System Dokumentation

## Überblick

SecurePass Manager verwendet ein verschlüsseltes Datenbank-Datei-System ähnlich wie KeePass. Die gesamte SQLite-Datenbank wird mit AES-256 verschlüsselt und in einer einzigen `.spdb` Datei gespeichert.

## Dateiformat: .spdb (SecurePass Database)

### Struktur

```
[16 Bytes Header] + [Verschlüsselte SQLite-Datenbank]
```

- **Header**: `SECUREPASS_DB_V1` (16 Bytes)
- **Verschlüsselung**: AES-256 via Python Fernet
- **Key Derivation**: SHA-256 Hash des Master-Passworts

### Vorteile

✅ **Cloud-Sync fähig**: Eine einzige Datei, einfach zu synchronisieren
✅ **Portabel**: Gesamte Datenbank in einer Datei
✅ **Sicher**: Vollständige AES-256 Verschlüsselung
✅ **Flexibel**: Speicherort frei wählbar
✅ **Multi-Datenbank**: Mehrere Datenbanken gleichzeitig möglich

## Workflow

### 1. Beim ersten Start

```
Keine letzte Datenbank gefunden
    ↓
Database Selector Dialog
    ↓
Wähle: "Neue Datenbank erstellen"
    ↓
New Database Dialog
    ├─ Datenbank-Name eingeben
    ├─ Speicherort wählen
    └─ Master-Passwort festlegen
    ↓
Datenbank wird erstellt (.spdb Datei)
    ↓
Login Dialog (automatisch mit gesetztem Passwort)
    ↓
Hauptfenster öffnet sich
```

### 2. Beim normalen Start

```
Letzte Datenbank gefunden
    ↓
Database Selector Dialog (mit Kürzlich-Liste)
    ↓
Wähle Datenbank aus Liste ODER
    ├─ Neue Datenbank erstellen
    └─ Andere Datenbank öffnen
    ↓
Login Dialog
    ├─ Master-Passwort eingeben
    └─ Datenbank wird entschlüsselt
    ↓
Hauptfenster öffnet sich
```

### 3. Cloud-Sync Workflow

```
Auf Computer A:
    Datenbank in Cloud-Ordner erstellen
    (z.B. Dropbox/SecurePass/Meine Passwörter.spdb)
    ↓
    Passwörter hinzufügen/bearbeiten
    ↓
    Beim Schließen: Automatisch in .spdb gespeichert
    ↓
    Cloud synchronisiert automatisch

Auf Computer B:
    SecurePass Manager öffnen
    ↓
    "Datenbank öffnen" wählen
    ↓
    Zur Cloud-Datei navigieren
    ↓
    Master-Passwort eingeben
    ↓
    Zugriff auf alle Passwörter!
```

## Technische Details

### DatabaseFile Klasse

Hauptklasse für verschlüsselte Datenbank-Operationen.

```python
from src.core.database_file import DatabaseFile

# Neue Datenbank erstellen
db_file = DatabaseFile("pfad/zur/datenbank.spdb")
db_file.create_new("mein-master-passwort")

# Bestehende Datenbank öffnen
db_file = DatabaseFile("pfad/zur/datenbank.spdb")
temp_db_path = db_file.open_database("mein-master-passwort")

# Änderungen speichern
db_file.save_database(temp_db_path)

# Schließen und aufräumen
db_file.close_database()
```

### DatabaseManager Klasse

Arbeitet mit verschlüsselten Dateien.

```python
from src.core.database import DatabaseManager

# Öffne verschlüsselte Datenbank
db_manager = DatabaseManager(
    encrypted_db_path="pfad/zur/datenbank.spdb",
    master_password="mein-passwort"
)

# Normale Operationen
categories = db_manager.get_all_categories()
entries = db_manager.get_all_password_entries()

# Änderungen werden automatisch gespeichert
entry = PasswordEntry(...)
db_manager.add_password_entry(entry)  # Speichert in .spdb

# Schließen
db_manager.close()
```

### Settings Klasse

Verwaltet Benutzereinstellungen.

```python
from src.core.settings import app_settings

# Letzte Datenbank speichern
app_settings.set_last_database("/pfad/zur/db.spdb")

# Letzte Datenbank abrufen
last_db = app_settings.get_last_database()

# Kürzlich verwendete Datenbanken
recent = app_settings.get_recent_databases()  # Liste der letzten 5
```

**Speicherort**: `~/.securepass/settings.json`

**Format**:
```json
{
  "last_database": "/pfad/zur/letzten.spdb",
  "recent_databases": [
    "/pfad/zur/letzten.spdb",
    "/pfad/zur/zweitletzten.spdb"
  ],
  "theme_mode": "light",
  "auto_lock_minutes": 5,
  "clipboard_clear_seconds": 30
}
```

## Standard-Speicherorte

### Windows
```
Datenbanken: C:\Users\<Username>\Documents\SecurePass\
Settings:    C:\Users\<Username>\.securepass\settings.json
```

### Linux/Mac
```
Datenbanken: /home/<username>/Documents/SecurePass/
Settings:    /home/<username>/.securepass/settings.json
```

## Sicherheitsaspekte

### Verschlüsselung

1. **Master-Passwort → Encryption Key**
   ```python
   key = SHA256(master_password).digest()
   key = base64.urlsafe_b64encode(key)  # Fernet-kompatibel
   ```

2. **Datenbank verschlüsseln**
   ```python
   fernet = Fernet(key)
   encrypted_data = fernet.encrypt(sqlite_database_bytes)
   ```

3. **In Datei schreiben**
   ```
   FILE: [Header: 16 bytes] + [Encrypted Data: variable]
   ```

### Temporäre Dateien

- Beim Öffnen: SQLite-DB temporär entschlüsselt
- Speicherort: System temp directory
- **Automatisch gelöscht**:
  - Bei normalem Schließen
  - Im Destruktor
  - Bei Exceptions

⚠️ **Wichtig**: Bei Systemabsturz können temp-Dateien übrig bleiben!

### Master-Passwort Hash

Zusätzlich zum Verschlüsselungs-Key wird ein Argon2id Hash in der Datenbank gespeichert:

```python
# Bei Datenbank-Erstellung
password_hash = master_password_manager.hash_password(password)
db.save_master_password_hash(password_hash)

# Bei Login
if master_password_manager.verify_password(input_password, stored_hash):
    # Passwort korrekt
```

**Warum zwei Mechanismen?**
- **Fernet-Verschlüsselung**: Schützt Datenbank-Datei
- **Argon2id Hash**: Verhindert Brute-Force auf Master-Passwort

## Migration von alter Version

Falls du eine alte unverschlüsselte `data/passwords.db` hast:

### Automatisches Migrations-Script

```python
# migrate_old_db.py
import sqlite3
from src.core.database_file import DatabaseFile

# Lese alte Datenbank
old_conn = sqlite3.connect("data/passwords.db")

# Erstelle neue verschlüsselte Datenbank
new_db = DatabaseFile("Documents/SecurePass/Migriert.spdb")
new_db.create_new("neues-master-passwort")

# Öffne verschlüsselte DB
temp_path = new_db.open_database("neues-master-passwort")
new_conn = sqlite3.connect(temp_path)

# Kopiere Daten
old_cursor = old_conn.cursor()
new_cursor = new_conn.cursor()

# Kategorien kopieren
old_cursor.execute("SELECT * FROM categories")
for row in old_cursor.fetchall():
    new_cursor.execute("INSERT INTO categories VALUES (?, ?, ?, ?)", row)

# Password Entries kopieren
old_cursor.execute("SELECT * FROM password_entries")
for row in old_cursor.fetchall():
    new_cursor.execute("INSERT INTO password_entries VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", row)

# Users kopieren
old_cursor.execute("SELECT * FROM users")
for row in old_cursor.fetchall():
    new_cursor.execute("INSERT INTO users VALUES (?, ?, ?)", row)

new_conn.commit()
new_conn.close()

# Speichere verschlüsselt
new_db.save_database(temp_path)
new_db.close_database()

old_conn.close()

print("Migration abgeschlossen!")
```

## Best Practices

### Cloud-Sync

✅ **Empfohlen:**
- Dropbox, Google Drive, OneDrive, iCloud
- Automatische Synchronisierung
- Versionierung aktivieren (für Wiederherstellung)

❌ **Nicht empfohlen:**
- Unverschlüsselte Cloud-Dienste ohne 2FA
- Öffentliche Freigaben
- USB-Sticks ohne Backup

### Backup-Strategie

1. **Automatisches Cloud-Backup**
   - Datenbank in Cloud-Ordner speichern
   - Automatisch synchronisiert

2. **Manuelle Backups**
   ```
   Wöchentlich: Kopiere .spdb Datei
   Speichere an: Externen Speicher + Cloud
   ```

3. **Versionierung**
   - Viele Cloud-Dienste bewahren alte Versionen auf
   - Bei Korruption: Alte Version wiederherstellen

### Master-Passwort

✅ **Gutes Master-Passwort:**
- Mindestens 16 Zeichen
- Kombination aus Wörtern + Zahlen + Sonderzeichen
- Einzigartig (nur für diese Datenbank)
- Passphrase: "Kaffee-Tasse_42_Rote_Wolke!"

❌ **Vermeiden:**
- Wiederverwendung von anderen Passwörtern
- Zu kurz (< 12 Zeichen)
- Nur Wörter aus Wörterbuch
- Persönliche Infos (Geburtsdatum, Namen)

⚠️ **WICHTIG**: Kein Passwort-Recovery möglich!

## Fehlerbehebung

### Fehler: "Falsches Master-Passwort"

**Ursachen:**
1. Tatsächlich falsches Passwort
2. Datenbank beschädigt
3. Falsche Verschlüsselung

**Lösung:**
1. Passwort erneut sorgfältig eingeben
2. Falls Cloud-Sync: Alte Version wiederherstellen
3. Aus Backup wiederherstellen

### Fehler: "Ungültiges Dateiformat"

**Ursachen:**
1. Keine .spdb Datei
2. Datei beschädigt
3. Falsche Version

**Lösung:**
1. Prüfe Dateiendung (.spdb)
2. Prüfe Dateigröße (sollte > 0 sein)
3. Aus Backup wiederherstellen

### Temporäre Dateien bleiben übrig

**Nach Absturz:**
```bash
# Windows
del %TEMP%\*.db

# Linux/Mac
rm /tmp/*.db
```

**Hinweis:** Nur sichere, wenn SecurePass nicht läuft!

## API-Referenz

### DatabaseFile

```python
class DatabaseFile:
    def __init__(self, file_path: str, master_password: str = None)
    def create_new(self, master_password: str) -> None
    def open_database(self, master_password: str) -> str
    def save_database(self, temp_db_path: str) -> None
    def close_database(self) -> None
    def change_master_password(self, old: str, new: str) -> None

    @staticmethod
    def is_valid_database_file(file_path: str) -> bool

    @staticmethod
    def get_default_database_path() -> Path
```

### AppSettings

```python
class AppSettings:
    def get(self, key: str, default=None) -> Any
    def set(self, key: str, value: Any) -> None
    def save(self) -> None

    def get_last_database(self) -> Optional[str]
    def set_last_database(self, path: str) -> None
    def get_recent_databases(self) -> List[str]
    def clear_recent_databases(self) -> None
```

## Changelog

### Version 1.1 (Aktuelle Version)

**Neu:**
- ✅ Verschlüsselte .spdb Dateiformat
- ✅ KeePass-style Datenbank-Auswahl
- ✅ Cloud-Sync Unterstützung
- ✅ Mehrere Datenbanken möglich
- ✅ Frei wählbarer Speicherort
- ✅ Settings-Persistierung
- ✅ Kürzlich verwendete Datenbanken

**Breaking Changes:**
- ⚠️ Altes Format (data/passwords.db) nicht mehr kompatibel
- ⚠️ Migration erforderlich (siehe oben)

---

**Stand**: November 2025
**Version**: 1.1.0
