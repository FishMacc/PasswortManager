# Code-Konventionen für SecurePass Manager

Projekt-spezifische Code-Standards und Best Practices.

---

## 🎯 Übersicht

Dieses Dokument definiert:
- Code-Style (PEP 8 + Projekt-spezifisch)
- Projektstruktur-Konventionen
- Naming Conventions
- Import-Reihenfolge
- Wo neue Dateien hinzufügen

---

## 📐 Code-Style

### Basis: PEP 8

**Allgemein:**
- Python 3.8+ Features erlaubt
- Line Length: **100 Zeichen** (nicht 79!)
- Indentation: **4 Spaces** (keine Tabs)
- Encoding: **UTF-8**

### Type Hints (empfohlen, nicht verpflichtend)

```python
# ✅ Gut - mit Type Hints
def encrypt(self, plaintext: str) -> bytes:
    return self._fernet.encrypt(plaintext.encode('utf-8'))

# ⚠️ Ok - ohne Type Hints (Legacy-Code)
def encrypt(self, plaintext):
    return self._fernet.encrypt(plaintext.encode('utf-8'))
```

**Für neuen Code:** Type Hints verwenden
**Für Legacy-Code:** Optional hinzufügen bei Änderungen

---

### Docstrings (empfohlen für öffentliche APIs)

**Format:** Google-Style

```python
def add_password_entry(self, entry: PasswordEntry) -> int:
    """Fügt einen Passwort-Eintrag zur Datenbank hinzu.

    Args:
        entry: PasswordEntry-Objekt mit allen Daten

    Returns:
        int: ID des eingefügten Eintrags

    Raises:
        DatabaseError: Falls Einfügen fehlschlägt
        ValueError: Falls entry ungültig ist
    """
    # ...
```

**Für neuen Code:** Docstrings für öffentliche Methoden
**Für interne Methoden:** Optional

---

### Imports

**Reihenfolge (PEP 8):**
```python
# 1. Standard Library
import os
import sys
from pathlib import Path

# 2. Third-Party
from PyQt6.QtWidgets import QWidget
from cryptography.fernet import Fernet
import pytest

# 3. Local/Project
from src.core.encryption import encryption_manager
from src.core.models import PasswordEntry
```

**Gruppierung:**
- Alphabetisch innerhalb jeder Gruppe
- Leere Zeile zwischen Gruppen

**Import-Style:**
```python
# ✅ Bevorzugt - Explizit
from src.core.encryption import EncryptionManager

# ⚠️ Ok - Für häufig genutzte
from src.gui.themes import theme
from src.gui.icons import icon_provider

# ❌ Vermeide - Star-Imports
from src.core import *  # NICHT NUTZEN!
```

---

## 📁 Projektstruktur-Konventionen

### Wo neue Dateien hinzufügen?

#### 1. Neue Core-Logik

**Szenario:** Neue Business-Logik (z.B. Backup, Export)

**Struktur:**
```
src/
├── core/           # Bestehend
└── backup/         # NEU
    ├── __init__.py
    ├── manager.py
    └── strategies.py
```

**Pattern:**
- Eigenes Modul-Verzeichnis unter `src/`
- `__init__.py` für Public API
- `manager.py` für Haupt-Klasse
- Weitere Dateien bei Bedarf

---

#### 2. Neue UI-Komponente

**Szenario:** Neuer Dialog oder Widget

**Struktur:**
```
src/gui/
├── main_window.py     # Bestehend
├── export_dialog.py   # NEU - Dialog
└── widgets.py         # ERWEITERN - oder neue Datei?
```

**Regel:**
- **Einzelne große Komponente:** Eigene Datei (`export_dialog.py`)
- **Kleine wiederverwendbare Widgets:** In `widgets.py` hinzufügen
- **Viele verwandte Widgets:** Eigenes `widgets/` Verzeichnis

**Beispiel - Eigenes Verzeichnis:**
```
src/gui/widgets/
├── __init__.py
├── password_entry.py
├── category_button.py
└── search_bar.py
```

---

#### 3. Neue Tests

**Pattern:** Mirror der Source-Struktur

