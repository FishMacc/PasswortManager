"""
Passwort-Generator Dialog mit modernem Design und Animationen
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSlider, QCheckBox, QProgressBar, QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont
from ..password.generator import password_generator
from ..password.strength import password_strength_checker, PasswordStrength
from .themes import theme
from .animations import animator
from .icons import icon_provider


class PasswordGeneratorDialog(QDialog):
    """Moderner Dialog zum Generieren von sicheren Passwörtern mit Apple-Design"""

    password_generated = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_password = ""
        self.setup_ui()
        self.generate_password()

    def setup_ui(self):
        """Erstellt das moderne, responsive UI des Generator-Dialogs"""
        self.setWindowTitle("Passwort Generieren")
        self.setModal(True)

        # Responsive Größe
        self.setMinimumSize(550, 600)
        self.resize(550, 600)

        c = theme.get_colors()

        # Haupt-Container mit Padding
        main_container = QWidget()
        main_layout = QVBoxLayout(main_container)
        main_layout.setSpacing(24)
        main_layout.setContentsMargins(40, 40, 40, 40)

        # === HEADER ===
        header_layout = QHBoxLayout()
        header_layout.setSpacing(15)

        # Icon
        icon_label = QLabel()
        icon_pixmap = icon_provider.get_pixmap("dice", c['primary'], 32)
        icon_label.setPixmap(icon_pixmap)
        icon_label.setFixedSize(32, 32)
        header_layout.addWidget(icon_label)

        # Titel
        title = QLabel("Passwort Generieren")
        title_font = QFont()
        title_font.setPointSize(22)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet(f"color: {c['text_primary']};")
        header_layout.addWidget(title)
        header_layout.addStretch()

        main_layout.addLayout(header_layout)

        # === PASSWORT ANZEIGE ===
        password_section = QFrame()
        password_section.setStyleSheet(f"""
            QFrame {{
                background-color: {c['surface']};
                border: 2px solid {c['surface_border']};
                border-radius: 16px;
                padding: 20px;
            }}
        """)
        password_layout = QVBoxLayout(password_section)
        password_layout.setSpacing(12)

        # Label
        password_label = QLabel("Generiertes Passwort")
        password_label_font = QFont()
        password_label_font.setPointSize(11)
        password_label_font.setBold(True)
        password_label.setFont(password_label_font)
        password_label.setStyleSheet(f"color: {c['text_secondary']}; background: transparent; border: none; padding: 0;")
        password_layout.addWidget(password_label)

        # Passwort Display und Copy Button
        display_layout = QHBoxLayout()
        display_layout.setSpacing(12)

        self.password_display = QLineEdit()
        self.password_display.setReadOnly(True)
        self.password_display.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.password_display.setMinimumHeight(56)
        password_font = QFont('Consolas', 13)
        password_font.setBold(True)
        self.password_display.setFont(password_font)
        self.password_display.setStyleSheet(f"""
            QLineEdit {{
                background-color: {c['background_tertiary']};
                border: 2px solid {c['surface_border']};
                border-radius: 12px;
                padding: 0 16px;
                color: {c['primary']};
                selection-background-color: {c['primary']};
                selection-color: white;
            }}
            QLineEdit:focus {{
                border-color: {c['primary']};
            }}
        """)
        display_layout.addWidget(self.password_display)

        # Copy Button mit Icon
        self.copy_button = QPushButton()
        copy_icon = icon_provider.get_icon("copy", c['text_primary'], 20)
        self.copy_button.setIcon(copy_icon)
        self.copy_button.setFixedSize(56, 56)
        self.copy_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.copy_button.clicked.connect(self.copy_password)
        self.copy_button.setToolTip("In Zwischenablage kopieren")
        self.copy_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {c['background_tertiary']};
                border: 2px solid {c['surface_border']};
                border-radius: 12px;
            }}
            QPushButton:hover {{
                background-color: {c['secondary']};
                border-color: {c['secondary']};
            }}
            QPushButton:pressed {{
                transform: scale(0.95);
            }}
        """)
        display_layout.addWidget(self.copy_button)

        password_layout.addLayout(display_layout)

        # Stärke-Anzeige
        strength_container = QVBoxLayout()
        strength_container.setSpacing(8)

        strength_header = QHBoxLayout()
        strength_label_text = QLabel("Passwortstärke:")
        strength_label_text.setStyleSheet(f"color: {c['text_secondary']}; font-size: 11px; background: transparent; border: none;")
        strength_header.addWidget(strength_label_text)

        self.strength_label = QLabel("Stark")
        self.strength_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        strength_font = QFont()
        strength_font.setBold(True)
        strength_font.setPointSize(11)
        self.strength_label.setFont(strength_font)
        self.strength_label.setStyleSheet(f"color: {c['secondary']}; background: transparent; border: none;")
        strength_header.addWidget(self.strength_label)
        strength_container.addLayout(strength_header)

        self.strength_bar = QProgressBar()
        self.strength_bar.setMaximum(100)
        self.strength_bar.setTextVisible(False)
        self.strength_bar.setFixedHeight(10)
        self.strength_bar.setStyleSheet(f"""
            QProgressBar {{
                border: none;
                border-radius: 5px;
                background-color: {c['background_tertiary']};
            }}
            QProgressBar::chunk {{
                background-color: {c['secondary']};
                border-radius: 5px;
            }}
        """)
        strength_container.addWidget(self.strength_bar)

        password_layout.addLayout(strength_container)
        main_layout.addWidget(password_section)

        # === OPTIONEN ===
        options_section = QFrame()
        options_section.setStyleSheet(f"""
            QFrame {{
                background-color: {c['surface']};
                border: 2px solid {c['surface_border']};
                border-radius: 16px;
                padding: 20px;
            }}
        """)
        options_layout = QVBoxLayout(options_section)
        options_layout.setSpacing(20)

        # Längen-Kontrolle
        length_container = QVBoxLayout()
        length_container.setSpacing(10)

        length_header = QHBoxLayout()
        length_title = QLabel("Passwortlänge")
        length_title_font = QFont()
        length_title_font.setPointSize(11)
        length_title_font.setBold(True)
        length_title.setFont(length_title_font)
        length_title.setStyleSheet(f"color: {c['text_primary']}; background: transparent; border: none;")
        length_header.addWidget(length_title)

        self.length_label = QLabel("16")
        self.length_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        length_value_font = QFont()
        length_value_font.setPointSize(14)
        length_value_font.setBold(True)
        self.length_label.setFont(length_value_font)
        self.length_label.setStyleSheet(f"color: {c['primary']}; background: transparent; border: none;")
        length_header.addWidget(self.length_label)
        length_container.addLayout(length_header)

        self.length_slider = QSlider(Qt.Orientation.Horizontal)
        self.length_slider.setMinimum(8)
        self.length_slider.setMaximum(64)
        self.length_slider.setValue(16)
        self.length_slider.setCursor(Qt.CursorShape.PointingHandCursor)
        self.length_slider.valueChanged.connect(self.on_options_changed)
        self.length_slider.setStyleSheet(f"""
            QSlider::groove:horizontal {{
                height: 8px;
                background: {c['background_tertiary']};
                border-radius: 4px;
            }}
            QSlider::handle:horizontal {{
                background: {c['primary']};
                width: 20px;
                height: 20px;
                margin: -6px 0;
                border-radius: 10px;
            }}
            QSlider::handle:horizontal:hover {{
                background: {c['primary_hover']};
                width: 24px;
                height: 24px;
                margin: -8px 0;
            }}
            QSlider::sub-page:horizontal {{
                background: {c['primary']};
                border-radius: 4px;
            }}
        """)
        length_container.addWidget(self.length_slider)

        # Min/Max Labels
        min_max_layout = QHBoxLayout()
        min_label = QLabel("8")
        min_label.setStyleSheet(f"color: {c['text_tertiary']}; font-size: 10px; background: transparent; border: none;")
        min_max_layout.addWidget(min_label)
        min_max_layout.addStretch()
        max_label = QLabel("64")
        max_label.setStyleSheet(f"color: {c['text_tertiary']}; font-size: 10px; background: transparent; border: none;")
        min_max_layout.addWidget(max_label)
        length_container.addLayout(min_max_layout)

        options_layout.addLayout(length_container)

        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet(f"background-color: {c['surface_border']}; border: none; max-height: 1px;")
        options_layout.addWidget(separator)

        # Zeichenoptionen
        chars_title = QLabel("Zeichenoptionen")
        chars_title_font = QFont()
        chars_title_font.setPointSize(11)
        chars_title_font.setBold(True)
        chars_title.setFont(chars_title_font)
        chars_title.setStyleSheet(f"color: {c['text_primary']}; background: transparent; border: none;")
        options_layout.addWidget(chars_title)

        # Checkboxen mit modernem Design
        checkbox_style = f"""
            QCheckBox {{
                color: {c['text_primary']};
                spacing: 12px;
                font-size: 13px;
                background: transparent;
                border: none;
                padding: 8px;
                border-radius: 8px;
            }}
            QCheckBox:hover {{
                background-color: {c['background_tertiary']};
            }}
            QCheckBox::indicator {{
                width: 22px;
                height: 22px;
                border-radius: 6px;
                border: 2px solid {c['surface_border']};
                background-color: {c['background']};
            }}
            QCheckBox::indicator:checked {{
                background-color: {c['primary']};
                border-color: {c['primary']};
                image: none;
            }}
            QCheckBox::indicator:checked:hover {{
                background-color: {c['primary_hover']};
            }}
            QCheckBox::indicator:hover {{
                border-color: {c['primary']};
            }}
        """

        self.uppercase_check = QCheckBox("Großbuchstaben (A-Z)")
        self.uppercase_check.setChecked(True)
        self.uppercase_check.setCursor(Qt.CursorShape.PointingHandCursor)
        self.uppercase_check.stateChanged.connect(self.on_options_changed)
        self.uppercase_check.setStyleSheet(checkbox_style)
        options_layout.addWidget(self.uppercase_check)

        self.lowercase_check = QCheckBox("Kleinbuchstaben (a-z)")
        self.lowercase_check.setChecked(True)
        self.lowercase_check.setCursor(Qt.CursorShape.PointingHandCursor)
        self.lowercase_check.stateChanged.connect(self.on_options_changed)
        self.lowercase_check.setStyleSheet(checkbox_style)
        options_layout.addWidget(self.lowercase_check)

        self.digits_check = QCheckBox("Zahlen (0-9)")
        self.digits_check.setChecked(True)
        self.digits_check.setCursor(Qt.CursorShape.PointingHandCursor)
        self.digits_check.stateChanged.connect(self.on_options_changed)
        self.digits_check.setStyleSheet(checkbox_style)
        options_layout.addWidget(self.digits_check)

        self.special_check = QCheckBox("Sonderzeichen (!@#$%^&*)")
        self.special_check.setChecked(True)
        self.special_check.setCursor(Qt.CursorShape.PointingHandCursor)
        self.special_check.stateChanged.connect(self.on_options_changed)
        self.special_check.setStyleSheet(checkbox_style)
        options_layout.addWidget(self.special_check)

        main_layout.addWidget(options_section)

        main_layout.addStretch()

        # === BUTTONS ===
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)

        # Regenerate Button
        regenerate_icon = icon_provider.get_icon("refresh", c['text_primary'], 18)
        self.regenerate_button = QPushButton(" Neu generieren")
        self.regenerate_button.setIcon(regenerate_icon)
        self.regenerate_button.setMinimumHeight(48)
        self.regenerate_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.regenerate_button.clicked.connect(self.generate_password)
        self.regenerate_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {c['background_tertiary']};
                color: {c['text_primary']};
                border: 2px solid {c['surface_border']};
                border-radius: 12px;
                padding: 0 20px;
                font-size: 14px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: {c['surface_hover']};
                border-color: {c['primary']};
            }}
            QPushButton:pressed {{
                transform: scale(0.98);
            }}
        """)
        button_layout.addWidget(self.regenerate_button)

        button_layout.addStretch()

        # Cancel Button
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
                padding: 0 24px;
                font-size: 14px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: {c['surface_hover']};
            }}
        """)
        button_layout.addWidget(self.cancel_button)

        # Accept Button
        accept_icon = icon_provider.get_icon("check", "white", 18)
        self.accept_button = QPushButton(" Übernehmen")
        self.accept_button.setIcon(accept_icon)
        self.accept_button.setMinimumHeight(48)
        self.accept_button.setMinimumWidth(140)
        self.accept_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.accept_button.clicked.connect(self.accept_password)
        self.accept_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {c['primary']};
                color: white;
                border: none;
                border-radius: 12px;
                padding: 0 24px;
                font-size: 14px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: {c['primary_hover']};
            }}
            QPushButton:pressed {{
                transform: scale(0.98);
            }}
        """)
        button_layout.addWidget(self.accept_button)

        main_layout.addLayout(button_layout)

        # Set main layout
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().addWidget(main_container)

        # Fade-in Animation
        QTimer.singleShot(50, lambda: animator.fade_in(main_container, 300))

    def on_options_changed(self):
        """Wird aufgerufen, wenn sich die Generator-Optionen ändern"""
        self.length_label.setText(str(self.length_slider.value()))
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

            if not any(options.values()):
                self.password_display.setText("Wähle mindestens eine Option aus")
                self.current_password = ""
                return

            password = password_generator.generate(length, options)
            self.current_password = password
            self.password_display.setText(password)

            # Animation beim Generieren
            animator.pulse(self.password_display, 1.02, 150)

            self.update_strength_display(password)

        except Exception as e:
            self.password_display.setText(f"Fehler: {str(e)}")

    def update_strength_display(self, password: str):
        """Aktualisiert die Passwort-Stärke-Anzeige mit Animation"""
        c = theme.get_colors()
        strength = password_strength_checker.check_strength(password)
        percentage = password_strength_checker.get_strength_percentage(password)

        # Animiere Progress Bar
        animation = QPropertyAnimation(self.strength_bar, b"value")
        animation.setDuration(400)
        animation.setStartValue(self.strength_bar.value())
        animation.setEndValue(percentage)
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        animation.start()
        self._strength_animation = animation

        self.strength_label.setText(strength.value)

        # Farbe basierend auf Stärke
        if strength == PasswordStrength.WEAK:
            color = c["danger"]
            label_color = c["danger"]
        elif strength == PasswordStrength.MEDIUM:
            color = c["warning"]
            label_color = c["warning"]
        else:
            color = c["secondary"]
            label_color = c["secondary"]

        self.strength_bar.setStyleSheet(f"""
            QProgressBar {{
                border: none;
                border-radius: 5px;
                background-color: {c['background_tertiary']};
            }}
            QProgressBar::chunk {{
                background-color: {color};
                border-radius: 5px;
            }}
        """)

        self.strength_label.setStyleSheet(f"color: {label_color}; background: transparent; border: none; font-weight: bold;")

    def copy_password(self):
        """Kopiert das generierte Passwort in die Zwischenablage mit visuellem Feedback"""
        if self.current_password:
            from ..utils.clipboard import clipboard_manager
            clipboard_manager.copy_to_clipboard(self.current_password, auto_clear_seconds=30)

            c = theme.get_colors()

            # Visuelles Feedback
            check_icon = icon_provider.get_icon("check", "white", 20)
            self.copy_button.setIcon(check_icon)
            self.copy_button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {c['secondary']};
                    border: none;
                    border-radius: 12px;
                }}
            """)

            # Pulse Animation
            animator.pulse(self.copy_button, 1.1, 200)

            # Zurücksetzen nach 1.5 Sekunden
            QTimer.singleShot(1500, self.reset_copy_button)

    def reset_copy_button(self):
        """Setzt den Copy-Button zurück"""
        c = theme.get_colors()
        copy_icon = icon_provider.get_icon("copy", c['text_primary'], 20)
        self.copy_button.setIcon(copy_icon)
        self.copy_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {c['background_tertiary']};
                border: 2px solid {c['surface_border']};
                border-radius: 12px;
            }}
            QPushButton:hover {{
                background-color: {c['secondary']};
                border-color: {c['secondary']};
            }}
        """)

    def accept_password(self):
        """Übernimmt das generierte Passwort"""
        if self.current_password:
            self.password_generated.emit(self.current_password)
            self.accept()

    def showEvent(self, event):
        """Override showEvent für Eingangs-Animation"""
        super().showEvent(event)
        # Kurze Verzögerung für smooth appearance
        QTimer.singleShot(10, lambda: self.setFocus())


# Import für Animation
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve
from PyQt6.QtWidgets import QWidget
