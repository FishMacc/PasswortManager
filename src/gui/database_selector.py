"""
Datenbank-Auswahl Dialog (ähnlich wie KeePass)

Ermöglicht das Öffnen bestehender oder Erstellen neuer Datenbanken.
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QFileDialog, QMessageBox, QListWidget, QListWidgetItem
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont
from pathlib import Path
from ..core.settings import app_settings
from ..core.database_file import DatabaseFile
from .themes import theme
from .icons import icon_provider
from .animations import animator


class DatabaseSelectorDialog(QDialog):
    """Dialog zur Auswahl oder Erstellung einer Datenbank"""

    database_selected = pyqtSignal(str)  # Pfad zur ausgewählten Datenbank

    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_database_path = None
        self.setup_ui()

        # Fade-in Animation
        QTimer.singleShot(50, lambda: self.animate_in())

    def animate_in(self):
        """Animiert den Dialog beim Öffnen"""
        animator.fade_in(self.header_container, 200)
        QTimer.singleShot(100, lambda: animator.fade_in(self.recent_container, 250))
        QTimer.singleShot(150, lambda: animator.fade_in(self.actions_container, 250))

    def setup_ui(self):
        """Erstellt das UI"""
        self.setWindowTitle("SecurePass Manager - Datenbank auswählen")
        self.setModal(True)
        self.setMinimumSize(650, 550)
        self.resize(650, 550)

        c = theme.get_colors()

        # Haupt-Container
        main_container = QWidget()
        main_layout = QVBoxLayout(main_container)
        main_layout.setSpacing(30)
        main_layout.setContentsMargins(40, 40, 40, 40)

        # === HEADER ===
        self.header_container = QFrame()
        header_layout = QVBoxLayout(self.header_container)
        header_layout.setSpacing(12)
        header_layout.setContentsMargins(0, 0, 0, 0)

        # Icon und Titel
        title_row = QHBoxLayout()
        title_row.setSpacing(15)

        shield_icon = QLabel()
        shield_pixmap = icon_provider.get_pixmap("shield", c['primary'], 48)
        shield_icon.setPixmap(shield_pixmap)
        shield_icon.setFixedSize(48, 48)
        title_row.addWidget(shield_icon)

        title_container = QVBoxLayout()
        title_container.setSpacing(4)

        title = QLabel("Willkommen bei SecurePass")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet(f"color: {c['text_primary']};")
        title_container.addWidget(title)

        subtitle = QLabel("Wähle eine Datenbank oder erstelle eine neue")
        subtitle.setStyleSheet(f"color: {c['text_secondary']}; font-size: 14px;")
        title_container.addWidget(subtitle)

        title_row.addLayout(title_container)
        title_row.addStretch()

        header_layout.addLayout(title_row)
        main_layout.addWidget(self.header_container)

        # === KÜRZLICH VERWENDETE DATENBANKEN ===
        recent_databases = app_settings.get_recent_databases()

        if recent_databases:
            self.recent_container = QFrame()
            self.recent_container.setStyleSheet(f"""
                QFrame {{
                    background-color: {c['surface']};
                    border: 2px solid {c['surface_border']};
                    border-radius: 16px;
                    padding: 20px;
                }}
            """)
            recent_layout = QVBoxLayout(self.recent_container)
            recent_layout.setSpacing(12)
            recent_layout.setContentsMargins(0, 0, 0, 0)

            recent_label = QLabel("Kürzlich verwendet")
            recent_label_font = QFont()
            recent_label_font.setPointSize(13)
            recent_label_font.setBold(True)
            recent_label.setFont(recent_label_font)
            recent_label.setStyleSheet(f"color: {c['text_primary']}; background: transparent; border: none;")
            recent_layout.addWidget(recent_label)

            # Liste der kürzlich verwendeten Datenbanken
            self.recent_list = QListWidget()
            self.recent_list.setMaximumHeight(150)
            self.recent_list.setStyleSheet(f"""
                QListWidget {{
                    background-color: {c['background']};
                    border: 2px solid {c['surface_border']};
                    border-radius: 10px;
                    padding: 8px;
                }}
                QListWidget::item {{
                    padding: 12px;
                    border-radius: 8px;
                    color: {c['text_primary']};
                }}
                QListWidget::item:hover {{
                    background-color: {c['surface_hover']};
                }}
                QListWidget::item:selected {{
                    background-color: {c['primary']};
                    color: white;
                }}
            """)
            self.recent_list.itemDoubleClicked.connect(self.on_recent_database_selected)

            for db_path in recent_databases:
                item = QListWidgetItem(str(Path(db_path).name))
                item.setData(Qt.ItemDataRole.UserRole, db_path)
                self.recent_list.addItem(item)

            recent_layout.addWidget(self.recent_list)
            main_layout.addWidget(self.recent_container)
        else:
            # Platzhalter wenn keine kürzlich verwendeten Datenbanken
            self.recent_container = QFrame()

        # === AKTIONEN ===
        self.actions_container = QFrame()
        actions_layout = QVBoxLayout(self.actions_container)
        actions_layout.setSpacing(12)
        actions_layout.setContentsMargins(0, 0, 0, 0)

        # Neue Datenbank Button
        new_db_button = self._create_action_button(
            "Neue Datenbank erstellen",
            "Erstelle eine neue verschlüsselte Datenbank",
            "plus",
            c['primary']
        )
        new_db_button.clicked.connect(self.create_new_database)
        actions_layout.addWidget(new_db_button)

        # Datenbank öffnen Button
        open_db_button = self._create_action_button(
            "Datenbank öffnen",
            "Öffne eine bestehende Datenbank-Datei (.spdb)",
            "folder_open",
            c['secondary']
        )
        open_db_button.clicked.connect(self.open_existing_database)
        actions_layout.addWidget(open_db_button)

        main_layout.addWidget(self.actions_container)

        main_layout.addStretch()

        # === FOOTER BUTTONS ===
        footer_layout = QHBoxLayout()
        footer_layout.setSpacing(12)

        exit_button = QPushButton("Beenden")
        exit_button.setMinimumHeight(48)
        exit_button.setMinimumWidth(120)
        exit_button.setCursor(Qt.CursorShape.PointingHandCursor)
        exit_button.clicked.connect(self.reject)
        exit_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {c['background_tertiary']};
                color: {c['text_primary']};
                border: 2px solid {c['surface_border']};
                border-radius: 12px;
                font-size: 14px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: {c['surface_hover']};
            }}
        """)
        footer_layout.addWidget(exit_button)

        footer_layout.addStretch()

        main_layout.addLayout(footer_layout)

        # Set main layout
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().addWidget(main_container)

    def _create_action_button(self, title: str, description: str, icon_name: str, accent_color: str) -> QPushButton:
        """Erstellt einen Action-Button"""
        c = theme.get_colors()

        button = QPushButton()
        button.setMinimumHeight(80)
        button.setCursor(Qt.CursorShape.PointingHandCursor)

        # Layout für Button-Inhalt
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        button_layout.setContentsMargins(20, 15, 20, 15)

        # Icon
        icon_label = QLabel()
        icon_pixmap = icon_provider.get_pixmap(icon_name, accent_color, 32)
        icon_label.setPixmap(icon_pixmap)
        icon_label.setFixedSize(32, 32)
        button_layout.addWidget(icon_label)

        # Text Container
        text_container = QVBoxLayout()
        text_container.setSpacing(4)

        title_label = QLabel(title)
        title_font = QFont()
        title_font.setPointSize(13)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet(f"color: {c['text_primary']}; background: transparent; border: none;")
        text_container.addWidget(title_label)

        desc_label = QLabel(description)
        desc_label.setStyleSheet(f"color: {c['text_secondary']}; font-size: 12px; background: transparent; border: none;")
        text_container.addWidget(desc_label)

        button_layout.addLayout(text_container)
        button_layout.addStretch()

        # Erstelle Container-Widget
        container = QWidget()
        container.setLayout(button_layout)

        # Da QPushButton kein Layout direkt unterstützt, verwenden wir Stylesheet
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {c['surface']};
                border: 2px solid {c['surface_border']};
                border-radius: 16px;
                text-align: left;
            }}
            QPushButton:hover {{
                background-color: {c['surface_hover']};
                border-color: {accent_color};
            }}
        """)

        return button

    def on_recent_database_selected(self, item: QListWidgetItem):
        """Callback wenn kürzlich verwendete Datenbank ausgewählt wurde"""
        db_path = item.data(Qt.ItemDataRole.UserRole)
        self.selected_database_path = db_path
        self.database_selected.emit(db_path)
        self.accept()

    def create_new_database(self):
        """Öffnet Dialog zum Erstellen einer neuen Datenbank"""
        from .database_new import NewDatabaseDialog

        dialog = NewDatabaseDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.selected_database_path = dialog.database_path
            self.database_selected.emit(dialog.database_path)
            self.accept()

    def open_existing_database(self):
        """Öffnet Datei-Dialog zum Auswählen einer bestehenden Datenbank"""
        default_path = str(DatabaseFile.get_default_database_path())

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Datenbank öffnen",
            default_path,
            "SecurePass Datenbank (*.spdb);;Alle Dateien (*.*)"
        )

        if file_path:
            # Prüfe ob gültige Datenbank-Datei
            if not DatabaseFile.is_valid_database_file(file_path):
                QMessageBox.warning(
                    self,
                    "Ungültige Datei",
                    "Die ausgewählte Datei ist keine gültige SecurePass-Datenbank."
                )
                return

            self.selected_database_path = file_path
            self.database_selected.emit(file_path)
            self.accept()

    def get_selected_database(self) -> str:
        """Gibt den Pfad zur ausgewählten Datenbank zurück"""
        return self.selected_database_path


from PyQt6.QtWidgets import QWidget
