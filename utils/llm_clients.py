import os

import httpx
from openai import AsyncOpenAI
from anthropic import AsyncAnthropic
import google.generativeai as genai


SYSTEM_PROMPT = "You are a helpful marketing assistant. Return valid JSON only."

DEFAULT_MODELS = {
    "OpenAI": "gpt-4o",
    "Anthropic": "claude-3-5-sonnet-20241022",
    "DeepSeek": "deepseek-chat",
    "Google": "gemini-1.5-pro",
}

DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")


async def call_openai(prompt: str, api_key: str, model: str = DEFAULT_MODELS["OpenAI"]) -> str:
    try:
        async with AsyncOpenAI(api_key=api_key) as client:
            response = await client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
            )
    except Exception as exc:
        raise ValueError(f"OpenAI API call failed: {exc}") from exc

    if not response.choices or not response.choices[0].message.content:
        raise ValueError("OpenAI response missing content")
    return response.choices[0].message.content


async def call_claude(prompt: str, api_key: str, model: str = DEFAULT_MODELS["Anthropic"]) -> str:
    try:
        async with AsyncAnthropic(api_key=api_key) as client:
            response = await client.messages.create(
                model=model,
                max_tokens=4096,
                temperature=0.7,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": prompt}],
            )
    except Exception as exc:
        raise ValueError(f"Anthropic API call failed: {exc}") from exc

    if not response.content:
        raise ValueError("Anthropic response missing content")
    return response.content[0].text


async def call_deepseek(prompt: str, api_key: str, model: str = DEFAULT_MODELS["DeepSeek"]) -> str:
    try:
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
            data = response.json()
    except Exception as exc:
        raise ValueError(f"DeepSeek API call failed: {exc}") from exc

    if not data.get("choices"):
        raise ValueError("DeepSeek response missing choices")
    return data["choices"][0]["message"]["content"]


async def call_gemini(prompt: str, api_key: str, model: str = DEFAULT_MODELS["Google"]) -> str:
    try:
        genai.configure(api_key=api_key)
        model_obj = genai.GenerativeModel(model)
        response = await model_obj.generate_content_async(
            f"{SYSTEM_PROMPT}\n\n{prompt}",
            generation_config={"temperature": 0.7},
        )
    except Exception as exc:
        raise ValueError(f"Gemini API call failed: {exc}") from exc

    if not response.text:
        raise ValueError("Gemini response missing text")
    return response.text


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
        case _:
            raise ValueError(f"Unknown provider: {provider}")
