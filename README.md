# DevUtility API Vault

A collection of useful developer utilities, built with Python and FastAPI. This project serves as a live, deployable API and a complete source code package for learning and building upon.

**Live API Link:** [https://dev-utility-api-vault.onrender.com](https://dev-utility-api-vault.onrender.com) (This is a placeholder, replace with your actual Render URL)

**API Documentation (Swagger UI):** [YOUR_LIVE_API_URL/docs](https://dev-utility-api-vault.onrender.com/docs)

---

## Features

This API provides 6 distinct, ready-to-use utility endpoints:

1.  **Markdown to HTML:** Convert Markdown text into HTML.
2.  **QR Code Generator:** Create a QR code from any string and get a base64 PNG image back.
3.  **Image to Base64:** Upload an image and receive its base64 encoded string.
4.  **Regex Tester:** Test regular expression patterns against a string of text.
5.  **Webpage Word Counter:** Scrape a public webpage and count its words and characters.
6.  **Text Summarizer:** A simple rule-based summarizer to get the key sentences from a block of text.

## Technology Stack

*   **Backend Framework:** [FastAPI](https://fastapi.tiangolo.com/)
*   **Server:** [Uvicorn](https://www.uvicorn.org/)
*   **Data Validation:** [Pydantic](https://pydantic-docs.helpmanual.io/)
*   **Language:** Python 3.9+
*   **Testing:** [Pytest](https://pytest.org/) & [HTTPX](https://www.python-httpx.org/)
*   **Key Libraries:** `requests`, `beautifulsoup4`, `python-markdown`, `qrcode`, `nltk`

## Local Setup Instructions

To run this project on your local machine, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/YOUR_USERNAME/dev-utility-api-vault.git
    cd dev-utility-api-vault
    ```

2.  **Create and activate a Python virtual environment:**
    ```bash
    # For macOS/Linux
    python3 -m venv .venv
    source .venv/bin/activate

    # For Windows
    python -m venv .venv
    .venv\Scripts\activate
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Download NLTK data (for the summarizer):**
    Run the `build.sh` script or execute the Python command manually.
    ```bash
    # Option 1: Run the build script
    ./build.sh

    # Option 2: Run Python command manually
    python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
    ```

5.  **Run the development server:**
    ```bash
    uvicorn app.main:app --reload
    ```

6.  **Access the API:**
    *   **API Root:** [http://127.0.0.1:8000](http://127.0.0.1:8000)
    *   **Interactive Docs:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Running Tests

To run the test suite, execute the following command from the project root directory:

```bash
pytest