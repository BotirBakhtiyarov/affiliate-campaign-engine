import httpx
from openai import AsyncOpenAI
from anthropic import AsyncAnthropic
import google.generativeai as genai


DEFAULT_MODELS = {
    "OpenAI": "gpt-4o",
    "Anthropic": "claude-3-5-sonnet-20241022",
    "DeepSeek": "deepseek-chat",
    "Google": "gemini-1.5-pro",
}


async def call_openai(prompt: str, api_key: str, model: str = DEFAULT_MODELS["OpenAI"]) -> str:
    client = AsyncOpenAI(api_key=api_key)
    response = await client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful marketing assistant. Return valid JSON only."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content


async def call_claude(prompt: str, api_key: str, model: str = DEFAULT_MODELS["Anthropic"]) -> str:
    client = AsyncAnthropic(api_key=api_key)
    response = await client.messages.create(
        model=model,
        max_tokens=4096,
        temperature=0.7,
        system="You are a helpful marketing assistant. Return valid JSON only.",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


async def call_deepseek(prompt: str, api_key: str, model: str = DEFAULT_MODELS["DeepSeek"]) -> str:
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": "You are a helpful marketing assistant. Return valid JSON only."},
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.7,
            },
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]


async def call_gemini(prompt: str, api_key: str, model: str = DEFAULT_MODELS["Google"]) -> str:
    genai.configure(api_key=api_key)
    model_obj = genai.GenerativeModel(model)
    response = await model_obj.generate_content_async(
        f"Return valid JSON only.\n\n{prompt}",
        generation_config={"temperature": 0.7},
    )
    return response.text


async def generate_content(prompt: str, provider: str, api_key: str) -> str:
    """Dispatch prompt to the selected provider and return raw text."""
    match provider:
        case "OpenAI":
            return await call_openai(prompt, api_key, DEFAULT_MODELS["OpenAI"])
        case "Anthropic":
            return await call_claude(prompt, api_key, DEFAULT_MODELS["Anthropic"])
        case "DeepSeek":
            return await call_deepseek(prompt, api_key, DEFAULT_MODELS["DeepSeek"])
        case "Google":
            return await call_gemini(prompt, api_key, DEFAULT_MODELS["Google"])
        case _:
            raise ValueError(f"Unknown provider: {provider}")
