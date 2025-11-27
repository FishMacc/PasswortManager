"""
Tests for password strength checker module
"""
import unittest
from src.password.strength import PasswordStrengthChecker, PasswordStrength


class TestPasswordStrength(unittest.TestCase):
    """Tests for password strength checking functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.checker = PasswordStrengthChecker()

    def test_weak_password_short(self):
        """Test that short passwords are weak"""
        strength = self.checker.check_strength("abc")
        self.assertEqual(strength, PasswordStrength.WEAK)

    def test_weak_password_only_lowercase(self):
        """Test that only lowercase passwords are weak"""
        strength = self.checker.check_strength("abcdefgh")
        self.assertEqual(strength, PasswordStrength.WEAK)

    def test_medium_password(self):
        """Test medium strength password"""
        strength = self.checker.check_strength("Abcdefgh123")
        self.assertIn(strength, [PasswordStrength.MEDIUM, PasswordStrength.STRONG])

    def test_strong_password(self):
        """Test strong password"""
        strength = self.checker.check_strength("Abcd123!@#XYZ")
        self.assertEqual(strength, PasswordStrength.STRONG)

    def test_very_strong_password(self):
        """Test very strong password"""
        strength = self.checker.check_strength("MyV3ry$tr0ng&C0mpl3x!P@ssw0rd")
        self.assertEqual(strength, PasswordStrength.STRONG)

    def test_empty_password(self):
        """Test empty password"""
        strength = self.checker.check_strength("")
        self.assertEqual(strength, PasswordStrength.WEAK)

    def test_strength_percentage_weak(self):
        """Test strength percentage for weak password"""
        percentage = self.checker.get_strength_percentage("abc")
        self.assertLess(percentage, 50)

    def test_strength_percentage_medium(self):
        """Test strength percentage for medium password"""
        percentage = self.checker.get_strength_percentage("Abcdef123")
        self.assertGreaterEqual(percentage, 30)

    def test_strength_percentage_strong(self):
        """Test strength percentage for strong password"""
        percentage = self.checker.get_strength_percentage("Abcd123!@#XYZ")
        self.assertGreater(percentage, 60)

    def test_password_with_all_character_types(self):
        """Test password containing all character types"""
        password = "Abc123!@#"
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(not c.isalnum() for c in password)

        self.assertTrue(has_upper)
        self.assertTrue(has_lower)
        self.assertTrue(has_digit)
        self.assertTrue(has_special)

        strength = self.checker.check_strength(password)
        self.assertIn(strength, [PasswordStrength.MEDIUM, PasswordStrength.STRONG])

    def test_long_password_is_stronger(self):
        """Test that longer passwords get higher scores"""
        short_password = "Abc123!@"
        long_password = "Abc123!@#XYZ456&*()_+ABC"

        short_percentage = self.checker.get_strength_percentage(short_password)
        long_percentage = self.checker.get_strength_percentage(long_password)

        self.assertGreater(long_percentage, short_percentage)


if __name__ == '__main__':
    unittest.main()
