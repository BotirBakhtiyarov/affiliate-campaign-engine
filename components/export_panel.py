import json
import streamlit as st


def _to_markdown(brief: dict, angle: dict, campaign: dict) -> str:
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
        "",
        "## Selected Angle",
        f"**{angle.get('name', '')}** — {angle.get('description', '')}",
        "",
        "## Generated Content",
        "",
    ]
    for channel, data in campaign.items():
        lines.append(f"### {channel.replace('_', ' ').title()}")
        lines.append("```json")
        lines.append(json.dumps(data, indent=2, ensure_ascii=False))
        lines.append("```")
        lines.append("")
    return "\n".join(lines)


def render_export_panel(brief: dict, angle: dict, campaign: dict):
    st.header("📦 Export Campaign")
    markdown = _to_markdown(brief, angle, campaign)
    st.download_button(
        label="⬇️ Export Full Campaign as Markdown",
        data=markdown,
        file_name=f"{brief.get('product_name', 'campaign').lower().replace(' ', '_')}_campaign.md",
        mime="text/markdown",
    )
