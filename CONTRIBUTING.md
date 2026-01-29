# Contributing to SlideSense

Thank you for your interest in contributing to SlideSense! This document provides guidelines for contributing to the project.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and collaborative environment.

## How to Contribute

### Reporting Bugs

1. **Check existing issues** to avoid duplicates
2. **Use the bug report template** when creating an issue
3. **Include detailed information**:
   - Python version
   - Operating system
   - Steps to reproduce
   - Expected vs actual behavior
   - Error messages/logs

### Suggesting Enhancements

1. **Check existing feature requests**
2. **Clearly describe the enhancement**
3. **Explain why it would be useful**
4. **Provide examples if possible**

### Pull Requests

#### Before You Start

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Set up development environment**
   ```bash
   pip install -r requirements.txt
   ```

#### Development Guidelines

**Code Quality**
- Follow PEP 8 style guidelines
- Add type hints to all functions
- Write docstrings for public functions
- Keep functions focused and small

**Testing**
- Write tests for new features
- Ensure all existing tests pass
- Aim for 80%+ code coverage
- Run tests before committing:
  ```bash
  python -m pytest tests/ -v
  ```

**Type Checking**
- Run mypy on changed files:
  ```bash
  python -m mypy your_file.py
  ```

**Documentation**
- Update README.md if needed
- Add docstrings to new functions
- Update CHANGELOG.md

#### Commit Messages

Use clear, descriptive commit messages:

```
type(scope): Brief description

Detailed explanation if needed

- Bullet points for changes
- Reference issues: #123
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Examples:
```
feat(voice): Add support for custom commands
fix(detector): Resolve fuzzy matching edge case
docs(readme): Update installation instructions
test(utils): Add tests for device management
```

#### Pull Request Process

1. **Update tests** - All tests must pass
2. **Update documentation** - Reflect your changes
3. **Run quality checks**:
   ```bash
   # Run tests
   python -m pytest tests/ -v
   
   # Check types
   python -m mypy main2.py utils.py
   
   # Check coverage
   python -m pytest tests/ --cov=. --cov-report=html
   ```

4. **Create pull request**:
   - Use clear title and description
   - Link related issues
   - Describe changes and rationale
   - Add screenshots for UI changes

5. **Address review feedback**
   - Respond to all comments
   - Make requested changes
   - Push updates to same branch

## Development Setup

### Prerequisites
- Python 3.8+
- Git
- Virtual environment (recommended)

### Setup Steps

1. **Clone your fork**
   ```bash
   git clone https://github.com/yourusername/slidesense.git
   cd slidesense
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run tests**
   ```bash
   python -m pytest tests/ -v
   ```

5. **Start developing!**

## Project Structure

```
slidesense/
├── main2.py              # Main CLI application
├── gui_unified_app.py    # GUI application
├── voice_detector.py     # Command detection
├── utils.py              # Utility functions
├── config.py             # Configuration
├── logger.py             # Logging
├── exceptions.py         # Custom exceptions
├── tests/                # Test suite
└── docs/                 # Documentation
```

## Coding Standards

### Python Style Guide
- Follow PEP 8
- Use 4 spaces for indentation
- Maximum line length: 100 characters
- Use descriptive variable names

### Type Hints
```python
def function_name(param1: str, param2: int) -> bool:
    """Function description.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
    """
    pass
```

### Error Handling
```python
from exceptions import SlideSenseException

try:
    # Your code
    pass
except SpecificException as e:
    logger.error(f"Error: {e}")
    raise SlideSenseException("User-friendly message") from e
```

### Testing
```python
import pytest

class TestYourFeature:
    def test_specific_behavior(self):
        """Test description"""
        # Arrange
        input_data = "test"
        
        # Act
        result = function_under_test(input_data)
        
        # Assert
        assert result == expected_output
```

## Review Process

### What We Look For

1. **Functionality**: Does it work as intended?
2. **Tests**: Are there adequate tests?
3. **Code Quality**: Is it clean and maintainable?
4. **Documentation**: Is it well-documented?
5. **Performance**: Does it maintain/improve performance?

### Response Time

- Initial review: Within 48 hours
- Follow-up reviews: Within 24 hours
- Merge: After approval from maintainers

## Questions?

- Open an issue with the "question" label
- Join our discussions
- Check existing documentation

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Credited in release notes
- Recognized in project documentation

Thank you for contributing to SlideSense! 🎉
