# Security-Checklist für SecurePass Manager

Sicherheits-Richtlinien und Review-Checkliste für neuen Code.

---

## 🎯 Überblick

Diese Checkliste hilft bei:
- Security-Review für neuen Code
- Vermeidung häufiger Sicherheitslücken
- Überprüfung von Verschlüsselung
- Input-Validierung
- Sichere Coding-Praktiken

---

## 🔒 Goldene Regeln

### 1. **Niemals Klartext-Passwörter speichern**
```python
# ❌ FALSCH
entry.password = "mein_passwort"  # Klartext!

# ✅ RICHTIG
entry.encrypted_password = encryption_manager.encrypt("mein_passwort")
```

---

### 2. **Niemals Passwörter loggen**
```python
# ❌ FALSCH
logger.debug(f"Passwort: {password}")
print(f"User password: {password}")

# ✅ RICHTIG
logger.debug(f"Passwort-Länge: {len(password)}")  # Nur Metadaten
```

---

### 3. **Niemals Secrets in Code**
```python
# ❌ FALSCH
API_KEY = "sk_live_abc123..."
DEFAULT_PASSWORD = "admin"

# ✅ RICHTIG
API_KEY = os.getenv("API_KEY")  # Aus Environment
# Oder: User-Eingabe
```

---

### 4. **Immer Input validieren**
```python
# ❌ FALSCH
user_input = request.get_data()
db.execute(f"SELECT * FROM users WHERE name = '{user_input}'")  # SQL-Injection!

# ✅ RICHTIG
user_input = request.get_data()
if not validate_input(user_input):
    raise ValueError("Invalid input")
db.execute("SELECT * FROM users WHERE name = ?", (user_input,))  # Parameterized
```

---

### 5. **Sichere Zufälligkeit nutzen**
```python
# ❌ FALSCH
import random
password = ''.join(random.choice(chars) for _ in range(16))  # NICHT SICHER!

# ✅ RICHTIG
import secrets
password = ''.join(secrets.choice(chars) for _ in range(16))  # Kryptografisch sicher
```

---

## 📋 Security-Review Checkliste

### Für JEDEN neuen Code durchgehen:

#### 1. Verschlüsselung

- [ ] **Werden sensible Daten verschlüsselt?**
  - Passwörter: ✅ Verschlüsselt
  - Notizen: ✅ Verschlüsselt
  - TOTP-Secrets: ✅ Verschlüsselt
  - Usernames: ⚠️ Klartext (für Suche)

- [ ] **Wird der richtige Algorithmus genutzt?**
  - AES-256 (Fernet): ✅ Ja
  - Deprecated (DES, MD5): ❌ Nein

- [ ] **Ist die Encryption-Key geschützt?**
  ```python
  # ✅ Key wird aus Master-Passwort abgeleitet
  # ✅ Key wird nicht persistent gespeichert
  # ✅ Key wird gelöscht bei Lock
  ```

---

#### 2. Passwort-Hashing

- [ ] **Wird ein sicherer Hash-Algorithmus genutzt?**
  - Argon2id: ✅ Ja (aktuell)
  - bcrypt/scrypt: ✅ Ok
  - SHA-256 pur: ❌ NEIN! (kein Salt, zu schnell)

- [ ] **Sind Hash-Parameter ausreichend?**
  ```python
  # Argon2id Parameter prüfen:
  time_cost >= 2        # ✅ Aktuell: 2
  memory_cost >= 64MB   # ✅ Aktuell: 64MB
  parallelism >= 2      # ✅ Aktuell: 4
  ```

- [ ] **Wird ein Salt verwendet?**
  ```python
  # ✅ Argon2id generiert automatisch Salt
  ```

---

#### 3. Input-Validierung

- [ ] **Wird User-Input validiert?**
  ```python
  # ✅ Längen-Checks
  if len(password) < 8:
      raise ValueError("Too short")

  # ✅ Zeichen-Checks
  if not is_valid_chars(input):
      raise ValueError("Invalid characters")

  # ✅ Type-Checks
  if not isinstance(entry_id, int):
      raise TypeError("ID must be int")
  ```

