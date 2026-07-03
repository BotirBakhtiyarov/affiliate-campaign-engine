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


def _render_ab_variants(variants: list[dict[str, Any]]) -> None:
    """Render A/B test variants as read-only cards."""
    for variant in variants:
        with st.container(border=True):
            label = variant.get("variant_label", "")
            st.subheader(f"🧪 Variant {label}" if label else "🧪 Variant")
            st.text_input("Headline", value=variant.get("headline", ""), disabled=True, key=f"ab_variant_headline_{label}")
            st.text_area("Primary Text", value=variant.get("primary_text", ""), disabled=True, key=f"ab_variant_body_{label}")
            st.text_input("CTA", value=variant.get("cta", ""), disabled=True, key=f"ab_variant_cta_{label}")


def render_content_display(
    campaign: dict[str, Any],
    ab_variants: list[dict[str, Any]] | None = None,
    key_prefix: str = "content",
) -> dict[str, Any]:
    """Render generated campaign content in editable tabs and return edited campaign."""
    st.header("📄 Generated Campaign")

    tab_names = ["Strategy Summary", "Landing Page", "Email Sequence", "Ad Copies", "Social Media", "SEO Meta"]
    keys = ["strategy_summary", "landing_page", "email_sequence", "ad_copies", "social_media", "seo_meta"]

    if ab_variants:
        tab_names.append("A/B Variants")
        keys.append("ab_variants")

    edited_campaign: dict[str, Any] = {}
    tabs = st.tabs(tab_names)
    for tab, key, label in zip(tabs, keys, tab_names):
        with tab:
            if key == "ab_variants":
                _render_ab_variants(ab_variants)
                continue

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
