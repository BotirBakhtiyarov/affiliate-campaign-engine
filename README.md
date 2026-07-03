> **Note:** `docs/` is excluded from this repo per project policy and lives only in the local workspace.

# Affiliate Campaign Engine

> AI-powered creative suite for affiliate media buyers. Turn one product brief into a coordinated, multi-channel campaign — complete with landing-page copy, ad variants, email sequences, social posts, SEO meta, UTM tracking links, and platform-ready CSV exports.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://affiliate-campaign-engine-rtkttqu8dpiewfansrekp4.streamlit.app/)

## Live Demo

Try it now: **https://affiliate-campaign-engine-rtkttqu8dpiewfansrekp4.streamlit.app/**

## What It Does

Media buyers run campaigns across Meta, Google, TikTok, Taboola, and email — and every channel needs its own copy, angle, and tracking. This tool automates that creative production:

1. Enter a product brief (name, description, price, audience, commission, duration).
2. The AI analyzes the brief and recommends the strongest marketing angle.
3. One click generates a full campaign across six channels.
4. Export everything as Markdown, generate UTM links, download a Meta/Google Ads CSV, or spin up A/B ad variants for testing.

## Why This Tool?

Coordinated creative is a bottleneck for performance marketing teams. Writing ad copy, landing pages, emails, and social posts that all tell the same story takes hours — and mistakes are expensive. This tool collapses that work into minutes while keeping messaging consistent, so media buyers can spend more time on targeting, bidding, and optimization.

## What's Next?

If this were a full-time role, the roadmap would be:

- **Meta Marketing API integration** — publish campaigns, ad sets, and ads directly from the app.
- **Google Ads & TikTok Ads connectors** — one-click cross-platform publishing.
- **Performance dashboard** — pull spend and conversion data, then surface winning creative.
- **Automated A/B test runner** — launch variants, measure significance, and auto-pause losers.
- **Landing-page builder** — generate and host simple lead-capture pages.

## Features

- **Multi-LLM support** — OpenAI, Anthropic, DeepSeek, Google Gemini, and Kimi.
- **Angle analysis** — AI recommends the best marketing angle from three options.
- **Coordinated content generation** for:
  - Strategy Summary
  - Landing Page
  - Email Sequence (5 emails)
  - Ad Copies (6 variants)
  - Social Media Kit (7 posts)
  - SEO Meta
- **A/B ad variant generator** — create multiple headline/body/CTA combinations for testing.
- **UTM link builder** — generate tracked URLs for any source, medium, and campaign.
- **CSV export** — download ad copy in a Meta/Google Ads bulk-upload format.
- **Markdown export** — export the entire campaign brief and content.
- **Editable preview tabs** — review and tweak generated content before export.

## Tech Stack

- Python 3.13
- Streamlit (UI)
- Asyncio + HTTPX (LLM clients)
- pytest + pytest-asyncio (testing)
- Jinja-style JSON prompt templates

## Project Structure

```
affiliate-campaign-engine/
├── app.py                      # Main Streamlit orchestration
├── components/                 # UI components
│   ├── sidebar.py
│   ├── brief_form.py
│   ├── angle_selector.py
│   ├── content_display.py
│   └── export_panel.py
├── utils/                      # Business logic
│   ├── llm_clients.py
│   ├── content_generator.py
│   ├── ab_test_generator.py
│   ├── utm_builder.py
│   ├── csv_export.py
│   ├── prompt_loader.py
│   ├── session_manager.py
│   └── async_helpers.py
├── prompts/                    # LLM prompt templates
├── tests/                      # pytest suite
├── requirements.txt
└── README.md
```

## Quick Start

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

## Usage

1. Fill out the brief form with product details.
2. Click **🔍 Analyze Brief** to get three marketing angles.
3. Select the recommended angle (or pick another).
4. Click **✨ Generate Full Campaign** to create all channel content.
5. Use the **📦 Export Campaign** section to:
   - Build a **UTM tracking link**.
   - Download a **CSV** for Meta/Google Ads.
   - Export the full campaign as **Markdown**.
6. Click **🧬 Generate A/B Variants** to create alternative ad copy and view it in the **A/B Variants** tab.

## Testing

```bash
pytest
```

The test suite covers prompt loading, LLM client dispatch, content generation, angle normalization, session management, UTM building, CSV export, and A/B variant generation.

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

You can also paste API keys manually in the sidebar when running the app locally.

## Contest Note

This project was built as a submission for a media-buying engineering contest. The goal was to ship a real, working tool that solves a creative-production problem for performance marketing teams.
