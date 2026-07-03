import csv
import io
from typing import Any


def generate_ads_csv(
    content: dict[str, Any],
    brief: dict[str, Any],
    angle: dict[str, Any],
    destination_url: str = "",
) -> str:
    """Generate a CSV of ad variants suitable for bulk upload to Meta/Google Ads."""
    output = io.StringIO()
    fieldnames = [
        "campaign_name",
        "ad_set_name",
        "ad_name",
        "platform",
        "headline",
        "primary_text",
        "description",
        "cta",
        "destination_url",
    ]
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()

    campaign_name = brief.get("product_name", "Campaign")
    ad_set_name = angle.get("name", "Default")
    ads = content.get("Ad Copies", [])

    for idx, ad in enumerate(ads, start=1):
        writer.writerow({
            "campaign_name": campaign_name,
            "ad_set_name": ad_set_name,
            "ad_name": f"{campaign_name} Ad {idx}",
            "platform": "Meta",
            "headline": ad.get("headline", ""),
            "primary_text": ad.get("body", ""),
            "description": ad.get("description", ""),
            "cta": ad.get("cta", ""),
            "destination_url": destination_url,
        })

    return output.getvalue()
