"""
Dev API Vault - A comprehensive collection of developer utilities.

This FastAPI application provides various utility endpoints for developers,
including markdown conversion, QR code generation, image processing, and more.
"""

import logging
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request as StarletteRequest

from . import routers, __version__
from .config import settings
from .openapi import API_METADATA, get_openapi_tags, get_operation_config, get_secure_operation_config


# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle application startup and shutdown events."""
    # Startup
    logger.info("Starting Dev API Vault...")
    
    # Download NLTK data if needed
    try:
        import nltk
        import ssl
        try:
            _create_unverified_https_context = ssl._create_unverified_context
        except AttributeError:
            pass
        else:
            ssl._create_default_https_context = _create_unverified_https_context
        
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        logger.info("NLTK data initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize NLTK data: {e}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Dev API Vault...")


# Custom exception handler for rate limiting
class RateLimitExceeded(HTTPException):
    def __init__(self, detail: str, retry_after: int):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=detail,
            headers={"Retry-After": str(retry_after)},
        )

# Rate limiting middleware
class RateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, limit: int = 100, window: int = 3600):
        super().__init__(app)
        self.limit = limit
        self.window = window
        self.requests = {}

    async def dispatch(self, request: StarletteRequest, call_next):
        # Skip rate limiting for health checks and docs
        if request.url.path in ["/health", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)
            
        client_ip = request.client.host
        current_time = int(time.time())
        
        # Clean up old entries
        for ip in list(self.requests.keys()):
            if current_time - self.requests[ip]["timestamp"] > self.window:
                del self.requests[ip]
        
        # Initialize or update request count
        if client_ip not in self.requests:
            self.requests[client_ip] = {"count": 1, "timestamp": current_time}
        else:
            self.requests[client_ip]["count"] += 1
        
        # Check rate limit
        if self.requests[client_ip]["count"] > self.limit:
            retry_after = self.window - (current_time - self.requests[client_ip]["timestamp"])
            raise RateLimitExceeded(
                detail=f"Rate limit exceeded. Try again in {retry_after} seconds.",
                retry_after=retry_after
            )
        
        # Add rate limit headers to response
        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(self.limit)
        response.headers["X-RateLimit-Remaining"] = str(self.limit - self.requests[client_ip]["count"])
        response.headers["X-RateLimit-Reset"] = str(self.requests[client_ip]["timestamp"] + self.window)
        
        return response

# Initialize FastAPI App with enhanced OpenAPI documentation
app = FastAPI(
    **API_METADATA,
    version=__version__,
    debug=settings.debug,
    openapi_tags=get_openapi_tags(),
    docs_url=None,  # We'll serve custom docs
    redoc_url=None,  # We'll serve custom ReDoc
    openapi_url="/openapi.json" if not settings.is_production else None,
    default_response_class=JSONResponse,
    lifespan=lifespan,
    root_path=settings.root_path or ""
)

# Serve static files for custom docs
app.mount("/static", StaticFiles(directory="static"), name="static")

# Custom docs endpoints
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title=f"{app.title} - Swagger UI",
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )

@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url="/openapi.json",
        title=f"{app.title} - ReDoc",
        redoc_js_url="/static/redoc.standalone.js",
    )

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["X-RateLimit-Limit", "X-RateLimit-Remaining", "X-RateLimit-Reset"]
)

# Add trusted host middleware for production
if settings.is_production:
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*.onrender.com", "localhost", "127.0.0.1"]
    )

# Add rate limiting middleware
app.add_middleware(RateLimiterMiddleware, limit=100, window=3600)  # 100 requests per hour

# Include the router with operation configuration
app.include_router(
    routers.router,
    **get_secure_operation_config()
)

# Override the default OpenAPI schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = app.openapi()
    
    # Add security scheme
    openapi_schema["components"]["securitySchemes"] = {
        "ApiKeyAuth": {
            "type": "apiKey",
            "in": "header",
            "name": "X-RapidAPI-Proxy-Secret",
            "description": "API key for authentication"
        }
    }
    
    # Add security to all operations
    for path in openapi_schema["paths"].values():
        for method in path.values():
            if method.get("security") is None:
                method["security"] = [{"ApiKeyAuth": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi


# Enhanced exception handlers
@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    """Handle value errors with appropriate error messages."""
    logger.warning(f"Value error on {request.url}: {exc}")
    return JSONResponse(
        status_code=400,
        content={"error": "Bad Request", "detail": str(exc)},
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """Handle any unexpected server errors for a clean response."""
    logger.error(f"Unexpected error on {request.url}: {exc}", exc_info=True)
    
    error_detail = str(exc) if settings.debug else "An unexpected server error occurred"
    
    return JSONResponse(
        status_code=500,
        content={"error": "Internal Server Error", "detail": error_detail},
    )


# Root Endpoint (Health Check)
@app.get("/", tags=["Health Check"])
async def root():
    """
    Health check endpoint to confirm the API is running.
    
    Returns:
        dict: Status information about the API
    """
    return {
        "status": "ok", 
        "message": "Welcome to Dev API Vault!",
        "version": settings.api_version,
        "environment": settings.fastapi_env
    }


@app.get("/health", tags=["Health Check"])
async def health_check():
    """
    Detailed health check endpoint.
    
    Returns:
        dict: Detailed health information
    """
    return {
        "status": "healthy",
        "api_version": settings.api_version,
        "environment": settings.fastapi_env,
        "debug_mode": settings.debug
    }