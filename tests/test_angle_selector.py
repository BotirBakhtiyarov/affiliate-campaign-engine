import sys
from unittest.mock import MagicMock
import pytest

# Mock streamlit before importing the component
st_mock = MagicMock()
st_mock.columns.return_value = [MagicMock(), MagicMock(), MagicMock()]
st_mock.session_state = {}
st_mock.header = MagicMock()
st_mock.subheader = MagicMock()
st_mock.write = MagicMock()
st_mock.caption = MagicMock()
st_mock.success = MagicMock()
st_mock.info = MagicMock()
st_mock.progress = MagicMock()
st_mock.button.return_value = False
sys.modules["streamlit"] = st_mock

from components.angle_selector import render_angle_selector


def test_render_angle_selector_handles_string_angles():
    """Angles returned as plain strings must not crash the selector."""
    angles_data = {
        "recommended": 0,
        "angles": ["Angle A", "Angle B"],
    }

    selected = render_angle_selector(angles_data)

    assert isinstance(selected, dict)
    assert selected["name"] == "Angle A"
