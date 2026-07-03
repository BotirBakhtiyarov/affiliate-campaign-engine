from typing import Any

import streamlit as st


def render_angle_selector(angles_data: dict[str, Any], key_prefix: str = "angle") -> dict[str, Any] | None:
    """Render angle cards and return the selected angle dictionary."""
    st.header("🎯 Select Marketing Angle")

    angles = angles_data.get("angles", [])
    if not angles:
        st.warning("No angles available.")
        return None

    recommended_index = max(0, min(angles_data.get("recommended", 0), len(angles) - 1))
    selected_index = st.session_state.get("selected_angle_index", recommended_index)

    def _chunks(items, size):
        for i in range(0, len(items), size):
            yield items[i : i + size]

    for chunk in _chunks(list(enumerate(angles)), 3):
        cols = st.columns(len(chunk))
        for col, (idx, angle) in zip(cols, chunk):
            with col:
                if idx == recommended_index:
                    st.success("⭐ Recommended")
                elif idx == selected_index:
                    st.info("✅ Selected")

                st.subheader(angle.get("name", f"Angle {idx + 1}"))
                st.write(angle.get("description", ""))
                st.caption(f"**Why it works:** {angle.get('rationale', '')}")
                progress = max(0.0, min(1.0, angle.get("conversion_potential", 5) / 10))
                st.progress(progress)
                st.caption(f"Conversion potential: {angle.get('conversion_potential', 5)}/10")

                is_selected = idx == selected_index
                button_label = "Selected" if is_selected else "Select"
                if st.button(button_label, key=f"{key_prefix}_select_{idx}", disabled=is_selected):
                    st.session_state["selected_angle_index"] = idx
                    st.session_state["selected_angle"] = angle
                    st.rerun()

    selected = st.session_state.get("selected_angle")
    if selected:
        st.info(f"Selected: **{selected['name']}**")
        return selected

    return angles[recommended_index]
