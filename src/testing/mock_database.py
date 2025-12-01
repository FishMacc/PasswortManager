"""
Mock-Datenbank für UI-Tests

Erstellt temporäre Test-Datenbanken mit Beispieldaten
für sichere UI-Tests ohne echte Benutzerdaten zu gefährden.
"""
import tempfile
import os
from pathlib import Path
from typing import List, Optional
from ..core.database import DatabaseManager
from ..core.database_file import DatabaseFile
from ..core.models import Category, PasswordEntry
from ..auth.master_password import master_password_manager


class MockDatabase:
    """Mock-Datenbank für Tests"""

    def __init__(self, master_password: str = "TestPassword123!"):
        self.master_password = master_password
        self.temp_dir = None
        self.db_file_path = None
        self.db_manager: Optional[DatabaseManager] = None

    def setup(self) -> DatabaseManager:
        """Erstellt eine temporäre Test-Datenbank"""
        # Temporäres Verzeichnis
        self.temp_dir = tempfile.mkdtemp(prefix="securepass_test_")
        self.db_file_path = os.path.join(self.temp_dir, "test_passwords.spdb")

        # Erstelle verschlüsselte Datenbank-Datei
        db_file = DatabaseFile()
        db_file.create_new(self.db_file_path, self.master_password)

        # Öffne Datenbank
        success = db_file.open(self.db_file_path, self.master_password)
        if not success:
            raise RuntimeError("Konnte Test-Datenbank nicht öffnen")

        # DatabaseManager initialisieren
        self.db_manager = DatabaseManager(db_file)

        # Master-Passwort speichern
        pw_hash = master_password_manager.hash_password(self.master_password)
        self.db_manager.set_master_password(pw_hash)

        # Beispieldaten hinzufügen
        self._populate_test_data()

        return self.db_manager

    def _populate_test_data(self):
        """Füllt die Datenbank mit Testdaten"""
        # Kategorien sind bereits vorhanden (Standard-Kategorien)
        categories = self.db_manager.get_all_categories()

        # Teste Passwort-Einträge hinzufügen
        test_entries = [
            {
                "name": "Test Gmail",
                "username": "testuser@gmail.com",
                "password": "TestPass123!",
                "website_url": "https://gmail.com",
                "notes": "Test E-Mail Account",
                "category_id": self._get_category_id_by_name(categories, "E-Mail")
            },
            {
                "name": "Test Bank",
                "username": "test_user",
                "password": "SecureBank456!",
                "website_url": "https://example-bank.com",
                "notes": "Test Banking Account",
                "category_id": self._get_category_id_by_name(categories, "Banking")
            },
            {
                "name": "Test Twitter",
                "username": "@testuser",
                "password": "Twitter789!",
                "website_url": "https://twitter.com",
                "notes": "Test Social Media",
                "category_id": self._get_category_id_by_name(categories, "Social Media")
            },
            {
                "name": "Test Website",
                "username": "admin",
                "password": "Admin2024!",
                "website_url": "https://test-website.com",
                "notes": "General test entry",
                "category_id": self._get_category_id_by_name(categories, "Allgemein")
            },
            {
                "name": "Test GitHub",
                "username": "testdev",
                "password": "GitHub2024!",
                "website_url": "https://github.com",
                "notes": "Development account",
                "category_id": self._get_category_id_by_name(categories, "Allgemein")
            }
        ]

        for entry_data in test_entries:
            entry = PasswordEntry(
                id=0,  # Wird von DB gesetzt
                category_id=entry_data["category_id"],
                name=entry_data["name"],
                username=entry_data["username"],
                password=entry_data["password"],
                website_url=entry_data["website_url"],
                notes=entry_data["notes"]
            )
            self.db_manager.add_password_entry(entry)

    def _get_category_id_by_name(self, categories: List[Category], name: str) -> int:
        """Findet Kategorie-ID nach Name"""
        for cat in categories:
            if cat.name == name:
                return cat.id
        # Fallback: Erste Kategorie
        return categories[0].id if categories else 1

    def cleanup(self):
        """Löscht temporäre Test-Datenbank"""
        if self.db_manager:
            self.db_manager.close()
            self.db_manager = None

        if self.db_file_path and os.path.exists(self.db_file_path):
            try:
                os.remove(self.db_file_path)
            except Exception as e:
                print(f"Warnung: Konnte Test-DB nicht löschen: {e}")

        if self.temp_dir and os.path.exists(self.temp_dir):
            try:
                os.rmdir(self.temp_dir)
            except Exception as e:
                print(f"Warnung: Konnte Temp-Dir nicht löschen: {e}")

    def get_test_credentials(self) -> dict:
        """Gibt Test-Zugangsdaten zurück"""
        return {
            "master_password": self.master_password,
            "db_path": self.db_file_path
        }

    def __enter__(self):
        """Context Manager Enter"""
        return self.setup()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context Manager Exit"""
        self.cleanup()
