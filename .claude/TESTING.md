# Testing-Guide für SecurePass Manager

Umfassende Anleitung für Testing im Projekt.

---

## 🎯 Testing-Philosophie

**Grundsätze:**
- Alle neuen Features brauchen Tests
- Bugfixes brauchen Tests die den Bug nachweisen
- Tests müssen vor jedem Push passing sein
- Coverage-Ziel: **80%+** für neuen Code

---

## 🚀 Quick Start

### Tests lokal ausführen

```bash
# Alle Tests ausführen
pytest

# Verbose Output (empfohlen)
pytest -v

# Mit Coverage
pytest --cov=src --cov-report=html

# Einzelne Datei
pytest tests/test_encryption.py

# Einzelnen Test
pytest tests/test_encryption.py::test_encrypt_decrypt

# Stop bei erstem Fehler
pytest -x

# Letzte fehlgeschlagene Tests wiederholen
pytest --lf
```

### Coverage Report ansehen

```bash
# Nach pytest --cov=src --cov-report=html
# Öffne: htmlcov/index.html im Browser
```

---

## 📁 Test-Struktur

```
tests/
├── __init__.py
├── test_database.py           # DatabaseManager Tests
├── test_encryption.py         # Verschlüsselungs-Tests
├── test_master_password.py    # Argon2id Hashing Tests
├── test_password_generator.py # Generator Tests
├── test_password_strength.py  # Stärke-Bewertung Tests
│
└── fixtures/                  # Shared Test-Daten (falls vorhanden)
```

---

## ✅ Wann Tests schreiben?

### 1. Neues Feature
```python
# Feature: TOTP-Support hinzufügen

# SCHRITT 1: Test schreiben (TDD optional)
# tests/test_totp.py
def test_generate_totp_secret():
    secret = totp_manager.generate_secret()
    assert len(secret) == 32
    assert isinstance(secret, str)

# SCHRITT 2: Feature implementieren
# src/totp/manager.py
def generate_secret():
    return pyotp.random_base32()

# SCHRITT 3: Test ausführen
pytest tests/test_totp.py -v
```

**Commit:**
```bash
git add tests/test_totp.py src/totp/
git commit -m "feat: Füge TOTP-Unterstützung hinzu mit Tests"
```

---

### 2. Bugfix
```python
# Bug: Passwörter mit Umlauten werden falsch verschlüsselt

# SCHRITT 1: Test für Bug schreiben
def test_encrypt_decrypt_with_umlauts():
    """Bug #42: Umlaute werden falsch verschlüsselt"""
    password = "Pässwört123!"
    encrypted = encryption_manager.encrypt(password)
    decrypted = encryption_manager.decrypt(encrypted)
    assert decrypted == password  # Sollte fehlschlagen

# SCHRITT 2: Test ausführen (sollte ROT sein)
pytest tests/test_encryption.py::test_encrypt_decrypt_with_umlauts

# SCHRITT 3: Bug fixen
# ... Code ändern ...

# SCHRITT 4: Test ausführen (sollte GRÜN sein)
pytest tests/test_encryption.py::test_encrypt_decrypt_with_umlauts
```

**Commit:**
```bash
git add tests/test_encryption.py src/core/encryption.py
git commit -m "fix: Behebe Umlaut-Encoding in Verschlüsselung

- Füge UTF-8 Encoding explizit hinzu
- Test für Bug #42 hinzugefügt

Fixes #42"
```

---

### 3. Refactoring
```bash
# VOR Refactoring: Alle Tests müssen passing sein
pytest -v
# ✅ All tests passed

# Refactoring durchführen
# ... Code ändern ...

# NACH Refactoring: Tests müssen immer noch passing sein
pytest -v
# ✅ All tests passed (keine Regression!)
```

---

## 📊 Coverage-Anforderungen

### Minimale Coverage pro Modul

| Modul | Coverage-Ziel | Aktuell | Status |
|-------|---------------|---------|--------|
| `src/core/encryption.py` | 95%+ | ? | ⚠️ |
| `src/core/database.py` | 85%+ | ? | ⚠️ |
| `src/auth/master_password.py` | 95%+ | ? | ⚠️ |
| `src/password/generator.py` | 90%+ | ? | ⚠️ |
| `src/password/strength.py` | 85%+ | ? | ⚠️ |
| `src/gui/*` | 50%+ | ? | ⚠️ (UI schwer testbar) |

### Coverage prüfen

```bash
# Coverage für spezifisches Modul
pytest --cov=src/core/encryption.py --cov-report=term-missing

# Zeigt fehlende Zeilen an
# src/core/encryption.py    85%   12-15, 34
```

---

## 🧪 Test-Typen

### 1. Unit Tests (meiste Tests)

**Zweck:** Einzelne Funktionen/Klassen isoliert testen

