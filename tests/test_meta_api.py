from unittest.mock import MagicMock, patch

import httpx
import pytest

from utils.meta_api import GRAPH_API_BASE, MetaPublisher, MetaPublisherError


class TestMetaPublisherDemoMode:
    def test_demo_mode_when_credentials_missing(self):
        publisher = MetaPublisher()
        assert publisher.demo_mode is True

    def test_create_campaign_demo_mode(self):
        publisher = MetaPublisher()
        result = publisher.create_campaign("Test Campaign")
        assert result["id"].startswith("demo_")
        assert result["name"] == "Test Campaign"
        assert result["demo_mode"] is True

    def test_create_ad_set_demo_mode(self):
        publisher = MetaPublisher()
        campaign = publisher.create_campaign("Test Campaign")
        result = publisher.create_ad_set(campaign["id"], "Test Ad Set")
        assert result["id"].startswith("demo_")
        assert result["campaign_id"] == campaign["id"]

    def test_create_ad_demo_mode(self):
        publisher = MetaPublisher()
        campaign = publisher.create_campaign("Test Campaign")
        ad_set = publisher.create_ad_set(campaign["id"], "Test Ad Set")
        result = publisher.create_ad(
            ad_set["id"],
            "Test Ad",
            headline="Headline",
            primary_text="Body",
            cta="Shop Now",
            destination_url="https://example.com",
        )
        assert result["id"].startswith("demo_")
        assert result["adset_id"] == ad_set["id"]


class TestMetaPublisherRealMode:
    def test_real_mode_requires_both_credentials(self):
        publisher = MetaPublisher(access_token="token", ad_account_id="")
        assert publisher.demo_mode is True

        publisher = MetaPublisher(access_token="", ad_account_id="123")
        assert publisher.demo_mode is True

        publisher = MetaPublisher(access_token="token", ad_account_id="123")
        assert publisher.demo_mode is False

    @patch("utils.meta_api.httpx.post")
    def test_create_campaign_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": "1234567890", "name": "Test Campaign"}
        mock_post.return_value = mock_response

        publisher = MetaPublisher(access_token="token", ad_account_id="act_123")
        result = publisher.create_campaign("Test Campaign")

        assert result["id"] == "1234567890"
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        url = args[0]
        assert url.startswith(GRAPH_API_BASE)
        assert kwargs["data"]["access_token"] == "token"

    @patch("utils.meta_api.httpx.post")
    def test_create_ad_set_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": "0987654321", "name": "Test Ad Set"}
        mock_post.return_value = mock_response

        publisher = MetaPublisher(access_token="token", ad_account_id="123")
        result = publisher.create_ad_set("camp_123", "Test Ad Set")

        assert result["id"] == "0987654321"
        mock_post.assert_called_once()

    @patch("utils.meta_api.httpx.post")
    def test_create_ad_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": "1122334455", "name": "Test Ad"}
        mock_post.return_value = mock_response

        publisher = MetaPublisher(access_token="token", ad_account_id="123")
        result = publisher.create_ad(
            "adset_123",
            "Test Ad",
            headline="H",
            primary_text="B",
            cta="Shop Now",
            destination_url="https://example.com",
        )

        assert result["id"] == "1122334455"
        mock_post.assert_called_once()

    @patch("utils.meta_api.httpx.post")
    def test_create_campaign_raises_on_api_error(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"error": {"message": "Invalid token"}}
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Bad request", request=MagicMock(), response=mock_response
        )
        mock_post.return_value = mock_response

        publisher = MetaPublisher(access_token="token", ad_account_id="123")
        with pytest.raises(MetaPublisherError):
            publisher.create_campaign("Test Campaign")
