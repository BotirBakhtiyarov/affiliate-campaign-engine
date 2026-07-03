import pytest
from utils.prompt_loader import load_prompt, format_prompt


def test_load_prompt_returns_dict(tmp_path):
    prompt_file = tmp_path / "test_prompt.json"
    prompt_file.write_text('{"system": "sys", "template": "tpl", "output_format": {"type": "json"}}')
    result = load_prompt(str(prompt_file))
    assert result["system"] == "sys"
    assert result["template"] == "tpl"


def test_format_prompt_substitutes_variables():
    template = "Product: {product_name}, Price: {price}"
    result = format_prompt(template, product_name="Widget", price="$10")
    assert result == "Product: Widget, Price: $10"
