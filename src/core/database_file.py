"""
Verschlüsseltes Datenbank-Datei Format

Erstellt und liest verschlüsselte .spdb (SecurePass Database) Dateien.
Die gesamte SQLite-Datenbank wird verschlüsselt in einer einzigen Datei gespeichert.
"""
import os
import sqlite3
import tempfile
import logging
from pathlib import Path
from typing import Optional
from cryptography.fernet import Fernet
import hashlib
import base64

logger = logging.getLogger(__name__)


class DatabaseFile:
    """Verwaltet verschlüsselte Datenbank-Dateien"""

    FILE_EXTENSION = ".spdb"
    FILE_HEADER = b"SECUREPASS_DB_V1"

    def __init__(self, file_path: str, master_password: Optional[str] = None):
        """
        Initialisiert DatabaseFile

        Args:
            file_path: Pfad zur Datenbank-Datei
            master_password: Master-Passwort für Ver-/Entschlüsselung
        """
        self.file_path = Path(file_path)
        self.master_password = master_password
        self.temp_db_path: Optional[Path] = None

    def _derive_key_from_password(self, password: str) -> bytes:
        """
        Leitet einen Verschlüsselungsschlüssel aus dem Passwort ab

        Args:
            password: Das Master-Passwort

        Returns:
            32-Byte Schlüssel für Fernet
        """
        # Verwende SHA256 und konvertiere zu Fernet-kompatiblem Format
        hash_bytes = hashlib.sha256(password.encode()).digest()
        return base64.urlsafe_b64encode(hash_bytes)

    def create_new(self, master_password: str):
        """
        Erstellt eine neue verschlüsselte Datenbank-Datei

        Args:
            master_password: Master-Passwort für die Verschlüsselung
        """
        self.master_password = master_password

        # Erstelle temporäre SQLite-Datenbank
        with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as tmp_file:
            temp_db = tmp_file.name

        try:
            # Erstelle leere Datenbank-Struktur
            conn = sqlite3.connect(temp_db)
            self._create_database_schema(conn)
            conn.close()

            # Lese Datenbank-Datei
            with open(temp_db, 'rb') as f:
                db_data = f.read()

            # Verschlüssele und speichere
            self._encrypt_and_save(db_data, master_password)

        finally:
            # Lösche temporäre Datei
            if os.path.exists(temp_db):
                os.remove(temp_db)

    def _create_database_schema(self, conn: sqlite3.Connection):
        """Erstellt das Datenbank-Schema"""
        cursor = conn.cursor()

        # Users Tabelle (für Master-Passwort Hash)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Kategorien Tabelle
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                color TEXT DEFAULT '#808080',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Standard-Kategorien einfügen
        default_categories = [
            ("Allgemein", "#6366f1"),
            ("Banking", "#10b981"),
            ("Social Media", "#8b5cf6"),
            ("E-Mail", "#f59e0b"),
        ]

        for name, color in default_categories:
            cursor.execute(
                "INSERT OR IGNORE INTO categories (name, color) VALUES (?, ?)",
                (name, color)
            )

        # Passwort-Einträge Tabelle
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS password_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                username TEXT,
                encrypted_password BLOB NOT NULL,
                encrypted_notes BLOB,
                website_url TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES categories (id)
            )
        """)

        conn.commit()

    def _encrypt_and_save(self, data: bytes, password: str):
        """
        Verschlüsselt Daten und speichert in Datei

        Args:
            data: Zu verschlüsselnde Daten
            password: Master-Passwort
        """
        # Verschlüssele Daten
        key = self._derive_key_from_password(password)
        fernet = Fernet(key)
        encrypted_data = fernet.encrypt(data)

        # Erstelle Verzeichnis falls nötig
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        # Schreibe Datei mit Header
        with open(self.file_path, 'wb') as f:
            f.write(self.FILE_HEADER)
            f.write(encrypted_data)

    def open_database(self, master_password: str) -> str:
        """
        Öffnet und entschlüsselt die Datenbank-Datei

        Args:
            master_password: Master-Passwort zum Entschlüsseln

        Returns:
            Pfad zur temporären entschlüsselten Datenbank

        Raises:
            ValueError: Wenn Datei nicht existiert oder Passwort falsch
            Exception: Bei anderen Fehlern
        """
        if not self.file_path.exists():
            raise ValueError(f"Datenbank-Datei nicht gefunden: {self.file_path}")

        self.master_password = master_password

        # Lese und entschlüssele Datei
        try:
            with open(self.file_path, 'rb') as f:
                # Prüfe Header
                header = f.read(len(self.FILE_HEADER))
                if header != self.FILE_HEADER:
                    raise ValueError("Ungültiges Dateiformat")

                # Lese verschlüsselte Daten
                encrypted_data = f.read()

            # Entschlüssele
            key = self._derive_key_from_password(master_password)
            fernet = Fernet(key)

            try:
                decrypted_data = fernet.decrypt(encrypted_data)
            except Exception:
                raise ValueError("Falsches Master-Passwort oder beschädigte Datei")

            # Erstelle temporäre Datenbank-Datei
            with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as tmp_file:
                tmp_file.write(decrypted_data)
                self.temp_db_path = Path(tmp_file.name)

            return str(self.temp_db_path)

        except ValueError:
            raise
        except Exception as e:
            raise Exception(f"Fehler beim Öffnen der Datenbank: {str(e)}")

    def save_database(self, temp_db_path: str):
        """
        Speichert die temporäre Datenbank zurück in die verschlüsselte Datei

        Args:
            temp_db_path: Pfad zur temporären Datenbank
        """
        if not self.master_password:
            raise ValueError("Master-Passwort nicht gesetzt")

        # Lese temporäre Datenbank
        with open(temp_db_path, 'rb') as f:
            db_data = f.read()

        # Verschlüssele und speichere
        self._encrypt_and_save(db_data, self.master_password)

    def close_database(self):
        """Schließt und löscht die temporäre Datenbank"""
        if self.temp_db_path and self.temp_db_path.exists():
            try:
                os.remove(self.temp_db_path)
                self.temp_db_path = None
            except Exception as e:
                logger.warning(f"Konnte temporäre Datei nicht löschen: {self.temp_db_path} - {e}")

    def change_master_password(self, old_password: str, new_password: str):
        """
        Ändert das Master-Passwort

        Args:
            old_password: Aktuelles Master-Passwort
            new_password: Neues Master-Passwort

        Raises:
            ValueError: Wenn altes Passwort falsch ist
        """
        # Öffne mit altem Passwort
        temp_db = self.open_database(old_password)

        try:
            # Lese Daten
            with open(temp_db, 'rb') as f:
                db_data = f.read()

            # Verschlüssele mit neuem Passwort
            self._encrypt_and_save(db_data, new_password)
            self.master_password = new_password

        finally:
            # Lösche temporäre Datei
            if os.path.exists(temp_db):
                os.remove(temp_db)

    @staticmethod
    def is_valid_database_file(file_path: str) -> bool:
        """
        Prüft ob eine Datei eine gültige Datenbank-Datei ist

        Args:
            file_path: Pfad zur Datei

        Returns:
            True wenn gültig, sonst False
        """
        try:
            with open(file_path, 'rb') as f:
                header = f.read(len(DatabaseFile.FILE_HEADER))
                return header == DatabaseFile.FILE_HEADER
        except Exception:
            return False

    @staticmethod
    def get_default_database_path() -> Path:
        """
        Gibt den Standard-Pfad für neue Datenbanken zurück

        Returns:
            Pfad zum Datenbank-Verzeichnis
        """
        # Verwende Dokumente-Ordner
        if os.name == 'nt':  # Windows
            docs = Path.home() / "Documents" / "SecurePass"
        else:  # Linux/Mac
            docs = Path.home() / "Documents" / "SecurePass"

        docs.mkdir(parents=True, exist_ok=True)
        return docs

    def __del__(self):
        """Destruktor - stellt sicher, dass temporäre Dateien gelöscht werden"""
        self.close_database()
