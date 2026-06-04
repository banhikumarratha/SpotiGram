"""
Gemini provider — Google Generative AI via langchain-google-genai.
Set GEMINI_API_KEY to enable. Falls back to Ollama if unavailable.
"""
import os
import time
import logging
from typing import Optional, AsyncIterator

from domain.models import AIResponse, AIProvider
from providers.base import BaseProvider

logger = logging.getLogger(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")


class GeminiProvider(BaseProvider):
    """Google Gemini via the google-generativeai SDK."""

    def __init__(self, api_key: str = GEMINI_API_KEY, model: str = GEMINI_DEFAULT_MODEL):
        self.api_key = api_key
        self.default_model = model

    async def is_available(self) -> bool:
        return bool(self.api_key)

    def _build_client(self):
        import google.generativeai as genai  # lazy import
        genai.configure(api_key=self.api_key)
        return genai

    async def complete(
        self,
        prompt: str,
        system: str = "",
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ) -> AIResponse:
        genai = self._build_client()
        model_name = model or self.default_model
        start = time.monotonic()

        full_prompt = f"{system}\n\n{prompt}" if system else prompt
        gen_model = genai.GenerativeModel(model_name)
        response = await gen_model.generate_content_async(
            full_prompt,
            generation_config={"temperature": temperature, "max_output_tokens": max_tokens},
        )
        content = response.text or ""
        return self._timed_response(content, AIProvider.GEMINI, model_name, start)

    async def stream(
        self,
        prompt: str,
        system: str = "",
        model: Optional[str] = None,
        temperature: float = 0.7,
    ) -> AsyncIterator[str]:
        genai = self._build_client()
        model_name = model or self.default_model
        full_prompt = f"{system}\n\n{prompt}" if system else prompt

        gen_model = genai.GenerativeModel(model_name)
        async for chunk in await gen_model.generate_content_async(
            full_prompt,
            generation_config={"temperature": temperature},
            stream=True,
        ):
            if chunk.text:
                yield chunk.text
