"""
Test edge cases and additional scenarios for Dev API Vault.
"""

import pytest
import json
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import os

# Set test environment before importing app
os.environ["RAPIDAPI_PROXY_SECRET"] = "test_secret_key"
os.environ["FASTAPI_ENV"] = "development"

from app.main import app

client = TestClient(app)
test_headers = {"X-RapidAPI-Proxy-Secret": "test_secret_key"}

class TestEdgeCases:
    """Test edge cases and additional scenarios."""
    
    # Test Markdown to HTML with XSS attempts
    def test_markdown_xss_prevention(self):
        """Test that XSS attempts in markdown are properly escaped."""
        xss_payload = "<script>alert('XSS')</script>"
        response = client.post(
            "/api/v1/markdown-to-html",
            json={"markdown_text": xss_payload},
            headers=test_headers
        )
        assert response.status_code == 200
        data = response.json()
        # The script tag should be escaped, not executed
        assert "&lt;script&gt;" in data["html_content"]
        assert "<script>" not in data["html_content"]

    # Test QR Code with special characters
    def test_qr_code_special_chars(self):
        """Test QR code generation with special characters."""
        special_text = "!@#$%^&*()_+{}|:\"<>?~`-=[]\\;',./"
        response = client.post(
            "/api/v1/qr-code",
            json={"data": special_text},
            headers=test_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["qr_code_base64"].startswith("data:image/png;base64,")

    # Test image upload with large file
    def test_large_image_upload(self):
        """Test that large image uploads are rejected."""
        # Create a large file (5.1 MB)
        large_file = b"x" * (5 * 1024 * 1024 + 1)  # 5MB + 1 byte
        
        with patch("tempfile.NamedTemporaryFile") as mock_temp:
            mock_temp.return_value.__enter__.return_value = MagicMock()
            mock_temp.return_value.__enter__.return_value.tell.return_value = 5 * 1024 * 1024 + 1
            
            response = client.post(
                "/api/v1/image-to-base64",
                files={"file": ("large.png", large_file, "image/png")},
                headers=test_headers
            )
            
            assert response.status_code == 413  # Payload Too Large

    # Test regex with potential ReDoS patterns
    def test_regex_redos_protection(self):
        """Test that potentially dangerous regex patterns are caught."""
        evil_pattern = r"^(a+)+$"
        evil_input = "a" * 1000 + "!"
        
        response = client.post(
            "/api/v1/regex-tester",
            json={"pattern": evil_pattern, "text": evil_input},
            headers=test_headers
        )
        
        # Should either reject the pattern or handle it safely
        assert response.status_code in [200, 400, 422]
        if response.status_code == 200:
            data = response.json()
            assert "matches" in data

    # Test word counter with malformed HTML
    @patch('app.routers.requests.get')
    def test_word_counter_malformed_html(self, mock_get):
        """Test word counter with malformed HTML content."""
        # Mock response with malformed HTML
        mock_response = MagicMock()
        mock_response.text = """<html><body><p>Test content</p><p>More content</body>"""
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        response = client.post(
            "/api/v1/word-counter",
            json={"url": "http://example.com"},
            headers=test_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["word_count"] > 0

    # Test summarizer with non-English text
    def test_summarizer_non_english(self):
        """Test text summarization with non-English text."""
        spanish_text = """
        El aprendizaje automático es una rama de la inteligencia artificial que se centra en el desarrollo 
        de sistemas que pueden aprender de los datos. Estos sistemas mejoran su rendimiento con la experiencia.
        El aprendizaje automático se utiliza en una amplia variedad de aplicaciones, como el reconocimiento 
        de voz, la visión por computadora y el procesamiento del lenguaje natural.
        """
        
        response = client.post(
            "/api/v1/summarize",
            json={"text": spanish_text, "max_sentences": 1},
            headers=test_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "summary" in data
        assert len(data["summary"].split(". ")) <= 2  # Should be 1-2 sentences

    # Test rate limiting
    def test_rate_limiting(self):
        """Test that rate limiting is working."""
        # Make multiple requests in quick succession
        for _ in range(15):  # Should be more than the rate limit
            response = client.get("/", headers=test_headers)
            
            # After rate limit is hit, we should get 429
            if response.status_code == 429:
                assert "Retry-After" in response.headers
                break
        else:
            # If we get here, rate limiting might not be working
            pytest.fail("Rate limiting not triggered")

    # Test invalid JSON
    def test_invalid_json(self):
        """Test handling of invalid JSON in request body."""
        response = client.post(
            "/api/v1/markdown-to-html",
            content="{"invalid": json",  # Malformed JSON
            headers={"Content-Type": "application/json", **test_headers}
        )
        assert response.status_code == 422  # Unprocessable Entity

    # Test CORS headers
    def test_cors_headers(self):
        """Test that CORS headers are properly set."""
        response = client.options(
            "/",
            headers={
                "Origin": "http://example.com",
                "Access-Control-Request-Method": "GET",
                **test_headers
            }
        )
        assert response.status_code == 200
        assert "access-control-allow-origin" in response.headers

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
