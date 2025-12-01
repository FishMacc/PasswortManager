# Debugging-Guide für SecurePass Manager

Troubleshooting, häufige Fehler und Debugging-Strategien.

---

## 🚨 Häufige Fehler & Lösungen

### 1. Import-Fehler

#### Problem: `ModuleNotFoundError: No module named 'PyQt6'`

**Ursache:** Dependencies nicht installiert

**Lösung:**
```bash
pip install -r requirements.txt

# Oder einzeln
pip install PyQt6>=6.6.0
```

---

#### Problem: `ImportError: cannot import name 'icon_provider'`

**Ursache:** Zirkuläre Imports oder Modul nicht gefunden

**Lösung:**
```bash
# 1. Prüfe Import-Pfade
python -c "import src.gui.icons; print(src.gui.icons.__file__)"

# 2. Prüfe __init__.py Dateien
ls -la src/gui/__init__.py

# 3. PYTHONPATH setzen (falls nötig)
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

---

### 2. Datenbank-Fehler

#### Problem: `sqlite3.OperationalError: no such table: password_entries`

**Ursache:** Datenbank nicht initialisiert

**Lösung:**
```python
# In src/core/database.py - Tabellen werden automatisch erstellt
# Falls nicht: Datenbank neu erstellen

# 1. Alte DB löschen (BACKUP ERST!)
rm test.spdb

# 2. Neu starten
python main.py
```

---

#### Problem: `sqlite3.DatabaseError: file is not a database`

**Ursache:** .spdb Datei korrupt oder nicht entschlüsselbar

**Lösung:**
```python
# 1. Master-Passwort falsch?
#    → Richtiges Passwort eingeben

# 2. Datei wirklich korrupt?
#    → Von Backup wiederherstellen

# 3. Debug: Datei-Header prüfen
with open("test.spdb", "rb") as f:
    header = f.read(16)
    print(header)  # Sollte b'SECUREPASS_DB_V1' sein
```

---

### 3. Verschlüsselungs-Fehler

#### Problem: `cryptography.fernet.InvalidToken`

**Ursache:** Falsche Encryption-Key oder korrupte Daten

**Lösung:**
```python
# 1. Master-Passwort geändert?
#    → Kann nicht entschlüsseln! Altes PW nötig

# 2. Debug: Prüfe ob Key gesetzt ist
from src.core.encryption import encryption_manager
print(encryption_manager.is_unlocked())  # Sollte True sein

# 3. Key manuell setzen
encryption_manager.set_master_password("dein_passwort")
```

---

#### Problem: `UnicodeDecodeError: 'utf-8' codec can't decode`

**Ursache:** Encoding-Probleme bei Verschlüsselung

**Lösung:**
```python
# In src/core/encryption.py
def encrypt(self, plaintext: str) -> bytes:
    return self._fernet.encrypt(plaintext.encode('utf-8'))  # Explizit UTF-8

def decrypt(self, ciphertext: bytes) -> str:
    return self._fernet.decrypt(ciphertext).decode('utf-8')  # Explizit UTF-8
```

---

### 4. UI-Fehler

#### Problem: Dialog zu groß für Bildschirm / überlappende Elemente

**Ursache:** Hardcoded Größen, kein responsive Design

**Lösung:**
```python
# In Dialog __init__:
self.setMinimumSize(400, 300)  # Minimum
self.resize(600, 500)          # Bevorzugt, aber anpassbar

# Responsive Größen nutzen
from src.gui.responsive import responsive
height = responsive.get_dialog_height()
```

**Siehe auch:** Letzte 5 Commits (UI-Layout-Fixes)

---

#### Problem: Icons werden nicht angezeigt

**Ursache:** icon_provider nicht importiert oder Farbe falsch

**Lösung:**
```python
# Richtiger Import
from src.gui.icons import icon_provider
from src.gui.themes import theme

# Icon erstellen
colors = theme.get_colors()
icon = icon_provider.get_icon("lock", colors["icon_primary"], 24)
button.setIcon(icon)
```

---

#### Problem: Dark Mode funktioniert nicht / Farben falsch

**Ursache:** Theme nicht aktualisiert oder Stylesheet überschrieben

**Lösung:**
```python
# 1. Theme neu laden
from src.gui.themes import theme
theme.apply_theme(app)

# 2. Prüfe ob Widget eigene Styles hat
widget.setStyleSheet("")  # Zurücksetzen

# 3. Nutze Theme-Farben
colors = theme.get_colors()
widget.setStyleSheet(f"background: {colors['background']};")
```

---

### 5. Performance-Probleme

#### Problem: Anwendung läuft langsam / friert ein

**Ursache:** Zu viele Einträge, nicht-optimierte Queries