```
src/backup/manager.py    →    tests/test_backup.py
src/gui/export_dialog.py →    tests/test_export_dialog.py (UI-Tests optional)
```

**Naming:**
- `test_<module_name>.py`
- Test-Funktionen: `test_<function_name>_<scenario>()`

---

#### 4. Neue Utility-Funktion

**Struktur:**
```
src/utils/
├── clipboard.py      # Bestehend
├── validators.py     # NEU - Input-Validierung
└── formatters.py     # NEU - String-Formatierung
```

**Regel:**
- Thematisch gruppieren
- Nicht alles in eine `utils.py` Datei!

---

## 🏷️ Naming Conventions

### Dateien & Module

```python
# ✅ Snake-Case für Dateien
database_manager.py
password_entry.py
totp_manager.py

# ❌ Nicht
DatabaseManager.py  # PascalCase nur für Klassen
passwordEntry.py    # camelCase nicht für Dateien
```

---

### Klassen

```python
# ✅ PascalCase
class DatabaseManager:
    pass

class PasswordEntry:
    pass

class TOTPManager:  # Akronyme groß
    pass

# ❌ Nicht
class database_manager:  # Snake-Case
class passwordentry:     # Kleingeschrieben
```

---

### Funktionen & Methoden

```python
# ✅ Snake-Case, Verb-basiert
def get_password_entry(entry_id):
    pass

def encrypt_password(plaintext):
    pass

def validate_user_input(text):
    pass

# ❌ Nicht
def PasswordEntry():     # PascalCase (Klasse!)
def GetEntry():          # camelCase
def entry():             # Nicht-deskriptiv
```

---

### Variablen

```python
# ✅ Snake-Case, deskriptiv
password_entry = ...
encryption_key = ...
max_retries = 3

# ⚠️ Ok für kurze Scopes
for i in range(10):
    pass

for entry in entries:  # Singular in Plural-Loop
    pass

# ❌ Nicht
pwdEntry = ...          # camelCase
e = ...                 # Zu kurz
PasswordEntry = ...     # PascalCase (Klasse!)
```

---

### Konstanten

```python
# ✅ SCREAMING_SNAKE_CASE
MAX_PASSWORD_LENGTH = 64
DEFAULT_TIMEOUT = 5 * 60 * 1000  # 5 Minuten in ms
DATABASE_VERSION = "1.0"

# ❌ Nicht
maxPasswordLength = 64
Max_Password_Length = 64
```

---

### Private Members

```python
class Example:
    def __init__(self):
        self.public_var = 1        # Public
        self._protected_var = 2    # Protected (Konvention)
        self.__private_var = 3     # Private (Name-Mangling)

    def public_method(self):       # Public
        pass

    def _internal_method(self):    # Internal/Protected
        pass

    def __private_method(self):    # Private (selten genutzt)
        pass
```

**Faustregel:**
- `_single_underscore` für Interna (meistens verwendet)
- `__double_underscore` nur bei Namens-Kollisionen (selten)

---

## 🎨 PyQt6-spezifische Konventionen

### Widget-Naming

```python
class MyDialog(QDialog):
    def __init__(self):
        super().__init__()

        # ✅ Widget-Typ als Suffix
        self.name_input = QLineEdit()
        self.save_button = QPushButton("Speichern")
        self.password_label = QLabel("Passwort:")

        # ⚠️ Ok - Ohne Suffix bei Eindeutigkeit
        self.layout = QVBoxLayout()
        self.form = QFormLayout()

        # ❌ Nicht
        self.input1 = QLineEdit()     # Nicht-deskriptiv
        self.nameQLineEdit = ...      # Type im Namen (redundant)
```

---

### Signal/Slot-Namen

```python
# ✅ Signals: past-tense (was passiert ist)
entry_saved = pyqtSignal(int)       # Entry wurde gespeichert
password_changed = pyqtSignal(str)

# ✅ Slots: on_<action> (Handler)
def on_save_button_clicked(self):
    pass

def on_entry_saved(self, entry_id):
    pass

# ❌ Nicht
save_entry = pyqtSignal()           # Verb (verwirrend)
button_click(self):                 # Kein "on_" Prefix
```

