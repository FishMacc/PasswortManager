"""
Dashboard mit Statistiken und Übersicht

Zeigt wichtige Metriken und Statistiken über die Passwort-Datenbank.
"""
import logging
from datetime import datetime, timedelta
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QScrollArea, QGridLayout, QPushButton
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from ..core.database import DatabaseManager
from .themes import theme
from .icons import icon_provider
from .animations import animator

logger = logging.getLogger(__name__)


class StatCard(QFrame):
    """Karte für einzelne Statistik"""

    def __init__(self, title: str, value: str, icon_name: str, color: str = None, parent=None):
        super().__init__(parent)
        self.title = title
        self.value_text = value
        self.icon_name = icon_name
        self.custom_color = color
        self.setup_ui()

    def setup_ui(self):
        """Erstellt das UI der Stat-Card"""
        c = theme.get_colors()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        # Icon + Value Row
        top_row = QHBoxLayout()

        # Icon
        icon_color = self.custom_color if self.custom_color else c['primary']
        icon = icon_provider.get_icon(self.icon_name, icon_color, 32)
        icon_label = QLabel()
        icon_label.setPixmap(icon.pixmap(32, 32))
        top_row.addWidget(icon_label)

        top_row.addStretch()

        # Value
        self.value_label = QLabel(self.value_text)
        value_font = QFont()
        value_font.setPointSize(24)
        value_font.setBold(True)
        self.value_label.setFont(value_font)
        self.value_label.setStyleSheet(f"color: {c['text_primary']}; background: transparent; border: none;")
        top_row.addWidget(self.value_label)

        layout.addLayout(top_row)

        # Title
        self.title_label = QLabel(self.title)
        title_font = QFont()
        title_font.setPointSize(12)
        self.title_label.setFont(title_font)
        self.title_label.setStyleSheet(f"color: {c['text_secondary']}; background: transparent; border: none;")
        layout.addWidget(self.title_label)

        # Card Style
        self.setStyleSheet(f"""
            StatCard {{
                background-color: {c['background_secondary']};
                border: 2px solid {c['surface_border']};
                border-radius: 12px;
            }}
            StatCard:hover {{
                border-color: {c['primary']};
                background-color: {c['surface_hover']};
            }}
        """)

        self.setMinimumSize(200, 120)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def update_value(self, new_value: str):
        """Aktualisiert den Wert"""
        self.value_text = new_value
        self.value_label.setText(new_value)
        animator.pulse(self.value_label, scale=1.05, duration=300)

    def mousePressEvent(self, event):
        """Animiere beim Klick"""
        animator.press(self)
        super().mousePressEvent(event)


