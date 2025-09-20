# Development Guide

## Dev API Vault - Development and Deployment Guide

This guide provides comprehensive instructions for setting up, developing, and deploying the Dev API Vault application.

## Table of Contents

1. [Local Development Setup](#local-development-setup)
2. [Project Structure](#project-structure)
3. [Configuration](#configuration)
4. [Running the Application](#running-the-application)
5. [Testing](#testing)
6. [Code Quality](#code-quality)
7. [Docker Deployment](#docker-deployment)
8. [Production Deployment](#production-deployment)
9. [Contributing](#contributing)

## Local Development Setup

### Prerequisites

- Python 3.9 or higher
- pip package manager
- Git
- Optional: Docker for containerized development

### Step 1: Clone the Repository

```bash
git clone https://github.com/KrunalValvi/Dev_Api_Vault.git
cd Dev_Api_Vault
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
# Install production dependencies
pip install -r requirements.txt

# For development, also install dev dependencies
pip install pytest pytest-asyncio pytest-cov black flake8 isort mypy
```

### Step 4: Environment Configuration

```bash
# Copy example environment file
cp .env.example .env

# Edit .env file with your configuration
# At minimum, set RAPIDAPI_PROXY_SECRET
```

### Step 5: Download NLTK Data

```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

## Project Structure

```
Dev_Api_Vault/
├── app/                    # Main application package
│   ├── __init__.py
│   ├── main.py            # FastAPI application entry point
│   ├── config.py          # Configuration management
│   ├── models.py          # Pydantic models
│   ├── routers.py         # API route handlers
│   ├── security.py        # Authentication and security
│   ├── middleware.py      # Rate limiting and other middleware
│   └── utils.py           # Security and utility functions
├── tests/                  # Test suite
│   ├── __init__.py
│   ├── conftest.py        # Test configuration and fixtures
│   └── test_api.py        # Comprehensive API tests
├── .env.example           # Example environment variables
├── .env                   # Environment variables (create from example)
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker container definition
├── docker-compose.yml     # Docker Compose configuration
├── API_REFERENCE.md       # API documentation
├── DEVELOPMENT.md         # This file
└── README.md              # Project overview
```

## Configuration

### Environment Variables

Create a `.env` file with the following variables:

```bash
# Required
RAPIDAPI_PROXY_SECRET=your_secret_key_here

# Optional (with defaults)
FASTAPI_ENV=development
DEBUG=True
LOG_LEVEL=INFO
RATE_LIMIT_REQUESTS_PER_MINUTE=60
REQUEST_TIMEOUT=10
ALLOWED_ORIGINS=["*"]
```

### Configuration Classes

The application uses Pydantic Settings for configuration management:

```python
from app.config import settings

# Access configuration
print(settings.rapidapi_proxy_secret)
print(settings.is_production)
print(settings.rate_limit_requests_per_minute)
```

## Running the Application

### Development Server

```bash
# Using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or using the VS Code built-in task (if configured)
# Ctrl+Shift+P -> "Tasks: Run Task" -> "Run FastAPI Dev Server"
```

### Production Server

```bash
# Using gunicorn for production
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Access Points

- **API Base**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_api.py

# Run specific test class
pytest tests/test_api.py::TestMarkdownToHtml

# Run with verbose output
pytest -v

# Run tests in parallel (install pytest-xdist first)
pytest -n auto
```

### Test Structure

The test suite includes:

- **Unit Tests**: Individual function testing
- **Integration Tests**: API endpoint testing
- **Security Tests**: Authentication and input validation
- **Error Handling Tests**: Edge cases and error conditions

### Writing Tests

```python
# Example test function
def test_new_endpoint(test_client, test_headers):
    response = test_client.post(
        "/api/v1/new-endpoint",
        json={"data": "test"},
        headers=test_headers
    )
    assert response.status_code == 200
    assert "expected_field" in response.json()
```

## Code Quality

### Code Formatting

```bash
# Format code with black
black app/ tests/

# Sort imports with isort
isort app/ tests/

# Check code style with flake8
flake8 app/ tests/
```

### Type Checking

```bash
# Run mypy for type checking
mypy app/
```

### Pre-commit Hooks

Install pre-commit hooks to automatically format code:

```bash
pip install pre-commit
pre-commit install

# Run hooks manually
pre-commit run --all-files
```

### Code Style Guidelines

- Follow PEP 8 style guide
- Use type hints for all functions
- Write docstrings for all public functions
- Keep functions focused and small
- Use meaningful variable names
- Add comments for complex logic

## Docker Deployment

### Building the Image

```bash
# Build the Docker image
docker build -t dev-api-vault .

# Build with specific tag
docker build -t dev-api-vault:v2.0.0 .
```

### Running with Docker

```bash
# Run single container
docker run -d \
  --name dev-api-vault \
  -p 8000:8000 \
  -e RAPIDAPI_PROXY_SECRET=your_secret \
  dev-api-vault

# Run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f api
```

### Docker Compose Configuration

```yaml
# docker-compose.yml
version: '3.8'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - RAPIDAPI_PROXY_SECRET=${RAPIDAPI_PROXY_SECRET}
      - FASTAPI_ENV=production
    restart: unless-stopped
```

## Production Deployment

### Platform Requirements

- Python 3.9+
- 512MB RAM minimum (1GB recommended)
- 100MB disk space
- HTTPS support recommended

### Deployment Platforms

#### Render.com
1. Connect GitHub repository
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Add environment variables

#### Heroku
```bash
# Create Procfile
echo "web: uvicorn app.main:app --host 0.0.0.0 --port \$PORT" > Procfile

# Deploy
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

#### Digital Ocean App Platform
```yaml
# .do/app.yaml
name: dev-api-vault
services:
- name: api
  source_dir: /
  github:
    repo: KrunalValvi/Dev_Api_Vault
    branch: main
  run_command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
  environment_slug: python
  instance_count: 1
  instance_size_slug: basic-xxs
```

### Environment Variables for Production

```bash
RAPIDAPI_PROXY_SECRET=secure_random_secret
FASTAPI_ENV=production
DEBUG=False
LOG_LEVEL=WARNING
RATE_LIMIT_REQUESTS_PER_MINUTE=100
ALLOWED_ORIGINS=["https://yourdomain.com"]
```

### Production Checklist

- [ ] Set secure `RAPIDAPI_PROXY_SECRET`
- [ ] Set `FASTAPI_ENV=production`
- [ ] Set `DEBUG=False`
- [ ] Configure proper `ALLOWED_ORIGINS`
- [ ] Set up HTTPS/SSL
- [ ] Configure monitoring and logging
- [ ] Set up backup strategy
- [ ] Test all endpoints in production environment

## Performance Optimization

### Application Performance

1. **Rate Limiting**: Configured per environment
2. **Request Timeouts**: Configurable timeout values
3. **Content Limits**: File size and text length limits
4. **Connection Pooling**: Reuse HTTP connections
5. **Caching**: Consider Redis for response caching

### Server Performance

```bash
# Use multiple workers for production
gunicorn app.main:app \
  -w 4 \
  -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --max-requests 1000 \
  --max-requests-jitter 100
```

## Monitoring and Logging

### Application Logs

```python
import logging

# Configure logging in production
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
```

### Health Monitoring

- Monitor `/health` endpoint
- Set up alerts for 4xx/5xx errors
- Monitor response times
- Track rate limit violations

## Contributing

### Development Workflow

1. Fork the repository
2. Create feature branch: `git checkout -b feature/new-feature`
3. Make changes and add tests
4. Run test suite: `pytest`
5. Check code quality: `black . && isort . && flake8 .`
6. Commit changes: `git commit -m "Add new feature"`
7. Push branch: `git push origin feature/new-feature`
8. Create Pull Request

### Pull Request Guidelines

- Include tests for new features
- Update documentation as needed
- Follow existing code style
- Add changelog entry
- Ensure all CI checks pass

### Code Review Process

1. Automated checks (tests, linting, security)
2. Manual code review by maintainers
3. Address feedback and update PR
4. Final approval and merge

## Troubleshooting

### Common Issues

**Import Errors**
```bash
# Ensure all dependencies are installed
pip install -r requirements.txt

# Check Python path
python -c "import sys; print(sys.path)"
```

**NLTK Data Missing**
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

**Port Already in Use**
```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>
```

**Environment Variables Not Loading**
```bash
# Check .env file exists and is readable
ls -la .env

# Verify environment loading
python -c "from app.config import settings; print(settings.dict())"
```

### Debug Mode

Enable debug mode for development:

```bash
export DEBUG=True
export FASTAPI_ENV=development
```

This enables:
- Detailed error messages
- Auto-reload on code changes
- Interactive API documentation
- Verbose logging

## Security Considerations

### Development Security

- Never commit secrets to version control
- Use `.env` files for local configuration
- Regularly update dependencies
- Run security audits: `pip audit`

### Production Security

- Use strong, random secrets
- Enable HTTPS only
- Configure CORS properly
- Monitor for suspicious activity
- Regular security updates

## Support

For issues and questions:

- **GitHub Issues**: [Create Issue](https://github.com/KrunalValvi/Dev_Api_Vault/issues)
- **Documentation**: [API Reference](API_REFERENCE.md)
- **Email**: Create an issue for support requests