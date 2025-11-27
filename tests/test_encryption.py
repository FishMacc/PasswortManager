"""
Tests for encryption module
"""
import unittest
from src.core.encryption import EncryptionManager


class TestEncryption(unittest.TestCase):
    """Tests for encryption functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.encryption_manager = EncryptionManager()
        self.test_password = "TestMasterPassword123!"

    def test_set_master_password(self):
        """Test setting master password"""
        self.encryption_manager.set_master_password(self.test_password)
        self.assertIsNotNone(self.encryption_manager.key)

    def test_encrypt_decrypt(self):
        """Test encryption and decryption"""
        self.encryption_manager.set_master_password(self.test_password)

        plaintext = "MySecretPassword123"
        encrypted = self.encryption_manager.encrypt(plaintext)

        # Encrypted should be different from plaintext
        self.assertNotEqual(plaintext, encrypted)

        # Decrypted should match plaintext
        decrypted = self.encryption_manager.decrypt(encrypted)
        self.assertEqual(plaintext, decrypted)

    def test_encrypt_empty_string(self):
        """Test encrypting empty string"""
        self.encryption_manager.set_master_password(self.test_password)

        encrypted = self.encryption_manager.encrypt("")
        decrypted = self.encryption_manager.decrypt(encrypted)
        self.assertEqual("", decrypted)

    def test_encrypt_unicode(self):
        """Test encrypting unicode characters"""
        self.encryption_manager.set_master_password(self.test_password)

        plaintext = "🔐 Passwort mit Émojis & Ümlautë"
        encrypted = self.encryption_manager.encrypt(plaintext)
        decrypted = self.encryption_manager.decrypt(encrypted)
        self.assertEqual(plaintext, decrypted)

    def test_clear_key(self):
        """Test clearing encryption key"""
        self.encryption_manager.set_master_password(self.test_password)
        self.assertIsNotNone(self.encryption_manager.key)

        self.encryption_manager.clear()
        self.assertIsNone(self.encryption_manager.key)

    def test_encrypt_without_key_raises_error(self):
        """Test that encrypting without key raises error"""
        with self.assertRaises(Exception):
            self.encryption_manager.encrypt("test")

    def test_decrypt_without_key_raises_error(self):
        """Test that decrypting without key raises error"""
        with self.assertRaises(Exception):
            self.encryption_manager.decrypt("test")

    def test_different_passwords_produce_different_keys(self):
        """Test that different master passwords produce different encrypted results"""
        plaintext = "TestPassword"

        self.encryption_manager.set_master_password("password1")
        encrypted1 = self.encryption_manager.encrypt(plaintext)

        self.encryption_manager.set_master_password("password2")
        encrypted2 = self.encryption_manager.encrypt(plaintext)

        # Different master passwords should produce different encrypted texts
        self.assertNotEqual(encrypted1, encrypted2)


if __name__ == '__main__':
    unittest.main()
