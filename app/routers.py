"""
API routers for Dev API Vault.
Contains all utility endpoints with proper error handling and validation.
"""

# Standard Library Imports
import base64
import io
import re
import logging
from collections import defaultdict
import heapq
from typing import List, Dict, Any

# Third-party Imports
import markdown
import qrcode
import requests
from bs4 import BeautifulSoup
from fastapi import APIRouter, HTTPException, File, UploadFile, Depends
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize

# Local Imports
from . import models
from . import security
from .config import settings
from .utils import (
    sanitize_filename, 
    validate_url_safety, 
    sanitize_user_input, 
    check_content_type_safety,
    validate_regex_safety
)

# Configure logging
logger = logging.getLogger(__name__)

# Initialize Router
router = APIRouter(
    prefix="/api/v1",
    tags=["Utilities"],
    dependencies=[Depends(security.verify_rapidapi_secret)]
)

# Utility functions
def validate_text_length(text: str, max_length: int = 50000) -> None:
    """Validate text length to prevent memory issues."""
    if len(text) > max_length:
        raise HTTPException(
            status_code=400,
            detail=f"Text too long. Maximum {max_length} characters allowed."
        )


def safe_web_request(url: str, timeout: int = None) -> requests.Response:
    """Make a safe web request with proper error handling."""
    timeout = timeout or settings.request_timeout
    
    # Validate URL safety
    if not validate_url_safety(str(url)):
        raise HTTPException(
            status_code=400,
            detail="URL not allowed for security reasons"
        )
    
    headers = {
        'User-Agent': 'Dev-API-Vault/2.0 (https://github.com/KrunalValvi/Dev_Api_Vault)'
    }
    
    try:
        response = requests.get(
            str(url), 
            timeout=timeout, 
            headers=headers,
            allow_redirects=True,
            verify=True,
            stream=False  # Don't stream to prevent large downloads
        )
        
        # Check content length before processing
        content_length = response.headers.get('content-length')
        if content_length and int(content_length) > 10 * 1024 * 1024:  # 10MB limit
            raise HTTPException(
                status_code=400,
                detail="Content too large to process"
            )
        
        response.raise_for_status()
        return response
    except requests.exceptions.Timeout:
        raise HTTPException(
            status_code=408, 
            detail="Request timeout while fetching the URL"
        )
    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=400, 
            detail="Could not connect to the provided URL"
        )
    except requests.exceptions.HTTPError as e:
        raise HTTPException(
            status_code=400, 
            detail=f"HTTP error {e.response.status_code}: {e.response.reason}"
        )
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=400, 
            detail=f"Could not fetch URL: {str(e)}"
        )


# --- API Endpoints ---

@router.post(
    "/markdown-to-html", 
    response_model=models.HtmlResponse, 
    summary="Convert Markdown to HTML"
)
async def convert_markdown_to_html(request: models.MarkdownRequest):
    """
    Convert Markdown text to HTML format.
    
    This endpoint takes Markdown text and converts it to clean HTML using
    the Python markdown library with safe defaults.
    
    Args:
        request: MarkdownRequest containing the markdown text
        
    Returns:
        HtmlResponse: The converted HTML content
        
    Raises:
        HTTPException: If text is too long or conversion fails
    """
    try:
        validate_text_length(request.markdown_text, 10000)
        
        # Sanitize input
        sanitized_text = sanitize_user_input(request.markdown_text, 10000)
        
        # Use safe markdown conversion with extensions
        html_content = markdown.markdown(
            sanitized_text,
            extensions=['tables', 'fenced_code', 'toc'],
            tab_length=4
        )
        
        logger.info(f"Successfully converted {len(request.markdown_text)} chars of markdown")
        return {"html_content": html_content}
        
    except Exception as e:
        logger.error(f"Markdown conversion failed: {e}")
        raise HTTPException(
            status_code=500,
            detail="Markdown conversion failed"
        )


