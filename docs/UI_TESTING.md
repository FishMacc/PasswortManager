# UI Testing Guide

Anleitung für das Testen der Benutzeroberfläche des SecurePass Managers.

## 🧪 UI Test Tool

Das Projekt enthält ein umfassendes UI-Test-Tool (`test_ui.py`), das automatisierte und interaktive Tests ermöglicht.

## Installation

Keine zusätzlichen Dependencies nötig - verwendet die gleichen Pakete wie die Hauptanwendung.

## Verwendung

### Interaktiver Modus (Empfohlen)

Öffnet ein grafisches Test-Fenster mit allen Test-Optionen:

```bash
python test_ui.py --interactive
```

Oder einfach:

```bash
python test_ui.py
```

### CLI-Modus

Führt Tests ohne GUI aus (für CI/CD):

```bash
# Alle Tests
python test_ui.py --test all

# Nur Theme-Tests
python test_ui.py --test theme

# Nur Dialog-Tests
python test_ui.py --test settings
```

## 🎨 Verfügbare Tests

### 1. Theme-Tests

**Manuelle Tests:**
- ☀️ **Light Mode**: Wechselt zu Light Mode und prüft Farben
- 🌙 **Dark Mode**: Wechselt zu Dark Mode und prüft Farben
- 🔄 **Toggle Theme**: Wechselt zwischen Modi hin und her

**Automatische Tests:**
- ▶️ **Theme Cycle Test**: Testet alle Theme-Modi automatisch nacheinander
  - Light → Dark → Toggle → Toggle
  - Dauer: ~5 Sekunden

### 2. Dialog-Tests

**Manuelle Tests:**
- ⚙️ **Einstellungs-Dialog**: Öffnet Settings im aktuellen Theme
- ⚙️ **Settings (Dark Mode)**: Wechselt zu Dark und öffnet Settings

**Automatische Tests:**
- Testet Dialog-Öffnung in beiden Themes
- Prüft Theme-Refresh während Dialog offen ist

### 3. Full UI Test

▶️ **Full UI Test** führt alle Tests nacheinander aus:
1. Light Mode + Settings Dialog
2. Dark Mode + Settings Dialog
3. Multiple Theme Toggles
4. Dauer: ~8 Sekunden

## 📋 Test-Output

Das Test-Tool zeigt Ergebnisse in Echtzeit:
- ℹ️ Info: Normale Log-Messages
- ✅ Success: Erfolgreiche Tests
- ❌ Error: Fehlgeschlagene Tests

Alle Logs werden auch in die Konsole geschrieben.

## 🎯 Was wird getestet?

### Theme-System
- ✅ Light Mode Farbanwendung
- ✅ Dark Mode Farbanwendung
- ✅ Theme-Wechsel ohne Neustart
- ✅ `theme_changed` Signal funktioniert
- ✅ Globales Stylesheet wird aktualisiert

### Settings-Dialog
- ✅ Dialog öffnet sich ohne Fehler
- ✅ Alle UI-Elemente werden gerendert
- ✅ Theme-Updates während Dialog offen
- ✅ Farben passen zum aktuellen Theme
- ✅ Buttons und Controls funktionieren

### Robustheit
- ✅ Keine AttributeErrors
- ✅ Keine Rendering-Fehler
- ✅ Keine Theme-Inkonsistenzen

## 🐛 Debugging

### Fehler reproduzieren

1. Starte interaktives Tool:
   ```bash
   python test_ui.py --interactive
   ```

2. Führe problematischen Test aus

3. Prüfe Test-Output im unteren Bereich

4. Logs findest du in:
   - Konsole: Detaillierte Logging-Messages
   - Test-Fenster: Zusammenfassung der Ergebnisse

### Häufige Probleme

**Dialog öffnet sich nicht:**
- Prüfe ob `theme_changed` Signal existiert
- Prüfe Theme-Klasse erbt von QObject

**Weiße/falsche Farben:**
- Prüfe ob `refresh_theme()` aufgerufen wird
- Prüfe ob alle Widgets im Dialog erfasst werden

**Crash beim Theme-Wechsel:**
- Prüfe ob alle Style-Updates exception-safe sind
- Prüfe ob alle referenzierten Widgets existieren

## 📊 Test-Metriken

Nach jedem Test zeigt das Tool:
- ✅ Anzahl erfolgreicher Tests
- ❌ Anzahl fehlgeschlagener Tests
- ⏱️ Ausführungszeit

## 🔄 CI/CD Integration

Für automatisierte Tests in CI/CD:

```bash
# In GitHub Actions, GitLab CI, etc.
python test_ui.py --test all
```

Exit Codes:
- `0`: Alle Tests erfolgreich
- `1+`: Anzahl fehlgeschlagener Tests

## 📝 Eigene Tests hinzufügen

Um neue Tests hinzuzufügen, editiere `test_ui.py`:

```python
def test_my_feature(self):
    """Testet mein neues Feature"""
    self.log_info("Teste mein Feature...")
    try:
        # Test-Code hier
        self.log_success("✓ Feature funktioniert")
    except Exception as e:
        self.log_error(f"✗ Feature fehlgeschlagen: {e}")
```

## 🚀 Best Practices

1. **Regelmäßig testen**: Führe Tests nach jeder UI-Änderung aus
2. **Beide Modi testen**: Teste immer Light UND Dark Mode
3. **Automatische Tests nutzen**: Für schnelle Regression-Tests
4. **Logs lesen**: Prüfe auch erfolgreiche Tests auf Warnungen

## 📚 Weitere Ressourcen

- **pytest Tests**: Siehe `tests/` für Unit-Tests
- **Logging**: `~/.securepass/logs/securepass.log`
- **Wissensdatenbank**: `.claude/knowledge-base.md`

---

**Letzte Aktualisierung**: 2025-12-01
**Version**: 1.0
