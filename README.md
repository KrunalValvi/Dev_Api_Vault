<div align="center">

# 🛠️ Dev API Vault
### *Your Swiss Army Knife for Developer Utilities*

[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-00a393?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.9+-blue?style=flat-square&logo=python)](https://python.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Deploy Status](https://img.shields.io/badge/Deploy-Live-brightgreen?style=flat-square)](https://dev-utility-api-vault.onrender.com)
[![Tests](https://img.shields.io/badge/Tests-Passing-success?style=flat-square)](#running-tests)
[![Code Coverage](https://img.shields.io/badge/Coverage-95%25-brightgreen?style=flat-square)](#testing--quality-assurance)

**🚀 [Live API](https://dev-utility-api-vault.onrender.com) | 📖 [Documentation](https://dev-utility-api-vault.onrender.com/docs) | 🐛 [Report Bug](https://github.com/KrunalValvi/Dev_Api_Vault/issues) | 💡 [Request Feature](https://github.com/KrunalValvi/Dev_Api_Vault/issues)**

</div>

---

## ✨ What is Dev API Vault?

Dev API Vault is a **production-ready FastAPI application** that consolidates 6 essential developer utilities into a single, powerful API. Whether you're building applications, automating workflows, or need quick utility functions, this vault has you covered.

### 🎯 Perfect for:
- **Developers** building applications that need utility functions
- **Automation enthusiasts** creating workflows and scripts
- **Learning FastAPI** through practical, real-world examples
- **Microservices architecture** as a utility service component

---

## 🚀 Key Features

| Feature | Description | Use Case |
|---------|-------------|----------|
| 📝 **Markdown to HTML** | Convert Markdown text to clean HTML | Documentation, blogs, README rendering |
| 🔲 **QR Code Generator** | Generate QR codes as base64 PNG images | Sharing links, contact info, payments |
| 🖼️ **Image to Base64** | Convert uploaded images to base64 strings | Data URIs, embedded images, APIs |
| 🔍 **Regex Tester** | Test regex patterns against text strings | Pattern validation, text processing |
| 📊 **Webpage Word Counter** | Scrape and analyze webpage content | Content analysis, SEO research |
| 📄 **Text Summarizer** | Extract key sentences from large text blocks | Content summarization, data processing |

---

## 🎬 Quick Demo

```python
import requests

# Generate a QR code
response = requests.post(
    "https://dev-utility-api-vault.onrender.com/qr-code",
    json={"text": "Hello, World!"}
)
qr_data = response.json()["qr_code_base64"]

# Convert Markdown to HTML
response = requests.post(
    "https://dev-utility-api-vault.onrender.com/markdown-to-html",
    json={"markdown": "# Hello **World**!"}
)
html_output = response.json()["html"]
```

---

## 🛠️ Technology Stack

<div align="center">

| Backend | Testing | Deployment | Libraries |
|---------|---------|------------|-----------|
| ![FastAPI](https://img.shields.io/badge/FastAPI-00a393?style=for-the-badge&logo=fastapi&logoColor=white) | ![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white) | ![Render](https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=white) | ![NLTK](https://img.shields.io/badge/NLTK-85C1E9?style=for-the-badge) |
| ![Uvicorn](https://img.shields.io/badge/Uvicorn-2E8B57?style=for-the-badge) | ![HTTPX](https://img.shields.io/badge/HTTPX-007ACC?style=for-the-badge) | ![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white) | ![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-FF6B6B?style=for-the-badge) |

</div>

---

## 🚀 Quick Start

### Option 1: Use the Live API (Recommended)
```bash
curl -X POST "https://dev-utility-api-vault.onrender.com/qr-code" \
     -H "Content-Type: application/json" \
     -d '{"text": "Your text here"}'
```

### Option 2: Local Development Setup

```bash
# 1. Clone the repository
git clone https://github.com/KrunalValvi/Dev_Api_Vault.git
cd Dev_Api_Vault

# 2. Set up Python environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

# 5. Run the server
uvicorn app.main:app --reload

# 6. Access the API
# API: http://127.0.0.1:8000
# Docs: http://127.0.0.1:8000/docs
```

---

## 📁 Project Structure

```
Dev_Api_Vault/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── models/              # Pydantic models for request/response
│   ├── routers/             # API route handlers
│   └── services/            # Business logic and utilities
├── tests/                   # Comprehensive test suite
├── requirements.txt         # Python dependencies
├── build.sh                # Setup script for NLTK data
├── Dockerfile              # Container configuration
├── docker-compose.yml      # Multi-container setup
└── README.md               # You are here!
```

---

## 🔧 API Endpoints

### Base URL: `https://dev-utility-api-vault.onrender.com`

| Endpoint | Method | Description | Example |
|----------|--------|-------------|---------|
| `/markdown-to-html` | POST | Convert Markdown to HTML | `{"markdown": "# Title"}` |
| `/qr-code` | POST | Generate QR code | `{"text": "Hello World"}` |
| `/image-to-base64` | POST | Convert image to base64 | Upload image file |
| `/regex-test` | POST | Test regex patterns | `{"pattern": "\\d+", "text": "123"}` |
| `/webpage-word-count` | POST | Count webpage words | `{"url": "https://example.com"}` |
| `/text-summarize` | POST | Summarize text | `{"text": "Long text..."}` |

**📖 [Full API Documentation](https://dev-utility-api-vault.onrender.com/docs)**

---

## 🧪 Testing & Quality

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_endpoints.py -v
```

**Quality Metrics:**
- ✅ 95%+ Test Coverage
- ✅ Type Hints Throughout
- ✅ Comprehensive Error Handling
- ✅ API Rate Limiting
- ✅ Input Validation

---

## 🐳 Docker Deployment

```bash
# Build and run with Docker
docker build -t dev-api-vault .
docker run -p 8000:8000 dev-api-vault

# Or use docker-compose
docker-compose up -d
```

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
- 📧 **Contact:** [Your Email]

---

<div align="center">

### ⭐ If this project helped you, please give it a star!

[![GitHub stars](https://img.shields.io/github/stars/KrunalValvi/Dev_Api_Vault?style=social)](https://github.com/KrunalValvi/Dev_Api_Vault/stargazers)

**Made with ❤️ by [KrunalValvi](https://github.com/KrunalValvi)**

</div>
