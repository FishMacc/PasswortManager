# SecurePass Manager

Ein sicherer Passwort-Manager mit Master-Passwort und modernnem PyQt6-Interface.

## Features

### ✨ Neues in Version 1.1

**Verschlüsselte Datenbank-Dateien (wie KeePass):**
- **Einzelne .spdb Datei** - Gesamte Datenbank in einer verschlüsselten Datei
- **Cloud-Sync fähig** - Einfach mit Dropbox, Google Drive, etc. synchronisieren
- **Frei wählbarer Speicherort** - Speichere Datenbank wo du willst
- **Mehrere Datenbanken** - Erstelle verschiedene Datenbanken (Privat, Arbeit, etc.)
- **Kürzlich verwendet** - Schneller Zugriff auf letzte Datenbanken
- **Vollständige AES-256 Verschlüsselung** der gesamten Datenbank-Datei

**Modernes Design:**
- **Apple-Stil UI** mit flüssigen Animationen und Übergängen
- **SVG-Icons** für gestochen scharfe Darstellung auf allen Displays
- **Responsive Design** optimiert für alle Bildschirmgrößen
- **Smooth Animationen** (Fade, Slide, Scale, Pulse) für bessere UX
- **Dark & Light Mode** mit sofortigem Themenwechsel
- **Verbesserte Bedienbarkeit** durch moderne, intuitive Oberfläche

### Sicherheit
- **AES-256 Verschlüsselung** für alle Passwörter und Notizen
- **Argon2id Hashing** für das Master-Passwort
- **Auto-Lock** nach 5 Minuten Inaktivität
- **Sichere Zwischenablage** mit automatischer Löschung nach 30 Sekunden
- Keine Plaintext-Speicherung von sensiblen Daten

### Funktionen
- **Master-Passwort System**
  - Beim ersten Start: Master-Passwort erstellen
  - Login mit Master-Passwort bei jedem Start
  - Alle Daten werden mit dem Master-Passwort verschlüsselt

- **Kategorien-System**
  - Standard-Kategorien: Allgemein, Banking, Social Media, E-Mail
  - Eigene Kategorien erstellen und verwalten
  - Farbliche Kennzeichnung

- **Passwort-Verwaltung**
  - Passwörter sicher speichern mit Name, Username, Passwort, URL und Notizen
  - Passwörter anzeigen/verstecken
  - Passwörter in Zwischenablage kopieren
  - Suche über alle Einträge

- **Passwort-Generator**
  - Einstellbare Länge (8-64 Zeichen)
  - Konfigurierbare Zeichensätze (Groß-/Kleinbuchstaben, Zahlen, Sonderzeichen)
  - Echtzeit-Stärkeanzeige
  - Direktes Übernehmen in Einträge

## Installation

### Voraussetzungen
- Python 3.8 oder höher
- pip (Python Package Manager)

### Schritte

1. **Repository klonen oder Dateien herunterladen**
   ```bash
   cd PasswortManager
   ```

2. **Abhängigkeiten installieren**
   ```bash
   pip install -r requirements.txt
   ```

3. **Anwendung starten**
   ```bash
   python main.py
   ```

## Erste Schritte

### 1. Datenbank erstellen
Beim ersten Start wirst du aufgefordert, eine Datenbank zu erstellen:
- Wähle "Neue Datenbank erstellen"
- Gib einen Namen ein (z.B. "Meine Passwörter")
- Wähle einen Speicherort (Standard: Dokumente/SecurePass/)
- Erstelle ein starkes Master-Passwort (mindestens 8 Zeichen)
- **Wichtig**: Das Master-Passwort kann nicht wiederhergestellt werden!

**Für Cloud-Sync:**
- Wähle einen Cloud-Ordner als Speicherort (z.B. Dropbox/SecurePass/)
- Die .spdb Datei wird automatisch synchronisiert
- Auf anderen Geräten: "Datenbank öffnen" und zur Cloud-Datei navigieren

### 2. Einträge hinzufügen
- Klicke auf "+ Neuer Eintrag"
- Fülle die Felder aus (Name, Kategorie, Username, Passwort)
- Nutze den Passwort-Generator (🎲) für sichere Passwörter
- Klicke auf "Speichern"

### 3. Passwörter verwalten
- **Anzeigen**: Klicke auf das Augen-Symbol (👁) um ein Passwort zu sehen
- **Kopieren**: Klicke auf das Clipboard-Symbol (📋) um es zu kopieren
- **Bearbeiten**: Klicke auf das Stift-Symbol (✏️)
- **Löschen**: Klicke auf das Papierkorb-Symbol (🗑)

### 4. Kategorien nutzen
- Klicke in der Sidebar auf eine Kategorie, um nur deren Einträge zu sehen
- Erstelle eigene Kategorien mit "+ Neue Kategorie"
- "Alle" zeigt alle Einträge unabhängig von der Kategorie

