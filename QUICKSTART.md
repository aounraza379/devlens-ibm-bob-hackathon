# 🚀 DevLens Quick Start Guide

Get up and running with DevLens in 5 minutes!

## Step 1: Install Dependencies

### Windows
```bash
cd DevLens
run.bat
```

### Mac/Linux
```bash
cd DevLens
chmod +x run.sh
./run.sh
```

### Manual Installation
```bash
pip install -r requirements.txt
python -c "import nltk; nltk.download('punkt'); nltk.download('brown')"
streamlit run app.py
```

## Step 2: Open the Application

The app will automatically open in your browser at:
```
http://localhost:8501
```

## Step 3: Try the Features

### 🎯 Test Sentiment Analysis
1. Go to **Tab 1: Team Sentiment Analytics**
2. Click "Upload File" and select `example_commits.txt`
3. Click "🔍 Analyze Sentiment"
4. View the sentiment distribution and detailed analysis

### 🎯 Test Code Summarization
1. Go to **Tab 2: Codebase Architecture Summarizer**
2. Click "Upload Files" and select `example_code.py`
3. Click "🔍 Analyze Code"
4. Review the code structure and complexity metrics

### 🎯 Generate a Playbook
1. After analyzing code in Tab 2
2. Go to **Tab 3: Automated Playbook Generator**
3. Enter a project name (e.g., "User Management System")
4. Click "📖 Generate Playbook"
5. Download as Markdown or HTML

## Optional: Add Groq API Key

For enhanced AI-powered features:

1. Get a FREE API key from https://console.groq.com/
2. Copy `.env.example` to `.env`
3. Add your Groq API key:
   ```
   GROQ_API_KEY=gsk_your-key-here
   ```
4. Or enter it in the sidebar when running the app

## Troubleshooting

### Port Already in Use
```bash
streamlit run app.py --server.port 8502
```

### Missing Dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Groq API Issues
Make sure your API key is valid and has available credits.

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore all three tabs and features
- Try with your own code and commit messages
- Export results and playbooks

## Need Help?

Check the main README.md for:
- Detailed usage guide
- Architecture overview
- Troubleshooting tips
- Configuration options

---

**Happy analyzing! 🔍**