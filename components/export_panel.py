import json
import re
from typing import Any

import streamlit as st

from utils.csv_export import generate_ads_csv
from utils.utm_builder import build_utm_url


def _sanitize_filename(name: str) -> str:
    """Sanitize a string for use as a filename."""
    safe = re.sub(r"[^\w\s-]", "", name).strip().lower()
    safe = re.sub(r"[-\s]+", "_", safe)
    return safe or "campaign"


def _slugify(name: str) -> str:
    """Convert a string to a URL-friendly slug."""
    safe = re.sub(r"[^\w\s-]", "", name).strip().lower()
    safe = re.sub(r"[-\s]+", "_", safe)
    return safe or "campaign"


def _default_utm_campaign(brief: dict[str, Any]) -> str:
    """Build a default UTM campaign name from the brief."""
    campaign = _slugify(brief.get("product_name", "campaign"))
    duration = _slugify(brief.get("campaign_duration", ""))
    if duration:
        campaign = f"{campaign}_{duration}"
    return campaign


def _to_markdown(brief: dict[str, Any], angle: dict[str, Any] | None, campaign: dict[str, Any]) -> str:
    """Convert brief, angle, and campaign content to Markdown."""
    angle_name = angle.get("name", "") if angle else ""
    angle_description = angle.get("description", "") if angle else ""

    lines = [
        f"# Affiliate Campaign: {brief.get('product_name', 'Untitled')}",
        "",
        "## Brief",
        f"- **Product:** {brief.get('product_name', '')}",
        f"- **Description:** {brief.get('product_description', '')}",
        f"- **Price:** {brief.get('price', '')}",
        f"- **Audience:** {brief.get('target_audience', '')}",
        f"- **Commission:** {brief.get('commission_rate', '')}",
        f"- **Promo Code:** {brief.get('promo_code', '')}",
        f"- **Duration:** {brief.get('campaign_duration', '')}",
        f"- **Unique Selling Points:** {brief.get('unique_selling_points', '')}",
        f"- **Competitor Notes:** {brief.get('competitor_notes', '')}",
        "",
        "## Selected Angle",
        f"**{angle_name}** — {angle_description}",
        "",
        "## Generated Content",
        "",
    ]
    for channel, data in campaign.items():
        lines.append(f"### {channel.replace('_', ' ').title()}")
        if isinstance(data, dict) and "error" in data:
            lines.append(f"**Error:** {data['error']}")
        elif isinstance(data, dict):
            for field, value in data.items():
                lines.append(f"#### {field.replace('_', ' ').title()}")
                if isinstance(value, (dict, list)):
                    lines.append("```json")
                    lines.append(json.dumps(value, indent=2, ensure_ascii=False))
                    lines.append("```")
                else:
                    lines.append(str(value))
                lines.append("")
        else:
            lines.append("```")
            lines.append(str(data))
            lines.append("```")
        lines.append("")
    return "\n".join(lines)


def _render_utm_builder(brief: dict[str, Any]) -> str | None:
    """Render the UTM link builder section and return the generated URL."""
    st.subheader("🔗 UTM Link Builder")
    base_url = st.text_input("Base URL", value="https://", key="utm_base_url")

    col1, col2 = st.columns(2)
    with col1:
        utm_source = st.selectbox(
            "Source",
            ["meta", "google", "tiktok", "taboola", "email"],
            key="utm_source",
        )
    with col2:
        utm_medium = st.selectbox(
            "Medium",
            ["paid_social", "cpc", "display", "email", "affiliate"],
            key="utm_medium",
        )

    utm_campaign = st.text_input(
        "Campaign",
        value=_default_utm_campaign(brief),
        key="utm_campaign",
    )

    col3, col4 = st.columns(2)
    with col3:
        utm_content = st.text_input("Content", value="ad_1", key="utm_content")
    with col4:
        utm_term = st.text_input("Term (optional)", value="", key="utm_term")

    if base_url and base_url != "https://":
        try:
            utm_url = build_utm_url(
                base_url,
                utm_source=utm_source,
                utm_medium=utm_medium,
                utm_campaign=utm_campaign,
                utm_content=utm_content or None,
                utm_term=utm_term or None,
            )
            st.code(utm_url, language="text")
            return utm_url
        except ValueError as exc:
            st.error(f"Invalid URL: {exc}")
    return None


def _render_csv_export(
    brief: dict[str, Any],
    angle: dict[str, Any] | None,
    campaign: dict[str, Any],
    destination_url: str,
) -> None:
    """Render the CSV export section for ad platforms."""
    st.subheader("📄 Export Ads CSV")
    csv_data = generate_ads_csv(
        campaign,
        brief,
        angle or {},
        destination_url=destination_url,
    )
    filename = f"{_sanitize_filename(brief.get('product_name', 'campaign'))}_ads.csv"
    st.download_button(
        label="⬇️ Download Ads CSV (Meta/Google Ads)",
        data=csv_data,
        file_name=filename,
        mime="text/csv",
        key="export_ads_csv",
    )


def render_export_panel(brief: dict[str, Any], angle: dict[str, Any] | None, campaign: dict[str, Any]) -> None:
    """Render the export panel with Markdown download, UTM builder, and CSV export."""
    st.header("📦 Export Campaign")

    markdown = _to_markdown(brief, angle, campaign)
    filename = f"{_sanitize_filename(brief.get('product_name', 'campaign'))}_campaign.md"
    st.download_button(
        label="⬇️ Export Full Campaign as Markdown",
        data=markdown,
        file_name=filename,
        mime="text/markdown",
        key="export_campaign_markdown",
    )

    st.markdown("---")
    utm_url = _render_utm_builder(brief)

    st.markdown("---")
    _render_csv_export(brief, angle, campaign, destination_url=utm_url or "")
