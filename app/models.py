"""
Pydantic models for Dev API Vault.
Defines request and response schemas for all API endpoints.
"""

from pydantic import BaseModel, Field, HttpUrl, validator
from typing import List, Optional, Union
import re


# 1. Markdown to HTML
class MarkdownRequest(BaseModel):
    """Request model for markdown to HTML conversion."""
    markdown_text: str = Field(
        ..., 
        example="# Hello World\n\nThis is **bold** text.", 
        description="The Markdown text to convert.",
        min_length=1,
        max_length=10000
    )
    
    @validator('markdown_text')
    def validate_markdown_text(cls, v):
        if not v.strip():
            raise ValueError("Markdown text cannot be empty or only whitespace")
        return v


class HtmlResponse(BaseModel):
    """Response model for markdown to HTML conversion."""
    html_content: str = Field(
        ..., 
        example="<h1>Hello World</h1>\n<p>This is <strong>bold</strong> text.</p>", 
        description="The resulting HTML content."
    )


# 2. QR Code Generator
class QrCodeRequest(BaseModel):
    """Request model for QR code generation."""
    data: str = Field(
        ..., 
        example="https://fastapi.tiangolo.com/", 
        description="The data to encode in the QR code.",
        max_length=2000
    )
    box_size: int = Field(
        10, 
        gt=0, 
        le=50,
        description="Size of each box in the QR code grid (1-50)."
    )
    border: int = Field(
        4, 
        ge=0, 
        le=20,
        description="Thickness of the border in boxes (0-20)."
    )


class QrCodeResponse(BaseModel):
    """Response model for QR code generation."""
    qr_code_base64: str = Field(
        ..., 
        description="Base64 encoded PNG image of the QR code, ready for use in an <img> tag."
    )


# 3. Image to Base64
class Base64Response(BaseModel):
    """Response model for image to base64 conversion."""
    filename: Optional[str] = Field(None, description="Original filename of the uploaded image")
    base64_string: str = Field(..., description="Base64 encoded image data")
    file_size: Optional[int] = Field(None, description="Size of the original file in bytes")
    content_type: Optional[str] = Field(None, description="MIME type of the uploaded file")


# 4. Regex Tester
class RegexRequest(BaseModel):
    """Request model for regex testing."""
    pattern: str = Field(
        ..., 
        example=r"\d+", 
        description="The regular expression pattern.",
        max_length=1000
    )
    text: str = Field(
        ..., 
        example="My number is 12345 and another is 67890.", 
        description="The text to search within.",
        max_length=50000
    )
    
    @validator('pattern')
    def validate_pattern(cls, v):
        try:
            re.compile(v)
        except re.error as e:
            raise ValueError(f"Invalid regex pattern: {e}")
        return v


class RegexResponse(BaseModel):
    """Response model for regex testing."""
    matches: List[str] = Field(..., description="List of matches found")
    match_count: int = Field(..., description="Total number of matches found")


# 5. Webpage Word Counter
class UrlRequest(BaseModel):
    """Request model for URL-based operations."""
    url: HttpUrl = Field(
        ..., 
        example="https://example.com", 
        description="The URL of the webpage to analyze."
    )


class WordCountResponse(BaseModel):
    """Response model for webpage word counting."""
    url: str = Field(..., description="The analyzed URL")
    word_count: int = Field(..., description="Number of words found")
    char_count: int = Field(..., description="Number of characters found")
    title: Optional[str] = Field(None, description="Page title if available")
    status_code: Optional[int] = Field(None, description="HTTP status code")


# 6. Rule-based Text Summarizer
class TextSummarizeRequest(BaseModel):
    """Request model for text summarization."""
    text: str = Field(
        ..., 
        min_length=50, 
        max_length=100000,
        description="Text to be summarized (minimum 50 characters)."
    )
    sentence_count: int = Field(
        3, 
        gt=0, 
        le=20,
        description="Number of sentences in the final summary (1-20)."
    )
    
    @validator('text')
    def validate_text(cls, v):
        if not v.strip():
            raise ValueError("Text cannot be empty or only whitespace")
        # Basic check for meaningful content
        words = v.split()
        if len(words) < 10:
            raise ValueError("Text must contain at least 10 words for meaningful summarization")
        return v


class SummaryResponse(BaseModel):
    """Response model for text summarization."""
    original_sentence_count: int = Field(..., description="Number of sentences in original text")
    summary: str = Field(..., description="Summarized text")
    summary_sentence_count: int = Field(..., description="Number of sentences in summary")


# Additional utility models
class ErrorResponse(BaseModel):
    """Standard error response model."""
    error: str = Field(..., description="Error type")
    detail: str = Field(..., description="Detailed error message")
    status_code: int = Field(..., description="HTTP status code")


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str = Field(..., description="Health status")
    version: str = Field(..., description="API version")
    environment: str = Field(..., description="Environment name")
    debug_mode: bool = Field(..., description="Debug mode status")