"""
Passwort-Generator Modul
Generiert sichere, zufällige Passwörter
"""
import secrets
import string
from typing import Dict


class PasswordGenerator:
    """Generiert sichere Passwörter mit konfigurierbaren Optionen"""

    def __init__(self):
        self.uppercase = string.ascii_uppercase
        self.lowercase = string.ascii_lowercase
        self.digits = string.digits
        self.special = "!@#$%^&*()_+-=[]{}|;:,.<>?"

    def generate(self, length: int = 16, options: Dict[str, bool] = None) -> str:
        """
        Generiert ein zufälliges Passwort

        Args:
            length: Länge des Passworts (8-64 Zeichen)
            options: Dictionary mit Optionen:
                - uppercase: Großbuchstaben verwenden
                - lowercase: Kleinbuchstaben verwenden
                - digits: Zahlen verwenden
                - special: Sonderzeichen verwenden

        Returns:
            Generiertes Passwort als String

        Raises:
            ValueError: Wenn Länge ungültig oder keine Option ausgewählt
        """
        if length < 8 or length > 64:
            raise ValueError("Passwort-Länge muss zwischen 8 und 64 Zeichen liegen")

        # Standard-Optionen, falls nicht angegeben
        if options is None:
            options = {
                "uppercase": True,
                "lowercase": True,
                "digits": True,
                "special": True
            }

        # Baue den Zeichensatz basierend auf den Optionen
        charset = ""
        required_chars = []

        if options.get("uppercase", False):
            charset += self.uppercase
            required_chars.append(secrets.choice(self.uppercase))

        if options.get("lowercase", False):
            charset += self.lowercase
            required_chars.append(secrets.choice(self.lowercase))

        if options.get("digits", False):
            charset += self.digits
            required_chars.append(secrets.choice(self.digits))

        if options.get("special", False):
            charset += self.special
            required_chars.append(secrets.choice(self.special))

        if not charset:
            raise ValueError("Mindestens eine Zeichenoption muss ausgewählt sein")

        # Generiere den Rest des Passworts
        remaining_length = length - len(required_chars)
        password_chars = required_chars + [
            secrets.choice(charset) for _ in range(remaining_length)
        ]

        # Mische die Zeichen zufällig
        secrets.SystemRandom().shuffle(password_chars)

        return "".join(password_chars)


# Globale Instanz
password_generator = PasswordGenerator()