@router.post(
    "/qr-code", 
    response_model=models.QrCodeResponse, 
    summary="Generate a QR Code"
)
async def generate_qr_code(request: models.QrCodeRequest):
    """
    Generate a QR code from the provided data.
    
    Creates a QR code image and returns it as a base64 encoded PNG.
    Supports customizable box size and border width.
    
    Args:
        request: QrCodeRequest with data and styling options
        
    Returns:
        QrCodeResponse: Base64 encoded PNG image of the QR code
        
    Raises:
        HTTPException: If QR code generation fails
    """
    try:
        validate_text_length(str(request.data), 2000)
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=min(request.box_size, 50),  # Limit box size
            border=min(request.border, 20),      # Limit border
        )
        qr.add_data(str(request.data))
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        
        logger.info(f"Generated QR code for {len(str(request.data))} chars of data")
        return {"qr_code_base64": f"data:image/png;base64,{img_str}"}
        
    except Exception as e:
        logger.error(f"QR code generation failed: {e}")
        raise HTTPException(
            status_code=500,
            detail="QR code generation failed"
        )


@router.post(
    "/image-to-base64", 
    response_model=models.Base64Response, 
    summary="Convert Image to Base64"
)
async def image_to_base64(file: UploadFile = File(...)):
    """
    Convert an uploaded image file to base64 string.
    
    Accepts common image formats and converts them to base64 encoding
    for use in data URIs or API responses.
    
    Args:
        file: Uploaded image file
        
    Returns:
        Base64Response: Filename and base64 encoded string
        
    Raises:
        HTTPException: If file is too large or not a valid image
    """
    try:
        # Validate file type
        allowed_types = ['image/png', 'image/jpeg', 'image/jpg', 'image/gif', 'image/webp']
        if not file.content_type or not check_content_type_safety(file.content_type, allowed_types):
            raise HTTPException(
                status_code=400,
                detail="File must be a supported image format (PNG, JPEG, GIF, WebP)"
            )
        
        # Read file content
        contents = await file.read()
        
        # Validate file size (10MB limit)
        if len(contents) > 10 * 1024 * 1024:
            raise HTTPException(
                status_code=400,
                detail="File too large. Maximum 10MB allowed."
            )
        
        base64_encoded_str = base64.b64encode(contents).decode("utf-8")
        
        # Sanitize filename
        safe_filename = sanitize_filename(file.filename) if file.filename else "unknown"
        
        logger.info(f"Converted image {safe_filename} ({len(contents)} bytes) to base64")
        return {
            "filename": safe_filename, 
            "base64_string": base64_encoded_str,
            "file_size": len(contents),
            "content_type": file.content_type
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Image conversion failed: {e}")
        raise HTTPException(
            status_code=500,
            detail="Image conversion failed"
        )


@router.post(
    "/regex-tester", 
    response_model=models.RegexResponse, 
    summary="Test a Regular Expression"
)
async def test_regex(request: models.RegexRequest):
    """
    Test a regular expression pattern against text.
    
    Finds all occurrences of a regex pattern within the given text
    and returns the matches. Includes pattern validation.
    
    Args:
        request: RegexRequest with pattern and text
        
    Returns:
        RegexResponse: List of matches found
        
    Raises:
        HTTPException: If regex pattern is invalid or text too long
    """
    try:
        validate_text_length(request.text, 50000)
        validate_text_length(request.pattern, 1000)
        
        # Validate regex pattern for safety
        if not validate_regex_safety(request.pattern):
            raise HTTPException(
                status_code=400,
                detail="Regex pattern not allowed for security reasons"
            )
        
        # Sanitize input text
        sanitized_text = sanitize_user_input(request.text, 50000)
        
        # Compile pattern first to validate it
        compiled_pattern = re.compile(request.pattern)
        matches = compiled_pattern.findall(sanitized_text)
        
        # Limit number of matches to prevent memory issues
        if len(matches) > 1000:
            matches = matches[:1000]
            logger.warning(f"Regex matches truncated to 1000 results")
        
        logger.info(f"Regex test found {len(matches)} matches")
        return {"matches": matches, "match_count": len(matches)}
        
    except re.error as e:
        logger.warning(f"Invalid regex pattern: {e}")
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid regular expression: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Regex testing failed: {e}")
        raise HTTPException(
            status_code=500,
            detail="Regex testing failed"
        )


@router.post(
    "/word-counter", 
    response_model=models.WordCountResponse, 
    summary="Count Words on a Webpage"
)
async def count_words_in_webpage(request: models.UrlRequest):
    """
    Fetch a webpage and count words and characters.
    
    Downloads the webpage content, extracts text (excluding scripts/styles),
    and provides word and character counts along with basic metadata.
    
    Args:
        request: UrlRequest with the URL to analyze
        
    Returns:
        WordCountResponse: Word count, character count, and metadata
        
    Raises:
        HTTPException: If URL cannot be fetched or processed
    """
    try:
        response = safe_web_request(request.url)
        
        # Parse HTML and extract text
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script, style, and other non-content elements
        for element in soup(["script", "style", "nav", "footer", "header"]):
            element.decompose()
            
        # Extract and clean text
        text = soup.get_text(separator=' ', strip=True)
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split())
        clean_text = ' '.join(chunk for chunk in chunks if chunk)
        
        word_count = len(clean_text.split()) if clean_text else 0
        char_count = len(clean_text)
        
        # Extract basic metadata
        title = soup.find('title')
        title_text = title.get_text().strip() if title else "No title found"
        
        logger.info(f"Word count completed for {request.url}: {word_count} words")
        
        return {
            "url": str(request.url),
            "word_count": word_count,
            "char_count": char_count,
            "title": title_text[:200],  # Limit title length
            "status_code": response.status_code
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Word counting failed for {request.url}: {e}")
        raise HTTPException(
            status_code=500,
            detail="Word counting failed"
        )


@router.post(
    "/summarize", 
    response_model=models.SummaryResponse, 
    summary="Summarize Text"
)
async def summarize_text(request: models.TextSummarizeRequest):
    """
    Perform rule-based text summarization.
    
    Uses NLTK to analyze text and extract the most important sentences
    based on word frequency and sentence scoring. Provides extractive
    summarization suitable for general content.
    
    Args:
        request: TextSummarizeRequest with text and sentence count
        
    Returns:
        SummaryResponse: Original sentence count and extracted summary
        
    Raises:
        HTTPException: If text processing fails or NLTK data unavailable
    """
    try:
        validate_text_length(request.text, 100000)
        
        # Tokenize sentences
        sentences = sent_tokenize(request.text)
        original_sentence_count = len(sentences)

        # Return original text if already short enough
        if original_sentence_count <= request.sentence_count:
            return {
                "original_sentence_count": original_sentence_count, 
                "summary": request.text.strip(),
                "summary_sentence_count": original_sentence_count
            }

        # Calculate word frequencies (excluding stopwords)
        try:
            stop_words = set(stopwords.words('english'))
        except LookupError:
            # Fallback if stopwords not available
            stop_words = set()
            logger.warning("NLTK stopwords not available, using empty set")

        word_frequencies = defaultdict(int)
        for word in word_tokenize(request.text.lower()):
            if word.isalnum() and word not in stop_words:
                word_frequencies[word] += 1
        
        # Handle edge case where no valid words found
        if not word_frequencies:
            summary = '. '.join(sentences[:request.sentence_count])
            return {
                "original_sentence_count": original_sentence_count,
                "summary": summary,
                "summary_sentence_count": min(request.sentence_count, original_sentence_count)
            }

        # Normalize frequencies
        max_freq = max(word_frequencies.values())
        for word in word_frequencies.keys():
            word_frequencies[word] = word_frequencies[word] / max_freq

        # Score sentences based on word frequencies
        sentence_scores = defaultdict(float)
        for i, sentence in enumerate(sentences):
            sentence_word_count = 0
            for word in word_tokenize(sentence.lower()):
                if word in word_frequencies:
                    sentence_scores[i] += word_frequencies[word]
                    sentence_word_count += 1
            
            # Normalize by sentence length to avoid bias toward long sentences
            if sentence_word_count > 0:
                sentence_scores[i] = sentence_scores[i] / sentence_word_count
        
        # Select top sentences
        summary_sentences_indices = heapq.nlargest(
            request.sentence_count, 
            sentence_scores, 
            key=sentence_scores.get
        )
        
        # Sort indices to maintain original order
        summary_sentences_indices.sort()
        summary = '. '.join([sentences[i] for i in summary_sentences_indices])
        
        logger.info(f"Summarized {original_sentence_count} sentences to {len(summary_sentences_indices)}")
        
        return {
            "original_sentence_count": original_sentence_count,
            "summary": summary,
            "summary_sentence_count": len(summary_sentences_indices)
        }
        
    except LookupError as e:
        logger.error(f"NLTK data not available: {e}")
        raise HTTPException(
            status_code=500,
            detail="Text processing libraries not properly initialized"
        )
    except Exception as e:
        logger.error(f"Text summarization failed: {e}")
        raise HTTPException(
            status_code=500,
            detail="Text summarization failed"
        )