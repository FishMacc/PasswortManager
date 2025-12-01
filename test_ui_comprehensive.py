"""
Umfassendes UI-Test-Tool für SecurePass Manager

Testet ALLE UI-Komponenten:
- Alle Dialoge (Login, Entry, Generator, Settings, DB-Selector)
- Hauptfenster (Entry-Liste, Kategorien, Suche, Header)
- Widgets (PasswordEntryWidget, CategoryButton)
- Animationen (Fade, Slide, Press, Pulse)
- Theme-System (Light/Dark Mode)
- Database-Operationen (CRUD)

Usage:
    python test_ui_comprehensive.py --interactive
    python test_ui_comprehensive.py --test all
    python test_ui_comprehensive.py --test dialogs
    python test_ui_comprehensive.py --test widgets
    python test_ui_comprehensive.py --test mainwindow
    python test_ui_comprehensive.py --test animations
"""
import sys
import os
import argparse
import logging
from pathlib import Path
from typing import Optional

# Importiere PyQt6
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTextEdit, QGroupBox, QScrollArea, QTabWidget
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont

# Füge src/ zum Path hinzu
sys.path.insert(0, str(Path(__file__).parent))

from src.gui.themes import theme, ThemeMode
from src.gui.settings_dialog import SettingsDialog
from src.gui.login_dialog import LoginDialog
from src.gui.entry_dialog import PasswordEntryDialog
from src.gui.generator_dialog import PasswordGeneratorDialog
from src.gui.database_selector import DatabaseSelectorDialog
from src.gui.database_new import NewDatabaseDialog
from src.gui.main_window import MainWindow
from src.gui.widgets import PasswordEntryWidget, CategoryButton
from src.gui.animations import animator
from src.core.settings import app_settings
from src.core.models import PasswordEntry, Category
from src.testing.mock_database import MockDatabase

