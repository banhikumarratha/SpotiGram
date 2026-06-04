"""
Grok provider — xAI API using OpenAI-compatible endpoint.
Set GROK_API_KEY to enable. Falls back to Ollama if unavailable.
"""
import os
import time
import logging
from typing import Optional, AsyncIterator

from domain.models import AIResponse, AIProvider
from providers.base import BaseProvider

logger = logging.getLogger(__name__)

GROK_API_KEY = os.getenv("GROK_API_KEY", "")
GROK_BASE_URL = os.getenv("GROK_BASE_URL", "https://api.x.ai/v1")
GROK_DEFAULT_MODEL = os.getenv("GROK_MODEL", "grok-beta")


class GrokProvider(BaseProvider):
    """xAI Grok via OpenAI-compatible API."""

    def __init__(self, api_key: str = GROK_API_KEY, model: str = GROK_DEFAULT_MODEL):
        self.api_key = api_key
        self.base_url = GROK_BASE_URL
        self.default_model = model

    async def is_available(self) -> bool:
        return bool(self.api_key)

    async def complete(
        self,
        prompt: str,
        system: str = "",
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ) -> AIResponse:
        from openai import AsyncOpenAI
        model = model or self.default_model
        start = time.monotonic()

        client = AsyncOpenAI(api_key=self.api_key, base_url=self.base_url)
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        res = await client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        content = res.choices[0].message.content or ""
        usage = {
            "prompt_tokens": res.usage.prompt_tokens if res.usage else 0,
            "completion_tokens": res.usage.completion_tokens if res.usage else 0,
        }
        return self._timed_response(content, AIProvider.GROK, model, start, usage=usage)

    async def stream(
        self,
        prompt: str,
        system: str = "",
        model: Optional[str] = None,
        temperature: float = 0.7,
    ) -> AsyncIterator[str]:
        from openai import AsyncOpenAI
        model = model or self.default_model
        client = AsyncOpenAI(api_key=self.api_key, base_url=self.base_url)

        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        async with await client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            stream=True,
        ) as stream:
            async for chunk in stream:
                delta = chunk.choices[0].delta.content
                if delta:
                    yield delta
