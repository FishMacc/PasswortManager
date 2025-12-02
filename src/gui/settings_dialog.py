"""
Einstellungs-Dialog mit modernem Design

Ermöglicht Konfiguration von:
- Theme (Dark/Light Mode)
- Auto-Lock Timeout
- Zwischenablage Timeout
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QSpinBox, QFrame, QScrollArea, QWidget, QGroupBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from ..core.settings import app_settings
from .themes import theme
from .icons import icon_provider
from .animations import animator


class SettingsDialog(QDialog):
    """Moderner Einstellungs-Dialog mit Kategorien"""

    # Signal wenn Einstellungen geändert wurden
    settings_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.load_settings()

        # Theme-Updates abonnieren
        theme.theme_changed.connect(self.refresh_theme)

    def setup_ui(self):
        """Erstellt das UI des Einstellungs-Dialogs"""
        self.setWindowTitle("Einstellungen")
        self.setModal(True)

        # Responsive Größe
        self.setMinimumSize(600, 500)
        self.resize(650, 600)

        c = theme.get_colors()

        # Hauptlayout
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # === HEADER ===
        header = QFrame()
        header.setStyleSheet(f"""
            QFrame {{
                background-color: {c['background_secondary']};
                border-bottom: 1px solid {c['surface_border']};
            }}
        """)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(24, 20, 24, 20)

        # Header Icon + Title
        settings_icon = icon_provider.get_icon("shield", c['primary'], 28)
        icon_label = QLabel()
        icon_label.setPixmap(settings_icon.pixmap(28, 28))
        header_layout.addWidget(icon_label)

        title = QLabel("Einstellungen")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet(f"color: {c['text_primary']}; background: transparent; border: none;")
        header_layout.addWidget(title)
        header_layout.addStretch()

        main_layout.addWidget(header)

        # === SCROLL AREA FÜR CONTENT ===
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet(f"""
            QScrollArea {{
                background-color: {c['background']};
                border: none;
            }}
        """)

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(24)
        content_layout.setContentsMargins(24, 24, 24, 24)

        # === DARSTELLUNG ===
        appearance_group = self.create_group_box("🎨 Darstellung")
        appearance_layout = QVBoxLayout()
        appearance_layout.setSpacing(16)

        # Theme Mode
        theme_row = self.create_setting_row(
            "Theme-Modus",
            "Wähle zwischen hellem und dunklem Design"
        )
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Hell", "Dunkel", "System"])
        self.theme_combo.setMinimumHeight(40)
        self.theme_combo.setCursor(Qt.CursorShape.PointingHandCursor)
        self.theme_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {c['background_tertiary']};
                color: {c['text_primary']};
                border: 2px solid {c['surface_border']};
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 14px;
            }}
            QComboBox:hover {{
                border-color: {c['primary']};
            }}
            QComboBox::drop-down {{
                border: none;
                width: 30px;
            }}
            QComboBox QAbstractItemView {{
                background-color: {c['background_tertiary']};
                color: {c['text_primary']};
                selection-background-color: {c['primary']};
                selection-color: white;
                border: 1px solid {c['surface_border']};
            }}
        """)
        theme_row.addWidget(self.theme_combo)
        appearance_layout.addLayout(theme_row)

        appearance_group.setLayout(appearance_layout)
        content_layout.addWidget(appearance_group)

        # === SICHERHEIT ===
        security_group = self.create_group_box("🔒 Sicherheit")
        security_layout = QVBoxLayout()
        security_layout.setSpacing(16)

        # Auto-Lock Timeout
        autolock_row = self.create_setting_row(
            "Auto-Lock Timeout",
            "Zeit bis zur automatischen Sperre (in Minuten)"
        )
        self.autolock_spin = QSpinBox()
        self.autolock_spin.setMinimum(1)
        self.autolock_spin.setMaximum(60)
        self.autolock_spin.setSuffix(" Min.")
        self.autolock_spin.setMinimumHeight(40)
        self.autolock_spin.setMinimumWidth(120)
        self.autolock_spin.setStyleSheet(f"""
            QSpinBox {{
                background-color: {c['background_tertiary']};
                color: {c['text_primary']};
                border: 2px solid {c['surface_border']};
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 14px;
            }}
            QSpinBox:hover {{
                border-color: {c['primary']};
            }}
            QSpinBox::up-button, QSpinBox::down-button {{
                background-color: {c['background_secondary']};
                border: none;
                width: 20px;
            }}
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {{
                background-color: {c['primary']};
            }}
        """)
        autolock_row.addWidget(self.autolock_spin)
        security_layout.addLayout(autolock_row)

        # Clipboard Clear Timeout
        clipboard_row = self.create_setting_row(
            "Zwischenablage löschen",
            "Sekunden bis Zwischenablage automatisch gelöscht wird"
        )
        self.clipboard_spin = QSpinBox()
        self.clipboard_spin.setMinimum(5)
        self.clipboard_spin.setMaximum(300)
        self.clipboard_spin.setSuffix(" Sek.")
        self.clipboard_spin.setMinimumHeight(40)
        self.clipboard_spin.setMinimumWidth(120)
        self.clipboard_spin.setStyleSheet(self.autolock_spin.styleSheet())
        clipboard_row.addWidget(self.clipboard_spin)
        security_layout.addLayout(clipboard_row)

        security_group.setLayout(security_layout)
        content_layout.addWidget(security_group)

        content_layout.addStretch()

        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)

        # === FOOTER MIT BUTTONS ===
        footer = QFrame()
        footer.setStyleSheet(f"""
            QFrame {{
                background-color: {c['background_secondary']};
                border-top: 1px solid {c['surface_border']};
            }}
        """)
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(24, 16, 24, 16)
        footer_layout.setSpacing(12)

        # Cancel Button
        self.cancel_button = QPushButton("Abbrechen")
        self.cancel_button.setMinimumHeight(44)
        self.cancel_button.setMinimumWidth(110)
        self.cancel_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.cancel_button.clicked.connect(self.reject)
        self.cancel_button.pressed.connect(lambda: animator.press(self.cancel_button, scale_factor=0.97, duration=120))
        self.cancel_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {c['background_tertiary']};
                color: {c['text_primary']};
                border: 2px solid {c['surface_border']};
                border-radius: 10px;
                font-size: 14px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: {c['surface_hover']};
            }}
        """)
        footer_layout.addWidget(self.cancel_button)

        footer_layout.addStretch()

        # Save Button
        save_icon = icon_provider.get_icon("check", "white", 18)
        self.save_button = QPushButton(" Speichern")
        self.save_button.setIcon(save_icon)
        self.save_button.setMinimumHeight(44)
        self.save_button.setMinimumWidth(130)
        self.save_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.save_button.clicked.connect(self.save_settings)
        self.save_button.pressed.connect(lambda: animator.press(self.save_button, scale_factor=0.96, duration=120))
        self.save_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {c['primary']};
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 14px;
                font-weight: 600;
                padding: 0 20px;
            }}
            QPushButton:hover {{
                background-color: {c['primary_hover']};
            }}
        """)
        footer_layout.addWidget(self.save_button)

        main_layout.addWidget(footer)

    def create_group_box(self, title: str) -> QGroupBox:
        """Erstellt eine Gruppe mit Titel"""
        c = theme.get_colors()

        group = QGroupBox(title)
        group.setStyleSheet(f"""
            QGroupBox {{
                background-color: {c['background_secondary']};
                border: 2px solid {c['surface_border']};
                border-radius: 12px;
                margin-top: 12px;
                padding: 20px;
                font-size: 15px;
                font-weight: 600;
                color: {c['text_primary']};
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 16px;
                padding: 0 8px;
                background-color: {c['background_secondary']};
            }}
        """)
        return group

    def create_setting_row(self, label_text: str, description: str) -> QHBoxLayout:
        """Erstellt eine Zeile mit Label und Beschreibung"""
        c = theme.get_colors()

        layout = QHBoxLayout()
        layout.setSpacing(16)

        # Label Container
        label_container = QVBoxLayout()
        label_container.setSpacing(4)

        # Hauptlabel
        label = QLabel(label_text)
        label_font = QFont()
        label_font.setPointSize(11)
        label_font.setBold(True)
        label.setFont(label_font)
        label.setStyleSheet(f"color: {c['text_primary']}; background: transparent; border: none;")
        label_container.addWidget(label)

        # Beschreibung
        desc = QLabel(description)
        desc.setWordWrap(True)
        desc.setStyleSheet(f"color: {c['text_secondary']}; font-size: 12px; background: transparent; border: none;")
        label_container.addWidget(desc)

        layout.addLayout(label_container, stretch=1)

        return layout

    def load_settings(self):
        """Lädt aktuelle Einstellungen"""
        # Theme Mode
        theme_mode = app_settings.get("theme_mode", "light")
        theme_index = {"light": 0, "dark": 1, "system": 2}.get(theme_mode, 0)
        self.theme_combo.setCurrentIndex(theme_index)

        # Auto-Lock
        auto_lock = app_settings.get("auto_lock_minutes", 5)
        self.autolock_spin.setValue(auto_lock)

        # Clipboard Clear
        clipboard_clear = app_settings.get("clipboard_clear_seconds", 30)
        self.clipboard_spin.setValue(clipboard_clear)

    def save_settings(self):
        """Speichert Einstellungen"""
        # Theme Mode
        theme_map = {0: "light", 1: "dark", 2: "system"}
        theme_mode = theme_map[self.theme_combo.currentIndex()]
        app_settings.set("theme_mode", theme_mode)

        # Auto-Lock
        app_settings.set("auto_lock_minutes", self.autolock_spin.value())

        # Clipboard Clear
        app_settings.set("clipboard_clear_seconds", self.clipboard_spin.value())

        # Emit Signal
        self.settings_changed.emit()

        self.accept()

    def refresh_theme(self):
        """Aktualisiert alle Farben basierend auf dem aktuellen Theme"""
        c = theme.get_colors()

        # Header
        if hasattr(self, 'findChild'):
            header = self.findChild(QFrame)
            if header:
                header.setStyleSheet(f"""
                    QFrame {{
                        background-color: {c['background_secondary']};
                        border-bottom: 1px solid {c['surface_border']};
                    }}
                """)

        # Update alle Labels im Header
        for label in self.findChildren(QLabel):
            if label.font().bold() and label.font().pointSize() == 18:
                # Title Label
                label.setStyleSheet(f"color: {c['text_primary']}; background: transparent; border: none;")

        # Update ScrollArea
        scroll_areas = self.findChildren(QScrollArea)
        for scroll in scroll_areas:
            scroll.setStyleSheet(f"""
                QScrollArea {{
                    background-color: {c['background']};
                    border: none;
                }}
            """)

        # Update ComboBox (Theme-Auswahl)
        if hasattr(self, 'theme_combo'):
            self.theme_combo.setStyleSheet(f"""
                QComboBox {{
                    background-color: {c['background_tertiary']};
                    color: {c['text_primary']};
                    border: 2px solid {c['surface_border']};
                    border-radius: 8px;
                    padding: 8px 12px;
                    font-size: 14px;
                }}
                QComboBox:hover {{
                    border-color: {c['primary']};
                }}
                QComboBox::drop-down {{
                    border: none;
                    width: 30px;
                }}
                QComboBox QAbstractItemView {{
                    background-color: {c['background_tertiary']};
                    color: {c['text_primary']};
                    selection-background-color: {c['primary']};
                    selection-color: white;
                    border: 1px solid {c['surface_border']};
                }}
            """)

        # Update SpinBoxes
        spinbox_style = f"""
            QSpinBox {{
                background-color: {c['background_tertiary']};
                color: {c['text_primary']};
                border: 2px solid {c['surface_border']};
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 14px;
            }}
            QSpinBox:hover {{
                border-color: {c['primary']};
            }}
            QSpinBox::up-button, QSpinBox::down-button {{
                background-color: {c['background_secondary']};
                border: none;
                width: 20px;
            }}
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {{
                background-color: {c['primary']};
            }}
        """
        if hasattr(self, 'autolock_spin'):
            self.autolock_spin.setStyleSheet(spinbox_style)
        if hasattr(self, 'clipboard_spin'):
            self.clipboard_spin.setStyleSheet(spinbox_style)

        # Update GroupBoxes
        for group in self.findChildren(QGroupBox):
            group.setStyleSheet(f"""
                QGroupBox {{
                    background-color: {c['background_secondary']};
                    border: 2px solid {c['surface_border']};
                    border-radius: 12px;
                    margin-top: 12px;
                    padding: 20px;
                    font-size: 15px;
                    font-weight: 600;
                    color: {c['text_primary']};
                }}
                QGroupBox::title {{
                    subcontrol-origin: margin;
                    left: 16px;
                    padding: 0 8px;
                    background-color: {c['background_secondary']};
                }}
            """)

        # Update alle Text-Labels in Settings
        for label in self.findChildren(QLabel):
            current_style = label.styleSheet()
            label_text = label.text()

            # Emoji-Labels (ℹ️) brauchen kein Color-Update
            if label_text in ['ℹ️']:
                label.setStyleSheet("font-size: 18px; background: transparent; border: none;")
            elif 'text_primary' in current_style or 'font-weight: bold' in current_style or label.font().bold():
                label.setStyleSheet(f"color: {c['text_primary']}; background: transparent; border: none;")
            elif 'text_secondary' in current_style or 'font-size: 12px' in current_style or 'font-size: 13px' in current_style:
                # Beschreibungen und Info-Texte
                font_size = '12px' if 'font-size: 12px' in current_style else '13px'
                label.setStyleSheet(f"color: {c['text_secondary']}; font-size: {font_size}; background: transparent; border: none;")

        # Update Footer
        for frame in self.findChildren(QFrame):
            if 'border-top: 1px solid' in frame.styleSheet():
                frame.setStyleSheet(f"""
                    QFrame {{
                        background-color: {c['background_secondary']};
                        border-top: 1px solid {c['surface_border']};
                    }}
                """)

        # Update Cancel Button
        if hasattr(self, 'cancel_button'):
            self.cancel_button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {c['background_tertiary']};
                    color: {c['text_primary']};
                    border: 2px solid {c['surface_border']};
                    border-radius: 10px;
                    font-size: 14px;
                    font-weight: 600;
                }}
                QPushButton:hover {{
                    background-color: {c['surface_hover']};
                }}
            """)

        # Update Save Button
        if hasattr(self, 'save_button'):
            self.save_button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {c['primary']};
                    color: white;
                    border: none;
                    border-radius: 10px;
                    font-size: 14px;
                    font-weight: 600;
                    padding: 0 20px;
                }}
                QPushButton:hover {{
                    background-color: {c['primary_hover']};
                }}
            """)

        # Update Icon im Header
        settings_icon = icon_provider.get_icon("shield", c['primary'], 28)
        for label in self.findChildren(QLabel):
            if label.pixmap() and not label.pixmap().isNull():
                label.setPixmap(settings_icon.pixmap(28, 28))
                break
