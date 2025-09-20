"""
Comprehensive test suite for Dev API Vault.
Tests all API endpoints with various scenarios including edge cases and error conditions.
"""

import pytest
import base64
import tempfile
import os
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock

# Set test environment before importing app
os.environ["RAPIDAPI_PROXY_SECRET"] = "test_secret_key"
os.environ["FASTAPI_ENV"] = "development"

from app.main import app

# Initialize the test client
client = TestClient(app)

# Test headers for authenticated requests
test_headers = {"X-RapidAPI-Proxy-Secret": "test_secret_key"}


class TestHealthChecks:
    """Test health check endpoints."""
    
    def test_root_endpoint(self):
        """Test the root endpoint for a successful response."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "Welcome to Dev API Vault!" in data["message"]
        assert "version" in data
        assert "environment" in data

    def test_health_endpoint(self):
        """Test the detailed health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "api_version" in data
        assert "environment" in data
        assert "debug_mode" in data


class TestMarkdownToHtml:
    """Test markdown to HTML conversion endpoint."""
    
    def test_markdown_to_html_success(self):
        """Test successful markdown to HTML conversion."""
        response = client.post(
            "/api/v1/markdown-to-html",
            json={"markdown_text": "# Title\n\n**bold text**"},
            headers=test_headers
        )
        assert response.status_code == 200
        data = response.json()
        # API correctly generates HTML with IDs and proper structure
        assert "<h1" in data["html_content"]
        assert "Title" in data["html_content"]
        assert "<strong>bold text</strong>" in data["html_content"]

    def test_markdown_to_html_empty_text(self):
        """Test markdown conversion with empty text."""
        response = client.post(
            "/api/v1/markdown-to-html", 
            json={"markdown_text": "   "},
            headers=test_headers
        )
        assert response.status_code == 422  # Validation error

    def test_markdown_to_html_very_long_text(self):
        """Test markdown conversion with text exceeding limits."""
        long_text = "# Header\n" + "A" * 20000  # Exceeds 10k limit
        response = client.post(
            "/api/v1/markdown-to-html",
            json={"markdown_text": long_text},
            headers=test_headers
        )
        assert response.status_code == 422  # Pydantic validation error    def test_markdown_to_html_with_tables(self):
    def test_markdown_to_html_with_tables(self):
        """Test markdown conversion with table-like text."""
        markdown_table = """
| Column 1 | Column 2 |
|----------|----------|
| Cell 1   | Cell 2   |
"""
        response = client.post(
            "/api/v1/markdown-to-html", 
            json={"markdown_text": markdown_table},
            headers=test_headers
        )
        assert response.status_code == 200
        data = response.json()
        # Basic markdown renders tables as paragraphs without table extension
        assert "<p>" in data["html_content"]
        assert "Column 1" in data["html_content"]
        assert "Cell 1" in data["html_content"]


