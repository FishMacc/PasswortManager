"""
Login-Dialog für Master-Passwort
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QColor
from ..auth.master_password import master_password_manager
from ..core.database import DatabaseManager
from ..core.encryption import encryption_manager
from .themes import theme


class LoginDialog(QDialog):
    """Dialog für Login mit Master-Passwort"""

    # Signal wird emittiert, wenn Login erfolgreich war
    login_successful = pyqtSignal()

    def __init__(self, db_manager: DatabaseManager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.is_first_time = not db_manager.has_master_password()
        self.setup_ui()

    def setup_ui(self):
        """Erstellt das UI des Login-Dialogs"""
        self.setWindowTitle("SecurePass Manager")
        self.setModal(True)
        self.setFixedSize(450, 350)

        # Modernes Design
        c = theme.get_colors()

        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)

        # Logo/Icon Bereich
        icon_label = QLabel("🔐")
        icon_font = QFont()
        icon_font.setPointSize(48)
        icon_label.setFont(icon_font)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon_label)

        # Titel
        title = QLabel("SecurePass Manager")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"color: {c['primary']}; margin-bottom: 10px;")
        layout.addWidget(title)

        # Untertitel
        if self.is_first_time:
            subtitle = QLabel("Erstelle dein Master-Passwort")
        else:
            subtitle = QLabel("Willkommen zurück")

        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet(f"color: {c['text_secondary']}; font-size: 14px; margin-bottom: 20px;")
        layout.addWidget(subtitle)

        # Passwort-Feld
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Master-Passwort eingeben...")
        self.password_input.setMinimumHeight(45)
        self.password_input.returnPressed.connect(self.handle_login)
        layout.addWidget(self.password_input)

        # Bestätigungs-Feld (nur beim ersten Mal)
        if self.is_first_time:
            self.confirm_input = QLineEdit()
            self.confirm_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.confirm_input.setPlaceholderText("Passwort bestätigen...")
            self.confirm_input.setMinimumHeight(45)
            self.confirm_input.returnPressed.connect(self.handle_login)
            layout.addWidget(self.confirm_input)

            # Hinweis
            hint = QLabel("⚠️ Dieses Passwort kann nicht wiederhergestellt werden!")
            hint.setWordWrap(True)
            hint.setStyleSheet(f"""
                color: {c['danger']};
                background-color: {c['background_tertiary']};
                padding: 12px;
                border-radius: 8px;
                font-size: 12px;
            """)
            layout.addWidget(hint)

        layout.addStretch()

        # Buttons
        self.login_button = QPushButton("Erstellen" if self.is_first_time else "Anmelden")
        self.login_button.setMinimumHeight(45)
        self.login_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.login_button.clicked.connect(self.handle_login)
        self.login_button.setStyleSheet(f"""
            QPushButton {{
                font-size: 15px;
                font-weight: 600;
                background-color: {c['primary']};
            }}
            QPushButton:hover {{
                background-color: {c['primary_hover']};
            }}
        """)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

        # Schatten-Effekt für moderneren Look
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 60))
        shadow.setOffset(0, 5)
        self.setGraphicsEffect(shadow)

        # Fokus auf Passwort-Feld
        self.password_input.setFocus()

    def handle_login(self):
        """Behandelt den Login-Versuch"""
        password = self.password_input.text()

        if not password:
            QMessageBox.warning(self, "Fehler", "Bitte gib ein Passwort ein.")
            return

        if self.is_first_time:
            # Neues Master-Passwort erstellen
            self.create_master_password(password)
        else:
            # Mit bestehendem Master-Passwort anmelden
            self.verify_master_password(password)

    def create_master_password(self, password: str):
        """
        Erstellt ein neues Master-Passwort

        Args:
            password: Das neue Master-Passwort
        """
        confirm = self.confirm_input.text()

        # Validierung
        if len(password) < 8:
            QMessageBox.warning(
                self,
                "Schwaches Passwort",
                "Das Master-Passwort muss mindestens 8 Zeichen lang sein."
            )
            return

        if password != confirm:
            QMessageBox.warning(
                self,
                "Fehler",
                "Die Passwörter stimmen nicht überein."
            )
            return

        # Passwort hashen und speichern
        try:
            password_hash = master_password_manager.hash_password(password)
            self.db_manager.save_master_password_hash(password_hash)

            # Encryption Manager initialisieren
            encryption_manager.set_master_password(password)

            QMessageBox.information(
                self,
                "Erfolg",
                "Master-Passwort wurde erfolgreich erstellt!"
            )

            self.login_successful.emit()
            self.accept()

        except Exception as e:
            QMessageBox.critical(
                self,
                "Fehler",
                f"Fehler beim Erstellen des Master-Passworts: {str(e)}"
            )

    def verify_master_password(self, password: str):
        """
        Überprüft das eingegebene Master-Passwort

        Args:
            password: Das eingegebene Passwort
        """
        try:
            stored_hash = self.db_manager.get_master_password_hash()

            if stored_hash is None:
                QMessageBox.critical(
                    self,
                    "Fehler",
                    "Kein Master-Passwort in der Datenbank gefunden."
                )
                return

            # Passwort verifizieren
            if master_password_manager.verify_password(password, stored_hash):
                # Encryption Manager initialisieren
                encryption_manager.set_master_password(password)

                self.login_successful.emit()
                self.accept()
            else:
                QMessageBox.warning(
                    self,
                    "Fehler",
                    "Falsches Master-Passwort."
                )
                self.password_input.clear()
                self.password_input.setFocus()

        except Exception as e:
            QMessageBox.critical(
                self,
                "Fehler",
                f"Fehler beim Überprüfen des Passworts: {str(e)}"
            )
