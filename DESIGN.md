# Design-System Dokumentation

## Übersicht

SecurePass Manager verwendet ein modernes, Apple-inspiriertes Design-System mit folgenden Kernprinzipien:

- **Klarheit**: Saubere, gut lesbare Typografie und ausreichend Weißraum
- **Konsistenz**: Einheitliche Farben, Abstände und Animationen
- **Feedback**: Visuelle Rückmeldungen für Benutzeraktionen
- **Responsive**: Funktioniert auf verschiedenen Bildschirmgrößen

## Farbsystem

### Light Mode
```python
Primärfarbe:    #6366f1  (Indigo)
Sekundärfarbe:  #10b981  (Grün)
Gefahr:         #ef4444  (Rot)
Warnung:        #f59e0b  (Orange)
Hintergrund:    #ffffff  (Weiß)
Text:           #111827  (Fast Schwarz)
```

### Dark Mode
```python
Primärfarbe:    #818cf8  (Heller Indigo)
Sekundärfarbe:  #34d399  (Heller Grün)
Gefahr:         #f87171  (Heller Rot)
Warnung:        #fbbf24  (Heller Orange)
Hintergrund:    #0f172a  (Slate 900)
Text:           #f1f5f9  (Fast Weiß)
```

## Typografie

### Schriftarten
- **System**: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto
- **Monospace**: 'Consolas', 'Courier New' (für Passwörter)

### Größen
- **Titel**: 22-24px, Bold
- **Überschriften**: 14-18px, Bold
- **Body**: 13-14px, Regular
- **Klein**: 11-12px, Regular

## Abstände und Größen

### Border Radius
- **Groß**: 16px (Cards, Container)
- **Mittel**: 12px (Buttons, Inputs)
- **Klein**: 8px (Tags, Badges)

### Spacing
- **XXL**: 40px (Außenabstände)
- **XL**: 24px (Sektionsabstände)
- **L**: 20px (Container-Padding)
- **M**: 12px (Element-Spacing)
- **S**: 8px (Kleine Abstände)

### Mindestgrößen
- **Buttons**: 40-48px Höhe
- **Input-Felder**: 45-56px Höhe
- **Icons**: 18-24px für UI, 32px für Header

## Icon-System

### SVG Icons
Alle Icons verwenden SVG für gestochen scharfe Darstellung:

```python
from src.gui.icons import icon_provider

# Icon erstellen
icon = icon_provider.get_icon("lock", "#6366f1", 24)

# Pixmap für QLabel
pixmap = icon_provider.get_pixmap("key", "#ef4444", 20)
```

### Verfügbare Icons
- **Sicherheit**: lock, unlock, shield, key
- **Aktionen**: eye, eye_off, copy, check, edit, trash
- **Navigation**: folder, folder_open, search, plus
- **UI**: dice, refresh, power, sun, moon, info, user, link

## Animations-System

### Fade Animationen
```python
from src.gui.animations import animator

# Fade In
animator.fade_in(widget, duration=300)

# Fade Out
animator.fade_out(widget, duration=300, on_finished=callback)
```

### Slide Animationen
```python
# Von oben einsliden
animator.slide_in_from_top(widget, duration=400, distance=50)

# Von unten einsliden
animator.slide_in_from_bottom(widget, duration=400, distance=50)
```

### Scale und Pulse
```python
# Scale In (von klein zu normal)
animator.scale_in(widget, duration=300)

# Pulse (kurzes Aufblinken)
animator.pulse(widget, scale_factor=1.05, duration=200)
```

### Shake Animation
```python
# Für Fehler-Feedback
animator.shake(widget, intensity=10, duration=50, times=3)
```

## Component Guidelines

### Buttons

#### Primary Button
```python
style = f"""
    QPushButton {{
        background-color: {c['primary']};
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0 24px;
        min-height: 48px;
        font-size: 14px;
        font-weight: 600;
    }}
    QPushButton:hover {{
        background-color: {c['primary_hover']};
    }}
"""
```

#### Secondary Button
```python
style = f"""
    QPushButton {{
        background-color: {c['background_tertiary']};
        color: {c['text_primary']};
        border: 2px solid {c['surface_border']};
        border-radius: 12px;
        padding: 0 24px;
        min-height: 48px;
    }}
    QPushButton:hover {{
        background-color: {c['surface_hover']};
        border-color: {c['primary']};
    }}
"""
```

#### Icon Button
```python
button = QPushButton()
icon = icon_provider.get_icon("copy", c['text_secondary'], 18)
button.setIcon(icon)
button.setFixedSize(40, 40)
button.setStyleSheet(f"""
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
```

### Input-Felder

