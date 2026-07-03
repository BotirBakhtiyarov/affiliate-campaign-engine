import pytest
from utils.prompt_loader import load_prompt, format_prompt, get_output_schema


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


def test_get_output_schema_returns_schema():
    prompt = {"output_format": {"type": "json", "schema": {"headline": "string"}}}
    result = get_output_schema(prompt)
    assert result == {"headline": "string"}


def test_get_output_schema_returns_none_when_missing():
    result = get_output_schema({})
    assert result is None


def test_get_output_schema_returns_none_for_non_dict_output_format():
    result = get_output_schema({"output_format": "json"})
    assert result is None


def test_load_prompt_raises_on_missing_file(tmp_path):
    missing = tmp_path / "missing.json"
    with pytest.raises(ValueError, match="Failed to load prompt"):
        load_prompt(str(missing))


def test_load_prompt_raises_on_invalid_json(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text("not json")
    with pytest.raises(ValueError, match="Failed to load prompt"):
        load_prompt(str(bad))


def test_format_prompt_accepts_path_object(tmp_path):
    prompt_file = tmp_path / "test_prompt.json"
    prompt_file.write_text('{"system": "s", "template": "t", "output_format": {}}')
    result = load_prompt(prompt_file)
    assert result["system"] == "s"
