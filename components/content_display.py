import json
from typing import Any

import pyperclip
import streamlit as st


def _dict_to_text(data: Any) -> str:
    """Serialize data to pretty JSON."""
    return json.dumps(data, indent=2, ensure_ascii=False)


def _parse_edited_text(text: str) -> Any:
    """Try to parse edited text as JSON; return raw text if invalid."""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return text


def _render_copy_download(label: str, text: str, key: str):
    """Render download and copy buttons for a channel."""
    col1, col2 = st.columns([1, 1])
    with col1:
        st.download_button(
            label=f"⬇️ Download {label}",
            data=text,
            file_name=f"{label.lower().replace(' ', '_')}.json",
            mime="application/json",
            key=f"download_{key}",
        )
    with col2:
        if st.button(f"📋 Copy {label}", key=f"copy_{key}"):
            try:
                pyperclip.copy(text)
                st.success("Copied to clipboard!")
            except Exception:
                st.info("Clipboard copy is not available in this environment. Please copy manually from the text area.")


def render_content_display(campaign: dict[str, Any], key_prefix: str = "content") -> dict[str, Any]:
    """Render generated campaign content in editable tabs and return edited campaign."""
    st.header("📄 Generated Campaign")

    tab_names = ["Strategy Summary", "Landing Page", "Email Sequence", "Ad Copies", "Social Media", "SEO Meta"]
    keys = ["strategy_summary", "landing_page", "email_sequence", "ad_copies", "social_media", "seo_meta"]

    edited_campaign: dict[str, Any] = {}
    tabs = st.tabs(tab_names)
    for tab, key, label in zip(tabs, keys, tab_names):
        with tab:
            data = campaign.get(key, {})
            if isinstance(data, dict) and "error" in data:
                st.error(f"Failed to generate {label}: {data['error']}")
                edited_campaign[key] = data
            else:
                original_text = _dict_to_text(data)
                edited_text = st.text_area(
                    f"Edit {label}",
                    value=original_text,
                    height=400,
                    key=f"{key_prefix}_edit_{key}",
                )
                edited_campaign[key] = _parse_edited_text(edited_text)
                _render_copy_download(label, edited_text, f"{key_prefix}_{key}")

    return edited_campaign
