"""
Anwendungs-Einstellungen und Konfiguration

Speichert Benutzereinstellungen wie letzte Datenbank, Theme-Modus, etc.
"""
import json
import os
from pathlib import Path
from typing import Optional


class AppSettings:
    """Verwaltet Anwendungseinstellungen"""

    def __init__(self):
        self.settings_dir = Path.home() / ".securepass"
        self.settings_file = self.settings_dir / "settings.json"
        self.settings = self._load_settings()

    def _load_settings(self) -> dict:
        """Lädt Einstellungen aus Datei"""
        if not self.settings_file.exists():
            return self._get_default_settings()

        try:
            with open(self.settings_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return self._get_default_settings()

    def _get_default_settings(self) -> dict:
        """Gibt Standard-Einstellungen zurück"""
        return {
            "last_database": None,
            "recent_databases": [],
            "theme_mode": "light",
            "auto_lock_minutes": 5,
            "clipboard_clear_seconds": 30,
            "window_geometry": None,
        }

    def save(self):
        """Speichert Einstellungen in Datei"""
        try:
            # Erstelle Verzeichnis falls nicht vorhanden
            self.settings_dir.mkdir(parents=True, exist_ok=True)

            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2)
        except Exception as e:
            print(f"Fehler beim Speichern der Einstellungen: {e}")

    def get(self, key: str, default=None):
        """Gibt einen Einstellungswert zurück"""
        return self.settings.get(key, default)

    def set(self, key: str, value):
        """Setzt einen Einstellungswert"""
        self.settings[key] = value
        self.save()

    def get_last_database(self) -> Optional[str]:
        """Gibt den Pfad zur zuletzt verwendeten Datenbank zurück"""
        return self.settings.get("last_database")

    def set_last_database(self, path: str):
        """Setzt die zuletzt verwendete Datenbank"""
        self.settings["last_database"] = path
        self._add_to_recent(path)
        self.save()

    def _add_to_recent(self, path: str):
        """Fügt Datenbank zu den kürzlich verwendeten hinzu"""
        recent = self.settings.get("recent_databases", [])

        # Entferne Pfad falls bereits vorhanden
        if path in recent:
            recent.remove(path)

        # Füge am Anfang hinzu
        recent.insert(0, path)

        # Behalte nur die letzten 5
        self.settings["recent_databases"] = recent[:5]

    def get_recent_databases(self) -> list:
        """Gibt Liste der kürzlich verwendeten Datenbanken zurück"""
        recent = self.settings.get("recent_databases", [])
        # Filtere nur existierende Dateien
        return [db for db in recent if os.path.exists(db)]

    def clear_recent_databases(self):
        """Löscht Liste der kürzlich verwendeten Datenbanken"""
        self.settings["recent_databases"] = []
        self.save()


# Globale Instanz
app_settings = AppSettings()
