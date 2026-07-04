import json
from pathlib import Path
from typing import Any

from utils.content_generator import _parse_json
from utils.llm_clients import generate_content
from utils.prompt_loader import format_prompt, get_output_schema, load_prompt


async def generate_ad_variants(
    brief: dict[str, Any],
    angle: dict[str, Any],
    provider: str,
    api_key: str,
    *,
    variant_count: int = 3,
    prompts_dir: str | Path = "prompts",
) -> list[dict[str, Any]]:
    """Generate {variant_count} ad copy variants using the configured LLM."""
    prompts_dir = Path(prompts_dir)
    prompt_path = prompts_dir / "ad_variant_generator.json"
    prompt_data = load_prompt(prompt_path)

    output_schema = get_output_schema(prompt_data) or {}
    variables = {
        "product_name": brief.get("product_name", ""),
        "description": brief.get("description", ""),
        "audience": brief.get("audience", ""),
        "angle_name": angle.get("name", ""),
        "angle_description": angle.get("description", ""),
        "price": brief.get("price", ""),
        "commission_rate": brief.get("commission_rate", ""),
        "promo_code": brief.get("promo_code", ""),
        "campaign_duration": brief.get("campaign_duration", ""),
        "variant_count": variant_count,
        "output_schema": json.dumps(output_schema, indent=2),
    }
    prompt_text = format_prompt(prompt_data["template"], **variables)
    raw = await generate_content(prompt_text, provider, api_key)

    data = _parse_json(raw)
    variants = data.get("variants", [])
    return [_normalize_variant(v) for v in variants]


def _normalize_variant(variant: Any) -> dict[str, Any]:
    if isinstance(variant, dict):
        return {
            "variant_label": variant.get("variant_label", ""),
            "headline": variant.get("headline", ""),
            "primary_text": variant.get("primary_text", ""),
            "cta": variant.get("cta", ""),
        }
    return {"variant_label": "", "headline": str(variant), "primary_text": "", "cta": ""}
