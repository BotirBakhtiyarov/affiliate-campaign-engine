import pytest
from utils.utm_builder import build_utm_url


def test_build_utm_url_with_all_params():
    url = build_utm_url(
        "https://example.com/shop",
        utm_source="meta",
        utm_medium="paid_social",
        utm_campaign="eco_sip_14d",
        utm_content="ad_1",
        utm_term="reusable_bottle",
    )
    assert url == (
        "https://example.com/shop?utm_source=meta&utm_medium=paid_social"
        "&utm_campaign=eco_sip_14d&utm_content=ad_1&utm_term=reusable_bottle"
    )


def test_build_utm_url_ignores_empty_params():
    url = build_utm_url(
        "https://example.com/shop",
        utm_source="google",
        utm_medium="cpc",
        utm_campaign="spring_sale",
    )
    assert url == "https://example.com/shop?utm_source=google&utm_medium=cpc&utm_campaign=spring_sale"


def test_build_utm_url_adds_scheme_when_missing():
    url = build_utm_url("example.com/shop", utm_source="meta", utm_medium="paid_social", utm_campaign="test")
    assert url.startswith("https://example.com/shop?")


def test_build_utm_url_raises_on_invalid_base():
    with pytest.raises(ValueError):
        build_utm_url("https://", utm_source="meta", utm_medium="paid_social", utm_campaign="test")
