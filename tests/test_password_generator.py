"""
Tests for password generator module
"""
import unittest
from src.password.generator import PasswordGenerator


class TestPasswordGenerator(unittest.TestCase):
    """Tests for password generation functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.generator = PasswordGenerator()

    def test_generate_default_password(self):
        """Test generating password with default options"""
        password = self.generator.generate(16)
        self.assertEqual(len(password), 16)

    def test_generate_various_lengths(self):
        """Test generating passwords of various lengths"""
        for length in [8, 12, 16, 24, 32, 64]:
            password = self.generator.generate(length)
            self.assertEqual(len(password), length)

    def test_generate_with_uppercase_only(self):
        """Test generating password with uppercase only"""
        options = {
            "uppercase": True,
            "lowercase": False,
            "digits": False,
            "special": False
        }
        password = self.generator.generate(20, options)
        self.assertTrue(all(c.isupper() or c.isalpha() for c in password))
        self.assertTrue(any(c.isupper() for c in password))

    def test_generate_with_lowercase_only(self):
        """Test generating password with lowercase only"""
        options = {
            "uppercase": False,
            "lowercase": True,
            "digits": False,
            "special": False
        }
        password = self.generator.generate(20, options)
        self.assertTrue(all(c.islower() or c.isalpha() for c in password))
        self.assertTrue(any(c.islower() for c in password))

    def test_generate_with_digits_only(self):
        """Test generating password with digits only"""
        options = {
            "uppercase": False,
            "lowercase": False,
            "digits": True,
            "special": False
        }
        password = self.generator.generate(20, options)
        self.assertTrue(all(c.isdigit() for c in password))

    def test_generate_with_all_options(self):
        """Test generating password with all character types"""
        options = {
            "uppercase": True,
            "lowercase": True,
            "digits": True,
            "special": True
        }
        password = self.generator.generate(50, options)
        self.assertEqual(len(password), 50)

        # Check that password contains at least one of each type
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(not c.isalnum() for c in password)

        self.assertTrue(has_upper, "Password should contain uppercase")
        self.assertTrue(has_lower, "Password should contain lowercase")
        self.assertTrue(has_digit, "Password should contain digits")
        self.assertTrue(has_special, "Password should contain special characters")

    def test_generate_minimum_length(self):
        """Test generating password with minimum length"""
        password = self.generator.generate(8)
        self.assertEqual(len(password), 8)

    def test_generate_maximum_length(self):
        """Test generating password with maximum length"""
        password = self.generator.generate(64)
        self.assertEqual(len(password), 64)

    def test_generate_randomness(self):
        """Test that generated passwords are different"""
        passwords = [self.generator.generate(16) for _ in range(10)]
        # All passwords should be unique
        self.assertEqual(len(passwords), len(set(passwords)))

    def test_generate_no_options_raises_error(self):
        """Test that generating with no options raises error"""
        options = {
            "uppercase": False,
            "lowercase": False,
            "digits": False,
            "special": False
        }
        with self.assertRaises(ValueError):
            self.generator.generate(16, options)


if __name__ == '__main__':
    unittest.main()
