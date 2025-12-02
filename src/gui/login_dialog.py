"""
Login-Dialog für Master-Passwort (für bestehende Datenbanken)
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QFrame, QInputDialog
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont
from ..auth.master_password import master_password_manager
from ..core.database import DatabaseManager
from ..core.encryption import encryption_manager
from ..core.totp_manager import totp_manager
from .themes import theme
from .icons import icon_provider
from .animations import animator
from .responsive import responsive


class LoginDialog(QDialog):
    """Dialog für Login mit Master-Passwort"""

    login_successful = pyqtSignal(str)  # Emit password when successful

    def __init__(self, db_path: str, parent=None):
        super().__init__(parent)
        self.db_path = db_path
        self.master_password = None
        self.setup_ui()

    def setup_ui(self):
        """Erstellt das moderne UI des Login-Dialogs"""
        self.setWindowTitle("SecurePass Manager - Login")
        self.setModal(True)

        # Feste Größe basierend auf tatsächlichem Inhalt
        self.setMinimumSize(420, 400)
        self.resize(420, 420)

        # Zentriere auf Bildschirm
        screen_info = responsive.get_screen_info()
        x = (screen_info['screen_width'] - 420) // 2
        y = (screen_info['screen_height'] - 420) // 2
        self.move(x, y)
        fonts = responsive.get_font_sizes()
        spacing = responsive.get_spacing()

        c = theme.get_colors()

        # Haupt-Layout direkt auf Dialog
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(spacing['section_spacing'])
        main_layout.setContentsMargins(spacing['margins'], spacing['margins'], spacing['margins'], spacing['margins'])

        # Logo/Icon Bereich
        icon_container = QHBoxLayout()
        icon_container.addStretch()

        shield_icon = QLabel()
        shield_pixmap = icon_provider.get_pixmap("shield", c['primary'], spacing['icon_size'])
        shield_icon.setPixmap(shield_pixmap)
        shield_icon.setFixedSize(spacing['icon_size'], spacing['icon_size'])
        icon_container.addWidget(shield_icon)

        icon_container.addStretch()
        main_layout.addLayout(icon_container)

        # Titel
        title = QLabel("SecurePass Manager")
        title_font = QFont()
        title_font.setPointSize(fonts['title'])
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"color: {c['primary']};")
        main_layout.addWidget(title)

        # Untertitel
        subtitle = QLabel("Datenbank entsperren")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet(f"color: {c['text_secondary']}; font-size: {fonts['subtitle']}px;")
        main_layout.addWidget(subtitle)

        # Datenbank-Pfad Anzeige
        from pathlib import Path
        db_name = Path(self.db_path).stem
        db_name_label = QLabel(f"📁 {db_name}")
        db_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        db_name_label.setStyleSheet(f"""
            color: {c['text_tertiary']};
            font-size: {fonts['small']}px;
            padding: 8px 16px;
            background-color: {c['background_tertiary']};
            border-radius: 8px;
        """)
        main_layout.addWidget(db_name_label)

        main_layout.addSpacing(20)

        # Passwort-Feld Container
        password_container = QFrame()
        password_container.setStyleSheet(f"""
            QFrame {{
                background-color: {c['surface']};
                border: 2px solid {c['surface_border']};
                border-radius: 16px;
            }}
        """)
        password_layout = QVBoxLayout(password_container)
        password_layout.setSpacing(12)
        password_layout.setContentsMargins(24, 24, 24, 24)

        password_label = QLabel("Master-Passwort:")
        password_label.setStyleSheet(f"color: {c['text_primary']}; font-weight: 600; font-size: {fonts['body']}px; background: transparent; border: none;")
        password_layout.addWidget(password_label)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Passwort eingeben...")
        self.password_input.setMinimumHeight(spacing['button_height'])
        self.password_input.returnPressed.connect(self.handle_login)
        self.password_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {c['input_background']};
                color: {c['text_primary']};
                border: 2px solid {c['input_border']};
                border-radius: 12px;
                padding: 0 16px;
                font-size: {fonts['body']}px;
            }}
            QLineEdit:focus {{
                border-color: {c['primary']};
            }}
        """)
        password_layout.addWidget(self.password_input)

        main_layout.addWidget(password_container)

        main_layout.addStretch()

        # Login Button
        lock_icon = icon_provider.get_icon("unlock", "white", 18)
        self.login_button = QPushButton(" Entsperren")
        self.login_button.setIcon(lock_icon)
        self.login_button.setMinimumHeight(spacing['button_height'])
        self.login_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.login_button.clicked.connect(self.handle_login)
        self.login_button.setStyleSheet(f"""
            QPushButton {{
                font-size: {fonts['button']}px;
                font-weight: 700;
                background-color: {c['primary']};
                color: white;
                border: none;
                border-radius: 12px;
            }}
            QPushButton:hover {{
                background-color: {c['primary_hover']};
            }}
        """)
        main_layout.addWidget(self.login_button)

        # Fokus auf Passwort-Feld nach kurzer Verzögerung
        QTimer.singleShot(100, lambda: self.password_input.setFocus())

    def handle_login(self):
        """Behandelt den Login-Versuch"""
        password = self.password_input.text()

        if not password:
            QMessageBox.warning(self, "Fehler", "Bitte gib das Master-Passwort ein.")
            return

        self.verify_master_password(password)

    def verify_master_password(self, password: str):
        """
        Überprüft das eingegebene Master-Passwort

        Args:
            password: Das eingegebene Passwort
        """
        try:
            # Versuche Datenbank mit Passwort zu öffnen
            db_manager = DatabaseManager(self.db_path, password)

            # Hole Master-Passwort Hash aus Datenbank
            stored_hash = db_manager.get_master_password_hash()

            if stored_hash is None:
                # Keine Hash vorhanden - erste Verwendung nach Erstellung
                # Speichere Hash
                password_hash = master_password_manager.hash_password(password)
                db_manager.save_master_password_hash(password_hash)

            else:
                # Verifiziere Passwort
                if not master_password_manager.verify_password(password, stored_hash):
                    db_manager.close()
                    raise ValueError("Falsches Passwort")

            # Prüfe ob 2FA aktiviert ist
            if db_manager.has_totp_enabled():
                encrypted_secret = db_manager.get_totp_secret()
                if encrypted_secret:
                    # Entschlüssle Secret
                    totp_secret = totp_manager.decrypt_secret(encrypted_secret)

                    # Schließe temporäre Verbindung vor Dialog
                    db_manager.close()

                    # Fordere TOTP-Code vom Benutzer
                    totp_code, ok = QInputDialog.getText(
                        self,
                        "Zwei-Faktor-Authentifizierung",
                        "Gib den 6-stelligen Code aus deiner\nAuthenticator-App ein:",
                        QLineEdit.EchoMode.Normal
                    )

                    if not ok or not totp_code:
                        # Benutzer hat abgebrochen
                        return

                    # Verifiziere TOTP-Code
                    if not totp_manager.verify_code(totp_secret, totp_code.strip()):
                        QMessageBox.warning(
                            self,
                            "Fehler",
                            "Ungültiger 2FA-Code. Bitte versuche es erneut."
                        )
                        self.password_input.clear()
                        return

                    # 2FA erfolgreich
            else:
                # Kein 2FA - schließe Verbindung
                db_manager.close()

            # Setze Encryption Manager
            encryption_manager.set_master_password(password)

            # Speichere Passwort für Hauptfenster
            self.master_password = password

            self.login_successful.emit(password)
            self.accept()

        except ValueError as e:
            QMessageBox.warning(
                self,
                "Fehler",
                "Falsches Master-Passwort."
            )
            self.password_input.clear()
            self.password_input.setFocus()
            animator.shake(self.password_input, 10, 50, 3)

        except Exception as e:
            QMessageBox.critical(
                self,
                "Fehler",
                f"Fehler beim Öffnen der Datenbank:\n{str(e)}"
            )
            self.reject()

    def get_master_password(self) -> str:
        """Gibt das eingegebene Master-Passwort zurück"""
        return self.master_password
