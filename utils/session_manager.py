from typing import Any


def init_session(state: dict[str, Any]) -> None:
    """Initialize default session state keys."""
    defaults = {
        "api_provider": "OpenAI",
        "api_key": "",
        "campaigns": [],
        "current_campaign": None,
    }
    for key, value in defaults.items():
        state.setdefault(key, value)


def save_campaign(state: dict[str, Any], campaign: dict) -> None:
    """Append a campaign to the campaigns list."""
    state["campaigns"].append(campaign)


def get_campaign(state: dict[str, Any], index: int) -> dict:
    """Retrieve a campaign by index."""
    return state["campaigns"][index]


def delete_campaign(state: dict[str, Any], index: int) -> None:
    """Remove a campaign by index."""
    del state["campaigns"][index]


def set_current_campaign(state: dict[str, Any], campaign: dict | None) -> None:
    """Set the active campaign."""
    state["current_campaign"] = campaign