**Debug:**
```python
# 1. Wie viele Einträge?
entries = db.get_all_password_entries()
print(f"Anzahl Einträge: {len(entries)}")

# 2. Query-Zeit messen
import time
start = time.time()
entries = db.get_all_password_entries()
print(f"Query-Zeit: {time.time() - start:.2f}s")

# 3. SQLite Profiling
db.conn.set_trace_callback(print)  # Alle Queries loggen
```

**Lösung:**
- Pagination implementieren
- Virtuelle Scroll-Liste nutzen
- Lazy Loading für Passwörter

---

### 6. Auto-Lock Probleme

#### Problem: Auto-Lock triggert zu früh / zu spät

**Debug:**
```python
# In src/gui/main_window.py
def reset_inactivity_timer(self):
    print(f"[DEBUG] Timer reset at {time.time()}")  # Temporär
    self.inactivity_timer.start(self.auto_lock_timeout)
```

**Lösung:**
```python
# Timer-Dauer ändern (in Millisekunden)
self.auto_lock_timeout = 5 * 60 * 1000  # 5 Minuten
```

---

### 7. Test-Fehler

#### Problem: `pytest: command not found`

**Lösung:**
```bash
pip install pytest pytest-cov

# Oder
python -m pytest
```

---

#### Problem: Tests schlagen fehl mit `EncryptionManager has no _fernet`

**Ursache:** Master-Passwort nicht gesetzt in Test

**Lösung:**
```python
def test_something():
    encryption_manager.set_master_password("test_password")
    # ... rest of test
```

---

## 🔍 Debugging-Strategien

### 1. Print-Debugging (schnell & einfach)

```python
# In verdächtiger Funktion
def save_password_entry(entry):
    print(f"[DEBUG] Saving entry: {entry.name}")
    print(f"[DEBUG] Encrypted password length: {len(entry.encrypted_password)}")

    result = db.add_password_entry(entry)

    print(f"[DEBUG] Entry ID: {result}")
    return result
```

**Wichtig:** Entferne alle `print()` vor Commit!

---

### 2. Logging (besser als Print)

```python
import logging

# Setup (einmalig in main.py)
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# In Modulen verwenden
logger = logging.getLogger(__name__)

def save_password_entry(entry):
    logger.debug(f"Saving entry: {entry.name}")
    # ...
    logger.info(f"Entry saved with ID: {result}")
    return result
```

**Vorteile:**
- Levels (DEBUG, INFO, WARNING, ERROR)
- Timestamps automatisch
- In Datei speicherbar

---

### 3. Python Debugger (pdb)

```python
# Import
import pdb

# Breakpoint setzen
def problematic_function():
    x = do_something()
    pdb.set_trace()  # Programm stoppt hier!
    y = do_something_else(x)
    return y
```

**pdb Befehle:**
- `n` - Next (nächste Zeile)
- `s` - Step (in Funktion rein)
- `c` - Continue (bis nächster Breakpoint)
- `p variable` - Print variable
- `l` - List (zeige Code um aktuelle Zeile)
- `q` - Quit

**Oder Python 3.7+ Breakpoint:**
```python
def problematic_function():
    x = do_something()
    breakpoint()  # Besser als pdb.set_trace()
    y = do_something_else(x)
```

---

### 4. PyQt6 Debug-Modus

```python
# In main.py - Vor QApplication erstellen
import sys
sys.argv.append('--debug')  # PyQt6 Debug-Modus

# Oder Environment Variable
export QT_DEBUG_PLUGINS=1
python main.py
```

**Zeigt:**
- Plugin-Loading
- Signal/Slot Verbindungen
- Widget-Hierarchie

---

### 5. Memory-Leaks finden

```python
# tracemalloc nutzen
import tracemalloc

# In main.py
tracemalloc.start()

# ... Anwendung läuft ...

# Memory-Snapshot
snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')

for stat in top_stats[:10]:
    print(stat)
```

---

### 6. SQLite Query-Debugging

```python
# In DatabaseManager
def __init__(self, db_path):
    self.conn = sqlite3.connect(db_path)

    # Debug: Alle Queries loggen
    self.conn.set_trace_callback(lambda query: print(f"[SQL] {query}"))
```

**Oder: SQLite Browser nutzen**
```bash
# Datenbank ansehen (temporäre entschlüsselte)
sqlite3 /tmp/securepass_temp_xyz.db

# Commands
.tables          # Alle Tabellen
.schema users    # Schema ansehen
SELECT * FROM password_entries LIMIT 5;
```

---

### 7. UI-Debugging mit QDebug

```python
from PyQt6.QtCore import qDebug, qWarning, qCritical

# In UI-Code
qDebug("Button clicked!")
qWarning("Invalid input detected")
qCritical("Database connection failed!")
```

---

## 🛠️ Debugging-Tools

### 1. Visual Studio Code