class TestQrCodeGeneration:
    """Test QR code generation endpoint."""
    
    def test_qr_code_generation_success(self):
        """Test successful QR code generation."""
        response = client.post(
            "/api/v1/qr-code", 
            json={"data": "test data", "box_size": 10, "border": 4},
            headers=test_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert "qr_code_base64" in data
        assert data["qr_code_base64"].startswith("data:image/png;base64,")

    def test_qr_code_custom_size(self):
        """Test QR code with custom size parameters."""
        response = client.post(
            "/api/v1/qr-code", 
            json={"data": "https://example.com", "box_size": 15, "border": 2},
            headers=test_headers
        )
        assert response.status_code == 200

    def test_qr_code_size_limits(self):
        """Test QR code with size parameters exceeding limits."""
        response = client.post(
            "/api/v1/qr-code", 
            json={"data": "test", "box_size": 100, "border": 50},  # Exceeds limits (max 50, 20)
            headers=test_headers
        )
        assert response.status_code == 422  # Validation error for invalid parameters

    def test_qr_code_very_long_data(self):
        """Test QR code with data exceeding limits."""
        long_data = "A" * 3000  # Exceeds 2k limit
        response = client.post(
            "/api/v1/qr-code",
            json={"data": long_data},
            headers=test_headers
        )
        assert response.status_code == 422  # Pydantic validation error
class TestImageToBase64:
    """Test image to base64 conversion endpoint."""
    
    def test_image_to_base64_success(self):
        """Test successful image conversion."""
        # Create a simple test image
        test_image_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x01\x00\x00\x00\x007n\xf9$\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xdb\x00\x00\x00\x00IEND\xaeB`\x82'
        
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
            tmp_file.write(test_image_data)
            tmp_file.flush()
            
            with open(tmp_file.name, 'rb') as f:
                response = client.post(
                    "/api/v1/image-to-base64",
                    files={"file": ("test.png", f, "image/png")},
                    headers=test_headers
                )
        
        os.unlink(tmp_file.name)
        
        assert response.status_code == 200
        data = response.json()
        assert "base64_string" in data
        assert "filename" in data
        assert "file_size" in data
        assert "content_type" in data

    def test_image_to_base64_invalid_file_type(self):
        """Test image conversion with invalid file type."""
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as tmp_file:
            tmp_file.write(b"This is not an image")
            tmp_file.flush()
            
            with open(tmp_file.name, 'rb') as f:
                response = client.post(
                    "/api/v1/image-to-base64",
                    files={"file": ("test.txt", f, "text/plain")},
                    headers=test_headers
                )
        
        os.unlink(tmp_file.name)
        assert response.status_code == 400


class TestRegexTester:
    """Test regex testing endpoint."""
    
    def test_regex_tester_success(self):
        """Test successful regex matching."""
        response = client.post(
            "/api/v1/regex-tester", 
            json={"pattern": r"\b\w{4}\b", "text": "This is a test sentence."},
            headers=test_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert "matches" in data
        assert "match_count" in data
        assert "This" in data["matches"]
        assert "test" in data["matches"]

    def test_regex_tester_invalid_pattern(self):
        """Test regex with invalid pattern."""
        response = client.post(
            "/api/v1/regex-tester", 
            json={"pattern": "[invalid", "text": "test text"},
            headers=test_headers
        )
        assert response.status_code == 422  # Validation error

    def test_regex_tester_no_matches(self):
        """Test regex with no matches."""
        response = client.post(
            "/api/v1/regex-tester", 
            json={"pattern": r"\d+", "text": "no numbers here"},
            headers=test_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["matches"] == []
        assert data["match_count"] == 0

    def test_regex_tester_many_matches(self):
        """Test regex with many matches (should be limited)."""
        text_with_many_numbers = " ".join([str(i) for i in range(2000)])
        response = client.post(
            "/api/v1/regex-tester", 
            json={"pattern": r"\d+", "text": text_with_many_numbers},
            headers=test_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["matches"]) <= 1000  # Should be limited


class TestWordCounter:
    """Test webpage word counter endpoint."""
    
    @patch('app.routers.safe_web_request')
    def test_word_counter_success(self, mock_request):
        """Test successful word counting."""
        mock_response = Mock()
        mock_response.content = b'<html><head><title>Test Page</title></head><body><p>Hello world test</p></body></html>'
        mock_response.status_code = 200
        mock_request.return_value = mock_response
        
        response = client.post(
            "/api/v1/word-counter", 
            json={"url": "https://example.com"},
            headers=test_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert "word_count" in data
        assert "char_count" in data
        assert "title" in data
        assert "status_code" in data
        assert data["word_count"] == 5  # "Test Page" + "Hello world test" = 5 words

    def test_word_counter_invalid_url(self):
        """Test word counter with invalid URL."""
        response = client.post(
            "/api/v1/word-counter", 
            json={"url": "http://invalid.url.that.does.not.exist.local"},
            headers=test_headers
        )
        assert response.status_code == 400


class TestTextSummarizer:
    """Test text summarization endpoint."""
    
    def test_summarizer_success(self):
        """Test successful text summarization."""
        text = (
            "The quick brown fox jumps over the lazy dog. This is the first sentence. "
            "The lazy dog, however, was not impressed. This is the second sentence. "
            "He simply rolled over and went back to sleep. This is the third sentence. "
            "The fox, defeated, went to find a less lazy animal. This is the fourth sentence."
        )
        response = client.post(
            "/api/v1/summarize", 
            json={"text": text, "sentence_count": 2},
            headers=test_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["original_sentence_count"] == 8  # API correctly counts all sentences including descriptions
        assert data["summary_sentence_count"] <= 2
        assert "summary" in data

    def test_summarizer_short_text(self):
        """Test summarization with text failing minimum word requirement."""
        short_text = "This is a short text. Only two sentences here."  # 9 words < 10 minimum
        response = client.post(
            "/api/v1/summarize", 
            json={"text": short_text, "sentence_count": 5},
            headers=test_headers
        )
        assert response.status_code == 422  # Validation error for insufficient words

    def test_summarizer_very_short_text(self):
        """Test summarization with text too short."""
        short_text = "Too short."
        response = client.post(
            "/api/v1/summarize", 
            json={"text": short_text, "sentence_count": 1},
            headers=test_headers
        )
        assert response.status_code == 422  # Validation error

    def test_summarizer_empty_text(self):
        """Test summarization with empty text."""
        response = client.post(
            "/api/v1/summarize", 
            json={"text": "   ", "sentence_count": 1},
            headers=test_headers
        )
        assert response.status_code == 422  # Validation error


class TestSecurity:
    """Test security and authentication."""
    
    def test_missing_api_key(self):
        """Test API call without authentication header."""
        response = client.post(
            "/api/v1/markdown-to-html", 
            json={"markdown_text": "# Test"}
        )
        # Should pass in development mode without key
        assert response.status_code in [200, 403]

    def test_invalid_api_key(self):
        """Test API call with invalid authentication header."""
        invalid_headers = {"X-RapidAPI-Proxy-Secret": "wrong_key"}
        response = client.post(
            "/api/v1/markdown-to-html", 
            json={"markdown_text": "# Test"},
            headers=invalid_headers
        )
        assert response.status_code == 403

    def test_valid_api_key(self):
        """Test API call with valid authentication header."""
        response = client.post(
            "/api/v1/markdown-to-html", 
            json={"markdown_text": "# Test"},
            headers=test_headers
        )
        assert response.status_code == 200


class TestErrorHandling:
    """Test error handling scenarios."""
    
    def test_malformed_json(self):
        """Test handling of malformed JSON."""
        response = client.post(
            "/api/v1/markdown-to-html",
            data="{invalid json}",
            headers={**test_headers, "Content-Type": "application/json"}
        )
        assert response.status_code == 422

    def test_missing_required_fields(self):
        """Test handling of missing required fields."""
        response = client.post(
            "/api/v1/markdown-to-html",
            json={},  # Missing markdown_text
            headers=test_headers
        )
        assert response.status_code == 422

    def test_invalid_field_types(self):
        """Test handling of invalid field types."""
        response = client.post(
            "/api/v1/qr-code",
            json={"data": "test", "box_size": "not_a_number"},
            headers=test_headers
        )
        assert response.status_code == 422


if __name__ == "__main__":
    pytest.main([__file__, "-v"])