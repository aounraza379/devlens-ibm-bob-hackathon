"""
DevLens - Repository Intelligence & Team Health Dashboard
A comprehensive engineering health check tool for code repositories
"""

import streamlit as st
import os
from typing import List, Dict, Tuple
import json
from datetime import datetime
import re
from pathlib import Path
import tempfile
import subprocess
import shutil

GROQ_MODEL = os.getenv("GROQ_MODEL", "meta-llama/llama-4-scout-17b-16e-instruct")


def get_configured_api_key() -> str:
    """Read the Groq key from Streamlit secrets or the environment."""
    try:
        secret_key = st.secrets.get("GROQ_API_KEY", "")
    except Exception:
        secret_key = ""
    return str(secret_key or os.getenv("GROQ_API_KEY", "") or "").strip()


def show_ai_fallback_notice() -> None:
    """Explain the fallback without exposing provider error details."""
    if not st.session_state.get("ai_fallback_notice_shown", False):
        st.info("AI enhancement is temporarily unavailable, so DevLens used its built-in analysis instead.")
        st.session_state.ai_fallback_notice_shown = True

# NLP and ML imports
try:
    from textblob import TextBlob
except ImportError:
    st.error("Please install textblob: pip install textblob")

try:
    from groq import Groq
except ImportError:
    st.error("Please install groq: pip install groq")

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ============================================================================
# CONFIGURATION & SETUP
# ============================================================================