### 5. Suche verwenden
- Nutze das Suchfeld oben rechts
- Suche funktioniert über Name und Username

## Sicherheitshinweise

### Master-Passwort
- **Wähle ein starkes Master-Passwort** mit mindestens 12 Zeichen
- Verwende Groß- und Kleinbuchstaben, Zahlen und Sonderzeichen
- **Teile dein Master-Passwort niemals** mit anderen
- **Es gibt keine Wiederherstellung** - wenn du es vergisst, sind alle Daten verloren

### Auto-Lock
- Die Anwendung sperrt sich automatisch nach 5 Minuten Inaktivität
- Du musst dein Master-Passwort erneut eingeben
- Dies schützt deine Daten, wenn du den Computer verlässt

### Zwischenablage
- Kopierte Passwörter werden nach 30 Sekunden automatisch aus der Zwischenablage gelöscht
- Dies verhindert, dass Passwörter unbeabsichtigt woanders eingefügt werden

### Backup
- Deine Daten werden in einer `.spdb` Datei gespeichert (Standard: Dokumente/SecurePass/)
- **Empfohlen**: Speichere die Datenbank in einem Cloud-Ordner für automatisches Backup
- **Alternativ**: Kopiere die .spdb Datei regelmäßig auf einen externen Speicher
- Die Datenbank-Datei ist vollständig verschlüsselt und kann nur mit dem Master-Passwort geöffnet werden
- **Versionierung**: Viele Cloud-Dienste bewahren alte Versionen auf - nutze dies für zusätzliche Sicherheit!

## Dateistruktur

```
PasswortManager/
├── main.py                 # Entry Point
├── requirements.txt        # Python-Abhängigkeiten
├── README.md              # Diese Datei
├── data/
│   └── passwords.db       # SQLite-Datenbank (wird beim ersten Start erstellt)
└── src/
    ├── core/              # Kern-Module
    │   ├── encryption.py  # AES-256 Verschlüsselung
    │   ├── database.py    # SQLite-Verwaltung
    │   └── models.py      # Datenmodelle
    ├── auth/              # Authentifizierung
    │   └── master_password.py  # Argon2 Hashing
    ├── password/          # Passwort-Tools
    │   ├── generator.py   # Generator
    │   └── strength.py    # Stärke-Bewertung
    ├── gui/               # Benutzeroberfläche
    │   ├── main_window.py
    │   ├── login_dialog.py
    │   ├── entry_dialog.py
    │   ├── generator_dialog.py
    │   └── widgets.py
    └── utils/             # Hilfsfunktionen
        └── clipboard.py   # Zwischenablage-Manager
```

## Technische Details

### Verschlüsselung
- **Algorithmus**: AES-256 (via Fernet)
- **Key-Derivation**: SHA256 des Master-Passworts
- **Master-Passwort**: Argon2id mit sicheren Parametern
  - Time cost: 2
  - Memory cost: 64 MB
  - Parallelism: 4

### Datenbank
- **Format**: SQLite
- **Tabellen**: users, categories, password_entries
- **Verschlüsselte Felder**: password, notes, totp_secret

### GUI & Design
- **Framework**: PyQt6
- **Icons**: SVG-basiert für skalierbare, gestochen scharfe Darstellung
- **Animationen**: Smooth Transitions (Fade, Slide, Scale, Pulse, Shake)
- **Layout**: Vollständig responsive mit modernen Abständen
- **Style**: Apple-inspiriertes Design mit Dark & Light Mode
- **Responsive**: Mindestgrößen für alle Dialoge und optimierte Layouts

## Häufige Fragen

**F: Kann ich mein Master-Passwort ändern?**
A: Aktuell nicht implementiert. Eine zukünftige Version könnte diese Funktion enthalten.

**F: Kann ich meine Daten exportieren?**
A: Die Datenbank liegt in `data/passwords.db`. Du kannst diese Datei kopieren, aber sie ist verschlüsselt.

**F: Ist die Anwendung sicher genug für sensible Daten?**
A: Die Anwendung verwendet industriestandard Verschlüsselung (AES-256, Argon2). Für private Nutzung ist sie sicher, aber sie wurde nicht professionell auditiert.

**F: Läuft die Anwendung auf macOS/Linux?**
A: Ja! PyQt6 und alle verwendeten Libraries sind plattformübergreifend.

## Lizenz

Dieses Projekt ist für Bildungszwecke erstellt worden.

## Unterstützung

Bei Problemen oder Fragen, erstelle ein Issue im Repository.

---

**⚠️ WICHTIG: Dieses Passwort-Manager-Tool wurde zu Bildungszwecken erstellt. Erstelle regelmäßig Backups und bewahre dein Master-Passwort sicher auf!**
