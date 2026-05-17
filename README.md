# DevLens - Repository Intelligence & Team Health Dashboard

A comprehensive engineering health check tool that analyzes code repositories, team sentiment, and automatically generates onboarding documentation.

## Features

### 1. Team Sentiment Analytics
- Analyzes Git commit messages and PR comments
- Detects team friction and development patterns
- Categorizes sentiment: Positive, Neutral, or Frustrated/Toxic
- Visual dashboards with charts and metrics

### 2. Codebase Architecture Summarizer
- Scans entire local repositories recursively
- Summarizes complex source code files
- Extracts classes, functions, and imports
- Assesses code complexity
- Provides architectural insights
- Supports 20+ programming languages

### 3. Automated Playbook Generator
- Generates markdown onboarding documentation using AI
- Creates structured developer guides with deep analysis
- Exports to Markdown and HTML formats
- Customizable for any project
- Uses Groq's llama-3.3-70b-versatile for intelligent generation

## Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or download the project:**
```bash
cd DevLens
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Download NLTK data (first time only):**
```python
python -c "import nltk; nltk.download('punkt'); nltk.download('brown')"
```

4. **(Optional) Set up Groq API key:**
```bash
cp .env.example .env
# Edit .env and add your Groq API key (get free at https://console.groq.com/)
```

### Running the Application

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

## Usage Guide

### Tab 1: Team Sentiment Analytics

1. Choose input method: "Paste Text" or "Upload File"
2. Enter commit messages or PR comments (one per line)
3. Click "Analyze Sentiment"
4. View sentiment distribution, detailed analysis, and export results

**Example Input:**
```
fix: resolved merge conflict
feat: added new authentication system
This PR looks great! Nice work
Why is this breaking again??
refactor: cleaned up legacy code
```

### Tab 2: Codebase Architecture Summarizer

**Option A: Scan Local Repository**
1. Enter the full path to your local repository (e.g., `C:/Users/YourName/Projects/my-repo`)
2. Click "Scan Repository"
3. The tool will recursively scan all supported code files
4. Review summaries, complexity metrics, and code structure

**Option B: Manual Upload**
1. Choose input method: "Paste Code" or "Upload Files"
2. Provide source code files
3. Click "Analyze Code"
4. Review results

**Supported Languages:**
- Python (.py)
- JavaScript/TypeScript (.js, .ts, .jsx, .tsx)
- Java (.java)
- C/C++ (.c, .cpp, .h)
- C# (.cs)
- Go (.go)
- Rust (.rs)
- PHP (.php)
- Ruby (.rb)
- Swift (.swift)
- Kotlin (.kt)
- Scala (.scala)
- HTML/CSS (.html, .css)
- Vue/Svelte (.vue, .svelte)

**Note on GitHub Repositories:**
To analyze a GitHub repository, first clone it locally:
```bash
git clone https://github.com/username/repository.git
cd repository
# Note the full path, then use it in DevLens
```

### Tab 3: Automated Playbook Generator

1. First, scan a repository or analyze code in Tab 2
2. Enter your project name
3. Click "Generate Playbook"
4. Download as Markdown or HTML

**With Groq API Key:** Generates intelligent, comprehensive playbooks with:
- Architecture Overview
- Module Relationships
- Technical Stack Analysis
- Complexity Analysis
- Step-by-Step Setup Guide
- Development Workflow
- Key Entry Points

**Without API Key:** Uses template-based generation with structured sections

## Architecture

### Core Engines

#### Engine A: Sentiment Analyzer
- Uses TextBlob for lightweight sentiment analysis
- No model downloads required
- Analyzes text polarity and categorizes emotions

#### Engine B: Code Summarizer
- Extracts code structure (classes, functions, imports)
- Assesses complexity levels
- Optional Groq integration for AI-enhanced summaries
- Rule-based fallback for offline use

#### Engine C: Playbook Generator
- Deep AI-powered generation using Groq's llama-3.3-70b-versatile
- Comprehensive context preparation from entire repository
- Template-based fallback when API key not provided
- Exports to multiple formats (Markdown, HTML)

### Technology Stack

- **Frontend:** Streamlit
- **NLP:** TextBlob for sentiment analysis
- **AI Enhancement:** Groq (llama-3.3-70b-versatile) for code summaries and playbooks
- **Visualization:** Plotly
- **Data Processing:** Pandas

## Configuration

### API Keys (Optional)

The application works without API keys using TextBlob. For enhanced features:

1. **Groq API Key:** Dramatically improves summarization and playbook quality
   - Get your FREE key from: https://console.groq.com/
   - Enter in the sidebar or set in `.env` file
   - Fast inference with llama-3.3-70b-versatile model

### Performance Tips

- **Without API Keys:** Uses TextBlob (lightweight, instant)
- **With Groq API:** Lightning-fast AI summaries, superior quality
- **Memory:** Minimal footprint, no model downloads required

## Example Outputs

### Sentiment Analysis Output
```json
{
  "overall_sentiment": "Positive",
  "positive_count": 3,
  "neutral_count": 1,
  "negative_count": 1,
  "average_polarity": 0.15
}
```

### Code Summary Output
```
File 'app.py' contains:
- 3 classes: SentimentAnalyzer, CodeSummarizer, PlaybookGenerator
- 15 functions: analyze_text, analyze_commits, summarize_code
- Complexity: Medium
- Lines: 1329
```

### Repository Scan Output
```
Successfully scanned 45 files
Total lines of code: 12,847
Complexity distribution:
- High: 5 files
- Medium: 18 files
- Low: 22 files
```

## Troubleshooting

### Common Issues

**1. Import Errors**
```bash
pip install --upgrade -r requirements.txt
```

**2. Path Not Found Error**
- Ensure the path exists and is correct
- Use forward slashes (/) or double backslashes (\\)
- Check that you have read permissions for the directory
- Example valid paths:
  - Windows: `C:/Users/YourName/Projects/my-repo`
  - Mac/Linux: `/home/username/projects/my-repo`

**3. Memory Issues**
- Close other applications
- Application is lightweight with no model downloads
- Process fewer files at once if needed

**4. Streamlit Port Already in Use**
```bash
streamlit run app.py --server.port 8502
```

**5. Groq API Issues**
- Verify your API key is valid
- Check rate limits (free tier has generous limits)
- Application will fall back to templates if API fails

## Use Cases

### For Engineering Managers
- Monitor team morale through commit sentiment
- Identify friction points in development
- Track communication patterns

### For Tech Leads
- Quickly understand new codebases
- Generate onboarding docs automatically
- Assess code complexity across projects

### For Developers
- Get up to speed on projects faster
- Understand architectural patterns
- Create documentation effortlessly

### For Open Source Contributors
- Analyze any GitHub repository (after cloning)
- Understand project structure quickly
- Generate contribution guides

## Limitations

- Sentiment analysis accuracy depends on text quality
- Code summarization works best with well-structured code
- Large repositories (>1000 files) may take longer to process
- Groq API has rate limits (free tier: generous limits)
- Requires local repository access (clone GitHub repos first)

## Privacy & Security

- Sentiment analysis happens locally with TextBlob
- Code summaries use Groq API only if key is provided
- No data is stored or transmitted without your consent
- API keys are never logged or shared
- Code analysis is performed in-memory
- Repository scanning is read-only

## Future Enhancements

- [ ] Direct GitHub API integration (no cloning needed)
- [ ] Support for more programming languages
- [ ] Team collaboration features
- [ ] Historical trend analysis
- [ ] Custom sentiment models
- [ ] CI/CD pipeline integration
- [ ] Export to PDF format

## Contributing

This is a hackathon MVP. Contributions welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - feel free to use for personal or commercial projects.

## Acknowledgments

- Groq for lightning-fast LLM inference
- Streamlit for the amazing framework
- TextBlob for sentiment analysis
- The open-source community

## Support

For issues or questions:
- Open an issue on GitHub
- Check the troubleshooting section
- Review the usage guide

---

**Built for the developer community**

*DevLens - Making code repositories more transparent and teams healthier*