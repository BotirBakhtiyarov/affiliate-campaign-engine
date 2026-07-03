import streamlit as st

from components.sidebar import render_sidebar
from components.brief_form import render_brief_form
from components.angle_selector import render_angle_selector
from components.content_display import render_content_display
from components.export_panel import render_export_panel
from utils.session_manager import init_session, set_current_campaign, save_campaign
from utils.content_generator import analyze_angles, generate_full_campaign
from utils.llm_clients import DEFAULT_MODELS


def _run_async(coro):
    """Run an async coroutine in a fresh event loop."""
    loop = st.session_state.get("_event_loop")
    if loop is None or loop.is_closed():
        loop = __import__("asyncio").new_event_loop()
        st.session_state["_event_loop"] = loop
    return loop.run_until_complete(coro)


st.set_page_config(
    page_title="Affiliate Campaign Engine",
    page_icon="🚀",
    layout="wide",
)

init_session(st.session_state)

st.title("🚀 Affiliate Campaign Engine")
st.caption("Generate coordinated affiliate marketing content with AI")

provider, api_key = render_sidebar()

if not api_key:
    st.warning("Please enter your API key in the sidebar to continue.")
    st.stop()

brief, analyze_triggered = render_brief_form()

if analyze_triggered:
    with st.spinner("Analyzing brief and generating angles..."):
        try:
            angles_data = _run_async(analyze_angles(brief, provider, api_key))
            st.session_state["angles_data"] = angles_data
            st.session_state["selected_angle_index"] = angles_data.get("recommended", 0)
            st.session_state["selected_angle"] = angles_data["angles"][angles_data.get("recommended", 0)]
            st.session_state["brief"] = brief
        except Exception as exc:
            st.error(f"Angle analysis failed: {exc}")

if "angles_data" in st.session_state:
    selected_angle = render_angle_selector(st.session_state["angles_data"])

    if st.button("✨ Generate Full Campaign", key="generate_campaign_button"):
        with st.spinner("Generating content across all channels..."):
            try:
                campaign = _run_async(
                    generate_full_campaign(st.session_state["brief"], selected_angle, provider, api_key)
                )
                st.session_state["current_campaign"] = {
                    "brief": st.session_state["brief"],
                    "angle": selected_angle,
                    "content": campaign,
                }
                save_campaign(st.session_state, st.session_state["current_campaign"])
            except Exception as exc:
                st.error(f"Campaign generation failed: {exc}")

if st.session_state.get("current_campaign"):
    campaign = st.session_state["current_campaign"]
    edited_content = render_content_display(campaign["content"])
    campaign["content"] = edited_content
    render_export_panel(campaign["brief"], campaign["angle"], campaign["content"])
