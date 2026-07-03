import asyncio
import os

import httpx
import openai
import anthropic
from openai import AsyncOpenAI
from anthropic import AsyncAnthropic


SYSTEM_PROMPT = "You are a helpful marketing assistant. Return valid JSON only."

DEFAULT_MODELS = {
    "OpenAI": "gpt-4o",
    "Anthropic": "claude-3-5-sonnet-20241022",
    "DeepSeek": "deepseek-chat",
    "Google": "gemini-1.5-pro",
    "Kimi": "moonshot-v1-8k",
}

DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")
KIMI_BASE_URL = "https://api.moonshot.cn/v1"


def _is_retryable(exc: Exception) -> bool:
    """Return True if the exception warrants a retry with backoff."""
    if isinstance(exc, (openai.APIConnectionError, openai.RateLimitError)):
        return True
    if isinstance(exc, (anthropic.APIConnectionError, anthropic.RateLimitError)):
        return True
    if isinstance(exc, (httpx.TimeoutException, httpx.ConnectError)):
        return True
    if isinstance(exc, httpx.HTTPStatusError):
        return exc.response.status_code >= 500
    return False


async def _with_retries(coro_func, *args, **kwargs):
    """Run a coroutine with up to 3 attempts and exponential backoff."""
    last_exc = None
    for attempt in range(3):
        try:
            return await coro_func(*args, **kwargs)
        except Exception as exc:
            last_exc = exc
            if attempt < 2 and _is_retryable(exc):
                await asyncio.sleep(2 ** attempt)
            else:
                raise last_exc


async def call_openai(prompt: str, api_key: str, model: str = DEFAULT_MODELS["OpenAI"]) -> str:
    async def _request():
        async with AsyncOpenAI(api_key=api_key) as client:
            return await client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
            )

    try:
        response = await _with_retries(_request)
    except Exception as exc:
        raise ValueError(f"OpenAI API call failed: {exc}") from exc

    if not response.choices or not response.choices[0].message.content:
        raise ValueError("OpenAI response missing content")
    return response.choices[0].message.content


async def call_claude(prompt: str, api_key: str, model: str = DEFAULT_MODELS["Anthropic"]) -> str:
    async def _request():
        async with AsyncAnthropic(api_key=api_key) as client:
            return await client.messages.create(
                model=model,
                max_tokens=4096,
                temperature=0.7,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": prompt}],
            )

    try:
        response = await _with_retries(_request)
    except Exception as exc:
        raise ValueError(f"Anthropic API call failed: {exc}") from exc

    if not response.content:
        raise ValueError("Anthropic response missing content")
    return response.content[0].text


async def call_deepseek(prompt: str, api_key: str, model: str = DEFAULT_MODELS["DeepSeek"]) -> str:
    async def _request():
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{DEEPSEEK_BASE_URL}/chat/completions",
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                json={
                    "model": model,
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": prompt},
                    ],
                    "temperature": 0.7,
                },
            )
            response.raise_for_status()
            return response.json()

    try:
        data = await _with_retries(_request)
    except Exception as exc:
        raise ValueError(f"DeepSeek API call failed: {exc}") from exc

    if not data.get("choices"):
        raise ValueError("DeepSeek response missing choices")
    return data["choices"][0]["message"]["content"]


async def call_gemini(prompt: str, api_key: str, model: str = DEFAULT_MODELS["Google"]) -> str:
    async def _request():
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
                params={"key": api_key},
                json={
                    "contents": [{"parts": [{"text": f"Return valid JSON only.\n\n{prompt}"}]}],
                    "generationConfig": {"temperature": 0.7},
                },
            )
            response.raise_for_status()
            return response.json()

    try:
        data = await _with_retries(_request)
    except Exception as exc:
        raise ValueError(f"Gemini API call failed: {exc}") from exc

    if (
        not data.get("candidates")
        or not data["candidates"][0].get("content")
        or not data["candidates"][0]["content"].get("parts")
        or not data["candidates"][0]["content"]["parts"][0].get("text")
    ):
        raise ValueError("Gemini response missing content")
    return data["candidates"][0]["content"]["parts"][0]["text"]


async def call_kimi(prompt: str, api_key: str, model: str = DEFAULT_MODELS["Kimi"]) -> str:
    async def _request():
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{KIMI_BASE_URL}/chat/completions",
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                json={
                    "model": model,
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": prompt},
                    ],
                    "temperature": 0.7,
                },
            )
            response.raise_for_status()
            return response.json()

    try:
        data = await _with_retries(_request)
    except Exception as exc:
        raise ValueError(f"Kimi API call failed: {exc}") from exc

    if not data.get("choices"):
        raise ValueError("Kimi response missing choices")
    return data["choices"][0]["message"]["content"]


async def generate_content(
    prompt: str, provider: str, api_key: str, model: str | None = None
) -> str:
    """Dispatch prompt to the selected provider and return raw text."""
    if provider not in DEFAULT_MODELS:
        raise ValueError(f"Unknown provider: {provider}")
    model = model or DEFAULT_MODELS[provider]
    match provider:
        case "OpenAI":
            return await call_openai(prompt, api_key, model)
        case "Anthropic":
            return await call_claude(prompt, api_key, model)
        case "DeepSeek":
            return await call_deepseek(prompt, api_key, model)
        case "Google":
            return await call_gemini(prompt, api_key, model)
        case "Kimi":
            return await call_kimi(prompt, api_key, model)
        case _:
            raise ValueError(f"Unknown provider: {provider}")
