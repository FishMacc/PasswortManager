"""
Dialog zum Erstellen einer neuen Datenbank
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QFileDialog, QMessageBox, QFrame, QWidget
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
from pathlib import Path
from ..core.database_file import DatabaseFile
from ..core.settings import app_settings
from ..auth.master_password import master_password_manager
from .themes import theme
from .icons import icon_provider
from .animations import animator
from .responsive import responsive


class NewDatabaseDialog(QDialog):
    """Dialog zum Erstellen einer neuen verschlüsselten Datenbank"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.database_path = None
        self.setup_ui()

        # Fade-in Animation
        QTimer.singleShot(50, lambda: self.animate_in())

    def animate_in(self):
        """Animiert den Dialog beim Öffnen"""
        if hasattr(self, 'header_container'):
            animator.fade_in(self.header_container, 200)
        if hasattr(self, 'form_container'):
            QTimer.singleShot(100, lambda: animator.fade_in(self.form_container, 250))
        if hasattr(self, 'button_container'):
            QTimer.singleShot(150, lambda: animator.fade_in(self.button_container, 250))

    def setup_ui(self):
        """Erstellt das UI"""
        self.setWindowTitle("Neue Datenbank erstellen")
        self.setModal(True)

        # Responsive Setup
        responsive.setup_dialog(self, base_width=500, base_height=450, min_width=400, min_height=350)
        fonts = responsive.get_font_sizes()
        spacing = responsive.get_spacing()

        c = theme.get_colors()

        # Haupt-Layout direkt auf Dialog
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(spacing['section_spacing'])
        main_layout.setContentsMargins(spacing['margins'], spacing['margins'], spacing['margins'], spacing['margins'])

        # === HEADER ===
        self.header_container = QFrame()
        header_layout = QHBoxLayout(self.header_container)
        header_layout.setSpacing(spacing['element_spacing'])
        header_layout.setContentsMargins(0, 0, 0, 0)

        icon_label = QLabel()
        icon_size = int(spacing['icon_size'] * 0.6)
        icon_pixmap = icon_provider.get_pixmap("plus", c['primary'], icon_size)
        icon_label.setPixmap(icon_pixmap)
        icon_label.setFixedSize(icon_size, icon_size)
        header_layout.addWidget(icon_label)

        title = QLabel("Neue Datenbank erstellen")
        title_font = QFont()
        title_font.setPointSize(fonts['title'])
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet(f"color: {c['text_primary']};")
        header_layout.addWidget(title)
        header_layout.addStretch()

        main_layout.addWidget(self.header_container)

        # === FORMULAR ===
        self.form_container = QFrame()
        self.form_container.setStyleSheet(f"""
            QFrame {{
                background-color: {c['surface']};
                border: 2px solid {c['surface_border']};
                border-radius: 16px;
            }}
        """)
        form_layout = QVBoxLayout(self.form_container)
        form_layout.setSpacing(spacing['element_spacing'] + 4)
        form_layout.setContentsMargins(20, 20, 20, 20)

        label_style = f"color: {c['text_primary']}; font-weight: 600; font-size: {fonts['body']}px; background: transparent; border: none;"
        input_style = f"""
            QLineEdit {{
                background-color: {c['input_background']};
                color: {c['text_primary']};
                border: 2px solid {c['input_border']};
                border-radius: 10px;
                padding: 0 16px;
                min-height: {spacing['button_height'] - 8}px;
                font-size: {fonts['body']}px;
            }}
            QLineEdit:focus {{
                border-color: {c['primary']};
            }}
        """

        # Datenbank-Name
        name_label = QLabel("Datenbank-Name:")
        name_label.setStyleSheet(label_style)
        form_layout.addWidget(name_label)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("z.B. Meine Passwörter")
        self.name_input.setStyleSheet(input_style)
        self.name_input.setText("Meine Passwörter")
        form_layout.addWidget(self.name_input)

        # Speicherort
        location_label = QLabel("Speicherort:")
        location_label.setStyleSheet(label_style)
        form_layout.addWidget(location_label)

        location_layout = QHBoxLayout()
        location_layout.setSpacing(10)

        self.location_input = QLineEdit()
        self.location_input.setReadOnly(True)
        self.location_input.setStyleSheet(input_style)
        default_path = DatabaseFile.get_default_database_path() / "Meine Passwörter.spdb"
        self.location_input.setText(str(default_path))
        location_layout.addWidget(self.location_input)

        browse_button = QPushButton()
        folder_icon = icon_provider.get_icon("folder", c['text_secondary'], 18)
        browse_button.setIcon(folder_icon)
        browse_button.setFixedSize(spacing['button_height'], spacing['button_height'])
        browse_button.setCursor(Qt.CursorShape.PointingHandCursor)
        browse_button.setToolTip("Durchsuchen...")
        browse_button.clicked.connect(self.browse_location)
        browse_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {c['background_tertiary']};
                border: 2px solid {c['surface_border']};
                border-radius: 10px;
            }}
            QPushButton:hover {{
                background-color: {c['primary']};
                border-color: {c['primary']};
            }}
        """)
        location_layout.addWidget(browse_button)

        form_layout.addLayout(location_layout)

        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet(f"background-color: {c['surface_border']}; border: none; max-height: 1px;")
        form_layout.addWidget(separator)

        # Master-Passwort
        password_label = QLabel("Master-Passwort:")
        password_label.setStyleSheet(label_style)
        form_layout.addWidget(password_label)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Mindestens 8 Zeichen")
        self.password_input.setStyleSheet(input_style)
        form_layout.addWidget(self.password_input)

        # Passwort bestätigen
        confirm_label = QLabel("Passwort bestätigen:")
        confirm_label.setStyleSheet(label_style)
        form_layout.addWidget(confirm_label)

        self.confirm_input = QLineEdit()
        self.confirm_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_input.setPlaceholderText("Passwort erneut eingeben")
        self.confirm_input.setStyleSheet(input_style)
        form_layout.addWidget(self.confirm_input)

        # Warnung
        warning = QLabel("⚠️ Das Master-Passwort kann nicht wiederhergestellt werden!")
        warning.setWordWrap(True)
        warning.setStyleSheet(f"""
            color: {c['danger']};
            background-color: {c['background_tertiary']};
            padding: 12px;
            border-radius: 8px;
            font-size: {fonts['small']}px;
        """)
        form_layout.addWidget(warning)

        main_layout.addWidget(self.form_container)

        main_layout.addStretch()

        # === BUTTONS ===
        self.button_container = QFrame()
        button_layout = QHBoxLayout(self.button_container)
        button_layout.setSpacing(12)
        button_layout.setContentsMargins(0, 0, 0, 0)

        cancel_button = QPushButton("Abbrechen")
        cancel_button.setMinimumHeight(spacing['button_height'])
        cancel_button.setMinimumWidth(120)
        cancel_button.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_button.clicked.connect(self.reject)
        cancel_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {c['background_tertiary']};
                color: {c['text_primary']};
                border: 2px solid {c['surface_border']};
                border-radius: 12px;
                font-size: {fonts['button']}px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: {c['surface_hover']};
            }}
        """)
        button_layout.addWidget(cancel_button)

        button_layout.addStretch()

        create_icon = icon_provider.get_icon("check", "white", 18)
        self.create_button = QPushButton(" Erstellen")
        self.create_button.setIcon(create_icon)
        self.create_button.setMinimumHeight(spacing['button_height'])
        self.create_button.setMinimumWidth(140)
        self.create_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.create_button.clicked.connect(self.create_database)
        self.create_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {c['primary']};
                color: white;
                border: none;
                border-radius: 12px;
                font-size: {fonts['button']}px;
                font-weight: 600;
                padding: 0 24px;
            }}
            QPushButton:hover {{
                background-color: {c['primary_hover']};
            }}
        """)
        button_layout.addWidget(self.create_button)

        main_layout.addWidget(self.button_container)

        # Fokus
        QTimer.singleShot(100, lambda: self.name_input.setFocus())
        QTimer.singleShot(110, lambda: self.name_input.selectAll())

    def browse_location(self):
        """Öffnet Datei-Dialog zum Auswählen des Speicherorts"""
        default_path = DatabaseFile.get_default_database_path()
        current_name = self.name_input.text() or "Meine Passwörter"

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Datenbank speichern unter",
            str(default_path / f"{current_name}.spdb"),
            "SecurePass Datenbank (*.spdb)"
        )

        if file_path:
            # Stelle sicher, dass Dateiendung korrekt ist
            if not file_path.endswith('.spdb'):
                file_path += '.spdb'

            self.location_input.setText(file_path)

            # Aktualisiere Name falls geändert
            name = Path(file_path).stem
            self.name_input.setText(name)

    def create_database(self):
        """Erstellt die neue Datenbank"""
        # Validierung
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Fehler", "Bitte gib einen Datenbank-Namen ein.")
            animator.shake(self.name_input, 8, 50, 3)
            return

        location = self.location_input.text().strip()
        if not location:
            QMessageBox.warning(self, "Fehler", "Bitte wähle einen Speicherort.")
            return

        password = self.password_input.text()
        confirm = self.confirm_input.text()

        # Passwort-Validierung
        if len(password) < 8:
            QMessageBox.warning(
                self,
                "Schwaches Passwort",
                "Das Master-Passwort muss mindestens 8 Zeichen lang sein."
            )
            animator.shake(self.password_input, 8, 50, 3)
            return

        if password != confirm:
            QMessageBox.warning(
                self,
                "Fehler",
                "Die Passwörter stimmen nicht überein."
            )
            animator.shake(self.confirm_input, 8, 50, 3)
            return

        # Prüfe ob Datei bereits existiert
        if Path(location).exists():
            reply = QMessageBox.question(
                self,
                "Datei existiert",
                "Eine Datei mit diesem Namen existiert bereits. Überschreiben?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply != QMessageBox.StandardButton.Yes:
                return

        try:
            # Erstelle Datenbank-Datei
            db_file = DatabaseFile(location)
            db_file.create_new(password)

            # Speichere in Einstellungen
            app_settings.set_last_database(location)

            self.database_path = location
            self.accept()

        except Exception as e:
            QMessageBox.critical(
                self,
                "Fehler",
                f"Fehler beim Erstellen der Datenbank:\n{str(e)}"
            )
