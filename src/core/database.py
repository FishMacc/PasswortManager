"""
Datenbank-Verwaltung für den Password Manager
Verwendet SQLite für lokale Speicherung
"""
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List, Optional
from .models import Category, PasswordEntry


class DatabaseManager:
    """Verwaltet alle Datenbankoperationen"""

    def __init__(self, db_path: str = "data/passwords.db"):
        """
        Initialisiert die Datenbankverbindung

        Args:
            db_path: Pfad zur SQLite-Datenbank
        """
        # Stelle sicher, dass das data-Verzeichnis existiert
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)

        self.db_path = db_path
        self.conn: Optional[sqlite3.Connection] = None
        self._connect()
        self._create_tables()
        self._create_default_categories()

    def _connect(self):
        """Stellt Verbindung zur Datenbank her"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row  # Ermöglicht Zugriff über Spaltennamen

    def _create_tables(self):
        """Erstellt die Datenbanktabellen, falls sie noch nicht existieren"""
        cursor = self.conn.cursor()

        # Users-Tabelle
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                master_password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Categories-Tabelle
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                color TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Password-Entries-Tabelle
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS password_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_id INTEGER,
                name TEXT NOT NULL,
                username TEXT,
                encrypted_password BLOB NOT NULL,
                encrypted_notes BLOB,
                website_url TEXT,
                totp_secret BLOB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(category_id) REFERENCES categories(id) ON DELETE SET NULL
            )
        """)

        self.conn.commit()

    def _create_default_categories(self):
        """Erstellt Standard-Kategorien, falls noch keine vorhanden sind"""
        default_categories = [
            ("Allgemein", "#808080"),
            ("Banking", "#4CAF50"),
            ("Social Media", "#2196F3"),
            ("E-Mail", "#FF9800"),
        ]

        cursor = self.conn.cursor()
        for name, color in default_categories:
            try:
                cursor.execute(
                    "INSERT INTO categories (name, color) VALUES (?, ?)",
                    (name, color)
                )
            except sqlite3.IntegrityError:
                # Kategorie existiert bereits
                pass

        self.conn.commit()

    # ==================== USER MANAGEMENT ====================

    def has_master_password(self) -> bool:
        """Prüft, ob bereits ein Master-Passwort gesetzt wurde"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        return count > 0

    def save_master_password_hash(self, password_hash: str):
        """
        Speichert den Hash des Master-Passworts

        Args:
            password_hash: Argon2-Hash des Master-Passworts
        """
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO users (master_password_hash) VALUES (?)",
            (password_hash,)
        )
        self.conn.commit()

    def get_master_password_hash(self) -> Optional[str]:
        """Ruft den gespeicherten Master-Passwort-Hash ab"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT master_password_hash FROM users LIMIT 1")
        row = cursor.fetchone()
        return row[0] if row else None

    # ==================== CATEGORY MANAGEMENT ====================

    def get_all_categories(self) -> List[Category]:
        """Ruft alle Kategorien ab"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM categories ORDER BY name")
        rows = cursor.fetchall()

        categories = []
        for row in rows:
            categories.append(Category(
                id=row["id"],
                name=row["name"],
                color=row["color"],
                created_at=datetime.fromisoformat(row["created_at"]) if row["created_at"] else None
            ))

        return categories

    def add_category(self, name: str, color: str = None) -> int:
        """
        Fügt eine neue Kategorie hinzu

        Args:
            name: Name der Kategorie
            color: Farbe der Kategorie (Hex-Code)

        Returns:
            ID der neuen Kategorie
        """
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO categories (name, color) VALUES (?, ?)",
            (name, color)
        )
        self.conn.commit()
        return cursor.lastrowid

    def update_category(self, category_id: int, name: str, color: str = None):
        """Aktualisiert eine Kategorie"""
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE categories SET name = ?, color = ? WHERE id = ?",
            (name, color, category_id)
        )
        self.conn.commit()

    def delete_category(self, category_id: int):
        """Löscht eine Kategorie"""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM categories WHERE id = ?", (category_id,))
        self.conn.commit()

    def get_category_by_id(self, category_id: int) -> Optional[Category]:
        """Ruft eine Kategorie anhand der ID ab"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM categories WHERE id = ?", (category_id,))
        row = cursor.fetchone()

        if row:
            return Category(
                id=row["id"],
                name=row["name"],
                color=row["color"],
                created_at=datetime.fromisoformat(row["created_at"]) if row["created_at"] else None
            )
        return None

    # ==================== PASSWORD ENTRY MANAGEMENT ====================

    def add_password_entry(self, entry: PasswordEntry) -> int:
        """
        Fügt einen neuen Passwort-Eintrag hinzu

        Args:
            entry: Der Passwort-Eintrag

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
        return cursor.lastrowid

    def update_password_entry(self, entry: PasswordEntry):
        """Aktualisiert einen Passwort-Eintrag"""
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE password_entries
            SET category_id = ?, name = ?, username = ?, encrypted_password = ?,
                encrypted_notes = ?, website_url = ?, totp_secret = ?, updated_at = ?
            WHERE id = ?
        """, (
            entry.category_id,
            entry.name,
            entry.username,
            entry.encrypted_password,
            entry.encrypted_notes,
            entry.website_url,
            entry.totp_secret,
            datetime.now().isoformat(),
            entry.id
        ))
        self.conn.commit()

    def delete_password_entry(self, entry_id: int):
        """Löscht einen Passwort-Eintrag"""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM password_entries WHERE id = ?", (entry_id,))
        self.conn.commit()

    def get_all_password_entries(self) -> List[PasswordEntry]:
        """Ruft alle Passwort-Einträge ab"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM password_entries ORDER BY name")
        rows = cursor.fetchall()

        entries = []
        for row in rows:
            entries.append(self._row_to_password_entry(row))

        return entries

    def get_password_entries_by_category(self, category_id: int) -> List[PasswordEntry]:
        """Ruft alle Passwort-Einträge einer Kategorie ab"""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM password_entries WHERE category_id = ? ORDER BY name",
            (category_id,)
        )
        rows = cursor.fetchall()

        entries = []
        for row in rows:
            entries.append(self._row_to_password_entry(row))

        return entries

    def search_password_entries(self, query: str) -> List[PasswordEntry]:
        """
        Sucht nach Passwort-Einträgen

        Args:
            query: Suchbegriff (wird in Name und Username gesucht)

        Returns:
            Liste der gefundenen Einträge
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM password_entries
            WHERE name LIKE ? OR username LIKE ?
            ORDER BY name
        """, (f"%{query}%", f"%{query}%"))
        rows = cursor.fetchall()

        entries = []
        for row in rows:
            entries.append(self._row_to_password_entry(row))

        return entries

    def _row_to_password_entry(self, row) -> PasswordEntry:
        """Konvertiert eine Datenbankzeile zu einem PasswordEntry-Objekt"""
        return PasswordEntry(
            id=row["id"],
            category_id=row["category_id"],
            name=row["name"],
            username=row["username"],
            encrypted_password=row["encrypted_password"],
            encrypted_notes=row["encrypted_notes"],
            website_url=row["website_url"],
            totp_secret=row["totp_secret"],
            created_at=datetime.fromisoformat(row["created_at"]) if row["created_at"] else None,
            updated_at=datetime.fromisoformat(row["updated_at"]) if row["updated_at"] else None
        )

    def close(self):
        """Schließt die Datenbankverbindung"""
        if self.conn:
            self.conn.close()
