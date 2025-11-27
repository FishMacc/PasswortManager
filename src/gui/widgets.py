"""
Benutzerdefinierte Widgets mit modernem Design und Animationen
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont
from ..core.models import PasswordEntry
from ..core.encryption import encryption_manager
from ..utils.clipboard import clipboard_manager
from .themes import theme
from .animations import animator
from .icons import icon_provider


class PasswordEntryWidget(QFrame):
    """Modernes Widget zur Anzeige eines Passwort-Eintrags mit Apple-Design"""

    edit_clicked = pyqtSignal(PasswordEntry)
    delete_clicked = pyqtSignal(PasswordEntry)

    def __init__(self, entry: PasswordEntry, parent=None):
        super().__init__(parent)
        self.entry = entry
        self.password_visible = False
        self.setup_ui()

        # Fade-in Animation beim Erstellen
        QTimer.singleShot(10, lambda: animator.fade_in(self, 200))

    def setup_ui(self):
        """Erstellt das moderne, responsive UI des Widgets"""
        c = theme.get_colors()

        self.setFrameStyle(QFrame.Shape.StyledPanel)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setMinimumHeight(120)

        # Basis-Styling
        self.setStyleSheet(f"""
            PasswordEntryWidget {{
                background-color: {c['surface']};
                border: 2px solid {c['surface_border']};
                border-radius: 16px;
                padding: 0px;
            }}
            PasswordEntryWidget:hover {{
                background-color: {c['surface_hover']};
                border-color: {c['primary']};
            }}
        """)

        # Haupt-Layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(20, 18, 20, 18)

        # === ERSTE ZEILE: Name und Action Buttons ===
        first_row = QHBoxLayout()
        first_row.setSpacing(12)

        # Icon und Name
        name_container = QHBoxLayout()
        name_container.setSpacing(10)

        # Key Icon
        key_icon_label = QLabel()
        key_pixmap = icon_provider.get_pixmap("key", c['primary'], 20)
        key_icon_label.setPixmap(key_pixmap)
        key_icon_label.setFixedSize(20, 20)
        name_container.addWidget(key_icon_label)

        # Name Label
        name_label = QLabel(self.entry.name)
        name_font = QFont()
        name_font.setPointSize(14)
        name_font.setBold(True)
        name_label.setFont(name_font)
        name_label.setStyleSheet(f"color: {c['text_primary']};")
        name_container.addWidget(name_label)
        name_container.addStretch()

        first_row.addLayout(name_container)
        first_row.addStretch()

        # Action Buttons
        button_style_base = f"""
            QPushButton {{
                background-color: {c['background_tertiary']};
                border: 2px solid {c['surface_border']};
                border-radius: 10px;
            }}
        """

        # View Button
        self.view_button = QPushButton()
        view_icon = icon_provider.get_icon("eye", c['text_secondary'], 18)
        self.view_button.setIcon(view_icon)
        self.view_button.setFixedSize(40, 40)
        self.view_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.view_button.clicked.connect(self.toggle_password)
        self.view_button.setToolTip("Passwort anzeigen/verstecken")
        self.view_button.setStyleSheet(button_style_base + f"""
            QPushButton:hover {{
                background-color: {c['primary']};
                border-color: {c['primary']};
            }}
        """)
        first_row.addWidget(self.view_button)

        # Copy Button
        self.copy_button = QPushButton()
        copy_icon = icon_provider.get_icon("copy", c['text_secondary'], 18)
        self.copy_button.setIcon(copy_icon)
        self.copy_button.setFixedSize(40, 40)
        self.copy_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.copy_button.clicked.connect(self.copy_password)
        self.copy_button.setToolTip("Passwort kopieren")
        self.copy_button.setStyleSheet(button_style_base + f"""
            QPushButton:hover {{
                background-color: {c['secondary']};
                border-color: {c['secondary']};
            }}
        """)
        first_row.addWidget(self.copy_button)

        # Edit Button
        self.edit_button = QPushButton()
        edit_icon = icon_provider.get_icon("edit", c['text_secondary'], 18)
        self.edit_button.setIcon(edit_icon)
        self.edit_button.setFixedSize(40, 40)
        self.edit_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.edit_button.clicked.connect(lambda: self.edit_clicked.emit(self.entry))
        self.edit_button.setToolTip("Bearbeiten")
        self.edit_button.setStyleSheet(button_style_base + f"""
            QPushButton:hover {{
                background-color: {c['warning']};
                border-color: {c['warning']};
            }}
        """)
        first_row.addWidget(self.edit_button)

        # Delete Button
        self.delete_button = QPushButton()
        delete_icon = icon_provider.get_icon("trash", c['text_secondary'], 18)
        self.delete_button.setIcon(delete_icon)
        self.delete_button.setFixedSize(40, 40)
        self.delete_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.delete_button.clicked.connect(lambda: self.delete_clicked.emit(self.entry))
        self.delete_button.setToolTip("Löschen")
        self.delete_button.setStyleSheet(button_style_base + f"""
            QPushButton:hover {{
                background-color: {c['danger']};
                border-color: {c['danger']};
            }}
        """)
        first_row.addWidget(self.delete_button)

        main_layout.addLayout(first_row)

        # === DETAILS CONTAINER ===
        details_layout = QVBoxLayout()
        details_layout.setSpacing(8)

        # Username (falls vorhanden)
        if self.entry.username:
            username_container = QHBoxLayout()
            username_container.setSpacing(8)

            user_icon_label = QLabel()
            user_pixmap = icon_provider.get_pixmap("user", c['text_tertiary'], 14)
            user_icon_label.setPixmap(user_pixmap)
            user_icon_label.setFixedSize(14, 14)
            username_container.addWidget(user_icon_label)

            username_label = QLabel(self.entry.username)
            username_label.setStyleSheet(f"color: {c['text_secondary']}; font-size: 13px;")
            username_container.addWidget(username_label)
            username_container.addStretch()

            details_layout.addLayout(username_container)

        # Passwort (versteckt)
        self.password_label = QLabel("••••••••••••")
        password_font = QFont('Consolas', 12)
        self.password_label.setFont(password_font)
        self.password_label.setStyleSheet(f"""
            color: {c['text_tertiary']};
            padding: 10px 14px;
            background-color: {c['background_tertiary']};
            border-radius: 8px;
        """)
        details_layout.addWidget(self.password_label)

        # Website (falls vorhanden)
        if self.entry.website_url:
            website_container = QHBoxLayout()
            website_container.setSpacing(8)

            link_icon_label = QLabel()
            link_pixmap = icon_provider.get_pixmap("link", c['primary'], 14)
            link_icon_label.setPixmap(link_pixmap)
            link_icon_label.setFixedSize(14, 14)
            website_container.addWidget(link_icon_label)

            website_label = QLabel(self.entry.website_url)
            website_label.setStyleSheet(f"color: {c['primary']}; font-size: 12px;")
            website_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            website_label.setCursor(Qt.CursorShape.IBeamCursor)
            website_container.addWidget(website_label)
            website_container.addStretch()

            details_layout.addLayout(website_container)

        main_layout.addLayout(details_layout)
        self.setLayout(main_layout)

    def toggle_password(self):
        """Toggle zwischen sichtbarem und verstecktem Passwort mit Animation"""
        c = theme.get_colors()
        self.password_visible = not self.password_visible

        if self.password_visible:
            try:
                decrypted = encryption_manager.decrypt(self.entry.encrypted_password)
                self.password_label.setText(decrypted)

                password_font = QFont('Consolas', 12)
                password_font.setBold(True)
                self.password_label.setFont(password_font)

                self.password_label.setStyleSheet(f"""
                    color: {c['text_primary']};
                    padding: 10px 14px;
                    background-color: {c['background_tertiary']};
                    border-radius: 8px;
                    border: 2px solid {c['primary']};
                """)

                # Update Icon
                eye_off_icon = icon_provider.get_icon("eye_off", c['text_secondary'], 18)
                self.view_button.setIcon(eye_off_icon)

                # Animation
                animator.pulse(self.password_label, 1.02, 150)

            except Exception as e:
                self.password_label.setText(f"❌ Fehler beim Entschlüsseln")
                self.password_label.setStyleSheet(f"""
                    color: {c['danger']};
                    padding: 10px 14px;
                    background-color: {c['background_tertiary']};
                    border-radius: 8px;
                """)
        else:
            self.password_label.setText("••••••••••••")
            password_font = QFont('Consolas', 12)
            self.password_label.setFont(password_font)

            self.password_label.setStyleSheet(f"""
                color: {c['text_tertiary']};
                padding: 10px 14px;
                background-color: {c['background_tertiary']};
                border-radius: 8px;
            """)

            # Update Icon
            eye_icon = icon_provider.get_icon("eye", c['text_secondary'], 18)
            self.view_button.setIcon(eye_icon)

    def copy_password(self):
        """Kopiert das Passwort in die Zwischenablage mit visuellem Feedback"""
        c = theme.get_colors()
        try:
            decrypted = encryption_manager.decrypt(self.entry.encrypted_password)
            clipboard_manager.copy_to_clipboard(decrypted, auto_clear_seconds=30)

            # Visuelles Feedback
            check_icon = icon_provider.get_icon("check", "white", 18)
            self.copy_button.setIcon(check_icon)
            self.copy_button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {c['secondary']};
                    border: none;
                    border-radius: 10px;
                }}
            """)

            # Pulse Animation
            animator.pulse(self.copy_button, 1.15, 180)

            # Zurücksetzen nach 1.5 Sekunden
            QTimer.singleShot(1500, self.reset_copy_button)

        except Exception as e:
            self.password_label.setText(f"❌ Fehler: {str(e)}")

    def reset_copy_button(self):
        """Setzt den Copy-Button zurück"""
        c = theme.get_colors()
        copy_icon = icon_provider.get_icon("copy", c['text_secondary'], 18)
        self.copy_button.setIcon(copy_icon)
        self.copy_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {c['background_tertiary']};
                border: 2px solid {c['surface_border']};
                border-radius: 10px;
            }}
            QPushButton:hover {{
                background-color: {c['secondary']};
                border-color: {c['secondary']};
            }}
        """)


class CategoryButton(QPushButton):
    """Moderner Button für Kategorien in der Sidebar"""

    def __init__(self, category_id: int, name: str, count: int, color: str = None, parent=None):
        super().__init__(parent)
        self.category_id = category_id
        self.category_name = name
        self.count = count
        self.color = color or "#808080"

        self.setCheckable(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setMinimumHeight(48)

        self.update_display()
        self.setStyleSheet(self._get_stylesheet())

    def update_display(self):
        """Aktualisiert die Anzeige des Buttons"""
        c = theme.get_colors()

        # Layout für Button-Inhalt
        layout = QHBoxLayout()
        layout.setContentsMargins(12, 0, 12, 0)
        layout.setSpacing(10)

        # Icon
        if "Alle" in self.category_name:
            icon_name = "folder"
        else:
            icon_name = "folder_open"

        icon_label = QLabel()
        icon_pixmap = icon_provider.get_pixmap(icon_name, c['text_secondary'], 18)
        icon_label.setPixmap(icon_pixmap)
        icon_label.setFixedSize(18, 18)

        # Text
        text_label = QLabel(f"{self.category_name}")
        text_label.setStyleSheet(f"color: {c['text_primary']}; font-size: 13px; background: transparent; border: none;")

        # Count Badge
        count_label = QLabel(str(self.count))
        count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        count_label.setFixedSize(28, 22)
        count_label.setStyleSheet(f"""
            background-color: {c['background_tertiary']};
            color: {c['text_secondary']};
            border-radius: 11px;
            font-size: 11px;
            font-weight: 600;
        """)

        # Zusammensetzen
        container = QWidget()
        button_layout = QHBoxLayout(container)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(10)
        button_layout.addWidget(icon_label)
        button_layout.addWidget(text_label)
        button_layout.addStretch()
        button_layout.addWidget(count_label)

        self.setText("")  # Entferne Text, verwende Layout
        # Da QPushButton kein Layout direkt unterstützt, verwenden wir weiterhin Text
        # aber mit besserem Styling
        self.setText(f"  {self.category_name}")

    def _get_stylesheet(self) -> str:
        """Gibt das Stylesheet für den Button zurück"""
        c = theme.get_colors()
        return f"""
            QPushButton {{
                text-align: left;
                padding: 12px 16px;
                border: none;
                border-left: 4px solid transparent;
                background-color: transparent;
                font-size: 14px;
                font-weight: 500;
                border-radius: 0px 12px 12px 0px;
                color: {c['text_primary']};
            }}
            QPushButton:hover {{
                background-color: {c['surface_hover']};
            }}
            QPushButton:checked {{
                background-color: {c['surface_hover']};
                border-left: 4px solid {self.color};
                font-weight: 700;
                color: {c['primary']};
            }}
            QPushButton:pressed {{
                background-color: {c['background_tertiary']};
            }}
        """

    def update_count(self, count: int):
        """Aktualisiert die Anzahl der Einträge"""
        self.count = count
        self.setText(f"  {self.category_name}")
        # Für eine bessere Anzeige können wir später ein Custom Paint Event verwenden
