"""
Passwort-Stärke-Bewertung
"""
import re
from enum import Enum


class PasswordStrength(Enum):
    """Passwort-Stärke Kategorien"""
    WEAK = "Schwach"
    MEDIUM = "Mittel"
    STRONG = "Stark"


class PasswordStrengthChecker:
    """Bewertet die Stärke von Passwörtern"""

    @staticmethod
    def check_strength(password: str) -> PasswordStrength:
        """
        Bewertet die Stärke eines Passworts

        Args:
            password: Das zu bewertende Passwort

        Returns:
            PasswordStrength Enum-Wert
        """
        if not password:
            return PasswordStrength.WEAK

        score = 0
        length = len(password)

        # Längen-Score
        if length >= 8:
            score += 1
        if length >= 12:
            score += 1
        if length >= 16:
            score += 1

        # Zeichentypen-Score
        if re.search(r'[a-z]', password):  # Kleinbuchstaben
            score += 1
        if re.search(r'[A-Z]', password):  # Großbuchstaben
            score += 1
        if re.search(r'\d', password):     # Zahlen
            score += 1
        if re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password):  # Sonderzeichen
            score += 1

        # Bewertung basierend auf Score
        if score <= 3:
            return PasswordStrength.WEAK
        elif score <= 5:
            return PasswordStrength.MEDIUM
        else:
            return PasswordStrength.STRONG

    @staticmethod
    def get_strength_percentage(password: str) -> int:
        """
        Gibt die Passwort-Stärke als Prozentwert zurück (0-100)

        Args:
            password: Das zu bewertende Passwort

        Returns:
            Stärke als Prozent (0-100)
        """
        if not password:
            return 0

        max_score = 7
        score = 0
        length = len(password)

        # Längen-Score (0-3 Punkte)
        if length >= 8:
            score += 1
        if length >= 12:
            score += 1
        if length >= 16:
            score += 1

        # Zeichentypen-Score (0-4 Punkte)
        if re.search(r'[a-z]', password):
            score += 1
        if re.search(r'[A-Z]', password):
            score += 1
        if re.search(r'\d', password):
            score += 1
        if re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password):
            score += 1

        return int((score / max_score) * 100)


# Globale Instanz
password_strength_checker = PasswordStrengthChecker()
