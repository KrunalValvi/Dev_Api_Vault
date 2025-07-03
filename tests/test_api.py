import pytest
from fastapi.testclient import TestClient
from app.main import app

# Initialize the test client
client = TestClient(app)

# --- Test Cases ---

def test_read_main():
    """Test the root endpoint for a successful response."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "Welcome to DevUtility API Vault!"}

def test_markdown_to_html_happy_path():
    """Test the markdown-to-html endpoint with valid input."""
    response = client.post("/api/v1/markdown-to-html", json={"markdown_text": "# Title\n\n*bold*"})
    assert response.status_code == 200
    assert response.json() == {"html_content": "<h1>Title</h1>\n<p><em>bold</em></p>"}

def test_qr_code_generator_happy_path():
    """Test the qr-code endpoint to ensure it returns a base64 string."""
    response = client.post("/api/v1/qr-code", json={"data": "test data", "box_size": 10, "border": 4})
    assert response.status_code == 200
    data = response.json()
    assert "qr_code_base64" in data
    assert data["qr_code_base64"].startswith("data:image/png;base64,")

def test_word_counter_invalid_url():
    """Test the word-counter endpoint with a URL that is expected to fail."""
    # Note: We use a non-routable address to ensure the test fails for the right reason.
    response = client.post("/api/v1/word-counter", json={"url": "http://invalid.url.that.does.not.exist.local"})
    assert response.status_code == 400
    assert "Could not fetch URL" in response.json()["detail"]

def test_regex_tester_happy_path():
    """Test the regex-tester endpoint with a valid pattern."""
    response = client.post("/api/v1/regex-tester", json={"pattern": "\\b\\w{4}\\b", "text": "This is a test sentence."})
    assert response.status_code == 200
    assert response.json() == {"matches": ["This", "test"]}

def test_summarizer_happy_path():
    """Test the summarizer endpoint with a reasonable block of text."""
    text = (
        "The quick brown fox jumps over the lazy dog. This is the first sentence. "
        "The lazy dog, however, was not impressed. This is the second sentence. "
        "He simply rolled over and went back to sleep. This is the third sentence. "
        "The fox, defeated, went to find a less lazy animal. This is the fourth."
    )
    response = client.post("/api/v1/summarize", json={"text": text, "sentence_count": 2})
    assert response.status_code == 200
    data = response.json()
    assert data["original_sentence_count"] == 4
    # The exact summary can vary, so we check for key components
    assert "fox" in data["summary"]
    assert "dog" in data["summary"]
    assert len(data["summary"].split('. ')) <= 3 # Check it's roughly 2 sentences