- [ ] **Wird Input sanitized?**
  ```python
  # ✅ SQL: Parameterized Queries
  cursor.execute("SELECT * FROM entries WHERE id = ?", (entry_id,))

  # ✅ HTML: Escaping (falls Web-UI)
  from html import escape
  safe_text = escape(user_input)

  # ✅ File-Paths: Validierung
  if ".." in filepath:
      raise ValueError("Path traversal detected!")
  ```

---

#### 4. SQL-Injection Prevention

- [ ] **Werden parameterized queries genutzt?**
  ```python
  # ❌ FALSCH - SQL-Injection möglich
  query = f"SELECT * FROM entries WHERE name = '{user_input}'"
  cursor.execute(query)

  # ✅ RICHTIG - Parameterized
  cursor.execute("SELECT * FROM entries WHERE name = ?", (user_input,))
  ```

- [ ] **Keine String-Konkatenation in SQL?**
  ```python
  # ❌ FALSCH
  query = "SELECT * FROM " + table_name  # Table-Name vom User!

  # ✅ RICHTIG (wenn Table-Name dynamisch)
  ALLOWED_TABLES = ["entries", "categories", "users"]
  if table_name not in ALLOWED_TABLES:
      raise ValueError("Invalid table")
  query = f"SELECT * FROM {table_name}"  # Jetzt ok (Whitelist)
  ```

---

#### 5. Temporäre Dateien

- [ ] **Werden temp-Dateien sicher erstellt?**
  ```python
  # ❌ FALSCH - Vorhersagbarer Name
  temp_file = "/tmp/database.db"  # Andere Prozesse können zugreifen!

  # ✅ RICHTIG - Zufälliger Name
  import tempfile
  fd, temp_file = tempfile.mkstemp(prefix="securepass_", suffix=".db")
  ```

- [ ] **Werden temp-Dateien gelöscht?**
  ```python
  # ✅ Im Destruktor
  def __del__(self):
      if self.temp_file and os.path.exists(self.temp_file):
          os.remove(self.temp_file)

  # ✅ Oder mit Context Manager
  with TemporaryDatabase() as db:
      # ... use db
      pass  # Automatisch gelöscht
  ```

- [ ] **Haben temp-Dateien sichere Permissions?**
  ```python
  # ✅ Nur Owner kann lesen/schreiben
  os.chmod(temp_file, 0o600)  # rw------- (600)
  ```

---

#### 6. Memory Management

- [ ] **Werden sensible Daten aus Memory gelöscht?**
  ```python
  # ✅ Encryption-Key löschen
  def clear(self):
      self._fernet = None
      self._key = None

  # ⚠️ Python GC löscht nicht sofort
  # Für extreme Sicherheit: ctypes.memset() nutzen
  ```

- [ ] **Keine sensiblen Daten in Logs/Exceptions?**
  ```python
  # ❌ FALSCH
  except Exception as e:
      logger.error(f"Fehler bei Passwort {password}: {e}")

  # ✅ RICHTIG
  except Exception as e:
      logger.error(f"Fehler bei Verschlüsselung: {e}")
      # Passwort NICHT loggen!
  ```

---

#### 7. Zwischenablage-Sicherheit

- [ ] **Wird Zwischenablage automatisch gelöscht?**
  ```python
  # ✅ Aktuell: 30 Sekunden Auto-Clear
  clipboard_manager.copy_to_clipboard(password, auto_clear_seconds=30)
  ```

- [ ] **Wird User gewarnt?**
  ```python
  # ✅ User-Feedback
  QMessageBox.information(self, "Info",
      "Passwort kopiert. Wird in 30s gelöscht.")
  ```

---

#### 8. Session-Management

- [ ] **Wird Session bei Inaktivität beendet?**
  ```python
  # ✅ Auto-Lock nach 5 Minuten
  self.auto_lock_timeout = 5 * 60 * 1000
  ```

- [ ] **Werden Keys bei Lock gelöscht?**
  ```python
  # ✅ Bei Lock
  def lock_application(self):
      encryption_manager.clear()  # Keys löschen
      # ... show login dialog
  ```

---

## 🛡️ Spezifische Sicherheits-Patterns

### Pattern 1: Verschlüsselung implementieren

