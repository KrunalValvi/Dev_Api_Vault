"""
Security module for Dev API Vault.
Handles authentication, rate limiting, and security middleware.
"""

import logging
from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader

from .config import settings

logger = logging.getLogger(__name__)

# Define the header we expect to receive from RapidAPI
api_key_header = APIKeyHeader(name="X-RapidAPI-Proxy-Secret", auto_error=False)


async def verify_rapidapi_secret(api_key: str = Security(api_key_header)):
    """
    Dependency to verify RapidAPI secret key.
    
    This function protects endpoints by checking the incoming request
    for the correct secret key in the X-RapidAPI-Proxy-Secret header.
    
    Args:
        api_key (str): The API key from the request header
        
    Returns:
        bool: True if authentication is successful
        
    Raises:
        HTTPException: If authentication fails or secret is not configured
    """
    # Skip authentication in development mode if no secret is set
    if settings.is_development and not settings.rapidapi_proxy_secret:
        logger.warning("Development mode: Skipping API key verification")
        return True
    
    # Check if the secret is configured on our server
    if not settings.rapidapi_proxy_secret:
        logger.error("API secret not configured on the server")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="API secret not configured on the server."
        )

    # Check if the header was provided and if it matches our secret
    if not api_key or api_key != settings.rapidapi_proxy_secret:
        logger.warning(f"Invalid API key attempt from request")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or missing API secret."
        )
    
    logger.debug("API key verification successful")
    return True


async def optional_rapidapi_secret(api_key: str = Security(api_key_header)):
    """
    Optional dependency for endpoints that don't require authentication.
    
    This can be used for public endpoints that optionally accept
    authentication for enhanced features.
    
    Args:
        api_key (str): The API key from the request header
        
    Returns:
        bool: True if authenticated, False if not
    """
    if not api_key or not settings.rapidapi_proxy_secret:
        return False
    
    return api_key == settings.rapidapi_proxy_secret