**.vscode/launch.json:**
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: SecurePass",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/main.py",
      "console": "integratedTerminal"
    }
  ]
}
```

**Breakpoints:** Klick auf Zeilennummer
**Debug-Panel:** F5 starten

---

### 2. PyCharm

1. Rechtsklick auf `main.py` → "Debug 'main'"
2. Breakpoints: Klick auf Zeilennummer
3. Debug-Toolbar nutzen (Step Over, Step Into, etc.)

---

### 3. ipdb (besserer Debugger)

```bash
pip install ipdb
```

```python
import ipdb
ipdb.set_trace()  # Wie pdb, aber mit Tab-Completion
```

---

## 📊 Performance-Profiling

### 1. cProfile (CPU-Profiling)

```bash
python -m cProfile -o profile.stats main.py

# Analyse
python -m pstats profile.stats
>>> sort cumtime
>>> stats 20  # Top 20 Funktionen
```

---

### 2. line_profiler (Zeilen-Profiling)

```bash
pip install line_profiler
```

```python
# Dekoriere Funktion
@profile
def slow_function():
    # ...
```

```bash
kernprof -l -v main.py
```

---

### 3. memory_profiler

```bash
pip install memory_profiler
```

```python
from memory_profiler import profile

@profile
def memory_intensive_function():
    # ...
```

```bash
python -m memory_profiler main.py
```

---

## 🔧 Troubleshooting-Checkliste

**Bei jedem Bug:**

- [ ] **Fehlermeldung vollständig lesen**
  - Was ist der genaue Error?
  - Welche Datei, welche Zeile?

- [ ] **Stack-Trace analysieren**
  - Wo kommt der Error her?
  - Was war der letzte erfolgreiche Schritt?

- [ ] **Reproduzierbar?**
  - Tritt der Fehler immer auf?
  - Unter welchen Bedingungen?

- [ ] **Minimales Beispiel erstellen**
  - Kann ich den Bug isolieren?
  - Was ist das kleinste Beispiel?

- [ ] **Logs prüfen**
  - Gibt es Warnungen?
  - Was steht im Output?

- [ ] **Recent Changes**
  - Was wurde zuletzt geändert?
  - `git log -5` ansehen

- [ ] **Tests ausführen**
  - `pytest -v`
  - Schlagen Tests fehl?

- [ ] **Google / Stack Overflow**
  - Haben andere das Problem?
  - Bekannte Lösungen?

- [ ] **Dokumentation lesen**
  - PyQt6 Docs
  - Python Docs
  - Project Docs

- [ ] **Issue erstellen**
  - Falls nicht lösbar
  - Mit allen Details

---

## 🎯 Debug-Workflow für Claude

**Als Claude-Assistent bei Problemen:**

### 1. Fehler verstehen
```
Benutzer: "Es funktioniert nicht!"

Claude:
- Lese die Fehlermeldung
- Prüfe Stack-Trace
- Identifiziere betroffene Datei:Zeile
```

### 2. Code untersuchen
```bash
# Relevante Datei lesen
Read: src/core/database.py

# Nach Error-Stelle suchen
Grep: "def problematic_function"
```

### 3. Debugging-Code hinzufügen
```python
# Temporär für Debug
import logging
logger = logging.getLogger(__name__)

def problematic_function():
    logger.debug(f"Input: {input_var}")
    # ... Code ...
    logger.debug(f"Output: {result}")
```

### 4. Testen
```bash
python main.py
# Oder
pytest tests/test_problematic.py -v
```

### 5. Fix implementieren
```python
# Problem gefunden → Fix schreiben
# Debug-Code entfernen (logging ok, print() weg!)
```

### 6. Commit
```bash
git add <dateien>
git commit -m "fix: Behebe Problem X

- Ursache: Y
- Lösung: Z
- Debug-Logs hinzugefügt

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## 📚 Nützliche Links

- **PyQt6 Docs**: https://www.riverbankcomputing.com/static/Docs/PyQt6/
- **Python Debugging**: https://docs.python.org/3/library/pdb.html
- **SQLite Docs**: https://www.sqlite.org/docs.html
- **Cryptography Docs**: https://cryptography.io/en/latest/

---

## 🎓 Zusammenfassung

**Typischer Debug-Prozess:**

1. ❌ **Fehler tritt auf**
2. 🔍 **Fehlermeldung lesen** (Stack-Trace!)
3. 🐛 **Print/Logging** hinzufügen
4. 🧪 **Reproduzieren** (manuell oder Test)
5. 💡 **Ursache identifizieren**
6. ✅ **Fix implementieren**
7. 🧪 **Test schreiben** (falls nicht vorhanden)
8. 🚀 **Commit & Push**

**Bei Unsicherheit:**
- Frage den Benutzer!
- Dokumentiere was du versucht hast
- Erstelle Issue falls komplex

---

**Letzte Aktualisierung**: 2025-12-01
**Status**: Vollständig
