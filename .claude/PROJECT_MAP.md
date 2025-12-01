# SecurePass Manager - Projekt-Map

Visuelle Übersicht über das Projekt für schnelle Orientierung.

---

## 🗺️ Datei-Landkarte

```
PasswortManager/
│
├── 🚀 main.py                              # START HIER! Entry Point
│
├── 📦 requirements.txt                     # Dependencies (pip install -r)
├── ⚙️ pytest.ini                          # Test-Konfiguration
│
├── 📂 src/                                # HAUPTCODE
│   │
│   ├── 🔐 auth/                           # Authentifizierung
│   │   └── master_password.py            # Argon2id Hashing (65 Zeilen)
│   │
│   ├── 🧠 core/                           # Kern-Logik
│   │   ├── database.py ⭐                # DatabaseManager (329 Zeilen)
│   │   ├── database_file.py ⭐           # .spdb Verschlüsselung (300 Zeilen)
│   │   ├── encryption.py ⭐              # AES-256 Fernet (81 Zeilen)
│   │   ├── models.py                     # Datenmodelle (46 Zeilen)
│   │   ├── settings.py                   # App-Einstellungen (Persistent)
│   │   │
│   │   └── 🗑️ database_old.py           # ALT - Entfernen!
│   │
│   ├── 🎨 gui/                            # Benutzeroberfläche
│   │   ├── main_window.py ⭐⭐           # Hauptfenster (705 Zeilen) !!!
│   │   ├── database_selector.py          # DB-Auswahl Dialog
│   │   ├── database_new.py               # Neue DB erstellen Dialog
│   │   ├── login_dialog.py               # Master-PW Eingabe
│   │   ├── entry_dialog.py               # Passwort-Eintrag Dialog
│   │   ├── generator_dialog.py           # Passwort-Generator Dialog
│   │   │
│   │   ├── widgets.py ⭐                 # Custom Widgets (420 Zeilen)
│   │   ├── themes.py ⭐                  # Dark/Light Mode (404 Zeilen)
│   │   ├── icons.py ⭐                   # SVG-Icons (248 Zeilen)
│   │   ├── animations.py ⭐              # UI-Animationen (324 Zeilen)
│   │   ├── responsive.py                 # Responsive Design
│   │   │
│   │   └── 🗑️ login_dialog_old.py       # ALT - Entfernen!
│   │
│   ├── 🔑 password/                       # Passwort-Tools
│   │   ├── generator.py                  # Kryptografisch sicherer Generator
│   │   └── strength.py                   # Stärke-Bewertung
│   │
│   └── 🛠️ utils/                          # Hilfsfunktionen
│       └── clipboard.py                  # Auto-Clear Zwischenablage
│
├── 🧪 tests/                              # Unit Tests
│   ├── test_database.py
│   ├── test_encryption.py
│   ├── test_master_password.py
│   ├── test_password_generator.py
│   └── test_password_strength.py
│
└── 📚 .claude/                            # Wissensdatenbank
    ├── knowledge-base.md ⭐⭐            # HAUPTDOKUMENTATION
    ├── QUICK_START.md ⭐                # Schnelleinstieg
    ├── SESSION_LOG.md                   # Änderungs-Protokoll
    ├── PROJECT_MAP.md                   # Diese Datei
    └── README.md                        # Übersicht .claude/

Legende:
⭐ = Wichtige Datei
⭐⭐ = Kritische Datei (Start hier)
🗑️ = Entfernen (veraltet)
```

---

## 🎯 Wo fange ich an?

### Projekt verstehen (5 Minuten)
1. **`.claude/QUICK_START.md`** - Übersicht
2. **`main.py`** - Entry Point (Startprozess)
3. **`src/core/database.py`** - Datenbank-Logik
4. **`src/gui/main_window.py`** - Hauptfenster

### Feature hinzufügen
1. **`src/core/models.py`** - Datenmodell anpassen?
2. **`src/core/database.py`** - CRUD-Methoden?
3. **`src/gui/`** - UI-Komponente erstellen
4. **`tests/`** - Tests schreiben

### Bug fixen
1. **`.claude/knowledge-base.md`** - "Bekannte Issues"
2. **Grep/Glob** - Fehler-Stelle finden
3. **Read** - Datei lesen
4. **Edit** - Reparieren

