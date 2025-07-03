from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional

# 1. Markdown to HTML
class MarkdownRequest(BaseModel):
    markdown_text: str = Field(..., example="# Hello World", description="The Markdown text to convert.")

class HtmlResponse(BaseModel):
    html_content: str = Field(..., example="<h1>Hello World</h1>", description="The resulting HTML content.")

# 2. QR Code Generator
class QrCodeRequest(BaseModel):
    data: str = Field(..., example="https://fastapi.tiangolo.com/", description="The data to encode in the QR code.")
    box_size: int = Field(10, gt=0, description="Size of each box in the QR code grid.")
    border: int = Field(4, ge=0, description="Thickness of the border in boxes.")

class QrCodeResponse(BaseModel):
    qr_code_base64: str = Field(..., description="Base64 encoded PNG image of the QR code, ready for use in an <img> tag.")

# 3. Image to Base64
class Base64Response(BaseModel):
    filename: str
    base64_string: str

# 4. Regex Tester
class RegexRequest(BaseModel):
    pattern: str = Field(..., example="\\d+", description="The regular expression pattern.")
    text: str = Field(..., example="My number is 12345.", description="The text to search within.")

class RegexResponse(BaseModel):
    matches: List[str]

# 5. Webpage Word Counter
class UrlRequest(BaseModel):
    url: HttpUrl = Field(..., example="https://example.com", description="The URL of the webpage to analyze.")

class WordCountResponse(BaseModel):
    url: str
    word_count: int
    char_count: int

# 6. Rule-based Text Summarizer
class TextSummarizeRequest(BaseModel):
    text: str = Field(..., min_length=50, description="Text to be summarized.")
    sentence_count: int = Field(3, gt=0, description="Number of sentences in the final summary.")

class SummaryResponse(BaseModel):
    original_sentence_count: int
    summary: str