```python
# ✅ Vollständiges Beispiel
from cryptography.fernet import Fernet
import hashlib
import base64

def encrypt_data(plaintext: str, master_password: str) -> bytes:
    # 1. Key-Derivation
    key_bytes = hashlib.sha256(master_password.encode('utf-8')).digest()
    key = base64.urlsafe_b64encode(key_bytes)

    # 2. Verschlüsseln
    fernet = Fernet(key)
    return fernet.encrypt(plaintext.encode('utf-8'))

def decrypt_data(ciphertext: bytes, master_password: str) -> str:
    # 1. Key-Derivation (gleich wie oben)
    key_bytes = hashlib.sha256(master_password.encode('utf-8')).digest()
    key = base64.urlsafe_b64encode(key_bytes)

    # 2. Entschlüsseln
    fernet = Fernet(key)
    return fernet.decrypt(ciphertext).decode('utf-8')
```

**Checkliste:**
- [ ] UTF-8 Encoding explizit
- [ ] Fehlerbehandlung (InvalidToken)
- [ ] Key-Derivation (nicht Klartext-Key!)

---

### Pattern 2: Sicherer Passwort-Generator

```python
# ✅ Vollständiges Beispiel
import secrets
import string

def generate_password(length: int = 16,
                     use_uppercase: bool = True,
                     use_lowercase: bool = True,
                     use_digits: bool = True,
                     use_special: bool = True) -> str:
    # 1. Zeichensatz erstellen
    chars = ""
    if use_lowercase:
        chars += string.ascii_lowercase
    if use_uppercase:
        chars += string.ascii_uppercase
    if use_digits:
        chars += string.digits
    if use_special:
        chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"

    if not chars:
        raise ValueError("Mindestens ein Zeichensatz erforderlich")

    # 2. Passwort generieren (kryptografisch sicher)
    password = ''.join(secrets.choice(chars) for _ in range(length))

    # 3. Garantiere mindestens ein Zeichen jedes Typs
    # (siehe src/password/generator.py für volle Implementierung)

    return password
```

**Checkliste:**
- [ ] `secrets` statt `random`
- [ ] Mindest-Zeichenanzahl jedes Typs
- [ ] Validierung der Inputs

---

### Pattern 3: SQL-Injection-Safe Queries

```python
# ✅ Vollständiges Beispiel
def search_entries(db, search_query: str) -> List[PasswordEntry]:
    # ❌ NIEMALS SO:
    # cursor.execute(f"SELECT * FROM password_entries WHERE name LIKE '%{search_query}%'")

    # ✅ RICHTIG:
    cursor = db.conn.cursor()
    cursor.execute(
        "SELECT * FROM password_entries WHERE name LIKE ?",
        (f"%{search_query}%",)  # Parameter als Tuple
    )
    return cursor.fetchall()
```

**Checkliste:**
- [ ] Parameterized Query (`?` Platzhalter)
- [ ] Parameter als Tuple übergeben
- [ ] KEINE String-Konkatenation

---

## 🚨 Häufige Sicherheitslücken

### 1. Hardcoded Secrets

```python
# ❌ NIEMALS SO:
DEFAULT_PASSWORD = "admin123"
API_KEY = "sk_live_..."
ENCRYPTION_KEY = "my_secret_key"

# ✅ RICHTIG:
# Aus Environment oder User-Eingabe
api_key = os.getenv("API_KEY")
```

---

### 2. Unsicherer Random

```python
# ❌ FALSCH
import random
token = random.randint(1000, 9999)  # NICHT SICHER!

# ✅ RICHTIG
import secrets
token = secrets.randbelow(9000) + 1000  # Kryptografisch sicher
```

---

### 3. Weak Crypto

```python
# ❌ DEPRECATED - NICHT NUTZEN
from Crypto.Cipher import DES  # DES ist gebrochen!
import md5  # MD5 ist gebrochen!

# ✅ RICHTIG
from cryptography.fernet import Fernet  # AES-256
import hashlib
hash = hashlib.sha256(data).digest()  # SHA-256
```

---

### 4. Path Traversal

