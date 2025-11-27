"""
Tests for master password hashing module
"""
import unittest
from src.auth.master_password import MasterPasswordManager


class TestMasterPassword(unittest.TestCase):
    """Tests for master password functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.manager = MasterPasswordManager()
        self.test_password = "MySecureMasterPassword123!"

    def test_hash_password(self):
        """Test password hashing"""
        password_hash = self.manager.hash_password(self.test_password)

        # Hash should not be empty
        self.assertIsNotNone(password_hash)
        self.assertGreater(len(password_hash), 0)

        # Hash should not equal the password
        self.assertNotEqual(password_hash, self.test_password)

    def test_verify_correct_password(self):
        """Test verifying correct password"""
        password_hash = self.manager.hash_password(self.test_password)
        is_valid = self.manager.verify_password(self.test_password, password_hash)

        self.assertTrue(is_valid)

    def test_verify_incorrect_password(self):
        """Test verifying incorrect password"""
        password_hash = self.manager.hash_password(self.test_password)
        is_valid = self.manager.verify_password("WrongPassword", password_hash)

        self.assertFalse(is_valid)

    def test_different_passwords_produce_different_hashes(self):
        """Test that different passwords produce different hashes"""
        hash1 = self.manager.hash_password("password1")
        hash2 = self.manager.hash_password("password2")

        self.assertNotEqual(hash1, hash2)

    def test_same_password_produces_different_hashes(self):
        """Test that same password produces different hashes due to salt"""
        hash1 = self.manager.hash_password(self.test_password)
        hash2 = self.manager.hash_password(self.test_password)

        # Due to random salt, hashes should be different
        self.assertNotEqual(hash1, hash2)

        # But both should verify correctly
        self.assertTrue(self.manager.verify_password(self.test_password, hash1))
        self.assertTrue(self.manager.verify_password(self.test_password, hash2))

    def test_hash_empty_password(self):
        """Test hashing empty password"""
        password_hash = self.manager.hash_password("")
        self.assertIsNotNone(password_hash)
        self.assertTrue(self.manager.verify_password("", password_hash))

    def test_hash_unicode_password(self):
        """Test hashing password with unicode characters"""
        unicode_password = "Pässwörd123!🔐"
        password_hash = self.manager.hash_password(unicode_password)

        self.assertTrue(self.manager.verify_password(unicode_password, password_hash))
        self.assertFalse(self.manager.verify_password("Password123!", password_hash))

    def test_verify_with_invalid_hash(self):
        """Test verifying with invalid hash format"""
        with self.assertRaises(Exception):
            self.manager.verify_password(self.test_password, "invalid_hash_format")


if __name__ == '__main__':
    unittest.main()
