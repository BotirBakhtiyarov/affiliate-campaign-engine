import pytest
from unittest.mock import AsyncMock, patch
from utils.llm_clients import generate_content


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
