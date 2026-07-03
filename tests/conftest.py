import pytest


@pytest.fixture
def sample_brief():
    return {
        "product_name": "Test Widget",
        "description": "A useful widget.",
        "price": "$29",
        "audience": "Small business owners",
        "commission_rate": "30%",
        "promo_code": "WIDGET30",
        "campaign_duration": "14 days",
        "unique_selling_points": "Easy setup, affordable, reliable.",
        "competitor_notes": "",
    }
