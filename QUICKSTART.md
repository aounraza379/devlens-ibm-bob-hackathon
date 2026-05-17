# DevLens Quick Start Guide

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

### Test Sentiment Analysis
1. Go to **Tab 1: Team Sentiment Analytics**
2. Click "Upload File" and select `example_commits.txt` (if available)
3. Or paste sample commit messages
4. Click "Analyze Sentiment"
5. View the sentiment distribution and detailed analysis

### Test Code Summarization

**Option A: Scan a Local Repository**
1. Go to **Tab 2: Codebase Architecture Summarizer**
2. Enter the full path to a local repository
   - Example: `C:/Users/YourName/Projects/my-repo`
   - Or use the DevLens project itself: `C:/Users/Aoun/Desktop/DevLens`
3. Click "Scan Repository"
4. Review the code structure and complexity metrics

**Option B: Upload Individual Files**
1. Go to **Tab 2: Codebase Architecture Summarizer**
2. Click "Upload Files" and select `example_code.py` or any code file
3. Click "Analyze Code"
4. Review the code structure and complexity metrics

### Generate a Playbook
1. After analyzing code in Tab 2
2. Go to **Tab 3: Automated Playbook Generator**
3. Enter a project name (e.g., "User Management System")
4. Click "Generate Playbook"
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

## Testing with GitHub Repositories

To analyze any GitHub repository:

1. Clone the repository locally:
   ```bash
   git clone https://github.com/username/repository.git
   cd repository
   pwd  # Note this path
   ```

2. Use the path in DevLens:
   - Windows: `C:/Users/YourName/repository`
   - Mac/Linux: `/home/username/repository`

3. DevLens will scan all supported code files recursively

## Troubleshooting

### Port Already in Use
```bash
streamlit run app.py --server.port 8502
```

### Missing Dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Path Not Found
- Ensure the path exists and is correct
- Use forward slashes (/) or double backslashes (\\)
- Check read permissions for the directory

### Groq API Issues
Make sure your API key is valid and has available credits.

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore all three tabs and features
- Try with your own code and commit messages
- Export results and playbooks
- Test with different repositories

## Testing Checklist

**Tab 1: Sentiment Analysis**
- [ ] Paste commit messages and analyze
- [ ] Upload a text file with commits
- [ ] Export results as JSON

**Tab 2: Code Summarization**
- [ ] Scan a local repository
- [ ] Upload individual code files
- [ ] Review complexity metrics
- [ ] Check file summaries

**Tab 3: Playbook Generation**
- [ ] Generate playbook without API key (template mode)
- [ ] Generate playbook with API key (AI mode)
- [ ] Download as Markdown
- [ ] Download as HTML

## Need Help?

Check the main README.md for:
- Detailed usage guide
- Architecture overview
- Troubleshooting tips
- Configuration options

---

**Happy analyzing!**