#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

echo "Downloading NLTK data..."
# Run NLTK downloader
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

echo "Build complete."