**Beispiel:**
```python
# tests/test_encryption.py
def test_encrypt_decrypt():
    """Test grundlegende Verschlüsselung"""
    encryption_manager.set_master_password("test_password")

    plaintext = "Secret123!"
    encrypted = encryption_manager.encrypt(plaintext)
    decrypted = encryption_manager.decrypt(encrypted)

    assert decrypted == plaintext
    assert encrypted != plaintext.encode()
```

**Eigenschaften:**
- ✅ Schnell (< 1 Sekunde)
- ✅ Isoliert (keine DB, keine Dateien)
- ✅ Deterministisch (immer gleiches Ergebnis)

---

### 2. Integration Tests

**Zweck:** Mehrere Module zusammen testen

**Beispiel:**
```python
# tests/test_database_integration.py
def test_save_and_load_password_entry():
    """Test gesamter Workflow: Speichern → Verschlüsseln → Laden → Entschlüsseln"""

    # Setup
    db = DatabaseManager(":memory:")
    encryption_manager.set_master_password("test")

    # Passwort-Eintrag erstellen
    entry = PasswordEntry(
        id=None,
        category_id=1,
        name="Test",
        username="user",
        encrypted_password=encryption_manager.encrypt("secret123"),
    )

    # Speichern
    entry_id = db.add_password_entry(entry)

    # Laden
    loaded_entry = db.get_password_entry_by_id(entry_id)

    # Entschlüsseln
    decrypted = encryption_manager.decrypt(loaded_entry.encrypted_password)

    assert decrypted == "secret123"
```

**Eigenschaften:**
- ⚠️ Langsamer (1-5 Sekunden)
- ⚠️ Komplexer (mehrere Komponenten)
- ✅ Realistischer (wie echte Nutzung)

---

### 3. UI Tests (optional, wenige)

**Zweck:** GUI-Komponenten testen

**Beispiel:**
```python
# tests/test_ui_entry_dialog.py
def test_entry_dialog_validation(qtbot):
    """Test Formular-Validierung"""
    dialog = PasswordEntryDialog()
    qtbot.addWidget(dialog)

    # Leeres Formular sollte nicht gespeichert werden können
    assert not dialog.validate()

    # Ausgefülltes Formular sollte valide sein
    dialog.name_input.setText("Test")
    dialog.username_input.setText("user")
    dialog.password_input.setText("pass123")

    assert dialog.validate()
```

**Eigenschaften:**
- ❌ Langsam (5-10 Sekunden)
- ❌ Komplex (PyQt6 Test-Framework)
- ⚠️ Flaky (manchmal fehlschlagend ohne Grund)

**Empfehlung:** Nur kritische UI-Flows testen

---

## 🛠️ Test-Fixtures & Helpers

### Pytest Fixtures verwenden

```python
# tests/conftest.py (shared fixtures)
import pytest
from src.core.encryption import EncryptionManager
from src.core.database import DatabaseManager

@pytest.fixture
def encryption_manager():
    """Verschlüsselungs-Manager mit Test-Passwort"""
    manager = EncryptionManager()
    manager.set_master_password("test_password_123")
    yield manager
    manager.clear()

@pytest.fixture
def in_memory_database():
    """In-Memory SQLite Datenbank für Tests"""
    db = DatabaseManager(":memory:")
    yield db
    db.close()

@pytest.fixture
def sample_password_entry():
    """Beispiel Passwort-Eintrag"""
    return PasswordEntry(
        id=None,
        category_id=1,
        name="Test Entry",
        username="testuser",
        encrypted_password=b"encrypted_data",
    )
```

**Verwendung:**
```python
# tests/test_database.py
def test_add_password_entry(in_memory_database, sample_password_entry):
    entry_id = in_memory_database.add_password_entry(sample_password_entry)
    assert entry_id > 0
```

---

## 🎯 Test-Driven Development (TDD) - Optional

**Workflow:**
1. 🔴 **RED**: Test schreiben (fehlschlagend)
2. 🟢 **GREEN**: Minimale Implementierung (Test passing)
3. 🔵 **REFACTOR**: Code verbessern (Test bleibt passing)

**Beispiel:**
```python
# 1. RED - Test schreiben
def test_password_strength_weak():
    result = password_checker.check_strength("123")
    assert result.category == StrengthCategory.WEAK

# Test ausführen → FEHLSCHLAG ✗

# 2. GREEN - Implementieren
def check_strength(password):
    if len(password) < 6:
        return PasswordStrength(category=StrengthCategory.WEAK, score=1)
    # ...

# Test ausführen → ERFOLG ✓

# 3. REFACTOR - Verbessern
def check_strength(password):
    score = _calculate_score(password)  # Extrahiert in Funktion
    return PasswordStrength(category=_categorize(score), score=score)

# Test ausführen → Immer noch ERFOLG ✓
```

---

## 🚨 Häufige Test-Fehler

