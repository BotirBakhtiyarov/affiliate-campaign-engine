import csv
import io

from utils.csv_export import generate_ads_csv


def test_generate_ads_csv_basic():
    content = {
        "ad_copies": {
            "ads": [
                {"headline": "Stay Hydrated", "primary_text": "Eco-friendly bottle.", "description": "Green", "cta": "Shop Now"},
                {"headline": "Go Green", "primary_text": "Ditch plastic today.", "description": "Eco", "cta": "Buy Now"},
            ]
        }
    }
    brief = {"product_name": "EcoSip", "campaign_duration": "14 days"}
    angle = {"name": "Sustainability"}
    csv_text = generate_ads_csv(content, brief, angle)

    reader = csv.DictReader(io.StringIO(csv_text))
    rows = list(reader)
    assert len(rows) == 2
    assert rows[0]["headline"] == "Stay Hydrated"
    assert rows[0]["primary_text"] == "Eco-friendly bottle."
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
        "ad_copies": {
            "ads": [
                {"headline": "Headline", "primary_text": "Body", "description": "Desc", "cta": "CTA"},
            ]
        }
    }
    csv_text = generate_ads_csv(content, {"product_name": "P"}, {"name": "A"}, destination_url="https://example.com?utm_source=meta")
    reader = csv.DictReader(io.StringIO(csv_text))
    rows = list(reader)
    assert rows[0]["destination_url"] == "https://example.com?utm_source=meta"
