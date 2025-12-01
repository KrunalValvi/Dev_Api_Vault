# Architecture Overview

## System Design

Dev API Vault is built as a **modular FastAPI microservice** designed for scalability, maintainability, and ease of deployment.

```
┌─────────────────────────────────────────────────────────────┐
│                     Client Applications                      │
│              (Web, Mobile, CLI, Third-party APIs)            │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/REST
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Application                       │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Middleware Layer                        │   │
│  │  • CORS Middleware (Cross-Origin Resource Sharing)  │   │
│  │  • Rate Limiting Middleware                         │   │
│  │  • Request/Response Logging                         │   │
│  │  • Security Headers (TrustedHost)                   │   │
│  └──────────────────────────────────────────────────────┘   │
│                         │                                    │
│  ┌──────────────────────▼──────────────────────────────┐   │
│  │              Router Layer (routers.py)              │   │
│  │  • /api/v1/markdown-to-html                        │   │
│  │  • /api/v1/qr-code                                 │   │
│  │  • /api/v1/image-to-base64                         │   │
│  │  • /api/v1/regex-tester                            │   │
│  │  • /api/v1/word-count                              │   │
│  │  • /api/v1/summarize                               │   │
│  └──────────────────────┬──────────────────────────────┘   │
│                         │                                    │
│  ┌──────────────────────▼──────────────────────────────┐   │
│  │         Business Logic Layer (utils.py)            │   │
│  │  • Markdown Processing                             │   │
│  │  • QR Code Generation                              │   │
│  │  • Image Encoding                                  │   │
│  │  • Regex Validation                                │   │
│  │  • Web Scraping & Analysis                         │   │
│  │  • Text Summarization (NLTK)                       │   │
│  └──────────────────────┬──────────────────────────────┘   │
│                         │                                    │
│  ┌──────────────────────▼──────────────────────────────┐   │
│  │         Data Validation Layer (models.py)          │   │
│  │  • Pydantic Request Models                         │   │
│  │  • Pydantic Response Models                        │   │
│  │  • Type Hints & Validation                         │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Directory Structure

```
Dev_Api_Vault/
├── app/                          # Main application package
│   ├── __init__.py              # Package initialization & version
│   ├── main.py                  # FastAPI app setup & lifespan
│   ├── config.py                # Configuration management (settings)
│   ├── models.py                # Pydantic request/response models
│   ├── routers.py               # API endpoint definitions
│   ├── utils.py                 # Business logic & utility functions
│   ├── security.py              # Authentication & security utilities
│   ├── middleware.py            # Custom middleware (rate limiting, etc.)
│   └── openapi.py               # OpenAPI/Swagger customization
│
├── tests/                        # Test suite
│   ├── __init__.py
│   ├── conftest.py              # Pytest configuration & fixtures
│   ├── test_api.py              # API endpoint tests
│   └── test_edge_cases.py       # Edge case & error handling tests
│
├── assets/                       # Static assets
│   └── demo/                    # Demo screenshots & documentation
│
├── static/                       # Static files (if needed)
│
├── .github/                      # GitHub configuration
│   └── workflows/               # CI/CD workflows
│
├── .env.example                 # Example environment variables
├── .gitignore                   # Git ignore patterns
├── .gitattributes               # Git attributes (line endings)
├── CHANGELOG.md                 # Version history
├── CONTRIBUTING.md              # Contribution guidelines
├── CODE_OF_CONDUCT.md           # Community code of conduct
├── DEVELOPMENT.md               # Development setup guide
├── LICENSE                      # MIT License
├── README.md                    # Project documentation
├── ARCHITECTURE.md              # This file
├── Dockerfile                   # Docker image configuration
├── docker-compose.yml           # Multi-container setup
├── pyproject.toml               # Poetry project configuration
├── requirements.txt             # Pip dependencies
└── build.sh                     # Build script for NLTK data
```

## Data Flow

### Request Processing Pipeline

```
1. Client Request
   ↓
2. Middleware Processing
   • CORS validation
   • Rate limit check
   • Request logging
   ↓
3. Router Matching
   • Path matching
   • HTTP method validation
   ↓
4. Request Validation
   • Pydantic model validation
   • Type checking
   ↓
