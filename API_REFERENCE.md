# API Reference

## Dev API Vault - Comprehensive API Documentation

This document provides detailed information about all available endpoints, request/response formats, and usage examples.

## Base URL

- **Production**: `https://dev-utility-api-vault.onrender.com`
- **Local Development**: `http://localhost:8000`

## Authentication

All API endpoints require authentication via the `X-RapidAPI-Proxy-Secret` header:

```http
X-RapidAPI-Proxy-Secret: your_secret_key_here
```

## Rate Limiting

- **Limit**: 60 requests per minute per IP address
- **Headers**: Response includes rate limit information:
  - `X-RateLimit-Limit`: Maximum requests per minute
  - `X-RateLimit-Remaining`: Remaining requests in current window
  - `X-RateLimit-Reset`: Unix timestamp when limit resets

## Endpoints

### 1. Health Check

#### GET `/`
Basic health check endpoint.

**Response:**
```json
{
  "status": "ok",
  "message": "Welcome to Dev API Vault!",
  "version": "2.0.0",
  "environment": "production"
}
```

#### GET `/health`
Detailed health check with system information.

**Response:**
```json
{
  "status": "healthy",
  "api_version": "2.0.0",
  "environment": "production",
  "debug_mode": false
}
```

### 2. Markdown to HTML Conversion

#### POST `/api/v1/markdown-to-html`
Convert Markdown text to HTML format.

**Request Body:**
```json
{
  "markdown_text": "# Hello World\n\nThis is **bold** text."
}
```

**Parameters:**
- `markdown_text` (string, required): Markdown text to convert (max 10,000 characters)

**Response:**
```json
{
  "html_content": "<h1>Hello World</h1>\n<p>This is <strong>bold</strong> text.</p>"
}
```

**Features:**
- Supports tables, fenced code blocks, and table of contents
- Input sanitization for security
- Proper HTML escaping

### 3. QR Code Generation

#### POST `/api/v1/qr-code`
Generate QR code as base64-encoded PNG image.

**Request Body:**
```json
{
  "data": "https://example.com",
  "box_size": 10,
  "border": 4
}
```

**Parameters:**
- `data` (string, required): Data to encode (max 2,000 characters)
- `box_size` (integer, optional): Size of each box (1-50, default: 10)
- `border` (integer, optional): Border thickness (0-20, default: 4)

**Response:**
```json
{
  "qr_code_base64": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..."
}
```

### 4. Image to Base64 Conversion

#### POST `/api/v1/image-to-base64`
Convert uploaded image to base64 string.

**Request:**
- Content-Type: `multipart/form-data`
- File parameter: `file`

**Supported formats:**
- PNG (`image/png`)
- JPEG (`image/jpeg`, `image/jpg`)
- GIF (`image/gif`)
- WebP (`image/webp`)

**Limits:**
- Maximum file size: 10MB

**Response:**
```json
{
  "filename": "example.png",
  "base64_string": "iVBORw0KGgoAAAANSUhEUgAA...",
  "file_size": 12345,
  "content_type": "image/png"
}
```

### 5. Regular Expression Tester

#### POST `/api/v1/regex-tester`
Test regex patterns against text.

**Request Body:**
```json
{
  "pattern": "\\d+",
  "text": "I have 123 apples and 456 oranges."
}
```

**Parameters:**
- `pattern` (string, required): Regular expression pattern (max 1,000 characters)
- `text` (string, required): Text to search (max 50,000 characters)

**Response:**
```json
{
  "matches": ["123", "456"],
  "match_count": 2
}
```

**Security Features:**
- Pattern validation to prevent ReDoS attacks
- Input sanitization
- Result limiting (max 1,000 matches)

### 6. Webpage Word Counter

#### POST `/api/v1/word-counter`
Fetch webpage and count words/characters.

**Request Body:**
```json
{
  "url": "https://example.com"
}
```

**Parameters:**
- `url` (string, required): Valid HTTP/HTTPS URL

**Response:**
```json
{
  "url": "https://example.com",
  "word_count": 150,
  "char_count": 850,
  "title": "Example Domain",
  "status_code": 200
}
```

**Security Features:**
- SSRF protection (blocks private IPs, localhost)
- Content size limits (10MB max)
- Request timeout protection

### 7. Text Summarization