class Dashboard(QWidget):
    """Dashboard mit Statistiken und Übersicht"""

    # Signals
    category_clicked = pyqtSignal(int)  # Category ID
    weak_passwords_clicked = pyqtSignal()
    recent_entries_clicked = pyqtSignal()

    def __init__(self, db_manager: DatabaseManager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.stat_cards = {}
        self.setup_ui()
        self.load_statistics()

    def setup_ui(self):
        """Erstellt das Dashboard-UI"""
        c = theme.get_colors()

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Header
        header_layout = QHBoxLayout()

        header_label = QLabel("📊 Dashboard")
        header_font = QFont()
        header_font.setPointSize(22)
        header_font.setBold(True)
        header_label.setFont(header_font)
        header_label.setStyleSheet(f"color: {c['text_primary']}; background: transparent; border: none;")
        header_layout.addWidget(header_label)

        header_layout.addStretch()

        # Refresh Button
        refresh_icon = icon_provider.get_icon("refresh", c['text_primary'], 18)
        self.refresh_button = QPushButton(" Aktualisieren")
        self.refresh_button.setIcon(refresh_icon)
        self.refresh_button.clicked.connect(self.refresh_stats)
        self.refresh_button.pressed.connect(lambda: animator.press(self.refresh_button))
        self.refresh_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.refresh_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {c['background_secondary']};
                color: {c['text_primary']};
                border: 2px solid {c['surface_border']};
                border-radius: 8px;
                padding: 8px 16px;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: {c['surface_hover']};
                border-color: {c['primary']};
            }}
        """)
        header_layout.addWidget(self.refresh_button)

        main_layout.addLayout(header_layout)

        # Scroll Area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet(f"""
            QScrollArea {{
                background-color: {c['background']};
                border: none;
            }}
        """)

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(20)

        # === STATISTIK-KARTEN ===
        stats_grid = QGridLayout()
        stats_grid.setSpacing(16)

        # Karte: Gesamt-Einträge
        self.stat_cards['total'] = StatCard(
            "Gesamt-Einträge",
            "0",
            "key",
            c['primary']
        )
        stats_grid.addWidget(self.stat_cards['total'], 0, 0)

        # Karte: Kategorien
        self.stat_cards['categories'] = StatCard(
            "Kategorien",
            "0",
            "folder",
            c['secondary']
        )
        stats_grid.addWidget(self.stat_cards['categories'], 0, 1)

        # Karte: Letzte 7 Tage
        self.stat_cards['recent'] = StatCard(
            "Letzte 7 Tage",
            "0",
            "refresh",
            c['warning']
        )
        stats_grid.addWidget(self.stat_cards['recent'], 0, 2)

        # Karte: Schwache Passwörter
        self.stat_cards['weak'] = StatCard(
            "Schwache Passwörter",
            "0",
            "shield",
            c['danger']
        )
        self.stat_cards['weak'].mousePressEvent = lambda e: self.weak_passwords_clicked.emit()
        stats_grid.addWidget(self.stat_cards['weak'], 0, 3)

        content_layout.addLayout(stats_grid)

        # === KATEGORIE-ÜBERSICHT ===
        cat_header = QLabel("📁 Kategorien-Übersicht")
        cat_header_font = QFont()
        cat_header_font.setPointSize(16)
        cat_header_font.setBold(True)
        cat_header.setFont(cat_header_font)
        cat_header.setStyleSheet(f"color: {c['text_primary']}; background: transparent; border: none;")
        content_layout.addWidget(cat_header)

        self.category_container = QVBoxLayout()
        self.category_container.setSpacing(8)
        content_layout.addLayout(self.category_container)

        # === LETZTE AKTIVITÄTEN ===
        activity_header = QLabel("🕒 Letzte Aktivitäten")
        activity_header_font = QFont()
        activity_header_font.setPointSize(16)
        activity_header_font.setBold(True)
        activity_header.setFont(activity_header_font)
        activity_header.setStyleSheet(f"color: {c['text_primary']}; background: transparent; border: none;")
        content_layout.addWidget(activity_header)

        self.activity_container = QVBoxLayout()
        self.activity_container.setSpacing(8)
        content_layout.addLayout(self.activity_container)

        content_layout.addStretch()

        scroll.setWidget(content)
        main_layout.addWidget(scroll)

    def load_statistics(self):
        """Lädt alle Statistiken"""
        try:
            # Gesamt-Einträge
            all_entries = self.db_manager.get_all_password_entries()
            self.stat_cards['total'].update_value(str(len(all_entries)))

            # Kategorien
            categories = self.db_manager.get_all_categories()
            self.stat_cards['categories'].update_value(str(len(categories)))

            # Letzte 7 Tage
            recent_count = self._count_recent_entries(all_entries, days=7)
            self.stat_cards['recent'].update_value(str(recent_count))

            # Schwache Passwörter (Platzhalter - braucht Strength-Check)
            weak_count = self._count_weak_passwords(all_entries)
            self.stat_cards['weak'].update_value(str(weak_count))

            # Lade Kategorie-Übersicht
            self._load_category_overview(categories, all_entries)

            # Lade Aktivitäten
            self._load_recent_activities(all_entries)

        except Exception as e:
            logger.error(f"Fehler beim Laden der Statistiken: {e}")

    def _count_recent_entries(self, entries, days: int = 7) -> int:
        """Zählt Einträge der letzten N Tage"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            count = 0

            for entry in entries:
                if entry.created_at:
                    # Parse created_at string
                    try:
                        created = datetime.fromisoformat(entry.created_at.replace('Z', '+00:00'))
                        if created >= cutoff_date:
                            count += 1
                    except:
                        pass

            return count
        except Exception as e:
            logger.error(f"Fehler beim Zählen recent entries: {e}")
            return 0

    def _count_weak_passwords(self, entries) -> int:
        """Zählt schwache Passwörter"""
        # TODO: Implementiere echten Strength-Check
        # Aktuell: Platzhalter mit Längen-Check
        try:
            weak_count = 0
            from ..core.encryption import encryption_manager

            for entry in entries:
                try:
                    # Entschlüssele und prüfe Länge
                    password = encryption_manager.decrypt(entry.encrypted_password)
                    if len(password) < 8:
                        weak_count += 1
                except:
                    pass

            return weak_count
        except Exception as e:
            logger.error(f"Fehler beim Zählen weak passwords: {e}")
            return 0

    def _load_category_overview(self, categories, entries):
        """Lädt Kategorie-Übersicht"""
        c = theme.get_colors()

        # Clear existing
        while self.category_container.count():
            item = self.category_container.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Zähle Einträge pro Kategorie
        cat_counts = {}
        for entry in entries:
            cat_id = entry.category_id
            cat_counts[cat_id] = cat_counts.get(cat_id, 0) + 1

        # Erstelle Kategorie-Balken
        for category in categories[:5]:  # Top 5
            count = cat_counts.get(category.id, 0)

            cat_frame = QFrame()
            cat_frame.setStyleSheet(f"""
                QFrame {{
                    background-color: {c['background_secondary']};
                    border: 1px solid {c['surface_border']};
                    border-radius: 8px;
                    padding: 12px;
                }}
                QFrame:hover {{
                    background-color: {c['surface_hover']};
                    border-color: {c['primary']};
                }}
            """)
            cat_frame.setCursor(Qt.CursorShape.PointingHandCursor)

            cat_layout = QHBoxLayout(cat_frame)

            # Color Indicator
            color_indicator = QLabel()
            color_indicator.setFixedSize(12, 12)
            color_indicator.setStyleSheet(f"""
                background-color: {category.color};
                border-radius: 6px;
            """)
            cat_layout.addWidget(color_indicator)

            # Name
            name_label = QLabel(category.name)
            name_label.setStyleSheet(f"color: {c['text_primary']}; background: transparent; border: none;")
            cat_layout.addWidget(name_label)

            cat_layout.addStretch()

            # Count
            count_label = QLabel(str(count))
            count_font = QFont()
            count_font.setBold(True)
            count_label.setFont(count_font)
            count_label.setStyleSheet(f"color: {c['primary']}; background: transparent; border: none;")
            cat_layout.addWidget(count_label)

            # Click Handler
            cat_frame.mousePressEvent = lambda e, cid=category.id: (
                animator.press(cat_frame),
                self.category_clicked.emit(cid)
            )

            self.category_container.addWidget(cat_frame)

    def _load_recent_activities(self, entries):
        """Lädt letzte Aktivitäten"""
        c = theme.get_colors()

        # Clear existing
        while self.activity_container.count():
            item = self.activity_container.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Sortiere nach Erstellungsdatum (neueste zuerst)
        try:
            sorted_entries = sorted(
                [e for e in entries if e.created_at],
                key=lambda x: x.created_at,
                reverse=True
            )[:5]  # Top 5
        except:
            sorted_entries = entries[:5]

        for entry in sorted_entries:
            activity_frame = QFrame()
            activity_frame.setStyleSheet(f"""
                QFrame {{
                    background-color: {c['background_secondary']};
                    border: 1px solid {c['surface_border']};
                    border-radius: 8px;
                    padding: 12px;
                }}
                QFrame:hover {{
                    background-color: {c['surface_hover']};
                }}
            """)

            activity_layout = QHBoxLayout(activity_frame)

            # Icon
            icon = icon_provider.get_icon("key", c['text_secondary'], 16)
            icon_label = QLabel()
            icon_label.setPixmap(icon.pixmap(16, 16))
            activity_layout.addWidget(icon_label)

            # Name
            name_label = QLabel(entry.name)
            name_label.setStyleSheet(f"color: {c['text_primary']}; background: transparent; border: none;")
            activity_layout.addWidget(name_label)

            activity_layout.addStretch()

            # Date
            if entry.created_at:
                try:
                    created = datetime.fromisoformat(entry.created_at.replace('Z', '+00:00'))
                    date_str = created.strftime("%d.%m.%Y")
                except:
                    date_str = "Unbekannt"
            else:
                date_str = "Unbekannt"

            date_label = QLabel(date_str)
            date_label.setStyleSheet(f"color: {c['text_secondary']}; background: transparent; border: none;")
            activity_layout.addWidget(date_label)

            self.activity_container.addWidget(activity_frame)

    def refresh_stats(self):
        """Aktualisiert alle Statistiken"""
        logger.info("Dashboard-Statistiken werden aktualisiert...")

        # Animiere Refresh-Button
        animator.press(self.refresh_button)

        # Lade Statistiken neu
        self.load_statistics()

        logger.info("Dashboard aktualisiert")

    def update_theme(self):
        """Aktualisiert Theme-Farben"""
        # Dashboard wird bei Bedarf neu gerendert
        self.setup_ui()
        self.load_statistics()
