"""
2FA/TOTP Setup Dialog

Ermöglicht das Einrichten von TOTP-Secrets mit QR-Code-Anzeige
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QFrame, QTextEdit, QGroupBox
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap, QImage
from ..core.totp_manager import totp_manager
from .themes import theme
from .icons import icon_provider
from .animations import animator
import logging

try:
    import qrcode
    QRCODE_AVAILABLE = True
except ImportError:
    QRCODE_AVAILABLE = False
    logging.warning("qrcode Bibliothek nicht verfügbar. QR-Code-Anzeige deaktiviert.")


class TOTPDialog(QDialog):
    """Dialog zum Einrichten und Anzeigen von TOTP/2FA"""

    totp_configured = pyqtSignal(str)  # Signal mit TOTP-Secret

    def __init__(self, parent=None, existing_secret: str = None, entry_name: str = "Account"):
        super().__init__(parent)
        self.existing_secret = existing_secret
        self.entry_name = entry_name
        self.totp_secret = existing_secret or totp_manager.generate_secret()

        self.setup_ui()

        # Timer für Live-Code-Updates (alle Sekunde)
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_totp_code)
        self.update_timer.start(1000)

        # Initial update
        self.update_totp_code()

        # Theme-Updates
        theme.theme_changed.connect(self.refresh_theme)

    def setup_ui(self):
        """Erstellt das UI des TOTP-Dialogs"""
        self.setWindowTitle("2FA/TOTP einrichten")
        self.setModal(True)
        self.setMinimumSize(500, 650)
        self.resize(550, 700)

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

        # Icon
        totp_icon = icon_provider.get_icon("shield", c['primary'], 28)
        icon_label = QLabel()
        icon_label.setPixmap(totp_icon.pixmap(28, 28))
        header_layout.addWidget(icon_label)

        # Title
        title = QLabel("🔐 Zwei-Faktor-Authentifizierung")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet(f"color: {c['text_primary']}; background: transparent; border: none;")
        header_layout.addWidget(title)
        header_layout.addStretch()

        main_layout.addWidget(header)

        # === CONTENT ===
        content = QFrame()
        content.setStyleSheet(f"QFrame {{ background-color: {c['background']}; border: none; }}")
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(20)
        content_layout.setContentsMargins(24, 24, 24, 24)

        # Info-Text
        info = QLabel(
            "Scanne den QR-Code mit deiner Authenticator-App\n"
            "(Google Authenticator, Authy, Microsoft Authenticator, etc.)\n"
            "oder gib das Secret manuell ein."
        )
        info.setWordWrap(True)
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info.setStyleSheet(f"""
            color: {c['text_secondary']};
            font-size: 13px;
            padding: 12px;
            background: transparent;
            border: none;
        """)
        content_layout.addWidget(info)

        # === QR-CODE ===
        qr_group = QGroupBox("QR-Code scannen")
        qr_group.setStyleSheet(f"""
            QGroupBox {{
                background-color: {c['background_secondary']};
                border: 2px solid {c['surface_border']};
                border-radius: 12px;
                margin-top: 12px;
                padding: 20px;
                font-size: 14px;
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
        qr_layout = QVBoxLayout()

        # QR-Code Label
        self.qr_label = QLabel()
        self.qr_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.qr_label.setMinimumSize(280, 280)
        self.qr_label.setStyleSheet(f"""
            QLabel {{
                background-color: white;
                border: 2px solid {c['surface_border']};
                border-radius: 8px;
                padding: 10px;
            }}
        """)
        qr_layout.addWidget(self.qr_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # QR-Code generieren
        self.generate_qr_code()

        qr_group.setLayout(qr_layout)
        content_layout.addWidget(qr_group)

        # === SECRET (Manuell) ===
        secret_group = QGroupBox("Oder manuell eingeben")
        secret_group.setStyleSheet(qr_group.styleSheet())
        secret_layout = QVBoxLayout()

        secret_label = QLabel("Secret (Base32):")
        secret_label.setStyleSheet(f"color: {c['text_secondary']}; font-size: 12px; background: transparent; border: none;")
        secret_layout.addWidget(secret_label)

        self.secret_edit = QLineEdit(self.totp_secret)
        self.secret_edit.setReadOnly(True)
        self.secret_edit.setMinimumHeight(44)
        self.secret_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont("Courier New", 12)
        self.secret_edit.setFont(font)
        self.secret_edit.setStyleSheet(f"""
            QLineEdit {{
                background-color: {c['background_tertiary']};
                color: {c['text_primary']};
                border: 2px solid {c['surface_border']};
                border-radius: 8px;
                padding: 10px;
            }}
        """)
        secret_layout.addWidget(self.secret_edit)

        # Copy Button
        copy_icon = icon_provider.get_icon("copy", "white", 16)
        copy_button = QPushButton(" Secret kopieren")
        copy_button.setIcon(copy_icon)
        copy_button.setMinimumHeight(40)
        copy_button.setCursor(Qt.CursorShape.PointingHandCursor)
        copy_button.clicked.connect(self.copy_secret)
        copy_button.pressed.connect(lambda: animator.press(copy_button, scale_factor=0.97, duration=120))
        copy_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {c['background_tertiary']};
                color: {c['text_primary']};
                border: 2px solid {c['surface_border']};
                border-radius: 8px;
                font-size: 13px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: {c['surface_hover']};
            }}
        """)
        secret_layout.addWidget(copy_button)

        secret_group.setLayout(secret_layout)
        content_layout.addWidget(secret_group)

        # === LIVE CODE ===
        code_group = QGroupBox("Aktueller Code")
        code_group.setStyleSheet(qr_group.styleSheet())
        code_layout = QVBoxLayout()

        self.code_label = QLabel("000000")
        code_font = QFont("Courier New", 32, QFont.Weight.Bold)
        self.code_label.setFont(code_font)
        self.code_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.code_label.setStyleSheet(f"""
            QLabel {{
                color: {c['primary']};
                background-color: {c['background_tertiary']};
                border: 2px solid {c['surface_border']};
                border-radius: 10px;
                padding: 20px;
            }}
        """)
        code_layout.addWidget(self.code_label)

        # Verbleibende Zeit
        self.time_label = QLabel("Verbleibend: 30s")
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.time_label.setStyleSheet(f"""
            color: {c['text_secondary']};
            font-size: 12px;
            margin-top: 8px;
            background: transparent;
            border: none;
        """)
        code_layout.addWidget(self.time_label)

        code_group.setLayout(code_layout)
        content_layout.addWidget(code_group)

        content_layout.addStretch()

        main_layout.addWidget(content)

        # === FOOTER ===
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
        cancel_button = QPushButton("Abbrechen")
        cancel_button.setMinimumHeight(44)
        cancel_button.setMinimumWidth(110)
        cancel_button.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_button.clicked.connect(self.reject)
        cancel_button.pressed.connect(lambda: animator.press(cancel_button, scale_factor=0.97, duration=120))
        cancel_button.setStyleSheet(f"""
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
        footer_layout.addWidget(cancel_button)

        footer_layout.addStretch()

        # Save Button
        check_icon = icon_provider.get_icon("check", "white", 18)
        save_button = QPushButton(" Speichern")
        save_button.setIcon(check_icon)
        save_button.setMinimumHeight(44)
        save_button.setMinimumWidth(130)
        save_button.setCursor(Qt.CursorShape.PointingHandCursor)
        save_button.clicked.connect(self.save_totp)
        save_button.pressed.connect(lambda: animator.press(save_button, scale_factor=0.96, duration=120))
        save_button.setStyleSheet(f"""
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
        footer_layout.addWidget(save_button)

        main_layout.addWidget(footer)

    def generate_qr_code(self):
        """Generiert QR-Code für TOTP-Secret"""
        if not QRCODE_AVAILABLE:
            self.qr_label.setText("qrcode-Bibliothek nicht installiert\n\n"
                                 "Installieren Sie: pip install qrcode[pil]")
            return

        # Provisioning URI
        uri = totp_manager.get_provisioning_uri(
            self.totp_secret,
            name=self.entry_name,
            issuer="SecurePass"
        )

        # QR-Code generieren
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(uri)
        qr.make(fit=True)

        # QR-Code in Image konvertieren
        img = qr.make_image(fill_color="black", back_color="white")

        # PIL Image → QPixmap
        img = img.convert("RGB")
        data = img.tobytes("raw", "RGB")
        qimage = QImage(data, img.size[0], img.size[1], QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)

        # Skalieren auf 250x250
        pixmap = pixmap.scaled(250, 250, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)

        self.qr_label.setPixmap(pixmap)

    def update_totp_code(self):
        """Aktualisiert den angezeigten TOTP-Code"""
        code = totp_manager.get_totp_code(self.totp_secret)
        remaining = totp_manager.get_remaining_seconds()

        # Code anzeigen
        self.code_label.setText(code)

        # Verbleibende Zeit
        self.time_label.setText(f"Verbleibend: {remaining}s")

        # Warnung bei wenig Zeit
        c = theme.get_colors()
        if remaining <= 5:
            self.time_label.setStyleSheet(f"""
                color: {c['danger']};
                font-size: 12px;
                font-weight: bold;
                margin-top: 8px;
                background: transparent;
                border: none;
            """)
        else:
            self.time_label.setStyleSheet(f"""
                color: {c['text_secondary']};
                font-size: 12px;
                margin-top: 8px;
                background: transparent;
                border: none;
            """)

    def copy_secret(self):
        """Kopiert Secret in Zwischenablage"""
        from PyQt6.QtWidgets import QApplication
        clipboard = QApplication.clipboard()
        clipboard.setText(self.totp_secret)

        # Feedback
        self.secret_edit.selectAll()
        animator.pulse(self.secret_edit, duration=400)

    def save_totp(self):
        """Speichert TOTP-Secret"""
        self.totp_configured.emit(self.totp_secret)
        self.accept()

    def refresh_theme(self):
        """Aktualisiert Theme"""
        c = theme.get_colors()

        # Header
        for frame in self.findChildren(QFrame):
            style = frame.styleSheet()
            if 'border-bottom: 1px solid' in style:
                frame.setStyleSheet(f"""
                    QFrame {{
                        background-color: {c['background_secondary']};
                        border-bottom: 1px solid {c['surface_border']};
                    }}
                """)
            elif 'border-top: 1px solid' in style:
                frame.setStyleSheet(f"""
                    QFrame {{
                        background-color: {c['background_secondary']};
                        border-top: 1px solid {c['surface_border']};
                    }}
                """)
            elif 'background-color:' in style and 'border: none' in style:
                frame.setStyleSheet(f"QFrame {{ background-color: {c['background']}; border: none; }}")

        # Update alle Komponenten...
        # (Vollständiges Theme-Update würde hier folgen)

    def closeEvent(self, event):
        """Stoppe Timer beim Schließen"""
        self.update_timer.stop()
        super().closeEvent(event)
