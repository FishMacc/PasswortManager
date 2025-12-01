"""
Animations-System für moderne UI-Übergänge im Apple-Stil

Bietet flüssige Animationen für Fenster, Widgets und UI-Elemente.
"""
from PyQt6.QtCore import (
    QPropertyAnimation, QEasingCurve, QParallelAnimationGroup,
    QSequentialAnimationGroup, QPoint, QSize, Qt, QTimer, pyqtProperty
)
from PyQt6.QtWidgets import QWidget, QGraphicsOpacityEffect
from PyQt6.QtGui import QColor
from typing import Optional


class AnimationHelper:
    """Hilfsklasse für einfache Animation-Erstellung"""

    @staticmethod
    def fade_in(widget: QWidget, duration: int = 300, on_finished: Optional[callable] = None):
        """
        Fade-In Animation für ein Widget

        Args:
            widget: Das zu animierende Widget
            duration: Dauer in Millisekunden
            on_finished: Callback-Funktion nach Abschluss
        """
        # Erstelle Opacity-Effekt falls noch nicht vorhanden
        if not widget.graphicsEffect() or not isinstance(widget.graphicsEffect(), QGraphicsOpacityEffect):
            effect = QGraphicsOpacityEffect(widget)
            widget.setGraphicsEffect(effect)
        else:
            effect = widget.graphicsEffect()

        # Animation
        animation = QPropertyAnimation(effect, b"opacity")
        animation.setDuration(duration)
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)

        if on_finished:
            animation.finished.connect(on_finished)

        animation.start()
        # Speichere Referenz, damit Animation nicht garbage collected wird
        widget._fade_animation = animation

    @staticmethod
    def fade_out(widget: QWidget, duration: int = 300, on_finished: Optional[callable] = None):
        """
        Fade-Out Animation für ein Widget

        Args:
            widget: Das zu animierende Widget
            duration: Dauer in Millisekunden
            on_finished: Callback-Funktion nach Abschluss
        """
        if not widget.graphicsEffect() or not isinstance(widget.graphicsEffect(), QGraphicsOpacityEffect):
            effect = QGraphicsOpacityEffect(widget)
            widget.setGraphicsEffect(effect)
        else:
            effect = widget.graphicsEffect()

        animation = QPropertyAnimation(effect, b"opacity")
        animation.setDuration(duration)
        animation.setStartValue(1.0)
        animation.setEndValue(0.0)
        animation.setEasingCurve(QEasingCurve.Type.InCubic)

        if on_finished:
            animation.finished.connect(on_finished)

        animation.start()
        widget._fade_animation = animation

    @staticmethod
    def slide_in_from_top(widget: QWidget, duration: int = 400, distance: int = 50):
        """
        Slide-In Animation von oben

        Args:
            widget: Das zu animierende Widget
            duration: Dauer in Millisekunden
            distance: Verschiebungs-Distanz in Pixeln
        """
        original_pos = widget.pos()
        start_pos = QPoint(original_pos.x(), original_pos.y() - distance)

        # Setze Startposition
        widget.move(start_pos)

        # Animation
        animation = QPropertyAnimation(widget, b"pos")
        animation.setDuration(duration)
        animation.setStartValue(start_pos)
        animation.setEndValue(original_pos)
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)

        animation.start()
        widget._slide_animation = animation

    @staticmethod
    def slide_in_from_bottom(widget: QWidget, duration: int = 400, distance: int = 50):
        """Slide-In Animation von unten"""
        original_pos = widget.pos()
        start_pos = QPoint(original_pos.x(), original_pos.y() + distance)

        widget.move(start_pos)

        animation = QPropertyAnimation(widget, b"pos")
        animation.setDuration(duration)
        animation.setStartValue(start_pos)
        animation.setEndValue(original_pos)
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)

        animation.start()
        widget._slide_animation = animation

    @staticmethod
    def scale_in(widget: QWidget, duration: int = 300):
        """
        Scale-In Animation (von klein zu normal)

        Args:
            widget: Das zu animierende Widget
            duration: Dauer in Millisekunden
        """
        original_size = widget.size()
        start_size = QSize(int(original_size.width() * 0.95), int(original_size.height() * 0.95))

        # Erstelle Opacity-Effekt
        if not widget.graphicsEffect():
            effect = QGraphicsOpacityEffect(widget)
            widget.setGraphicsEffect(effect)
        else:
            effect = widget.graphicsEffect()

        # Größen-Animation
        size_animation = QPropertyAnimation(widget, b"size")
        size_animation.setDuration(duration)
        size_animation.setStartValue(start_size)
        size_animation.setEndValue(original_size)
        size_animation.setEasingCurve(QEasingCurve.Type.OutBack)

        # Opacity-Animation
        opacity_animation = QPropertyAnimation(effect, b"opacity")
        opacity_animation.setDuration(duration)
        opacity_animation.setStartValue(0.0)
        opacity_animation.setEndValue(1.0)
        opacity_animation.setEasingCurve(QEasingCurve.Type.OutCubic)

        # Parallel-Gruppe
        group = QParallelAnimationGroup(widget)
        group.addAnimation(size_animation)
        group.addAnimation(opacity_animation)

        group.start()
        widget._scale_animation = group

    @staticmethod
    def pulse(widget: QWidget, scale_factor: float = 1.05, duration: int = 200):
        """
        Pulse Animation (kurzes Aufblinken/Vergrößern)

        Args:
            widget: Das zu animierende Widget
            scale_factor: Vergrößerungsfaktor
            duration: Dauer in Millisekunden
        """
        original_size = widget.size()
        larger_size = QSize(
            int(original_size.width() * scale_factor),
            int(original_size.height() * scale_factor)
        )

        # Vergrößern
        expand = QPropertyAnimation(widget, b"size")
        expand.setDuration(duration)
        expand.setStartValue(original_size)
        expand.setEndValue(larger_size)
        expand.setEasingCurve(QEasingCurve.Type.OutCubic)

        # Verkleinern
        shrink = QPropertyAnimation(widget, b"size")
        shrink.setDuration(duration)
        shrink.setStartValue(larger_size)
        shrink.setEndValue(original_size)
        shrink.setEasingCurve(QEasingCurve.Type.InCubic)

        # Sequenz
        sequence = QSequentialAnimationGroup(widget)
        sequence.addAnimation(expand)
        sequence.addAnimation(shrink)

        sequence.start()
        widget._pulse_animation = sequence

    @staticmethod
    def press(widget: QWidget, scale_factor: float = 0.95, duration: int = 100):
        """
        Press Animation (Button wird beim Drücken kleiner)

        Optimiert für Button-Press-Effekte - schnelle, subtile Scale-Animation

        Args:
            widget: Das zu animierende Widget (typischerweise QPushButton)
            scale_factor: Verkleinerungsfaktor (0.95 = 95% der Größe)
            duration: Dauer in Millisekunden (sollte kurz sein, 100-150ms)
        """
        original_size = widget.size()
        pressed_size = QSize(
            int(original_size.width() * scale_factor),
            int(original_size.height() * scale_factor)
        )

        # Verkleinern (schnell)
        shrink = QPropertyAnimation(widget, b"size")
        shrink.setDuration(duration)
        shrink.setStartValue(original_size)
        shrink.setEndValue(pressed_size)
        shrink.setEasingCurve(QEasingCurve.Type.OutCubic)

        # Zurück zur Originalgröße (etwas langsamer für smooth release)
        expand = QPropertyAnimation(widget, b"size")
        expand.setDuration(int(duration * 1.5))
        expand.setStartValue(pressed_size)
        expand.setEndValue(original_size)
        expand.setEasingCurve(QEasingCurve.Type.OutElastic)

        # Sequenz
        sequence = QSequentialAnimationGroup(widget)
        sequence.addAnimation(shrink)
        sequence.addAnimation(expand)

        sequence.start()
        widget._press_animation = sequence

    @staticmethod
    def shake(widget: QWidget, intensity: int = 10, duration: int = 50, times: int = 3):
        """
        Shake Animation (für Fehler-Feedback)

        Args:
            widget: Das zu animierende Widget
            intensity: Intensität der Bewegung in Pixeln
            duration: Dauer pro Bewegung in Millisekunden
            times: Anzahl der Wiederholungen
        """
        original_pos = widget.pos()

        animations = []
        for i in range(times):
            # Nach rechts
            right = QPropertyAnimation(widget, b"pos")
            right.setDuration(duration)
            right.setStartValue(original_pos)
            right.setEndValue(QPoint(original_pos.x() + intensity, original_pos.y()))
            right.setEasingCurve(QEasingCurve.Type.InOutCubic)

            # Nach links
            left = QPropertyAnimation(widget, b"pos")
            left.setDuration(duration)
            left.setStartValue(QPoint(original_pos.x() + intensity, original_pos.y()))
            left.setEndValue(QPoint(original_pos.x() - intensity, original_pos.y()))
            left.setEasingCurve(QEasingCurve.Type.InOutCubic)

            animations.extend([right, left])

        # Zurück zur ursprünglichen Position
        back = QPropertyAnimation(widget, b"pos")
        back.setDuration(duration)
        back.setStartValue(QPoint(original_pos.x() - intensity, original_pos.y()))
        back.setEndValue(original_pos)
        back.setEasingCurve(QEasingCurve.Type.InOutCubic)
        animations.append(back)

        # Sequenz
        sequence = QSequentialAnimationGroup(widget)
        for anim in animations:
            sequence.addAnimation(anim)

        sequence.start()
        widget._shake_animation = sequence

    @staticmethod
    def smooth_scroll(widget: QWidget, property_name: bytes, target_value: int,
                      duration: int = 300, easing=QEasingCurve.Type.OutCubic):
        """
        Smooth Scroll Animation

        Args:
            widget: Das zu animierende Widget
            property_name: Name der Property (z.B. b"value")
            target_value: Zielwert
            duration: Dauer in Millisekunden
            easing: Easing-Kurve
        """
        animation = QPropertyAnimation(widget, property_name)
        animation.setDuration(duration)
        animation.setEndValue(target_value)
        animation.setEasingCurve(easing)

        animation.start()
        widget._scroll_animation = animation


