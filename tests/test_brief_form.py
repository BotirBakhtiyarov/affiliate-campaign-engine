import sys
from unittest.mock import MagicMock
import pytest

# Mock streamlit before importing the component
st_mock = MagicMock()
st_mock.form.return_value.__enter__ = lambda *args: None
st_mock.form.return_value.__exit__ = lambda *args: None
st_mock.columns.return_value = [MagicMock(), MagicMock()]
sys.modules["streamlit"] = st_mock

from components.brief_form import render_brief_form


def test_render_brief_form_returns_dict_and_flag():
    st_mock.text_input.return_value = "  value  "
    st_mock.text_area.return_value = "  description  "
    st_mock.form_submit_button.return_value = True

    brief, is_complete = render_brief_form()

    assert isinstance(brief, dict)
    assert brief["product_name"] == "value"
    assert brief["description"] == "description"
    assert is_complete is True
