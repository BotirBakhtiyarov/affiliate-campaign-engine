import csv
import io

from utils.csv_export import generate_ads_csv


def test_generate_ads_csv_basic():
    content = {
        "Ad Copies": [
            {"headline": "Stay Hydrated", "body": "Eco-friendly bottle.", "cta": "Shop Now"},
            {"headline": "Go Green", "body": "Ditch plastic today.", "cta": "Buy Now"},
        ]
    }
    brief = {"product_name": "EcoSip", "campaign_duration": "14 days"}
    angle = {"name": "Sustainability"}
    csv_text = generate_ads_csv(content, brief, angle)

    reader = csv.DictReader(io.StringIO(csv_text))
    rows = list(reader)
    assert len(rows) == 2
    assert rows[0]["headline"] == "Stay Hydrated"
    assert rows[0]["campaign_name"] == "EcoSip"
    assert "destination_url" in rows[0]


def test_generate_ads_csv_no_ad_copies():
    content = {}
    brief = {"product_name": "EcoSip"}
    angle = {"name": "Sustainability"}
    csv_text = generate_ads_csv(content, brief, angle)
    reader = csv.DictReader(io.StringIO(csv_text))
    assert list(reader) == []


def test_generate_ads_csv_includes_destination_url():
    content = {
        "Ad Copies": [
            {"headline": "Headline", "body": "Body", "cta": "CTA"},
        ]
    }
    csv_text = generate_ads_csv(content, {"product_name": "P"}, {"name": "A"}, destination_url="https://example.com?utm_source=meta")
    reader = csv.DictReader(io.StringIO(csv_text))
    rows = list(reader)
    assert rows[0]["destination_url"] == "https://example.com?utm_source=meta"
