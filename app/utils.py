"""
Security utilities for Dev API Vault.
Additional security functions and validation helpers.
"""

import re
import hashlib
import secrets
from typing import Optional, List
from urllib.parse import urlparse


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to prevent directory traversal and other attacks.
    
    Args:
        filename: Original filename
        
    Returns:
        str: Sanitized filename safe for use
    """
    if not filename:
        return "unknown"
    
    # Remove path components
    filename = filename.split("/")[-1].split("\\")[-1]
    
    # Remove or replace dangerous characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Limit length
    if len(filename) > 255:
        name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
        filename = name[:250] + ('.' + ext if ext else '')
    
    return filename or "unknown"


def validate_url_safety(url: str) -> bool:
    """
    Validate URL for safety (prevent SSRF attacks).
    
    Args:
        url: URL to validate
        
    Returns:
        bool: True if URL is considered safe
    """
    try:
        parsed = urlparse(str(url))
        
        # Must have scheme
        if not parsed.scheme or parsed.scheme not in ['http', 'https']:
            return False
        
        # Must have hostname
        if not parsed.hostname:
            return False
        
        # Block localhost and private IP ranges
        hostname = parsed.hostname.lower()
        
        # Block localhost variations
        if hostname in ['localhost', '127.0.0.1', '0.0.0.0', '::1']:
            return False
        
        # Block private IP ranges (basic check)
        if (hostname.startswith('192.168.') or 
            hostname.startswith('10.') or 
            hostname.startswith('172.16.') or
            hostname.startswith('172.17.') or
            hostname.startswith('172.18.') or
            hostname.startswith('172.19.') or
            hostname.startswith('172.2') or
            hostname.startswith('172.3') or
            hostname.startswith('169.254.')):  # Link-local
            return False
        
        # Block other suspicious patterns
        if (hostname.startswith('.') or 
            hostname.endswith('.local') or
            '.local.' in hostname):
            return False
        
        return True
        
    except Exception:
        return False


def generate_secure_token(length: int = 32) -> str:
    """
    Generate a cryptographically secure random token.
    
    Args:
        length: Length of token in bytes
        
    Returns:
        str: Hex-encoded secure token
    """
    return secrets.token_hex(length)


def hash_api_key(api_key: str, salt: Optional[str] = None) -> tuple[str, str]:
    """
    Hash an API key with salt for secure storage.
    
    Args:
        api_key: The API key to hash
        salt: Optional salt (will generate if not provided)
        
    Returns:
        tuple: (hashed_key, salt)
    """
    if salt is None:
        salt = secrets.token_hex(16)
    
    # Use PBKDF2 for key derivation
    key_hash = hashlib.pbkdf2_hmac(
        'sha256',
        api_key.encode('utf-8'),
        salt.encode('utf-8'),
        100000  # iterations
    )
    
    return key_hash.hex(), salt


def verify_api_key(api_key: str, stored_hash: str, salt: str) -> bool:
    """
    Verify an API key against stored hash.
    
    Args:
        api_key: The API key to verify
        stored_hash: The stored hash
        salt: The salt used for hashing
        
    Returns:
        bool: True if key is valid
    """
    computed_hash, _ = hash_api_key(api_key, salt)
    return secrets.compare_digest(computed_hash, stored_hash)


def sanitize_user_input(text: str, max_length: int = 10000) -> str:
    """
    Sanitize user input to prevent various injection attacks.
    
    Args:
        text: Input text to sanitize
        max_length: Maximum allowed length
        
    Returns:
        str: Sanitized text
    """
    if not text:
        return ""
    
    # Limit length
    text = text[:max_length]
    
    # Remove null bytes and other control characters
    text = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]', '', text)
    
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()


def check_content_type_safety(content_type: str, allowed_types: List[str]) -> bool:
    """
    Check if content type is in allowed list.
    
    Args:
        content_type: The content type to check
        allowed_types: List of allowed content types
        
    Returns:
        bool: True if content type is allowed
    """
    if not content_type:
        return False
    
    # Normalize content type (remove parameters)
    content_type = content_type.split(';')[0].strip().lower()
    
    return content_type in [t.lower() for t in allowed_types]


def validate_regex_safety(pattern: str) -> bool:
    """
    Validate regex pattern for safety (prevent ReDoS attacks).
    
    Args:
        pattern: Regex pattern to validate
        
    Returns:
        bool: True if pattern is considered safe
    """
    # Basic checks for potentially dangerous patterns
    dangerous_patterns = [
        r'\(\?\#',  # Embedded comments
        r'\(\?\<',  # Lookbehind
        r'\(\?\=',  # Lookahead
        r'\*\+',    # Nested quantifiers
        r'\+\*',    # Nested quantifiers
        r'\*\*',    # Nested quantifiers
        r'\+\+',    # Nested quantifiers
        r'\{\d+,\}', # Large range quantifiers
    ]
    
    for dangerous in dangerous_patterns:
        if re.search(dangerous, pattern):
            return False
    
    # Check for extremely long patterns
    if len(pattern) > 1000:
        return False
    
    # Check for excessive nesting
    nesting_level = 0
    max_nesting = 10
    
    for char in pattern:
        if char == '(':
            nesting_level += 1
            if nesting_level > max_nesting:
                return False
        elif char == ')':
            nesting_level -= 1
    
    return True