import json
from pathlib import Path


def load_prompt(path: str | Path) -> dict:
    """Load a JSON prompt template from disk."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError, PermissionError) as exc:
        raise ValueError(f"Failed to load prompt from {path}: {exc}") from exc


def format_prompt(template: str, **kwargs) -> str:
    """Substitute template variables."""
    return template.format(**kwargs)


def get_output_schema(prompt: dict) -> dict | None:
    """Return the expected output schema from a prompt, if present."""
    output_format = prompt.get("output_format")
    if isinstance(output_format, dict):
        return output_format.get("schema")
    return None
