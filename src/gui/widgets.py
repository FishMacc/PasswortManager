"""
Benutzerdefinierte Widgets für die GUI
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont
from ..core.models import PasswordEntry
from ..core.encryption import encryption_manager
from ..utils.clipboard import clipboard_manager
from .themes import theme


class PasswordEntryWidget(QFrame):
    """Widget zur Anzeige eines Passwort-Eintrags mit modernem Design"""

    # Signals
    edit_clicked = pyqtSignal(PasswordEntry)
    delete_clicked = pyqtSignal(PasswordEntry)

    def __init__(self, entry: PasswordEntry, parent=None):
        super().__init__(parent)
        self.entry = entry
        self.password_visible = False
        self.setup_ui()

    def setup_ui(self):
        """Erstellt das UI des Widgets"""
        c = theme.get_colors()

        self.setFrameStyle(QFrame.Shape.StyledPanel)
        self.setStyleSheet(f"""
            PasswordEntryWidget {{
                background-color: {c['surface']};
                border: 2px solid {c['surface_border']};
                border-radius: 12px;
                padding: 15px;
                margin: 8px 0px;
            }}
            PasswordEntryWidget:hover {{
                background-color: {c['surface_hover']};
                border-color: {c['primary']};
            }}
        """)

        layout = QVBoxLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(5, 5, 5, 5)

        # Erste Zeile: Name und Buttons
        first_row = QHBoxLayout()

        # Name mit Icon
        name_container = QHBoxLayout()
        name_icon = QLabel("🔑")
        name_icon.setStyleSheet("font-size: 16px;")
        name_container.addWidget(name_icon)

        name_label = QLabel(self.entry.name)
        name_font = QFont()
        name_font.setPointSize(12)
        name_font.setBold(True)
        name_label.setFont(name_font)
        name_label.setStyleSheet(f"color: {c['text_primary']};")
        name_container.addWidget(name_label)
        name_container.addStretch()

        first_row.addLayout(name_container)
        first_row.addStretch()

        # Buttons
        self.view_button = QPushButton("👁")
        self.view_button.setFixedSize(35, 35)
        self.view_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.view_button.clicked.connect(self.toggle_password)
        self.view_button.setToolTip("Passwort anzeigen/verstecken")
        self.view_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {c['background_tertiary']};
                border: 1px solid {c['surface_border']};
                border-radius: 8px;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {c['primary']};
                border-color: {c['primary']};
            }}
        """)
        first_row.addWidget(self.view_button)

        self.copy_button = QPushButton("📋")
        self.copy_button.setFixedSize(35, 35)
        self.copy_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.copy_button.clicked.connect(self.copy_password)
        self.copy_button.setToolTip("Passwort kopieren")
        self.copy_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {c['background_tertiary']};
                border: 1px solid {c['surface_border']};
                border-radius: 8px;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {c['secondary']};
                border-color: {c['secondary']};
            }}
        """)
        first_row.addWidget(self.copy_button)

        self.edit_button = QPushButton("✏️")
        self.edit_button.setFixedSize(35, 35)
        self.edit_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.edit_button.clicked.connect(lambda: self.edit_clicked.emit(self.entry))
        self.edit_button.setToolTip("Bearbeiten")
        self.edit_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {c['background_tertiary']};
                border: 1px solid {c['surface_border']};
                border-radius: 8px;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {c['warning']};
                border-color: {c['warning']};
            }}
        """)
        first_row.addWidget(self.edit_button)

        self.delete_button = QPushButton("🗑")
        self.delete_button.setFixedSize(35, 35)
        self.delete_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.delete_button.clicked.connect(lambda: self.delete_clicked.emit(self.entry))
        self.delete_button.setToolTip("Löschen")
        self.delete_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {c['background_tertiary']};
                border: 1px solid {c['surface_border']};
                border-radius: 8px;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {c['danger']};
                border-color: {c['danger']};
            }}
        """)
        first_row.addWidget(self.delete_button)

        layout.addLayout(first_row)

        # Zweite Zeile: Username
        if self.entry.username:
            username_label = QLabel(f"👤 {self.entry.username}")
            username_label.setStyleSheet(f"color: {c['text_secondary']}; font-size: 12px;")
            layout.addWidget(username_label)

        # Dritte Zeile: Passwort (versteckt)
        self.password_label = QLabel("••••••••••••")
        self.password_label.setStyleSheet(f"""
            color: {c['text_tertiary']};
            font-family: 'Courier New', monospace;
            font-size: 13px;
            padding: 5px;
            background-color: {c['background_tertiary']};
            border-radius: 5px;
        """)
        layout.addWidget(self.password_label)

        # Vierte Zeile: Website (falls vorhanden)
        if self.entry.website_url:
            website_label = QLabel(f"🔗 {self.entry.website_url}")
            website_label.setStyleSheet(f"color: {c['primary']}; font-size: 11px;")
            website_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            website_label.setCursor(Qt.CursorShape.IBeamCursor)
            layout.addWidget(website_label)

        self.setLayout(layout)

    def toggle_password(self):
        """Toggle zwischen sichtbarem und verstecktem Passwort"""
        c = theme.get_colors()
        self.password_visible = not self.password_visible

        if self.password_visible:
            try:
                decrypted = encryption_manager.decrypt(self.entry.encrypted_password)
                self.password_label.setText(decrypted)
                self.password_label.setStyleSheet(f"""
                    color: {c['text_primary']};
                    font-family: 'Courier New', monospace;
                    font-size: 13px;
                    font-weight: 600;
                    padding: 5px;
                    background-color: {c['background_tertiary']};
                    border-radius: 5px;
                """)
                self.view_button.setText("🙈")
            except Exception as e:
                self.password_label.setText(f"❌ Fehler: {str(e)}")
        else:
            self.password_label.setText("••••••••••••")
            self.password_label.setStyleSheet(f"""
                color: {c['text_tertiary']};
                font-family: 'Courier New', monospace;
                font-size: 13px;
                padding: 5px;
                background-color: {c['background_tertiary']};
                border-radius: 5px;
            """)
            self.view_button.setText("👁")

    def copy_password(self):
        """Kopiert das Passwort in die Zwischenablage"""
        c = theme.get_colors()
        try:
            decrypted = encryption_manager.decrypt(self.entry.encrypted_password)
            clipboard_manager.copy_to_clipboard(decrypted, auto_clear_seconds=30)

            # Visuelles Feedback
            original_text = self.copy_button.text()
            self.copy_button.setText("✓")
            self.copy_button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {c['secondary']};
                    border: 1px solid {c['secondary']};
                    color: white;
                    border-radius: 8px;
                    font-size: 14px;
                    font-weight: bold;
                }}
            """)

            # Zurücksetzen nach 1 Sekunde
            QTimer.singleShot(1000, lambda: self.reset_copy_button(original_text))

        except Exception as e:
            self.password_label.setText(f"❌ Fehler: {str(e)}")

    def reset_copy_button(self, original_text: str):
        """Setzt den Copy-Button zurück"""
        c = theme.get_colors()
        self.copy_button.setText(original_text)
        self.copy_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {c['background_tertiary']};
                border: 1px solid {c['surface_border']};
                border-radius: 8px;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {c['secondary']};
                border-color: {c['secondary']};
            }}
        """)


class CategoryButton(QPushButton):
    """Button für eine Kategorie in der Sidebar mit modernem Design"""

    def __init__(self, category_id: int, name: str, count: int, color: str = None, parent=None):
        super().__init__(parent)
        self.category_id = category_id
        self.category_name = name
        self.count = count
        self.color = color or "#808080"

        self.setText(f"  {name} ({count})")
        self.setCheckable(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet(self._get_stylesheet())

    def _get_stylesheet(self) -> str:
        """Gibt das Stylesheet für den Button zurück"""
        c = theme.get_colors()
        return f"""
            QPushButton {{
                text-align: left;
                padding: 12px 15px;
                border: none;
                border-left: 4px solid transparent;
                background-color: transparent;
                font-size: 13px;
                border-radius: 0px 8px 8px 0px;
            }}
            QPushButton:hover {{
                background-color: {c['surface_hover']};
            }}
            QPushButton:checked {{
                background-color: {c['surface_hover']};
                border-left: 4px solid {self.color};
                font-weight: 600;
                color: {c['primary']};
            }}
        """

    def update_count(self, count: int):
        """Aktualisiert die Anzahl der Einträge"""
        self.count = count
        self.setText(f"  {self.category_name} ({count})")
