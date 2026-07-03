import json
import re
from typing import Any

import streamlit as st


def _sanitize_filename(name: str) -> str:
    """Sanitize a string for use as a filename."""
    safe = re.sub(r"[^\w\s-]", "", name).strip().lower()
    safe = re.sub(r"[-\s]+", "_", safe)
    return safe or "campaign"


def _to_markdown(brief: dict[str, Any], angle: dict[str, Any] | None, campaign: dict[str, Any]) -> str:
    """Convert brief, angle, and campaign content to Markdown."""
    angle_name = angle.get("name", "") if angle else ""
    angle_description = angle.get("description", "") if angle else ""

    lines = [
        f"# Affiliate Campaign: {brief.get('product_name', 'Untitled')}",
        "",
        "## Brief",
        f"- **Product:** {brief.get('product_name', '')}",
        f"- **Description:** {brief.get('description', '')}",
        f"- **Price:** {brief.get('price', '')}",
        f"- **Audience:** {brief.get('audience', '')}",
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


def render_export_panel(brief: dict[str, Any], angle: dict[str, Any] | None, campaign: dict[str, Any]) -> None:
    """Render the export panel with a Markdown download button."""
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
