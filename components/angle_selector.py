import streamlit as st


def render_angle_selector(angles_data: dict):
    st.header("🎯 Select Marketing Angle")

    recommended_index = angles_data.get("recommended", 0)
    angles = angles_data.get("angles", [])

    selected_index = st.session_state.get("selected_angle_index", recommended_index)

    cols = st.columns(min(len(angles), 3))
    for idx, angle in enumerate(angles):
        with cols[idx]:
            badge = "⭐ Recommended" if idx == recommended_index else ""
            if badge:
                st.success(badge)
            st.subheader(angle.get("name", f"Angle {idx + 1}"))
            st.write(angle.get("description", ""))
            st.caption(f"**Why it works:** {angle.get('rationale', '')}")
            st.progress(angle.get("conversion_potential", 5) / 10)
            st.caption(f"Conversion potential: {angle.get('conversion_potential', 5)}/10")
            if st.button("Select", key=f"select_angle_{idx}"):
                st.session_state["selected_angle_index"] = idx
                st.session_state["selected_angle"] = angle
                st.rerun()

    if "selected_angle" in st.session_state:
        st.info(f"Selected: **{st.session_state['selected_angle']['name']}**")
        return st.session_state["selected_angle"]

    return angles[recommended_index] if angles else None
