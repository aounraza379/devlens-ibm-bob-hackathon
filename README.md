# 🔍 DevLens - Repository Intelligence & Team Health Dashboard

A comprehensive engineering health check tool that analyzes code repositories, team sentiment, and automatically generates onboarding documentation.

## 🌟 Features

### 1. **Team Sentiment Analytics** 📊
- Analyzes Git commit messages and PR comments
- Detects team friction and development patterns
- Categorizes sentiment: Positive, Neutral, or Frustrated/Toxic
- Visual dashboards with charts and metrics

### 2. **Codebase Architecture Summarizer** 🏗️
- Summarizes complex source code files
- Extracts classes, functions, and imports
- Assesses code complexity
- Provides architectural insights

### 3. **Automated Playbook Generator** 📖
- Generates markdown onboarding documentation
- Creates structured developer guides
- Exports to Markdown and HTML formats
- Customizable for any project

## 🚀 Quick Start

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

## 📖 Usage Guide

### Tab 1: Team Sentiment Analytics

1. Choose input method: "Paste Text" or "Upload File"
2. Enter commit messages or PR comments (one per line)
3. Click "🔍 Analyze Sentiment"
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

1. Choose input method: "Paste Code" or "Upload Files"
2. Provide source code files (supports .py, .js, .java, .cpp, .ts, etc.)
3. Click "🔍 Analyze Code"
4. Review summaries, complexity metrics, and code structure

**Supported Languages:**
- Python (.py)
- JavaScript/TypeScript (.js, .ts, .jsx, .tsx)
- Java (.java)
- C/C++ (.c, .cpp)

### Tab 3: Automated Playbook Generator

1. First, analyze code in Tab 2
2. Enter your project name
3. Click "📖 Generate Playbook"
4. Download as Markdown or HTML

## 🛠️ Architecture

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
- Template-based generation system
- Optional Groq integration for natural language
- Exports to multiple formats (Markdown, HTML)

### Technology Stack

- **Frontend:** Streamlit
- **NLP:** TextBlob for sentiment analysis
- **AI Enhancement:** Groq (llama-3.3-70b-versatile) for code summaries
- **Visualization:** Plotly
- **Data Processing:** Pandas

## 💡 Configuration

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

## 📊 Example Outputs

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
- Lines: 847
```

## 🔧 Troubleshooting

### Common Issues

**1. Import Errors**
```bash
pip install --upgrade -r requirements.txt
```

**2. Memory Issues**
- Close other applications
- Application is lightweight with no model downloads
- Process fewer files at once if needed

**4. Streamlit Port Already in Use**
```bash
streamlit run app.py --server.port 8502
```

## 🎯 Use Cases

### For Engineering Managers
- Monitor team morale through commit sentiment
- Identify friction points in development
- Track communication patterns

### For Tech Leads
- Quickly understand new codebases
- Generate onboarding docs automatically
- Assess code complexity

### For Developers
- Get up to speed on projects faster
- Understand architectural patterns
- Create documentation effortlessly

## 🚧 Limitations

- Sentiment analysis accuracy depends on text quality
- Code summarization works best with well-structured code
- Large files (>10,000 lines) may take longer to process
- Groq API has rate limits (free tier: generous limits)

## 🔐 Privacy & Security

- Sentiment analysis happens locally with TextBlob
- Code summaries use Groq API only if key is provided
- No data is stored or transmitted without your consent
- API keys are never logged or shared
- Code analysis is performed in-memory

## 📈 Future Enhancements

- [ ] Support for more programming languages
- [ ] Git repository direct integration
- [ ] Team collaboration features
- [ ] Historical trend analysis
- [ ] Custom sentiment models
- [ ] CI/CD pipeline integration

## 🤝 Contributing

This is a hackathon MVP. Contributions welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - feel free to use for personal or commercial projects.

## 🙏 Acknowledgments

- Groq for lightning-fast LLM inference
- Streamlit for the amazing framework
- TextBlob for sentiment analysis
- The open-source community

## 📞 Support

For issues or questions:
- Open an issue on GitHub
- Check the troubleshooting section
- Review the usage guide

---

**Built with ❤️ for the developer community**

*DevLens - Making code repositories more transparent and teams healthier*