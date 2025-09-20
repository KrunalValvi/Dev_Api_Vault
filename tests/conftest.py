"""
Configuration for pytest.
Sets up test environment and fixtures.
"""

import pytest
import os
from fastapi.testclient import TestClient


def pytest_configure(config):
    """Configure pytest with test environment variables."""
    # Set test environment variables
    os.environ["RAPIDAPI_PROXY_SECRET"] = "test_secret_key"
    os.environ["FASTAPI_ENV"] = "development"
    os.environ["DEBUG"] = "true"


@pytest.fixture(scope="session")
def test_client():
    """Create a test client for the FastAPI app."""
    from app.main import app
    return TestClient(app)


@pytest.fixture
def test_headers():
    """Provide test headers with authentication."""
    return {"X-RapidAPI-Proxy-Secret": "test_secret_key"}


@pytest.fixture
def sample_markdown():
    """Provide sample markdown text for testing."""
    return """
# Sample Document

This is a **bold** text and this is *italic* text.

## Code Example

```python
def hello_world():
    print("Hello, World!")
```

## List Example

- Item 1
- Item 2
- Item 3

| Column 1 | Column 2 |
|----------|----------|
| Cell 1   | Cell 2   |
"""


@pytest.fixture
def sample_long_text():
    """Provide sample long text for summarization testing."""
    return """
    Natural language processing (NLP) is a subfield of linguistics, computer science, 
    and artificial intelligence concerned with the interactions between computers and 
    human language. In particular, how to program computers to process and analyze 
    large amounts of natural language data. The goal is a computer capable of 
    understanding the contents of documents, including the contextual nuances of 
    the language within them.
    
    The technology can then accurately extract information and insights contained 
    in the documents as well as categorize and organize the documents themselves. 
    Challenges in natural language processing frequently involve speech recognition, 
    natural language understanding, and natural language generation.
    
    Natural language processing has its roots in the 1950s. Already in 1950, 
    Alan Turing published an article titled "Computing Machinery and Intelligence" 
    which proposed what is now called the Turing test as a criterion of intelligence. 
    The Georgetown experiment in 1954 involved fully automatic translation of more 
    than sixty Russian sentences into English.
    
    The authors claimed that within three or five years, machine translation would 
    be a solved problem. However, real progress was much slower, and after the 
    ALPAC report in 1966, which found that ten-year-long research had failed to 
    fulfill the expectations, funding for machine translation was dramatically reduced.
    """