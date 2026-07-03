import pytest
from utils.session_manager import init_session, save_campaign, get_campaign, set_current_campaign


def test_init_session():
    state = {}
    init_session(state)
    assert state["api_provider"] == "OpenAI"
    assert state["api_key"] == ""
    assert state["campaigns"] == []
    assert state["current_campaign"] is None


def test_save_and_get_campaign():
    state = {"campaigns": [], "current_campaign": None}
    campaign = {"product_name": "Test"}
    save_campaign(state, campaign)
    assert len(state["campaigns"]) == 1
    assert get_campaign(state, 0)["product_name"] == "Test"


def test_set_current_campaign():
    state = {"current_campaign": None}
    campaign = {"product_name": "Test"}
    set_current_campaign(state, campaign)
    assert state["current_campaign"] == campaign
