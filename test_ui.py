"""
UI-Test-Tool für SecurePass Manager

Dieses Skript ermöglicht automatisierte Tests der UI:
- Theme-Wechsel (Light/Dark)
- Dialog-Öffnungen
- Button-Funktionalität
- Layout-Rendering

Usage:
    python test_ui.py --test theme
    python test_ui.py --test settings
    python test_ui.py --test all
    python test_ui.py --interactive  # Öffnet Test-Fenster
"""
import sys
import os
import argparse
import logging
from pathlib import Path

# Importiere PyQt6
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTextEdit, QGroupBox, QComboBox
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont

# Füge src/ zum Path hinzu
sys.path.insert(0, str(Path(__file__).parent))

from src.gui.themes import theme, ThemeMode
from src.gui.settings_dialog import SettingsDialog
from src.core.settings import app_settings

# Logger konfigurieren
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class UITestWindow(QMainWindow):
    """Test-Fenster für UI-Tests"""

    def __init__(self):
        super().__init__()
        self.test_results = []
        self.setup_ui()

    def setup_ui(self):
        """Erstellt das Test-UI"""
        self.setWindowTitle("SecurePass Manager - UI Test Tool")
        self.setMinimumSize(900, 700)

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Header
        header = QLabel("🧪 SecurePass UI Test Tool")
        header_font = QFont()
        header_font.setPointSize(20)
        header_font.setBold(True)
        header.setFont(header_font)
        main_layout.addWidget(header)

        # Theme Tests
        theme_group = self.create_theme_test_group()
        main_layout.addWidget(theme_group)

        # Dialog Tests
        dialog_group = self.create_dialog_test_group()
        main_layout.addWidget(dialog_group)

        # Automatische Tests
        auto_group = self.create_auto_test_group()
        main_layout.addWidget(auto_group)

        # Test Output
        output_label = QLabel("📋 Test-Ergebnisse:")
        output_font = QFont()
        output_font.setPointSize(12)
        output_font.setBold(True)
        output_label.setFont(output_font)
        main_layout.addWidget(output_label)

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setMinimumHeight(200)
        main_layout.addWidget(self.output_text)

        # Theme anwenden
        self.update_theme()

    def create_theme_test_group(self) -> QGroupBox:
        """Erstellt Theme-Test-Gruppe"""
        group = QGroupBox("🎨 Theme-Tests")
        layout = QVBoxLayout(group)

        # Info
        info = QLabel("Teste Theme-Wechsel und Farbanwendung")
        layout.addWidget(info)

        # Buttons
        button_layout = QHBoxLayout()

        self.btn_light = QPushButton("☀️ Light Mode")
        self.btn_light.clicked.connect(self.test_light_mode)
        button_layout.addWidget(self.btn_light)

        self.btn_dark = QPushButton("🌙 Dark Mode")
        self.btn_dark.clicked.connect(self.test_dark_mode)
        button_layout.addWidget(self.btn_dark)

        self.btn_toggle = QPushButton("🔄 Toggle Theme")
        self.btn_toggle.clicked.connect(self.test_toggle_theme)
        button_layout.addWidget(self.btn_toggle)

        layout.addLayout(button_layout)

        # Status
        self.theme_status = QLabel("Aktuelles Theme: Light")
        layout.addWidget(self.theme_status)

        return group

    def create_dialog_test_group(self) -> QGroupBox:
        """Erstellt Dialog-Test-Gruppe"""
        group = QGroupBox("🪟 Dialog-Tests")
        layout = QVBoxLayout(group)

        # Info
        info = QLabel("Teste Dialog-Öffnungen und Theme-Updates")
        layout.addWidget(info)

        # Buttons
        button_layout = QHBoxLayout()

        self.btn_settings = QPushButton("⚙️ Einstellungs-Dialog")
        self.btn_settings.clicked.connect(self.test_settings_dialog)
        button_layout.addWidget(self.btn_settings)

        self.btn_settings_dark = QPushButton("⚙️ Settings (Dark Mode)")
        self.btn_settings_dark.clicked.connect(self.test_settings_dialog_dark)
        button_layout.addWidget(self.btn_settings_dark)

        layout.addLayout(button_layout)

        return group

    def create_auto_test_group(self) -> QGroupBox:
        """Erstellt automatische Test-Gruppe"""
        group = QGroupBox("🤖 Automatische Tests")
        layout = QVBoxLayout(group)

        # Info
        info = QLabel("Führe automatisierte UI-Tests aus")
        layout.addWidget(info)

        # Buttons
        button_layout = QHBoxLayout()

        self.btn_auto_theme = QPushButton("▶️ Theme Cycle Test")
        self.btn_auto_theme.clicked.connect(self.run_theme_cycle_test)
        button_layout.addWidget(self.btn_auto_theme)

        self.btn_auto_full = QPushButton("▶️ Full UI Test")
        self.btn_auto_full.clicked.connect(self.run_full_ui_test)
        button_layout.addWidget(self.btn_auto_full)

        self.btn_clear = QPushButton("🗑️ Clear Output")
        self.btn_clear.clicked.connect(self.clear_output)
        button_layout.addWidget(self.btn_clear)

        layout.addLayout(button_layout)

        # Progress
        self.auto_status = QLabel("Status: Bereit")
        layout.addWidget(self.auto_status)

        return group

    def update_theme(self):
        """Aktualisiert das Theme"""
        c = theme.get_colors()

        # Theme Status aktualisieren
        current = "Dark" if theme.current_mode == ThemeMode.DARK else "Light"
        self.theme_status.setText(f"Aktuelles Theme: {current}")

        # App-Theme anwenden
        QApplication.instance().setStyleSheet(theme.get_stylesheet())

        self.log_success(f"Theme auf {current} aktualisiert")

    def test_light_mode(self):
        """Testet Light Mode"""
        self.log_info("Teste Light Mode...")
        theme.set_mode(ThemeMode.LIGHT)
        self.update_theme()

    def test_dark_mode(self):
        """Testet Dark Mode"""
        self.log_info("Teste Dark Mode...")
        theme.set_mode(ThemeMode.DARK)
        self.update_theme()

    def test_toggle_theme(self):
        """Testet Theme-Toggle"""
        old_mode = theme.current_mode
        self.log_info(f"Toggle Theme von {old_mode.value}...")
        theme.toggle_mode()
        self.update_theme()

    def test_settings_dialog(self):
        """Testet Einstellungs-Dialog im aktuellen Theme"""
        self.log_info("Öffne Einstellungs-Dialog...")
        try:
            dialog = SettingsDialog(self)
            self.log_success("✓ Einstellungs-Dialog erfolgreich erstellt")

            # Dialog öffnen
            result = dialog.exec()
            if result:
                self.log_success("✓ Einstellungen gespeichert")
            else:
                self.log_info("Dialog abgebrochen")

        except Exception as e:
            self.log_error(f"✗ Fehler beim Öffnen des Dialogs: {e}")
            logger.exception("Settings Dialog Error")

    def test_settings_dialog_dark(self):
        """Testet Einstellungs-Dialog im Dark Mode"""
        self.log_info("Wechsle zu Dark Mode und öffne Einstellungen...")
        theme.set_mode(ThemeMode.DARK)
        self.update_theme()
        QTimer.singleShot(100, self.test_settings_dialog)

    def run_theme_cycle_test(self):
        """Führt automatischen Theme-Cycle-Test aus"""
        self.log_info("=== Starte Theme Cycle Test ===")
        self.auto_status.setText("Status: Running Theme Cycle...")

        # Test 1: Light Mode
        QTimer.singleShot(500, lambda: self.test_light_mode())

        # Test 2: Dark Mode
        QTimer.singleShot(1500, lambda: self.test_dark_mode())

        # Test 3: Toggle
        QTimer.singleShot(2500, lambda: self.test_toggle_theme())

        # Test 4: Toggle wieder
        QTimer.singleShot(3500, lambda: self.test_toggle_theme())

        # Abschluss
        QTimer.singleShot(4500, lambda: self._finish_theme_cycle())

    def _finish_theme_cycle(self):
        """Beendet Theme Cycle Test"""
        self.log_success("=== Theme Cycle Test abgeschlossen ===")
        self.auto_status.setText("Status: Theme Cycle ✓")

    def run_full_ui_test(self):
        """Führt vollständigen UI-Test aus"""
        self.log_info("=== Starte Full UI Test ===")
        self.auto_status.setText("Status: Running Full Test...")

        # Test 1: Light Mode + Settings
        QTimer.singleShot(500, self._test_light_settings)

        # Test 2: Dark Mode + Settings
        QTimer.singleShot(3000, self._test_dark_settings)

        # Test 3: Toggle Test
        QTimer.singleShot(5500, self._test_toggle_multiple)

        # Abschluss
        QTimer.singleShot(8000, self._finish_full_test)

    def _test_light_settings(self):
        """Test: Light Mode + Settings Dialog"""
        self.log_info("Test 1/3: Light Mode + Settings...")
        theme.set_mode(ThemeMode.LIGHT)
        self.update_theme()
        QTimer.singleShot(500, lambda: self._open_and_close_settings())

    def _test_dark_settings(self):
        """Test: Dark Mode + Settings Dialog"""
        self.log_info("Test 2/3: Dark Mode + Settings...")
        theme.set_mode(ThemeMode.DARK)
        self.update_theme()
        QTimer.singleShot(500, lambda: self._open_and_close_settings())

    def _test_toggle_multiple(self):
        """Test: Multiple Theme Toggles"""
        self.log_info("Test 3/3: Multiple Toggles...")
        theme.toggle_mode()
        self.update_theme()
        QTimer.singleShot(500, lambda: theme.toggle_mode())
        QTimer.singleShot(500, lambda: self.update_theme())

    def _open_and_close_settings(self):
        """Öffnet und schließt Settings automatisch"""
        try:
            dialog = SettingsDialog(self)
            self.log_success("✓ Settings Dialog erstellt")
            # Automatisch nach 1 Sekunde schließen
            QTimer.singleShot(1000, dialog.accept)
            dialog.exec()
        except Exception as e:
            self.log_error(f"✗ Settings Dialog Fehler: {e}")

    def _finish_full_test(self):
        """Beendet Full UI Test"""
        self.log_success("=== Full UI Test abgeschlossen ===")
        self.auto_status.setText("Status: Full Test ✓")

    def clear_output(self):
        """Löscht Test-Output"""
        self.output_text.clear()
        self.test_results.clear()
        self.log_info("Output gelöscht")

    def log_info(self, message: str):
        """Loggt Info-Message"""
        self.output_text.append(f"ℹ️  {message}")
        logger.info(message)

    def log_success(self, message: str):
        """Loggt Success-Message"""
        self.output_text.append(f"✅ {message}")
        logger.info(message)
        self.test_results.append(("SUCCESS", message))

    def log_error(self, message: str):
        """Loggt Error-Message"""
        self.output_text.append(f"❌ {message}")
        logger.error(message)
        self.test_results.append(("ERROR", message))


