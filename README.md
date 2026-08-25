# DevLens - Repository Intelligence & Team Health Dashboard

DevLens is a Streamlit application for repository analysis, team sentiment analysis, and developer onboarding playbook generation.

## Features

### Team Sentiment Analytics

- Analyzes pasted commit messages and pull-request comments
- Classifies sentiment as positive, neutral, or frustrated/toxic
- Displays sentiment metrics and charts

### Codebase Architecture Summarizer

- Scans local repositories or GitHub repositories cloned locally
- Supports Python, JavaScript, TypeScript, Java, C/C++, C#, Go, Rust, PHP, Ruby, Swift, Kotlin, Scala, HTML, CSS, Vue, and Svelte
- Extracts classes, functions, imports, line counts, and simple complexity levels
- Uses optional AI summaries with a built-in local fallback

### Automated Playbook Generator

- Creates onboarding documentation in Markdown
- Includes architecture, module, technical-stack, complexity, setup, workflow, and entry-point sections when AI generation succeeds
- Uses built-in template generation when no key is configured or an AI request fails
- Provides Markdown and HTML downloads

## Run Locally

Requirements: Python 3.8 or newer.

```bash
pip install -r requirements.txt
streamlit run app.py
```

The app runs at `http://localhost:8501` by default.

## AI Configuration

### Streamlit Cloud

Add the following in the app's **Settings > Secrets**:

```toml
GROQ_API_KEY = "gsk_your-key-here"
```

The deployment key remains server-side. The sidebar field is optional and accepts a temporary session key. A manually entered key overrides the managed deployment key for that session; leaving the field blank uses the managed key.

### Local Use

Set `GROQ_API_KEY` in the shell before starting Streamlit. The application does not automatically load a `.env` file.

The default model is:

```text
meta-llama/llama-4-scout-17b-16e-instruct
```

Set `GROQ_MODEL` to use another model available to the configured Groq key.

## AI Versus Built-In Analysis

The sidebar status means that a key was found. It does not verify that the latest provider request succeeded.

With a working AI request, each non-empty file receives a natural-language model summary. The playbook generator then sends the collected summaries and repository statistics to the model for one additional AI-generated playbook request.

Without AI, file summaries are generated locally from detected classes, functions, imports, and line counts. The playbook is generated from a deterministic Markdown template.

If an AI request fails, the provider's raw error is hidden and DevLens uses the built-in fallback instead.

## Request Count and Limits

For a scan containing `N` readable supported files:

- No API key: `0` Groq requests
- Working key: up to `N` summary requests, one per non-empty file
- Playbook generation: `1` additional request
- Full scan plus playbook: up to `N + 1` requests

Empty files do not require a summary request. Repeating a scan or generating another playbook sends requests again; results are not cached.

Configured output limits are:

- File summary: up to 150 output tokens
- Playbook: up to 4,000 output tokens

The app does not currently display token usage, cost, quota, or rate-limit information.

## Repository Scanning

The scanner recursively reads supported source files and ignores common generated or dependency directories, including `venv`, `.venv`, `node_modules`, `.git`, `__pycache__`, `dist`, `build`, `.next`, `target`, and `coverage`.

For GitHub repositories, clone the repository locally first and provide its local path to DevLens.

## Troubleshooting

### AI fallback appears

A key being detected only enables the AI path. The actual request may still fail because of an invalid key, unavailable model, permissions, quota, rate limits, or a provider/network error. Confirm that the configured model is available to the key and that `GROQ_MODEL` is not overriding it with an inaccessible value.

### Import errors

```bash
pip install --upgrade -r requirements.txt
```

### Path errors

Use an existing repository directory and forward slashes, for example:

```text
C:/Users/YourName/Projects/my-repo
```

## Privacy

Sentiment and structural analysis run locally. Source code is sent to Groq only when an AI key is configured and the AI path is used. API keys are not intentionally logged or displayed by the application.

## License

MIT License.
