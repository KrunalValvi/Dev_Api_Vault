"""
Configuration module for Dev API Vault.
Handles environment variables and application settings.
"""

import os
from typing import List, Optional
from pydantic import Field

try:
    from pydantic_settings import BaseSettings
except ImportError:
    # Create a simple fallback for BaseSettings
    from pydantic import BaseModel
    
    class BaseSettings(BaseModel):
        class Config:
            env_file = ".env"
            env_file_encoding = "utf-8"
            case_sensitive = False


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Configuration
    rapidapi_proxy_secret: Optional[str] = Field(
        default=None,
        env="RAPIDAPI_PROXY_SECRET",
        description="Secret key for RapidAPI proxy authentication"
    )
    
    # FastAPI Configuration
    fastapi_env: str = Field(
        default="development",
        env="FASTAPI_ENV",
        description="Environment mode (development, staging, production)"
    )
    
    debug: bool = Field(
        default=True,
        env="DEBUG",
        description="Enable debug mode"
    )
    
    # CORS Configuration
    allowed_origins: List[str] = Field(
        default=["*"],
        env="ALLOWED_ORIGINS",
        description="List of allowed CORS origins"
    )
    
    # Rate Limiting
    rate_limit_requests_per_minute: int = Field(
        default=60,
        env="RATE_LIMIT_REQUESTS_PER_MINUTE",
        description="Maximum requests per minute per IP"
    )
    
    # Logging
    log_level: str = Field(
        default="INFO",
        env="LOG_LEVEL",
        description="Logging level"
    )
    
    # External API Configuration
    request_timeout: int = Field(
        default=10,
        env="REQUEST_TIMEOUT",
        description="Timeout for external API requests in seconds"
    )
    
    # API Metadata
    api_title: str = "Dev API Vault"
    api_description: str = "A comprehensive collection of developer utilities built with FastAPI"
    api_version: str = "2.0.0"
    
    class Config:
        """Pydantic config class."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        
    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.fastapi_env.lower() == "production"
    
    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.fastapi_env.lower() == "development"


# Global settings instance
settings = Settings()