---

## 🔥 Hot Files (häufig bearbeitet)

### Top 5 - Diese Dateien ändern sich oft

1. **`src/gui/main_window.py`** (705 Zeilen)
   - Hauptfenster-Logik
   - Layout-Änderungen (letzte 5 Commits!)
   - Auto-Lock, Theme-Toggle

2. **`src/core/database.py`** (329 Zeilen)
   - CRUD für Passwörter
   - Kategorie-Management
   - Zentrale Datenbank-Schnittstelle

3. **`src/gui/widgets.py`** (420 Zeilen)
   - PasswordEntryWidget
   - CategoryButton
   - UI-Updates

4. **`src/gui/themes.py`** (404 Zeilen)
   - Dark/Light Mode
   - Farbpaletten
   - Globales Stylesheet

5. **`src/gui/entry_dialog.py`**
   - Passwort-Eintrag bearbeiten
   - Formular-Validierung

---

## 🛡️ Security Files (nicht anfassen ohne Grund)

### Diese Dateien sind sicherheitskritisch

- **`src/core/encryption.py`** - AES-256 Verschlüsselung
- **`src/core/database_file.py`** - .spdb Verschlüsselung
- **`src/auth/master_password.py`** - Argon2id Hashing
- **`src/password/generator.py`** - Kryptografisch sicherer Generator

**Warnung**: Änderungen hier können Sicherheit kompromittieren!

---

## 📊 Datei-Größen (Top 10)

| Datei | Zeilen | Wichtigkeit | Status |
|-------|--------|-------------|--------|
| `gui/main_window.py` | 705 | ⭐⭐⭐ | Aktiv |
| `gui/widgets.py` | 420 | ⭐⭐ | Aktiv |
| `gui/themes.py` | 404 | ⭐⭐ | Stabil |
| `core/database.py` | 329 | ⭐⭐⭐ | Aktiv |
| `gui/animations.py` | 324 | ⭐ | Stabil |
| `core/database_file.py` | 300 | ⭐⭐⭐ | Stabil |
| `gui/icons.py` | 248 | ⭐ | Stabil |
| `password/strength.py` | 102 | ⭐ | Stabil |
| `password/generator.py` | 86 | ⭐⭐ | Stabil |
| `core/encryption.py` | 81 | ⭐⭐⭐ | Stabil |

---

## 🔄 Datenfluss-Diagramm

```
┌─────────────────────────────────────────────────────────────┐
│                         main.py                             │
│                    (Application Start)                      │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              database_selector.py                           │
│           (Wähle/Erstelle Datenbank)                        │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                 login_dialog.py                             │
│            (Master-Passwort eingeben)                       │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                database_file.py                             │
│        (Entschlüssele .spdb → Temp SQLite)                  │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                  database.py                                │
│         (DatabaseManager initialisiert)                     │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                 main_window.py                              │
│           (Hauptfenster angezeigt)                          │
│                                                             │
│  ┌──────────────┬─────────────┬───────────────┐           │
│  │ Sidebar      │ Content     │ Header        │           │
│  │ (Kategorien) │ (Einträge)  │ (Suche, Lock) │           │
│  └──────────────┴─────────────┴───────────────┘           │
│                                                             │
│  ┌─────────────────────────────────────────────┐          │
│  │         Auto-Lock Timer (5 Min.)            │          │
│  └─────────────────────────────────────────────┘          │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
        ┌─────────────────────────┐
        │   Benutzeraktionen      │
        └─────────────────────────┘
                │
    ┌───────────┼───────────┬──────────────┐
    │           │           │              │
    ▼           ▼           ▼              ▼
entry_dialog  generator  Lock           Suche
(Bearbeiten)  (PW Gen)  (Zurück zu     (Filter)
                         Login)
```

---

## 🧩 Modul-Abhängigkeiten

```
main.py
  └─> gui/database_selector.py
        └─> gui/database_new.py
              └─> core/database_file.py
                    └─> core/encryption.py
  └─> gui/login_dialog.py
        └─> auth/master_password.py
  └─> core/database.py
        └─> core/models.py
        └─> core/encryption.py
  └─> gui/main_window.py
        ├─> gui/widgets.py
        ├─> gui/themes.py
        ├─> gui/icons.py
        ├─> gui/animations.py
        ├─> gui/entry_dialog.py
        │     └─> gui/generator_dialog.py
        │           └─> password/generator.py
        │           └─> password/strength.py
        └─> utils/clipboard.py
```