---

## 🔧 Singleton-Pattern Konvention

**Projekt nutzt globale Singleton-Instanzen:**

```python
# In Modul definieren
# src/core/encryption.py
class EncryptionManager:
    # ...

# Singleton-Instanz am Ende der Datei
encryption_manager = EncryptionManager()
```

**Verwendung:**
```python
# ✅ Singleton importieren
from src.core.encryption import encryption_manager

# Direkt nutzen
encryption_manager.encrypt("test")

# ❌ NICHT neue Instanz erstellen
from src.core.encryption import EncryptionManager
manager = EncryptionManager()  # FALSCH - bricht Singleton!
```

**Bestehende Singletons:**
- `encryption_manager` (src/core/encryption.py)
- `app_settings` (src/core/settings.py)
- `theme` (src/gui/themes.py)
- `icon_provider` (src/gui/icons.py)
- `clipboard_manager` (src/utils/clipboard.py)
- `master_password_manager` (src/auth/master_password.py)
- `password_generator` (src/password/generator.py)
- `animator` (src/gui/animations.py)

---

## 💾 Datenbank-Konventionen

### Tabellen-Namen

```sql
-- ✅ Plural, snake_case
CREATE TABLE password_entries (...)
CREATE TABLE categories (...)
CREATE TABLE users (...)

-- ❌ Nicht
CREATE TABLE PasswordEntry (...)  -- PascalCase
CREATE TABLE category (...)       -- Singular
```

---

### Spalten-Namen

```sql
-- ✅ Snake-case, deskriptiv
id INTEGER PRIMARY KEY
name TEXT NOT NULL
encrypted_password BLOB
created_at TIMESTAMP

-- ❌ Nicht
Id INTEGER                    -- PascalCase
encryptedPassword BLOB        -- camelCase
pwd BLOB                      -- Abkürzungen
```

---

## 🧪 Test-Konventionen

### Test-Datei-Namen

```python
# ✅ test_<module>.py
test_encryption.py
test_database.py
test_password_generator.py

# ❌ Nicht
encryption_test.py          # Suffix falsch
test_encryption_tests.py    # Redundant
```

---

### Test-Funktions-Namen

```python
# ✅ Beschreibend, test_<was>_<szenario>()
def test_encrypt_decrypt_roundtrip():
    pass

def test_encrypt_with_empty_password_raises_error():
    pass

def test_database_add_entry_returns_id():
    pass

# ❌ Nicht
def test1():                        # Nicht-deskriptiv
def test_encryption():              # Zu vage
def testEncryptDecrypt():           # camelCase
```

---

## 📝 Kommentare

### Wann kommentieren?

**✅ Kommentieren bei:**
- Komplexe Algorithmen
- Nicht-offensichtliche Workarounds
- Sicherheits-relevante Entscheidungen
- TODOs und FIXMEs

```python
# ✅ Gute Kommentare
def encrypt(self, plaintext: str) -> bytes:
    """Verschlüsselt mit AES-256-CBC."""
    # WICHTIG: UTF-8 Encoding explizit, da Master-Passwort
    # Umlaute enthalten kann (Bug #42)
    return self._fernet.encrypt(plaintext.encode('utf-8'))

# TODO: Implementiere Schlüssel-Rotation für langfristige Sicherheit
# FIXME: Memory-Leak bei großen Datenbanken (>10000 Einträge)
# SECURITY: Passwort-Hash wird mit Argon2id erstellt (CPU+Memory-Hard)
```

**❌ Nicht kommentieren:**
- Offensichtlichen Code
- Was der Code tut (Code selbst erklärt es)

```python
# ❌ Schlechte Kommentare
# Erstelle Variable i
i = 0

# Inkrementiere i
i += 1

# Rufe Funktion auf
result = some_function()
```

---

## 🎯 Fehlerbehandlung

### Exception-Handling Pattern