class AnimatedWidget(QWidget):
    """
    Basis-Widget mit eingebauter Animation-Unterstützung

    Kann als Basis für eigene animierte Widgets verwendet werden.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self._opacity_effect)
        self._opacity_effect.setOpacity(1.0)

    @pyqtProperty(float)
    def opacity(self):
        """Opacity-Property für Animationen"""
        return self._opacity_effect.opacity()

    @opacity.setter
    def opacity(self, value: float):
        """Setzt die Opacity"""
        self._opacity_effect.setOpacity(value)

    def animate_in(self, animation_type: str = "fade", duration: int = 300):
        """
        Animiert das Widget beim Erscheinen

        Args:
            animation_type: Art der Animation ("fade", "slide_top", "slide_bottom", "scale")
            duration: Dauer in Millisekunden
        """
        if animation_type == "fade":
            AnimationHelper.fade_in(self, duration)
        elif animation_type == "slide_top":
            AnimationHelper.slide_in_from_top(self, duration)
        elif animation_type == "slide_bottom":
            AnimationHelper.slide_in_from_bottom(self, duration)
        elif animation_type == "scale":
            AnimationHelper.scale_in(self, duration)

    def animate_out(self, animation_type: str = "fade", duration: int = 300,
                    on_finished: Optional[callable] = None):
        """
        Animiert das Widget beim Verschwinden

        Args:
            animation_type: Art der Animation
            duration: Dauer in Millisekunden
            on_finished: Callback nach Abschluss
        """
        if animation_type == "fade":
            AnimationHelper.fade_out(self, duration, on_finished)


# Globale Helper-Instanz
animator = AnimationHelper()
