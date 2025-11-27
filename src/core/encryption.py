"""
Verschlüsselungs-Module für sichere Datenspeicherung
Verwendet AES-256 via cryptography.Fernet
"""
import base64
import hashlib
from cryptography.fernet import Fernet
from typing import Optional


class EncryptionManager:
    """Verwaltet die Verschlüsselung und Entschlüsselung von Daten"""

    def __init__(self):
        self._fernet: Optional[Fernet] = None
        self._master_password: Optional[str] = None

    def set_master_password(self, master_password: str):
        """
        Setzt das Master-Passwort und leitet daraus den Encryption-Key ab

        Args:
            master_password: Das Master-Passwort des Benutzers
        """
        self._master_password = master_password
        # Key-Derivation: Master-Passwort -> SHA256 -> Fernet Key
        key = hashlib.sha256(master_password.encode()).digest()
        # Fernet benötigt Base64-encoded Key
        fernet_key = base64.urlsafe_b64encode(key)
        self._fernet = Fernet(fernet_key)

    def encrypt(self, plaintext: str) -> bytes:
        """
        Verschlüsselt einen String

        Args:
            plaintext: Der zu verschlüsselnde Text

        Returns:
            Verschlüsselter Text als bytes

        Raises:
            RuntimeError: Wenn kein Master-Passwort gesetzt wurde
        """
        if self._fernet is None:
            raise RuntimeError("Kein Master-Passwort gesetzt. Rufe zuerst set_master_password() auf.")

        return self._fernet.encrypt(plaintext.encode())

    def decrypt(self, ciphertext: bytes) -> str:
        """
        Entschlüsselt verschlüsselte Daten

        Args:
            ciphertext: Die verschlüsselten Daten

        Returns:
            Entschlüsselter Text als String

        Raises:
            RuntimeError: Wenn kein Master-Passwort gesetzt wurde
            cryptography.fernet.InvalidToken: Wenn das Passwort falsch ist
        """
        if self._fernet is None:
            raise RuntimeError("Kein Master-Passwort gesetzt. Rufe zuerst set_master_password() auf.")

        return self._fernet.decrypt(ciphertext).decode()

    def clear(self):
        """Löscht den Encryption-Key aus dem Speicher (für Lock-Funktion)"""
        self._fernet = None
        self._master_password = None

    def is_unlocked(self) -> bool:
        """Prüft, ob die Verschlüsselung entsperrt ist"""
        return self._fernet is not None


# Globale Instanz (Singleton-Pattern)
encryption_manager = EncryptionManager()
