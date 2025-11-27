# Contributing to SecurePass Manager

Thank you for your interest in contributing to SecurePass Manager! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Maintain a professional environment

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- pip (Python package manager)

### Setting Up Development Environment

1. Clone the repository
```bash
git clone <repository-url>
cd PasswortManager
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run tests to verify setup
```bash
pytest
```

4. Run the application
```bash
python main.py
```

## Development Workflow

### 1. Choose a Feature or Fix

- Check existing issues or feature branches in `FEATURES.md`
- Create a new issue to discuss major changes
- Comment on an issue to claim it

### 2. Create a Branch

Branch naming conventions:
- `feature/feature-name` - New features
- `bugfix/bug-description` - Bug fixes
- `hotfix/critical-fix` - Urgent production fixes
- `refactor/what-refactoring` - Code refactoring
- `docs/what-documenting` - Documentation updates
- `test/what-testing` - Test additions

```bash
git checkout main
git pull origin main
git checkout -b feature/your-feature-name
```

### 3. Make Changes

- Write clean, readable code
- Follow PEP 8 style guidelines
- Add docstrings to functions and classes
- Keep commits focused and atomic
- Write meaningful commit messages

### 4. Write Tests

- Add unit tests for new functionality
- Ensure all tests pass: `pytest`
- Aim for high code coverage: `pytest --cov=src`
- Test edge cases and error conditions

### 5. Update Documentation

- Update README.md if needed
- Add docstrings to new code
- Update FEATURES.md for feature work
- Include usage examples where appropriate

### 6. Commit Changes

Write clear, descriptive commit messages:

```bash
git add <files>
git commit -m "Add feature: brief description

Longer description explaining what and why, not how.
Include any breaking changes or migration notes.

Fixes #issue-number"
```

### 7. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub with:
- Clear title and description
- Reference to related issues
- Screenshots for UI changes
- List of changes made

## Code Style Guidelines

### Python Style

- Follow PEP 8
- Use 4 spaces for indentation
- Maximum line length: 100 characters
- Use type hints where appropriate
- Use meaningful variable names

### Code Organization

```python
"""
Module description

Longer description if needed.
"""
import standard_library
import third_party_libraries
from local_modules import something


class MyClass:
    """Class description"""

    def __init__(self):
        """Initialize the class"""
        pass

    def public_method(self):
        """Public method description"""
        pass

    def _private_method(self):
        """Private method description"""
        pass
```

### GUI Code

- Separate UI setup from business logic
- Use theme colors from `themes.py`
- Make UI responsive
- Add tooltips for user guidance
- Handle errors gracefully with user-friendly messages

### Database Code

- Use parameterized queries to prevent SQL injection
- Close connections properly
- Handle database errors
- Use transactions for multiple operations

### Security Code

- Never log sensitive data
- Use encryption for all sensitive storage
- Follow principle of least privilege
- Validate all user input
- Use secure random number generation

## Testing Guidelines

### Writing Tests

```python
import unittest
from src.module import MyClass


class TestMyClass(unittest.TestCase):
    """Tests for MyClass"""

    def setUp(self):
        """Set up test fixtures"""
        self.instance = MyClass()

    def tearDown(self):
        """Clean up after tests"""
        pass

    def test_something(self):
        """Test description"""
        result = self.instance.do_something()
        self.assertEqual(result, expected_value)
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_encryption.py

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test
pytest tests/test_encryption.py::TestEncryption::test_encrypt_decrypt
```

## Commit Message Guidelines

### Format

```
Type: Brief description (50 chars or less)

More detailed explanation if necessary. Wrap at 72 characters.
Explain what and why, not how.

- Bullet points are okay
- Use present tense: "Add feature" not "Added feature"
- Reference issues: "Fixes #123" or "Relates to #456"
```

### Types

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, etc.)
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

### Examples

Good commit messages:
```
feat: Add TOTP support for 2FA codes

Implements Time-based One-Time Password generation using pyotp.
Users can now store TOTP secrets and generate 6-digit codes.

Fixes #42
```

```
fix: Correct password strength calculation

The strength checker was not properly weighing character diversity.
Updated algorithm to better reflect actual password security.
```

Bad commit messages:
```
fixed stuff
```

```
updated files
```

## Pull Request Guidelines

### Before Submitting

- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] No merge conflicts with main
- [ ] Commit history is clean

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe testing done

## Screenshots (if applicable)
Add screenshots for UI changes

## Checklist
- [ ] Tests pass
- [ ] Documentation updated
- [ ] Code follows style guide
- [ ] No breaking changes (or documented)

## Related Issues
Fixes #issue-number
```

## Security Considerations

### Reporting Security Issues

**Do not open public issues for security vulnerabilities.**

Instead, email security concerns to [security email] with:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### Security Best Practices

- Never commit secrets or passwords
- Use environment variables for sensitive config
- Validate and sanitize all input
- Use prepared statements for database queries
- Keep dependencies updated
- Follow OWASP guidelines

## Getting Help

- Check existing documentation
- Search closed issues
- Ask in discussions
- Create a new issue with details

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Release notes
- Project documentation

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

---

Thank you for contributing to SecurePass Manager! 🔐
