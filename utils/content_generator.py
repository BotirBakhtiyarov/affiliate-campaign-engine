import asyncio
import json
import re
from pathlib import Path
from typing import Any

from utils.llm_clients import generate_content
from utils.prompt_loader import load_prompt, format_prompt


PROMPTS_DIR = Path(__file__).parent.parent / "prompts"
CHANNELS = [
    "strategy_summary",
    "landing_page",
    "email_sequence",
    "ad_copies",
    "social_media",
    "seo_meta",
]


def _extract_json(text: str) -> str:
    """Extract JSON from markdown fences or balanced braces/arrays."""
    fenced = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    if fenced:
        return fenced.group(1).strip()

    for opener, closer in (("{", "}"), ("[", "]")):
        start = text.find(opener)
        if start == -1:
            continue
        depth = 0
        for i, ch in enumerate(text[start:], start=start):
            if ch == opener:
                depth += 1
            elif ch == closer:
                depth -= 1
                if depth == 0:
                    return text[start : i + 1]
    return text


def _parse_json(text: str) -> Any:
    """Parse JSON from LLM response, with fallback extraction."""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        try:
            return json.loads(_extract_json(text))
        except json.JSONDecodeError as exc:
            raise ValueError(f"Could not parse JSON from response: {text[:200]}") from exc


def _build_prompt(prompt_name: str, brief: dict, angle: dict | str | None, prompts_dir: Path) -> str:
    prompt_path = prompts_dir / f"{prompt_name}.json"
    prompt_data = load_prompt(prompt_path)
    template = prompt_data["template"]
    if isinstance(angle, str):
        angle_name = angle
        angle_description = ""
    elif angle:
        angle_name = angle.get("name", "")
        angle_description = angle.get("description", "")
    else:
        angle_name = ""
        angle_description = ""
    context = {
        "product_name": brief.get("product_name", ""),
        "description": brief.get("description", ""),
        "price": brief.get("price", ""),
        "audience": brief.get("audience", ""),
        "commission_rate": brief.get("commission_rate", ""),
        "promo_code": brief.get("promo_code", ""),
        "campaign_duration": brief.get("campaign_duration", ""),
        "unique_selling_points": brief.get("unique_selling_points", ""),
        "competitor_notes": brief.get("competitor_notes", ""),
        "angle_name": angle_name,
        "angle_description": angle_description,
    }
    return format_prompt(template, **context)


async def analyze_angles(
    brief: dict, provider: str, api_key: str, prompts_dir: Path | str = PROMPTS_DIR
) -> dict:
    """Analyze brief and return 3 angles + recommendation."""
    prompts_dir = Path(prompts_dir)
    prompt_text = _build_prompt("angle_analyzer", brief, None, prompts_dir)
    raw = await generate_content(prompt_text, provider, api_key)
    return _parse_json(raw)


async def generate_channel_content(
    brief: dict, angle: dict | str, channel: str, provider: str, api_key: str, prompts_dir: Path | str = PROMPTS_DIR
) -> dict:
    """Generate content for a single channel."""
    prompts_dir = Path(prompts_dir)
    prompt_text = _build_prompt(channel, brief, angle, prompts_dir)
    raw = await generate_content(prompt_text, provider, api_key)
    return _parse_json(raw)


async def generate_full_campaign(
    brief: dict, angle: dict | str, provider: str, api_key: str, prompts_dir: Path | str = PROMPTS_DIR
) -> dict:
    """Generate all six channels in parallel."""
    prompts_dir = Path(prompts_dir)
    coroutines = [
        generate_channel_content(brief, angle, channel, provider, api_key, prompts_dir)
        for channel in CHANNELS
    ]
    results = await asyncio.gather(*coroutines, return_exceptions=True)

    campaign = {}
    for channel, result in zip(CHANNELS, results):
        if isinstance(result, Exception):
            campaign[channel] = {"error": str(result), "error_type": type(result).__name__}
        else:
            campaign[channel] = result
    return campaign
