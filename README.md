# Affiliate Campaign Engine

AI-powered creative suite for affiliate media buyers. Feed it one product brief and get a coordinated, multi-channel campaign — landing-page copy, ad variants, email sequences, social posts, SEO meta, UTM tracking links, and a Meta/Google Ads CSV export.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://affiliate-campaign-engine-rtkttqu8dpiewfansrekp4.streamlit.app/)

**Live demo:** https://affiliate-campaign-engine-rtkttqu8dpiewfansrekp4.streamlit.app/

---

## The Problem

Performance marketing teams spend hours producing coordinated copy across Meta, Google, TikTok, Taboola, and email. One weak headline or inconsistent angle can burn ad spend. This tool turns that creative bottleneck into a five-minute workflow.

## What It Does

1. **Brief in.** Enter product details, audience, price, commission, and campaign duration.
2. **Angle out.** The AI analyzes the brief and recommends the strongest marketing angle from three options.
3. **Campaign generated.** One click produces coordinated content for six channels.
4. **Export ready.** Generate UTM links, download a platform-ready ad CSV, export Markdown, or spin up A/B variants.

## Features

- **Multi-LLM support** — OpenAI, Anthropic, DeepSeek, Google Gemini, Kimi.
- **AI angle analysis** — 3 angles + data-driven recommendation.
- **Full campaign generation** across:
  - Strategy Summary
  - Landing Page
  - Email Sequence (5 emails)
  - Ad Copies (6 variants)
  - Social Media Kit (7 posts)
  - SEO Meta
- **A/B ad variant generator** for rapid creative testing.
- **UTM link builder** for clean campaign tracking.
- **CSV export** formatted for Meta/Google Ads bulk upload.
- **Markdown export** of the full campaign.
- **Editable preview tabs** to review and tweak before exporting.

## Tech Stack

- Python 3.13
- Streamlit
- Asyncio + HTTPX
- pytest / pytest-asyncio
- JSON prompt templates

## Project Structure

```
affiliate-campaign-engine/
├── app.py                  # Main Streamlit app
├── components/             # UI components
├── utils/                  # LLM clients, generators, exporters
├── prompts/                # LLM prompt templates
├── tests/                  # pytest suite
├── requirements.txt
└── README.md
```

## Quick Start

```bash
git clone <repo-url>
cd affiliate-campaign-engine
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Then paste your API key in the sidebar and click **Save Settings**.

## Usage

1. Fill out the brief form.
2. Click **🔍 Analyze Brief** to generate angles.
3. Pick the recommended angle or choose another.
4. Click **✨ Generate Full Campaign**.
5. In **📦 Export Campaign**:
   - Build a **UTM link**.
   - Download an **Ads CSV**.
   - Export the full campaign as **Markdown**.
6. Click **🧬 Generate A/B Variants** to create alternative copy and view it in the **A/B Variants** tab.

## Testing

```bash
pytest
```

The suite covers prompt loading, LLM dispatch, content generation, angle normalization, session management, UTM building, CSV export, and A/B variant generation.

## Deploy

1. Push to GitHub.
2. Connect the repo on [Streamlit Cloud](https://streamlit.io/cloud).
3. Add API keys under **Settings → Secrets**:

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

You can also enter keys manually in the sidebar for local runs.

## Why This Tool?

Coordinated creative is slow, repetitive, and easy to get wrong. This tool automates the repetitive part so media buyers can focus on targeting, bidding, and scaling.

## What's Next?

Given more time, the next builds would be:

- Meta Marketing API integration for direct ad publishing.
- Google Ads and TikTok Ads connectors.
- Performance dashboard tied to real spend and conversion data.
- Automated A/B test runner with statistical significance alerts.
- Built-in landing-page builder and host.

## Built For

This project was built as a submission for a media-buying engineering contest — a real, working tool that solves a creative-production problem for performance marketing teams.