---

## 🎨 UI-Komponenten-Baum

```
MainWindow
│
├─ QWidget (Central Widget)
│   │
│   └─ QSplitter (Horizontal)
│       │
│       ├─ QWidget (Sidebar)
│       │   ├─ QLabel (Logo + Titel)
│       │   ├─ QScrollArea
│       │   │   └─ QVBoxLayout
│       │   │       ├─ CategoryButton ("Alle")
│       │   │       ├─ CategoryButton (x4 Standard)
│       │   │       └─ QPushButton ("+ Neue Kategorie")
│       │   └─ ...
│       │
│       └─ QWidget (Content)
│           ├─ QHBoxLayout (Header)
│           │   ├─ QLabel (Titel)
│           │   └─ QPushButton ("+ Neuer Eintrag")
│           │
│           └─ QScrollArea
│               └─ QVBoxLayout
│                   ├─ PasswordEntryWidget (Entry 1)
│                   ├─ PasswordEntryWidget (Entry 2)
│                   └─ ...
│
├─ QMenuBar
│   ├─ "Datei" (Sperren, Beenden)
│   ├─ "Ansicht" (Dark Mode)
│   └─ "Hilfe" (Über)
│
└─ QTimer (Auto-Lock)
```

---

## 🔍 Schnelle Code-Suche

### Finde wichtige Funktionen

```bash
# Verschlüsselung
Grep: "def encrypt" → src/core/encryption.py:33

# Master-Passwort verifizieren
Grep: "def verify_password" → src/auth/master_password.py:38

# Passwörter laden
Grep: "def get_all_password_entries" → src/core/database.py:169

# Passwort-Generator
Grep: "def generate" → src/password/generator.py:45

# Auto-Lock
Grep: "def lock_application" → src/gui/main_window.py:568

# Theme wechseln
Grep: "def toggle_mode" → src/gui/themes.py:89
```

### Finde UI-Komponenten

```bash
# Alle Dialoge
Glob: "src/gui/*_dialog.py"

# Alle Widgets
Grep: "class.*Widget" → src/gui/widgets.py

# Alle Tests
Glob: "tests/test_*.py"
```

---

## 📈 Projekt-Statistik

**Code-Zeilen** (ca.):
- Gesamt: ~5000 Zeilen
- Core-Logik: ~1100 Zeilen
- GUI: ~3200 Zeilen
- Passwort-Tools: ~200 Zeilen
- Tests: ~500 Zeilen

**Module**:
- Hauptmodule: 15
- Tests: 5
- Veraltete: 2

**UI-Komponenten**:
- Dialoge: 5
- Custom Widgets: 2
- Icons: 21 SVG

**Singletons**: 8

---

## 🚨 Kritische Stellen (Achtung!)

### ⚠️ Problem-Bereiche

1. **`src/core/database.py:323-328`**
   - Destruktor mit bare `pass`
   - Risk: Temporäre Dateien nicht gelöscht

2. **`src/gui/main_window.py:550-580`**
   - Auto-Lock Timer
   - Frequent changes (letzte Commits)

3. **`src/gui/*_dialog.py`**
   - Layout-Probleme (letzte 5 Commits)
   - Responsive Design instabil

4. **`src/core/database_old.py`**
   - Veralteter Code
   - Sollte entfernt werden

---

## ✅ Checkliste für Neulinge

Erste Schritte:
- [ ] `.claude/QUICK_START.md` gelesen
- [ ] `main.py` verstanden (Entry Point)
- [ ] `src/core/database.py` überflogen
- [ ] `src/gui/main_window.py` überflogen
- [ ] Projekt gestartet (`python main.py`)
- [ ] Tests ausgeführt (`pytest`)

Entwicklung:
- [ ] Wissensdatenbank konsultiert
- [ ] Code-Stil verstanden (Singletons, MVC)
- [ ] Sicherheits-Checkliste gelesen
- [ ] Tests geschrieben

---

**Letzte Aktualisierung**: 2025-12-01
**Status**: Vollständig & aktuell