5. Business Logic Execution
   • Utility function processing
   • External API calls (if needed)
   ↓
6. Response Formatting
   • Pydantic response model
   • JSON serialization
   ↓
7. Middleware Post-Processing
   • Response logging
   • Security headers
   ↓
8. Client Response
```

## Key Components

### 1. **FastAPI Application** (`main.py`)
- Entry point for the application
- Middleware configuration
- Lifespan management (startup/shutdown)
- OpenAPI documentation setup
- Static file serving

### 2. **Configuration Management** (`config.py`)
- Environment variable loading
- Settings validation
- Default values
- Environment-specific configurations

### 3. **Data Models** (`models.py`)
- Request payload schemas
- Response payload schemas
- Pydantic validation rules
- Type hints for IDE support

### 4. **API Routes** (`routers.py`)
- Endpoint definitions
- HTTP method handlers
- Request/response documentation
- Error handling

### 5. **Business Logic** (`utils.py`)
- Core utility implementations
- External library integrations
- Data processing functions
- Helper methods

### 6. **Security** (`security.py`)
- API key validation
- Authentication helpers
- Password hashing utilities
- Token management

### 7. **Middleware** (`middleware.py`)
- Rate limiting implementation
- Request/response logging
- Custom headers
- Error handling middleware

### 8. **OpenAPI Customization** (`openapi.py`)
- Custom API metadata
- Tag definitions
- Operation configurations
- Security scheme definitions

## Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Framework** | FastAPI | Modern async web framework |
| **Server** | Uvicorn | ASGI application server |
| **Validation** | Pydantic | Data validation & serialization |
| **Markdown** | markdown | Markdown to HTML conversion |
| **QR Codes** | qrcode + Pillow | QR code generation |
| **Web Scraping** | BeautifulSoup4 + requests | HTML parsing & HTTP requests |
| **Text Processing** | NLTK | Natural language processing |
| **Testing** | Pytest | Unit & integration testing |
| **Code Quality** | Black, isort, Flake8, mypy | Linting & formatting |
| **Containerization** | Docker | Application containerization |
| **CI/CD** | GitHub Actions | Automated testing & deployment |

## Deployment Architecture

### Local Development
```
Developer Machine
├── Python venv
├── FastAPI app (uvicorn)
├── SQLite (optional)
└── NLTK data cache
```

### Docker Deployment
```
Docker Container
├── Python 3.9+ runtime
├── FastAPI app (uvicorn)
├── All dependencies
└── NLTK data (pre-downloaded)
```

### Cloud Deployment (Render/Heroku)
```
Cloud Platform
├── Container registry
├── Managed Python runtime
├── Auto-scaling
├── Health checks
└── Environment variables
```

## Security Considerations

1. **Input Validation**: All inputs validated via Pydantic models
2. **Rate Limiting**: Middleware prevents abuse
3. **CORS Configuration**: Restricted to allowed origins
4. **Trusted Hosts**: TrustedHostMiddleware prevents header injection
5. **Environment Variables**: Sensitive data in `.env` files
6. **Error Handling**: Generic error messages to prevent information leakage
7. **Logging**: Comprehensive logging without sensitive data

## Performance Optimization

1. **Async/Await**: Non-blocking I/O operations
2. **Caching**: Response caching where applicable
3. **Connection Pooling**: Reused HTTP connections
4. **NLTK Data**: Pre-downloaded to avoid runtime downloads
5. **Static File Serving**: Efficient static file delivery

## Scalability

- **Horizontal Scaling**: Stateless design allows multiple instances
- **Load Balancing**: Can be deployed behind a load balancer
- **Database Ready**: Can integrate with PostgreSQL/MongoDB
- **Microservice Ready**: Can be split into separate services

## Future Enhancements

- [ ] Database integration (PostgreSQL/MongoDB)
- [ ] Caching layer (Redis)
- [ ] Message queue (Celery/RabbitMQ)
- [ ] WebSocket support for real-time operations
- [ ] GraphQL endpoint
- [ ] Advanced authentication (OAuth2/JWT)
- [ ] API versioning strategy
- [ ] Monitoring & observability (Prometheus/Grafana)

---

**Last Updated**: 2025-12-01
**Version**: 1.0.0
