import asyncio

import streamlit as st
from utils.llm_clients import DEFAULT_MODELS, generate_content


PROVIDERS = ["OpenAI", "Anthropic", "DeepSeek", "Google"]


def _run_async(coro):
    """Run an async coroutine in a fresh event loop."""
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


def render_sidebar():
    """Render the settings sidebar and return the selected provider and API key."""
    st.sidebar.title("⚙️ Settings")

    provider = st.sidebar.radio("LLM Provider", PROVIDERS, index=PROVIDERS.index(st.session_state.get("api_provider", "OpenAI")))
    api_key = st.sidebar.text_input(
        f"{provider} API Key",
        value=st.session_state.get("api_key", ""),
        type="password",
        help="Your API key is used only for this session and is never logged.",
    )

    if st.sidebar.button("💾 Save Settings", key="save_settings_button"):
        st.session_state["api_provider"] = provider
        st.session_state["api_key"] = api_key
        st.sidebar.success("Settings saved!")

    if st.sidebar.button("🧪 Test Connection", key="test_connection_button"):
        if not api_key:
            st.sidebar.error("Please enter an API key first.")
        else:
            with st.spinner("Testing connection..."):
                try:
                    prompt = "Return a one-word response: 'OK'"
                    response = _run_async(generate_content(prompt, provider, api_key))
                    if response.strip().upper() == "OK":
                        st.sidebar.success("Connection successful!")
                    else:
                        st.sidebar.warning("Connected, but response was unexpected.")
                except Exception as exc:
                    st.sidebar.error(f"Connection failed: {exc}")

    st.sidebar.markdown("---")
    st.sidebar.markdown("**Selected model:**")
    st.sidebar.caption(DEFAULT_MODELS.get(provider, "Unknown"))

    return provider, api_key
