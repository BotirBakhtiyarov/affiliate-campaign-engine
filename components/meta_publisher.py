from typing import Any

import streamlit as st

from utils.async_helpers import run_async
from utils.meta_api import MetaPublisher, MetaPublisherError


def render_meta_publisher(
    brief: dict[str, Any],
    angle: dict[str, Any] | None,
    campaign: dict[str, Any],
    destination_url: str = "",
) -> None:
    """Render the Meta Ads publisher section."""
    st.subheader("📘 Publish to Meta Ads")

    access_token = st.text_input(
        "Meta Access Token",
        value="",
        type="password",
        help="Leave blank to use demo mode (no real API call).",
        key="meta_access_token",
    )
    ad_account_id = st.text_input(
        "Ad Account ID",
        value="",
        help="Example: 1234567890 or act_1234567890. Leave blank for demo mode.",
        key="meta_ad_account_id",
    )

    col1, col2 = st.columns(2)
    with col1:
        daily_budget = st.number_input(
            "Daily Budget ($)",
            min_value=1.0,
            max_value=10000.0,
            value=20.0,
            step=5.0,
            key="meta_daily_budget",
        )
    with col2:
        country = st.selectbox(
            "Target Country",
            ["US", "CA", "GB", "AU", "DE", "FR"],
            key="meta_country",
        )

    publisher = MetaPublisher(access_token=access_token, ad_account_id=ad_account_id)

    if publisher.demo_mode:
        st.info("ℹ️ Demo mode: no real API calls will be made. Add a Meta access token and ad account ID to publish live.")

    ad_copies = campaign.get("Ad Copies", [])
    ad_copy = ad_copies[0] if ad_copies else {
        "headline": brief.get("product_name", "Ad"),
        "body": brief.get("product_description", ""),
        "cta": "Shop Now",
    }

    url = destination_url or brief.get("product_url", "")
    if not url and not publisher.demo_mode:
        st.warning("Please enter a destination URL in the UTM builder or brief to publish a live ad.")

    if st.button("📤 Publish Campaign to Meta", key="publish_meta_button"):
        with st.spinner("Publishing to Meta Ads..."):
            try:
                campaign_name = brief.get("product_name", "Campaign")
                angle_name = angle.get("name", "Default") if angle else "Default"

                created_campaign = run_async(publisher.create_campaign(campaign_name))
                created_ad_set = run_async(
                    publisher.create_ad_set(
                        campaign_id=created_campaign["id"],
                        name=f"{campaign_name} - {angle_name}",
                        daily_budget_cents=int(daily_budget * 100),
                        country=country,
                    )
                )
                created_ad = run_async(
                    publisher.create_ad(
                        ad_set_id=created_ad_set["id"],
                        name=f"{campaign_name} Ad 1",
                        headline=ad_copy.get("headline", ""),
                        primary_text=ad_copy.get("body", ""),
                        cta=ad_copy.get("cta", "Shop Now"),
                        destination_url=url or "https://example.com",
                    )
                )

                if created_campaign.get("demo_mode"):
                    st.success("Demo publish complete! In live mode, this would create campaign, ad set, and ad on Meta.")
                else:
                    st.success("Campaign published to Meta Ads!")

                st.json({
                    "campaign_id": created_campaign.get("id"),
                    "ad_set_id": created_ad_set.get("id"),
                    "ad_id": created_ad.get("id"),
                })
            except MetaPublisherError as exc:
                st.error(f"Meta publish failed: {exc}")
            except Exception as exc:
                st.error(f"Unexpected error: {exc}")
