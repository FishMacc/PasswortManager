"""
TOTP-Setup-Dialog für Datenbank-Unlock 2FA

Ermöglicht das Einrichten von Zwei-Faktor-Authentifizierung für das Entsperren
der Datenbank mittels QR-Code oder manuellem Secret.
"""
import logging
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QLineEdit, QMessageBox, QApplication
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QPixmap
from ..core.totp_manager import totp_manager
from .themes import theme
from .icons import icon_provider
from .animations import animator
from .responsive import responsive

logger = logging.getLogger(__name__)


class TOTPSetupDialog(QDialog):
    """Dialog zum Einrichten von 2FA für Datenbank-Unlock"""

    totp_configured = pyqtSignal(str)  # Emittiert das TOTP-Secret bei erfolgreicher Konfiguration

    def __init__(self, database_name: str, parent=None):
        super().__init__(parent)
        self.database_name = database_name
        self.totp_secret = totp_manager.generate_secret()
        self.totp_update_timer = None
        self.qr_code_pixmap = None
        self.setup_ui()

        # Starte Live-Code-Updates
        self.start_totp_updates()

    def setup_ui(self):
        """Erstellt das UI"""
        self.setWindowTitle("2FA einrichten")
        self.setModal(True)
        self.setMinimumSize(600, 780)
        self.resize(600, 780)

        # Zentriere auf Bildschirm
        screen_info = responsive.get_screen_info()
        x = (screen_info['screen_width'] - 600) // 2
        y = (screen_info['screen_height'] - 780) // 2
        self.move(x, y)

        fonts = responsive.get_font_sizes()
        spacing = responsive.get_spacing()
        c = theme.get_colors()

        # Haupt-Layout
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(spacing['section_spacing'])
        main_layout.setContentsMargins(
            spacing['margins'], spacing['margins'],
            spacing['margins'], spacing['margins']
        )

        # === HEADER ===
        header_layout = QHBoxLayout()
        header_layout.setSpacing(10)

        shield_icon_label = QLabel()
        shield_icon_size = 32
        shield_icon_pixmap = icon_provider.get_pixmap("shield", c['primary'], shield_icon_size)
        shield_icon_label.setPixmap(shield_icon_pixmap)
        shield_icon_label.setFixedSize(shield_icon_size, shield_icon_size)
        header_layout.addWidget(shield_icon_label)

        title_label = QLabel("Zwei-Faktor-Authentifizierung")
        title_font = QFont()
        title_font.setPointSize(fonts['title'])
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet(f"color: {c['text_primary']};")
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        main_layout.addLayout(header_layout)

        # === INFO ===
        info_label = QLabel(
            f"Richte 2FA für <b>{self.database_name}</b> ein. "
            "Du benötigst eine Authenticator-App wie Google Authenticator, Authy oder Microsoft Authenticator."
        )
        info_label.setWordWrap(True)
        info_label.setStyleSheet(f"color: {c['text_secondary']}; font-size: {fonts['body']}px;")
        main_layout.addWidget(info_label)

        # === QR-CODE ===
        qr_container = QFrame()
        qr_container.setStyleSheet(f"""
            QFrame {{
                background-color: {c['surface']};
                border: 2px solid {c['surface_border']};
                border-radius: 12px;
                padding: 16px;
            }}
        """)
        qr_layout = QVBoxLayout(qr_container)
        qr_layout.setSpacing(10)

        qr_label = QLabel("Schritt 1: QR-Code scannen")
        qr_label.setStyleSheet(f"color: {c['text_primary']}; font-weight: 600; font-size: {fonts['body']}px;")
        qr_layout.addWidget(qr_label)

        # QR-Code-Anzeige
        self.qr_code_label = QLabel()
        self.qr_code_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.qr_code_label.setMinimumSize(300, 300)
        self.qr_code_label.setStyleSheet(f"background-color: white; border: 2px solid {c['surface_border']}; border-radius: 8px;")
        qr_layout.addWidget(self.qr_code_label)

        # Button zum Vergrößern des QR-Codes
        enlarge_button_layout = QHBoxLayout()
        enlarge_button_layout.addStretch()

        enlarge_qr_button = QPushButton("🔍 QR-Code vergrößern")
        enlarge_qr_button.setMinimumHeight(36)
        enlarge_qr_button.setCursor(Qt.CursorShape.PointingHandCursor)
        enlarge_qr_button.clicked.connect(self.show_enlarged_qr)
        enlarge_qr_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {c['background_tertiary']};
                color: {c['text_primary']};
                border: 2px solid {c['surface_border']};
                border-radius: 8px;
                padding: 6px 16px;
                font-size: {fonts['body']-1}px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: {c['surface_hover']};
                border-color: {c['primary']};
            }}
        """)
        enlarge_button_layout.addWidget(enlarge_qr_button)
        enlarge_button_layout.addStretch()
        qr_layout.addLayout(enlarge_button_layout)

        self.generate_qr_code()

        main_layout.addWidget(qr_container)

        # === MANUELLES SECRET ===
        secret_container = QFrame()
        secret_container.setStyleSheet(f"""
            QFrame {{
                background-color: {c['surface']};
                border: 2px solid {c['surface_border']};
                border-radius: 12px;
                padding: 16px;
            }}
        """)
        secret_layout = QVBoxLayout(secret_container)
        secret_layout.setSpacing(10)

        secret_label = QLabel("Oder manuell eingeben:")
        secret_label.setStyleSheet(f"color: {c['text_primary']}; font-weight: 600; font-size: {fonts['body']}px;")
        secret_layout.addWidget(secret_label)

        secret_row = QHBoxLayout()
        secret_row.setSpacing(8)

        self.secret_input = QLineEdit()
        self.secret_input.setText(self.totp_secret)
        self.secret_input.setReadOnly(True)
        secret_font = QFont("Courier New", fonts['body'])
        self.secret_input.setFont(secret_font)
        self.secret_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {c['input_background']};
                color: {c['text_primary']};
                border: 2px solid {c['input_border']};
                border-radius: 8px;
                padding: 0 12px;
                min-height: {spacing['button_height']}px;
            }}
        """)
        secret_row.addWidget(self.secret_input)

        copy_icon = icon_provider.get_icon("copy", c['text_primary'], 16)
        self.copy_secret_button = QPushButton()
        self.copy_secret_button.setIcon(copy_icon)
        self.copy_secret_button.setFixedSize(spacing['button_height'], spacing['button_height'])
        self.copy_secret_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.copy_secret_button.setToolTip("Secret kopieren")
        self.copy_secret_button.clicked.connect(self.copy_secret)
        self.copy_secret_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {c['background_tertiary']};
                border: 2px solid {c['surface_border']};
                border-radius: 8px;
            }}
            QPushButton:hover {{
                background-color: {c['primary']};
                border-color: {c['primary']};
            }}
        """)
        secret_row.addWidget(self.copy_secret_button)

        secret_layout.addLayout(secret_row)
        main_layout.addWidget(secret_container)

        # === LIVE CODE ===
        code_container = QFrame()
        code_container.setStyleSheet(f"""
            QFrame {{
                background-color: {c['surface']};
                border: 2px solid {c['primary']};
                border-radius: 12px;
                padding: 16px;
            }}
        """)
        code_layout = QVBoxLayout(code_container)
        code_layout.setSpacing(8)

        code_header = QLabel("Schritt 2: Code testen")
        code_header.setStyleSheet(f"color: {c['text_primary']}; font-weight: 600; font-size: {fonts['body']}px;")
        code_layout.addWidget(code_header)

        code_row = QHBoxLayout()
        code_row.setSpacing(8)

        current_code_label = QLabel("Aktueller Code:")
        current_code_label.setStyleSheet(f"color: {c['text_secondary']}; font-size: {fonts['body']}px;")
        code_row.addWidget(current_code_label)

        self.totp_code_label = QLabel("000000")
        code_font = QFont("Courier New", fonts['title'], QFont.Weight.Bold)
        self.totp_code_label.setFont(code_font)
        self.totp_code_label.setStyleSheet(f"color: {c['primary']};")
        code_row.addWidget(self.totp_code_label)

        self.totp_time_label = QLabel("(30s)")
        self.totp_time_label.setStyleSheet(f"color: {c['text_secondary']}; font-size: {fonts['body']-1}px;")
        code_row.addWidget(self.totp_time_label)

        code_row.addStretch()

        code_layout.addLayout(code_row)
        main_layout.addWidget(code_container)

        main_layout.addStretch()

        # === BUTTONS ===
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        self.cancel_button = QPushButton("Abbrechen")
        self.cancel_button.setMinimumHeight(spacing['button_height'])
        self.cancel_button.setMinimumWidth(120)
        self.cancel_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.cancel_button.clicked.connect(self.reject)
        self.cancel_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {c['background_tertiary']};
                color: {c['text_primary']};
                border: 2px solid {c['surface_border']};
                border-radius: 10px;
                font-size: {fonts['button']}px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: {c['surface_hover']};
            }}
        """)
        button_layout.addWidget(self.cancel_button)

        button_layout.addStretch()

        check_icon = icon_provider.get_icon("check", "white", 16)
        self.save_button = QPushButton(" 2FA aktivieren")
        self.save_button.setIcon(check_icon)
        self.save_button.setMinimumHeight(spacing['button_height'])
        self.save_button.setMinimumWidth(150)
        self.save_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.save_button.clicked.connect(self.save_totp)
        self.save_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {c['primary']};
                color: white;
                border: none;
                border-radius: 10px;
                font-size: {fonts['button']}px;
                font-weight: 600;
                padding: 0 20px;
            }}
            QPushButton:hover {{
                background-color: {c['primary_hover']};
            }}
        """)
        button_layout.addWidget(self.save_button)

        main_layout.addLayout(button_layout)

    def generate_qr_code(self):
        """Generiert und zeigt QR-Code an"""
        try:
            import qrcode
            from io import BytesIO

            # Generiere provisioning URI
            uri = totp_manager.get_provisioning_uri(
                secret=self.totp_secret,
                name=self.database_name,
                issuer="SecurePass Manager"
            )

            # Erstelle QR-Code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(uri)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")

            # Konvertiere zu QPixmap
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)

            pixmap = QPixmap()
            pixmap.loadFromData(buffer.read())
            # Speichere Original-Pixmap für vergrößerte Ansicht
            self.qr_code_pixmap = pixmap
            scaled_pixmap = pixmap.scaled(300, 300, Qt.AspectRatioMode.KeepAspectRatio)
            self.qr_code_label.setPixmap(scaled_pixmap)

        except ImportError:
            self.qr_code_label.setText("QR-Code-Generierung nicht verfügbar\n(qrcode Bibliothek fehlt)")
            self.qr_code_label.setStyleSheet(f"color: {theme.get_colors()['text_secondary']}; font-size: 12px;")
        except Exception as e:
            logger.error(f"Fehler beim Generieren des QR-Codes: {e}")
            self.qr_code_label.setText(f"Fehler beim Generieren\ndes QR-Codes")
            self.qr_code_label.setStyleSheet(f"color: {theme.get_colors()['danger']}; font-size: 12px;")

    def show_enlarged_qr(self):
        """Zeigt QR-Code in vergrößerter Ansicht"""
        if not self.qr_code_pixmap:
            return

        # Erstelle Dialog
        enlarged_dialog = QDialog(self)
        enlarged_dialog.setWindowTitle("QR-Code - Vergrößerte Ansicht")
        enlarged_dialog.setModal(True)

        # Layout
        layout = QVBoxLayout(enlarged_dialog)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Info-Label
        c = theme.get_colors()
        fonts = responsive.get_font_sizes()
        info = QLabel("Scanne diesen QR-Code mit deiner Authenticator-App")
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info.setStyleSheet(f"color: {c['text_secondary']}; font-size: {fonts['body']}px;")
        layout.addWidget(info)

        # Großer QR-Code
        qr_label = QLabel()
        qr_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Skaliere auf 500x500 (sehr groß)
        large_pixmap = self.qr_code_pixmap.scaled(
            500, 500,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        qr_label.setPixmap(large_pixmap)
        qr_label.setStyleSheet(f"""
            background-color: white;
            border: 2px solid {c['surface_border']};
            border-radius: 12px;
            padding: 20px;
        """)
        layout.addWidget(qr_label)

        # Schließen-Button
        close_button = QPushButton("Schließen")
        close_button.setMinimumHeight(44)
        close_button.setCursor(Qt.CursorShape.PointingHandCursor)
        close_button.clicked.connect(enlarged_dialog.accept)
        close_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {c['primary']};
                color: white;
                border: none;
                border-radius: 10px;
                font-size: {fonts['button']}px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: {c['primary_hover']};
            }}
        """)
        layout.addWidget(close_button)

        # Größe und Zentrieren
        enlarged_dialog.setMinimumSize(600, 700)
        enlarged_dialog.resize(600, 700)

        screen_info = responsive.get_screen_info()
        x = (screen_info['screen_width'] - 600) // 2
        y = (screen_info['screen_height'] - 700) // 2
        enlarged_dialog.move(x, y)

        enlarged_dialog.exec()

    def start_totp_updates(self):
        """Startet Live-Code-Updates"""
        self.totp_update_timer = QTimer()
        self.totp_update_timer.timeout.connect(self.update_totp_display)
        self.totp_update_timer.start(1000)  # Jede Sekunde
        self.update_totp_display()

    def update_totp_display(self):
        """Aktualisiert TOTP-Code-Anzeige"""
        try:
            code = totp_manager.get_totp_code(self.totp_secret)
            remaining = totp_manager.get_remaining_seconds()

            self.totp_code_label.setText(code)
            self.totp_time_label.setText(f"({remaining}s)")

            # Warnung bei wenig Zeit
            c = theme.get_colors()
            fonts = responsive.get_font_sizes()
            if remaining <= 5:
                self.totp_time_label.setStyleSheet(f"color: {c['danger']}; font-weight: bold; font-size: {fonts['body']-1}px;")
            else:
                self.totp_time_label.setStyleSheet(f"color: {c['text_secondary']}; font-size: {fonts['body']-1}px;")

        except Exception as e:
            logger.error(f"Fehler beim Aktualisieren des TOTP-Codes: {e}")

    def copy_secret(self):
        """Kopiert Secret in Zwischenablage"""
        clipboard = QApplication.clipboard()
        clipboard.setText(self.totp_secret)
        animator.pulse(self.secret_input, duration=300)

    def save_totp(self):
        """Speichert TOTP-Konfiguration"""
        # Bestätigung vom Benutzer
        reply = QMessageBox.question(
            self,
            "2FA aktivieren",
            "Hast du den QR-Code erfolgreich in deiner Authenticator-App gescannt?\n\n"
            "⚠️ WICHTIG: Bewahre dein Master-Passwort UND dein Authenticator-Gerät sicher auf. "
            "Ohne beides kannst du nicht mehr auf deine Datenbank zugreifen!",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.totp_configured.emit(self.totp_secret)
            self.accept()

    def closeEvent(self, event):
        """Stoppe Timer beim Schließen"""
        if self.totp_update_timer:
            self.totp_update_timer.stop()
        super().closeEvent(event)
