"""
Datenbank-Manager für verschlüsselte Datenbank-Dateien

Arbeitet mit DatabaseFile zusammen, um verschlüsselte .spdb Dateien zu verwalten.
"""
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List, Optional
from .models import Category, PasswordEntry
from .database_file import DatabaseFile


class DatabaseManager:
    """Verwaltet alle Datenbankoperationen mit verschlüsselten Dateien"""

    def __init__(self, encrypted_db_path: str, master_password: str):
        """
        Initialisiert die Datenbankverbindung

        Args:
            encrypted_db_path: Pfad zur verschlüsselten .spdb Datei
            master_password: Master-Passwort zum Entschlüsseln
        """
        self.encrypted_db_path = encrypted_db_path
        self.master_password = master_password
        self.db_file = DatabaseFile(encrypted_db_path, master_password)
        self.temp_db_path: Optional[str] = None
        self.conn: Optional[sqlite3.Connection] = None

        # Öffne verschlüsselte Datenbank
        self._open_encrypted_database()

    def _open_encrypted_database(self):
        """Öffnet und entschlüsselt die Datenbank"""
        try:
            # Entschlüssele Datenbank zu temporärer Datei
            self.temp_db_path = self.db_file.open_database(self.master_password)

            # Verbinde mit temporärer Datenbank
            self.conn = sqlite3.connect(self.temp_db_path)
            self.conn.row_factory = sqlite3.Row

        except ValueError as e:
            raise ValueError(f"Fehler beim Öffnen der Datenbank: {str(e)}")
        except Exception as e:
            raise Exception(f"Unerwarteter Fehler: {str(e)}")

    def save_changes(self):
        """Speichert Änderungen zurück in die verschlüsselte Datei"""
        if self.conn:
            self.conn.commit()

        if self.temp_db_path:
            try:
                self.db_file.save_database(self.temp_db_path)
            except Exception as e:
                raise Exception(f"Fehler beim Speichern: {str(e)}")

    def close(self):
        """Schließt die Datenbank und löscht temporäre Dateien"""
        if self.conn:
            self.conn.close()
            self.conn = None

        if self.db_file:
            self.db_file.close_database()

    # ==================== USER MANAGEMENT ====================

    def has_master_password(self) -> bool:
        """Prüft ob ein Master-Passwort existiert"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        return count > 0

    def get_master_password_hash(self) -> Optional[str]:
        """Gibt den Master-Passwort-Hash zurück"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT password_hash FROM users LIMIT 1")
        result = cursor.fetchone()
        return result['password_hash'] if result else None

    def save_master_password_hash(self, password_hash: str):
        """Speichert den Master-Passwort-Hash"""
        cursor = self.conn.cursor()

        # Lösche alte Hashes
        cursor.execute("DELETE FROM users")

        # Füge neuen Hash ein
        cursor.execute(
            "INSERT INTO users (password_hash) VALUES (?)",
            (password_hash,)
        )

        self.conn.commit()
        # Speichere auch in verschlüsselte Datei
        self.save_changes()

    # ==================== CATEGORY MANAGEMENT ====================

    def get_all_categories(self) -> List[Category]:
        """Gibt alle Kategorien zurück"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM categories ORDER BY name")

        categories = []
        for row in cursor.fetchall():
            category = Category(
                id=row['id'],
                name=row['name'],
                color=row['color'] or '#808080'
            )
            categories.append(category)

        return categories

    def get_category_by_id(self, category_id: int) -> Optional[Category]:
        """Gibt eine Kategorie anhand der ID zurück"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM categories WHERE id = ?", (category_id,))
        row = cursor.fetchone()

        if row:
            return Category(
                id=row['id'],
                name=row['name'],
                color=row['color'] or '#808080'
            )
        return None

    def add_category(self, name: str, color: str = "#808080") -> int:
        """
        Fügt eine neue Kategorie hinzu

        Args:
            name: Name der Kategorie
            color: Farbe der Kategorie (Hex-Format)

        Returns:
            ID der neuen Kategorie

        Raises:
            sqlite3.IntegrityError: Wenn Kategorie bereits existiert
        """
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO categories (name, color) VALUES (?, ?)",
            (name, color)
        )
        self.conn.commit()
        self.save_changes()
        return cursor.lastrowid

    def update_category(self, category_id: int, name: str, color: str):
        """Aktualisiert eine Kategorie"""
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE categories SET name = ?, color = ? WHERE id = ?",
            (name, color, category_id)
        )
        self.conn.commit()
        self.save_changes()

    def delete_category(self, category_id: int):
        """
        Löscht eine Kategorie

        Hinweis: Password-Entries werden auf NULL gesetzt (ON DELETE SET NULL)
        """
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM categories WHERE id = ?", (category_id,))
        self.conn.commit()
        self.save_changes()

    # ==================== PASSWORD ENTRY MANAGEMENT ====================

    def get_all_password_entries(self) -> List[PasswordEntry]:
        """Gibt alle Passwort-Einträge zurück"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM password_entries
            ORDER BY updated_at DESC
        """)

        entries = []
        for row in cursor.fetchall():
            entry = self._row_to_password_entry(row)
            entries.append(entry)

        return entries

    def get_password_entries_by_category(self, category_id: int) -> List[PasswordEntry]:
        """Gibt alle Einträge einer Kategorie zurück"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM password_entries
            WHERE category_id = ?
            ORDER BY updated_at DESC
        """, (category_id,))

        entries = []
        for row in cursor.fetchall():
            entry = self._row_to_password_entry(row)
            entries.append(entry)

        return entries

    def search_password_entries(self, query: str) -> List[PasswordEntry]:
        """
        Sucht nach Passwort-Einträgen

        Args:
            query: Suchbegriff

        Returns:
            Liste der gefundenen Einträge
        """
        cursor = self.conn.cursor()
        search_pattern = f"%{query}%"

        cursor.execute("""
            SELECT * FROM password_entries
            WHERE name LIKE ? OR username LIKE ? OR website_url LIKE ?
            ORDER BY updated_at DESC
        """, (search_pattern, search_pattern, search_pattern))

        entries = []
        for row in cursor.fetchall():
            entry = self._row_to_password_entry(row)
            entries.append(entry)

        return entries

    def get_password_entry_by_id(self, entry_id: int) -> Optional[PasswordEntry]:
        """Gibt einen Passwort-Eintrag anhand der ID zurück"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM password_entries WHERE id = ?", (entry_id,))
        row = cursor.fetchone()

        if row:
            return self._row_to_password_entry(row)
        return None

    def add_password_entry(self, entry: PasswordEntry) -> int:
        """
        Fügt einen neuen Passwort-Eintrag hinzu

        Args:
            entry: Der zu speichernde Eintrag

        Returns:
            ID des neuen Eintrags
        """
        cursor = self.conn.cursor()

        cursor.execute("""
            INSERT INTO password_entries
            (category_id, name, username, encrypted_password, encrypted_notes, website_url, totp_secret)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            entry.category_id,
            entry.name,
            entry.username,
            entry.encrypted_password,
            entry.encrypted_notes,
            entry.website_url,
            entry.totp_secret
        ))

        self.conn.commit()
        self.save_changes()
        return cursor.lastrowid

    def update_password_entry(self, entry: PasswordEntry):
        """Aktualisiert einen bestehenden Passwort-Eintrag"""
        cursor = self.conn.cursor()

        cursor.execute("""
            UPDATE password_entries
            SET category_id = ?, name = ?, username = ?,
                encrypted_password = ?, encrypted_notes = ?, website_url = ?,
                totp_secret = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (
            entry.category_id,
            entry.name,
            entry.username,
            entry.encrypted_password,
            entry.encrypted_notes,
            entry.website_url,
            entry.totp_secret,
            entry.id
        ))

        self.conn.commit()
        self.save_changes()

    def delete_password_entry(self, entry_id: int):
        """Löscht einen Passwort-Eintrag"""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM password_entries WHERE id = ?", (entry_id,))
        self.conn.commit()
        self.save_changes()

    def _row_to_password_entry(self, row: sqlite3.Row) -> PasswordEntry:
        """Konvertiert eine Datenbank-Zeile zu einem PasswordEntry-Objekt"""
        return PasswordEntry(
            id=row['id'],
            category_id=row['category_id'],
            name=row['name'],
            username=row['username'],
            encrypted_password=row['encrypted_password'],
            encrypted_notes=row['encrypted_notes'],
            website_url=row['website_url'],
            totp_secret=row['totp_secret'],
            created_at=row['created_at'],
            updated_at=row['updated_at']
        )

    def __del__(self):
        """Destruktor - stellt sicher, dass die Datenbank geschlossen wird"""
        try:
            self.close()
        except Exception:
            pass
