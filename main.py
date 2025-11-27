"""
SecurePass Manager - Moderner Passwort-Manager mit Dark Mode
Entry Point der Anwendung
"""
import sys
from PyQt6.QtWidgets import QApplication
from src.core.database import DatabaseManager
from src.gui.login_dialog import LoginDialog
from src.gui.main_window import MainWindow
from src.gui.themes import theme


def main():
    """Hauptfunktion - Startet die Anwendung"""
    # Erstelle QApplication
    app = QApplication(sys.argv)
    app.setApplicationName("SecurePass Manager")
    app.setOrganizationName("SecurePass")

    # Wende Theme an
    theme.apply_theme(app)

    # Initialisiere Datenbank
    db_manager = DatabaseManager()

    # Zeige Login-Dialog
    login_dialog = LoginDialog(db_manager)

    if login_dialog.exec() == LoginDialog.DialogCode.Accepted:
        # Login erfolgreich, zeige Hauptfenster
        main_window = MainWindow(db_manager)
        main_window.show()

        # Starte Event-Loop
        sys.exit(app.exec())
    else:
        # Login abgebrochen
        sys.exit(0)


if __name__ == "__main__":
    main()
