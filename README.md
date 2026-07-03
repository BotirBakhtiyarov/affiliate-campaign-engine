# Affiliate Campaign Engine

A Streamlit web app for generating coordinated affiliate marketing content across 6 channels using OpenAI, Anthropic, DeepSeek, or Google Gemini.

## Features

- Multi-LLM provider support
- AI-powered angle analysis (3 angles + recommendation)
- Coordinated content generation for:
  - Strategy Summary
  - Landing Page
  - Email Sequence (5 emails)
  - Ad Copies (6 variants)
  - Social Media Kit (7 posts)
  - SEO Meta
- Real-time preview with editable tabs
- Markdown export

## Local Setup

```bash
git clone <repo-url>
cd affiliate-campaign-engine
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

4. Enter your API key in the sidebar and click **Save Settings**.

## Testing

```bash
pytest
```

## Deploy to Streamlit Cloud

1. Push this repo to GitHub.
2. Go to [Streamlit Cloud](https://streamlit.io/cloud) and connect the repo.
3. Add your API keys in **Settings → Secrets**:

```toml
[openai]
api_key = "..."

[anthropic]
api_key = "..."

[deepseek]
api_key = "..."

[google]
api_key = "..."
```

You can also paste API keys manually in the sidebar when running the app.

4. Click **Deploy**.
