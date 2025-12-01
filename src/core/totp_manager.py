"""
TOTP (Time-based One-Time Password) Manager

Verwaltet 2FA/TOTP-Secrets und generiert 6-stellige Codes
für Authenticator-Apps (Google Authenticator, Authy, etc.)
"""
import pyotp
import base64
from typing import Optional, Tuple
from .encryption import encryption_manager


class TOTPManager:
    """Manager für TOTP/2FA Funktionalität"""

    @staticmethod
    def generate_secret() -> str:
        """
        Generiert ein neues TOTP-Secret (Base32)

        Returns:
            Base32-codiertes Secret (z.B. "JBSWY3DPEHPK3PXP")
        """
        return pyotp.random_base32()

    @staticmethod
    def get_totp_code(secret: str) -> str:
        """
        Generiert aktuellen 6-stelligen TOTP-Code

        Args:
            secret: Base32-codiertes TOTP-Secret

        Returns:
            6-stelliger Code (z.B. "123456")
        """
        totp = pyotp.TOTP(secret)
        return totp.now()

    @staticmethod
    def get_remaining_seconds() -> int:
        """
        Gibt verbleibende Sekunden bis zum nächsten Code zurück

        Returns:
            Sekunden bis Code-Wechsel (0-29)
        """
        import time
        return 30 - (int(time.time()) % 30)

    @staticmethod
    def verify_code(secret: str, code: str) -> bool:
        """
        Verifiziert einen TOTP-Code

        Args:
            secret: Base32-codiertes TOTP-Secret
            code: 6-stelliger Code zum Verifizieren

        Returns:
            True wenn Code gültig ist
        """
        totp = pyotp.TOTP(secret)
        return totp.verify(code, valid_window=1)  # ±30 Sekunden Toleranz

    @staticmethod
    def get_provisioning_uri(secret: str, name: str, issuer: str = "SecurePass") -> str:
        """
        Generiert Provisioning URI für QR-Code

        Args:
            secret: Base32-codiertes TOTP-Secret
            name: Account-Name (z.B. "Google:user@example.com")
            issuer: Issuer-Name (Standard: "SecurePass")

        Returns:
            otpauth:// URI für QR-Code
        """
        totp = pyotp.TOTP(secret)
        return totp.provisioning_uri(name=name, issuer_name=issuer)

    @staticmethod
    def encrypt_secret(secret: str) -> bytes:
        """
        Verschlüsselt TOTP-Secret für Datenbank-Speicherung

        Args:
            secret: Base32-codiertes TOTP-Secret

        Returns:
            Verschlüsselte Secret-Bytes
        """
        return encryption_manager.encrypt(secret)

    @staticmethod
    def decrypt_secret(encrypted_secret: bytes) -> str:
        """
        Entschlüsselt TOTP-Secret aus Datenbank

        Args:
            encrypted_secret: Verschlüsselte Secret-Bytes

        Returns:
            Base32-codiertes TOTP-Secret
        """
        return encryption_manager.decrypt(encrypted_secret)


# Globale Singleton-Instanz
totp_manager = TOTPManager()
