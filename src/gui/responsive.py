"""
Responsive Design Helper für automatische Anpassung an Bildschirmgröße

Passt Dialog-Größen, Schriftgrößen und Abstände automatisch an die verfügbare Bildschirmgröße an.
"""
from PyQt6.QtWidgets import QApplication, QDialog
from PyQt6.QtCore import QSize, QRect
from PyQt6.QtGui import QScreen
from typing import Tuple, Dict
import math


class ResponsiveHelper:
    """Helper-Klasse für responsive Design"""

    @staticmethod
    def get_screen_info() -> Dict:
        """
        Gibt Informationen über den Bildschirm zurück

        Returns:
            Dict mit screen_width, screen_height, dpi, scale_factor
        """
        screen: QScreen = QApplication.primaryScreen()
        screen_geometry: QRect = screen.availableGeometry()
        dpi = screen.logicalDotsPerInch()

        # Berechne Scale-Factor basierend auf DPI
        # Standard DPI ist 96, also 1.0 = 96 DPI
        scale_factor = dpi / 96.0

        return {
            'screen_width': screen_geometry.width(),
            'screen_height': screen_geometry.height(),
            'dpi': dpi,
            'scale_factor': scale_factor
        }

    @staticmethod
    def get_size_category() -> str:
        """
        Bestimmt die Größenkategorie des Bildschirms

        Returns:
            'small' (< 1000px), 'medium' (1000-1600px), 'large' (> 1600px)
        """
        screen_info = ResponsiveHelper.get_screen_info()
        width = screen_info['screen_width']

        if width < 1000:
            return 'small'
        elif width < 1600:
            return 'medium'
        else:
            return 'large'

    @staticmethod
    def calculate_dialog_size(base_width: int, base_height: int, min_width: int = 400, min_height: int = 300) -> Tuple[int, int]:
        """
        Berechnet optimale Dialog-Größe basierend auf Bildschirmgröße

        Args:
            base_width: Basis-Breite für große Bildschirme
            base_height: Basis-Höhe für große Bildschirme
            min_width: Minimale Breite
            min_height: Minimale Höhe

        Returns:
            Tuple (width, height)
        """
        screen_info = ResponsiveHelper.get_screen_info()
        screen_width = screen_info['screen_width']
        screen_height = screen_info['screen_height']

        # Maximale Dialog-Größe: 75% der Bildschirmgröße (reduziert von 85%)
        max_width = int(screen_width * 0.75)
        max_height = int(screen_height * 0.75)

        # Skaliere basierend auf Bildschirmgröße - VIEL KLEINER
        if screen_width < 1000:
            # Kleine Bildschirme: 80% der Breite
            width = min(int(screen_width * 0.80), base_width)
            height = min(int(screen_height * 0.75), base_height)
        elif screen_width < 1400:
            # Mittlere Bildschirme: 70% der Basis-Größe
            width = min(int(base_width * 0.75), max_width)
            height = min(int(base_height * 0.75), max_height)
        else:
            # Große Bildschirme: 80% der Basis-Größe
            width = min(int(base_width * 0.8), max_width)
            height = min(int(base_height * 0.8), max_height)

        # Stelle sicher, dass Mindestgrößen eingehalten werden
        width = max(width, min_width)
        height = max(height, min_height)

        return (width, height)

    @staticmethod
    def get_font_sizes() -> Dict[str, int]:
        """
        Gibt angepasste Schriftgrößen basierend auf Bildschirmgröße zurück

        Returns:
            Dict mit title, subtitle, body, small
        """
        category = ResponsiveHelper.get_size_category()

        sizes = {
            'small': {
                'title': 16,
                'subtitle': 11,
                'body': 11,
                'small': 9,
                'button': 12
            },
            'medium': {
                'title': 18,
                'subtitle': 12,
                'body': 12,
                'small': 10,
                'button': 13
            },
            'large': {
                'title': 20,
                'subtitle': 13,
                'body': 13,
                'small': 11,
                'button': 13
            }
        }

        return sizes[category]

    @staticmethod
    def get_spacing() -> Dict[str, int]:
        """
        Gibt angepasste Abstände basierend auf Bildschirmgröße zurück

        Returns:
            Dict mit margins, section_spacing, element_spacing
        """
        category = ResponsiveHelper.get_size_category()

        spacing = {
            'small': {
                'margins': 15,
                'section_spacing': 12,
                'element_spacing': 6,
                'icon_size': 32,
                'button_height': 36
            },
            'medium': {
                'margins': 20,
                'section_spacing': 14,
                'element_spacing': 8,
                'icon_size': 36,
                'button_height': 40
            },
            'large': {
                'margins': 25,
                'section_spacing': 16,
                'element_spacing': 10,
                'icon_size': 40,
                'button_height': 42
            }
        }

        return spacing[category]

    @staticmethod
    def setup_dialog(dialog: QDialog, base_width: int, base_height: int, min_width: int = 400, min_height: int = 300):
        """
        Konfiguriert einen Dialog für responsive Design

        Args:
            dialog: Der zu konfigurierende Dialog
            base_width: Basis-Breite
            base_height: Basis-Höhe
            min_width: Minimale Breite
            min_height: Minimale Höhe
        """
        width, height = ResponsiveHelper.calculate_dialog_size(base_width, base_height, min_width, min_height)

        dialog.setMinimumSize(min_width, min_height)
        dialog.resize(width, height)

        # Zentriere Dialog auf Bildschirm
        screen_info = ResponsiveHelper.get_screen_info()
        screen_width = screen_info['screen_width']
        screen_height = screen_info['screen_height']

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        dialog.move(x, y)


# Globale Instanz
responsive = ResponsiveHelper()