```python
# ❌ FALSCH
filename = user_input  # "../../etc/passwd"
with open(filename) as f:
    data = f.read()  # GEFÄHRLICH!

# ✅ RICHTIG
from pathlib import Path
base_dir = Path("/safe/directory")
filepath = (base_dir / user_input).resolve()
if not filepath.is_relative_to(base_dir):
    raise ValueError("Path traversal detected!")
```

---

### 5. Command Injection

```python
# ❌ FALSCH
import os
filename = user_input
os.system(f"cat {filename}")  # GEFÄHRLICH!

# ✅ RICHTIG
import subprocess
subprocess.run(["cat", filename], check=True)  # Sicher (Liste statt String)
```

---

## 🧪 Security-Testing

### 1. Encryption-Tests

```python
def test_encrypt_decrypt_roundtrip():
    """Test dass Verschlüsselung reversibel ist"""
    encryption_manager.set_master_password("test")
    plaintext = "Secret123!"
    encrypted = encryption_manager.encrypt(plaintext)
    decrypted = encryption_manager.decrypt(encrypted)
    assert decrypted == plaintext

def test_different_passwords_different_ciphertext():
    """Test dass gleicher Plaintext unterschiedlich verschlüsselt wird"""
    encryption_manager.set_master_password("test")
    encrypted1 = encryption_manager.encrypt("secret")
    encrypted2 = encryption_manager.encrypt("secret")
    # Fernet nutzt IV, also sollten sie unterschiedlich sein
    assert encrypted1 != encrypted2

def test_wrong_password_fails():
    """Test dass falsches Passwort fehlschlägt"""
    encryption_manager.set_master_password("password1")
    encrypted = encryption_manager.encrypt("secret")

    encryption_manager.set_master_password("password2")
    with pytest.raises(Exception):  # InvalidToken
        encryption_manager.decrypt(encrypted)
```

---

### 2. SQL-Injection-Tests

```python
def test_sql_injection_protection():
    """Test dass SQL-Injection verhindert wird"""
    db = DatabaseManager(":memory:")

    # Versuche SQL-Injection
    malicious_input = "'; DROP TABLE password_entries; --"

    # Sollte NICHT crashen oder Tabelle löschen
    results = db.search_password_entries(malicious_input)

    # Tabelle sollte noch existieren
    assert db.get_all_password_entries() is not None
```

---

### 3. Input-Validation-Tests

```python
def test_password_length_validation():
    """Test dass zu kurze Passwörter abgelehnt werden"""
    with pytest.raises(ValueError):
        validate_password("abc")  # Zu kurz

def test_special_characters_in_password():
    """Test dass Sonderzeichen funktionieren"""
    password = "P@$$w0rd!<>\"'&"
    encrypted = encryption_manager.encrypt(password)
    decrypted = encryption_manager.decrypt(encrypted)
    assert decrypted == password
```

---

## 📚 Security-Resourcen

### Kryptografie
- **Cryptography Library**: https://cryptography.io/
- **OWASP Crypto**: https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html

### Passwort-Sicherheit
- **OWASP Password Storage**: https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
- **Argon2**: https://www.password-hashing.net/

### Allgemein
- **OWASP Top 10**: https://owasp.org/www-project-top-ten/
- **Python Security**: https://python.readthedocs.io/en/stable/library/security_warnings.html

---

## 🎯 Zusammenfassung für Claude

**VOR jedem Commit:**

```bash
# 1. Security-Review durchführen
- [ ] Checkliste oben durchgehen
- [ ] Keine Passwörter im Klartext
- [ ] Keine Passwörter in Logs
- [ ] Input validiert
- [ ] SQL-Injection sicher

# 2. Security-Tests schreiben
pytest tests/test_security.py

# 3. Commit
git commit -m "feat: Füge Feature XYZ hinzu (Security-Reviewed)"
```

**Bei Unsicherheit:**
- Frage den Benutzer!
- Konsultiere OWASP
- Lieber zu vorsichtig als zu lax

**Wenn Sicherheitslücke gefunden:**
1. ⚠️ SOFORT Benutzer informieren
2. Issue erstellen (privat falls kritisch!)
3. Hotfix-Branch erstellen
4. Fix implementieren + Test
5. Sofort mergen (Sicherheit = Priorität!)

---

**Letzte Aktualisierung**: 2025-12-01
**Status**: Vollständig
**Version**: 1.0
