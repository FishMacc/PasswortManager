"""
Master-Passwort-Verwaltung mit Argon2id Hashing
"""
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


class MasterPasswordManager:
    """Verwaltet das Master-Passwort mit Argon2id Hashing"""

    def __init__(self):
        # Argon2id PasswordHasher mit sicheren Standard-Parametern
        self.ph = PasswordHasher(
            time_cost=2,  # Anzahl der Iterationen
            memory_cost=65536,  # 64 MB Speicher
            parallelism=4,  # 4 parallele Threads
            hash_len=32,  # 32 Bytes Hash-Länge
            salt_len=16,  # 16 Bytes Salt-Länge
        )

    def hash_password(self, password: str) -> str:
        """
        Hasht ein Passwort mit Argon2id

        Args:
            password: Das zu hashende Passwort

        Returns:
            Der Argon2-Hash als String
        """
        return self.ph.hash(password)

    def verify_password(self, password: str, hash_value: str) -> bool:
        """
        Überprüft, ob ein Passwort mit dem Hash übereinstimmt

        Args:
            password: Das zu prüfende Passwort
            hash_value: Der gespeicherte Argon2-Hash

        Returns:
            True wenn das Passwort korrekt ist, sonst False
        """
        try:
            self.ph.verify(hash_value, password)
            return True
        except VerifyMismatchError:
            return False

    def check_needs_rehash(self, hash_value: str) -> bool:
        """
        Prüft, ob ein Hash mit neuen Parametern neu erstellt werden sollte

        Args:
            hash_value: Der zu prüfende Hash

        Returns:
            True wenn der Hash neu erstellt werden sollte
        """
        return self.ph.check_needs_rehash(hash_value)


# Globale Instanz
master_password_manager = MasterPasswordManager()
