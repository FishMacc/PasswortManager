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
            'small' (< 900px), 'medium' (900-1400px), 'large' (> 1400px)
        """
        screen_info = ResponsiveHelper.get_screen_info()
        width = screen_info['screen_width']

        if width < 900:
            return 'small'
        elif width < 1400:
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

        # Maximale Dialog-Größe: 85% der Bildschirmgröße
        max_width = int(screen_width * 0.85)
        max_height = int(screen_height * 0.85)

        # Skaliere basierend auf Bildschirmgröße
        if screen_width < 900:
            # Kleine Bildschirme: 90% der Breite
            width = min(int(screen_width * 0.90), base_width)
            height = min(int(screen_height * 0.85), base_height)
        elif screen_width < 1400:
            # Mittlere Bildschirme: 70% der Basis-Größe
            width = min(int(base_width * 0.85), max_width)
            height = min(int(base_height * 0.85), max_height)
        else:
            # Große Bildschirme: Volle Basis-Größe
            width = min(base_width, max_width)
            height = min(base_height, max_height)

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
                'title': 18,
                'subtitle': 12,
                'body': 12,
                'small': 10,
                'button': 13
            },
            'medium': {
                'title': 22,
                'subtitle': 13,
                'body': 13,
                'small': 11,
                'button': 14
            },
            'large': {
                'title': 26,
                'subtitle': 14,
                'body': 14,
                'small': 12,
                'button': 15
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
                'margins': 20,
                'section_spacing': 16,
                'element_spacing': 8,
                'icon_size': 40,
                'button_height': 44
            },
            'medium': {
                'margins': 30,
                'section_spacing': 20,
                'element_spacing': 10,
                'icon_size': 48,
                'button_height': 48
            },
            'large': {
                'margins': 40,
                'section_spacing': 24,
                'element_spacing': 12,
                'icon_size': 64,
                'button_height': 52
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
