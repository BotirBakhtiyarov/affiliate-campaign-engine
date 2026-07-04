import sys
from unittest.mock import MagicMock

# Mock streamlit before importing the component
st_mock = MagicMock()
sys.modules["streamlit"] = st_mock

from unittest.mock import patch

from components.export_panel import _to_markdown, render_export_panel


def test_to_markdown_uses_brief_form_keys():
    """Markdown export must read the same keys the brief form produces."""
    brief = {
        "product_name": "EcoSip",
        "description": "Eco-friendly bottle",
        "audience": "office workers",
        "unique_selling_points": "BPA-free",
        "competitor_notes": "Cheaper rivals",
        "price": "$20",
        "commission_rate": "30%",
        "promo_code": "ECO20",
        "campaign_duration": "14 days",
    }
    angle = {"name": "Sustainability", "description": "Go green"}
    campaign = {}

    markdown = _to_markdown(brief, angle, campaign)

    assert "Eco-friendly bottle" in markdown
    assert "office workers" in markdown
    assert "BPA-free" in markdown
    assert "Cheaper rivals" in markdown


def test_render_export_panel_returns_utm_url():
    """The UTM builder URL must be returned so Meta publisher can use it."""
    with patch("components.export_panel._render_utm_builder", return_value="https://example.com?utm_source=meta"):
        result = render_export_panel(
            {"product_name": "EcoSip"},
            {"name": "Sustainability"},
            {},
        )

    assert result == "https://example.com?utm_source=meta"
