"""
Theme-System für Light und Dark Mode
"""
from enum import Enum
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtWidgets import QApplication


class ThemeMode(Enum):
    """Theme-Modi"""
    LIGHT = "light"
    DARK = "dark"


class Theme(QObject):
    """Theme-Verwaltung mit modernen Farben"""

    # Signal wird emittiert, wenn das Theme gewechselt wird
    theme_changed = pyqtSignal()

    # Light Mode Farben
    LIGHT = {
        # Hauptfarben
        "primary": "#6366f1",  # Indigo
        "primary_hover": "#4f46e5",
        "primary_light": "#818cf8",
        "secondary": "#10b981",  # Grün
        "secondary_hover": "#059669",
        "danger": "#ef4444",  # Rot
        "danger_hover": "#dc2626",
        "warning": "#f59e0b",  # Orange

        # Hintergrundfarben
        "background": "#ffffff",
        "background_secondary": "#f9fafb",
        "background_tertiary": "#f3f4f6",

        # Oberflächenfarben
        "surface": "#ffffff",
        "surface_hover": "#f9fafb",
        "surface_border": "#e5e7eb",

        # Textfarben
        "text_primary": "#111827",
        "text_secondary": "#6b7280",
        "text_tertiary": "#9ca3af",
        "text_on_primary": "#ffffff",

        # Spezielle Farben
        "input_background": "#ffffff",
        "input_border": "#d1d5db",
        "input_focus": "#6366f1",

        # Schatten
        "shadow": "rgba(0, 0, 0, 0.1)",
        "shadow_hover": "rgba(0, 0, 0, 0.15)",
    }

    # Dark Mode Farben
    DARK = {
        # Hauptfarben
        "primary": "#818cf8",  # Heller Indigo
        "primary_hover": "#a5b4fc",
        "primary_light": "#c7d2fe",
        "secondary": "#34d399",  # Heller Grün
        "secondary_hover": "#6ee7b7",
        "danger": "#f87171",  # Heller Rot
        "danger_hover": "#fca5a5",
        "warning": "#fbbf24",  # Heller Orange

        # Hintergrundfarben
        "background": "#0f172a",  # Slate 900
        "background_secondary": "#1e293b",  # Slate 800
        "background_tertiary": "#334155",  # Slate 700

        # Oberflächenfarben
        "surface": "#1e293b",
        "surface_hover": "#334155",
        "surface_border": "#475569",

        # Textfarben
        "text_primary": "#f1f5f9",
        "text_secondary": "#cbd5e1",
        "text_tertiary": "#94a3b8",
        "text_on_primary": "#0f172a",

        # Spezielle Farben
        "input_background": "#1e293b",
        "input_border": "#475569",
        "input_focus": "#818cf8",

        # Schatten
        "shadow": "rgba(0, 0, 0, 0.4)",
        "shadow_hover": "rgba(0, 0, 0, 0.6)",
    }

    def __init__(self):
        super().__init__()
        self.current_mode = ThemeMode.LIGHT

    def get_colors(self):
        """Gibt die aktuellen Theme-Farben zurück"""
        return self.DARK if self.current_mode == ThemeMode.DARK else self.LIGHT

    def toggle_mode(self):
        """Wechselt zwischen Light und Dark Mode"""
        self.current_mode = ThemeMode.DARK if self.current_mode == ThemeMode.LIGHT else ThemeMode.LIGHT
        self.theme_changed.emit()

    def set_mode(self, mode: ThemeMode):
        """Setzt einen bestimmten Theme-Modus"""
        self.current_mode = mode
        self.theme_changed.emit()

    def get_stylesheet(self) -> str:
        """Gibt das globale Stylesheet zurück"""
        c = self.get_colors()

        return f"""
            /* Globale Styles */
            QWidget {{
                background-color: {c["background"]};
                color: {c["text_primary"]};
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
                font-size: 13px;
            }}

            /* Buttons */
            QPushButton {{
                background-color: {c["primary"]};
                color: {c["text_on_primary"]};
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: 500;
            }}

            QPushButton:hover {{
                background-color: {c["primary_hover"]};
            }}

            QPushButton:pressed {{
                background-color: {c["primary"]};
            }}

            QPushButton:disabled {{
                background-color: {c["background_tertiary"]};
                color: {c["text_tertiary"]};
            }}

            /* Secondary Button */
            QPushButton[class="secondary"] {{
                background-color: {c["background_tertiary"]};
                color: {c["text_primary"]};
            }}

            QPushButton[class="secondary"]:hover {{
                background-color: {c["surface_hover"]};
            }}

            /* Danger Button */
            QPushButton[class="danger"] {{
                background-color: {c["danger"]};
                color: white;
            }}

            QPushButton[class="danger"]:hover {{
                background-color: {c["danger_hover"]};
            }}

            /* Input Fields */
            QLineEdit, QTextEdit {{
                background-color: {c["input_background"]};
                color: {c["text_primary"]};
                border: 2px solid {c["input_border"]};
                border-radius: 8px;
                padding: 10px 15px;
            }}

            QLineEdit:focus, QTextEdit:focus {{
                border: 2px solid {c["input_focus"]};
                outline: none;
            }}

            /* ComboBox */
            QComboBox {{
                background-color: {c["input_background"]};
                color: {c["text_primary"]};
                border: 2px solid {c["input_border"]};
                border-radius: 8px;
                padding: 10px 15px;
                min-height: 20px;
            }}

            QComboBox:hover {{
                border: 2px solid {c["primary"]};
            }}

            QComboBox::drop-down {{
                border: none;
                width: 30px;
            }}

            QComboBox::down-arrow {{
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid {c["text_secondary"]};
                width: 0;
                height: 0;
            }}

            QComboBox QAbstractItemView {{
                background-color: {c["surface"]};
                color: {c["text_primary"]};
                border: 1px solid {c["surface_border"]};
                border-radius: 8px;
                selection-background-color: {c["primary"]};
                selection-color: white;
                padding: 5px;
            }}

            /* Labels */
            QLabel {{
                background-color: transparent;
                color: {c["text_primary"]};
                border: none;
            }}

            /* ScrollArea */
            QScrollArea {{
                border: none;
                background-color: {c["background"]};
            }}

            /* ScrollBar */
            QScrollBar:vertical {{
                background-color: {c["background"]};
                width: 12px;
                border-radius: 6px;
            }}

            QScrollBar::handle:vertical {{
                background-color: {c["surface_border"]};
                border-radius: 6px;
                min-height: 30px;
            }}

            QScrollBar::handle:vertical:hover {{
                background-color: {c["text_tertiary"]};
            }}

            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}

            QScrollBar:horizontal {{
                background-color: {c["background"]};
                height: 12px;
                border-radius: 6px;
            }}

            QScrollBar::handle:horizontal {{
                background-color: {c["surface_border"]};
                border-radius: 6px;
                min-width: 30px;
            }}

            QScrollBar::handle:horizontal:hover {{
                background-color: {c["text_tertiary"]};
            }}

            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
                width: 0px;
            }}

            /* ProgressBar */
            QProgressBar {{
                border: none;
                border-radius: 5px;
                background-color: {c["background_tertiary"]};
                text-align: center;
                color: {c["text_primary"]};
            }}

            QProgressBar::chunk {{
                border-radius: 5px;
                background-color: {c["primary"]};
            }}

            /* CheckBox */
            QCheckBox {{
                spacing: 8px;
                color: {c["text_primary"]};
            }}

            QCheckBox::indicator {{
                width: 20px;
                height: 20px;
                border-radius: 5px;
                border: 2px solid {c["input_border"]};
                background-color: {c["input_background"]};
            }}

            QCheckBox::indicator:checked {{
                background-color: {c["primary"]};
                border-color: {c["primary"]};
            }}

            QCheckBox::indicator:hover {{
                border-color: {c["primary"]};
            }}

            /* Slider */
            QSlider::groove:horizontal {{
                height: 6px;
                background: {c["background_tertiary"]};
                border-radius: 3px;
            }}

            QSlider::handle:horizontal {{
                background: {c["primary"]};
                width: 18px;
                height: 18px;
                margin: -6px 0;
                border-radius: 9px;
            }}

            QSlider::handle:horizontal:hover {{
                background: {c["primary_hover"]};
            }}

            /* MenuBar */
            QMenuBar {{
                background-color: {c["background"]};
                color: {c["text_primary"]};
                border-bottom: 1px solid {c["surface_border"]};
                padding: 5px;
            }}

            QMenuBar::item {{
                padding: 8px 12px;
                border-radius: 5px;
            }}

            QMenuBar::item:selected {{
                background-color: {c["surface_hover"]};
            }}

            /* Menu */
            QMenu {{
                background-color: {c["surface"]};
                color: {c["text_primary"]};
                border: 1px solid {c["surface_border"]};
                border-radius: 8px;
                padding: 5px;
            }}

            QMenu::item {{
                padding: 8px 30px 8px 15px;
                border-radius: 5px;
            }}

            QMenu::item:selected {{
                background-color: {c["primary"]};
                color: white;
            }}

            /* Dialog */
            QDialog {{
                background-color: {c["background"]};
            }}

            /* Frame */
            QFrame {{
                background-color: transparent;
            }}

            /* MessageBox */
            QMessageBox {{
                background-color: {c["background"]};
            }}

            QMessageBox QLabel {{
                color: {c["text_primary"]};
            }}

            /* Splitter */
            QSplitter::handle {{
                background-color: {c["surface_border"]};
            }}

            QSplitter::handle:hover {{
                background-color: {c["primary"]};
            }}
        """

    def apply_theme(self, app: QApplication):
        """Wendet das aktuelle Theme auf die Anwendung an"""
        app.setStyleSheet(self.get_stylesheet())


# Globale Theme-Instanz
theme = Theme()
