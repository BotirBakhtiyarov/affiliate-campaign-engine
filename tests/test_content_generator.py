import json
import pytest
from unittest.mock import AsyncMock, patch
from utils.content_generator import (
    CHANNELS,
    _extract_json,
    _normalize_angle,
    _parse_json,
    analyze_angles,
    generate_channel_content,
    generate_full_campaign,
)


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


def test_normalize_angle_converts_string_to_dict():
    result = _normalize_angle("Simple Angle")
    assert result == {
        "name": "Simple Angle",
        "description": "",
        "rationale": "",
        "conversion_potential": 5,
    }


def test_normalize_angle_fills_missing_fields():
    result = _normalize_angle({"name": "Only Name"})
    assert result["name"] == "Only Name"
    assert result["description"] == ""
    assert result["rationale"] == ""
    assert result["conversion_potential"] == 5


def test_normalize_angle_keeps_existing_fields():
    result = _normalize_angle({
        "name": "N",
        "description": "D",
        "rationale": "R",
        "conversion_potential": 8,
    })
    assert result == {
        "name": "N",
        "description": "D",
        "rationale": "R",
        "conversion_potential": 8,
    }


@pytest.mark.asyncio
async def test_analyze_angles_normalizes_string_angles(tmp_path):
    prompt_dir = tmp_path / "prompts"
    prompt_dir.mkdir()
    prompt_file = prompt_dir / "angle_analyzer.json"
    prompt_file.write_text(json.dumps({
        "system": "sys",
        "template": "Brief: {product_name}",
        "output_format": {"type": "json"}
    }))

    fake_response = json.dumps({
        "recommended": 0,
        "angles": ["Angle A", "Angle B", "Angle C"],
    })

    with patch("utils.content_generator.generate_content", new=AsyncMock(return_value=fake_response)):
        result = await analyze_angles(
            {"product_name": "Widget"}, "OpenAI", "key", prompts_dir=str(prompt_dir)
        )
        assert result["recommended"] == 0
        assert len(result["angles"]) == 3
        assert all(isinstance(a, dict) for a in result["angles"])
        assert result["angles"][0]["name"] == "Angle A"


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


def test_extract_json_from_markdown_fences():
    text = 'Some text\n```json\n{"ok": true}\n```\nMore text'
    assert _extract_json(text) == '{"ok": true}'


def test_extract_json_nested_object():
    text = 'prefix {"outer": {"inner": 1}} suffix'
    assert _extract_json(text) == '{"outer": {"inner": 1}}'


def test_extract_json_no_json():
    assert _extract_json("no json here") == "no json here"


def test_parse_json_markdown_wrapped():
    text = '```json\n{"ok": true}\n```'
    assert _parse_json(text) == {"ok": True}


def test_parse_json_invalid_raises():
    with pytest.raises(ValueError, match="Could not parse JSON"):
        _parse_json("not valid json")


@pytest.mark.asyncio
async def test_generate_channel_content(tmp_path):
    prompt_dir = tmp_path / "prompts"
    prompt_dir.mkdir()
    (prompt_dir / "landing_page.json").write_text(json.dumps({
        "system": "sys",
        "template": "Brief: {product_name} Angle: {angle_name}",
        "output_format": {"type": "json"}
    }))

    fake_response = json.dumps({"headline": "Buy Now"})
    angle = {"name": "Angle X", "description": "Great angle"}
    brief = {"product_name": "Widget"}

    with patch("utils.content_generator.generate_content", new=AsyncMock(return_value=fake_response)) as mock:
        result = await generate_channel_content(
            brief, angle, "landing_page", "OpenAI", "key", prompts_dir=str(prompt_dir)
        )
        assert result["headline"] == "Buy Now"
        mock.assert_awaited_once()
        prompt_arg = mock.await_args[0][0]
        assert "Widget" in prompt_arg
        assert "Angle X" in prompt_arg


@pytest.mark.asyncio
async def test_generate_full_campaign_partial_failure(tmp_path):
    prompt_dir = tmp_path / "prompts"
    prompt_dir.mkdir()
    for name in CHANNELS:
        template = "landing_page Brief: {product_name}" if name == "landing_page" else "Brief: {product_name}"
        (prompt_dir / f"{name}.json").write_text(json.dumps({
            "system": "sys", "template": template, "output_format": {"type": "json"}
        }))

    async def side_effect(*args, **kwargs):
        if "landing_page" in args[0]:
            raise ValueError("LLM failed")
        return '{"ok": true}'

    with patch("utils.content_generator.generate_content", new=AsyncMock(side_effect=side_effect)):
        result = await generate_full_campaign(
            {"product_name": "Widget"}, {"name": "A", "description": "d"}, "OpenAI", "key", prompts_dir=str(prompt_dir)
        )
        assert result["landing_page"]["error"] == "LLM failed"
        assert result["landing_page"]["error_type"] == "ValueError"
        assert result["email_sequence"] == {"ok": True}
