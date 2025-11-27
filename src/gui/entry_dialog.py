"""
Dialog zum Hinzufügen/Bearbeiten von Passwort-Einträgen
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel,
    QLineEdit, QPushButton, QComboBox, QTextEdit, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from typing import Optional, List
from ..core.models import PasswordEntry, Category
from ..core.encryption import encryption_manager
from .generator_dialog import PasswordGeneratorDialog


class PasswordEntryDialog(QDialog):
    """Dialog zum Erstellen oder Bearbeiten von Passwort-Einträgen"""

    # Signal wird emittiert, wenn ein Eintrag gespeichert wurde
    entry_saved = pyqtSignal(PasswordEntry)

    def __init__(self, categories: List[Category], entry: Optional[PasswordEntry] = None, parent=None):
        """
        Initialisiert den Dialog

        Args:
            categories: Liste aller verfügbaren Kategorien
            entry: Bestehender Eintrag zum Bearbeiten (None für neuen Eintrag)
            parent: Eltern-Widget
        """
        super().__init__(parent)
        self.categories = categories
        self.entry = entry
        self.is_edit_mode = entry is not None
        self.password_visible = False
        self.setup_ui()

        # Falls Bearbeitungs-Modus, lade Daten
        if self.is_edit_mode:
            self.load_entry_data()

    def setup_ui(self):
        """Erstellt das UI des Entry-Dialogs"""
        title = "Eintrag bearbeiten" if self.is_edit_mode else "Neuer Eintrag"
        self.setWindowTitle(title)
        self.setModal(True)
        self.setFixedSize(500, 550)

        layout = QVBoxLayout()
        layout.setSpacing(15)

        # Titel
        title_label = QLabel(title)
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        layout.addWidget(title_label)

        # Formular
        form_layout = QFormLayout()
        form_layout.setSpacing(10)

        # Name/Titel
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("z.B. Gmail Account")
        form_layout.addRow("Name/Titel:", self.name_input)

        # Kategorie
        self.category_combo = QComboBox()
        for category in self.categories:
            self.category_combo.addItem(category.name, category.id)
        form_layout.addRow("Kategorie:", self.category_combo)

        # Benutzername
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("z.B. user@example.com")
        form_layout.addRow("Benutzername:", self.username_input)

        # Passwort
        password_layout = QHBoxLayout()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Passwort")
        password_layout.addWidget(self.password_input)

        self.toggle_password_button = QPushButton("👁")
        self.toggle_password_button.setFixedSize(35, 30)
        self.toggle_password_button.clicked.connect(self.toggle_password_visibility)
        self.toggle_password_button.setToolTip("Passwort anzeigen/verstecken")
        password_layout.addWidget(self.toggle_password_button)

        self.generate_button = QPushButton("🎲")
        self.generate_button.setFixedSize(35, 30)
        self.generate_button.clicked.connect(self.open_generator)
        self.generate_button.setToolTip("Passwort generieren")
        password_layout.addWidget(self.generate_button)

        form_layout.addRow("Passwort:", password_layout)

        # Website
        self.website_input = QLineEdit()
        self.website_input.setPlaceholderText("https://...")
        form_layout.addRow("Website:", self.website_input)

        layout.addLayout(form_layout)

        # Notizen
        layout.addWidget(QLabel("Notizen:"))
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Zusätzliche Informationen...")
        self.notes_input.setMaximumHeight(100)
        layout.addWidget(self.notes_input)

        layout.addStretch()

        # Buttons
        button_layout = QHBoxLayout()

        self.cancel_button = QPushButton("Abbrechen")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        button_layout.addStretch()

        self.save_button = QPushButton("Speichern")
        self.save_button.clicked.connect(self.save_entry)
        button_layout.addWidget(self.save_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

        # Fokus auf Name-Feld
        self.name_input.setFocus()

    def load_entry_data(self):
        """Lädt die Daten des zu bearbeitenden Eintrags"""
        if not self.entry:
            return

        self.name_input.setText(self.entry.name)
        self.username_input.setText(self.entry.username or "")
        self.website_input.setText(self.entry.website_url or "")

        # Kategorie auswählen
        for i in range(self.category_combo.count()):
            if self.category_combo.itemData(i) == self.entry.category_id:
                self.category_combo.setCurrentIndex(i)
                break

        # Passwort entschlüsseln
        try:
            decrypted_password = encryption_manager.decrypt(self.entry.encrypted_password)
            self.password_input.setText(decrypted_password)
        except Exception as e:
            QMessageBox.warning(self, "Fehler", f"Fehler beim Entschlüsseln des Passworts: {str(e)}")

        # Notizen entschlüsseln
        if self.entry.encrypted_notes:
            try:
                decrypted_notes = encryption_manager.decrypt(self.entry.encrypted_notes)
                self.notes_input.setPlainText(decrypted_notes)
            except Exception:
                pass

    def toggle_password_visibility(self):
        """Toggle zwischen sichtbarem und verstecktem Passwort"""
        self.password_visible = not self.password_visible

        if self.password_visible:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.toggle_password_button.setText("🙈")
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.toggle_password_button.setText("👁")

    def open_generator(self):
        """Öffnet den Passwort-Generator Dialog"""
        generator_dialog = PasswordGeneratorDialog(self)
        generator_dialog.password_generated.connect(self.on_password_generated)
        generator_dialog.exec()

    def on_password_generated(self, password: str):
        """
        Wird aufgerufen, wenn ein Passwort generiert wurde

        Args:
            password: Das generierte Passwort
        """
        self.password_input.setText(password)

    def save_entry(self):
        """Validiert und speichert den Eintrag"""
        # Validierung
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Fehler", "Bitte gib einen Namen ein.")
            return

        password = self.password_input.text()
        if not password:
            QMessageBox.warning(self, "Fehler", "Bitte gib ein Passwort ein.")
            return

        username = self.username_input.text().strip()
        website = self.website_input.text().strip()
        notes = self.notes_input.toPlainText().strip()
        category_id = self.category_combo.currentData()

        # Verschlüssele Passwort und Notizen
        try:
            encrypted_password = encryption_manager.encrypt(password)
            encrypted_notes = encryption_manager.encrypt(notes) if notes else None

            # Erstelle oder aktualisiere Eintrag
            if self.is_edit_mode:
                # Aktualisiere bestehenden Eintrag
                self.entry.name = name
                self.entry.username = username
                self.entry.encrypted_password = encrypted_password
                self.entry.encrypted_notes = encrypted_notes
                self.entry.website_url = website
                self.entry.category_id = category_id
            else:
                # Erstelle neuen Eintrag
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
            QMessageBox.critical(
                self,
                "Fehler",
                f"Fehler beim Verschlüsseln der Daten: {str(e)}"
            )
