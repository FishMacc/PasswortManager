"""
SecurePass Manager - Moderner Passwort-Manager mit verschlüsselten Datenbanken
Entry Point der Anwendung
"""
import sys
import logging
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from src.core.database import DatabaseManager
from src.core.settings import app_settings
from src.gui.database_selector import DatabaseSelectorDialog
from src.gui.login_dialog import LoginDialog
from src.gui.main_window import MainWindow
from src.gui.themes import theme


def setup_logging():
    """Konfiguriert das Logging-System"""
    # Log-Verzeichnis erstellen
    log_dir = Path.home() / ".securepass" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    log_file = log_dir / "securepass.log"

    # Logging-Konfiguration
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()  # Zusätzlich in Konsole
        ]
    )

    # Setze Log-Level für externe Libraries höher
    logging.getLogger('PyQt6').setLevel(logging.WARNING)

    logger = logging.getLogger(__name__)
    logger.info("SecurePass Manager gestartet")

    return logger


def main():
    """Hauptfunktion - Startet die Anwendung"""
    # Logging initialisieren
    logger = setup_logging()

    # Erstelle QApplication
    app = QApplication(sys.argv)
    app.setApplicationName("SecurePass Manager")
    app.setOrganizationName("SecurePass")

    # Wende Theme an
    theme.apply_theme(app)

    # === SCHRITT 1: Datenbank auswählen ===
    selector_dialog = DatabaseSelectorDialog()

    if selector_dialog.exec() != DatabaseSelectorDialog.DialogCode.Accepted:
        # Benutzer hat abgebrochen
        sys.exit(0)

    database_path = selector_dialog.get_selected_database()

    if not database_path:
        sys.exit(0)

    # === SCHRITT 2: Login mit Master-Passwort ===
    login_dialog = LoginDialog(database_path)

    if login_dialog.exec() != LoginDialog.DialogCode.Accepted:
        # Login abgebrochen
        sys.exit(0)

    master_password = login_dialog.get_master_password()

    if not master_password:
        sys.exit(0)

    # === SCHRITT 3: Öffne Datenbank ===
    try:
        db_manager = DatabaseManager(database_path, master_password)

        # Speichere als letzte verwendete Datenbank
        app_settings.set_last_database(database_path)

        # === SCHRITT 4: Zeige Hauptfenster ===
        main_window = MainWindow(db_manager)
        main_window.show()

        # Starte Event-Loop
        exit_code = app.exec()

        # Schließe Datenbank beim Beenden
        db_manager.close()

        sys.exit(exit_code)

    except Exception as e:
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.critical(
            None,
            "Fehler",
            f"Fehler beim Öffnen der Datenbank:\n{str(e)}"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