def run_interactive_test():
    """Startet interaktives Test-Fenster"""
    app = QApplication(sys.argv)

    # Theme initialisieren
    theme.apply_theme(app)

    window = UITestWindow()
    window.show()

    sys.exit(app.exec())


def run_cli_test(test_type: str):
    """Führt CLI-basierte Tests aus"""
    app = QApplication(sys.argv)
    theme.apply_theme(app)

    logger.info(f"=== Starte {test_type} Test ===")

    if test_type == "theme":
        # Theme Test
        logger.info("Test: Light Mode")
        theme.set_mode(ThemeMode.LIGHT)
        logger.info(f"✓ Theme ist {theme.current_mode.value}")

        logger.info("Test: Dark Mode")
        theme.set_mode(ThemeMode.DARK)
        logger.info(f"✓ Theme ist {theme.current_mode.value}")

        logger.info("Test: Toggle")
        theme.toggle_mode()
        logger.info(f"✓ Theme ist {theme.current_mode.value}")

    elif test_type == "settings":
        # Settings Dialog Test
        try:
            window = QMainWindow()
            window.show()

            logger.info("Test: Settings Dialog Light Mode")
            theme.set_mode(ThemeMode.LIGHT)
            dialog = SettingsDialog(window)
            logger.info("✓ Settings Dialog erstellt (Light)")

            logger.info("Test: Settings Dialog Dark Mode")
            theme.set_mode(ThemeMode.DARK)
            dialog2 = SettingsDialog(window)
            logger.info("✓ Settings Dialog erstellt (Dark)")

            logger.info("✓ Settings Dialog Tests erfolgreich")
        except Exception as e:
            logger.error(f"✗ Settings Dialog Fehler: {e}")
            return 1

    elif test_type == "all":
        # Alle Tests
        logger.info("Führe alle Tests aus...")
        result1 = run_cli_test("theme")
        result2 = run_cli_test("settings")
        return result1 + result2

    logger.info(f"=== {test_type} Test abgeschlossen ===")
    return 0


def main():
    """Hauptfunktion"""
    parser = argparse.ArgumentParser(
        description="UI Test Tool für SecurePass Manager"
    )
    parser.add_argument(
        "--test",
        choices=["theme", "settings", "all"],
        help="Führt spezifischen Test aus"
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Öffnet interaktives Test-Fenster"
    )

    args = parser.parse_args()

    if args.interactive:
        run_interactive_test()
    elif args.test:
        return run_cli_test(args.test)
    else:
        # Standard: Interaktiv
        run_interactive_test()


if __name__ == "__main__":
    sys.exit(main() or 0)
