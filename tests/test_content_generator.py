import json
import pytest
from unittest.mock import AsyncMock, patch
from utils.content_generator import analyze_angles, generate_full_campaign


@pytest.mark.asyncio
async def test_analyze_angles_parses_json(tmp_path):
    prompt_dir = tmp_path / "prompts"
    prompt_dir.mkdir()
    prompt_file = prompt_dir / "angle_analyzer.json"
    prompt_file.write_text(json.dumps({
        "system": "sys",
        "template": "Brief: {product_name}",
        "output_format": {"type": "json"}
    }))

    fake_response = json.dumps({
        "recommended": 1,
        "angles": [
            {"name": "A", "description": "desc", "rationale": "r", "conversion_potential": 7},
            {"name": "B", "description": "desc", "rationale": "r", "conversion_potential": 9},
            {"name": "C", "description": "desc", "rationale": "r", "conversion_potential": 6},
        ]
    })

    with patch("utils.content_generator.generate_content", new=AsyncMock(return_value=fake_response)) as mock:
        result = await analyze_angles(
            {"product_name": "Widget"}, "OpenAI", "key", prompts_dir=str(prompt_dir)
        )
        assert result["recommended"] == 1
        assert len(result["angles"]) == 3


@pytest.mark.asyncio
async def test_generate_full_campaign_returns_all_channels(tmp_path):
    prompt_dir = tmp_path / "prompts"
    prompt_dir.mkdir()
    for name in ["strategy_summary", "landing_page", "email_sequence", "ad_copies", "social_media", "seo_meta"]:
        (prompt_dir / f"{name}.json").write_text(json.dumps({
            "system": "sys", "template": "Brief: {product_name}", "output_format": {"type": "json"}
        }))

    fake_response = json.dumps({"ok": True})

    with patch("utils.content_generator.generate_content", new=AsyncMock(return_value=fake_response)) as mock:
        result = await generate_full_campaign(
            {"product_name": "Widget"}, "Angle", "OpenAI", "key", prompts_dir=str(prompt_dir)
        )
        assert set(result.keys()) == {"strategy_summary", "landing_page", "email_sequence", "ad_copies", "social_media", "seo_meta"}
        assert all(result[ch] == {"ok": True} for ch in result)
