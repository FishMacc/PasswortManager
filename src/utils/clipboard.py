"""
Clipboard-Management mit Auto-Clear nach 30 Sekunden
"""
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer


class ClipboardManager:
    """Verwaltet das Kopieren von Passwörtern in die Zwischenablage"""

    def __init__(self):
        self.clear_timer = None

    def copy_to_clipboard(self, text: str, auto_clear_seconds: int = 30):
        """
        Kopiert Text in die Zwischenablage und löscht ihn nach einer bestimmten Zeit

        Args:
            text: Der zu kopierende Text
            auto_clear_seconds: Zeit in Sekunden bis zur automatischen Löschung
        """
        clipboard = QApplication.clipboard()
        clipboard.setText(text)

        # Stoppe vorherigen Timer, falls vorhanden
        if self.clear_timer is not None:
            self.clear_timer.stop()

        # Erstelle neuen Timer zum automatischen Löschen
        if auto_clear_seconds > 0:
            self.clear_timer = QTimer()
            self.clear_timer.setSingleShot(True)
            self.clear_timer.timeout.connect(self._clear_clipboard)
            self.clear_timer.start(auto_clear_seconds * 1000)

    def _clear_clipboard(self):
        """Löscht die Zwischenablage"""
        clipboard = QApplication.clipboard()
        clipboard.clear()

    def cancel_auto_clear(self):
        """Bricht das automatische Löschen ab"""
        if self.clear_timer is not None:
            self.clear_timer.stop()
            self.clear_timer = None


# Globale Instanz
clipboard_manager = ClipboardManager()
