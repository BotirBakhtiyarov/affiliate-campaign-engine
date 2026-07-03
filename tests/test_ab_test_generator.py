import json
from unittest.mock import AsyncMock, patch

import pytest

from utils.ab_test_generator import generate_ad_variants


@pytest.mark.asyncio
async def test_generate_ad_variants_returns_list(tmp_path):
    prompt_dir = tmp_path / "prompts"
    prompt_dir.mkdir()
    prompt_file = prompt_dir / "ad_variant_generator.json"
    prompt_file.write_text(json.dumps({
        "system": "sys",
        "template": "Product: {product_name}",
        "output_format": {"type": "json"}
    }))

    fake_response = json.dumps({
        "variants": [
            {"variant_label": "A", "headline": "H1", "primary_text": "B1", "cta": "C1"},
            {"variant_label": "B", "headline": "H2", "primary_text": "B2", "cta": "C2"},
        ]
    })

    with patch("utils.ab_test_generator.generate_content", new=AsyncMock(return_value=fake_response)):
        result = await generate_ad_variants(
            {"product_name": "Widget"}, {"name": "Angle"}, "OpenAI", "key", prompts_dir=str(prompt_dir)
        )
        assert len(result) == 2
        assert result[0]["variant_label"] == "A"


@pytest.mark.asyncio
async def test_generate_ad_variants_normalizes_missing_fields(tmp_path):
    prompt_dir = tmp_path / "prompts"
    prompt_dir.mkdir()
    prompt_file = prompt_dir / "ad_variant_generator.json"
    prompt_file.write_text(json.dumps({
        "system": "sys",
        "template": "Product: {product_name}",
        "output_format": {"type": "json"}
    }))

    fake_response = json.dumps({
        "variants": [
            {"headline": "Only Headline"},
        ]
    })

    with patch("utils.ab_test_generator.generate_content", new=AsyncMock(return_value=fake_response)):
        result = await generate_ad_variants(
            {"product_name": "Widget"}, {"name": "Angle"}, "OpenAI", "key", prompts_dir=str(prompt_dir)
        )
        assert len(result) == 1
        assert result[0]["headline"] == "Only Headline"
        assert result[0]["variant_label"] == ""
