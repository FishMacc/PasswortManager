"""
Tests for database module
"""
import unittest
import os
import tempfile
from src.core.database import DatabaseManager
from src.core.models import PasswordEntry, Category
from src.core.encryption import EncryptionManager


class TestDatabase(unittest.TestCase):
    """Tests for database functionality"""

    def setUp(self):
        """Set up test fixtures"""
        # Create temporary database file
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()

        self.db_manager = DatabaseManager(self.temp_db.name)

        # Setup encryption for testing
        self.encryption = EncryptionManager()
        self.encryption.set_master_password("TestMasterPassword123!")

    def tearDown(self):
        """Clean up test fixtures"""
        # Close database connection
        if hasattr(self, 'db_manager'):
            self.db_manager.close()

        # Delete temporary database file
        if os.path.exists(self.temp_db.name):
            os.remove(self.temp_db.name)

    def test_create_tables(self):
        """Test that tables are created"""
        # Tables should be created in __init__
        categories = self.db_manager.get_all_categories()
        self.assertIsNotNone(categories)

    def test_add_category(self):
        """Test adding a category"""
        category_id = self.db_manager.add_category("Test Category")
        self.assertIsNotNone(category_id)
        self.assertGreater(category_id, 0)

    def test_get_all_categories(self):
        """Test getting all categories"""
        # Should have default categories
        categories = self.db_manager.get_all_categories()
        self.assertGreater(len(categories), 0)

        # Add new category
        self.db_manager.add_category("New Category")
        categories = self.db_manager.get_all_categories()

        # Check that new category exists
        self.assertTrue(any(cat.name == "New Category" for cat in categories))

    def test_add_password_entry(self):
        """Test adding a password entry"""
        # Get a category
        categories = self.db_manager.get_all_categories()
        category_id = categories[0].id

        # Create entry
        entry = PasswordEntry(
            id=None,
            category_id=category_id,
            name="Test Entry",
            username="testuser",
            encrypted_password=self.encryption.encrypt("testpass123"),
            encrypted_notes=self.encryption.encrypt("Test notes"),
            website_url="https://test.com"
        )

        entry_id = self.db_manager.add_password_entry(entry)
        self.assertIsNotNone(entry_id)
        self.assertGreater(entry_id, 0)

    def test_get_password_entry(self):
        """Test getting a password entry"""
        # Add entry
        categories = self.db_manager.get_all_categories()
        category_id = categories[0].id

        entry = PasswordEntry(
            id=None,
            category_id=category_id,
            name="Test Entry",
            username="testuser",
            encrypted_password=self.encryption.encrypt("testpass123"),
            encrypted_notes=None,
            website_url="https://test.com"
        )

        entry_id = self.db_manager.add_password_entry(entry)

        # Get entry
        retrieved_entry = self.db_manager.get_password_entry(entry_id)
        self.assertIsNotNone(retrieved_entry)
        self.assertEqual(retrieved_entry.name, "Test Entry")
        self.assertEqual(retrieved_entry.username, "testuser")

    def test_update_password_entry(self):
        """Test updating a password entry"""
        # Add entry
        categories = self.db_manager.get_all_categories()
        category_id = categories[0].id

        entry = PasswordEntry(
            id=None,
            category_id=category_id,
            name="Original Name",
            username="testuser",
            encrypted_password=self.encryption.encrypt("testpass123"),
            encrypted_notes=None,
            website_url="https://test.com"
        )

        entry_id = self.db_manager.add_password_entry(entry)
        entry.id = entry_id

        # Update entry
        entry.name = "Updated Name"
        entry.username = "newuser"
        self.db_manager.update_password_entry(entry)

        # Get updated entry
        updated_entry = self.db_manager.get_password_entry(entry_id)
        self.assertEqual(updated_entry.name, "Updated Name")
        self.assertEqual(updated_entry.username, "newuser")

    def test_delete_password_entry(self):
        """Test deleting a password entry"""
        # Add entry
        categories = self.db_manager.get_all_categories()
        category_id = categories[0].id

        entry = PasswordEntry(
            id=None,
            category_id=category_id,
            name="Test Entry",
            username="testuser",
            encrypted_password=self.encryption.encrypt("testpass123"),
            encrypted_notes=None,
            website_url="https://test.com"
        )

        entry_id = self.db_manager.add_password_entry(entry)

        # Delete entry
        self.db_manager.delete_password_entry(entry_id)

        # Entry should not exist
        deleted_entry = self.db_manager.get_password_entry(entry_id)
        self.assertIsNone(deleted_entry)

    def test_get_password_entries_by_category(self):
        """Test getting entries by category"""
        categories = self.db_manager.get_all_categories()
        category_id = categories[0].id

        # Add multiple entries
        for i in range(3):
            entry = PasswordEntry(
                id=None,
                category_id=category_id,
                name=f"Entry {i}",
                username="testuser",
                encrypted_password=self.encryption.encrypt("testpass123"),
                encrypted_notes=None,
                website_url="https://test.com"
            )
            self.db_manager.add_password_entry(entry)

        # Get entries by category
        entries = self.db_manager.get_password_entries_by_category(category_id)
        self.assertGreaterEqual(len(entries), 3)

    def test_search_password_entries(self):
        """Test searching password entries"""
        categories = self.db_manager.get_all_categories()
        category_id = categories[0].id

        # Add entries
        entry1 = PasswordEntry(
            id=None,
            category_id=category_id,
            name="Gmail Account",
            username="user@gmail.com",
            encrypted_password=self.encryption.encrypt("testpass123"),
            encrypted_notes=None,
            website_url="https://gmail.com"
        )
        self.db_manager.add_password_entry(entry1)

        entry2 = PasswordEntry(
            id=None,
            category_id=category_id,
            name="Facebook Account",
            username="user@example.com",
            encrypted_password=self.encryption.encrypt("testpass123"),
            encrypted_notes=None,
            website_url="https://facebook.com"
        )
        self.db_manager.add_password_entry(entry2)

        # Search by name
        results = self.db_manager.search_password_entries("Gmail")
        self.assertGreater(len(results), 0)
        self.assertTrue(any(e.name == "Gmail Account" for e in results))

        # Search by username
        results = self.db_manager.search_password_entries("gmail.com")
        self.assertGreater(len(results), 0)

    def test_master_password_storage(self):
        """Test master password hash storage"""
        # Should not have master password initially
        self.assertFalse(self.db_manager.has_master_password())

        # Save master password hash
        test_hash = "test_hash_value"
        self.db_manager.save_master_password_hash(test_hash)

        # Should have master password now
        self.assertTrue(self.db_manager.has_master_password())

        # Retrieved hash should match
        retrieved_hash = self.db_manager.get_master_password_hash()
        self.assertEqual(retrieved_hash, test_hash)


if __name__ == '__main__':
    unittest.main()
