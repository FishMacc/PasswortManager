# Quick Start Guide für Claude Nachfolger

**Ziel**: In 2 Minuten auf dem gleichen Wissensstand sein

---

## 1. Was ist das Projekt?

**SecurePass Manager** - Python Passwort-Manager mit PyQt6
- **Status**: Voll funktionsfähig, aktive Entwicklung
- **Verschlüsselung**: AES-256 + Argon2id
- **UI**: Apple-Stil, Dark/Light Mode, Animationen

---

## 2. Erste Schritte

### Projekt verstehen (3 Minuten)
```bash
# 1. Lese die vollständige Wissensdatenbank
Read: .claude/knowledge-base.md

# 2. Wichtigste Dateien kennen
Read: src/core/database.py       # Datenbank-Manager
Read: src/core/encryption.py     # Verschlüsselung
Read: src/gui/main_window.py     # Hauptfenster

# 3. Projekt starten
python main.py
```

### Projekt testen
```bash
# Dependencies installieren (falls noch nicht)
pip install -r requirements.txt

# Tests ausführen
pytest -v

# Mit Coverage
pytest --cov=src
```

---

## 3. Aktuelle Probleme (Priorität)

### ✅ BEHOBEN (2025-12-01 Session)
1. ~~**Exception-Handling & Logging**~~ - Logging-System implementiert ✅
2. ~~**Debug-Statements**~~ - `print()` durch `logger` ersetzt ✅
3. ~~**Alte Dateien**~~ - `database_old.py`, `login_dialog_old.py`, `nul` gelöscht ✅
4. ~~**CSS transform Fehler**~~ - Nicht unterstützte Property entfernt ✅
5. ~~**Lock-Crash**~~ - TypeError beim Sperren behoben ✅
6. ~~**Theme-Bug**~~ - Theme-Wechsel funktioniert komplett ✅
7. ~~**KeyError Settings**~~ - 'background_primary' → 'background' korrigiert ✅

### FEATURES HINZUGEFÜGT (2025-12-01)
- Button-Press-Animationen (animator.press())
- Einstellungs-Dialog (Theme, Auto-Lock, Zwischenablage, 2FA-Info)
- Cleaner Header (kompakter Lock-Button)
- 7 animierte Buttons in Dialogen

### NIEDRIG (optional)
- **Exception-Handling**: `entry_dialog.py:353` - Logging für Notizen-Entschlüsselung
- **Code-Review**: main_window.py (~700 Zeilen) - Evtl. später aufteilen

---

## 4. Projekt-Struktur (Überblick)

```
PasswortManager/
├── main.py                  # Entry Point - hier startet alles
├── requirements.txt         # Python Dependencies
│
├── src/
│   ├── auth/               # Master-Passwort Hashing (Argon2id)
│   ├── core/               # Verschlüsselung, Datenbank, Modelle
│   ├── gui/                # Alle UI-Komponenten (PyQt6)
│   ├── password/           # Generator + Stärke-Bewertung
│   └── utils/              # Zwischenablage
│
└── tests/                  # pytest Tests
```

---

## 5. Wichtigste Konzepte

### Globale Singleton-Instanzen
```python
# Diese Instanzen sind überall verfügbar
from src.core.encryption import encryption_manager
from src.core.settings import app_settings
from src.gui.themes import theme
from src.gui.icons import icon_provider
from src.utils.clipboard import clipboard_manager
```

### Verschlüsselungsfluss
```
Master-Passwort
    ↓ SHA256
Fernet Key
    ↓ AES-256
Verschlüsselte .spdb Datei
    ↓ Temporär entschlüsselt
SQLite (Passwörter nochmal verschlüsselt)
```

### Datenfluss
```
Start → Database Selector → Login → Main Window
                                        ↓
                                   Auto-Lock (5 Min.)
```

---

## 6. Häufige Aufgaben

### Neues Feature hinzufügen
1. Modell in `src/core/models.py` anpassen (falls nötig)
2. Datenbank-Schema in `src/core/database.py` erweitern
3. UI-Komponente in `src/gui/` erstellen
4. Tests in `tests/` schreiben
5. `pytest` ausführen

### UI-Komponente erstellen
```python
# Immer diese Importe verwenden
from src.gui.themes import theme
from src.gui.icons import icon_provider
from src.gui.animations import animator

# Theme-Farben verwenden
colors = theme.get_colors()
button.setStyleSheet(f"background: {colors['primary']};")

# Icons verwenden
icon = icon_provider.get_icon("lock", colors["icon_primary"], 24)
button.setIcon(icon)

# Animationen
animator.fade_in(widget, duration=300)
```

### Verschlüsselung verwenden
```python
from src.core.encryption import encryption_manager

# Verschlüsseln
encrypted = encryption_manager.encrypt("mein_passwort")  # bytes

# Entschlüsseln
decrypted = encryption_manager.decrypt(encrypted)  # str
```

---

## 7. Git-Status

**Branch**: main
**Letzte Commits**: UI-Layout-Fixes (5 Commits)

**Uncommitted**:
- `.claude/settings.local.json` (modified)

---

## 8. Tastenkombinationen im Code

- **Ctrl+L**: Anwendung sperren
- **Ctrl+D**: Dark Mode umschalten
- **Ctrl+Q**: Beenden

---

## 9. Datenbankstruktur (schnell)

```sql
users            → id, password_hash (Argon2id)
categories       → id, name, color
password_entries → id, name, username, encrypted_password, ...
```

---

## 10. Wenn du stecken bleibst

### Code verstehen
```bash
# Suche nach Funktionen/Klassen
Grep: "class DatabaseManager"
Grep: "def encrypt"

# Finde alle UI-Dialoge
Glob: "src/gui/*_dialog.py"

# Finde alle Tests
Glob: "tests/test_*.py"
```

### Dokumentation finden
- **Vollständig**: `.claude/knowledge-base.md`
- **Projekt**: `README.md`, `DATABASE.md`, `DESIGN.md`, `FEATURES.md`

---

## 11. Git Workflow

**WICHTIG**: Immer Branches für Features/Fixes erstellen!

```bash
# Feature starten
git checkout -b feature/mein-feature

# Committen
git add <dateien>
git commit -m "feat: Beschreibung"

# Pushen
git push -u origin feature/mein-feature

# PR erstellen
gh pr create
```

**Vollständige Dokumentation**: `.claude/GIT_WORKFLOW.md`

---

## 12. Checkliste für Nachfolger

Beim ersten Mal:
- [ ] `.claude/knowledge-base.md` vollständig lesen
- [ ] Projekt einmal starten (`python main.py`)
- [ ] Tests ausführen (`pytest`)
- [ ] Hauptdateien überfliegen (database.py, main_window.py, encryption.py)

Bei jeder neuen Aufgabe:
- [ ] In `knowledge-base.md` nachschlagen
- [ ] Relevanten Code lesen
- [ ] Tests schreiben/ausführen
- [ ] Wissensdatenbank aktualisieren (falls größere Änderungen)

---

**Du bist bereit! Bei Fragen: Konsultiere `.claude/knowledge-base.md`**
