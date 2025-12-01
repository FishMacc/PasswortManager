"""
Hauptfenster der Anwendung mit modernem Design und Dark Mode
"""
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QScrollArea, QMessageBox, QSplitter,
    QFrame
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QAction
from typing import List, Optional
from ..core.database import DatabaseManager
from ..core.models import PasswordEntry, Category
from ..core.encryption import encryption_manager
from .widgets import PasswordEntryWidget, CategoryButton
from .entry_dialog import PasswordEntryDialog
from .login_dialog import LoginDialog
from .settings_dialog import SettingsDialog
from .themes import theme, ThemeMode
from .icons import icon_provider
from ..core.settings import app_settings


class MainWindow(QMainWindow):
    """Hauptfenster der Password Manager Anwendung mit modernem Design"""

    def __init__(self, db_manager: DatabaseManager):
        super().__init__()
        self.db_manager = db_manager
        self.current_category_id: Optional[int] = None
        self.all_entries: List[PasswordEntry] = []
        self.displayed_entries: List[PasswordEntry] = []
        self.categories: List[Category] = []
        self.category_buttons: List[CategoryButton] = []

        # Auto-Lock Timer (5 Minuten)
        self.auto_lock_timer = QTimer()
        self.auto_lock_timer.timeout.connect(self.lock_application)
        self.auto_lock_minutes = 5

        self.setup_ui()
        self.load_categories()
        self.load_all_entries()
        self.show_all_entries()

        # Starte Auto-Lock Timer
        self.reset_auto_lock_timer()

    def setup_ui(self):
        """Erstellt das UI des Hauptfensters"""
        self.setWindowTitle("SecurePass Manager")
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(900, 600)

        # Menüleiste
        self.create_menu_bar()

        # Haupt-Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header
        self.header = self.create_header()
        main_layout.addWidget(self.header)

        # Splitter für Sidebar und Content
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.splitter.setHandleWidth(2)

        # Sidebar
        self.sidebar = self.create_sidebar()
        self.splitter.addWidget(self.sidebar)

        # Content Area
        self.content = self.create_content_area()
        self.splitter.addWidget(self.content)

        # Splitter-Verhältnis
        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 4)
        self.splitter.setSizes([250, 950])

        main_layout.addWidget(self.splitter)

        central_widget.setLayout(main_layout)

    def create_menu_bar(self):
        """Erstellt die Menüleiste"""
        menubar = self.menuBar()

        # Datei-Menü
        file_menu = menubar.addMenu("Datei")

        lock_action = QAction("🔒 Sperren", self)
        lock_action.setShortcut("Ctrl+L")
        lock_action.triggered.connect(self.lock_application)
        file_menu.addAction(lock_action)

        file_menu.addSeparator()

        # Einstellungen
        settings_action = QAction("⚙️ Einstellungen", self)
        settings_action.setShortcut("Ctrl+,")
        settings_action.triggered.connect(self.open_settings)
        file_menu.addAction(settings_action)

        file_menu.addSeparator()

        exit_action = QAction("Beenden", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Ansicht-Menü
        view_menu = menubar.addMenu("Ansicht")

        theme_action = QAction("🌓 Dark Mode umschalten", self)
        theme_action.setShortcut("Ctrl+D")
        theme_action.triggered.connect(self.toggle_theme)
        view_menu.addAction(theme_action)

        # Hilfe-Menü
        help_menu = menubar.addMenu("Hilfe")

        about_action = QAction("Über", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def create_header(self) -> QWidget:
        """Erstellt den Header-Bereich"""
        c = theme.get_colors()

        header = QFrame()
        header.setFixedHeight(90)
        header.setStyleSheet(f"""
            QFrame {{
                background-color: {c['surface']};
                border: none;
            }}
        """)

        layout = QHBoxLayout(header)
        layout.setContentsMargins(20, 10, 20, 10)

        # Logo und Titel
        title_container = QHBoxLayout()
        logo = QLabel("🔐")
        logo_font = QFont()
        logo_font.setPointSize(24)
        logo.setFont(logo_font)
        title_container.addWidget(logo)

        title = QLabel("SecurePass")
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet(f"color: {c['primary']};")
        title_container.addWidget(title)
        title_container.addStretch()

        layout.addLayout(title_container)
        layout.addStretch()

        # Suchfeld
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Passwörter durchsuchen...")
        self.search_input.setMinimumWidth(300)
        self.search_input.setMaximumWidth(400)
        self.search_input.setMinimumHeight(40)
        self.search_input.textChanged.connect(self.on_search_changed)
        layout.addWidget(self.search_input)

        layout.addStretch()

        # Lock Button mit Icon und Text
        self.lock_button = QPushButton(" Manager sperren")
        lock_icon = icon_provider.get_icon("lock", c['text_primary'], 20)
        self.lock_button.setIcon(lock_icon)
        self.lock_button.setMinimumHeight(44)
        self.lock_button.setMinimumWidth(160)
        self.lock_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.lock_button.clicked.connect(self.lock_application)
        self.lock_button.setToolTip("Anwendung sperren (Ctrl+L)")
        self.lock_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {c['background_tertiary']};
                color: {c['text_primary']};
                border: 2px solid {c['surface_border']};
                border-radius: 12px;
                padding: 0 16px;
                font-size: 14px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: {c['danger']};
                color: white;
                border-color: {c['danger']};
            }}
        """)
        from .animations import animator
        self.lock_button.pressed.connect(lambda: animator.press(self.lock_button, scale_factor=0.96, duration=120))
        layout.addWidget(self.lock_button)

        return header

    def create_sidebar(self) -> QWidget:
        """Erstellt die Sidebar mit Kategorien"""
        c = theme.get_colors()

        sidebar = QFrame()
        sidebar.setMinimumWidth(200)
        sidebar.setMaximumWidth(300)
        sidebar.setStyleSheet(f"""
            QFrame {{
                background-color: {c['background_secondary']};
                border-right: 2px solid {c['surface_border']};
            }}
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(15, 20, 15, 20)
        layout.setSpacing(15)

        # Kategorien-Label
        categories_label = QLabel("Kategorien")
        categories_font = QFont()
        categories_font.setPointSize(14)
        categories_font.setBold(True)
        categories_label.setFont(categories_font)
        categories_label.setStyleSheet(f"color: {c['text_primary']}; padding-left: 5px;")
        layout.addWidget(categories_label)

        # Kategorie-Buttons Container
        self.categories_container = QVBoxLayout()
        self.categories_container.setSpacing(5)
        layout.addLayout(self.categories_container)

        layout.addStretch()

        # Neue Kategorie Button
        add_category_button = QPushButton("+ Neue Kategorie")
        add_category_button.setMinimumHeight(40)
        add_category_button.setCursor(Qt.CursorShape.PointingHandCursor)
        add_category_button.clicked.connect(self.add_category)
        add_category_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {c['primary']};
                color: white;
                border: none;
                border-radius: 10px;
                font-weight: 600;
                padding: 10px;
            }}
            QPushButton:hover {{
                background-color: {c['primary_hover']};
            }}
        """)
        layout.addWidget(add_category_button)

        sidebar.setLayout(layout)
        return sidebar

    def create_content_area(self) -> QWidget:
        """Erstellt den Content-Bereich"""
        c = theme.get_colors()

        content = QWidget()
        content.setStyleSheet(f"background-color: {c['background']};")

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 25, 30, 25)
        layout.setSpacing(20)

        # Header mit Titel und Neuer-Eintrag-Button
        content_header = QHBoxLayout()

        self.content_title = QLabel("Alle Einträge")
        content_title_font = QFont()
        content_title_font.setPointSize(16)
        content_title_font.setBold(True)
        self.content_title.setFont(content_title_font)
        self.content_title.setStyleSheet(f"color: {c['text_primary']};")
        content_header.addWidget(self.content_title)

        content_header.addStretch()

        add_entry_button = QPushButton("+ Neuer Eintrag")
        add_entry_button.setMinimumHeight(45)
        add_entry_button.setMinimumWidth(150)
        add_entry_button.setCursor(Qt.CursorShape.PointingHandCursor)
        add_entry_button.clicked.connect(self.add_entry)
        add_entry_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {c['secondary']};
                color: white;
                border: none;
                border-radius: 10px;
                font-weight: 600;
                font-size: 14px;
                padding: 10px 20px;
            }}
            QPushButton:hover {{
                background-color: {c['secondary_hover']};
            }}
        """)
        content_header.addWidget(add_entry_button)

        layout.addLayout(content_header)

        # Scroll Area für Einträge
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setStyleSheet(f"background-color: {c['background']};")

        self.entries_container = QWidget()
        self.entries_container.setStyleSheet(f"background-color: {c['background']};")
        self.entries_layout = QVBoxLayout()
        self.entries_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.entries_layout.setSpacing(10)
        self.entries_container.setLayout(self.entries_layout)

        scroll_area.setWidget(self.entries_container)
        layout.addWidget(scroll_area)

        content.setLayout(layout)
        return content

    def toggle_theme(self):
        """Wechselt zwischen Light und Dark Mode"""
        theme.toggle_mode()

        # Wende globales Stylesheet an
        from PyQt6.QtWidgets import QApplication
        QApplication.instance().setStyleSheet(theme.get_stylesheet())

        # Aktualisiere Theme-spezifische Styles
        self.update_theme_styles()

    def update_theme_styles(self):
        """Aktualisiert die Farben aller Komponenten basierend auf dem aktuellen Theme"""
        c = theme.get_colors()

        # Update Header
        self.header.setStyleSheet(f"""
            QFrame {{
                background-color: {c['surface']};
                border-bottom: 2px solid {c['surface_border']};
            }}
        """)

        # Update Title
        title_widgets = self.header.findChildren(QLabel)
        for widget in title_widgets:
            if "SecurePass" in widget.text():
                widget.setStyleSheet(f"color: {c['primary']};")

        # Update lock button style
        lock_icon = icon_provider.get_icon("lock", c['text_primary'], 20)
        self.lock_button.setIcon(lock_icon)
        self.lock_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {c['background_tertiary']};
                color: {c['text_primary']};
                border: 2px solid {c['surface_border']};
                border-radius: 12px;
                padding: 0 16px;
                font-size: 14px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: {c['danger']};
                color: white;
                border-color: {c['danger']};
            }}
        """)

        # Update Sidebar
        self.sidebar.setStyleSheet(f"""
            QFrame {{
                background-color: {c['background_secondary']};
                border-right: 2px solid {c['surface_border']};
            }}
        """)

        # Update sidebar labels
        for widget in self.sidebar.findChildren(QLabel):
            if "Kategorien" in widget.text():
                widget.setStyleSheet(f"color: {c['text_primary']}; padding-left: 5px;")

        # Update "Neue Kategorie" Button
        for widget in self.sidebar.findChildren(QPushButton):
            if "Neue Kategorie" in widget.text():
                widget.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {c['primary']};
                        color: white;
                        border: none;
                        border-radius: 10px;
                        font-weight: 600;
                        padding: 10px;
                    }}
                    QPushButton:hover {{
                        background-color: {c['primary_hover']};
                    }}
                """)

        # Update separator
        for widget in self.sidebar.findChildren(QFrame):
            if widget.frameShape() == QFrame.Shape.HLine:
                widget.setStyleSheet(f"background-color: {c['surface_border']};")

        # Update Content Area
        self.content.setStyleSheet(f"background-color: {c['background']};")
        self.entries_container.setStyleSheet(f"background-color: {c['background']};")

        # Update content title
        self.content_title.setStyleSheet(f"color: {c['text_primary']};")

        # Update "Neuer Eintrag" Button
        for widget in self.content.findChildren(QPushButton):
            if "Neuer Eintrag" in widget.text():
                widget.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {c['secondary']};
                        color: white;
                        border: none;
                        border-radius: 10px;
                        font-weight: 600;
                        font-size: 14px;
                        padding: 10px 20px;
                    }}
                    QPushButton:hover {{
                        background-color: {c['secondary_hover']};
                    }}
                """)

        # Update alle Kategorie-Buttons
        for button in self.category_buttons:
            button.setStyleSheet(button._get_stylesheet())

        # Update alle Entry-Widgets
        self.update_entry_widgets()

    def load_categories(self):
        """Lädt alle Kategorien aus der Datenbank"""
        self.categories = self.db_manager.get_all_categories()

    def update_category_list(self):
        """Aktualisiert die Kategorie-Liste in der Sidebar"""
        # Lösche alte Buttons
        for button in self.category_buttons:
            button.deleteLater()
        self.category_buttons.clear()

        # "Alle"-Button
        all_count = len(self.all_entries)
        all_button = CategoryButton(None, "📁 Alle", all_count, "#6366f1")
        all_button.clicked.connect(lambda: self.show_all_entries())
        self.categories_container.addWidget(all_button)
        self.category_buttons.append(all_button)

        if self.current_category_id is None:
            all_button.setChecked(True)

        # Kategorie-Buttons
        for category in self.categories:
            count = len(self.db_manager.get_password_entries_by_category(category.id))
            button = CategoryButton(category.id, f"📂 {category.name}", count, category.color)
            button.clicked.connect(lambda checked, cat_id=category.id: self.show_category(cat_id))
            self.categories_container.addWidget(button)
            self.category_buttons.append(button)

            if self.current_category_id == category.id:
                button.setChecked(True)

    def load_all_entries(self):
        """Lädt alle Passwort-Einträge aus der Datenbank"""
        self.all_entries = self.db_manager.get_all_password_entries()

    def show_all_entries(self):
        """Zeigt alle Einträge an"""
        self.current_category_id = None
        self.content_title.setText(f"📚 Alle Einträge ({len(self.all_entries)})")
        self.displayed_entries = self.all_entries
        self.update_entry_widgets()
        self.update_category_list()

    def show_category(self, category_id: int):
        """
        Zeigt Einträge einer bestimmten Kategorie an

        Args:
            category_id: ID der anzuzeigenden Kategorie
        """
        self.current_category_id = category_id
        category = next((cat for cat in self.categories if cat.id == category_id), None)

        if category:
            self.displayed_entries = self.db_manager.get_password_entries_by_category(category_id)
            self.content_title.setText(f"📂 {category.name} ({len(self.displayed_entries)})")
            self.update_entry_widgets()
            self.update_category_list()

    def on_search_changed(self, query: str):
        """
        Wird aufgerufen, wenn sich der Suchbegriff ändert

        Args:
            query: Der Suchbegriff
        """
        if not query:
            # Zeige alle Einträge der aktuellen Kategorie
            if self.current_category_id is None:
                self.show_all_entries()
            else:
                self.show_category(self.current_category_id)
        else:
            # Durchsuche Einträge
            self.displayed_entries = self.db_manager.search_password_entries(query)
            self.content_title.setText(f"🔍 Suchergebnisse ({len(self.displayed_entries)})")
            self.update_entry_widgets()

    def update_entry_widgets(self):
        """Aktualisiert die Anzeige der Passwort-Einträge"""
        c = theme.get_colors()

        # Lösche alte Widgets
        while self.entries_layout.count():
            item = self.entries_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Erstelle neue Widgets
        if not self.displayed_entries:
            no_entries_label = QLabel("Keine Einträge vorhanden")
            no_entries_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_entries_label.setStyleSheet(f"""
                color: {c['text_tertiary']};
                padding: 100px;
                font-size: 16px;
            """)
            self.entries_layout.addWidget(no_entries_label)
        else:
            for entry in self.displayed_entries:
                widget = PasswordEntryWidget(entry)
                widget.edit_clicked.connect(self.edit_entry)
                widget.delete_clicked.connect(self.delete_entry)
                self.entries_layout.addWidget(widget)

    def add_entry(self):
        """Öffnet Dialog zum Hinzufügen eines neuen Eintrags"""
        dialog = PasswordEntryDialog(self.categories, parent=self)
        dialog.entry_saved.connect(self.on_entry_saved)
        dialog.exec()

    def edit_entry(self, entry: PasswordEntry):
        """
        Öffnet Dialog zum Bearbeiten eines Eintrags

        Args:
            entry: Der zu bearbeitende Eintrag
        """
        dialog = PasswordEntryDialog(self.categories, entry, parent=self)
        dialog.entry_saved.connect(self.on_entry_saved)
        dialog.exec()

    def on_entry_saved(self, entry: PasswordEntry):
        """
        Wird aufgerufen, wenn ein Eintrag gespeichert wurde

        Args:
            entry: Der gespeicherte Eintrag
        """
        if entry.id is None:
            # Neuer Eintrag
            entry.id = self.db_manager.add_password_entry(entry)
        else:
            # Bestehender Eintrag aktualisieren
            self.db_manager.update_password_entry(entry)

        # Aktualisiere Ansicht
        self.load_all_entries()
        if self.current_category_id is None:
            self.show_all_entries()
        else:
            self.show_category(self.current_category_id)

    def delete_entry(self, entry: PasswordEntry):
        """
        Löscht einen Eintrag nach Bestätigung

        Args:
            entry: Der zu löschende Eintrag
        """
        reply = QMessageBox.question(
            self,
            "Eintrag löschen",
            f"Möchtest du '{entry.name}' wirklich löschen?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.db_manager.delete_password_entry(entry.id)

            # Aktualisiere Ansicht
            self.load_all_entries()
            if self.current_category_id is None:
                self.show_all_entries()
            else:
                self.show_category(self.current_category_id)

    def add_category(self):
        """Öffnet Dialog zum Hinzufügen einer neuen Kategorie"""
        from PyQt6.QtWidgets import QInputDialog

        name, ok = QInputDialog.getText(self, "Neue Kategorie", "Kategorie-Name:")

        if ok and name:
            try:
                self.db_manager.add_category(name)
                self.load_categories()
                self.update_category_list()
            except Exception as e:
                QMessageBox.warning(self, "Fehler", f"Fehler beim Erstellen der Kategorie: {str(e)}")

    def lock_application(self):
        """Sperrt die Anwendung"""
        # Lösche Encryption-Key
        encryption_manager.clear()

        # Stoppe Auto-Lock Timer
        self.auto_lock_timer.stop()

        # Zeige Login-Dialog
        self.hide()
        login_dialog = LoginDialog(self.db_manager)
        login_dialog.login_successful.connect(self.on_unlock)

        if login_dialog.exec() != LoginDialog.DialogCode.Accepted:
            # Benutzer hat abgebrochen, beende Anwendung
            self.close()

    def on_unlock(self):
        """Wird aufgerufen, wenn die Anwendung entsperrt wurde"""
        self.show()
        self.reset_auto_lock_timer()

    def reset_auto_lock_timer(self):
        """Setzt den Auto-Lock Timer zurück"""
        self.auto_lock_timer.start(self.auto_lock_minutes * 60 * 1000)

    def show_about(self):
        """Zeigt den Über-Dialog"""
        QMessageBox.about(
            self,
            "Über SecurePass Manager",
            "SecurePass Manager v1.0\n\n"
            "Ein moderner, sicherer Passwort-Manager mit:\n"
            "• AES-256 Verschlüsselung\n"
            "• Argon2 Master-Passwort Hashing\n"
            "• Dark Mode Support\n"
            "• Auto-Lock nach 5 Minuten\n"
            "• Passwort-Generator\n"
            "• Kategorien-System\n\n"
            "Erstellt mit Python und PyQt6"
        )

    def open_settings(self):
        """Öffnet den Einstellungs-Dialog"""
        dialog = SettingsDialog(self)
        dialog.settings_changed.connect(self.on_settings_changed)
        dialog.exec()

    def on_settings_changed(self):
        """Wird aufgerufen, wenn Einstellungen geändert wurden"""
        # Auto-Lock Timer aktualisieren
        self.auto_lock_minutes = app_settings.get("auto_lock_minutes", 5)
        self.reset_auto_lock_timer()

        # Theme aktualisieren
        theme_mode = app_settings.get("theme_mode", "light")
        if theme_mode == "dark":
            theme.set_mode(ThemeMode.DARK)
        elif theme_mode == "light":
            theme.set_mode(ThemeMode.LIGHT)
        # System-Theme würde hier implementiert werden

        # UI neu rendern
        theme.apply_theme(self.parentWidget() if self.parent() else self)

    # Event-Handler für Auto-Lock
    def mousePressEvent(self, event):
        """Reset Auto-Lock Timer bei Maus-Aktivität"""
        self.reset_auto_lock_timer()
        super().mousePressEvent(event)

    def keyPressEvent(self, event):
        """Reset Auto-Lock Timer bei Tastatur-Aktivität"""
        self.reset_auto_lock_timer()
        super().keyPressEvent(event)