```python
style = f"""
    QLineEdit {{
        background-color: {c['input_background']};
        color: {c['text_primary']};
        border: 2px solid {c['input_border']};
        border-radius: 12px;
        padding: 0 16px;
        min-height: 48px;
    }}
    QLineEdit:focus {{
        border-color: {c['primary']};
    }}
"""
```

### Cards/Container

```python
style = f"""
    QFrame {{
        background-color: {c['surface']};
        border: 2px solid {c['surface_border']};
        border-radius: 16px;
        padding: 20px;
    }}
"""
```

### Progress Bars

```python
style = f"""
    QProgressBar {{
        border: none;
        border-radius: 5px;
        background-color: {c['background_tertiary']};
        height: 10px;
    }}
    QProgressBar::chunk {{
        background-color: {c['primary']};
        border-radius: 5px;
    }}
"""
```

### Checkboxen

```python
style = f"""
    QCheckBox {{
        color: {c['text_primary']};
        spacing: 12px;
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
    }}
"""
```

## Responsive Design

### Mindestgrößen
```python
# Dialoge
dialog.setMinimumSize(550, 600)

# Hauptfenster
window.setMinimumSize(900, 600)

# Sidebar
sidebar.setMinimumWidth(200)
sidebar.setMaximumWidth(300)
```

### Size Policies
```python
widget.setSizePolicy(
    QSizePolicy.Policy.Expanding,
    QSizePolicy.Policy.Fixed
)
```

## Animationen Best Practices

### Timing
- **Schnell** (150-200ms): Hover-Effekte, kleine Änderungen
- **Normal** (300-400ms): Dialoge, Übergänge
- **Langsam** (500-600ms): Große Änderungen, wichtige Übergänge

### Easing
- **OutCubic**: Für Eingangs-Animationen (smooth ending)
- **InCubic**: Für Ausgangs-Animationen (smooth beginning)
- **InOutCubic**: Für Bewegungen
- **OutBack**: Für Bounce-Effekt

### Beispiel-Sequenz
```python
# 1. Fade in Container
animator.fade_in(container, 300)

# 2. Nach kurzer Verzögerung: Slide in Content
QTimer.singleShot(100, lambda: animator.slide_in_from_top(content, 400))

# 3. Pulse bei Aktion
button.clicked.connect(lambda: animator.pulse(button, 1.1, 200))
```

## Accessibility

### Kontrast
- Text auf Hintergrund: Mindestens 4.5:1
- Große Text/Icons: Mindestens 3:1
- Primärfarben auf weiß: >4.5:1

### Fokus-Indikatoren
```python
QLineEdit:focus {{
    border: 2px solid {c['primary']};
    outline: none;
}}
```

### Tooltips
Alle Icon-Buttons sollten Tooltips haben:
```python
button.setToolTip("Passwort kopieren")
```

## Theme-Wechsel

```python
from src.gui.themes import theme, ThemeMode

# Zwischen Light/Dark wechseln
theme.toggle_mode()

# Spezifischen Modus setzen
theme.set_mode(ThemeMode.DARK)

# Aktuelles Theme anwenden
app.setStyleSheet(theme.get_stylesheet())
```

## Performance

### Icon-Caching
Icons werden on-the-fly generiert. Für bessere Performance bei vielen Widgets:
```python
# Icons einmal erstellen und wiederverwenden
self._icons = {
    'copy': icon_provider.get_icon("copy", c['text_secondary'], 18),
    'edit': icon_provider.get_icon("edit", c['text_secondary'], 18),
    # ...
}
```

### Animation-Referenzen
Animationen müssen als Widget-Attribut gespeichert werden:
```python
animation.start()
widget._animation = animation  # Verhindert Garbage Collection
```

## Testing

### Visuelle Tests
1. Teste alle Komponenten in Light und Dark Mode
2. Teste auf verschiedenen DPI-Einstellungen (100%, 125%, 150%, 200%)
3. Teste bei verschiedenen Fenstergrößen (Minimum bis Maximum)
4. Teste alle Hover- und Active-States
5. Teste alle Animationen auf flüssige Ausführung

### Responsive Tests
```python
# Teste mit verschiedenen Größen
window.resize(900, 600)   # Minimum
window.resize(1200, 800)  # Normal
window.resize(1920, 1080) # Groß
```

## Changelog

### Version 1.1 (2025)
- ✅ SVG-Icon-System implementiert
- ✅ Animations-System mit Fade, Slide, Scale, Pulse, Shake
- ✅ Passwortgenerator komplett überarbeitet
- ✅ Widgets modernisiert mit Icons und Animationen
- ✅ Responsive Design verbessert
- ⏳ Entry Dialog Modernisierung (geplant)
- ⏳ Login Dialog Modernisierung (geplant)
- ⏳ Main Window Modernisierung (geplant)

---

**Letzte Aktualisierung**: November 2025
**Version**: 1.1.0
