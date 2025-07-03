# Standard Library Imports
import base64
import io
import re
from collections import defaultdict
import heapq

# Third-party Imports
import markdown
import qrcode
import requests
from bs4 import BeautifulSoup
from fastapi import APIRouter, HTTPException, File, UploadFile
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize

# Local Imports
from . import models

# Initialize Router
router = APIRouter(
    prefix="/api/v1",
    tags=["Utilities"]
)

# --- API Endpoints ---

@router.post("/markdown-to-html", response_model=models.HtmlResponse, summary="Convert Markdown to HTML")
async def convert_markdown_to_html(request: models.MarkdownRequest):
    """Converts a string of Markdown text into its HTML representation."""
    html_content = markdown.markdown(request.markdown_text)
    return {"html_content": html_content}

@router.post("/qr-code", response_model=models.QrCodeResponse, summary="Generate a QR Code")
async def generate_qr_code(request: models.QrCodeRequest):
    """Generates a QR code from the provided data and returns it as a base64 encoded PNG."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=request.box_size,
        border=request.border,
    )
    qr.add_data(str(request.data))
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    
    return {"qr_code_base64": f"data:image/png;base64,{img_str}"}

@router.post("/image-to-base64", response_model=models.Base64Response, summary="Convert Image to Base64")
async def image_to_base64(file: UploadFile = File(...)):
    """Encodes an uploaded image file into a base64 string."""
    contents = await file.read()
    base64_encoded_str = base64.b64encode(contents).decode("utf-8")
    return {"filename": file.filename, "base64_string": base64_encoded_str}

@router.post("/regex-tester", response_model=models.RegexResponse, summary="Test a Regular Expression")
async def test_regex(request: models.RegexRequest):
    """Finds all occurrences of a regex pattern within a given text."""
    try:
        matches = re.findall(request.pattern, request.text)
        return {"matches": matches}
    except re.error as e:
        raise HTTPException(status_code=400, detail=f"Invalid regular expression: {e}")


@router.post("/word-counter", response_model=models.WordCountResponse, summary="Count Words on a Webpage")
async def count_words_in_webpage(request: models.UrlRequest):
    """Fetches a webpage, extracts its text content, and returns word and character counts."""
    try:
        response = requests.get(str(request.url), timeout=10)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        
        soup = BeautifulSoup(response.content, 'html.parser')
        # Remove script and style elements to avoid counting code
        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()
            
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split(" "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        word_count = len(text.split())
        char_count = len(text)
        
        return {"url": str(request.url), "word_count": word_count, "char_count": char_count}
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Could not fetch URL: {e}")

@router.post("/summarize", response_model=models.SummaryResponse, summary="Summarize Text")
async def summarize_text(request: models.TextSummarizeRequest):
    """
    Performs a rule-based summarization of a given block of text using NLTK.
    This requires NLTK 'punkt' and 'stopwords' to be downloaded.
    """
    sentences = sent_tokenize(request.text)
    original_sentence_count = len(sentences)

    if original_sentence_count <= request.sentence_count:
        return {"original_sentence_count": original_sentence_count, "summary": request.text}

    stop_words = set(stopwords.words('english'))
    word_frequencies = defaultdict(int)
    for word in word_tokenize(request.text.lower()):
        if word.isalnum() and word not in stop_words:
            word_frequencies[word] += 1
    
    if not word_frequencies:
         return {"original_sentence_count": original_sentence_count, "summary": ' '.join(sentences[:request.sentence_count])}

    max_freq = max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word] / max_freq)

    sentence_scores = defaultdict(float)
    for i, sentence in enumerate(sentences):
        for word in word_tokenize(sentence.lower()):
            if word in word_frequencies:
                sentence_scores[i] += word_frequencies[word]
    
    summary_sentences_indices = heapq.nlargest(request.sentence_count, sentence_scores, key=sentence_scores.get)
    summary = ' '.join([sentences[i] for i in sorted(summary_sentences_indices)])
    
    return {"original_sentence_count": original_sentence_count, "summary": summary}