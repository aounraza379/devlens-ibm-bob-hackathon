#!/bin/bash

echo "Starting DevLens - Repository Intelligence Dashboard"
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt
echo ""
echo "Downloading NLTK data..."
python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('brown', quiet=True)"
echo ""
echo "Starting Streamlit application..."
streamlit run app.py

# Made with Bob
