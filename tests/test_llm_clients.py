import pytest
from unittest.mock import AsyncMock, patch
from utils.llm_clients import DEFAULT_MODELS, generate_content


@pytest.mark.asyncio
async def test_generate_content_dispatches_to_openai():
    with patch("utils.llm_clients.call_openai", new=AsyncMock(return_value='{"ok": true}')) as mock:
        result = await generate_content("hello", "OpenAI", "fake-key")
        assert result == '{"ok": true}'
        mock.assert_awaited_once_with("hello", "fake-key", "gpt-4o")


@pytest.mark.asyncio
async def test_generate_content_raises_on_unknown_provider():
    with pytest.raises(ValueError, match="Unknown provider"):
        await generate_content("hello", "Unknown", "fake-key")


@pytest.mark.asyncio
async def test_generate_content_dispatches_to_claude():
    with patch("utils.llm_clients.call_claude", new=AsyncMock(return_value='{"ok": true}')) as mock:
        result = await generate_content("hello", "Anthropic", "fake-key")
        assert result == '{"ok": true}'
        mock.assert_awaited_once_with("hello", "fake-key", DEFAULT_MODELS["Anthropic"])


@pytest.mark.asyncio
async def test_generate_content_dispatches_to_deepseek():
    with patch("utils.llm_clients.call_deepseek", new=AsyncMock(return_value='{"ok": true}')) as mock:
        result = await generate_content("hello", "DeepSeek", "fake-key")
        assert result == '{"ok": true}'
        mock.assert_awaited_once_with("hello", "fake-key", DEFAULT_MODELS["DeepSeek"])


@pytest.mark.asyncio
async def test_generate_content_dispatches_to_gemini():
    with patch("utils.llm_clients.call_gemini", new=AsyncMock(return_value='{"ok": true}')) as mock:
        result = await generate_content("hello", "Google", "fake-key")
        assert result == '{"ok": true}'
        mock.assert_awaited_once_with("hello", "fake-key", DEFAULT_MODELS["Google"])


@pytest.mark.asyncio
async def test_generate_content_uses_custom_model():
    with patch("utils.llm_clients.call_openai", new=AsyncMock(return_value='{"ok": true}')) as mock:
        await generate_content("hello", "OpenAI", "fake-key", model="gpt-4o-mini")
        mock.assert_awaited_once_with("hello", "fake-key", "gpt-4o-mini")
