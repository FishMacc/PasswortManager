# SecurePass Manager

Ein lokal betriebener Passwort-Manager mit Master-Passwort-Schutz, moderner PyQt6-Oberfläche und verschlüsselter SQLite-Datenbank. Entwickelt zu Bildungszwecken.

## Features

- **Verschlüsselte Datenbank** – Alle Einträge und Notizen werden mit AES-256 gesichert; die Datenbankdatei (`.spdb`) ist cloud-sync-fähig.
- **Sicheres Master-Passwort** – Argon2id-Hashing mit Zeit-/Speicher-/Parallelitätsparametern.
- **TOTP/2FA-Unterstützung** – Einmalpasswörter für Dienste, die TOTP unterstützen.
- **Passwort-Generator** – Konfigurierbare Länge und Zeichensätze mit Echtzeit-Stärkeanzeige.
- **Kategorien & Suche** – Organisation in Gruppen und schnelle Volltextsuche.
- **Auto-Lock & Zwischenablage-Schutz** – Automatische Sperre nach Inaktivität und Löschung kopierter Passwörter nach 30 Sekunden.
- **Dark & Light Mode** – Sofortiger Themenwechsel über die Einstellungen.

## Voraussetzungen

- Python 3.8 oder höher
- `pip`

## Installation

```bash
git clone https://github.com/FishMacc/PasswortManager.git
cd PasswortManager
pip install -r requirements.txt
```

## Start

```bash
python main.py
```

## Erste Schritte

1. **Datenbank anlegen** – Beim ersten Start "Neue Datenbank erstellen" wählen, Speicherort festlegen und ein starkes Master-Passwort vergeben.
2. **Einträge hinzufügen** – Mit "+ Neuer Eintrag" Name, Kategorie, Benutzername, Passwort, URL und Notizen speichern.
3. **Passwörter nutzen** – Anzeigen, kopieren, bearbeiten oder löschen über die Symbole in der Eintragsliste.
4. **Cloud-Backup** – Die `.spdb`-Datei liegt an einem frei wählbaren Ort (z. B. Dropbox/Google Drive). Sie ist verschlüsselt und kann nur mit dem Master-Passwort geöffnet werden.

## Tests

```bash
# Alle Tests ausführen
pytest

# Mit Coverage-Report
pytest --cov=src --cov-report=html
```

Zusätzliche UI-Testtools:

```bash
python test_ui_comprehensive.py --test all   # CLI-Modus
python test_ui_comprehensive.py --interactive # Interaktives Test-Fenster
```

Siehe `docs/COMPREHENSIVE_UI_TESTING.md` und `docs/UI_TESTING.md` für Details.

## Sicherheitshinweise

- Das Master-Passwort kann **nicht wiederhergestellt** werden – bei Verlust sind alle Daten unlesbar.
- Wähle ein Master-Passwort mit mindestens 12 Zeichen, Groß-/Kleinbuchstaben, Zahlen und Sonderzeichen.
- Speichere regelmäßig Backups der `.spdb`-Datei an einem separaten Ort.
- Dieses Projekt wurde zu Bildungszwecken erstellt und ist nicht professionell auditiert.

## Technischer Überblick

| Komponente | Verwendung |
|------------|------------|
| Verschlüsselung | AES-256 über `cryptography` (Fernet) |
| Schlüsselableitung | Argon2id über `argon2-cffi` |
| Datenbank | SQLite mit Tabellen für Benutzer, Kategorien und Einträge |
| GUI | PyQt6 mit SVG-Icons und responsivem Layout |

Weitere Details zur Architektur finden sich in `DESIGN.md`, zur Datenbank in `DATABASE.md` und zum Beitragsworkflow in `CONTRIBUTING.md`.

## Lizenz

Dieses Projekt ist für Bildungszwecke erstellt worden.

---

**⚠️ Wichtig:** *SecurePass Manager* ist ein Lernprojekt. Verwende es nur für nicht-kritische Daten, solange kein unabhängiges Sicherheitsaudit vorliegt.
