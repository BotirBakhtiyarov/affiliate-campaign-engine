# Affiliate Campaign Engine

A Streamlit web app for generating coordinated affiliate marketing content across 6 channels using OpenAI, Anthropic, DeepSeek, Google Gemini, or Kimi.

## Features

- Multi-LLM provider support (OpenAI, Anthropic, DeepSeek, Google Gemini, Kimi)
- AI-powered angle analysis (3 angles + recommendation)
- Coordinated content generation for:
  - Strategy Summary
  - Landing Page
  - Email Sequence (5 emails)
  - Ad Copies (6 variants)
  - Social Media Kit (7 posts)
  - SEO Meta
- A/B ad variant generator for rapid creative testing
- UTM link builder for campaign tracking
- CSV export for Meta/Google Ads bulk upload
- Real-time preview with editable tabs
- Markdown export

## Local Setup

1. Clone the repo:

```bash
git clone <repo-url>
cd affiliate-campaign-engine
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the app:

```bash
streamlit run app.py
```

5. Enter your API key in the sidebar and click **Save Settings**.

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

[kimi]
api_key = "..."
```

4. Click **Deploy**.

You can also paste API keys manually in the sidebar when running the app.

## Why this tool?

Media buyers spend hours writing coordinated copy for ads, landing pages, emails, and social posts across multiple platforms. This tool turns a single product brief into a full campaign brief and ad-ready assets in seconds, cutting creative production time and keeping messaging consistent across every channel.

## What's next?

If this were a full-time role, the next builds would be:

- Direct Meta Marketing API integration to create campaigns, ad sets, and ads without leaving the app.
- Google Ads and TikTok Ads API connectors for cross-platform publishing.
- Performance dashboard that pulls spend/conversion data and surfaces winning creative.
- Automated A/B test runner with statistical significance alerts.
