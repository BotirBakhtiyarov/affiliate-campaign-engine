import json
from pathlib import Path


def load_prompt(path: str | Path) -> dict:
    """Load a JSON prompt template from disk."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def format_prompt(template: str, **kwargs) -> str:
    """Substitute template variables."""
    return template.format(**kwargs)


def get_output_schema(prompt: dict) -> dict | None:
    """Return the expected output schema from a prompt, if present."""
    return prompt.get("output_format", {}).get("schema")
