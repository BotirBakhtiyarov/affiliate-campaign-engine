from typing import Any

import httpx

GRAPH_API_BASE = "https://graph.facebook.com/v19.0"


class MetaPublisherError(Exception):
    """Raised when a Meta Marketing API call fails."""

    def __init__(self, message: str, response: dict[str, Any] | None = None):
        super().__init__(message)
        self.response = response


class MetaPublisher:
    """Minimal Meta Marketing API publisher for campaigns, ad sets, and ads.

    If access_token or ad_account_id is missing, the publisher runs in demo mode
    and returns fake IDs without making network calls.
    """

    def __init__(self, access_token: str = "", ad_account_id: str = ""):
        self.access_token = access_token.strip()
        self.ad_account_id = ad_account_id.strip().lstrip("act_")
        self._demo_counter = 0

    @property
    def demo_mode(self) -> bool:
        return not self.access_token or not self.ad_account_id

    def _next_demo_id(self) -> str:
        self._demo_counter += 1
        return f"demo_{self._demo_counter:04d}"

    def _post(self, path: str, data: dict[str, Any]) -> dict[str, Any]:
        if self.demo_mode:
            raise RuntimeError("_post should not be called in demo mode")

        url = f"{GRAPH_API_BASE}{path}"
        payload = {**data, "access_token": self.access_token}
        try:
            response = httpx.post(url, data=payload, timeout=30)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as exc:
            try:
                body = exc.response.json()
            except Exception:
                body = None
            raise MetaPublisherError(
                f"Meta API error: {exc.response.status_code}", response=body
            ) from exc
        except Exception as exc:
            raise MetaPublisherError(f"Meta API request failed: {exc}") from exc

    def create_campaign(
        self,
        name: str,
        objective: str = "OUTCOME_SALES",
        status: str = "PAUSED",
    ) -> dict[str, Any]:
        """Create a Meta campaign."""
        if self.demo_mode:
            return {"id": self._next_demo_id(), "name": name, "demo_mode": True}

        return self._post(
            f"/act_{self.ad_account_id}/campaigns",
            {
                "name": name,
                "objective": objective,
                "status": status,
                "special_ad_categories": "[]",
            },
        )

    def create_ad_set(
        self,
        campaign_id: str,
        name: str,
        daily_budget_cents: int = 2000,
        country: str = "US",
        status: str = "PAUSED",
    ) -> dict[str, Any]:
        """Create a Meta ad set under a campaign."""
        if self.demo_mode:
            return {
                "id": self._next_demo_id(),
                "campaign_id": campaign_id,
                "name": name,
                "demo_mode": True,
            }

        return self._post(
            f"/act_{self.ad_account_id}/adsets",
            {
                "name": name,
                "campaign_id": campaign_id,
                "daily_budget": daily_budget_cents,
                "billing_event": "IMPRESSIONS",
                "optimization_goal": "OFFSITE_CONVERSIONS",
                "targeting": f'{{"geo_locations":{{"countries":["{country}"]}}}}',
                "status": status,
            },
        )

    def create_ad(
        self,
        ad_set_id: str,
        name: str,
        headline: str,
        primary_text: str,
        cta: str,
        destination_url: str,
        status: str = "PAUSED",
    ) -> dict[str, Any]:
        """Create a Meta ad under an ad set."""
        if self.demo_mode:
            return {
                "id": self._next_demo_id(),
                "adset_id": ad_set_id,
                "name": name,
                "demo_mode": True,
            }

        creative = {
            "object_type": "SHARE",
            "title": headline,
            "body": primary_text,
            "call_to_action": {"type": cta.upper().replace(" ", "_")},
            "object_url": destination_url,
        }

        return self._post(
            f"/act_{self.ad_account_id}/ads",
            {
                "name": name,
                "adset_id": ad_set_id,
                "creative": creative,
                "status": status,
            },
        )
