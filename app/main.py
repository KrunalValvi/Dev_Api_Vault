"""
Dev API Vault - A comprehensive collection of developer utilities.

This FastAPI application provides various utility endpoints for developers,
including markdown conversion, QR code generation, image processing, and more.
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from . import routers
from .config import settings


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


# Initialize FastAPI App
app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version,
    lifespan=lifespan,
    debug=settings.debug,
    contact={
        "name": "API Support",
        "url": "https://github.com/KrunalValvi/Dev_Api_Vault",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    docs_url="/docs" if not settings.is_production else None,
    redoc_url="/redoc" if not settings.is_production else None,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Add trusted host middleware for production
if settings.is_production:
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*.onrender.com", "localhost", "127.0.0.1"]
    )

# Add rate limiting middleware
from .middleware import RateLimitMiddleware
app.add_middleware(RateLimitMiddleware)

# Include the router from routers.py
app.include_router(routers.router)


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