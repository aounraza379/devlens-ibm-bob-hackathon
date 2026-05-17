# DevLens - Comprehensive Testing & Demo Guide

This guide provides step-by-step instructions for testing all features and demonstrating the DevLens project.

## Table of Contents
1. [Pre-Testing Setup](#pre-testing-setup)
2. [Feature Testing](#feature-testing)
3. [Demo Scenarios](#demo-scenarios)
4. [Using External Repositories](#using-external-repositories)
5. [Troubleshooting](#troubleshooting)

---

## Pre-Testing Setup

### 1. Environment Setup
```bash
# Navigate to project directory
cd DevLens

# Install dependencies
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('brown')"

# Start the application
streamlit run app.py
```

### 2. Optional: Groq API Key Setup
For AI-powered playbook generation:
1. Visit https://console.groq.com/
2. Sign up for a free account
3. Generate an API key
4. Enter it in the sidebar OR add to `.env` file

---

## Feature Testing

### Test 1: Team Sentiment Analytics

**Objective:** Verify sentiment analysis works correctly

**Test Data:**
```
fix: resolved critical bug in authentication
feat: added amazing new dashboard feature
This code is terrible and needs complete rewrite
Great work on this PR! Very clean implementation
Why does this keep breaking every release??
refactor: improved performance by 50%
```

**Steps:**
1. Open Tab 1: "Team Sentiment Analytics"
2. Select "Paste Text" option
3. Paste the test data above
4. Click "Analyze Sentiment"

**Expected Results:**
- Overall sentiment should be calculated
- Pie chart showing distribution (Positive/Neutral/Negative)
- Bar chart with counts
- Detailed analysis for each message
- Ability to export as JSON

**Success Criteria:**
- [ ] Sentiment analysis completes without errors
- [ ] Charts display correctly
- [ ] Individual messages are categorized
- [ ] Export functionality works

---

### Test 2: Code Summarization - Manual Upload

**Objective:** Verify code analysis works with uploaded files

**Test Data:** Use the `example_code.py` file or create a simple Python file:
```python
class UserManager:
    def __init__(self):
        self.users = []
    
    def add_user(self, name, email):
        user = {"name": name, "email": email}
        self.users.append(user)
        return user
    
    def get_user(self, email):
        for user in self.users:
            if user["email"] == email:
                return user
        return None
```

**Steps:**
1. Open Tab 2: "Codebase Architecture Summarizer"
2. Scroll to "Manual File Upload" section
3. Select "Upload Files"
4. Upload the test file
5. Click "Analyze Code"

**Expected Results:**
- File is analyzed successfully
- Summary shows classes and functions
- Complexity level is assigned
- Structure details are displayed

**Success Criteria:**
- [ ] File uploads successfully
- [ ] Code structure is extracted
- [ ] Complexity is calculated
- [ ] Summary is generated

---

### Test 3: Repository Scanning - Local Project

**Objective:** Verify full repository scanning works

**Test Options:**

**Option A: Test with DevLens itself**
```
Path: C:/Users/Aoun/Desktop/DevLens
(Adjust to your actual path)
```

**Option B: Test with any local project**
```
Path: C:/Users/YourName/Projects/your-project
```

**Steps:**
1. Open Tab 2: "Codebase Architecture Summarizer"
2. In "Local Repository Scanner" section
3. Enter the full path to a repository
4. Click "Scan Repository"

**Expected Results:**
- Success message with file count
- All code files are discovered
- Each file is analyzed
- Statistics are displayed (files, lines, classes, functions)
- Complexity distribution chart appears

**Success Criteria:**
- [ ] Repository path is validated
- [ ] Files are scanned recursively
- [ ] Ignored directories are skipped (venv, node_modules, .git)
- [ ] All supported file types are processed
- [ ] Results are stored in session state

---

### Test 4: Playbook Generation - Without API Key

**Objective:** Verify template-based playbook generation

**Prerequisites:** Complete Test 3 first

**Steps:**
1. Ensure NO Groq API key is entered in sidebar
2. Open Tab 3: "Automated Playbook Generator"
3. Enter project name: "Test Project"
4. Click "Generate Playbook"

**Expected Results:**
- Warning about no API key
- Template-based playbook is generated
- Playbook includes:
  - Project Overview
  - Architecture Summary
  - File details
  - Getting Started guide
  - Key Components
  - Best Practices
- Download buttons appear (Markdown & HTML)

**Success Criteria:**
- [ ] Playbook generates without errors
- [ ] All sections are present
- [ ] File information is included
- [ ] Downloads work correctly

---

### Test 5: Playbook Generation - With API Key

**Objective:** Verify AI-powered playbook generation

**Prerequisites:** 
- Complete Test 3 first
- Have valid Groq API key

**Steps:**
1. Enter Groq API key in sidebar
2. Open Tab 3: "Automated Playbook Generator"
3. Enter project name: "Test Project"
4. Click "Generate Playbook"

**Expected Results:**
- Success message about Groq AI enabled
- AI-generated playbook with:
  - Architecture Overview
  - Module Relationships
  - Technical Stack
  - Code Organization
  - Complexity Analysis
  - Environment Setup
  - Development Workflow
  - Key Entry Points
- More detailed and intelligent content than template
- Download buttons work

**Success Criteria:**
- [ ] API key is accepted
- [ ] Groq API call succeeds
- [ ] AI-generated content is comprehensive
- [ ] Content is well-structured
- [ ] Downloads work correctly

---

## Demo Scenarios

### Scenario 1: Quick Demo (5 minutes)

**Purpose:** Show all three features quickly

1. **Sentiment Analysis (1 min)**
   - Paste 5-6 commit messages
   - Show sentiment distribution
   - Highlight positive vs negative detection

2. **Code Analysis (2 min)**
   - Upload a single Python file
   - Show extracted classes/functions
   - Explain complexity levels

3. **Playbook Generation (2 min)**
   - Generate playbook from analyzed code
   - Show markdown output
   - Download as HTML

### Scenario 2: Full Repository Analysis (10 minutes)

**Purpose:** Demonstrate enterprise-level capabilities

1. **Setup (1 min)**
   - Show Groq API key configuration
   - Explain benefits of AI enhancement

2. **Repository Scan (3 min)**
   - Enter path to a real project
   - Show scanning progress
   - Display statistics and complexity distribution

3. **Deep Analysis (3 min)**
   - Review individual file summaries
   - Show class and function extraction
   - Explain complexity metrics

4. **AI Playbook (3 min)**
   - Generate comprehensive playbook
   - Show AI-generated insights
   - Download and preview

### Scenario 3: Team Health Check (8 minutes)

**Purpose:** Focus on sentiment analysis for team management

1. **Collect Data (2 min)**
   - Show how to export Git commit messages
   - Demonstrate file upload

2. **Analysis (3 min)**
   - Run sentiment analysis
   - Interpret results
   - Identify friction points

3. **Insights (3 min)**
   - Show detailed message breakdown
   - Explain polarity scores
   - Export results for reporting

---

## Using External Repositories

### Testing with GitHub Repositories

**Any public GitHub repository can be analyzed!**

#### Example 1: Small Python Project
```bash
# Clone a small repository
git clone https://github.com/pallets/flask.git
cd flask

# Note the path (use pwd on Mac/Linux or cd on Windows)
# Example: C:/Users/YourName/flask

# Use this path in DevLens Tab 2 or Tab 3
```

#### Example 2: Your Own Projects
```bash
# Clone your own repository
git clone https://github.com/yourusername/your-repo.git
cd your-repo

# Use the full path in DevLens
```

#### Example 3: Open Source Projects
Popular repositories to test with:
- **Flask**: https://github.com/pallets/flask
- **Requests**: https://github.com/psf/requests
- **Django**: https://github.com/django/django (large)
- **FastAPI**: https://github.com/tiangolo/fastapi

**Steps:**
1. Clone the repository locally
2. Note the full path
3. Enter path in DevLens
4. Scan and analyze
5. Generate playbook

---

## Troubleshooting

### Issue 1: Path Not Found

**Error:** "Path does not exist: C:/Users/..."

**Solutions:**
- Verify the path exists: `cd C:/Users/YourName/Projects/repo`
- Use forward slashes: `C:/Users/...` not `C:\Users\...`
- Or use double backslashes: `C:\\Users\\...`
- Check spelling and capitalization
- Ensure you have read permissions

### Issue 2: No Files Found

**Error:** "Successfully scanned 0 files"

**Solutions:**
- Check if repository contains supported file types
- Verify you're not in an empty directory
- Ensure files aren't in ignored directories (venv, node_modules)
- Try a different repository

### Issue 3: Groq API Error

**Error:** "Groq API error: ..."

**Solutions:**
- Verify API key is correct
- Check internet connection
- Verify API key has available credits
- Application will fall back to templates automatically

### Issue 4: Memory Issues

**Error:** Application becomes slow or unresponsive

**Solutions:**
- Close other applications
- Test with smaller repositories first
- Restart the Streamlit application
- Process files in batches

### Issue 5: Import Errors

**Error:** "ModuleNotFoundError: No module named..."

**Solutions:**
```bash
pip install --upgrade -r requirements.txt
python -c "import nltk; nltk.download('punkt'); nltk.download('brown')"
```

---

## Testing Checklist

### Basic Functionality
- [ ] Application starts without errors
- [ ] All three tabs are accessible
- [ ] Sidebar configuration works
- [ ] API key input functions

### Tab 1: Sentiment Analysis
- [ ] Text paste works
- [ ] File upload works
- [ ] Analysis completes successfully
- [ ] Charts display correctly
- [ ] Export to JSON works

### Tab 2: Code Summarization
- [ ] Repository scanning works
- [ ] Path validation functions
- [ ] File upload works
- [ ] Code paste works
- [ ] Structure extraction works
- [ ] Complexity calculation works
- [ ] Statistics display correctly

### Tab 3: Playbook Generation
- [ ] Repository scanning works (independent)
- [ ] Template generation works (no API key)
- [ ] AI generation works (with API key)
- [ ] Markdown download works
- [ ] HTML download works
- [ ] Content is well-formatted

### Edge Cases
- [ ] Empty input handling
- [ ] Invalid path handling
- [ ] Large repository handling
- [ ] API key error handling
- [ ] Network error handling

---

## Performance Benchmarks

### Expected Performance

**Small Repository (10-50 files):**
- Scan time: 2-5 seconds
- Analysis time: 5-10 seconds
- Playbook generation: 3-8 seconds (with API)

**Medium Repository (50-200 files):**
- Scan time: 5-15 seconds
- Analysis time: 15-30 seconds
- Playbook generation: 5-12 seconds (with API)

**Large Repository (200+ files):**
- Scan time: 15-60 seconds
- Analysis time: 30-120 seconds
- Playbook generation: 8-15 seconds (with API)

---

## Conclusion

This testing guide covers all major features and scenarios. For production deployment:

1. Test with multiple repository types
2. Verify API key management
3. Test error handling
4. Validate export functionality
5. Check performance with large codebases

For questions or issues, refer to README.md or open a GitHub issue.

---

**Last Updated:** 2026-05-17
**Version:** 1.0