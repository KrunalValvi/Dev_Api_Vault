# Contributing to Dev API Vault

Thank you for your interest in contributing to Dev API Vault! This document provides guidelines and information for contributors.

## 🚀 Quick Start for Contributors

1. **Fork** the repository
2. **Clone** your fork locally
3. **Create** a new branch for your feature
4. **Make** your changes
5. **Test** your changes
6. **Submit** a pull request

## 📋 Development Setup

### Prerequisites
- Python 3.9 or higher
- Git
- A code editor (VS Code recommended)

### Local Development Environment

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/Dev_Api_Vault.git
cd Dev_Api_Vault

# Set up virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies (including dev dependencies)
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

## 🎯 Types of Contributions

### 🐛 Bug Reports
- Use the bug report template
- Include steps to reproduce
- Provide system information
- Add relevant logs or screenshots

### 💡 Feature Requests
- Use the feature request template
- Explain the use case
- Provide examples if possible
- Consider implementation complexity

### 🔧 Code Contributions
- Follow the coding standards below
- Add tests for new features
- Update documentation
- Ensure all tests pass

## 📝 Coding Standards

### Python Code Style
- Follow **PEP 8** style guide
- Use **type hints** for all functions
- Maximum line length: **88 characters** (Black formatter)
- Use **meaningful variable names**

### Code Structure
```python
# Example function structure
from typing import Optional

def process_text(
    text: str, 
    max_length: Optional[int] = None
) -> dict[str, str]:
    """
    Process text input and return formatted result.
    
    Args:
        text: Input text to process
        max_length: Optional maximum length limit
        
    Returns:
        Dictionary containing processed text and metadata
        
    Raises:
        ValueError: If text is empty or invalid
    """
    if not text.strip():
        raise ValueError("Text cannot be empty")
    
    # Implementation here
    return {"processed_text": text, "length": len(text)}
```

### API Design Guidelines
- Use **RESTful conventions**
- Include **comprehensive error handling**
- Provide **clear response schemas**
- Add **input validation**

## 🧪 Testing Requirements

### Test Coverage
- Maintain **90%+ test coverage**
- Test both **success and error cases**
- Include **integration tests** for APIs

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test categories
pytest -m "unit"        # Unit tests only
pytest -m "integration" # Integration tests only
```

### Writing Tests
```python
# Example test structure
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_qr_code_generation():
    """Test QR code generation with valid input."""
    response = client.post(
        "/qr-code",
        json={"text": "Hello World"}
    )
    assert response.status_code == 200
    assert "qr_code_base64" in response.json()

def test_qr_code_empty_text():
    """Test QR code generation with empty text."""
    response = client.post(
        "/qr-code",
        json={"text": ""}
    )
    assert response.status_code == 422
```

## 📖 Documentation Guidelines

### Code Documentation
- Add **docstrings** to all functions and classes
- Use **Google-style docstrings**
- Include **type hints**
- Document **complex algorithms**

### API Documentation
- Update **OpenAPI schemas** for new endpoints
- Add **example requests/responses**
- Include **error code documentation**

## 🔄 Pull Request Process

### Before Submitting
- [ ] All tests pass locally
- [ ] Code follows style guidelines
- [ ] Documentation is updated
- [ ] No merge conflicts with main branch

### PR Template
- Use the provided PR template
- Link related issues
- Describe changes clearly
- Include screenshots for UI changes

### Review Process
1. **Automated checks** must pass
2. **Code review** by maintainers
3. **Testing** in staging environment
4. **Approval** and merge

## 🏷️ Commit Message Format

Use **Conventional Commits** format:

```
type(scope): description

feat(api): add text summarization endpoint
fix(qr): handle empty string input gracefully
docs(readme): update installation instructions
test(regex): add edge case tests
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Adding or updating tests
- `refactor`: Code refactoring
- `style`: Formatting changes
- `ci`: CI/CD changes

## 🚨 Security Guidelines

### Reporting Security Issues
- **DO NOT** open public issues for security vulnerabilities
- Email security issues to: [security@yourproject.com]
- Include detailed steps to reproduce
- Allow reasonable time for fixes before disclosure

### Secure Coding Practices
- **Validate all inputs**
- **Sanitize user data**
- **Use parameterized queries**
- **Implement proper authentication**
- **Follow OWASP guidelines**

## 🎖️ Recognition

Contributors are recognized in:
- **README.md** contributors section
- **CHANGELOG.md** release notes
- **GitHub releases** acknowledgments

## 📞 Getting Help

- **GitHub Discussions** for general questions
- **GitHub Issues** for bugs and features
- **Discord/Slack** for real-time chat (if available)

## 📄 Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you agree to uphold this code.

---

Thank you for contributing to Dev API Vault! 🙏
