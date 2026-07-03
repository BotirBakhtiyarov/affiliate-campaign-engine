import json

import pyperclip
import streamlit as st


def _dict_to_text(data: dict) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False)


def _render_copy_download(label: str, data: dict, key: str):
    text = _dict_to_text(data)
    col1, col2, col3 = st.columns([1, 1, 1])
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
                st.info("Copy not available in this environment. Use the text area or download button.")
    with col3:
        st.code(text, language="json")


def render_content_display(campaign: dict):
    st.header("📄 Generated Campaign")

    tab_names = ["Strategy Summary", "Landing Page", "Email Sequence", "Ad Copies", "Social Media", "SEO Meta"]
    keys = ["strategy_summary", "landing_page", "email_sequence", "ad_copies", "social_media", "seo_meta"]

    tabs = st.tabs(tab_names)
    for tab, key, label in zip(tabs, keys, tab_names):
        with tab:
            data = campaign.get(key, {})
            if "error" in data:
                st.error(f"Failed to generate {label}: {data['error']}")
            else:
                st.text_area(
                    f"Edit {label}",
                    value=_dict_to_text(data),
                    height=400,
                    key=f"edit_{key}",
                )
                _render_copy_download(label, data, key)
