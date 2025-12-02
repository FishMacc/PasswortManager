"""
Datenmodelle für den Password Manager
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Category:
    """Kategorie für Passwort-Einträge"""
    id: Optional[int]
    name: str
    color: Optional[str] = None
    created_at: Optional[datetime] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class PasswordEntry:
    """Passwort-Eintrag mit allen relevanten Informationen"""
    id: Optional[int]
    category_id: Optional[int]
    name: str
    username: str
    encrypted_password: bytes
    encrypted_notes: Optional[bytes] = None
    website_url: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    # Nicht-verschlüsselte Versionen (nur zur Laufzeit)
    decrypted_password: Optional[str] = None
    decrypted_notes: Optional[str] = None

    def __post_init__(self):
        now = datetime.now()
        if self.created_at is None:
            self.created_at = now
        if self.updated_at is None:
            self.updated_at = now