```python
# ✅ Spezifische Exceptions fangen
try:
    entry = db.get_password_entry(entry_id)
except EntryNotFoundError as e:
    logger.warning(f"Entry {entry_id} not found: {e}")
    return None
except DatabaseError as e:
    logger.error(f"Database error: {e}")
    raise

# ⚠️ Nur wenn wirklich nötig - Generisch + Re-Raise
try:
    risky_operation()
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    raise  # Re-raise!

# ❌ NIEMALS - Stilles Ignorieren
try:
    something()
except:
    pass  # BÖSE!
```

---

### Eigene Exceptions

```python
# ✅ Projekt-spezifische Exceptions
# In src/core/exceptions.py
class SecurePassError(Exception):
    """Base Exception für alle SecurePass Fehler"""
    pass

class EncryptionError(SecurePassError):
    """Verschlüsselungs-Fehler"""
    pass

class DatabaseError(SecurePassError):
    """Datenbank-Fehler"""
    pass
```

---

## 🏗️ Architektur-Patterns

### Datenmodelle (Dataclasses)

```python
# ✅ Dataclasses für Modelle
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class PasswordEntry:
    id: Optional[int]
    name: str
    username: str
    encrypted_password: bytes
    created_at: Optional[datetime] = None
```

**Vorteile:**
- Automatische `__init__`, `__repr__`, `__eq__`
- Type Hints integriert
- Weniger Boilerplate

---

### Repository-Pattern (DatabaseManager)

```python
# ✅ CRUD-Operationen in Manager-Klasse
class DatabaseManager:
    def get_all_entries(self) -> List[PasswordEntry]:
        pass

    def get_entry_by_id(self, entry_id: int) -> Optional[PasswordEntry]:
        pass

    def add_entry(self, entry: PasswordEntry) -> int:
        pass

    def update_entry(self, entry: PasswordEntry) -> None:
        pass

    def delete_entry(self, entry_id: int) -> None:
        pass
```

---

## 📋 Pre-Commit Checkliste

**Vor jedem Commit prüfen:**

- [ ] **Code-Style**
  - PEP 8 konform (Line Length 100)
  - Imports sortiert
  - Keine Trailing Whitespaces

- [ ] **Naming**
  - Snake-case für Funktionen/Variablen
  - PascalCase für Klassen
  - Deskriptive Namen

- [ ] **Kommentare**
  - Keine Debug-Prints (`print()` entfernen!)
  - TODOs dokumentiert
  - Komplexe Stellen erklärt

- [ ] **Tests**
  - Tests passing (`pytest`)
  - Neue Tests für neue Features
  - Coverage akzeptabel

- [ ] **Git**
  - Sinnvolle Commit-Message
  - Keine Secrets committed
  - Branch-Namen korrekt

---

## 🛠️ Tooling (optional, empfohlen)

### Black (Code-Formatter)

```bash
pip install black

# Formatieren
black src/ tests/

# Check-only
black --check src/
```

**Konfiguration:** `pyproject.toml`
```toml
[tool.black]
line-length = 100
target-version = ['py38']
```

---

### Pylint (Linter)

```bash
pip install pylint

# Linting
pylint src/

# Mit Config
pylint --rcfile=.pylintrc src/
```

---

### mypy (Type-Checker)

```bash
pip install mypy

# Type-Checking
mypy src/
```

**Optional** - Projekt nutzt Type Hints, aber nicht verpflichtend

---

## 🎓 Zusammenfassung

### Neue Datei erstellen - Checkliste

1. **Wo?** Richtige Verzeichnisstruktur (siehe oben)
2. **Name?** Snake-case, deskriptiv
3. **Imports?** Sortiert (stdlib, third-party, local)
4. **Klasse?** PascalCase, Docstring
5. **Funktionen?** Snake-case, Verben, Type Hints
6. **Tests?** `test_<module>.py` erstellen
7. **Commit?** Sinnvolle Message, Branch

### Bestehende Datei ändern - Checkliste

1. **Lesen** - Verstehe bestehenden Code-Stil
2. **Konsistent** - Folge bestehendem Stil
3. **Tests** - Passe Tests an / erstelle neue
4. **Review** - Prüfe Diffs vor Commit

---

**Letzte Aktualisierung**: 2025-12-01
**Status**: Vollständig
