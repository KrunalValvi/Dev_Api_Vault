<div align="center">

<div align="center">

# 🛠️ Dev API Vault
### *Your Swiss Army Knife for Developer Utilities*

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-00a393.svg?logo=fastapi)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Tests](https://github.com/KrunalValvi/Dev_Api_Vault/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/KrunalValvi/Dev_Api_Vault/actions)
[![codecov](https://codecov.io/gh/KrunalValvi/Dev_Api_Vault/graph/badge.svg?token=YOUR_TOKEN_HERE)](https://codecov.io/gh/KrunalValvi/Dev_Api_Vault)

[![Open in Dev Containers](https://img.shields.io/static/v1?label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/KrunalValvi/Dev_Api_Vault)
[![Open in GitHub Codespaces](https://img.shields.io/badge/GitHub_Codespaces-Open-blue?logo=github)](https://github.com/codespaces/new?hide_repo_select=true&ref=main&repo=KrunalValvi/Dev_Api_Vault)

</div>

## 🚀 Overview

Dev API Vault is a **production-ready** FastAPI application that consolidates essential developer utilities into a single, powerful API. It's designed to help developers streamline their workflow with commonly needed tools accessible via RESTful endpoints.

## ✨ Features

- **Markdown to HTML Converter** - Convert markdown text to clean HTML
- **QR Code Generator** - Generate QR codes from text or URLs
- **Image to Base64** - Convert images to base64 encoded strings
- **Regex Tester** - Test and validate regular expressions
- **Webpage Word Counter** - Count words from any webpage URL
- **Text Summarizer** - Generate concise summaries from large text blocks
- **RESTful API** - Easy-to-use endpoints with proper HTTP methods
- **Rate Limiting** - Built-in rate limiting for API protection
- **Comprehensive Documentation** - Interactive API docs with OpenAPI/Swagger
- **Production Ready** - Containerized with Docker and deployable anywhere

## 🎯 Use Cases

- Quickly generate QR codes for URLs or text
- Convert documentation from Markdown to HTML
- Process images in API workflows
- Test and debug regular expressions
- Analyze web content programmatically
- Summarize articles or documentation
- Educational purposes for learning FastAPI

## 🛠️ Tech Stack

- **Backend Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Language**: Python 3.9+
- **API Documentation**: OpenAPI (Swagger UI & ReDoc)
- **Testing**: Pytest, HTTPX
- **Code Quality**: Black, isort, Flake8, mypy
- **Containerization**: Docker
- **CI/CD**: GitHub Actions
- **Deployment**: Render (or any cloud provider)

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Git
- (Optional) Docker & Docker Compose

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/KrunalValvi/Dev_Api_Vault.git
   cd Dev_Api_Vault
   ```

2. **Set up a virtual environment**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

6. **Access the API documentation**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Using Docker

```bash
# Build the Docker image
docker build -t dev-api-vault .

# Run the container
docker run -d --name dev-api-vault -p 8000:80 dev-api-vault
```

## 📚 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/markdown-to-html` | POST | Convert markdown to HTML |
| `/api/v1/qr-code` | POST | Generate QR code from text |
| `/api/v1/image-to-base64` | POST | Convert image to base64 |
| `/api/v1/regex-tester` | POST | Test regular expressions |
| `/api/v1/word-count` | GET | Count words in a webpage |
| `/api/v1/summarize` | POST | Generate text summary |

For detailed API documentation, visit the interactive [Swagger UI](http://localhost:8000/docs) after starting the server.

## 🧪 Running Tests

```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Run with coverage
pytest --cov=app --cov-report=term-missing

# Run linters
black .
flake8
mypy .
```

## 📂 Project Structure

```
Dev_Api_Vault/
├── .github/                  # GitHub configuration
│   └── workflows/            # GitHub Actions workflows
├── app/                      # Application source code
│   ├── __init__.py           # Package initialization
│   ├── main.py               # FastAPI application
│   ├── config.py             # Configuration settings
│   ├── models.py             # Pydantic models
│   ├── routers.py            # API routes
│   ├── security.py           # Authentication & security
│   └── utils.py              # Utility functions
├── static/                   # Static files
├── tests/                    # Test files
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_api.py
│   └── test_edge_cases.py
├── .env.example              # Example environment variables
├── .gitignore                # Git ignore file
├── docker-compose.yml        # Docker Compose configuration
├── Dockerfile                # Docker configuration
├── pyproject.toml            # Project configuration
├── README.md                 # This file
└── requirements.txt          # Project dependencies
```

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📝 Changelog

See [CHANGELOG.md](CHANGELOG.md) for a list of notable changes.

## 📧 Contact

Krunal Valvi - [@krunalvalvi](https://twitter.com/krunalvalvi)

Project Link: [https://github.com/KrunalValvi/Dev_Api_Vault](https://github.com/KrunalValvi/Dev_Api_Vault)

## 🔍 Keywords

`fastapi`, `python`, `api`, `developer-tools`, `rest-api`, `markdown`, `qrcode`, `regex`, `text-processing`, `web-development`, `open-source`, `docker`, `github-actions`, `api-documentation`, `swagger`, `redoc`, `backend`, `web-services`, `automation`, `productivity-tools`, `devops`

---

<div align="center">
  Made with ❤️ by Krunal Valvi
</div>

[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-00a393?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.9+-blue?style=flat-square&logo=python)](https://python.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Deploy Status](https://img.shields.io/badge/Deploy-Live-brightgreen?style=flat-square)](https://dev-utility-api-vault.onrender.com)
[![Tests](https://img.shields.io/badge/Tests-Passing-success?style=flat-square)](#running-tests)
[![Code Coverage](https://img.shields.io/badge/Coverage-95%25-brightgreen?style=flat-square)](#testing--quality-assurance)

**🚀 [Live API](https://dev-utility-api-vault.onrender.com) | 📖 [Documentation](https://dev-utility-api-vault.onrender.com/docs) | 🐛 [Report Bug](https://github.com/KrunalValvi/Dev_Api_Vault/issues) | 💡 [Request Feature](https://github.com/KrunalValvi/Dev_Api_Vault/issues)**

</div>

---

## 📚 Additional Documentation

- **[Architecture Overview](ARCHITECTURE.md)** - System design and component details
- **[Contributing Guidelines](CONTRIBUTING.md)** - How to contribute to the project
- **[Development Guide](DEVELOPMENT.md)** - Local development setup
- **[API Reference](API_REFERENCE.md)** - Detailed endpoint documentation

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Quick Contribution Steps:
1. 🍴 Fork the repository
2. 🌿 Create a feature branch (`git checkout -b feature/amazing-feature`)
3. 💻 Make your changes
4. ✅ Add tests for new functionality
5. 🧪 Run the test suite (`pytest`)
6. 📝 Commit your changes (`git commit -m 'Add amazing feature'`)
7. 📤 Push to your branch (`git push origin feature/amazing-feature`)
8. 🔄 Open a Pull Request

---

## 🗺️ Roadmap

- [ ] **v1.1.0** - Authentication & API Keys
- [ ] **v1.2.0** - Rate limiting and usage analytics
- [ ] **v1.3.0** - Additional text processing utilities
- [ ] **v1.4.0** - WebSocket support for real-time operations
- [ ] **v2.0.0** - Machine learning-powered text analysis

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **FastAPI** team for the amazing framework
- **Python** community for excellent libraries
- **Contributors** who make this project better

---

## 📞 Support & Community

- 🐛 **Bug Reports:** [GitHub Issues](https://github.com/KrunalValvi/Dev_Api_Vault/issues)
- 💡 **Feature Requests:** [GitHub Issues](https://github.com/KrunalValvi/Dev_Api_Vault/issues)
- 💬 **Discussions:** [GitHub Discussions](https://github.com/KrunalValvi/Dev_Api_Vault/discussions)
- 📧 **Contact:** krunalvalvi05@gmail.com

---

<div align="center">

### ⭐ If this project helped you, please give it a star!

[![GitHub stars](https://img.shields.io/github/stars/KrunalValvi/Dev_Api_Vault?style=social)](https://github.com/KrunalValvi/Dev_Api_Vault/stargazers)

**Made with ❤️ by [KrunalValvi](https://github.com/KrunalValvi)**

</div>
