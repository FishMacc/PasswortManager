"""
Screenshot-Vergleichs-System für UI-Tests

Ermöglicht automatische Screenshot-Tests und visuelle Regression-Tests.
"""
import os
import logging
from pathlib import Path
from typing import Optional, Tuple
from PIL import Image, ImageChops, ImageDraw, ImageFont
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QSize

logger = logging.getLogger(__name__)


class ScreenshotCompare:
    """Vergleicht Screenshots für UI-Regression-Tests"""

    def __init__(self, base_dir: str = "test_screenshots"):
        """
        Initialisiert Screenshot-Vergleich

        Args:
            base_dir: Verzeichnis für Screenshots
        """
        self.base_dir = Path(base_dir)
        self.baseline_dir = self.base_dir / "baseline"
        self.current_dir = self.base_dir / "current"
        self.diff_dir = self.base_dir / "diff"

        # Erstelle Verzeichnisse
        for dir_path in [self.baseline_dir, self.current_dir, self.diff_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)

    def capture_widget(self, widget: QWidget, name: str) -> str:
        """
        Erstellt Screenshot eines Widgets

        Args:
            widget: Das Widget
            name: Name für den Screenshot

        Returns:
            Pfad zum Screenshot
        """
        try:
            # Stelle sicher dass Widget sichtbar ist
            if not widget.isVisible():
                widget.show()
                widget.repaint()

            # Erstelle Pixmap
            pixmap = widget.grab()

            # Speichere in current
            filepath = self.current_dir / f"{name}.png"
            pixmap.save(str(filepath))

            logger.info(f"Screenshot erstellt: {filepath}")
            return str(filepath)

        except Exception as e:
            logger.error(f"Fehler beim Screenshot erstellen: {e}")
            return ""

    def save_as_baseline(self, name: str) -> bool:
        """
        Speichert aktuellen Screenshot als Baseline

        Args:
            name: Name des Screenshots

        Returns:
            True wenn erfolgreich
        """
        try:
            current_path = self.current_dir / f"{name}.png"
            baseline_path = self.baseline_dir / f"{name}.png"

            if not current_path.exists():
                logger.error(f"Kein aktueller Screenshot gefunden: {name}")
                return False

            # Kopiere nach baseline
            import shutil
            shutil.copy(current_path, baseline_path)

            logger.info(f"Baseline gespeichert: {baseline_path}")
            return True

        except Exception as e:
            logger.error(f"Fehler beim Baseline speichern: {e}")
            return False

    def compare(self, name: str, threshold: float = 0.01) -> Tuple[bool, float, Optional[str]]:
        """
        Vergleicht aktuellen Screenshot mit Baseline

        Args:
            name: Name des Screenshots
            threshold: Akzeptabler Unterschied (0.0 - 1.0)

        Returns:
            (passed, difference, diff_image_path)
            - passed: True wenn innerhalb threshold
            - difference: Prozentsatz Unterschied (0.0 - 1.0)
            - diff_image_path: Pfad zum Diff-Bild
        """
        try:
            current_path = self.current_dir / f"{name}.png"
            baseline_path = self.baseline_dir / f"{name}.png"

            if not baseline_path.exists():
                logger.warning(f"Keine Baseline gefunden für: {name}")
                logger.info("Tipp: Nutze save_as_baseline() um Baseline zu erstellen")
                return (False, 1.0, None)

            if not current_path.exists():
                logger.error(f"Kein aktueller Screenshot gefunden: {name}")
                return (False, 1.0, None)

            # Lade Bilder
            baseline_img = Image.open(baseline_path)
            current_img = Image.open(current_path)

            # Prüfe Dimensionen
            if baseline_img.size != current_img.size:
                logger.warning(f"Unterschiedliche Größen: {baseline_img.size} vs {current_img.size}")
                # Skaliere current auf baseline-Größe
                current_img = current_img.resize(baseline_img.size, Image.Resampling.LANCZOS)

            # Berechne Differenz
            diff = ImageChops.difference(baseline_img, current_img)

            # Konvertiere zu Graustufen für Analyse
            diff_gray = diff.convert('L')
            diff_data = list(diff_gray.getdata())

            # Berechne Prozentsatz nicht-schwarzer Pixel
            total_pixels = len(diff_data)
            different_pixels = sum(1 for pixel in diff_data if pixel > 10)  # Schwellwert für "different"
            difference_pct = different_pixels / total_pixels

            # Erstelle visuelles Diff-Bild
            diff_path = self._create_diff_image(baseline_img, current_img, diff, name)

            # Prüfe gegen threshold
            passed = difference_pct <= threshold

            logger.info(f"Screenshot-Vergleich '{name}': {difference_pct:.2%} Unterschied (Threshold: {threshold:.2%})")
            if not passed:
                logger.warning(f"Screenshot-Test FEHLGESCHLAGEN: {name}")
                logger.warning(f"Diff-Bild: {diff_path}")

            return (passed, difference_pct, diff_path)

        except Exception as e:
            logger.error(f"Fehler beim Screenshot-Vergleich: {e}")
            return (False, 1.0, None)

    def _create_diff_image(self, baseline: Image.Image, current: Image.Image,
                           diff: Image.Image, name: str) -> str:
        """
        Erstellt visuelles Diff-Bild mit Side-by-Side Vergleich

        Args:
            baseline: Baseline-Bild
            current: Aktuelles Bild
            diff: Differenz-Bild
            name: Name des Tests

        Returns:
            Pfad zum Diff-Bild
        """
        try:
            # Berechne Größen
            width = baseline.width
            height = baseline.height

            # Erstelle Side-by-Side Bild (3 Spalten)
            total_width = width * 3 + 40  # 3 Bilder + Abstand
            total_height = height + 60  # + Header

            result = Image.new('RGB', (total_width, total_height), 'white')
            draw = ImageDraw.Draw(result)

            # Versuche Font zu laden (optional)
            try:
                font = ImageFont.truetype("arial.ttf", 14)
            except:
                font = ImageFont.load_default()

            # Header-Texte
            draw.text((10, 10), "Baseline", fill='black', font=font)
            draw.text((width + 20, 10), "Current", fill='black', font=font)
            draw.text((width * 2 + 30, 10), "Diff (verstärkt)", fill='black', font=font)

            # Paste Bilder
            result.paste(baseline, (0, 40))
            result.paste(current, (width + 10, 40))

            # Verstärke Diff für bessere Sichtbarkeit
            diff_enhanced = Image.eval(diff, lambda x: min(255, x * 5))
            result.paste(diff_enhanced, (width * 2 + 20, 40))

            # Speichere
            diff_path = self.diff_dir / f"{name}_diff.png"
            result.save(diff_path)

            return str(diff_path)

        except Exception as e:
            logger.error(f"Fehler beim Diff-Bild erstellen: {e}")
            return ""

    def cleanup_current(self):
        """Löscht alle aktuellen Screenshots"""
        try:
            import shutil
            if self.current_dir.exists():
                shutil.rmtree(self.current_dir)
                self.current_dir.mkdir(parents=True, exist_ok=True)
            logger.info("Aktuelle Screenshots gelöscht")
        except Exception as e:
            logger.error(f"Fehler beim Cleanup: {e}")

    def get_stats(self) -> dict:
        """
        Gibt Statistiken über Screenshots zurück

        Returns:
            Dict mit baseline_count, current_count, diff_count
        """
        return {
            "baseline_count": len(list(self.baseline_dir.glob("*.png"))),
            "current_count": len(list(self.current_dir.glob("*.png"))),
            "diff_count": len(list(self.diff_dir.glob("*.png")))
        }


# Singleton-Instanz
screenshot_compare = ScreenshotCompare()