#### POST `/api/v1/summarize`
Perform extractive text summarization using NLTK.

**Request Body:**
```json
{
  "text": "Long text content to be summarized...",
  "sentence_count": 3
}
```

**Parameters:**
- `text` (string, required): Text to summarize (50-100,000 characters, min 10 words)
- `sentence_count` (integer, optional): Number of sentences in summary (1-20, default: 3)

**Response:**
```json
{
  "original_sentence_count": 10,
  "summary": "Summary text with key sentences...",
  "summary_sentence_count": 3
}
```

**Algorithm:**
- Uses word frequency analysis with stopword filtering
- Sentence scoring based on important words
- Maintains original sentence order in summary

## Error Responses

All endpoints return consistent error responses:

```json
{
  "error": "Bad Request",
  "detail": "Specific error message",
  "status_code": 400
}
```

### Common HTTP Status Codes

- `200` - Success
- `400` - Bad Request (invalid input, malformed data)
- `403` - Forbidden (invalid/missing API key)
- `408` - Request Timeout (external URL timeout)
- `422` - Validation Error (invalid field values)
- `429` - Too Many Requests (rate limit exceeded)
- `500` - Internal Server Error

### Error Examples

**Authentication Error:**
```json
{
  "detail": "Invalid or missing API secret."
}
```

**Validation Error:**
```json
{
  "detail": [
    {
      "loc": ["body", "markdown_text"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

**Rate Limit Error:**
```json
{
  "detail": "Rate limit exceeded. Please try again later."
}
```

## SDKs and Examples

### Python Example

```python
import requests

# Configuration
base_url = "https://dev-utility-api-vault.onrender.com"
headers = {"X-RapidAPI-Proxy-Secret": "your_secret_key"}

# Generate QR Code
response = requests.post(
    f"{base_url}/api/v1/qr-code",
    json={"data": "Hello, World!", "box_size": 15},
    headers=headers
)
qr_data = response.json()
print(f"QR Code: {qr_data['qr_code_base64'][:50]}...")

# Convert Markdown
response = requests.post(
    f"{base_url}/api/v1/markdown-to-html",
    json={"markdown_text": "# My Document\n\nThis is **important**."},
    headers=headers
)
html_data = response.json()
print(f"HTML: {html_data['html_content']}")
```

### JavaScript Example

```javascript
const baseUrl = 'https://dev-utility-api-vault.onrender.com';
const headers = {
  'Content-Type': 'application/json',
  'X-RapidAPI-Proxy-Secret': 'your_secret_key'
};

// Summarize text
async function summarizeText(text) {
  const response = await fetch(`${baseUrl}/api/v1/summarize`, {
    method: 'POST',
    headers: headers,
    body: JSON.stringify({
      text: text,
      sentence_count: 2
    })
  });
  
  const data = await response.json();
  return data.summary;
}
```

### cURL Examples

```bash
# Test regex pattern
curl -X POST "https://dev-utility-api-vault.onrender.com/api/v1/regex-tester" \
  -H "Content-Type: application/json" \
  -H "X-RapidAPI-Proxy-Secret: your_secret_key" \
  -d '{
    "pattern": "\\b\\w+@\\w+\\.\\w+\\b",
    "text": "Contact us at admin@example.com or support@test.org"
  }'

# Count words on webpage
curl -X POST "https://dev-utility-api-vault.onrender.com/api/v1/word-counter" \
  -H "Content-Type: application/json" \
  -H "X-RapidAPI-Proxy-Secret: your_secret_key" \
  -d '{"url": "https://example.com"}'
```

## Security Considerations

1. **Input Validation**: All inputs are validated and sanitized
2. **Rate Limiting**: 60 requests per minute per IP
3. **SSRF Protection**: URLs are validated to prevent server-side request forgery
4. **File Validation**: Uploaded files are checked for type and size
5. **ReDoS Protection**: Regex patterns are validated for safety
6. **Content Limits**: All inputs have reasonable size limits

## Support

- **Documentation**: [API Docs](https://dev-utility-api-vault.onrender.com/docs)
- **Issues**: [GitHub Issues](https://github.com/KrunalValvi/Dev_Api_Vault/issues)
- **Repository**: [GitHub Repo](https://github.com/KrunalValvi/Dev_Api_Vault)