import copy
import logging

import streamlit as st

from components.sidebar import render_sidebar
from components.brief_form import render_brief_form
from components.angle_selector import render_angle_selector
from components.content_display import render_content_display
from components.export_panel import render_export_panel
from utils.async_helpers import run_async
from utils.session_manager import init_session, save_campaign, delete_campaign
from utils.ab_test_generator import generate_ad_variants
from utils.content_generator import analyze_angles, generate_full_campaign, _normalize_angle


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    st.set_page_config(
        page_title="Affiliate Campaign Engine",
        page_icon="🚀",
        layout="wide",
    )

    init_session(st.session_state)

    st.title("🚀 Affiliate Campaign Engine")
    st.caption("Generate coordinated affiliate marketing content with AI")

    if st.session_state.get("campaigns"):
        st.subheader("📁 Saved Campaigns")
        campaign_names = [f"{i+1}. {c['brief'].get('product_name', 'Untitled')}" for i, c in enumerate(st.session_state["campaigns"])]
        selected_idx = st.selectbox("Load a saved campaign", range(len(campaign_names)), format_func=lambda i: campaign_names[i], key="load_campaign_select")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Load Campaign", key="load_campaign_button"):
                loaded = st.session_state["campaigns"][selected_idx]
                st.session_state["current_campaign"] = loaded
                st.session_state["brief"] = loaded["brief"]
                selected_angle = _normalize_angle(loaded["angle"])
                st.session_state["angles_data"] = {"recommended": 0, "angles": [selected_angle]}
                st.session_state["selected_angle"] = selected_angle
                st.rerun()
        with col2:
            if st.button("Delete Campaign", key="delete_campaign_button"):
                delete_campaign(st.session_state, selected_idx)
                st.rerun()

    provider, api_key = render_sidebar()

    if not api_key:
        st.warning("Please enter your API key in the sidebar to continue.")
        st.stop()

    brief, analyze_triggered = render_brief_form()

    if analyze_triggered:
        with st.spinner("Analyzing brief and generating angles..."):
            try:
                angles_data = run_async(analyze_angles(brief, provider, api_key))
                st.session_state["angles_data"] = angles_data
                st.session_state["selected_angle_index"] = angles_data.get("recommended", 0)
                st.session_state["selected_angle"] = angles_data["angles"][angles_data.get("recommended", 0)]
                st.session_state["brief"] = brief
            except Exception as exc:
                st.session_state.pop("angles_data", None)
                st.session_state.pop("selected_angle", None)
                logger.exception("Angle analysis failed")
                st.error(f"Angle analysis failed: {exc}")

    if "angles_data" in st.session_state:
        selected_angle = render_angle_selector(st.session_state["angles_data"])

        if st.button("✨ Generate Full Campaign", key="generate_campaign_button"):
            with st.spinner("Generating content across all channels..."):
                try:
                    campaign = run_async(
                        generate_full_campaign(st.session_state["brief"], selected_angle, provider, api_key)
                    )
                    st.session_state["current_campaign"] = {
                        "brief": st.session_state["brief"],
                        "angle": selected_angle,
                        "content": campaign,
                    }
                    save_campaign(st.session_state, copy.deepcopy(st.session_state["current_campaign"]))
                except Exception as exc:
                    st.session_state.pop("current_campaign", None)
                    logger.exception("Campaign generation failed")
                    st.error(f"Campaign generation failed: {exc}")

        if st.button("🧬 Generate A/B Variants", key="generate_ab_variants_button"):
            with st.spinner("Generating A/B test variants..."):
                try:
                    variants = run_async(
                        generate_ad_variants(st.session_state["brief"], selected_angle, provider, api_key)
                    )
                    st.session_state["ab_variants"] = variants
                except Exception as exc:
                    st.session_state.pop("ab_variants", None)
                    logger.exception("A/B variant generation failed")
                    st.error(f"A/B variant generation failed: {exc}")

    if st.session_state.get("current_campaign"):
        campaign = st.session_state["current_campaign"]
        ab_variants = st.session_state.get("ab_variants")
        edited_content = render_content_display(campaign["content"], ab_variants=ab_variants)
        campaign["content"] = edited_content
        render_export_panel(campaign["brief"], campaign["angle"], campaign["content"])


if __name__ == "__main__":
    main()