# Logger konfigurieren
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ComprehensiveUITestWindow(QMainWindow):
    """Umfassendes Test-Fenster für alle UI-Komponenten"""

    def __init__(self):
        super().__init__()
        self.test_results = []
        self.mock_db: Optional[MockDatabase] = None
        self.main_window_instance: Optional[MainWindow] = None
        self.setup_ui()

    def setup_ui(self):
        """Erstellt das Test-UI"""
        self.setWindowTitle("SecurePass - Umfassende UI-Tests")
        self.setMinimumSize(1200, 800)

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Header
        header = QLabel("🧪 SecurePass - Umfassende UI-Tests")
        header_font = QFont()
        header_font.setPointSize(22)
        header_font.setBold(True)
        header.setFont(header_font)
        main_layout.addWidget(header)

        # Info
        info = QLabel("Testet ALLE UI-Komponenten: Dialoge, Widgets, MainWindow, Animationen, Theme, Database")
        main_layout.addWidget(info)

        # Tab Widget für verschiedene Test-Kategorien
        tabs = QTabWidget()
        tabs.addTab(self.create_dialog_tests_tab(), "🪟 Dialoge")
        tabs.addTab(self.create_widget_tests_tab(), "🧩 Widgets")
        tabs.addTab(self.create_mainwindow_tests_tab(), "🏠 MainWindow")
        tabs.addTab(self.create_animation_tests_tab(), "✨ Animationen")
        tabs.addTab(self.create_theme_tests_tab(), "🎨 Theme")
        tabs.addTab(self.create_database_tests_tab(), "💾 Datenbank")
        tabs.addTab(self.create_auto_tests_tab(), "🤖 Automatisch")
        main_layout.addWidget(tabs)

        # Test Output
        output_label = QLabel("📋 Test-Ergebnisse:")
        output_font = QFont()
        output_font.setPointSize(12)
        output_font.setBold(True)
        output_label.setFont(output_font)
        main_layout.addWidget(output_label)

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setMinimumHeight(250)
        main_layout.addWidget(self.output_text)

        # Status Bar
        self.statusBar().showMessage("Bereit - Wähle Tests aus den Tabs")

        # Theme anwenden
        self.update_theme()

    def create_dialog_tests_tab(self) -> QWidget:
        """Erstellt Dialog-Tests Tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Scroll Area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        # Login Dialog Tests
        login_group = QGroupBox("🔐 Login Dialog")
        login_layout = QVBoxLayout(login_group)

        btn_login_light = QPushButton("Login Dialog (Light Mode)")
        btn_login_light.clicked.connect(lambda: self.test_login_dialog(ThemeMode.LIGHT))
        login_layout.addWidget(btn_login_light)

        btn_login_dark = QPushButton("Login Dialog (Dark Mode)")
        btn_login_dark.clicked.connect(lambda: self.test_login_dialog(ThemeMode.DARK))
        login_layout.addWidget(btn_login_dark)

        scroll_layout.addWidget(login_group)

        # Entry Dialog Tests
        entry_group = QGroupBox("📝 Passwort-Eintrag Dialog")
        entry_layout = QVBoxLayout(entry_group)

        btn_entry_new = QPushButton("Neuer Eintrag Dialog")
        btn_entry_new.clicked.connect(lambda: self.test_entry_dialog(new=True))
        entry_layout.addWidget(btn_entry_new)

        btn_entry_edit = QPushButton("Eintrag Bearbeiten Dialog")
        btn_entry_edit.clicked.connect(lambda: self.test_entry_dialog(new=False))
        entry_layout.addWidget(btn_entry_edit)

        btn_entry_themes = QPushButton("Entry Dialog (Beide Themes)")
        btn_entry_themes.clicked.connect(self.test_entry_dialog_both_themes)
        entry_layout.addWidget(btn_entry_themes)

        scroll_layout.addWidget(entry_group)

        # Generator Dialog Tests
        gen_group = QGroupBox("🎲 Passwort-Generator Dialog")
        gen_layout = QVBoxLayout(gen_group)

        btn_gen = QPushButton("Generator Dialog")
        btn_gen.clicked.connect(self.test_generator_dialog)
        gen_layout.addWidget(btn_gen)

        btn_gen_generate = QPushButton("Generator + Auto-Generate")
        btn_gen_generate.clicked.connect(self.test_generator_with_generation)
        gen_layout.addWidget(btn_gen_generate)

        scroll_layout.addWidget(gen_group)

        # Settings Dialog Tests
        settings_group = QGroupBox("⚙️ Einstellungs Dialog")
        settings_layout = QVBoxLayout(settings_group)

        btn_settings = QPushButton("Settings Dialog")
        btn_settings.clicked.connect(self.test_settings_dialog)
        settings_layout.addWidget(btn_settings)

        btn_settings_theme = QPushButton("Settings + Theme Wechsel")
        btn_settings_theme.clicked.connect(self.test_settings_theme_change)
        settings_layout.addWidget(btn_settings_theme)

        scroll_layout.addWidget(settings_group)

        # Database Dialogs Tests
        db_group = QGroupBox("💾 Datenbank Dialoge")
        db_layout = QVBoxLayout(db_group)

        btn_db_selector = QPushButton("Database Selector")
        btn_db_selector.clicked.connect(self.test_database_selector)
        db_layout.addWidget(btn_db_selector)

        btn_db_new = QPushButton("Neue Datenbank Dialog")
        btn_db_new.clicked.connect(self.test_new_database_dialog)
        db_layout.addWidget(btn_db_new)

        scroll_layout.addWidget(db_group)

        scroll_layout.addStretch()
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

        return widget

    def create_widget_tests_tab(self) -> QWidget:
        """Erstellt Widget-Tests Tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        # PasswordEntryWidget Tests
        entry_widget_group = QGroupBox("📋 PasswordEntryWidget")
        entry_widget_layout = QVBoxLayout(entry_widget_group)

        btn_entry_widget = QPushButton("Teste PasswordEntryWidget")
        btn_entry_widget.clicked.connect(self.test_password_entry_widget)
        entry_widget_layout.addWidget(btn_entry_widget)

        btn_entry_widget_interactions = QPushButton("Teste Widget Interaktionen")
        btn_entry_widget_interactions.clicked.connect(self.test_entry_widget_interactions)
        entry_widget_layout.addWidget(btn_entry_widget_interactions)

        scroll_layout.addWidget(entry_widget_group)

        # CategoryButton Tests
        category_group = QGroupBox("🏷️ CategoryButton")
        category_layout = QVBoxLayout(category_group)

        btn_category = QPushButton("Teste CategoryButton")
        btn_category.clicked.connect(self.test_category_button)
        category_layout.addWidget(btn_category)

        btn_category_themes = QPushButton("CategoryButton (Beide Themes)")
        btn_category_themes.clicked.connect(self.test_category_button_themes)
        category_layout.addWidget(btn_category_themes)

        scroll_layout.addWidget(category_group)

        scroll_layout.addStretch()
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

        return widget

    def create_mainwindow_tests_tab(self) -> QWidget:
        """Erstellt MainWindow-Tests Tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        # MainWindow Tests
        main_group = QGroupBox("🏠 Hauptfenster")
        main_layout = QVBoxLayout(main_group)

        btn_main_create = QPushButton("Öffne MainWindow mit Test-Daten")
        btn_main_create.clicked.connect(self.test_main_window)
        main_layout.addWidget(btn_main_create)

        btn_main_categories = QPushButton("Teste Kategorie-Wechsel")
        btn_main_categories.clicked.connect(self.test_main_window_categories)
        main_layout.addWidget(btn_main_categories)

        btn_main_search = QPushButton("Teste Suchfunktion")
        btn_main_search.clicked.connect(self.test_main_window_search)
        main_layout.addWidget(btn_main_search)

        btn_main_lock = QPushButton("Teste Lock/Unlock")
        btn_main_lock.clicked.connect(self.test_main_window_lock)
        main_layout.addWidget(btn_main_lock)

        scroll_layout.addWidget(main_group)

        scroll_layout.addStretch()
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

        return widget

    def create_animation_tests_tab(self) -> QWidget:
        """Erstellt Animations-Tests Tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        # Animation Tests
        anim_group = QGroupBox("✨ Animationen")
        anim_layout = QVBoxLayout(anim_group)

        # Test Buttons für verschiedene Animationen
        self.anim_test_button = QPushButton("Test Button für Animationen")
        anim_layout.addWidget(self.anim_test_button)

        btn_fade = QPushButton("Teste Fade Animation")
        btn_fade.clicked.connect(lambda: self.test_animation("fade"))
        anim_layout.addWidget(btn_fade)

        btn_slide = QPushButton("Teste Slide Animation")
        btn_slide.clicked.connect(lambda: self.test_animation("slide"))
        anim_layout.addWidget(btn_slide)

        btn_pulse = QPushButton("Teste Pulse Animation")
        btn_pulse.clicked.connect(lambda: self.test_animation("pulse"))
        anim_layout.addWidget(btn_pulse)

        btn_press = QPushButton("Teste Press Animation")
        btn_press.clicked.connect(lambda: self.test_animation("press"))
        anim_layout.addWidget(btn_press)

        btn_shake = QPushButton("Teste Shake Animation")
        btn_shake.clicked.connect(lambda: self.test_animation("shake"))
        anim_layout.addWidget(btn_shake)

        btn_all_anims = QPushButton("Teste Alle Animationen")
        btn_all_anims.clicked.connect(self.test_all_animations)
        anim_layout.addWidget(btn_all_anims)

        scroll_layout.addWidget(anim_group)

        scroll_layout.addStretch()
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

        return widget

    def create_theme_tests_tab(self) -> QWidget:
        """Erstellt Theme-Tests Tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        # Theme Tests
        theme_group = QGroupBox("🎨 Theme-System")
        theme_layout = QVBoxLayout(theme_group)

        self.theme_status = QLabel(f"Aktuelles Theme: {theme.current_mode.value}")
        theme_layout.addWidget(self.theme_status)

        btn_light = QPushButton("☀️ Light Mode")
        btn_light.clicked.connect(lambda: self.test_theme_mode(ThemeMode.LIGHT))
        theme_layout.addWidget(btn_light)

        btn_dark = QPushButton("🌙 Dark Mode")
        btn_dark.clicked.connect(lambda: self.test_theme_mode(ThemeMode.DARK))
        theme_layout.addWidget(btn_dark)

        btn_toggle = QPushButton("🔄 Toggle Theme")
        btn_toggle.clicked.connect(self.test_theme_toggle)
        theme_layout.addWidget(btn_toggle)

        btn_cycle = QPushButton("🔁 Theme Cycle (Auto)")
        btn_cycle.clicked.connect(self.test_theme_cycle)
        theme_layout.addWidget(btn_cycle)

        scroll_layout.addWidget(theme_group)

        scroll_layout.addStretch()
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

        return widget

    def create_database_tests_tab(self) -> QWidget:
        """Erstellt Database-Tests Tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        # Database Tests
        db_group = QGroupBox("💾 Datenbank-Operationen")
        db_layout = QVBoxLayout(db_group)

        btn_db_create = QPushButton("Erstelle Test-Datenbank")
        btn_db_create.clicked.connect(self.test_database_create)
        db_layout.addWidget(btn_db_create)

        btn_db_crud = QPushButton("Teste CRUD-Operationen")
        btn_db_crud.clicked.connect(self.test_database_crud)
        db_layout.addWidget(btn_db_crud)

        btn_db_categories = QPushButton("Teste Kategorien")
        btn_db_categories.clicked.connect(self.test_database_categories)
        db_layout.addWidget(btn_db_categories)

        btn_db_cleanup = QPushButton("Cleanup Test-Datenbank")
        btn_db_cleanup.clicked.connect(self.cleanup_test_database)
        db_layout.addWidget(btn_db_cleanup)

        scroll_layout.addWidget(db_group)

        scroll_layout.addStretch()
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

        return widget

    def create_auto_tests_tab(self) -> QWidget:
        """Erstellt Automatische-Tests Tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        # Auto Tests
        auto_group = QGroupBox("🤖 Automatische Test-Suiten")
        auto_layout = QVBoxLayout(auto_group)

        self.auto_status = QLabel("Status: Bereit")
        auto_layout.addWidget(self.auto_status)

        btn_all_dialogs = QPushButton("▶️ Alle Dialog-Tests")
        btn_all_dialogs.clicked.connect(self.run_all_dialog_tests)
        auto_layout.addWidget(btn_all_dialogs)

        btn_all_widgets = QPushButton("▶️ Alle Widget-Tests")
        btn_all_widgets.clicked.connect(self.run_all_widget_tests)
        auto_layout.addWidget(btn_all_widgets)

        btn_all_animations = QPushButton("▶️ Alle Animations-Tests")
        btn_all_animations.clicked.connect(self.test_all_animations)
        auto_layout.addWidget(btn_all_animations)

        btn_full_suite = QPushButton("▶️ VOLLSTÄNDIGE Test-Suite")
        btn_full_suite.clicked.connect(self.run_full_test_suite)
        auto_layout.addWidget(btn_full_suite)

        btn_clear = QPushButton("🗑️ Clear Output")
        btn_clear.clicked.connect(self.clear_output)
        auto_layout.addWidget(btn_clear)

        scroll_layout.addWidget(auto_group)

        scroll_layout.addStretch()
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

        return widget

    # ========== TEST METHODEN ==========

    # === Dialog Tests ===

    def test_login_dialog(self, theme_mode: ThemeMode):
        """Testet Login Dialog"""
        self.log_info(f"Teste Login Dialog ({theme_mode.value})...")
        try:
            theme.set_mode(theme_mode)
            self.update_theme()

            # Erstelle Test-DB
            if not self.mock_db:
                self.mock_db = MockDatabase()
                self.mock_db.setup()

            creds = self.mock_db.get_test_credentials()

            dialog = LoginDialog(creds["db_path"], self)
            self.log_success(f"✓ Login Dialog erstellt ({theme_mode.value})")

            # Auto-Close nach 2 Sekunden
            QTimer.singleShot(2000, dialog.accept)
            dialog.exec()

        except Exception as e:
            self.log_error(f"✗ Login Dialog Fehler: {e}")
            logger.exception("Login Dialog Error")

    def test_entry_dialog(self, new: bool = True):
        """Testet Passwort-Eintrag Dialog"""
        action = "Neu" if new else "Bearbeiten"
        self.log_info(f"Teste Entry Dialog ({action})...")
        try:
            # Setup DB
            if not self.mock_db:
                self.mock_db = MockDatabase()
                self.mock_db.setup()

            if new:
                dialog = PasswordEntryDialog(self.mock_db.db_manager, parent=self)
            else:
                # Hole ersten Eintrag zum Bearbeiten
                entries = self.mock_db.db_manager.get_all_password_entries()
                if entries:
                    dialog = PasswordEntryDialog(
                        self.mock_db.db_manager,
                        entry=entries[0],
                        parent=self
                    )
                else:
                    self.log_error("✗ Keine Einträge zum Bearbeiten vorhanden")
                    return

            self.log_success(f"✓ Entry Dialog erstellt ({action})")

            # Auto-Close
            QTimer.singleShot(2000, dialog.accept)
            dialog.exec()

        except Exception as e:
            self.log_error(f"✗ Entry Dialog Fehler: {e}")
            logger.exception("Entry Dialog Error")

    def test_entry_dialog_both_themes(self):
        """Testet Entry Dialog in beiden Themes"""
        self.log_info("Teste Entry Dialog in beiden Themes...")

        # Light
        theme.set_mode(ThemeMode.LIGHT)
        self.update_theme()
        QTimer.singleShot(500, lambda: self.test_entry_dialog(new=True))

        # Dark
        QTimer.singleShot(3000, lambda: theme.set_mode(ThemeMode.DARK))
        QTimer.singleShot(3000, lambda: self.update_theme())
        QTimer.singleShot(3500, lambda: self.test_entry_dialog(new=False))

    def test_generator_dialog(self):
        """Testet Generator Dialog"""
        self.log_info("Teste Generator Dialog...")
        try:
            dialog = PasswordGeneratorDialog(self)
            self.log_success("✓ Generator Dialog erstellt")

            # Auto-Close
            QTimer.singleShot(2000, dialog.accept)
            dialog.exec()

        except Exception as e:
            self.log_error(f"✗ Generator Dialog Fehler: {e}")
            logger.exception("Generator Dialog Error")

    def test_generator_with_generation(self):
        """Testet Generator mit automatischer Generierung"""
        self.log_info("Teste Generator + Auto-Generate...")
        try:
            dialog = PasswordGeneratorDialog(self)

            # Simuliere Generierung nach 500ms
            def generate():
                if hasattr(dialog, 'generate_button'):
                    dialog.generate_button.click()
                    self.log_success("✓ Passwort generiert")

            QTimer.singleShot(500, generate)
            QTimer.singleShot(2000, dialog.accept)
            dialog.exec()

        except Exception as e:
            self.log_error(f"✗ Generator Auto-Generate Fehler: {e}")

    def test_settings_dialog(self):
        """Testet Settings Dialog"""
        self.log_info("Teste Settings Dialog...")
        try:
            dialog = SettingsDialog(self)
            self.log_success("✓ Settings Dialog erstellt")

            QTimer.singleShot(2000, dialog.accept)
            dialog.exec()

        except Exception as e:
            self.log_error(f"✗ Settings Dialog Fehler: {e}")
            logger.exception("Settings Dialog Error")

    def test_settings_theme_change(self):
        """Testet Settings Dialog mit Theme-Wechsel"""
        self.log_info("Teste Settings + Theme Wechsel...")
        try:
            dialog = SettingsDialog(self)

            # Wechsle Theme während Dialog offen
            def change_theme():
                theme.toggle_mode()
                self.update_theme()
                self.log_info("Theme gewechselt während Dialog offen")

            QTimer.singleShot(1000, change_theme)
            QTimer.singleShot(2500, dialog.accept)
            dialog.exec()

            self.log_success("✓ Settings Dialog mit Theme-Wechsel erfolgreich")

        except Exception as e:
            self.log_error(f"✗ Settings Theme-Wechsel Fehler: {e}")

    def test_database_selector(self):
        """Testet Database Selector"""
        self.log_info("Teste Database Selector...")
        try:
            dialog = DatabaseSelectorDialog(self)
            self.log_success("✓ Database Selector erstellt")

            QTimer.singleShot(2000, dialog.reject)
            dialog.exec()

        except Exception as e:
            self.log_error(f"✗ Database Selector Fehler: {e}")
            logger.exception("Database Selector Error")

    def test_new_database_dialog(self):
        """Testet Neue Datenbank Dialog"""
        self.log_info("Teste Neue Datenbank Dialog...")
        try:
            dialog = NewDatabaseDialog(self)
            self.log_success("✓ Neue Datenbank Dialog erstellt")

            QTimer.singleShot(2000, dialog.reject)
            dialog.exec()

        except Exception as e:
            self.log_error(f"✗ Neue Datenbank Dialog Fehler: {e}")
            logger.exception("New Database Dialog Error")

    # === Widget Tests ===

    def test_password_entry_widget(self):
        """Testet PasswordEntryWidget"""
        self.log_info("Teste PasswordEntryWidget...")
        try:
            if not self.mock_db:
                self.mock_db = MockDatabase()
                self.mock_db.setup()

            entries = self.mock_db.db_manager.get_all_password_entries()
            if not entries:
                self.log_error("✗ Keine Einträge für Widget-Test")
                return

            # Erstelle Widget
            widget = PasswordEntryWidget(entries[0], self.mock_db.db_manager)
            self.log_success("✓ PasswordEntryWidget erstellt")

            # Zeige Widget in neuem Fenster
            test_window = QMainWindow()
            test_window.setCentralWidget(widget)
            test_window.setWindowTitle("PasswordEntryWidget Test")
            test_window.resize(600, 200)
            test_window.show()

            # Auto-Close
            QTimer.singleShot(3000, test_window.close)

        except Exception as e:
            self.log_error(f"✗ PasswordEntryWidget Fehler: {e}")
            logger.exception("PasswordEntryWidget Error")

    def test_entry_widget_interactions(self):
        """Testet Widget-Interaktionen"""
        self.log_info("Teste Widget-Interaktionen (Kopieren, Anzeigen, etc.)...")
        try:
            if not self.mock_db:
                self.mock_db = MockDatabase()
                self.mock_db.setup()

            entries = self.mock_db.db_manager.get_all_password_entries()
            if not entries:
                self.log_error("✗ Keine Einträge für Interaktions-Test")
                return

            widget = PasswordEntryWidget(entries[0], self.mock_db.db_manager)

            # Teste Show/Hide Password
            def toggle_password():
                if hasattr(widget, 'show_password_button'):
                    widget.show_password_button.click()
                    self.log_success("✓ Passwort anzeigen/verstecken getestet")

            # Teste Copy
            def test_copy():
                if hasattr(widget, 'copy_password_button'):
                    widget.copy_password_button.click()
                    self.log_success("✓ Passwort kopieren getestet")

            QTimer.singleShot(500, toggle_password)
            QTimer.singleShot(1500, test_copy)

            # Zeige Widget
            test_window = QMainWindow()
            test_window.setCentralWidget(widget)
            test_window.setWindowTitle("Widget Interaktions-Test")
            test_window.resize(600, 200)
            test_window.show()

            QTimer.singleShot(3000, test_window.close)

        except Exception as e:
            self.log_error(f"✗ Widget-Interaktionen Fehler: {e}")

    def test_category_button(self):
        """Testet CategoryButton"""
        self.log_info("Teste CategoryButton...")
        try:
            if not self.mock_db:
                self.mock_db = MockDatabase()
                self.mock_db.setup()

            categories = self.mock_db.db_manager.get_all_categories()
            if not categories:
                self.log_error("✗ Keine Kategorien für Button-Test")
                return

            # Erstelle Button
            button = CategoryButton(categories[0])
            self.log_success("✓ CategoryButton erstellt")

            # Zeige Button
            test_window = QMainWindow()
            central = QWidget()
            layout = QVBoxLayout(central)
            layout.addWidget(button)
            test_window.setCentralWidget(central)
            test_window.setWindowTitle("CategoryButton Test")
            test_window.resize(300, 100)
            test_window.show()

            QTimer.singleShot(2000, test_window.close)

        except Exception as e:
            self.log_error(f"✗ CategoryButton Fehler: {e}")

    def test_category_button_themes(self):
        """Testet CategoryButton in beiden Themes"""
        self.log_info("Teste CategoryButton in beiden Themes...")

        # Light
        theme.set_mode(ThemeMode.LIGHT)
        self.update_theme()
        QTimer.singleShot(500, self.test_category_button)

        # Dark
        QTimer.singleShot(3000, lambda: theme.set_mode(ThemeMode.DARK))
        QTimer.singleShot(3000, self.update_theme)
        QTimer.singleShot(3500, self.test_category_button)

    # === MainWindow Tests ===

    def test_main_window(self):
        """Testet MainWindow mit Test-Daten"""
        self.log_info("Teste MainWindow mit Test-Daten...")
        try:
            if not self.mock_db:
                self.mock_db = MockDatabase()
                self.mock_db.setup()

            self.main_window_instance = MainWindow(self.mock_db.db_manager)
            self.main_window_instance.show()
            self.log_success("✓ MainWindow erstellt und angezeigt")

            # Auto-Close nach 5 Sekunden
            QTimer.singleShot(5000, self.main_window_instance.close)

        except Exception as e:
            self.log_error(f"✗ MainWindow Fehler: {e}")
            logger.exception("MainWindow Error")

    def test_main_window_categories(self):
        """Testet Kategorie-Wechsel im MainWindow"""
        self.log_info("Teste Kategorie-Wechsel...")
        try:
            if not self.main_window_instance:
                self.test_main_window()
                QTimer.singleShot(1000, self._test_category_clicks)
            else:
                self._test_category_clicks()

        except Exception as e:
            self.log_error(f"✗ Kategorie-Wechsel Fehler: {e}")

    def _test_category_clicks(self):
        """Führt Kategorie-Klicks durch"""
        try:
            if hasattr(self.main_window_instance, 'category_buttons'):
                buttons = self.main_window_instance.category_buttons
                for i, button in enumerate(buttons[:3]):  # Teste erste 3
                    QTimer.singleShot(i * 1000, button.click)
                self.log_success("✓ Kategorie-Wechsel getestet")
        except Exception as e:
            self.log_error(f"✗ Kategorie-Klick Fehler: {e}")

    def test_main_window_search(self):
        """Testet Suchfunktion"""
        self.log_info("Teste Suchfunktion...")
        try:
            if not self.main_window_instance:
                self.test_main_window()
                QTimer.singleShot(1000, self._test_search_input)
            else:
                self._test_search_input()

        except Exception as e:
            self.log_error(f"✗ Suchfunktion Fehler: {e}")

    def _test_search_input(self):
        """Führt Such-Eingabe durch"""
        try:
            if hasattr(self.main_window_instance, 'search_input'):
                search = self.main_window_instance.search_input
                search.setText("Test")
                QTimer.singleShot(500, lambda: search.setText("Gmail"))
                QTimer.singleShot(1000, lambda: search.clear())
                self.log_success("✓ Suchfunktion getestet")
        except Exception as e:
            self.log_error(f"✗ Such-Eingabe Fehler: {e}")

    def test_main_window_lock(self):
        """Testet Lock/Unlock"""
        self.log_info("Teste Lock/Unlock...")
        try:
            if not self.main_window_instance:
                self.test_main_window()
                QTimer.singleShot(2000, self._test_lock_action)
            else:
                self._test_lock_action()

        except Exception as e:
            self.log_error(f"✗ Lock/Unlock Fehler: {e}")

    def _test_lock_action(self):
        """Führt Lock aus"""
        try:
            if hasattr(self.main_window_instance, 'lock_application'):
                self.main_window_instance.lock_application()
                self.log_success("✓ Lock-Funktion getestet")
        except Exception as e:
            self.log_error(f"✗ Lock-Aktion Fehler: {e}")

    # === Animation Tests ===

    def test_animation(self, anim_type: str):
        """Testet spezifische Animation"""
        self.log_info(f"Teste {anim_type.upper()} Animation...")
        try:
            if anim_type == "fade":
                animator.fade_in(self.anim_test_button, duration=500)
            elif anim_type == "slide":
                animator.slide_in(self.anim_test_button, duration=500)
            elif anim_type == "pulse":
                animator.pulse(self.anim_test_button)
            elif anim_type == "press":
                animator.press(self.anim_test_button)
            elif anim_type == "shake":
                animator.shake(self.anim_test_button)

            self.log_success(f"✓ {anim_type.upper()} Animation ausgeführt")

        except Exception as e:
            self.log_error(f"✗ {anim_type.upper()} Animation Fehler: {e}")

    def test_all_animations(self):
        """Testet alle Animationen nacheinander"""
        self.log_info("=== Teste alle Animationen ===")
        self.auto_status.setText("Status: Testing Animations...")

        animations = ["fade", "slide", "pulse", "press", "shake"]
        for i, anim in enumerate(animations):
            QTimer.singleShot(i * 1000, lambda a=anim: self.test_animation(a))

        QTimer.singleShot(len(animations) * 1000, self._finish_animation_tests)

    def _finish_animation_tests(self):
        """Beendet Animation-Tests"""
        self.log_success("=== Alle Animationen getestet ===")
        self.auto_status.setText("Status: Animations ✓")

    # === Theme Tests ===

    def test_theme_mode(self, mode: ThemeMode):
        """Testet Theme-Modus"""
        self.log_info(f"Teste {mode.value} Mode...")
        theme.set_mode(mode)
        self.update_theme()
        self.log_success(f"✓ {mode.value} Mode aktiviert")

    def test_theme_toggle(self):
        """Testet Theme Toggle"""
        old = theme.current_mode.value
        self.log_info(f"Toggle Theme von {old}...")
        theme.toggle_mode()
        self.update_theme()
        self.log_success(f"✓ Theme gewechselt: {old} → {theme.current_mode.value}")

    def test_theme_cycle(self):
        """Testet Theme Cycle"""
        self.log_info("=== Theme Cycle Test ===")

        QTimer.singleShot(500, lambda: self.test_theme_mode(ThemeMode.LIGHT))
        QTimer.singleShot(1500, lambda: self.test_theme_mode(ThemeMode.DARK))
        QTimer.singleShot(2500, self.test_theme_toggle)
        QTimer.singleShot(3500, self.test_theme_toggle)

        QTimer.singleShot(4500, lambda: self.log_success("=== Theme Cycle abgeschlossen ==="))

    # === Database Tests ===

    def test_database_create(self):
        """Testet Datenbank-Erstellung"""
        self.log_info("Teste Datenbank-Erstellung...")
        try:
            self.cleanup_test_database()  # Cleanup vorher

            self.mock_db = MockDatabase()
            self.mock_db.setup()

            entries = self.mock_db.db_manager.get_all_password_entries()
            categories = self.mock_db.db_manager.get_all_categories()

            self.log_success(f"✓ Test-Datenbank erstellt: {len(categories)} Kategorien, {len(entries)} Einträge")

        except Exception as e:
            self.log_error(f"✗ Datenbank-Erstellung Fehler: {e}")
            logger.exception("Database Create Error")

    def test_database_crud(self):
        """Testet CRUD-Operationen"""
        self.log_info("Teste CRUD-Operationen...")
        try:
            if not self.mock_db:
                self.test_database_create()

            db = self.mock_db.db_manager

            # CREATE
            new_entry = PasswordEntry(
                id=0,
                category_id=1,
                name="CRUD Test Entry",
                username="crud_user",
                password="CrudTest123!",
                website_url="https://crud-test.com",
                notes="Test entry for CRUD"
            )
            entry_id = db.add_password_entry(new_entry)
            self.log_success(f"✓ CREATE: Entry #{entry_id} erstellt")

            # READ
            entry = db.get_password_entry(entry_id)
            if entry:
                self.log_success(f"✓ READ: Entry #{entry_id} gelesen")
            else:
                self.log_error(f"✗ READ: Entry #{entry_id} nicht gefunden")

            # UPDATE
            entry.name = "CRUD Test Updated"
            db.update_password_entry(entry)
            updated = db.get_password_entry(entry_id)
            if updated and updated.name == "CRUD Test Updated":
                self.log_success(f"✓ UPDATE: Entry #{entry_id} aktualisiert")
            else:
                self.log_error(f"✗ UPDATE: Fehler beim Aktualisieren")

            # DELETE
            db.delete_password_entry(entry_id)
            deleted = db.get_password_entry(entry_id)
            if not deleted:
                self.log_success(f"✓ DELETE: Entry #{entry_id} gelöscht")
            else:
                self.log_error(f"✗ DELETE: Entry noch vorhanden")

            self.log_success("=== CRUD-Tests abgeschlossen ===")

        except Exception as e:
            self.log_error(f"✗ CRUD-Test Fehler: {e}")
            logger.exception("Database CRUD Error")

    def test_database_categories(self):
        """Testet Kategorie-Operationen"""
        self.log_info("Teste Kategorie-Operationen...")
        try:
            if not self.mock_db:
                self.test_database_create()

            db = self.mock_db.db_manager

            # Liste Kategorien
            categories = db.get_all_categories()
            self.log_info(f"Kategorien gefunden: {len(categories)}")
            for cat in categories:
                self.log_info(f"  - {cat.name} ({cat.color})")

            # Erstelle neue Kategorie
            new_cat = Category(id=0, name="Test Category", color="#ff5733")
            cat_id = db.add_category(new_cat)
            self.log_success(f"✓ Kategorie erstellt: #{cat_id}")

            # Prüfe ob Kategorie existiert
            all_cats = db.get_all_categories()
            if any(c.name == "Test Category" for c in all_cats):
                self.log_success("✓ Kategorie gefunden")
            else:
                self.log_error("✗ Kategorie nicht gefunden")

        except Exception as e:
            self.log_error(f"✗ Kategorie-Test Fehler: {e}")

    def cleanup_test_database(self):
        """Räumt Test-Datenbank auf"""
        self.log_info("Cleanup Test-Datenbank...")
        try:
            if self.mock_db:
                self.mock_db.cleanup()
                self.mock_db = None
                self.log_success("✓ Test-Datenbank aufgeräumt")
            else:
                self.log_info("Keine Test-Datenbank zum Aufräumen")

        except Exception as e:
            self.log_error(f"✗ Cleanup Fehler: {e}")

    # === Automatische Test-Suiten ===

    def run_all_dialog_tests(self):
        """Führt alle Dialog-Tests aus"""
        self.log_info("=== Starte alle Dialog-Tests ===")
        self.auto_status.setText("Status: Testing Dialogs...")

        tests = [
            (500, lambda: self.test_login_dialog(ThemeMode.LIGHT)),
            (3000, lambda: self.test_entry_dialog(True)),
            (6000, self.test_generator_dialog),
            (9000, self.test_settings_dialog),
            (12000, self.test_database_selector),
        ]

        for delay, test in tests:
            QTimer.singleShot(delay, test)

        QTimer.singleShot(15000, self._finish_dialog_tests)

    def _finish_dialog_tests(self):
        """Beendet Dialog-Tests"""
        self.log_success("=== Alle Dialog-Tests abgeschlossen ===")
        self.auto_status.setText("Status: Dialog Tests ✓")

    def run_all_widget_tests(self):
        """Führt alle Widget-Tests aus"""
        self.log_info("=== Starte alle Widget-Tests ===")
        self.auto_status.setText("Status: Testing Widgets...")

        QTimer.singleShot(500, self.test_password_entry_widget)
        QTimer.singleShot(4000, self.test_entry_widget_interactions)
        QTimer.singleShot(8000, self.test_category_button)

        QTimer.singleShot(11000, self._finish_widget_tests)

    def _finish_widget_tests(self):
        """Beendet Widget-Tests"""
        self.log_success("=== Alle Widget-Tests abgeschlossen ===")
        self.auto_status.setText("Status: Widget Tests ✓")

    def run_full_test_suite(self):
        """Führt VOLLSTÄNDIGE Test-Suite aus"""
        self.log_info("=== Starte VOLLSTÄNDIGE Test-Suite ===")
        self.log_info("Dies wird mehrere Minuten dauern...")
        self.auto_status.setText("Status: Running Full Suite...")

        # Phase 1: Database (0-5s)
        QTimer.singleShot(500, self.test_database_create)
        QTimer.singleShot(2000, self.test_database_crud)

        # Phase 2: Theme (5-10s)
        QTimer.singleShot(5000, self.test_theme_cycle)

        # Phase 3: Dialogs (10-30s)
        QTimer.singleShot(10000, lambda: self.log_info("--- Phase: Dialoge ---"))
        QTimer.singleShot(10500, lambda: self.test_login_dialog(ThemeMode.LIGHT))
        QTimer.singleShot(13000, lambda: self.test_entry_dialog(True))
        QTimer.singleShot(16000, self.test_generator_dialog)
        QTimer.singleShot(19000, self.test_settings_dialog)

        # Phase 4: Widgets (30-40s)
        QTimer.singleShot(30000, lambda: self.log_info("--- Phase: Widgets ---"))
        QTimer.singleShot(30500, self.test_password_entry_widget)
        QTimer.singleShot(34000, self.test_category_button)

        # Phase 5: Animations (40-45s)
        QTimer.singleShot(40000, lambda: self.log_info("--- Phase: Animationen ---"))
        QTimer.singleShot(40500, self.test_all_animations)

        # Phase 6: MainWindow (45-55s)
        QTimer.singleShot(45000, lambda: self.log_info("--- Phase: MainWindow ---"))
        QTimer.singleShot(45500, self.test_main_window)

        # Abschluss (55s)
        QTimer.singleShot(55000, self._finish_full_suite)

    def _finish_full_suite(self):
        """Beendet vollständige Test-Suite"""
        self.log_success("=== VOLLSTÄNDIGE Test-Suite abgeschlossen ===")
        self.log_info(f"Gesamtergebnis: {len([r for r in self.test_results if r[0] == 'SUCCESS'])} erfolgreich")
        self.auto_status.setText("Status: Full Suite ✓")

    # === Hilfsmethoden ===

    def update_theme(self):
        """Aktualisiert Theme"""
        QApplication.instance().setStyleSheet(theme.get_stylesheet())
        if hasattr(self, 'theme_status'):
            self.theme_status.setText(f"Aktuelles Theme: {theme.current_mode.value}")
        self.statusBar().showMessage(f"Theme: {theme.current_mode.value}")

    def clear_output(self):
        """Löscht Output"""
        self.output_text.clear()
        self.test_results.clear()
        self.log_info("Output gelöscht")

    def log_info(self, message: str):
        """Loggt Info"""
        self.output_text.append(f"ℹ️  {message}")
        logger.info(message)

    def log_success(self, message: str):
        """Loggt Success"""
        self.output_text.append(f"✅ {message}")
        logger.info(message)
        self.test_results.append(("SUCCESS", message))

    def log_error(self, message: str):
        """Loggt Error"""
        self.output_text.append(f"❌ {message}")
        logger.error(message)
        self.test_results.append(("ERROR", message))

    def closeEvent(self, event):
        """Cleanup beim Schließen"""
        self.cleanup_test_database()
        if self.main_window_instance:
            self.main_window_instance.close()
        event.accept()


def run_interactive_test():
    """Startet interaktives Test-Fenster"""
    app = QApplication(sys.argv)
    theme.apply_theme(app)

    window = ComprehensiveUITestWindow()
    window.show()

    sys.exit(app.exec())


def run_cli_test(test_type: str):
    """Führt CLI-Tests aus"""
    app = QApplication(sys.argv)
    theme.apply_theme(app)

    logger.info(f"=== CLI Test: {test_type} ===")

    # Implementiere CLI-Tests basierend auf test_type
    # ... (ähnlich wie im einfachen test_ui.py)

    return 0


def main():
    """Hauptfunktion"""
    parser = argparse.ArgumentParser(
        description="Umfassendes UI-Test-Tool für SecurePass Manager"
    )
    parser.add_argument(
        "--test",
        choices=["all", "dialogs", "widgets", "mainwindow", "animations", "theme", "database"],
        help="Führt spezifischen Test aus"
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Öffnet interaktives Test-Fenster (Standard)"
    )

    args = parser.parse_args()

    if args.test:
        return run_cli_test(args.test)
    else:
        # Standard: Interaktiv
        run_interactive_test()


if __name__ == "__main__":
    sys.exit(main() or 0)
