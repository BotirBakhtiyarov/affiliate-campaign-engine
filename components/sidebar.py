import asyncio

import streamlit as st
from utils.llm_clients import generate_content


PROVIDERS = ["OpenAI", "Anthropic", "DeepSeek", "Google"]
DEFAULT_MODELS = {
    "OpenAI": "gpt-4o",
    "Anthropic": "claude-3-5-sonnet-20241022",
    "DeepSeek": "deepseek-chat",
    "Google": "gemini-1.5-pro",
}


def render_sidebar():
    st.sidebar.title("⚙️ Settings")

    provider = st.sidebar.radio("LLM Provider", PROVIDERS, index=PROVIDERS.index(st.session_state.get("api_provider", "OpenAI")))
    api_key = st.sidebar.text_input(
        f"{provider} API Key",
        value=st.session_state.get("api_key", ""),
        type="password",
        help="Your API key is used only for this session and is never logged.",
    )

    if st.sidebar.button("💾 Save Settings"):
        st.session_state["api_provider"] = provider
        st.session_state["api_key"] = api_key
        st.sidebar.success("Settings saved!")

    if st.sidebar.button("🧪 Test Connection"):
        if not api_key:
            st.sidebar.error("Please enter an API key first.")
        else:
            with st.spinner("Testing connection..."):
                try:
                    prompt = "Return a one-word response: 'OK'"
                    response = asyncio.run(generate_content(prompt, provider, api_key))
                    if "OK" in response or len(response) > 0:
                        st.sidebar.success("Connection successful!")
                    else:
                        st.sidebar.warning("Connected, but response was unexpected.")
                except Exception as exc:
                    st.sidebar.error(f"Connection failed: {exc}")

    st.sidebar.markdown("---")
    st.sidebar.markdown("**Selected model:**")
    st.sidebar.caption(DEFAULT_MODELS.get(provider, "Unknown"))

    return provider, api_key
