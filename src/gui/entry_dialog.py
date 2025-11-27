"""
Dialog zum Hinzufügen/Bearbeiten von Passwort-Einträgen mit modernem Design
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel,
    QLineEdit, QPushButton, QComboBox, QTextEdit, QMessageBox, QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont
from typing import Optional, List
from ..core.models import PasswordEntry, Category
from ..core.encryption import encryption_manager
from .generator_dialog import PasswordGeneratorDialog
from .themes import theme
from .icons import icon_provider
from .animations import animator


class PasswordEntryDialog(QDialog):
    """Moderner Dialog zum Erstellen oder Bearbeiten von Passwort-Einträgen"""

    entry_saved = pyqtSignal(PasswordEntry)

    def __init__(self, categories: List[Category], entry: Optional[PasswordEntry] = None, parent=None):
        super().__init__(parent)
        self.categories = categories
        self.entry = entry
        self.is_edit_mode = entry is not None
        self.password_visible = False
        self.setup_ui()

        if self.is_edit_mode:
            self.load_entry_data()

        # Fade-in Animation
        QTimer.singleShot(50, lambda: self.animate_in())

    def animate_in(self):
        """Animiert den Dialog beim Öffnen"""
        for widget in [self.header_container, self.form_container, self.notes_container, self.button_container]:
            animator.fade_in(widget, 250)

    def setup_ui(self):
        """Erstellt das moderne, responsive UI"""
        title = "Eintrag bearbeiten" if self.is_edit_mode else "Neuer Eintrag"
        self.setWindowTitle(title)
        self.setModal(True)
        self.setMinimumSize(580, 680)
        self.resize(580, 680)

        c = theme.get_colors()

        # Haupt-Container
        main_container = QWidget()
        main_layout = QVBoxLayout(main_container)
        main_layout.setSpacing(24)
        main_layout.setContentsMargins(40, 40, 40, 40)

        # === HEADER ===
        self.header_container = QFrame()
        header_layout = QHBoxLayout(self.header_container)
        header_layout.setSpacing(15)
        header_layout.setContentsMargins(0, 0, 0, 0)

        icon_name = "edit" if self.is_edit_mode else "plus"
        icon_label = QLabel()
        icon_pixmap = icon_provider.get_pixmap(icon_name, c['primary'], 32)
        icon_label.setPixmap(icon_pixmap)
        icon_label.setFixedSize(32, 32)
        header_layout.addWidget(icon_label)

        title_label = QLabel(title)
        title_font = QFont()
        title_font.setPointSize(22)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet(f"color: {c['text_primary']};")
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        main_layout.addWidget(self.header_container)

        # === FORMULAR ===
        self.form_container = QFrame()
        self.form_container.setStyleSheet(f"""
            QFrame {{
                background-color: {c['surface']};
                border: 2px solid {c['surface_border']};
                border-radius: 16px;
                padding: 24px;
            }}
        """)
        form_layout = QFormLayout(self.form_container)
        form_layout.setSpacing(16)
        form_layout.setContentsMargins(0, 0, 0, 0)

        label_style = f"color: {c['text_primary']}; font-weight: 600; font-size: 13px;"
        input_style = f"""
            QLineEdit, QComboBox {{
                background-color: {c['input_background']};
                color: {c['text_primary']};
                border: 2px solid {c['input_border']};
                border-radius: 10px;
                padding: 12px 16px;
                min-height: 20px;
                font-size: 13px;
            }}
            QLineEdit:focus, QComboBox:focus {{
                border-color: {c['primary']};
            }}
        """

        # Name
        name_label = QLabel("Name/Titel:")
        name_label.setStyleSheet(label_style)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("z.B. Gmail Account")
        self.name_input.setStyleSheet(input_style)
        form_layout.addRow(name_label, self.name_input)

        # Kategorie
        category_label = QLabel("Kategorie:")
        category_label.setStyleSheet(label_style)
        self.category_combo = QComboBox()
        self.category_combo.setStyleSheet(input_style)
        for category in self.categories:
            self.category_combo.addItem(category.name, category.id)
        form_layout.addRow(category_label, self.category_combo)

        # Username
        username_label = QLabel("Benutzername:")
        username_label.setStyleSheet(label_style)
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("z.B. user@example.com")
        self.username_input.setStyleSheet(input_style)
        form_layout.addRow(username_label, self.username_input)

        # Passwort
        password_label = QLabel("Passwort:")
        password_label.setStyleSheet(label_style)

        password_container = QHBoxLayout()
        password_container.setSpacing(10)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Passwort eingeben")
        self.password_input.setStyleSheet(input_style)
        self.password_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        password_container.addWidget(self.password_input)

        # Toggle Password Button
        self.toggle_password_button = QPushButton()
        eye_icon = icon_provider.get_icon("eye", c['text_secondary'], 18)
        self.toggle_password_button.setIcon(eye_icon)
        self.toggle_password_button.setFixedSize(44, 44)
        self.toggle_password_button.clicked.connect(self.toggle_password_visibility)
        self.toggle_password_button.setToolTip("Passwort anzeigen/verstecken")
        self.toggle_password_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.toggle_password_button.setStyleSheet(f"""
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
        password_container.addWidget(self.toggle_password_button)

        # Generate Button
        self.generate_button = QPushButton()
        dice_icon = icon_provider.get_icon("dice", c['text_secondary'], 18)
        self.generate_button.setIcon(dice_icon)
        self.generate_button.setFixedSize(44, 44)
        self.generate_button.clicked.connect(self.open_generator)
        self.generate_button.setToolTip("Passwort generieren")
        self.generate_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.generate_button.setStyleSheet(f"""
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
        password_container.addWidget(self.generate_button)

        form_layout.addRow(password_label, password_container)

        # Website
        website_label = QLabel("Website:")
        website_label.setStyleSheet(label_style)
        self.website_input = QLineEdit()
        self.website_input.setPlaceholderText("https://...")
        self.website_input.setStyleSheet(input_style)
        form_layout.addRow(website_label, self.website_input)

        main_layout.addWidget(self.form_container)

        # === NOTIZEN ===
        self.notes_container = QFrame()
        self.notes_container.setStyleSheet(f"""
            QFrame {{
                background-color: {c['surface']};
                border: 2px solid {c['surface_border']};
                border-radius: 16px;
                padding: 20px;
            }}
        """)
        notes_layout = QVBoxLayout(self.notes_container)
        notes_layout.setSpacing(12)
        notes_layout.setContentsMargins(0, 0, 0, 0)

        notes_label = QLabel("Notizen:")
        notes_label.setStyleSheet(f"color: {c['text_primary']}; font-weight: 600; font-size: 13px;")
        notes_layout.addWidget(notes_label)

        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Zusätzliche Informationen...")
        self.notes_input.setMinimumHeight(100)
        self.notes_input.setMaximumHeight(120)
        self.notes_input.setStyleSheet(f"""
            QTextEdit {{
                background-color: {c['input_background']};
                color: {c['text_primary']};
                border: 2px solid {c['input_border']};
                border-radius: 10px;
                padding: 12px 16px;
                font-size: 13px;
            }}
            QTextEdit:focus {{
                border-color: {c['primary']};
            }}
        """)
        notes_layout.addWidget(self.notes_input)

        main_layout.addWidget(self.notes_container)

        main_layout.addStretch()

        # === BUTTONS ===
        self.button_container = QFrame()
        button_layout = QHBoxLayout(self.button_container)
        button_layout.setSpacing(12)
        button_layout.setContentsMargins(0, 0, 0, 0)

        self.cancel_button = QPushButton("Abbrechen")
        self.cancel_button.setMinimumHeight(48)
        self.cancel_button.setMinimumWidth(120)
        self.cancel_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.cancel_button.clicked.connect(self.reject)
        self.cancel_button.setStyleSheet(f"""
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
        button_layout.addWidget(self.cancel_button)

        button_layout.addStretch()

        save_icon = icon_provider.get_icon("check", "white", 18)
        self.save_button = QPushButton(" Speichern")
        self.save_button.setIcon(save_icon)
        self.save_button.setMinimumHeight(48)
        self.save_button.setMinimumWidth(140)
        self.save_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.save_button.clicked.connect(self.save_entry)
        self.save_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {c['primary']};
                color: white;
                border: none;
                border-radius: 12px;
                font-size: 14px;
                font-weight: 600;
                padding: 0 24px;
            }}
            QPushButton:hover {{
                background-color: {c['primary_hover']};
            }}
        """)
        button_layout.addWidget(self.save_button)

        main_layout.addWidget(self.button_container)

        # Set main layout
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().addWidget(main_container)

        # Fokus
        self.name_input.setFocus()

    def load_entry_data(self):
        """Lädt die Daten des zu bearbeitenden Eintrags"""
        if not self.entry:
            return

        self.name_input.setText(self.entry.name)
        self.username_input.setText(self.entry.username or "")
        self.website_input.setText(self.entry.website_url or "")

        for i in range(self.category_combo.count()):
            if self.category_combo.itemData(i) == self.entry.category_id:
                self.category_combo.setCurrentIndex(i)
                break

        try:
            decrypted_password = encryption_manager.decrypt(self.entry.encrypted_password)
            self.password_input.setText(decrypted_password)
        except Exception as e:
            QMessageBox.warning(self, "Fehler", f"Fehler beim Entschlüsseln: {str(e)}")

        if self.entry.encrypted_notes:
            try:
                decrypted_notes = encryption_manager.decrypt(self.entry.encrypted_notes)
                self.notes_input.setPlainText(decrypted_notes)
            except Exception:
                pass

    def toggle_password_visibility(self):
        """Toggle Passwort-Sichtbarkeit mit Icon-Wechsel"""
        c = theme.get_colors()
        self.password_visible = not self.password_visible

        if self.password_visible:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
            eye_off_icon = icon_provider.get_icon("eye_off", c['text_secondary'], 18)
            self.toggle_password_button.setIcon(eye_off_icon)
            animator.pulse(self.password_input, 1.01, 150)
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
            eye_icon = icon_provider.get_icon("eye", c['text_secondary'], 18)
            self.toggle_password_button.setIcon(eye_icon)

    def open_generator(self):
        """Öffnet den Passwort-Generator"""
        generator_dialog = PasswordGeneratorDialog(self)
        generator_dialog.password_generated.connect(self.on_password_generated)
        generator_dialog.exec()

    def on_password_generated(self, password: str):
        """Callback für generiertes Passwort mit Animation"""
        self.password_input.setText(password)
        animator.pulse(self.password_input, 1.02, 200)

    def save_entry(self):
        """Validiert und speichert den Eintrag"""
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Fehler", "Bitte gib einen Namen ein.")
            animator.shake(self.name_input, 8, 50, 3)
            return

        password = self.password_input.text()
        if not password:
            QMessageBox.warning(self, "Fehler", "Bitte gib ein Passwort ein.")
            animator.shake(self.password_input, 8, 50, 3)
            return

        username = self.username_input.text().strip()
        website = self.website_input.text().strip()
        notes = self.notes_input.toPlainText().strip()
        category_id = self.category_combo.currentData()

        try:
            encrypted_password = encryption_manager.encrypt(password)
            encrypted_notes = encryption_manager.encrypt(notes) if notes else None

            if self.is_edit_mode:
                self.entry.name = name
                self.entry.username = username
                self.entry.encrypted_password = encrypted_password
                self.entry.encrypted_notes = encrypted_notes
                self.entry.website_url = website
                self.entry.category_id = category_id
            else:
                self.entry = PasswordEntry(
                    id=None,
                    category_id=category_id,
                    name=name,
                    username=username,
                    encrypted_password=encrypted_password,
                    encrypted_notes=encrypted_notes,
                    website_url=website
                )

            self.entry_saved.emit(self.entry)
            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Fehler", f"Fehler beim Verschlüsseln: {str(e)}")


from PyQt6.QtWidgets import QWidget
