"""
TOTP-Manager für Datenbank-Unlock 2FA

Verwaltet TOTP-Secrets für Zwei-Faktor-Authentifizierung beim Entsperren
der Datenbank (nicht für einzelne Passwort-Einträge).
"""
import logging
import pyotp
import time
from typing import Optional
from .encryption import encryption_manager

logger = logging.getLogger(__name__)


class TOTPManager:
    """Manager für TOTP-basierte Zwei-Faktor-Authentifizierung"""

    def generate_secret(self) -> str:
        """
        Generiert ein neues Base32-kodiertes TOTP-Secret

        Returns:
            Base32-String (z.B. "JBSWY3DPEHPK3PXP")
        """
        return pyotp.random_base32()

    def get_totp_code(self, secret: str) -> str:
        """
        Generiert aktuellen 6-stelligen TOTP-Code

        Args:
            secret: Base32-kodiertes TOTP-Secret

        Returns:
            6-stelliger TOTP-Code (z.B. "123456")
        """
        totp = pyotp.TOTP(secret)
        return totp.now()

    def get_remaining_seconds(self) -> int:
        """
        Gibt verbleibende Sekunden bis zum nächsten Code zurück

        Returns:
            Sekunden (0-30)
        """
        return 30 - (int(time.time()) % 30)

    def verify_code(self, secret: str, code: str) -> bool:
        """
        Verifiziert einen TOTP-Code

        Args:
            secret: Base32-kodiertes TOTP-Secret
            code: 6-stelliger Code vom Benutzer

        Returns:
            True wenn Code gültig, False sonst
        """
        try:
            totp = pyotp.TOTP(secret)
            # valid_window=1 erlaubt ±30 Sekunden Zeittoleranz
            return totp.verify(code, valid_window=1)
        except Exception as e:
            logger.error(f"Fehler bei TOTP-Verifizierung: {e}")
            return False

    def get_provisioning_uri(self, secret: str, name: str, issuer: str = "SecurePass") -> str:
        """
        Generiert provisioning URI für QR-Code

        Args:
            secret: Base32-kodiertes TOTP-Secret
            name: Name der Datenbank (z.B. "MyPasswords.spdb")
            issuer: Name der Anwendung

        Returns:
            URI im Format otpauth://totp/...
        """
        totp = pyotp.TOTP(secret)
        return totp.provisioning_uri(name=name, issuer_name=issuer)

    def encrypt_secret(self, secret: str) -> bytes:
        """
        Verschlüsselt TOTP-Secret für Speicherung in DB

        Args:
            secret: Base32-kodiertes TOTP-Secret (Klartext)

        Returns:
            Verschlüsseltes Secret als bytes
        """
        return encryption_manager.encrypt(secret)

    def decrypt_secret(self, encrypted_secret: bytes) -> str:
        """
        Entschlüsselt TOTP-Secret aus DB

        Args:
            encrypted_secret: Verschlüsseltes Secret (bytes)

        Returns:
            Base32-kodiertes TOTP-Secret (Klartext)
        """
        return encryption_manager.decrypt(encrypted_secret)


# Globale Singleton-Instanz
totp_manager = TOTPManager()