### 1. Tests sind nicht isoliert
```python
# ❌ FALSCH
def test_add_entry():
    db = DatabaseManager("test.db")  # Shared state!
    # ...

# ✅ RICHTIG
def test_add_entry():
    db = DatabaseManager(":memory:")  # Isoliert
    # ...
```

---

### 2. Tests sind nicht deterministisch
```python
# ❌ FALSCH
def test_random_password():
    pw = generator.generate(12)
    assert pw == "aB3$xY9@qW2!"  # Zufällig!

# ✅ RICHTIG
def test_random_password():
    pw = generator.generate(12)
    assert len(pw) == 12
    assert any(c.isupper() for c in pw)
    assert any(c.isdigit() for c in pw)
```

---

### 3. Tests testen Implementierung statt Verhalten
```python
# ❌ FALSCH
def test_encrypt_uses_fernet():
    assert isinstance(encryption_manager._fernet, Fernet)

# ✅ RICHTIG
def test_encrypt_decrypt_roundtrip():
    encrypted = encryption_manager.encrypt("test")
    decrypted = encryption_manager.decrypt(encrypted)
    assert decrypted == "test"
```

---

## 📋 Pre-Push Checkliste

**Vor jedem Push:**
```bash
# 1. Alle Tests ausführen
pytest -v

# 2. Coverage prüfen
pytest --cov=src --cov-report=term-missing

# 3. Falls Coverage < 80% für neue Dateien:
#    → Mehr Tests schreiben!

# 4. Alle Tests passing?
#    ✅ JA → Push erlaubt
#    ❌ NEIN → Erst fixen!
```

---

## 🔧 Debugging fehlgeschlagener Tests

### Test-Output verstehen
```bash
pytest -v

# Output:
# tests/test_encryption.py::test_encrypt_decrypt FAILED

# Details:
# >       assert decrypted == plaintext
# E       AssertionError: assert 'test' == 'test123'
```

### Einzelnen Test mit mehr Details
```bash
pytest tests/test_encryption.py::test_encrypt_decrypt -vv

# Oder mit pdb (Python Debugger)
pytest tests/test_encryption.py::test_encrypt_decrypt --pdb
```

### Print-Debugging in Tests
```python
def test_something():
    result = some_function()
    print(f"DEBUG: result = {result}")  # Sichtbar mit pytest -s
    assert result == expected
```

```bash
pytest tests/test_something.py -s  # -s zeigt prints
```

---

## 🎓 Test-Best-Practices

### 1. Test-Namen sind Dokumentation
```python
# ❌ Schlechter Name
def test_1():
    pass

# ✅ Guter Name
def test_encrypt_decrypt_with_special_characters():
    pass

# ✅ Noch besser (beschreibt Erwartung)
def test_encrypt_decrypt_preserves_special_characters():
    pass
```

---

### 2. AAA-Pattern (Arrange-Act-Assert)
```python
def test_add_password_entry():
    # ARRANGE - Setup
    db = DatabaseManager(":memory:")
    entry = PasswordEntry(name="Test", ...)

    # ACT - Aktion ausführen
    entry_id = db.add_password_entry(entry)

    # ASSERT - Überprüfen
    assert entry_id > 0
    assert db.get_password_entry_by_id(entry_id) is not None
```

---

### 3. Ein Test = Eine Assertion (Faustregel)
```python
# ⚠️ Nicht ideal (mehrere Assertions)
def test_password_entry():
    entry = create_entry()
    assert entry.name == "Test"
    assert entry.username == "user"
    assert entry.encrypted_password is not None

# ✅ Besser (aufgeteilt)
def test_password_entry_has_name():
    entry = create_entry()
    assert entry.name == "Test"

def test_password_entry_has_username():
    entry = create_entry()
    assert entry.username == "user"

def test_password_entry_has_encrypted_password():
    entry = create_entry()
    assert entry.encrypted_password is not None
```

**Grund:** Bei Fehlschlag weißt du genau was kaputt ist.

---

## 📚 Testing-Resourcen

### Pytest Dokumentation
- https://docs.pytest.org/

### PyQt6 Testing
- https://pytest-qt.readthedocs.io/

### Coverage
- https://coverage.readthedocs.io/

---

## 🎯 Zusammenfassung für Claude

**Als Claude-Assistent:**

### VOR jedem Push:
```bash
pytest -v  # Alle Tests müssen passing sein!
```

### BEI neuem Feature:
1. Tests schreiben (`tests/test_<feature>.py`)
2. Feature implementieren
3. Tests ausführen
4. Coverage prüfen (80%+ Ziel)

### BEI Bugfix:
1. Test für Bug schreiben (sollte fehlschlagen)
2. Bug fixen
3. Test ausführen (sollte passing sein)

### Commit-Message:
```bash
git commit -m "feat: Füge Feature XYZ hinzu

- Implementierung in src/...
- Tests in tests/test_...
- Coverage: 85%

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

**Letzte Aktualisierung**: 2025-12-01
**Status**: Vollständig
