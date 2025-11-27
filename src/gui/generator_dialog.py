"""
Passwort-Generator Dialog
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSlider, QCheckBox, QProgressBar
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from ..password.generator import password_generator
from ..password.strength import password_strength_checker, PasswordStrength
from .themes import theme


class PasswordGeneratorDialog(QDialog):
    """Dialog zum Generieren von sicheren Passwörtern"""

    # Signal wird emittiert, wenn ein Passwort übernommen wird
    password_generated = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_password = ""
        self.setup_ui()
        self.generate_password()  # Generiere initiales Passwort

    def setup_ui(self):
        """Erstellt das UI des Generator-Dialogs"""
        self.setWindowTitle("Passwort Generieren")
        self.setModal(True)
        self.setFixedSize(500, 500)

        c = theme.get_colors()

        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Titel mit Icon
        title_layout = QHBoxLayout()
        title_icon = QLabel("🎲")
        title_icon_font = QFont()
        title_icon_font.setPointSize(20)
        title_icon.setFont(title_icon_font)
        title_layout.addWidget(title_icon)

        title = QLabel("Passwort Generieren")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet(f"color: {c['text_primary']};")
        title_layout.addWidget(title)
        title_layout.addStretch()
        layout.addLayout(title_layout)

        # Generiertes Passwort Anzeige
        password_label = QLabel("Generiertes Passwort")
        password_label.setStyleSheet(f"color: {c['text_secondary']}; font-weight: 500;")
        layout.addWidget(password_label)

        password_layout = QHBoxLayout()
        self.password_display = QLineEdit()
        self.password_display.setReadOnly(True)
        self.password_display.setMinimumHeight(50)
        self.password_display.setStyleSheet(f"""
            QLineEdit {{
                font-family: 'Courier New', monospace;
                font-size: 14px;
                font-weight: 600;
                background-color: {c['background_tertiary']};
                border: 2px solid {c['surface_border']};
            }}
        """)
        password_layout.addWidget(self.password_display)

        self.copy_button = QPushButton("📋")
        self.copy_button.setFixedSize(50, 50)
        self.copy_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.copy_button.clicked.connect(self.copy_password)
        self.copy_button.setToolTip("In Zwischenablage kopieren")
        self.copy_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {c['background_tertiary']};
                border: 2px solid {c['surface_border']};
                font-size: 18px;
            }}
            QPushButton:hover {{
                background-color: {c['surface_hover']};
            }}
        """)
        password_layout.addWidget(self.copy_button)

        layout.addLayout(password_layout)

        # Stärke-Anzeige
        strength_layout = QHBoxLayout()
        strength_label_text = QLabel("Stärke:")
        strength_label_text.setStyleSheet(f"color: {c['text_secondary']};")
        strength_layout.addWidget(strength_label_text)

        self.strength_bar = QProgressBar()
        self.strength_bar.setMaximum(100)
        self.strength_bar.setTextVisible(False)
        self.strength_bar.setFixedHeight(8)
        strength_layout.addWidget(self.strength_bar)

        self.strength_label = QLabel("Stark")
        self.strength_label.setMinimumWidth(80)
        self.strength_label.setStyleSheet(f"color: {c['text_primary']}; font-weight: 600;")
        strength_layout.addWidget(self.strength_label)

        layout.addLayout(strength_layout)

        # Trennlinie
        separator = QLabel()
        separator.setFixedHeight(1)
        separator.setStyleSheet(f"background-color: {c['surface_border']};")
        layout.addWidget(separator)

        # Längen-Slider
        length_label = QLabel("Länge")
        length_label.setStyleSheet(f"color: {c['text_secondary']}; font-weight: 500; margin-top: 10px;")
        layout.addWidget(length_label)

        slider_layout = QHBoxLayout()
        self.length_slider = QSlider(Qt.Orientation.Horizontal)
        self.length_slider.setMinimum(8)
        self.length_slider.setMaximum(64)
        self.length_slider.setValue(16)
        self.length_slider.setCursor(Qt.CursorShape.PointingHandCursor)
        self.length_slider.valueChanged.connect(self.on_options_changed)
        slider_layout.addWidget(self.length_slider)

        self.length_label = QLabel("16")
        self.length_label.setMinimumWidth(30)
        self.length_label.setStyleSheet(f"""
            color: {c['primary']};
            font-weight: 700;
            font-size: 14px;
        """)
        slider_layout.addWidget(self.length_label)

        layout.addLayout(slider_layout)

        # Optionen
        options_label = QLabel("Zeichenoptionen")
        options_label.setStyleSheet(f"color: {c['text_secondary']}; font-weight: 500; margin-top: 15px;")
        layout.addWidget(options_label)

        self.uppercase_check = QCheckBox("Großbuchstaben (A-Z)")
        self.uppercase_check.setChecked(True)
        self.uppercase_check.setCursor(Qt.CursorShape.PointingHandCursor)
        self.uppercase_check.stateChanged.connect(self.on_options_changed)
        layout.addWidget(self.uppercase_check)

        self.lowercase_check = QCheckBox("Kleinbuchstaben (a-z)")
        self.lowercase_check.setChecked(True)
        self.lowercase_check.setCursor(Qt.CursorShape.PointingHandCursor)
        self.lowercase_check.stateChanged.connect(self.on_options_changed)
        layout.addWidget(self.lowercase_check)

        self.digits_check = QCheckBox("Zahlen (0-9)")
        self.digits_check.setChecked(True)
        self.digits_check.setCursor(Qt.CursorShape.PointingHandCursor)
        self.digits_check.stateChanged.connect(self.on_options_changed)
        layout.addWidget(self.digits_check)

        self.special_check = QCheckBox("Sonderzeichen (!@#$...)")
        self.special_check.setChecked(True)
        self.special_check.setCursor(Qt.CursorShape.PointingHandCursor)
        self.special_check.stateChanged.connect(self.on_options_changed)
        layout.addWidget(self.special_check)

        layout.addStretch()

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        self.regenerate_button = QPushButton("🔄 Neu generieren")
        self.regenerate_button.setMinimumHeight(40)
        self.regenerate_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.regenerate_button.clicked.connect(self.generate_password)
        self.regenerate_button.setProperty("class", "secondary")
        button_layout.addWidget(self.regenerate_button)

        button_layout.addStretch()

        self.cancel_button = QPushButton("Abbrechen")
        self.cancel_button.setMinimumHeight(40)
        self.cancel_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.cancel_button.clicked.connect(self.reject)
        self.cancel_button.setProperty("class", "secondary")
        button_layout.addWidget(self.cancel_button)

        self.accept_button = QPushButton("✓ Übernehmen")
        self.accept_button.setMinimumHeight(40)
        self.accept_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.accept_button.clicked.connect(self.accept_password)
        button_layout.addWidget(self.accept_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def on_options_changed(self):
        """Wird aufgerufen, wenn sich die Generator-Optionen ändern"""
        # Aktualisiere Längen-Label
        self.length_label.setText(str(self.length_slider.value()))

        # Generiere neues Passwort
        self.generate_password()

    def generate_password(self):
        """Generiert ein neues Passwort basierend auf den Optionen"""
        try:
            length = self.length_slider.value()
            options = {
                "uppercase": self.uppercase_check.isChecked(),
                "lowercase": self.lowercase_check.isChecked(),
                "digits": self.digits_check.isChecked(),
                "special": self.special_check.isChecked()
            }

            # Stelle sicher, dass mindestens eine Option ausgewählt ist
            if not any(options.values()):
                self.password_display.setText("Wähle mindestens eine Option aus")
                self.current_password = ""
                return

            # Generiere Passwort
            password = password_generator.generate(length, options)
            self.current_password = password
            self.password_display.setText(password)

            # Update Stärke-Anzeige
            self.update_strength_display(password)

        except Exception as e:
            self.password_display.setText(f"Fehler: {str(e)}")

    def update_strength_display(self, password: str):
        """
        Aktualisiert die Passwort-Stärke-Anzeige

        Args:
            password: Das zu bewertende Passwort
        """
        c = theme.get_colors()
        strength = password_strength_checker.check_strength(password)
        percentage = password_strength_checker.get_strength_percentage(password)

        self.strength_bar.setValue(percentage)
        self.strength_label.setText(strength.value)

        # Farbe basierend auf Stärke
        if strength == PasswordStrength.WEAK:
            color = c["danger"]  # Rot
        elif strength == PasswordStrength.MEDIUM:
            color = c["warning"]  # Orange
        else:
            color = c["secondary"]  # Grün

        self.strength_bar.setStyleSheet(f"""
            QProgressBar {{
                border: none;
                border-radius: 4px;
                background-color: {c['background_tertiary']};
                text-align: center;
            }}
            QProgressBar::chunk {{
                background-color: {color};
                border-radius: 4px;
            }}
        """)

    def copy_password(self):
        """Kopiert das generierte Passwort in die Zwischenablage"""
        if self.current_password:
            from ..utils.clipboard import clipboard_manager
            clipboard_manager.copy_to_clipboard(self.current_password, auto_clear_seconds=30)

    def accept_password(self):
        """Übernimmt das generierte Passwort"""
        if self.current_password:
            self.password_generated.emit(self.current_password)
            self.accept()