st.set_page_config(
    page_title="DevLens - Repository Intelligence",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .positive {
        color: #28a745;
        font-weight: bold;
    }
    .neutral {
        color: #ffc107;
        font-weight: bold;
    }
    .negative {
        color: #dc3545;
        font-weight: bold;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: 3rem;
        padding: 0 2rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# REPOSITORY SCANNER UTILITY
# ============================================================================

class RepositoryScanner:
    """Scans local repository folders and extracts code files"""
    
    SUPPORTED_EXTENSIONS = {
        '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.c', '.h', 
        '.cs', '.go', '.rs', '.php', '.rb', '.swift', '.kt', '.scala',
        '.html', '.css', '.vue', '.svelte'
    }
    
    IGNORE_DIRS = {
        'venv', '.venv', 'env', '.env', 'node_modules', '.git', '__pycache__',
        '.pytest_cache', '.mypy_cache', 'dist', 'build', '.next', '.nuxt',
        'target', 'bin', 'obj', '.idea', '.vscode', 'coverage'
    }
    
    def __init__(self):
        self.scanned_files = []
        self.total_lines = 0
        self.file_count = 0
    
    def scan_repository(self, repo_path: str) -> Dict:
        """
        Recursively scan a repository and extract all code files
        
        Args:
            repo_path: Path to the repository root or GitHub URL
            
        Returns:
            Dictionary containing scanned files and metadata
        """
        self.scanned_files = []
        self.total_lines = 0
        self.file_count = 0
        
        repo_path = repo_path.strip()
        is_github_url = repo_path.startswith("http://github.com/") or repo_path.startswith("https://github.com/")
        
        temp_dir = None
        if is_github_url:
            temp_dir = tempfile.mkdtemp()
            try:
                subprocess.run(["git", "clone", repo_path, temp_dir], check=True, capture_output=True)
                scan_path = temp_dir
            except subprocess.CalledProcessError as e:
                shutil.rmtree(temp_dir, ignore_errors=True)
                return {
                    "success": False,
                    "error": f"Failed to clone GitHub repository: {e.stderr.decode('utf-8', errors='ignore')}",
                    "files": [],
                    "stats": {}
                }
        else:
            scan_path = os.path.normpath(repo_path)
            if not os.path.exists(scan_path):
                return {
                    "success": False,
                    "error": f"Path does not exist: {scan_path}",
                    "files": [],
                    "stats": {}
                }
            
            if not os.path.isdir(scan_path):
                return {
                    "success": False,
                    "error": f"Path is not a directory: {scan_path}",
                    "files": [],
                    "stats": {}
                }
        
        try:
            # Walk through directory
            for root, dirs, files in os.walk(scan_path):
                # Filter out ignored directories
                dirs[:] = [d for d in dirs if d not in self.IGNORE_DIRS]
                
                for file in files:
                    file_path = os.path.join(root, file)
                    file_ext = os.path.splitext(file)[1].lower()
                    
                    # Check if file extension is supported
                    if file_ext in self.SUPPORTED_EXTENSIONS:
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()
                                lines = len(content.split('\n'))
                                
                                # Get relative path from repo root
                                rel_path = os.path.relpath(file_path, scan_path)
                                
                                self.scanned_files.append({
                                    "filename": file,
                                    "relative_path": rel_path,
                                    "full_path": file_path,
                                    "content": content,
                                    "lines": lines,
                                    "extension": file_ext
                                })
                                
                                self.total_lines += lines
                                self.file_count += 1
                        except Exception as e:
                            # Skip files that can't be read
                            continue
            
            if temp_dir:
                shutil.rmtree(temp_dir, ignore_errors=True)
                
            return {
                "success": True,
                "files": self.scanned_files,
                "stats": {
                    "total_files": self.file_count,
                    "total_lines": self.total_lines,
                    "repo_path": repo_path
                }
            }
        
        except Exception as e:
            if temp_dir:
                shutil.rmtree(temp_dir, ignore_errors=True)
            return {
                "success": False,
                "error": str(e),
                "files": [],
                "stats": {}
            }

# ============================================================================
# ENGINE A: SENTIMENT ANALYSIS ENGINE
# ============================================================================

class SentimentAnalyzer:
    """Analyzes Git commit messages and PR comments for team sentiment"""
    
    def __init__(self):
        # Use TextBlob only - lightweight and no model downloads
        pass
    
    def analyze_text(self, text: str) -> Dict:
        """Analyze sentiment of a single text"""
        if not text or not text.strip():
            return {"label": "NEUTRAL", "score": 0.5, "polarity": 0.0}
        
        try:
            # Use TextBlob for sentiment analysis
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            
            if polarity > 0.1:
                sentiment = "Positive"
            elif polarity < -0.1:
                sentiment = "Frustrated/Toxic"
            else:
                sentiment = "Neutral"
            
            return {
                "label": sentiment,
                "score": abs(polarity),
                "polarity": polarity
            }
        except Exception as e:
            st.error(f"Error analyzing sentiment: {e}")
            return {"label": "Neutral", "score": 0.5, "polarity": 0.0}
    
    def analyze_commits(self, commits: List[str]) -> Dict:
        """Analyze multiple commit messages"""
        if not commits:
            return {
                "overall_sentiment": "Neutral",
                "positive_count": 0,
                "neutral_count": 0,
                "negative_count": 0,
                "average_polarity": 0.0,
                "details": []
            }
        
        results = []
        positive_count = 0
        neutral_count = 0
        negative_count = 0
        total_polarity = 0.0
        
        for commit in commits:
            analysis = self.analyze_text(commit)
            results.append({
                "text": commit,
                "sentiment": analysis["label"],
                "score": analysis["score"],
                "polarity": analysis["polarity"]
            })
            
            if analysis["label"] == "Positive":
                positive_count += 1
            elif analysis["label"] == "Frustrated/Toxic":
                negative_count += 1
            else:
                neutral_count += 1
            
            total_polarity += analysis["polarity"]
        
        avg_polarity = total_polarity / len(commits) if commits else 0.0
        
        # Determine overall sentiment
        if avg_polarity > 0.1:
            overall = "Positive"
        elif avg_polarity < -0.1:
            overall = "Frustrated/Toxic"
        else:
            overall = "Neutral"
        
        return {
            "overall_sentiment": overall,
            "positive_count": positive_count,
            "neutral_count": neutral_count,
            "negative_count": negative_count,
            "average_polarity": avg_polarity,
            "details": results
        }

# ============================================================================
# ENGINE B: CODE SUMMARIZATION ENGINE
# ============================================================================

class CodeSummarizer:
    """Summarizes complex source code files into architectural summaries"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.use_groq = False
        self.groq_client = None
        
        if api_key:
            try:
                self.groq_client = Groq(api_key=api_key)
                self.use_groq = True
            except Exception:
                self.groq_client = None
    
    def extract_code_structure(self, code: str) -> Dict:
        """Extract structural information from code"""
        structure = {
            "classes": [],
            "functions": [],
            "imports": [],
            "comments": []
        }
        
        lines = code.split('\n')
        
        for line in lines:
            line_stripped = line.strip()
            
            # Extract classes
            if line_stripped.startswith('class '):
                class_match = re.match(r'class\s+(\w+)', line_stripped)
                if class_match:
                    structure["classes"].append(class_match.group(1))
            
            # Extract functions
            elif line_stripped.startswith('def '):
                func_match = re.match(r'def\s+(\w+)', line_stripped)
                if func_match:
                    structure["functions"].append(func_match.group(1))
            
            # Extract imports
            elif line_stripped.startswith('import ') or line_stripped.startswith('from '):
                structure["imports"].append(line_stripped)
            
            # Extract comments
            elif line_stripped.startswith('#') or line_stripped.startswith('//'):
                structure["comments"].append(line_stripped)
        
        return structure
    
    def summarize_code(self, code: str, filename: str = "code") -> Dict:
        """Generate a summary of the code"""
        if not code or not code.strip():
            return {
                "summary": "Empty code file",
                "structure": {"classes": [], "functions": [], "imports": [], "comments": []},
                "complexity": "Low",
                "lines": 0,
                "filename": filename
            }
        
        # Extract structure
        structure = self.extract_code_structure(code)
        lines = len(code.split('\n'))
        
        # Determine complexity
        total_elements = len(structure["classes"]) + len(structure["functions"])
        if total_elements > 20:
            complexity = "High"
        elif total_elements > 10:
            complexity = "Medium"
        else:
            complexity = "Low"
        
        # Generate summary
        summary_text = self._generate_summary(code, structure, filename)
        
        return {
            "summary": summary_text,
            "structure": structure,
            "complexity": complexity,
            "lines": lines,
            "filename": filename
        }
    
    def _generate_summary(self, code: str, structure: Dict, filename: str) -> str:
        """Generate natural language summary"""
        
        # Try Groq first if available
        if self.use_groq and self.groq_client:
            try:
                chat_completion = self.groq_client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a code documentation expert. Provide concise architectural summaries in 2-3 sentences."
                        },
                        {
                            "role": "user",
                            "content": f"Summarize this code file '{filename}':\n\n{code[:2000]}"
                        }
                    ],
                    model=GROQ_MODEL,
                    temperature=0.3,
                    max_tokens=150
                )
                return chat_completion.choices[0].message.content.strip()
            except Exception:
                show_ai_fallback_notice()
        
        # Fallback: rule-based summary
        summary_parts = [f"File '{filename}' contains:"]
        
        if structure["classes"]:
            summary_parts.append(f"{len(structure['classes'])} class(es): {', '.join(structure['classes'][:3])}")
        
        if structure["functions"]:
            summary_parts.append(f"{len(structure['functions'])} function(s): {', '.join(structure['functions'][:3])}")
        
        if structure["imports"]:
            summary_parts.append(f"Uses {len(structure['imports'])} import(s)")
        
        return ". ".join(summary_parts) + "."

# ============================================================================
# ENGINE C: PLAYBOOK GENERATOR
# ============================================================================

class PlaybookGenerator:
    """Generates onboarding playbooks from code summaries using deep Groq AI"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.use_groq = False
        self.groq_client = None
        self.used_fallback = False
        
        if api_key:
            try:
                self.groq_client = Groq(api_key=api_key)
                self.use_groq = True
            except Exception:
                self.groq_client = None
    
    def generate_playbook(self, repo_analysis: Dict, project_name: str = "Project") -> str:
        """
        Generate a comprehensive markdown onboarding playbook using Groq AI
        
        Args:
            repo_analysis: Complete repository analysis data from session state
            project_name: Name of the project
            
        Returns:
            Markdown formatted playbook
        """
        
        if not repo_analysis or 'summaries' not in repo_analysis:
            return "# Onboarding Playbook\n\nNo code summaries available."
        
        summaries = repo_analysis['summaries']
        
        # Use Groq for deep AI generation
        if self.use_groq and self.groq_client:
            try:
                # Prepare comprehensive context for the LLM
                context = self._prepare_context(summaries, repo_analysis)
                
                # Create detailed prompt for deep analysis
                prompt = f"""You are a senior software architect creating a comprehensive Developer Onboarding Playbook for "{project_name}".

Based on the complete repository analysis below, generate a beautiful, detailed, multi-section Markdown playbook that includes:

1. **Architecture Overview**: High-level system design and key components
2. **Module Relationships**: How different parts of the codebase interact
3. **Technical Stack**: Technologies, frameworks, and dependencies used
4. **Code Organization**: Directory structure and file organization patterns
5. **Complexity Analysis**: Areas of high complexity and potential technical debt
6. **Step-by-Step Environment Setup**: Detailed setup instructions
7. **Development Workflow**: How to contribute and best practices
8. **Key Entry Points**: Where to start reading the code

Repository Analysis:
{context}

Generate a professional, well-structured playbook with clear sections, code examples where relevant, and actionable guidance for new developers."""

                chat_completion = self.groq_client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a senior software architect and technical writer. Create comprehensive, well-structured developer onboarding documentation in beautiful Markdown format."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    model=GROQ_MODEL,
                    temperature=0.6,
                    max_tokens=4000
                )
                
                return chat_completion.choices[0].message.content.strip()
                
            except Exception:
                self.used_fallback = True
                show_ai_fallback_notice()
                return self._generate_fallback_playbook(summaries, project_name, repo_analysis)
        else:
            # Fallback if no API key
            self.used_fallback = True
            return self._generate_fallback_playbook(summaries, project_name, repo_analysis)
    
    def _prepare_context(self, summaries: List[Dict], repo_analysis: Dict) -> str:
        """Prepare comprehensive context for LLM"""
        context_parts = []
        
        # Repository statistics
        stats = repo_analysis.get('stats', {})
        context_parts.append(f"Total Files: {stats.get('total_files', 0)}")
        context_parts.append(f"Total Lines of Code: {stats.get('total_lines', 0)}")
        context_parts.append(f"Repository Path: {stats.get('repo_path', 'N/A')}\n")
        
        # File summaries with full details
        context_parts.append("File Analysis:")
        for i, summary in enumerate(summaries, 1):
            filename = summary.get('filename', 'Unnamed file')
            context_parts.append(f"\n{i}. {filename}")
            context_parts.append(f"   Path: {summary.get('relative_path', 'N/A')}")
            context_parts.append(f"   Lines: {summary.get('lines', 0)}")
            context_parts.append(f"   Complexity: {summary.get('complexity', 'Unknown')}")
            context_parts.append(f"   Summary: {summary.get('summary', 'No summary available')}")
            
            structure = summary.get('structure', {})
            if structure.get('classes'):
                context_parts.append(f"   Classes: {', '.join(structure['classes'][:10])}")
            if structure.get('functions'):
                context_parts.append(f"   Functions: {', '.join(structure['functions'][:15])}")
            if structure.get('imports'):
                context_parts.append(f"   Key Imports: {', '.join(structure['imports'][:5])}")
        
        return "\n".join(context_parts)
    
    def _generate_fallback_playbook(self, summaries: List[Dict], project_name: str, repo_analysis: Dict) -> str:
        """Generate template-based playbook as fallback"""
        playbook = f"# {project_name} - Developer Onboarding Playbook\n\n"
        playbook += f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n"
        playbook += "---\n\n"
        
        stats = repo_analysis.get('stats', {})
        
        playbook += "## Project Overview\n\n"
        playbook += f"This project consists of {stats.get('total_files', len(summaries))} file(s). "
        playbook += f"Total lines of code: ~{stats.get('total_lines', sum(s.get('lines', 0) for s in summaries))}\n\n"
        
        playbook += "## Architecture Summary\n\n"
        
        for summary in summaries:
            filename = summary.get('filename', 'Unnamed file')
            playbook += f"### {filename}\n\n"
            playbook += f"**Path:** `{summary.get('relative_path', filename)}`\n\n"
            playbook += f"**Complexity:** {summary.get('complexity', 'Unknown')}\n\n"
            playbook += f"**Summary:** {summary.get('summary', 'No summary available')}\n\n"
            
            structure = summary.get('structure', {})
            if structure.get('classes'):
                playbook += f"**Classes:** {', '.join(structure['classes'][:5])}\n\n"
            if structure.get('functions'):
                playbook += f"**Functions:** {', '.join(structure['functions'][:5])}\n\n"
            
            playbook += "---\n\n"
        
        playbook += "## Getting Started\n\n"
        playbook += "1. **Clone the repository** and set up your development environment\n"
        playbook += "2. **Review the architecture** - Start with the main entry points\n"
        playbook += "3. **Understand dependencies** - Check import statements and requirements\n"
        playbook += "4. **Run tests** - Ensure everything works in your environment\n"
        playbook += "5. **Make your first contribution** - Start with small, well-defined tasks\n\n"
        
        playbook += "## Key Components\n\n"
        
        all_classes = []
        all_functions = []
        
        for summary in summaries:
            structure = summary.get('structure', {})
            all_classes.extend(structure.get('classes', []))
            all_functions.extend(structure.get('functions', []))
        
        if all_classes:
            playbook += f"**Main Classes:** {', '.join(set(all_classes[:10]))}\n\n"
        
        if all_functions:
            playbook += f"**Key Functions:** {', '.join(set(all_functions[:10]))}\n\n"
        
        playbook += "## Best Practices\n\n"
        playbook += "- Follow the existing code style and conventions\n"
        playbook += "- Write clear commit messages\n"
        playbook += "- Add tests for new features\n"
        playbook += "- Document complex logic\n"
        playbook += "- Ask questions when unsure\n\n"
        
        playbook += "## Contributing\n\n"
        playbook += "1. Create a feature branch\n"
        playbook += "2. Make your changes\n"
        playbook += "3. Test thoroughly\n"
        playbook += "4. Submit a pull request\n"
        playbook += "5. Address review feedback\n\n"
        
        playbook += "---\n\n"
        playbook += "*This playbook was automatically generated by DevLens*\n"
        
        return playbook

# ============================================================================
# STREAMLIT UI
# ============================================================================

def main():
    """Main application entry point"""
    
    # Initialize session state for repo analysis
    if 'repo_analysis' not in st.session_state:
        st.session_state.repo_analysis = None
    st.session_state.ai_fallback_notice_shown = False
    
    # Header
    st.markdown('<div class="main-header">DevLens</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Repository Intelligence & Team Health Dashboard</div>', unsafe_allow_html=True)
    
    # Sidebar configuration
    with st.sidebar:
        st.header("Configuration")
        
        configured_api_key = get_configured_api_key()
        entered_api_key = st.text_input(
            "AI enhancement key (Optional)",
            type="password",
            placeholder="Enter a key for this session",
            help="Optional. DevLens also reads GROQ_API_KEY from Streamlit secrets or environment variables."
        )
        api_key = entered_api_key.strip() or configured_api_key
        
        if not api_key:
            st.caption("Built-in analysis is active. Add an AI key for richer summaries and playbooks.")
        elif not entered_api_key:
            st.caption("Managed AI enhancement is active. Leave this field blank to keep using it.")
        else:
            st.caption("Using the key entered for this session. Clear it to return to the managed key.")
        
        st.markdown("---")
        st.markdown("### About DevLens")
        st.markdown("""
        DevLens provides comprehensive engineering health checks:
        
        - **Team Sentiment**: Analyze commit messages and PR comments
        - **Code Summarization**: Understand complex codebases quickly
        - **Onboarding Playbooks**: Auto-generate documentation
        
        **Powered by:**
        - TextBlob for sentiment analysis
        - Groq for AI-enhanced summaries (optional)
        """)
        
        st.markdown("---")
        st.markdown("*Built with Streamlit & Groq*")
    
    # Initialize engines
    sentiment_analyzer = SentimentAnalyzer()
    code_summarizer = CodeSummarizer(api_key if api_key else None)
    playbook_generator = PlaybookGenerator(api_key if api_key else None)
    repo_scanner = RepositoryScanner()
    
    # Main tabs
    tab1, tab2, tab3 = st.tabs([
        "Team Sentiment Analytics",
        "Codebase Architecture Summarizer",
        "Automated Playbook Generator"
    ])
    
    # ========================================================================
    # TAB 1: TEAM SENTIMENT ANALYTICS
    # ========================================================================
    with tab1:
        st.header("Team Sentiment Analytics")
        st.markdown("Analyze Git commit messages and PR comments to understand team dynamics and friction points.")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            input_method = st.radio(
                "Input Method:",
                ["Paste Text", "Upload File"],
                horizontal=True
            )
            
            commits = []
            
            if input_method == "Paste Text":
                commit_text = st.text_area(
                    "Paste commit messages or PR comments (one per line):",
                    height=300,
                    placeholder="fix: resolved merge conflict\nfeat: added new feature\nThis PR looks good!\nWhy is this breaking again??"
                )
                
                if commit_text:
                    commits = [line.strip() for line in commit_text.split('\n') if line.strip()]
            
            else:
                uploaded_file = st.file_uploader(
                    "Upload a text file with commits/comments",
                    type=['txt', 'log']
                )
                
                if uploaded_file:
                    content = uploaded_file.read().decode('utf-8')
                    commits = [line.strip() for line in content.split('\n') if line.strip()]
            
            if st.button("Analyze Sentiment", type="primary", use_container_width=True):
                if commits:
                    with st.spinner("Analyzing sentiment..."):
                        results = sentiment_analyzer.analyze_commits(commits)
                        
                        # Store in session state
                        st.session_state['sentiment_results'] = results
                else:
                    st.warning("Please provide commit messages or comments to analyze.")
        
        with col2:
            st.markdown("### Quick Stats")
            if 'sentiment_results' in st.session_state:
                results = st.session_state['sentiment_results']
                
                st.metric("Overall Sentiment", results['overall_sentiment'])
                st.metric("Total Analyzed", len(results['details']))
                st.metric("Average Polarity", f"{results['average_polarity']:.2f}")
        
        # Display results
        if 'sentiment_results' in st.session_state:
            results = st.session_state['sentiment_results']
            
            st.markdown("---")
            st.subheader("Sentiment Distribution")
            
            # Create visualization
            col1, col2 = st.columns(2)
            
            with col1:
                # Pie chart
                fig_pie = go.Figure(data=[go.Pie(
                    labels=['Positive', 'Neutral', 'Frustrated/Toxic'],
                    values=[
                        results['positive_count'],
                        results['neutral_count'],
                        results['negative_count']
                    ],
                    marker=dict(colors=['#28a745', '#ffc107', '#dc3545'])
                )])
                fig_pie.update_layout(title="Sentiment Breakdown")
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col2:
                # Bar chart
                sentiment_df = pd.DataFrame({
                    'Sentiment': ['Positive', 'Neutral', 'Frustrated/Toxic'],
                    'Count': [
                        results['positive_count'],
                        results['neutral_count'],
                        results['negative_count']
                    ]
                })
                
                fig_bar = px.bar(
                    sentiment_df,
                    x='Sentiment',
                    y='Count',
                    color='Sentiment',
                    color_discrete_map={
                        'Positive': '#28a745',
                        'Neutral': '#ffc107',
                        'Frustrated/Toxic': '#dc3545'
                    }
                )
                fig_bar.update_layout(title="Sentiment Counts", showlegend=False)
                st.plotly_chart(fig_bar, use_container_width=True)
            
            # Detailed results
            st.subheader("Detailed Analysis")
            
            for i, detail in enumerate(results['details'], 1):
                sentiment_class = "positive" if detail['sentiment'] == "Positive" else "negative" if detail['sentiment'] == "Frustrated/Toxic" else "neutral"
                
                with st.expander(f"Message {i}: {detail['sentiment']} (Score: {detail['score']:.2f})"):
                    st.markdown(f"**Text:** {detail['text']}")
                    st.markdown(f"**Sentiment:** <span class='{sentiment_class}'>{detail['sentiment']}</span>", unsafe_allow_html=True)
                    st.markdown(f"**Confidence:** {detail['score']:.2%}")
                    st.markdown(f"**Polarity:** {detail['polarity']:.3f}")
            
            # Export option
            st.markdown("---")
            if st.button("Export Results as JSON"):
                json_str = json.dumps(results, indent=2)
                st.download_button(
                    label="Download JSON",
                    data=json_str,
                    file_name=f"sentiment_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
    
    # ========================================================================
    # TAB 2: CODEBASE ARCHITECTURE SUMMARIZER
    # ========================================================================
    with tab2:
        st.header("Codebase Architecture Summarizer")
        st.markdown("Scan a local repository or upload source code files to get clear architectural summaries and insights.")
        
        # Repository folder scanning section
        st.subheader("Local or GitHub Repository Scanner")
        st.info("**Note:** You can enter a local directory path OR a GitHub URL (e.g. `https://github.com/username/repo`).")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            repo_path = st.text_input(
                "Enter Local Repository Path or GitHub URL:",
                placeholder="Example: C:/Users/YourName/Projects/my-repo OR https://github.com/...",
                help="Enter the full path to your local repository folder OR a GitHub repository URL."
            )
            
            # Show current working directory as reference
            st.caption(f"Current working directory: {os.getcwd()}")
        
        with col2:
            st.markdown("###")
            if st.button("Scan Repository", type="primary", use_container_width=True):
                if repo_path:
                    with st.spinner(f"Scanning repository: {repo_path}..."):
                        scan_result = repo_scanner.scan_repository(repo_path)
                        
                        if scan_result['success']:
                            st.success(f"Successfully scanned {scan_result['stats']['total_files']} files!")
                            
                            # Analyze all scanned files
                            with st.spinner("Analyzing code structure..."):
                                summaries = []
                                for file_data in scan_result['files']:
                                    summary = code_summarizer.summarize_code(
                                        file_data['content'],
                                        file_data['filename']
                                    )
                                    summary['relative_path'] = file_data['relative_path']
                                    summaries.append(summary)
                                
                                # Store in session state
                                st.session_state.repo_analysis = {
                                    'summaries': summaries,
                                    'stats': scan_result['stats']
                                }
                                st.session_state['code_summaries'] = summaries
                        else:
                            st.error(f"Error: {scan_result['error']}")
                            st.info("**Troubleshooting Tips:**\n- Ensure the path exists and is correct\n- Use forward slashes (/) or double backslashes (\\\\)\n- Check that you have read permissions for the directory")
                else:
                    st.warning("Please enter a repository path.")
        
        st.markdown("---")
        
        # Manual file upload section
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Manual File Upload")
            input_method = st.radio(
                "Input Method:",
                ["Paste Code", "Upload Files"],
                horizontal=True,
                key="code_input_method"
            )
            
            code_files = []
            
            if input_method == "Paste Code":
                filename = st.text_input("Filename:", value="main.py")
                code_text = st.text_area(
                    "Paste your source code:",
                    height=300,
                    placeholder="def hello_world():\n    print('Hello, World!')"
                )
                
                if code_text:
                    code_files.append({"filename": filename, "content": code_text})
            
            else:
                uploaded_files = st.file_uploader(
                    "Upload source code files",
                    type=['py', 'js', 'java', 'cpp', 'c', 'ts', 'jsx', 'tsx'],
                    accept_multiple_files=True
                )
                
                if uploaded_files:
                    for uploaded_file in uploaded_files:
                        content = uploaded_file.read().decode('utf-8')
                        code_files.append({
                            "filename": uploaded_file.name,
                            "content": content
                        })
            
            if st.button("Analyze Code", type="secondary", use_container_width=True):
                if code_files:
                    with st.spinner("Analyzing code structure..."):
                        summaries = []
                        
                        for file_data in code_files:
                            summary = code_summarizer.summarize_code(
                                file_data['content'],
                                file_data['filename']
                            )
                            summaries.append(summary)
                        
                        # Update session state
                        if st.session_state.repo_analysis:
                            st.session_state.repo_analysis['summaries'].extend(summaries)
                        else:
                            st.session_state.repo_analysis = {
                                'summaries': summaries,
                                'stats': {
                                    'total_files': len(summaries),
                                    'total_lines': sum(s['lines'] for s in summaries)
                                }
                            }
                        st.session_state['code_summaries'] = st.session_state.repo_analysis['summaries']
                else:
                    st.warning("Please provide code to analyze.")
        
        with col2:
            st.markdown("### Quick Stats")
            if st.session_state.repo_analysis:
                stats = st.session_state.repo_analysis.get('stats', {})
                summaries = st.session_state.repo_analysis.get('summaries', [])
                
                st.metric("Files Analyzed", stats.get('total_files', len(summaries)))
                st.metric("Total Lines", stats.get('total_lines', sum(s['lines'] for s in summaries)))
                
                total_classes = sum(len(s.get('structure', {}).get('classes', [])) for s in summaries)
                total_functions = sum(len(s.get('structure', {}).get('functions', [])) for s in summaries)
                
                st.metric("Classes", total_classes)
                st.metric("Functions", total_functions)
        
        # Display results
        if st.session_state.repo_analysis:
            summaries = st.session_state.repo_analysis['summaries']
            
            st.markdown("---")
            st.subheader("Code Analysis Results")
            
            # Complexity distribution
            complexity_counts = {}
            for summary in summaries:
                complexity = summary['complexity']
                complexity_counts[complexity] = complexity_counts.get(complexity, 0) + 1
            
            if complexity_counts:
                fig_complexity = go.Figure(data=[go.Bar(
                    x=list(complexity_counts.keys()),
                    y=list(complexity_counts.values()),
                    marker=dict(color=['#28a745', '#ffc107', '#dc3545'])
                )])
                fig_complexity.update_layout(
                    title="Complexity Distribution",
                    xaxis_title="Complexity Level",
                    yaxis_title="Number of Files"
                )
                st.plotly_chart(fig_complexity, use_container_width=True)
            
            # Detailed summaries
            st.subheader("File Summaries")
            
            for summary in summaries:
                filename = summary.get('filename', 'Unnamed file')
                complexity = summary.get('complexity', 'Unknown')
                with st.expander(f"{filename} - {complexity} Complexity"):
                    if 'relative_path' in summary:
                        st.markdown(f"**Path:** `{summary['relative_path']}`")
                    st.markdown(f"**Summary:** {summary['summary']}")
                    st.markdown(f"**Lines of Code:** {summary['lines']}")
                    st.markdown(f"**Complexity:** {summary['complexity']}")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        structure = summary.get('structure', {})
                        if structure.get('classes'):
                            st.markdown("**Classes:**")
                            for cls in structure['classes']:
                                st.markdown(f"- `{cls}`")
                    
                    with col2:
                        if structure.get('functions'):
                            st.markdown("**Functions:**")
                            for func in structure['functions'][:10]:
                                st.markdown(f"- `{func}`")
                    
                    if structure.get('imports'):
                        st.markdown("**Key Imports:**")
                        for imp in structure['imports'][:5]:
                            st.code(imp, language='python')
    
    # ========================================================================
    # TAB 3: AUTOMATED PLAYBOOK GENERATOR
    # ========================================================================
    with tab3:
        st.header("Automated Playbook Generator")
        st.markdown("Generate comprehensive onboarding documentation from your code summaries using deep AI analysis.")
        
        # Repository folder scanning section for Tab 3
        st.subheader("Local or GitHub Repository Scanner")
        st.info("**Note:** You can enter a local directory path OR a GitHub URL (e.g. `https://github.com/username/repo`).")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            repo_path_tab3 = st.text_input(
                "Enter Local Repository Path or GitHub URL:",
                placeholder="Example: C:/Users/YourName/Projects/my-repo OR https://github.com/...",
                help="Enter the full path to your local repository folder OR a GitHub repository URL.",
                key="repo_path_tab3"
            )
            
            # Show current working directory as reference
            st.caption(f"Current working directory: {os.getcwd()}")
        
        with col2:
            st.markdown("###")
            if st.button("Scan Repository", type="primary", use_container_width=True, key="scan_repo_tab3"):
                if repo_path_tab3:
                    with st.spinner(f"Scanning repository: {repo_path_tab3}..."):
                        scan_result = repo_scanner.scan_repository(repo_path_tab3)
                        
                        if scan_result['success']:
                            st.success(f"Successfully scanned {scan_result['stats']['total_files']} files!")
                            
                            # Analyze all scanned files
                            with st.spinner("Analyzing code structure..."):
                                summaries = []
                                for file_data in scan_result['files']:
                                    summary = code_summarizer.summarize_code(
                                        file_data['content'],
                                        file_data['filename']
                                    )
                                    summary['relative_path'] = file_data['relative_path']
                                    summaries.append(summary)
                                
                                # Store in session state
                                st.session_state.repo_analysis = {
                                    'summaries': summaries,
                                    'stats': scan_result['stats']
                                }
                        else:
                            st.error(f"Error: {scan_result['error']}")
                            st.info("**Troubleshooting Tips:**\n- Ensure the path exists and is correct\n- Use forward slashes (/) or double backslashes (\\\\)\n- Check that you have read permissions for the directory")
                else:
                    st.warning("Please enter a repository path.")
        
        st.markdown("---")
        
        if not st.session_state.repo_analysis:
            st.info("Please scan a repository or analyze code in the 'Codebase Architecture Summarizer' tab first!")
        else:
            col1, col2 = st.columns([3, 1])
            
            with col1:
                project_name = st.text_input(
                    "Project Name:",
                    value="My Project",
                    help="Name of your project for the playbook"
                )
            
            with col2:
                st.markdown("### Files Ready")
                summaries = st.session_state.repo_analysis['summaries']
                st.metric("Code Files", len(summaries))
            
            # Check for API key
            if not api_key:
                st.info("Built-in playbook generation is active. Add an AI enhancement key for a more detailed result.")
            else:
                st.info("AI key detected. The connection will be verified when you generate the playbook.")
            
            if st.button("Generate Playbook", type="primary", use_container_width=True):
                with st.spinner("Generating comprehensive onboarding playbook with deep AI analysis..."):
                    playbook = playbook_generator.generate_playbook(
                        st.session_state.repo_analysis,
                        project_name
                    )
                    st.session_state['playbook'] = playbook
                    if playbook_generator.used_fallback:
                        st.success("Playbook generated with DevLens built-in analysis.")
                    else:
                        st.success("AI-enhanced playbook generated successfully.")
            
            # Display playbook
            if 'playbook' in st.session_state:
                st.markdown("---")
                st.subheader("Generated Playbook")
                
                # Display the playbook
                st.markdown(st.session_state['playbook'])
                
                # Download options
                st.markdown("---")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.download_button(
                        label="Download as Markdown",
                        data=st.session_state['playbook'],
                        file_name=f"{project_name.replace(' ', '_')}_playbook.md",
                        mime="text/markdown"
                    )
                
                with col2:
                    # Convert to HTML for download
                    playbook_html = st.session_state['playbook'].replace('\n', '<br>')
                    html_content = f"""
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <title>{project_name} - Onboarding Playbook</title>
                        <style>
                            body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
                            h1 {{ color: #1f77b4; }}
                            h2 {{ color: #333; border-bottom: 2px solid #1f77b4; padding-bottom: 5px; }}
                            code {{ background-color: #f4f4f4; padding: 2px 5px; border-radius: 3px; }}
                        </style>
                    </head>
                    <body>
                        {playbook_html}
                    </body>
                    </html>
                    """
                    
                    st.download_button(
                        label="Download as HTML",
                        data=html_content,
                        file_name=f"{project_name.replace(' ', '_')}_playbook.html",
                        mime="text/html"
                    )

# ============================================================================
# RUN APPLICATION
# ============================================================================

if __name__ == "__main__":
    main()

# Made with Bob
