import sys
from unittest.mock import MagicMock, patch

# Mock streamlit before importing the component
st_mock = MagicMock()
st_mock.columns.return_value = [MagicMock(), MagicMock()]
st_mock.button.return_value = True
sys.modules["streamlit"] = st_mock

from components.meta_publisher import render_meta_publisher


def test_render_meta_publisher_uses_ad_copies_structure():
    """Meta publisher must read the actual campaign ad_copies structure."""
    publisher_mock = MagicMock()
    publisher_mock.demo_mode = True
    publisher_mock.create_campaign.return_value = {"id": "demo_0001", "demo_mode": True}
    publisher_mock.create_ad_set.return_value = {"id": "demo_0002", "demo_mode": True}
    publisher_mock.create_ad.return_value = {"id": "demo_0003", "demo_mode": True}

    with patch("components.meta_publisher.MetaPublisher", return_value=publisher_mock):
        campaign = {
            "ad_copies": {
                "ads": [
                    {
                        "headline": "Stay Hydrated",
                        "primary_text": "Eco-friendly bottle.",
                        "cta": "Shop Now",
                    }
                ]
            }
        }
        brief = {
            "product_name": "EcoSip",
            "description": "Eco-friendly reusable bottle",
        }
        angle = {"name": "Sustainability"}

        render_meta_publisher(brief, angle, campaign, destination_url="https://example.com/shop")

    publisher_mock.create_campaign.assert_called_once_with("EcoSip")
    publisher_mock.create_ad.assert_called_once()
    args, kwargs = publisher_mock.create_ad.call_args
    assert kwargs["headline"] == "Stay Hydrated"
    assert kwargs["primary_text"] == "Eco-friendly bottle."
    assert kwargs["cta"] == "Shop Now"
    assert kwargs["destination_url"] == "https://example.com/shop"
