# Tests

This directory contains unit tests for the SecurePass Manager application.

## Running Tests

### Run all tests
```bash
pytest
```

### Run tests with coverage
```bash
pytest --cov=src --cov-report=html
```

### Run specific test file
```bash
pytest tests/test_encryption.py
```

### Run specific test
```bash
pytest tests/test_encryption.py::TestEncryption::test_encrypt_decrypt
```

## Test Structure

- `test_encryption.py` - Tests for encryption/decryption functionality
- `test_password_generator.py` - Tests for password generation
- `test_password_strength.py` - Tests for password strength checking
- `test_master_password.py` - Tests for master password hashing
- `test_database.py` - Tests for database operations

## Test Coverage

The tests cover:
- Encryption and decryption with different inputs
- Password generation with various options
- Password strength evaluation
- Master password hashing and verification
- Database CRUD operations
- Search functionality
- Category management
