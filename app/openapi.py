"""
Enhanced OpenAPI documentation for Dev API Vault.
This module provides additional OpenAPI documentation and schemas.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from enum import Enum

# Common schemas
class ErrorResponse(BaseModel):
    """Standard error response schema."""
    error: str = Field(..., description="Error message")
    code: int = Field(..., description="HTTP status code")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")

class RateLimitHeaders(BaseModel):
    """Rate limit headers."""
    x_ratelimit_limit: int = Field(..., alias="X-RateLimit-Limit", description="Request limit per hour")
    x_ratelimit_remaining: int = Field(..., alias="X-RateLimit-Remaining", description="Remaining requests in the current period")
    x_ratelimit_reset: int = Field(..., alias="X-RateLimit-Reset", description="Time when the rate limit resets (UTC timestamp)")

# API Tags
class Tags(str, Enum):
    """API tags for grouping endpoints."""
    CONVERSION = "Conversion"
    GENERATION = "Generation"
    UTILITIES = "Utilities"
    AUTH = "Authentication"
    STATUS = "Status"

# Rate limit responses
RATE_LIMIT_RESPONSES = {
    429: {
        "description": "Rate limit exceeded",
        "model": ErrorResponse,
        "headers": {
            "Retry-After": {
                "description": "Number of seconds to wait before making a new request",
                "schema": {"type": "integer"}
            },
            **RateLimitHeaders.schema()
        }
    }
}

# Common error responses
ERROR_RESPONSES = {
    400: {"model": ErrorResponse, "description": "Bad Request"},
    401: {"model": ErrorResponse, "description": "Unauthorized"},
    403: {"model": ErrorResponse, "description": "Forbidden"},
    404: {"model": ErrorResponse, "description": "Not Found"},
    422: {"model": ErrorResponse, "description": "Validation Error"},
    500: {"model": ErrorResponse, "description": "Internal Server Error"},
    **RATE_LIMIT_RESPONSES
}

# API Metadata
API_METADATA = {
    "title": "Dev API Vault",
    "description": """
    ## 🚀 Dev API Vault
    
    A comprehensive collection of developer utilities including text processing, 
    code conversion, and data transformation tools.
    
    ### 🔒 Authentication
    
    This API requires an API key for authentication. Include it in the `X-RapidAPI-Proxy-Secret` header.
    
    ### 📝 Rate Limiting
    
    - **Free Tier**: 100 requests/hour
    - **Pro Tier**: 10,000 requests/hour (contact support for upgrade)
    
    ### 📚 API Versioning
    
    The current API version is `v1`. All endpoints are prefixed with `/api/v1/`.
    
    ### 🔄 Response Format
    
    All API responses are in JSON format and include standard HTTP status codes.
    
    ### 🔗 Quick Links
    - [GitHub Repository](https://github.com/KrunalValvi/Dev_Api_Vault)
    - [Report an Issue](https://github.com/KrunalValvi/Dev_Api_Vault/issues)
    - [Request a Feature](https://github.com/KrunalValvi/Dev_Api_Vault/issues/new?template=feature_request.md)
    """,
    "version": "1.0.0",
    "contact": {
        "name": "API Support",
        "url": "https://github.com/KrunalValvi/Dev_Api_Vault/issues",
        "email": "support@example.com"
    },
    "license_info": {
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    },
    "terms_of_service": "https://github.com/KrunalValvi/Dev_Api_Vault/blob/main/TERMS.md",
    "externalDocs": {
        "description": "API Reference",
        "url": "https://dev-utility-api-vault.onrender.com/redoc"
    },
    "servers": [
        {
            "url": "https://dev-utility-api-vault.onrender.com/api/v1",
            "description": "Production server"
        },
        {
            "url": "http://localhost:8000/api/v1",
            "description": "Local development server"
        }
    ]
}

def get_openapi_tags() -> List[Dict[str, str]]:
    """Get the list of tags for the OpenAPI documentation."""
    return [
        {"name": Tags.CONVERSION, "description": "Convert between different formats"},
        {"name": Tags.GENERATION, "description": "Generate content like QR codes"},
        {"name": Tags.UTILITIES, "description": "General utility functions"},
        {"name": Tags.AUTH, "description": "Authentication and API keys"},
        {"name": Tags.STATUS, "description": "Health and status checks"},
    ]

def get_operation_config() -> Dict[str, Any]:
    """Get common operation configuration."""
    return {
        "responses": ERROR_RESPONSES,
        "tags": [tag["name"] for tag in get_openapi_tags()]
    }

def get_secure_operation_config() -> Dict[str, Any]:
    """Get operation configuration for endpoints requiring authentication."""
    return {
        **get_operation_config(),
        "security": [{"ApiKeyAuth": []}],
        "responses": {
            **ERROR_RESPONSES,
            401: {"description": "Missing or invalid API key"},
            403: {"description": "Insufficient permissions"}
        }
    }
